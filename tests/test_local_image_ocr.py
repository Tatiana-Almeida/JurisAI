from io import BytesIO
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image

from documents.models import Document
from ocr.local_engines import LocalOCREngineUnavailable
from ocr.models import OCRAuditLog, OCRJob, OCRResult
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def build_upload(name, content, content_type):
    return SimpleUploadedFile(name, content, content_type=content_type)


def build_png_bytes():
    buffer = BytesIO()
    image = Image.new('RGB', (32, 32), color='white')
    image.save(buffer, format='PNG')
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


@pytest.fixture
def isolated_media_root():
    with tempfile.TemporaryDirectory() as tmpdir:
        with override_settings(MEDIA_ROOT=tmpdir):
            yield tmpdir


@pytest.fixture
def local_ocr_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(local_ocr_tenant):
    return authenticated_client(local_ocr_tenant['admin_b'])


@pytest.fixture
def client_a(local_ocr_tenant):
    return authenticated_client(local_ocr_tenant['admin_a'])


@pytest.mark.django_db
def test_settings_accept_local_tesseract_provider(local_ocr_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'preferred_ocr_model': 'tesseract-default',
            'image_ocr_mode': 'local',
            'scanned_pdf_ocr_mode': 'local_placeholder',
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['preferred_ocr_provider'] == 'tesseract'
    assert response.data['image_ocr_mode'] == 'local'


@pytest.mark.django_db
def test_advanced_run_image_with_local_ocr_disabled_returns_skipped(
    local_ocr_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=local_ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='disabled.png',
        content_bytes=build_png_bytes(),
        content_type='image/png',
        content='nao alterar',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'skipped'
    assert response.data['reason'] == 'advanced_ocr_disabled'
    assert response.data['result'] is None


@pytest.mark.django_db
def test_advanced_run_image_with_local_ocr_enabled_and_mocked_engine_returns_completed(
    local_ocr_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=local_ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='local-image.png',
        content_bytes=build_png_bytes(),
        content_type='image/png',
        content='nao alterar',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'preferred_ocr_model': 'local-hybrid-test',
            'image_ocr_mode': 'local',
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_image(self, file_bytes):
            return 'Texto extraido da imagem via mock.'

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['reason'] == 'local_image_ocr_completed'
    assert response.data['job']['status'] == 'completed'
    assert response.data['job']['extraction_method'] == 'image_local'
    assert response.data['result']['extracted_text'] == 'Texto extraido da imagem via mock.'

    job = OCRJob.objects.get(pk=response.data['job']['id'])
    result = OCRResult.objects.get(pk=response.data['result']['id'])
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])

    assert job.organization == local_ocr_tenant['org_b']
    assert result.document == document
    assert audit_log.action == 'completed'
    assert audit_log.reason == 'local_image_ocr_completed'


@pytest.mark.django_db
def test_advanced_run_creates_controlled_failure_when_local_engine_is_unavailable(
    local_ocr_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=local_ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='unavailable.png',
        content_bytes=build_png_bytes(),
        content_type='image/png',
        content='nao alterar',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'image_ocr_mode': 'local',
        },
        format='json',
    ).status_code == 200

    def failing_engine(settings):
        raise LocalOCREngineUnavailable('tesseract_binary_not_available')

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', failing_engine)

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'failed'
    assert response.data['reason'] == 'local_ocr_engine_unavailable'
    assert response.data['job']['status'] == 'failed'
    assert response.data['result'] is None
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert audit_log.status == 'failed'
    assert audit_log.reason == 'local_ocr_engine_unavailable'
    assert audit_log.metadata['engine_reason'] == 'tesseract_binary_not_available'


@pytest.mark.django_db
def test_advanced_run_blocks_cross_tenant_image_document(local_ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=local_ocr_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='cross-tenant.png',
        content_bytes=build_png_bytes(),
        content_type='image/png',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 400
    assert OCRAuditLog.objects.count() == 0


@pytest.mark.django_db
def test_advanced_run_scanned_pdf_local_mode_returns_placeholder(
    local_ocr_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=local_ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan.pdf',
        content_bytes=b'%PDF-1.4 fake scanned pdf',
        content_type='application/pdf',
        content='',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
        },
        format='json',
    ).status_code == 200

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'skipped'
    assert response.data['reason'] == 'scanned_pdf_local_ocr_not_implemented'
    assert response.data['result'] is None
