import hashlib
import os
import re
import unicodedata
from dataclasses import dataclass

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from knowledge_base.models import DocumentChunk, KnowledgeDocument


DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 150
DEFAULT_SEARCH_LIMIT = 5
MAX_SOURCE_EXCERPT_LENGTH = 280


@dataclass
class SearchResult:
    chunk: DocumentChunk
    score: int


def normalize_text(text):
    text = (text or '').strip().lower()
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(char for char in normalized if not unicodedata.combining(char))


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


def _tokenize_query(query):
    normalized_query = normalize_text(query)
    terms = re.findall(r'[a-z0-9]+', normalized_query)
    return [term for term in terms if len(term) >= 2]


def _count_term_hits(text, terms):
    normalized_text = normalize_text(text)
    return sum(normalized_text.count(term) for term in terms)


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


@transaction.atomic
def index_document_for_knowledge_base(document, knowledge_base, user):
    organization = knowledge_base.organization
    title = _build_document_title(document)
    indexed_text, metadata = _build_document_index_text(document)
    chunks = split_text_into_chunks(indexed_text)

    if not chunks and indexed_text:
        chunks = [indexed_text]

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
            )
        )

    DocumentChunk.objects.bulk_create(chunk_models)
    knowledge_document.status = 'indexed'
    knowledge_document.indexed_at = timezone.now()
    knowledge_document.save(update_fields=['status', 'indexed_at', 'updated_at'])

    return knowledge_document, len(chunk_models)


def search_chunks(organization, query, knowledge_base=None, limit=DEFAULT_SEARCH_LIMIT):
    terms = _tokenize_query(query)
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
    ranked = []
    for chunk in candidates:
        score = _count_term_hits(chunk.content, terms)
        score += _count_term_hits(chunk.knowledge_document.title, terms)
        if score > 0:
            ranked.append(SearchResult(chunk=chunk, score=score))

    ranked.sort(
        key=lambda result: (
            -result.score,
            -result.chunk.created_at.timestamp(),
            result.chunk.chunk_index,
        )
    )
    return ranked[: max(1, min(limit or DEFAULT_SEARCH_LIMIT, 10))]


def build_grounded_answer(query, chunks):
    if not chunks:
        return {
            'query': query,
            'status': 'no_sources',
            'answer': (
                'Nao foram encontradas fontes suficientes na base de conhecimento '
                'da organizacao para responder com seguranca.'
            ),
            'sources': [],
        }

    sources = [_build_source_payload(result) for result in chunks]
    lines = ['Resposta gerada com base nos documentos encontrados na base de conhecimento:']
    for source in sources:
        lines.append(f"- {source['title']}: {source['excerpt']}")

    return {
        'query': query,
        'status': 'completed',
        'answer': '\n'.join(lines),
        'sources': sources,
    }
