from io import BytesIO
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from documents.models import Document
from knowledge_base.models import DocumentChunk, KnowledgeBase, KnowledgeDocument
from ocr.local_engines import LocalOCREngineUnavailable, PDFRasterizationUnavailable
from ocr.models import OCRAuditLog, OCRJob, OCRKnowledgeBasePipelineRun, OCRResult
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def build_upload(name, content, content_type):
    return SimpleUploadedFile(name, content, content_type=content_type)


def build_pdf_bytes(text=''):
    buffer = BytesIO()
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=200)
    if text:
        font = writer._add_object(
            DictionaryObject(
                {
                    NameObject('/Type'): NameObject('/Font'),
                    NameObject('/Subtype'): NameObject('/Type1'),
                    NameObject('/BaseFont'): NameObject('/Helvetica'),
                }
            )
        )
        page[NameObject('/Resources')] = DictionaryObject(
            {NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})}
        )
        safe_text = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        content_stream = DecodedStreamObject()
        content_stream.set_data(
            f'BT\n/F1 12 Tf\n72 120 Td\n({safe_text}) Tj\nET'.encode('latin-1', errors='ignore')
        )
        page[NameObject('/Contents')] = writer._add_object(content_stream)
    writer.write(buffer)
    return buffer.getvalue()


def create_document_with_file(*, tenant, organization_key, case_key, filename, content_bytes, content_type, content=''):
    law_case = tenant[case_key]
    return Document.objects.create(
        law_case=law_case,
        organization=tenant[organization_key],
        type='internal',
        content=content,
        file=build_upload(filename, content_bytes, content_type),
        version=Document.objects.filter(law_case=law_case).count() + 1,
    )


def create_knowledge_base(tenant, org_key='org_b', user_key='admin_b', name='Base Scanned OCR Pipeline'):
    return KnowledgeBase.objects.create(
        organization=tenant[org_key],
        name=name,
        created_by=tenant[user_key],
    )


@pytest.fixture
def isolated_media_root():
    with tempfile.TemporaryDirectory() as tmpdir:
        with override_settings(MEDIA_ROOT=tmpdir):
            yield tmpdir


@pytest.fixture
def pipeline_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(pipeline_tenant):
    return authenticated_client(pipeline_tenant['admin_b'])


@pytest.fixture
def client_a(pipeline_tenant):
    return authenticated_client(pipeline_tenant['admin_a'])


@pytest.mark.django_db
def test_pipeline_with_textual_pdf_keeps_standard_ocr_flow(pipeline_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='textual-pipeline.pdf',
        content_bytes=build_pdf_bytes('Texto juridico suficiente para OCR textual e indexacao.'),
        content_type='application/pdf',
        content='antes',
    )
    knowledge_base = create_knowledge_base(pipeline_tenant)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['used_advanced_ocr'] is False
    assert response.data['advanced_ocr_reason'] == ''


@pytest.mark.django_db
def test_pipeline_with_scanned_pdf_uses_local_advanced_ocr_when_enabled(
    pipeline_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scanned-pipeline.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    knowledge_base = create_knowledge_base(pipeline_tenant)
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
        },
        format='json',
    ).status_code == 200

    service_module = __import__('ocr.services', fromlist=['run_ocr_for_document'])

    def empty_standard_ocr(document, user, update_document_content=False):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='pdf_text',
            error_message='Nao foi possivel extrair texto util do documento.',
        )
        return job, None

    def scanned_pdf_success(document, user):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='completed',
            extraction_method='scanned_pdf_local',
        )
        result = OCRResult.objects.create(
            organization=document.organization,
            job=job,
            document=document,
            extracted_text='Texto extraido do PDF escaneado com conteudo suficiente para indexacao.',
            char_count=70,
            metadata={'content_updated': False},
        )
        audit_log = OCRAuditLog.objects.create(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='completed',
            provider='tesseract',
            mode='local',
            status='ok',
            reason='local_scanned_pdf_ocr_completed',
            metadata={'target_type': 'scanned_pdf'},
            created_by=user,
        )
        return {
            'status': 'completed',
            'reason': 'local_scanned_pdf_ocr_completed',
            'job': job,
            'result': result,
            'audit_log': audit_log,
        }

    monkeypatch.setattr(service_module, 'run_ocr_for_document', empty_standard_ocr)
    monkeypatch.setattr(service_module, 'run_local_scanned_pdf_ocr', scanned_pdf_success)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['used_advanced_ocr'] is True
    assert response.data['advanced_ocr_reason'] == 'standard_pdf_text_extraction_empty'
    assert response.data['ocr_audit_log'] is not None
    document.refresh_from_db()
    assert document.content == 'Texto extraido do PDF escaneado com conteudo suficiente para indexacao.'
    assert KnowledgeDocument.objects.filter(document=document, knowledge_base=knowledge_base).exists()
    assert DocumentChunk.objects.filter(document=document, knowledge_document__knowledge_base=knowledge_base).exists()

    ask_response = client_b.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Qual texto foi extraido do PDF escaneado?', 'limit': 5},
        format='json',
    )
    assert ask_response.status_code == 200
    assert ask_response.data['sources']
    assert any(source['document_id'] == str(document.id) for source in ask_response.data['sources'])


