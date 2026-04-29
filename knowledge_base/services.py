import hashlib
import os
import re
import unicodedata
from dataclasses import dataclass

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from knowledge_base.models import (
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


@dataclass
class SearchResult:
    chunk: DocumentChunk
    score: float
    exact_phrase_matches: int
    terms_found: int
    term_frequency: int
    title_hits: int


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
        return SearchResult(
            chunk=chunk,
            score=0,
            exact_phrase_matches=0,
            terms_found=0,
            term_frequency=0,
            title_hits=0,
        )

    normalized_query = normalize_text(query)
    normalized_content = normalize_text(chunk.content)
    normalized_title = normalize_text(chunk.knowledge_document.title)

    exact_phrase_matches = normalized_content.count(normalized_query) if normalized_query else 0
    title_phrase_matches = normalized_title.count(normalized_query) if normalized_query else 0
    term_frequency = _count_term_hits(chunk.content, terms)
    title_hits = _count_term_hits(chunk.knowledge_document.title, terms)
    terms_found = sum(
        1
        for term in terms
        if term in normalized_content or term in normalized_title
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
    return {
        'knowledge_document_id': str(chunk.knowledge_document_id),
        'document_id': str(chunk.document_id) if chunk.document_id else None,
        'title': chunk.knowledge_document.title,
        'chunk_id': str(chunk.id),
        'chunk_index': chunk.chunk_index,
        'excerpt': excerpt,
        'score': result.score,
    }


def _resolve_confidence(chunks):
    if not chunks:
        return None

    top_score = chunks[0].score
    sources_count = len(chunks)

    if top_score >= 18 and sources_count >= 2:
        return 'high'
    if top_score >= 8:
        return 'medium'
    if top_score >= MIN_CONFIDENCE_SCORE:
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


def validate_embedding_policy(settings):
    errors = {}
    if settings.external_embeddings_enabled and not settings.allow_document_content_to_external_provider:
        errors['external_embeddings_enabled'] = (
            'Nao e permitido ativar embeddings externos sem consentimento para '
            'envio de conteudo documental.'
        )

    if settings.retrieval_mode in {'hybrid', 'embeddings'} and not settings.embedding_provider:
        errors['embedding_provider'] = (
            'Embedding provider e obrigatorio quando retrieval_mode e hybrid ou embeddings.'
        )

    max_sources = settings.max_sources_per_answer
    if max_sources < 1 or max_sources > 20:
        errors['max_sources_per_answer'] = 'Este campo deve ficar entre 1 e 20.'

    return errors


def should_use_external_embeddings(settings):
    return bool(
        settings.external_embeddings_enabled
        and settings.allow_document_content_to_external_provider
        and settings.embedding_provider
    )


def get_effective_retrieval_mode(settings):
    if settings.retrieval_mode == 'textual':
        return 'textual'
    if should_use_external_embeddings(settings):
        return 'textual'
    return 'textual'


def _resolve_embedding_fallback_reason(settings):
    if not settings.external_embeddings_enabled:
        return 'external_embeddings_disabled'
    if not settings.allow_document_content_to_external_provider:
        return 'external_provider_not_allowed'
    if not settings.embedding_provider:
        return 'embedding_provider_not_configured'
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
        'audit_log_id': str(audit_log.id),
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

            chunks_deleted, _ = knowledge_document.chunks.all().delete()

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


def search_chunks(organization, query, knowledge_base=None, limit=DEFAULT_SEARCH_LIMIT):
    terms = tokenize_query(query)
    if not terms:
        return []

    queryset = DocumentChunk.objects.select_related(
        'knowledge_document',
        'document',
    ).filter(
        organization=organization,
        knowledge_document__status='indexed',
    )

    if knowledge_base is not None:
        queryset = queryset.filter(knowledge_document__knowledge_base=knowledge_base)

    search_filter = Q()
    for term in terms:
        search_filter |= Q(content__icontains=term)
        search_filter |= Q(knowledge_document__title__icontains=term)

    candidates = queryset.filter(search_filter)
    return rank_chunks(query, candidates, limit=limit)


def build_grounded_answer(query, chunks, *, settings=None):
    confidence = _resolve_confidence(chunks)
    min_threshold = getattr(settings, 'min_confidence_threshold', 'low') if settings is not None else 'low'
    threshold_rank = _confidence_rank(min_threshold)
    confidence_rank = _confidence_rank(confidence)
    meets_threshold = confidence is not None and confidence_rank >= threshold_rank
    if not chunks or confidence is None:
        return {
            'query': query,
            'status': 'no_sources',
            'answer': (
                'Nao foram encontradas fontes suficientes na base de conhecimento '
                'da organizacao para responder com seguranca.'
            ),
            'retrieval_method': 'textual',
            'sources_count': 0,
            'confidence': 'low',
            'sources': [],
        }

    if not meets_threshold:
        return {
            'query': query,
            'status': 'no_sources',
            'answer': (
                'Nao foram encontradas fontes suficientes na base de conhecimento '
                'da organizacao para responder com seguranca.'
            ),
            'retrieval_method': 'textual',
            'sources_count': 0,
            'confidence': confidence or 'low',
            'sources': [],
        }

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
        'retrieval_method': 'textual',
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
