import hashlib
import math
import os
import re
import unicodedata
from dataclasses import dataclass

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from knowledge_base.embedding_providers import (
    LOCAL_EMBEDDING_MODEL,
    LOCAL_EMBEDDING_PROVIDER,
    get_embedding_provider,
)
from knowledge_base.models import (
    ChunkEmbedding,
    DocumentChunk,
    EmbeddingAuditLog,
    IndexingJob,
    KnowledgeDocument,
    RAGSettings,
)


DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 150
DEFAULT_SEARCH_LIMIT = 5
MAX_SOURCE_EXCERPT_LENGTH = 280
MIN_CONFIDENCE_SCORE = 4
LOCAL_RETRIEVAL_MIN_SCORE = 0.18


@dataclass
class SearchResult:
    chunk: DocumentChunk
    score: float
    exact_phrase_matches: int = 0
    terms_found: int = 0
    term_frequency: int = 0
    title_hits: int = 0
    text_score: float = 0.0
    embedding_score: float = 0.0
    final_score: float = 0.0

    def __post_init__(self):
        if self.final_score == 0 and self.score != 0:
            self.final_score = self.score
        if self.score == 0 and self.final_score != 0:
            self.score = self.final_score


def normalize_text(text):
    text = (text or '').strip().lower()
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(char for char in normalized if not unicodedata.combining(char))


def tokenize_query(query):
    normalized_query = normalize_text(query)
    terms = re.findall(r'[a-z0-9]+', normalized_query)
    return [term for term in terms if len(term) >= 2]


def split_text_into_chunks(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_CHUNK_OVERLAP):
    normalized_text = (text or '').strip()
    if not normalized_text:
        return []

    if chunk_size <= 0:
        raise ValueError('chunk_size must be positive')

    overlap = max(0, min(overlap, chunk_size - 1)) if chunk_size > 1 else 0
    start = 0
    chunks = []
    text_length = len(normalized_text)

    while start < text_length:
        end = min(text_length, start + chunk_size)
        chunk = normalized_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_length:
            break
        start = max(end - overlap, start + 1)

    return chunks


def _build_document_title(document):
    if document is None:
        return 'Documento sem titulo'

    filename = ''
    if getattr(document, 'file', None):
        filename = os.path.basename(document.file.name or '')

    case_title = getattr(getattr(document, 'law_case', None), 'title', '')
    parts = [part for part in [case_title, filename or document.type] if part]
    return ' - '.join(parts) if parts else f'Documento {document.id}'


def _build_document_index_text(document):
    content = (getattr(document, 'content', '') or '').strip()
    metadata = {
        'content_insufficient': False,
        'filename': '',
    }

    if getattr(document, 'file', None):
        metadata['filename'] = os.path.basename(document.file.name or '')

    if content:
        return content, metadata

    fallback_parts = [_build_document_title(document)]
    if metadata['filename'] and metadata['filename'] not in fallback_parts:
        fallback_parts.append(metadata['filename'])
    metadata['content_insufficient'] = True
    return ' '.join(part for part in fallback_parts if part), metadata


def _count_term_hits(text, terms):
    normalized_text = normalize_text(text)
    return sum(normalized_text.count(term) for term in terms)


def calculate_text_score(query, chunk):
    terms = tokenize_query(query)
    if not terms:
        return SearchResult(chunk=chunk, score=0)

    normalized_query = normalize_text(query)
    normalized_content = normalize_text(chunk.content)
    normalized_title = normalize_text(chunk.knowledge_document.title)

    exact_phrase_matches = normalized_content.count(normalized_query) if normalized_query else 0
    title_phrase_matches = normalized_title.count(normalized_query) if normalized_query else 0
    term_frequency = _count_term_hits(chunk.content, terms)
    title_hits = _count_term_hits(chunk.knowledge_document.title, terms)
    terms_found = sum(
        1 for term in terms if term in normalized_content or term in normalized_title
    )

    score = (
        exact_phrase_matches * 10
        + title_phrase_matches * 12
        + terms_found * 3
        + term_frequency
        + title_hits * 2
    )

    return SearchResult(
        chunk=chunk,
        score=score,
        exact_phrase_matches=exact_phrase_matches + title_phrase_matches,
        terms_found=terms_found,
        term_frequency=term_frequency,
        title_hits=title_hits,
        text_score=float(score),
        final_score=float(score),
    )


