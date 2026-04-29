import os
from io import BytesIO

from django.utils import timezone
from docx import Document as DocxDocument
from pypdf import PdfReader

from knowledge_base.services import index_document_for_knowledge_base
from ocr.models import OCRJob, OCRKnowledgeBasePipelineRun, OCRResult


SUPPORTED_TXT_EXTENSIONS = {'.txt'}
SUPPORTED_PDF_EXTENSIONS = {'.pdf'}
SUPPORTED_DOCX_EXTENSIONS = {'.docx'}


def detect_extraction_method(document):
    if not getattr(document, 'file', None):
        return 'unsupported'

    filename = getattr(document.file, 'name', '') or ''
    extension = os.path.splitext(filename)[1].lower()

    if extension in SUPPORTED_TXT_EXTENSIONS:
        return 'txt'
    if extension in SUPPORTED_PDF_EXTENSIONS:
        return 'pdf_text'
    if extension in SUPPORTED_DOCX_EXTENSIONS:
        return 'docx_text'
    return 'unsupported'


def _read_document_bytes(document):
    if not getattr(document, 'file', None):
        raise ValueError('Documento sem ficheiro associado.')

    document.file.open('rb')
    try:
        document.file.seek(0)
        return document.file.read()
    finally:
        document.file.close()


def extract_text_from_txt(file_bytes):
    try:
        return file_bytes.decode('utf-8').strip()
    except UnicodeDecodeError:
        return file_bytes.decode('latin-1').strip()


def extract_text_from_pdf(file_bytes):
    reader = PdfReader(BytesIO(file_bytes))
    extracted_parts = []
    for page in reader.pages:
        extracted_parts.append((page.extract_text() or '').strip())
    return '\n'.join(part for part in extracted_parts if part).strip()


def extract_text_from_docx(file_bytes):
    document = DocxDocument(BytesIO(file_bytes))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return '\n'.join(paragraphs).strip()


def update_document_content_from_ocr(document, extracted_text, user=None):
    document.content = extracted_text
    document.save(update_fields=['content', 'updated_at'])
    return document


def _build_result_metadata(document, extraction_method, extracted_text):
    return {
        'document_id': str(document.id),
        'extraction_method': extraction_method,
        'content_updated': False,
        'has_text': bool(extracted_text.strip()),
    }


def run_ocr_for_document(document, user, update_document_content=False):
    extraction_method = detect_extraction_method(document)
    job = OCRJob.objects.create(
        organization=document.organization,
        document=document,
        requested_by=user,
        status='pending',
        extraction_method=extraction_method,
    )

    job.status = 'running'
    job.started_at = timezone.now()
    job.save(update_fields=['status', 'started_at', 'updated_at'])

    try:
        if extraction_method == 'unsupported':
            raise ValueError('Formato de ficheiro nao suportado para extracao local nesta fase.')

        file_bytes = _read_document_bytes(document)
        if extraction_method == 'txt':
            extracted_text = extract_text_from_txt(file_bytes)
        elif extraction_method == 'pdf_text':
            extracted_text = extract_text_from_pdf(file_bytes)
        elif extraction_method == 'docx_text':
            extracted_text = extract_text_from_docx(file_bytes)
        else:
            raise ValueError('Metodo de extracao nao suportado.')

        if not extracted_text:
            raise ValueError('Nao foi possivel extrair texto util do documento.')

        result = OCRResult.objects.create(
            organization=document.organization,
            job=job,
            document=document,
            extracted_text=extracted_text,
            char_count=len(extracted_text),
            metadata=_build_result_metadata(document, extraction_method, extracted_text),
        )

        if update_document_content:
            update_document_content_from_ocr(document, extracted_text, user=user)
            result.metadata['content_updated'] = True
            result.save(update_fields=['metadata'])

        job.status = 'completed'
        job.finished_at = timezone.now()
        job.error_message = ''
        job.save(update_fields=['status', 'finished_at', 'error_message', 'updated_at'])
        return job, result
    except Exception as exc:
        job.status = 'failed'
        job.finished_at = timezone.now()
        job.error_message = str(exc)
        job.save(update_fields=['status', 'finished_at', 'error_message', 'updated_at'])
        return job, None


def run_ocr_to_knowledge_base_pipeline(
    document,
    knowledge_base,
    user,
    update_document_content=True,
):
    if not update_document_content:
        raise ValueError('update_document_content must be true for OCR-to-KnowledgeBase pipeline.')

    user_organization = getattr(user, 'organization', None)
    if (
        user_organization is None
        or document.organization_id != user_organization.id
        or knowledge_base.organization_id != user_organization.id
    ):
        raise ValueError('Os recursos do pipeline devem pertencer a organizacao atual.')

    pipeline_run = OCRKnowledgeBasePipelineRun.objects.create(
        organization=user_organization,
        document=document,
        knowledge_base=knowledge_base,
        status='pending',
        step='started',
        update_document_content=True,
        created_by=user,
        metadata={
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
        },
    )

    pipeline_run.status = 'running'
    pipeline_run.started_at = timezone.now()
    pipeline_run.save(update_fields=['status', 'started_at', 'updated_at'])

    try:
        pipeline_run.step = 'ocr'
        pipeline_run.save(update_fields=['step', 'updated_at'])
        ocr_job, ocr_result = run_ocr_for_document(
            document=document,
            user=user,
            update_document_content=False,
        )
        pipeline_run.ocr_job = ocr_job
        pipeline_run.ocr_result = ocr_result
        pipeline_run.metadata['ocr_job_status'] = ocr_job.status
        pipeline_run.save(update_fields=['ocr_job', 'ocr_result', 'metadata', 'updated_at'])

        if ocr_job.status != 'completed' or ocr_result is None:
            raise ValueError(ocr_job.error_message or 'OCR falhou antes da indexacao.')

        pipeline_run.step = 'apply_to_document'
        pipeline_run.save(update_fields=['step', 'updated_at'])
        update_document_content_from_ocr(document, ocr_result.extracted_text, user=user)
        ocr_result.metadata['content_updated'] = True
        ocr_result.save(update_fields=['metadata'])

        pipeline_run.step = 'index_document'
        pipeline_run.save(update_fields=['step', 'updated_at'])
        knowledge_document, chunks_created, chunks_deleted, indexing_job = index_document_for_knowledge_base(
            document=document,
            knowledge_base=knowledge_base,
            user=user,
        )
        pipeline_run.knowledge_document = knowledge_document
        pipeline_run.indexing_job = indexing_job
        pipeline_run.metadata.update(
            {
                'chunks_created': chunks_created,
                'chunks_deleted': chunks_deleted,
                'knowledge_document_status': knowledge_document.status,
            }
        )
        pipeline_run.status = 'completed'
        pipeline_run.step = 'completed'
        pipeline_run.finished_at = timezone.now()
        pipeline_run.error_message = ''
        pipeline_run.save(
            update_fields=[
                'knowledge_document',
                'indexing_job',
                'metadata',
                'status',
                'step',
                'finished_at',
                'error_message',
                'updated_at',
            ]
        )
        return pipeline_run
    except Exception as exc:
        pipeline_run.status = 'failed'
        pipeline_run.step = 'failed'
        pipeline_run.finished_at = timezone.now()
        pipeline_run.error_message = str(exc)
        pipeline_run.save(
            update_fields=['status', 'step', 'finished_at', 'error_message', 'updated_at']
        )
        return pipeline_run
