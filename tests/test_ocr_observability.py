from io import BytesIO
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from pypdf import PdfWriter

from documents.models import Document
from knowledge_base.models import DocumentChunk, KnowledgeBase
from ocr.models import OCRAuditLog, OCRJob, OCRPageResult, OCRResult, OCRSettings
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def build_upload(name, content, content_type):
    return SimpleUploadedFile(name, content, content_type=content_type)


def build_pdf_bytes():
    buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=200)
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


def create_knowledge_base(tenant, org_key='org_b', user_key='admin_b', name='Base OCR Observability'):
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
def observability_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(observability_tenant):
    return authenticated_client(observability_tenant['admin_b'])


@pytest.fixture
def client_a(observability_tenant):
    return authenticated_client(observability_tenant['admin_a'])


def build_page_output(text, page_number):
    return {
        'page_number': page_number,
        'text': text,
        'char_count': len(text),
        'status': 'completed',
        'error_message': '',
        'metadata': {'page_label': f'page-{page_number}'},
    }


def build_engine_output(page_texts, total_pages_detected=None):
    pages = [build_page_output(text, index) for index, text in enumerate(page_texts, start=1)]
    return {
        'extracted_text': '\n\n'.join(page_texts).strip(),
        'pages': pages,
        'pages_processed': len(pages),
        'pages_failed': 0,
        'total_pages_detected': total_pages_detected or len(pages),
        'pages_limit_applied': bool(total_pages_detected and total_pages_detected > len(pages)),
    }


@pytest.mark.django_db
def test_ocr_settings_accept_valid_tenant_limits(observability_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'max_scanned_pdf_pages': 7,
            'max_ocr_file_size_mb': 30,
            'max_ocr_chars_output': 12000,
            'store_page_level_ocr': True,
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['max_scanned_pdf_pages'] == 7
    assert response.data['max_ocr_file_size_mb'] == 30
    assert response.data['max_ocr_chars_output'] == 12000
    assert response.data['store_page_level_ocr'] is True


@pytest.mark.django_db
def test_ocr_settings_reject_invalid_max_scanned_pdf_pages(observability_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {'max_scanned_pdf_pages': 0},
        format='json',
    )

    assert response.status_code == 400
    assert 'max_scanned_pdf_pages' in response.data['details']


@pytest.mark.django_db
def test_ocr_settings_reject_invalid_max_ocr_file_size_mb(observability_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {'max_ocr_file_size_mb': 201},
        format='json',
    )

    assert response.status_code == 400
    assert 'max_ocr_file_size_mb' in response.data['details']


@pytest.mark.django_db
def test_scanned_pdf_ocr_creates_page_results_when_enabled(
    observability_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='page-results.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'store_page_level_ocr': True,
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            assert max_pages == 10
            return build_engine_output(
                ['Primeira pagina util.', 'Segunda pagina util.', 'Terceira pagina util.'],
                total_pages_detected=3,
            )

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    result = OCRResult.objects.get(pk=response.data['result']['id'])
    page_results = OCRPageResult.objects.filter(ocr_result=result).order_by('page_number')
    assert page_results.count() == 3
    assert page_results.first().page_number == 1
    assert result.metadata['pages_processed'] == 3
    assert result.metadata['pages_failed'] == 0
    assert result.metadata['total_pages_detected'] == 3


@pytest.mark.django_db
def test_page_results_are_filtered_by_tenant(observability_tenant, client_a, client_b, isolated_media_root, monkeypatch):
    document_b = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='tenant-b.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    document_a = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='tenant-a.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )

    for client in (client_a, client_b):
        assert client.patch(
            '/api/v1/ocr/settings/',
            {
                'advanced_ocr_enabled': True,
                'preferred_ocr_provider': 'tesseract',
                'scanned_pdf_ocr_mode': 'local',
                'store_page_level_ocr': True,
            },
            format='json',
        ).status_code == 200

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            return build_engine_output(['Pagina unica.'])

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response_a = client_a.post(f'/api/v1/ocr/documents/{document_a.id}/advanced-run/', {'mode': 'auto'}, format='json')
    response_b = client_b.post(f'/api/v1/ocr/documents/{document_b.id}/advanced-run/', {'mode': 'auto'}, format='json')

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    list_response = client_b.get('/api/v1/ocr/page-results/')
    assert list_response.status_code == 200
    assert list_response.data['count'] == 1
    assert list_response.data['results'][0]['document'] == str(document_b.id)


@pytest.mark.django_db
def test_result_pages_endpoint_does_not_expose_other_tenant(observability_tenant, client_a, client_b, isolated_media_root, monkeypatch):
    document = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='foreign-pages.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    assert client_a.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'store_page_level_ocr': True,
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            return build_engine_output(['Pagina protegida.'])

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_a.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )
    result_id = response.data['result']['id']

    detail_response = client_b.get(f'/api/v1/ocr/results/{result_id}/pages/')
    assert detail_response.status_code == 404