def rank_chunks(query, chunks, limit=DEFAULT_SEARCH_LIMIT):
    ranked = []
    for chunk in chunks:
        result = calculate_text_score(query, chunk)
        if result.score > 0 and result.terms_found > 0:
            ranked.append(result)

    ranked.sort(
        key=lambda result: (
            -result.score,
            -result.exact_phrase_matches,
            -result.terms_found,
            -result.term_frequency,
            -result.title_hits,
            -result.chunk.created_at.timestamp(),
            result.chunk.chunk_index,
        )
    )
    return ranked[: max(1, min(limit or DEFAULT_SEARCH_LIMIT, 10))]


def _build_source_payload(result):
    chunk = result.chunk
    excerpt = chunk.content[:MAX_SOURCE_EXCERPT_LENGTH].strip()
    payload = {
        'knowledge_document_id': str(chunk.knowledge_document_id),
        'document_id': str(chunk.document_id) if chunk.document_id else None,
        'title': chunk.knowledge_document.title,
        'chunk_id': str(chunk.id),
        'chunk_index': chunk.chunk_index,
        'excerpt': excerpt,
        'score': round(result.score, 6),
        'final_score': round(result.final_score, 6),
    }
    if result.text_score > 0:
        payload['text_score'] = round(result.text_score, 6)
    if result.embedding_score > 0:
        payload['embedding_score'] = round(result.embedding_score, 6)
    return payload


def _resolve_confidence(chunks):
    if not chunks:
        return None

    top_score = chunks[0].final_score
    sources_count = len(chunks)
    has_embedding_component = any(result.embedding_score > 0 for result in chunks)

    if has_embedding_component and top_score <= 1.5:
        if top_score >= 0.75 and sources_count >= 2:
            return 'high'
        if top_score >= 0.5:
            return 'medium'
        if top_score >= 0.3:
            return 'low'
        return None

    effective_score = chunks[0].text_score or top_score
    if effective_score >= 18 and sources_count >= 2:
        return 'high'
    if effective_score >= 8:
        return 'medium'
    if effective_score >= MIN_CONFIDENCE_SCORE:
        return 'low'
    return None


def _confidence_rank(confidence):
    return {
        'low': 1,
        'medium': 2,
        'high': 3,
    }.get(confidence, 0)


def get_rag_settings(organization):
    settings, _ = RAGSettings.objects.get_or_create(
        organization=organization,
        defaults={
            'retrieval_mode': 'textual',
            'external_embeddings_enabled': False,
            'allow_document_content_to_external_provider': False,
            'max_sources_per_answer': DEFAULT_SEARCH_LIMIT,
            'min_confidence_threshold': 'low',
        },
    )
    return settings


def _is_local_embedding_configuration(settings):
    return bool(
        settings.embedding_provider == LOCAL_EMBEDDING_PROVIDER
        and (settings.embedding_model or LOCAL_EMBEDDING_MODEL) == LOCAL_EMBEDDING_MODEL
    )


def _is_external_embedding_configuration(settings):
    return bool(settings.embedding_provider and settings.embedding_provider != LOCAL_EMBEDDING_PROVIDER)


def validate_embedding_policy(settings):
    errors = {}

    if settings.retrieval_mode in {'hybrid', 'embeddings'} and not settings.embedding_provider:
        errors['embedding_provider'] = (
            'Embedding provider e obrigatorio quando retrieval_mode e hybrid ou embeddings.'
        )

    if settings.external_embeddings_enabled and not settings.allow_document_content_to_external_provider:
        errors['external_embeddings_enabled'] = (
            'Nao e permitido ativar embeddings externos sem consentimento para '
            'envio de conteudo documental.'
        )

    max_sources = settings.max_sources_per_answer
    if max_sources < 1 or max_sources > 20:
        errors['max_sources_per_answer'] = 'Este campo deve ficar entre 1 e 20.'

    return errors


def should_use_external_embeddings(settings):
    return bool(
        _is_external_embedding_configuration(settings)
        and settings.external_embeddings_enabled
        and settings.allow_document_content_to_external_provider
    )


def should_use_local_embeddings(settings):
    return settings.retrieval_mode in {'hybrid', 'embeddings'} and _is_local_embedding_configuration(settings)


def get_effective_retrieval_mode(settings):
    if settings.retrieval_mode == 'textual':
        return 'textual'
    if should_use_local_embeddings(settings):
        return settings.retrieval_mode
    return 'textual'


