import os
from io import BytesIO

from docx import Document as DocxDocument
from pypdf import PdfReader

from ocr.models import OCRJob, OCRResult


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
    from django.utils import timezone
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
