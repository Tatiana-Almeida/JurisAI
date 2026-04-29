import os
from io import BytesIO

from django.utils import timezone
from docx import Document as DocxDocument
from pypdf import PdfReader

from knowledge_base.services import index_document_for_knowledge_base
from ocr.local_engines import LocalOCREngineUnavailable, get_local_ocr_engine
from ocr.models import (
    OCRAuditLog,
    OCRJob,
    OCRKnowledgeBasePipelineRun,
    OCRResult,
    OCRSettings,
)


SUPPORTED_TXT_EXTENSIONS = {'.txt'}
SUPPORTED_PDF_EXTENSIONS = {'.pdf'}
SUPPORTED_DOCX_EXTENSIONS = {'.docx'}
SUPPORTED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}


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


def _document_extension(document):
    if not getattr(document, 'file', None):
        return ''
    filename = getattr(document.file, 'name', '') or ''
    return os.path.splitext(filename)[1].lower()


def get_ocr_settings(organization):
    settings, _ = OCRSettings.objects.get_or_create(
        organization=organization,
        defaults={
            'advanced_ocr_enabled': False,
            'external_ocr_enabled': False,
            'allow_document_content_to_external_ocr_provider': False,
            'preferred_ocr_provider': 'local',
            'preferred_ocr_model': '',
            'image_ocr_mode': 'disabled',
            'scanned_pdf_ocr_mode': 'disabled',
            'require_human_review': True,
        },
    )
    return settings


def validate_ocr_provider_policy(settings):
    errors = {}

    if settings.external_ocr_enabled and not settings.allow_document_content_to_external_ocr_provider:
        errors['external_ocr_enabled'] = (
            'Nao e permitido ativar OCR externo sem consentimento para envio de conteudo documental.'
        )

    if settings.image_ocr_mode == 'external' and not settings.external_ocr_enabled:
        errors['image_ocr_mode'] = 'OCR externo deve estar ativado para image_ocr_mode=external.'

    if settings.scanned_pdf_ocr_mode == 'external' and not settings.external_ocr_enabled:
        errors['scanned_pdf_ocr_mode'] = 'OCR externo deve estar ativado para scanned_pdf_ocr_mode=external.'

    return errors


def should_use_external_ocr(settings):
    return bool(
        settings.external_ocr_enabled
        and settings.allow_document_content_to_external_ocr_provider
        and settings.preferred_ocr_provider not in {'', 'local', 'tesseract'}
    )


def record_ocr_audit_log(
    *,
    organization,
    action,
    provider='',
    mode='',
    status='ok',
    reason='',
    metadata=None,
    created_by=None,
    document=None,
    ocr_job=None,
):
    return OCRAuditLog.objects.create(
        organization=organization,
        document=document,
        ocr_job=ocr_job,
        action=action,
        provider=provider,
        mode=mode,
        status=status,
        reason=reason,
        metadata=metadata or {},
        created_by=created_by,
    )


def detect_scanned_pdf_candidate(document):
    return _document_extension(document) in SUPPORTED_PDF_EXTENSIONS and not (document.content or '').strip()


def detect_image_document(document):
    return _document_extension(document) in SUPPORTED_IMAGE_EXTENSIONS


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


def _build_advanced_ocr_failure_job(document, user, reason):
    job = OCRJob.objects.create(
        organization=document.organization,
        document=document,
        requested_by=user,
        status='pending',
        extraction_method='unsupported',
    )
    job.status = 'failed'
    job.started_at = timezone.now()
    job.finished_at = timezone.now()
    job.error_message = reason
    job.save(update_fields=['status', 'started_at', 'finished_at', 'error_message', 'updated_at'])
    return job


def _create_advanced_ocr_job(document, user, extraction_method):
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
    return job


def _fail_advanced_ocr_job(job, reason):
    job.status = 'failed'
    job.finished_at = timezone.now()
    job.error_message = reason
    job.save(update_fields=['status', 'finished_at', 'error_message', 'updated_at'])
    return job


def _complete_advanced_ocr_job(job):
    job.status = 'completed'
    job.finished_at = timezone.now()
    job.error_message = ''
    job.save(update_fields=['status', 'finished_at', 'error_message', 'updated_at'])
    return job


def run_local_image_ocr(document, user):
    settings = get_ocr_settings(document.organization)
    provider = settings.preferred_ocr_provider or 'local'
    metadata = {
        'document_id': str(document.id),
        'advanced_ocr_enabled': settings.advanced_ocr_enabled,
        'configured_mode': settings.image_ocr_mode,
        'provider': provider,
        'target_type': 'image',
    }

    job = _create_advanced_ocr_job(document, user, 'image_local')

    try:
        file_bytes = _read_document_bytes(document)
        engine = get_local_ocr_engine(settings)
        extracted_text = engine.extract_text_from_image(file_bytes)
        if not extracted_text:
            raise LocalOCREngineUnavailable('local_image_ocr_no_text')

        result = OCRResult.objects.create(
            organization=document.organization,
            job=job,
            document=document,
            extracted_text=extracted_text,
            char_count=len(extracted_text),
            metadata={
                **_build_result_metadata(document, 'image_local', extracted_text),
                'provider': getattr(engine, 'provider', provider),
                'model': getattr(engine, 'model', settings.preferred_ocr_model or ''),
                'target_type': 'image',
            },
        )
        _complete_advanced_ocr_job(job)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='completed',
            provider=getattr(engine, 'provider', provider),
            mode=settings.image_ocr_mode,
            status='ok',
            reason='local_image_ocr_completed',
            metadata={**metadata, 'char_count': result.char_count},
            created_by=user,
        )
        return {
            'status': 'completed',
            'reason': 'local_image_ocr_completed',
            'job': job,
            'result': result,
            'audit_log': audit_log,
        }
    except LocalOCREngineUnavailable as exc:
        reason = str(exc)
        _fail_advanced_ocr_job(job, reason)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='failed',
            provider=provider,
            mode=settings.image_ocr_mode,
            status='failed',
            reason='local_ocr_engine_unavailable',
            metadata={**metadata, 'engine_reason': reason},
            created_by=user,
        )
        return {
            'status': 'failed',
            'reason': 'local_ocr_engine_unavailable',
            'job': job,
            'result': None,
            'audit_log': audit_log,
        }
    except Exception as exc:
        reason = str(exc)
        _fail_advanced_ocr_job(job, reason)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='failed',
            provider=provider,
            mode=settings.image_ocr_mode,
            status='failed',
            reason='local_image_ocr_failed',
            metadata={**metadata, 'engine_reason': reason},
            created_by=user,
        )
        return {
            'status': 'failed',
            'reason': 'local_image_ocr_failed',
            'job': job,
            'result': None,
            'audit_log': audit_log,
        }