def _resolve_embedding_fallback_reason(settings):
    if settings.retrieval_mode == 'textual':
        return 'retrieval_mode_textual'
    if not settings.embedding_provider:
        return 'embedding_provider_not_configured'
    if settings.embedding_provider == LOCAL_EMBEDDING_PROVIDER:
        return 'embeddings_not_prepared'
    if not settings.external_embeddings_enabled:
        return 'external_embeddings_disabled'
    if not settings.allow_document_content_to_external_provider:
        return 'external_provider_not_allowed'
    return 'provider_not_implemented'


def record_embedding_audit_log(
    *,
    organization,
    provider='',
    model='',
    action,
    status='ok',
    reason='',
    metadata=None,
    created_by=None,
    chunk=None,
    knowledge_document=None,
):
    return EmbeddingAuditLog.objects.create(
        organization=organization,
        provider=provider,
        model=model,
        action=action,
        status=status,
        reason=reason,
        metadata=metadata or {},
        created_by=created_by,
        chunk=chunk,
        knowledge_document=knowledge_document,
    )


def generate_embeddings_placeholder(
    *,
    organization,
    settings,
    knowledge_document=None,
    created_by=None,
):
    provider = settings.embedding_provider or ''
    model = settings.embedding_model or ''
    reason = _resolve_embedding_fallback_reason(settings)
    audit_log = record_embedding_audit_log(
        organization=organization,
        provider=provider,
        model=model,
        action='skipped',
        status='skipped',
        reason=reason,
        metadata={
            'retrieval_mode': settings.retrieval_mode,
            'effective_retrieval_mode': get_effective_retrieval_mode(settings),
            'external_embeddings_enabled': settings.external_embeddings_enabled,
        },
        created_by=created_by,
        knowledge_document=knowledge_document,
    )
    return {
        'status': 'skipped',
        'reason': reason,
        'provider': provider,
        'model': model,
        'chunks_processed': 0,
        'embeddings_created': 0,
        'embeddings_skipped': 0,
        'audit_log_id': str(audit_log.id),
        'effective_retrieval_mode': get_effective_retrieval_mode(settings),
    }


def _create_indexing_job(knowledge_base, user, document=None, knowledge_document=None, metadata=None):
    return IndexingJob.objects.create(
        organization=knowledge_base.organization,
        knowledge_base=knowledge_base,
        knowledge_document=knowledge_document,
        document=document,
        status='pending',
        metadata=metadata or {},
        created_by=user,
    )


def index_document_for_knowledge_base(document, knowledge_base, user, *, reindex=False):
    organization = knowledge_base.organization
    title = _build_document_title(document)
    knowledge_document, _ = KnowledgeDocument.objects.get_or_create(
        organization=organization,
        knowledge_base=knowledge_base,
        document=document,
        defaults={
            'title': title,
            'source_type': 'document',
            'status': 'pending',
            'created_by': user,
        },
    )

    job = _create_indexing_job(
        knowledge_base=knowledge_base,
        user=user,
        document=document,
        knowledge_document=knowledge_document,
        metadata={'reindex': reindex},
    )
    job.status = 'running'
    job.started_at = timezone.now()
    job.save(update_fields=['status', 'started_at', 'updated_at'])

    try:
        with transaction.atomic():
            indexed_text, metadata = _build_document_index_text(document)
            chunks = split_text_into_chunks(indexed_text)

            if not chunks and indexed_text:
                chunks = [indexed_text]

            knowledge_document.title = title
            knowledge_document.source_type = 'document'
            knowledge_document.created_by = knowledge_document.created_by or user
            knowledge_document.error_message = ''
            knowledge_document.status = 'pending'
            knowledge_document.save(
                update_fields=[
                    'title',
                    'source_type',
                    'created_by',
                    'error_message',
                    'status',
                    'updated_at',
                ]
            )

            chunks_deleted = knowledge_document.chunks.count()
            knowledge_document.chunks.all().delete()

            chunk_models = []
            for index, chunk_content in enumerate(chunks):
                chunk_metadata = {
                    **metadata,
                    'document_type': getattr(document, 'type', ''),
                    'law_case_id': str(document.law_case_id) if document.law_case_id else None,
                }
                chunk_models.append(
                    DocumentChunk(
                        organization=organization,
                        knowledge_document=knowledge_document,
                        document=document,
                        chunk_index=index,
                        content=chunk_content,
                        content_hash=hashlib.sha256(chunk_content.encode('utf-8')).hexdigest(),
                        metadata=chunk_metadata,
                        char_count=len(chunk_content),
                        embedding_status='not_generated',
                    )
                )

            DocumentChunk.objects.bulk_create(chunk_models)
            knowledge_document.status = 'indexed'
            knowledge_document.indexed_at = timezone.now()
            knowledge_document.save(update_fields=['status', 'indexed_at', 'updated_at'])

        job.status = 'completed'
        job.finished_at = timezone.now()
        job.chunks_created = len(chunk_models)
        job.chunks_deleted = chunks_deleted
        job.save(
            update_fields=[
                'status',
                'finished_at',
                'chunks_created',
                'chunks_deleted',
                'updated_at',
            ]
        )
        return knowledge_document, len(chunk_models), chunks_deleted, job
    except Exception as exc:
        knowledge_document.status = 'failed'
        knowledge_document.error_message = str(exc)
        knowledge_document.save(update_fields=['status', 'error_message', 'updated_at'])

        job.status = 'failed'
        job.finished_at = timezone.now()
        job.error_message = str(exc)
        job.save(update_fields=['status', 'finished_at', 'error_message', 'updated_at'])
        raise