@pytest.mark.django_db
def test_max_scanned_pdf_pages_limits_processed_pages(observability_tenant, client_b, isolated_media_root, monkeypatch):
    document = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='page-limit.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'max_scanned_pdf_pages': 2,
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            assert max_pages == 2
            return build_engine_output(['Pagina 1.', 'Pagina 2.'], total_pages_detected=3)

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    result = OCRResult.objects.get(pk=response.data['result']['id'])
    assert result.metadata['pages_processed'] == 2
    assert result.metadata['total_pages_detected'] == 3
    assert result.metadata['pages_limit_applied'] is True
    assert OCRPageResult.objects.filter(ocr_result=result).count() == 2


@pytest.mark.django_db
def test_max_ocr_chars_output_truncates_result_and_marks_metadata(
    observability_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='truncate.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'max_ocr_chars_output': 1000,
        },
        format='json',
    ).status_code == 200

    long_text = 'A' * 1500

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            return build_engine_output([long_text])

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    result = OCRResult.objects.get(pk=response.data['result']['id'])
    assert result.char_count == 1000
    assert result.metadata['output_truncated'] is True
    assert len(result.extracted_text) == 1000


@pytest.mark.django_db
def test_file_above_max_ocr_file_size_mb_fails_safely(observability_tenant, client_b, isolated_media_root):
    content_bytes = b'X' * (2 * 1024 * 1024)
    document = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='large.pdf',
        content_bytes=content_bytes,
        content_type='application/pdf',
        content='',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'max_ocr_file_size_mb': 1,
        },
        format='json',
    ).status_code == 200

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'failed'
    assert response.data['reason'] == 'ocr_file_size_limit_exceeded'
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert audit_log.reason == 'ocr_file_size_limit_exceeded'


@pytest.mark.django_db
def test_pipeline_continues_with_scanned_pdf_metadata(observability_tenant, client_b, isolated_media_root, monkeypatch):
    document = create_document_with_file(
        tenant=observability_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='pipeline-observability.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )
    knowledge_base = create_knowledge_base(observability_tenant)
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
            'store_page_level_ocr': True,
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
            extracted_text='Texto de pagina um.\n\nTexto de pagina dois.',
            char_count=40,
            metadata={
                'content_updated': False,
                'pages_processed': 2,
                'pages_failed': 0,
                'total_pages_detected': 2,
                'output_truncated': False,
                'pages_limit_applied': False,
            },
        )
        OCRPageResult.objects.create(
            organization=document.organization,
            ocr_result=result,
            ocr_job=job,
            document=document,
            page_number=1,
            extracted_text='Texto de pagina um.',
            char_count=19,
            status='completed',
            metadata={},
        )
        OCRPageResult.objects.create(
            organization=document.organization,
            ocr_result=result,
            ocr_job=job,
            document=document,
            page_number=2,
            extracted_text='Texto de pagina dois.',
            char_count=20,
            status='completed',
            metadata={},
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
            metadata={'pages_processed': 2},
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
    assert response.data['used_advanced_ocr'] is True
    result = OCRResult.objects.get(pk=response.data['ocr_result'])
    assert result.metadata['pages_processed'] == 2
    assert OCRPageResult.objects.filter(ocr_result=result).count() == 2
    assert DocumentChunk.objects.filter(document=document, knowledge_document__knowledge_base=knowledge_base).exists()