def run_local_scanned_pdf_ocr(document, user):
    settings = get_ocr_settings(document.organization)
    provider = settings.preferred_ocr_provider or 'local'
    reason = 'scanned_pdf_local_ocr_not_implemented'
    job = _build_advanced_ocr_failure_job(document, user, reason)
    audit_log = record_ocr_audit_log(
        organization=document.organization,
        document=document,
        ocr_job=job,
        action='skipped',
        provider=provider,
        mode=settings.scanned_pdf_ocr_mode,
        status='skipped',
        reason=reason,
        metadata={
            'document_id': str(document.id),
            'target_type': 'scanned_pdf',
            'configured_mode': settings.scanned_pdf_ocr_mode,
        },
        created_by=user,
    )
    return {'status': 'skipped', 'reason': reason, 'job': job, 'result': None, 'audit_log': audit_log}


def run_advanced_ocr(document, user, mode='auto'):
    settings = get_ocr_settings(document.organization)
    provider = settings.preferred_ocr_provider or 'local'

    if detect_image_document(document):
        target_type = 'image'
        configured_mode = settings.image_ocr_mode
    elif detect_scanned_pdf_candidate(document):
        target_type = 'scanned_pdf'
        configured_mode = settings.scanned_pdf_ocr_mode
    else:
        target_type = 'unsupported_target'
        configured_mode = 'disabled'

    metadata = {
        'document_id': str(document.id),
        'requested_mode': mode,
        'configured_mode': configured_mode,
        'target_type': target_type,
        'advanced_ocr_enabled': settings.advanced_ocr_enabled,
        'external_ocr_enabled': settings.external_ocr_enabled,
    }

    if target_type == 'unsupported_target':
        reason = 'advanced_ocr_not_required'
        job = _build_advanced_ocr_failure_job(document, user, reason)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='skipped',
            provider=provider,
            mode=configured_mode,
            status='skipped',
            reason=reason,
            metadata=metadata,
            created_by=user,
        )
        return {'status': 'skipped', 'reason': reason, 'job': job, 'result': None, 'audit_log': audit_log}

    if not settings.advanced_ocr_enabled or configured_mode == 'disabled':
        reason = 'advanced_ocr_disabled'
        job = _build_advanced_ocr_failure_job(document, user, reason)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='skipped',
            provider=provider,
            mode=configured_mode,
            status='skipped',
            reason=reason,
            metadata=metadata,
            created_by=user,
        )
        return {'status': 'skipped', 'reason': reason, 'job': job, 'result': None, 'audit_log': audit_log}

    if configured_mode == 'local_placeholder':
        reason = (
            'scanned_pdf_local_ocr_not_implemented'
            if target_type == 'scanned_pdf'
            else 'local_image_ocr_not_implemented'
        )
        job = _build_advanced_ocr_failure_job(document, user, reason)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='skipped',
            provider=provider,
            mode=configured_mode,
            status='skipped',
            reason=reason,
            metadata=metadata,
            created_by=user,
        )
        return {'status': 'skipped', 'reason': reason, 'job': job, 'result': None, 'audit_log': audit_log}

    if configured_mode == 'external':
        reason = 'external_ocr_not_allowed' if not should_use_external_ocr(settings) else 'external_ocr_not_implemented'
        job = _build_advanced_ocr_failure_job(document, user, reason)
        audit_log = record_ocr_audit_log(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='skipped',
            provider=provider,
            mode=configured_mode,
            status='skipped',
            reason=reason,
            metadata=metadata,
            created_by=user,
        )
        return {'status': 'skipped', 'reason': reason, 'job': job, 'result': None, 'audit_log': audit_log}

    if configured_mode == 'local':
        if target_type == 'image':
            return run_local_image_ocr(document, user)
        if target_type == 'scanned_pdf':
            return run_local_scanned_pdf_ocr(document, user)

    reason = 'advanced_ocr_not_implemented'
    job = _build_advanced_ocr_failure_job(document, user, reason)
    audit_log = record_ocr_audit_log(
        organization=document.organization,
        document=document,
        ocr_job=job,
        action='skipped',
        provider=provider,
        mode=configured_mode,
        status='skipped',
        reason=reason,
        metadata=metadata,
        created_by=user,
    )
    return {'status': 'skipped', 'reason': reason, 'job': job, 'result': None, 'audit_log': audit_log}


def run_advanced_ocr_placeholder(document, user, mode='auto'):
    return run_advanced_ocr(document=document, user=user, mode=mode)