def _chunk_queryset(organization, knowledge_base=None):
    queryset = DocumentChunk.objects.select_related(
        'knowledge_document',
        'document',
        'embedding',
    ).filter(
        organization=organization,
        knowledge_document__status='indexed',
    )
    if knowledge_base is not None:
        queryset = queryset.filter(knowledge_document__knowledge_base=knowledge_base)
    return queryset


def search_chunks(organization, query, knowledge_base=None, limit=DEFAULT_SEARCH_LIMIT):
    terms = tokenize_query(query)
    if not terms:
        return []

    queryset = _chunk_queryset(organization, knowledge_base=knowledge_base)
    search_filter = Q()
    for term in terms:
        search_filter |= Q(content__icontains=term)
        search_filter |= Q(knowledge_document__title__icontains=term)

    candidates = queryset.filter(search_filter)
    return rank_chunks(query, candidates, limit=limit)


def generate_local_embedding(text):
    provider = get_embedding_provider(
        type('LocalSettings', (), {'embedding_provider': LOCAL_EMBEDDING_PROVIDER, 'embedding_model': LOCAL_EMBEDDING_MODEL})()
    )
    return provider.generate_embedding(text)


def cosine_similarity(vector_a, vector_b):
    if not vector_a or not vector_b or len(vector_a) != len(vector_b):
        return 0.0

    dot_product = sum(left * right for left, right in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(value * value for value in vector_a))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def _get_existing_embedding(chunk):
    try:
        return chunk.embedding
    except ChunkEmbedding.DoesNotExist:
        return None


def generate_chunk_embeddings(knowledge_base, knowledge_document=None, user=None):
    settings = get_rag_settings(knowledge_base.organization)
    provider = get_embedding_provider(settings)

    if settings.retrieval_mode == 'textual':
        return generate_embeddings_placeholder(
            organization=knowledge_base.organization,
            settings=settings,
            knowledge_document=knowledge_document,
            created_by=user,
        )

    if provider.provider != LOCAL_EMBEDDING_PROVIDER:
        return generate_embeddings_placeholder(
            organization=knowledge_base.organization,
            settings=settings,
            knowledge_document=knowledge_document,
            created_by=user,
        )

    queryset = _chunk_queryset(knowledge_base.organization, knowledge_base=knowledge_base)
    if knowledge_document is not None:
        queryset = queryset.filter(knowledge_document=knowledge_document)

    chunks_processed = queryset.count()
    embeddings_created = 0
    embeddings_skipped = 0

    for chunk in queryset:
        existing_embedding = _get_existing_embedding(chunk)
        if (
            existing_embedding is not None
            and existing_embedding.provider == provider.provider
            and existing_embedding.model == provider.model
            and existing_embedding.status == 'generated'
            and existing_embedding.vector
        ):
            embeddings_skipped += 1
            if chunk.embedding_status != 'generated':
                chunk.embedding_status = 'generated'
                chunk.save(update_fields=['embedding_status'])
            continue

        vector = provider.generate_embedding(chunk.content)
        if existing_embedding is None:
            ChunkEmbedding.objects.create(
                organization=chunk.organization,
                chunk=chunk,
                provider=provider.provider,
                model=provider.model,
                vector=vector,
                status='generated',
            )
        else:
            existing_embedding.provider = provider.provider
            existing_embedding.model = provider.model
            existing_embedding.vector = vector
            existing_embedding.status = 'generated'
            existing_embedding.error_message = ''
            existing_embedding.save(
                update_fields=['provider', 'model', 'vector', 'status', 'error_message', 'updated_at']
            )

        chunk.embedding_status = 'generated'
        chunk.save(update_fields=['embedding_status'])
        embeddings_created += 1

    audit_log = record_embedding_audit_log(
        organization=knowledge_base.organization,
        provider=provider.provider,
        model=provider.model,
        action='completed',
        status='ok',
        reason='local_embeddings_generated',
        metadata={
            'knowledge_base_id': str(knowledge_base.id),
            'knowledge_document_id': str(knowledge_document.id) if knowledge_document else None,
            'chunks_processed': chunks_processed,
            'embeddings_created': embeddings_created,
            'embeddings_skipped': embeddings_skipped,
        },
        created_by=user,
        knowledge_document=knowledge_document,
    )

    return {
        'status': 'completed',
        'provider': provider.provider,
        'model': provider.model,
        'chunks_processed': chunks_processed,
        'embeddings_created': embeddings_created,
        'embeddings_skipped': embeddings_skipped,
        'audit_log_id': str(audit_log.id),
        'effective_retrieval_mode': get_effective_retrieval_mode(settings),
    }