@pytest.mark.django_db
def test_pipeline_fails_if_scanned_pdf_mode_is_not_local(
    pipeline_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scanned-disabled.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    knowledge_base = create_knowledge_base(pipeline_tenant)

    service_module = __import__('ocr.services', fromlist=['run_ocr_for_document'])

    def empty_standard_ocr(document, user, update_document_content=False):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='pdf_text',
            error_message='Nao foi possivel extrair texto util do documento.',
        )
        return job, None

    monkeypatch.setattr(service_module, 'run_ocr_for_document', empty_standard_ocr)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 400
    assert response.data['status'] == 'failed'
    assert 'nao esta habilitado' in response.data['error_message']


@pytest.mark.django_db
def test_pipeline_fails_cleanly_when_pdf_rasterization_is_unavailable(
    pipeline_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scanned-poppler.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    knowledge_base = create_knowledge_base(pipeline_tenant)
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
        },
        format='json',
    ).status_code == 200

    service_module = __import__('ocr.services', fromlist=['run_ocr_for_document'])

    def empty_standard_ocr(document, user, update_document_content=False):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='pdf_text',
            error_message='Nao foi possivel extrair texto util do documento.',
        )
        return job, None

    def advanced_fail(document, user):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='scanned_pdf_local',
            error_message='poppler_not_available',
        )
        audit_log = OCRAuditLog.objects.create(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='failed',
            provider='tesseract',
            mode='local',
            status='failed',
            reason='pdf_rasterization_unavailable',
            metadata={'engine_reason': 'poppler_not_available'},
            created_by=user,
        )
        return {
            'status': 'failed',
            'reason': 'pdf_rasterization_unavailable',
            'job': job,
            'result': None,
            'audit_log': audit_log,
        }

    monkeypatch.setattr(service_module, 'run_ocr_for_document', empty_standard_ocr)
    monkeypatch.setattr(service_module, 'run_local_scanned_pdf_ocr', advanced_fail)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 400
    assert response.data['status'] == 'failed'
    assert response.data['used_advanced_ocr'] is True
    assert response.data['ocr_audit_log'] is not None
    assert 'poppler_not_available' in response.data['error_message']


@pytest.mark.django_db
def test_pipeline_fails_cleanly_when_tesseract_is_unavailable(
    pipeline_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scanned-tesseract.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    knowledge_base = create_knowledge_base(pipeline_tenant)
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
        },
        format='json',
    ).status_code == 200

    service_module = __import__('ocr.services', fromlist=['run_ocr_for_document'])

    def empty_standard_ocr(document, user, update_document_content=False):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='pdf_text',
            error_message='Nao foi possivel extrair texto util do documento.',
        )
        return job, None

    def advanced_fail(document, user):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='scanned_pdf_local',
            error_message='tesseract_binary_not_available',
        )
        audit_log = OCRAuditLog.objects.create(
            organization=document.organization,
            document=document,
            ocr_job=job,
            action='failed',
            provider='tesseract',
            mode='local',
            status='failed',
            reason='local_ocr_engine_unavailable',
            metadata={'engine_reason': 'tesseract_binary_not_available'},
            created_by=user,
        )
        return {
            'status': 'failed',
            'reason': 'local_ocr_engine_unavailable',
            'job': job,
            'result': None,
            'audit_log': audit_log,
        }

    monkeypatch.setattr(service_module, 'run_ocr_for_document', empty_standard_ocr)
    monkeypatch.setattr(service_module, 'run_local_scanned_pdf_ocr', advanced_fail)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 400
    assert response.data['status'] == 'failed'
    assert response.data['used_advanced_ocr'] is True
    assert 'tesseract_binary_not_available' in response.data['error_message']


@pytest.mark.django_db
def test_pipeline_still_blocks_cross_tenant_document_for_scanned_pdf(
    pipeline_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=pipeline_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='foreign-scanned.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    knowledge_base = create_knowledge_base(pipeline_tenant)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 400
    assert OCRKnowledgeBasePipelineRun.objects.count() == 0
