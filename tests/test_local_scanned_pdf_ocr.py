from io import BytesIO
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from documents.models import Document
from knowledge_base.models import DocumentChunk, KnowledgeBase
from ocr.local_engines import LocalOCREngineUnavailable, PDFRasterizationUnavailable
from ocr.models import OCRAuditLog, OCRJob, OCRResult
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def build_upload(name, content, content_type):
    return SimpleUploadedFile(name, content, content_type=content_type)


def build_png_bytes():
    buffer = BytesIO()
    image = Image.new('RGB', (32, 32), color='white')
    image.save(buffer, format='PNG')
    return buffer.getvalue()


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


def create_knowledge_base(tenant, org_key='org_b', user_key='admin_b', name='Base OCR PDF'):
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
def scanned_pdf_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(scanned_pdf_tenant):
    return authenticated_client(scanned_pdf_tenant['admin_b'])


@pytest.fixture
def client_a(scanned_pdf_tenant):
    return authenticated_client(scanned_pdf_tenant['admin_a'])


@pytest.mark.django_db
def test_settings_accept_scanned_pdf_local_mode(scanned_pdf_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'preferred_ocr_provider': 'tesseract',
            'scanned_pdf_ocr_mode': 'local',
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['scanned_pdf_ocr_mode'] == 'local'


@pytest.mark.django_db
def test_advanced_run_pdf_with_scanned_pdf_mode_disabled_returns_skipped(
    scanned_pdf_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='disabled-scan.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'skipped'
    assert response.data['reason'] == 'advanced_ocr_disabled'


@pytest.mark.django_db
def test_advanced_run_pdf_with_local_mode_and_mocked_engine_returns_completed(
    scanned_pdf_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan-local.pdf',
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
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            assert max_pages == 10
            return 'Pagina 1 mock.\n\nPagina 2 mock.'

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['reason'] == 'local_scanned_pdf_ocr_completed'
    assert response.data['job']['status'] == 'completed'
    assert response.data['job']['extraction_method'] == 'scanned_pdf_local'
    assert response.data['result']['extracted_text'] == 'Pagina 1 mock.\n\nPagina 2 mock.'

    result = OCRResult.objects.get(pk=response.data['result']['id'])
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert result.char_count == len('Pagina 1 mock.\n\nPagina 2 mock.')
    assert audit_log.action == 'completed'
    assert audit_log.reason == 'local_scanned_pdf_ocr_completed'


@pytest.mark.django_db
def test_advanced_run_pdf_with_rasterization_failure_is_controlled(
    scanned_pdf_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan-raster.pdf',
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
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            raise PDFRasterizationUnavailable('poppler_not_available')

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'failed'
    assert response.data['reason'] == 'pdf_rasterization_unavailable'
    assert response.data['job']['status'] == 'failed'
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert audit_log.reason == 'pdf_rasterization_unavailable'


@pytest.mark.django_db
def test_advanced_run_pdf_with_tesseract_failure_is_controlled(
    scanned_pdf_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan-tesseract.pdf',
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
        },
        format='json',
    ).status_code == 200

    class FakeEngine:
        def extract_text_from_scanned_pdf(self, file_bytes, max_pages=None):
            raise LocalOCREngineUnavailable('tesseract_binary_not_available')

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'failed'
    assert response.data['reason'] == 'local_ocr_engine_unavailable'
    assert response.data['job']['status'] == 'failed'
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert audit_log.reason == 'local_ocr_engine_unavailable'


@pytest.mark.django_db
def test_advanced_run_blocks_cross_tenant_scanned_pdf_document(
    scanned_pdf_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='foreign-scan.pdf',
        content_bytes=build_pdf_bytes(),
        content_type='application/pdf',
        content='',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 400
    assert OCRAuditLog.objects.count() == 0


@pytest.mark.django_db
def test_existing_textual_pdf_ocr_still_works(scanned_pdf_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='textual.pdf',
        content_bytes=build_pdf_bytes('PDF textual continua funcional'),
        content_type='application/pdf',
        content='',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': False},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['job']['status'] == 'completed'
    assert 'PDF textual continua funcional' in response.data['result']['extracted_text']


@pytest.mark.django_db
def test_existing_image_ocr_flow_still_works(scanned_pdf_tenant, client_b, isolated_media_root, monkeypatch):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='image-regression.png',
        content_bytes=build_png_bytes(),
        content_type='image/png',
        content='',
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

    class FakeEngine:
        provider = 'tesseract'
        model = 'tesseract-default'

        def extract_text_from_image(self, file_bytes):
            return 'Texto de imagem ainda funcional.'

    monkeypatch.setattr('ocr.services.get_local_ocr_engine', lambda settings: FakeEngine())

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/advanced-run/',
        {'mode': 'auto'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['result']['extracted_text'] == 'Texto de imagem ainda funcional.'


@pytest.mark.django_db
def test_existing_ocr_to_knowledge_base_pipeline_still_works(
    scanned_pdf_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=scanned_pdf_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='pipeline.txt',
        content_bytes='Texto OCR pipeline KB.'.encode('utf-8'),
        content_type='text/plain',
        content='antes',
    )
    knowledge_base = create_knowledge_base(scanned_pdf_tenant)

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
    document.refresh_from_db()
    assert document.content == 'Texto OCR pipeline KB.'
    assert DocumentChunk.objects.filter(document=document, knowledge_document__knowledge_base=knowledge_base).exists()