def search_chunks_by_embedding(organization, query, knowledge_base=None, limit=DEFAULT_SEARCH_LIMIT):
    query_vector = generate_local_embedding(query)
    queryset = _chunk_queryset(organization, knowledge_base=knowledge_base).filter(
        embedding__status='generated',
        embedding__provider=LOCAL_EMBEDDING_PROVIDER,
        embedding__vector__isnull=False,
    )

    ranked = []
    for chunk in queryset:
        similarity = cosine_similarity(query_vector, chunk.embedding.vector or [])
        if similarity >= LOCAL_RETRIEVAL_MIN_SCORE:
            ranked.append(
                SearchResult(
                    chunk=chunk,
                    score=similarity,
                    embedding_score=similarity,
                    final_score=similarity,
                )
            )

    ranked.sort(
        key=lambda result: (
            -result.final_score,
            -result.chunk.created_at.timestamp(),
            result.chunk.chunk_index,
        )
    )
    return ranked[: max(1, min(limit or DEFAULT_SEARCH_LIMIT, 10))]


def hybrid_search_chunks(organization, query, knowledge_base=None, limit=DEFAULT_SEARCH_LIMIT):
    text_results = search_chunks(
        organization=organization,
        query=query,
        knowledge_base=knowledge_base,
        limit=max(limit, DEFAULT_SEARCH_LIMIT),
    )
    embedding_results = search_chunks_by_embedding(
        organization=organization,
        query=query,
        knowledge_base=knowledge_base,
        limit=max(limit, DEFAULT_SEARCH_LIMIT),
    )

    result_map = {}
    max_text_score = max((result.text_score for result in text_results), default=0.0)

    for result in text_results:
        result_map[str(result.chunk.id)] = SearchResult(
            chunk=result.chunk,
            score=result.score,
            exact_phrase_matches=result.exact_phrase_matches,
            terms_found=result.terms_found,
            term_frequency=result.term_frequency,
            title_hits=result.title_hits,
            text_score=result.text_score,
            embedding_score=0.0,
            final_score=0.0,
        )

    for result in embedding_results:
        key = str(result.chunk.id)
        if key not in result_map:
            result_map[key] = SearchResult(
                chunk=result.chunk,
                score=result.score,
                embedding_score=result.embedding_score,
                final_score=0.0,
            )
        else:
            result_map[key].embedding_score = result.embedding_score

    combined = []
    for result in result_map.values():
        normalized_text_score = (result.text_score / max_text_score) if max_text_score > 0 else 0.0
        result.final_score = round((normalized_text_score * 0.6) + (result.embedding_score * 0.4), 6)
        result.score = result.final_score
        if result.final_score > 0:
            combined.append(result)

    combined.sort(
        key=lambda result: (
            -result.final_score,
            -result.text_score,
            -result.embedding_score,
            -result.chunk.created_at.timestamp(),
            result.chunk.chunk_index,
        )
    )
    return combined[: max(1, min(limit or DEFAULT_SEARCH_LIMIT, 10))]


def get_retrieval_method(settings):
    if settings.retrieval_mode == 'textual':
        return 'textual'
    if should_use_local_embeddings(settings):
        return 'local_embedding' if settings.retrieval_mode == 'embeddings' else 'hybrid'
    return 'textual_fallback'


def fallback_to_textual_search(organization, query, knowledge_base=None, limit=DEFAULT_SEARCH_LIMIT):
    return search_chunks(
        organization=organization,
        query=query,
        knowledge_base=knowledge_base,
        limit=limit,
    )


def retrieve_chunks_for_query(*, organization, query, knowledge_base=None, settings=None, limit=DEFAULT_SEARCH_LIMIT):
    settings = settings or get_rag_settings(organization)
    configured_method = get_retrieval_method(settings)

    if settings.retrieval_mode == 'textual':
        return {
            'results': fallback_to_textual_search(organization, query, knowledge_base, limit),
            'retrieval_method': 'textual',
            'effective_retrieval_mode': 'textual',
            'fallback_used': False,
            'fallback_reason': None,
        }

    if should_use_local_embeddings(settings):
        if settings.retrieval_mode == 'embeddings':
            embedding_results = search_chunks_by_embedding(organization, query, knowledge_base, limit)
            if embedding_results:
                return {
                    'results': embedding_results,
                    'retrieval_method': 'local_embedding',
                    'effective_retrieval_mode': 'embeddings',
                    'fallback_used': False,
                    'fallback_reason': None,
                }
        else:
            hybrid_results = hybrid_search_chunks(organization, query, knowledge_base, limit)
            if any(result.embedding_score > 0 for result in hybrid_results):
                return {
                    'results': hybrid_results,
                    'retrieval_method': 'hybrid',
                    'effective_retrieval_mode': 'hybrid',
                    'fallback_used': False,
                    'fallback_reason': None,
                }

        return {
            'results': fallback_to_textual_search(organization, query, knowledge_base, limit),
            'retrieval_method': 'textual_fallback',
            'effective_retrieval_mode': 'textual',
            'fallback_used': True,
            'fallback_reason': 'embeddings_not_prepared',
        }

    fallback_reason = _resolve_embedding_fallback_reason(settings)
    return {
        'results': fallback_to_textual_search(organization, query, knowledge_base, limit),
        'retrieval_method': 'textual_fallback' if configured_method == 'textual_fallback' else 'textual',
        'effective_retrieval_mode': 'textual',
        'fallback_used': configured_method == 'textual_fallback',
        'fallback_reason': fallback_reason if configured_method == 'textual_fallback' else None,
    }


def build_grounded_answer(query, chunks, *, settings=None, retrieval_method='textual'):
    confidence = _resolve_confidence(chunks)
    min_threshold = getattr(settings, 'min_confidence_threshold', 'low') if settings is not None else 'low'
    threshold_rank = _confidence_rank(min_threshold)
    confidence_rank = _confidence_rank(confidence)
    meets_threshold = confidence is not None and confidence_rank >= threshold_rank
    no_sources_payload = {
        'query': query,
        'status': 'no_sources',
        'answer': (
            'Nao foram encontradas fontes suficientes na base de conhecimento '
            'da organizacao para responder com seguranca.'
        ),
        'retrieval_method': retrieval_method,
        'sources_count': 0,
        'confidence': confidence or 'low',
        'sources': [],
    }

    if not chunks or confidence is None or not meets_threshold:
        return no_sources_payload

    sources = [_build_source_payload(result) for result in chunks]
    lines = [
        'Resposta baseada nos trechos encontrados na base de conhecimento da organizacao.',
    ]
    for source in sources:
        lines.append(f"- {source['title']}: {source['excerpt']}")

    return {
        'query': query,
        'status': 'completed',
        'answer': '\n'.join(lines),
        'retrieval_method': retrieval_method,
        'sources_count': len(sources),
        'confidence': confidence,
        'sources': sources,
    }


def resolve_retrieval_behavior(settings):
    effective_mode = get_effective_retrieval_mode(settings)
    configured_mode = settings.retrieval_mode
    fallback_used = configured_mode != effective_mode
    fallback_reason = None

    if fallback_used:
        fallback_reason = _resolve_embedding_fallback_reason(settings)

    return {
        'effective_retrieval_mode': effective_mode,
        'fallback_used': fallback_used,
        'fallback_reason': fallback_reason,
    }
