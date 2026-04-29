from io import BytesIO
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from docx import Document as DocxBuilder
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from documents.models import Document
from ocr.models import OCRJob, OCRResult
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def build_upload(name, content, content_type):
    return SimpleUploadedFile(name, content, content_type=content_type)


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


def build_docx_bytes(text):
    buffer = BytesIO()
    document = DocxBuilder()
    document.add_paragraph(text)
    document.save(buffer)
    return buffer.getvalue()


def build_pdf_bytes(text):
    buffer = BytesIO()
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=200)
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


@pytest.fixture
def isolated_media_root():
    with tempfile.TemporaryDirectory() as tmpdir:
        with override_settings(MEDIA_ROOT=tmpdir):
            yield tmpdir


@pytest.fixture
def ocr_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(ocr_tenant):
    return authenticated_client(ocr_tenant['admin_b'])


@pytest.fixture
def client_a(ocr_tenant):
    return authenticated_client(ocr_tenant['admin_a'])


@pytest.mark.django_db
def test_txt_valid_extracts_text(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='ocr.txt',
        content_bytes='Texto extraido do txt local.'.encode('utf-8'),
        content_type='text/plain',
        content='conteudo original',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': False},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['job']['status'] == 'completed'
    assert response.data['job']['extraction_method'] == 'txt'
    assert response.data['result']['extracted_text'] == 'Texto extraido do txt local.'
    document.refresh_from_db()
    assert document.content == 'conteudo original'


@pytest.mark.django_db
def test_txt_with_update_document_content_true_updates_document(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='ocr-update.txt',
        content_bytes='Texto aplicado ao document.content.'.encode('utf-8'),
        content_type='text/plain',
        content='antes do ocr',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': True},
        format='json',
    )

    assert response.status_code == 200
    document.refresh_from_db()
    assert document.content == 'Texto aplicado ao document.content.'


@pytest.mark.django_db
def test_pdf_textual_valid_extracts_text(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='ocr.pdf',
        content_bytes=build_pdf_bytes('Texto juridico do PDF'),
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
    assert response.data['job']['extraction_method'] == 'pdf_text'
    assert 'Texto juridico do PDF' in response.data['result']['extracted_text']


@pytest.mark.django_db
def test_docx_valid_extracts_text(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='ocr.docx',
        content_bytes=build_docx_bytes('Paragrafo do DOCX para extracao.'),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        content='',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': False},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['job']['status'] == 'completed'
    assert response.data['job']['extraction_method'] == 'docx_text'
    assert 'Paragrafo do DOCX para extracao.' in response.data['result']['extracted_text']


@pytest.mark.django_db
def test_unsupported_document_creates_failed_job(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan.png',
        content_bytes=b'\x89PNG\r\n\x1a\nfakepng',
        content_type='image/png',
        content='nao alterar',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': False},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['job']['status'] == 'failed'
    assert response.data['job']['extraction_method'] == 'unsupported'
    assert response.data['result'] is None


@pytest.mark.django_db
def test_user_cannot_run_ocr_for_other_organization_document(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='foreign.txt',
        content_bytes='Segredo tenant A'.encode('utf-8'),
        content_type='text/plain',
        content='original',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': False},
        format='json',
    )

    assert response.status_code == 400
    assert OCRJob.objects.count() == 0


@pytest.mark.django_db
def test_jobs_list_only_returns_current_organization(ocr_tenant, client_a, client_b, isolated_media_root):
    document_a = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='a.txt',
        content_bytes='Texto A'.encode('utf-8'),
        content_type='text/plain',
    )
    document_b = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='b.txt',
        content_bytes='Texto B'.encode('utf-8'),
        content_type='text/plain',
    )
    assert client_a.post(f'/api/v1/ocr/documents/{document_a.id}/run/', {}, format='json').status_code == 200
    assert client_b.post(f'/api/v1/ocr/documents/{document_b.id}/run/', {}, format='json').status_code == 200

    response = client_b.get('/api/v1/ocr/jobs/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['organization'] == str(ocr_tenant['org_b'].id)


@pytest.mark.django_db
def test_results_list_only_returns_current_organization(ocr_tenant, client_a, client_b, isolated_media_root):
    document_a = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='a.docx',
        content_bytes=build_docx_bytes('Texto A'),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    document_b = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='b.docx',
        content_bytes=build_docx_bytes('Texto B'),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    assert client_a.post(f'/api/v1/ocr/documents/{document_a.id}/run/', {}, format='json').status_code == 200
    assert client_b.post(f'/api/v1/ocr/documents/{document_b.id}/run/', {}, format='json').status_code == 200

    response = client_b.get('/api/v1/ocr/results/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['organization'] == str(ocr_tenant['org_b'].id)


@pytest.mark.django_db
def test_apply_to_document_updates_document_content(ocr_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='apply.txt',
        content_bytes='Texto do OCR aplicavel.'.encode('utf-8'),
        content_type='text/plain',
        content='antes',
    )
    run_response = client_b.post(f'/api/v1/ocr/documents/{document.id}/run/', {}, format='json')
    result_id = run_response.data['result']['id']

    response = client_b.post(f'/api/v1/ocr/results/{result_id}/apply-to-document/', {}, format='json')

    assert response.status_code == 200
    document.refresh_from_db()
    assert document.content == 'Texto do OCR aplicavel.'


@pytest.mark.django_db
def test_apply_to_document_blocks_cross_tenant_access(ocr_tenant, client_a, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='apply-foreign.txt',
        content_bytes='Texto tenant A'.encode('utf-8'),
        content_type='text/plain',
        content='antes',
    )
    run_response = client_a.post(f'/api/v1/ocr/documents/{document.id}/run/', {}, format='json')
    result_id = run_response.data['result']['id']

    response = client_b.post(f'/api/v1/ocr/results/{result_id}/apply-to-document/', {}, format='json')

    assert response.status_code == 404


@pytest.mark.django_db
def test_extraction_error_registers_failed_without_erasing_document(ocr_tenant, client_b, isolated_media_root, monkeypatch):
    document = create_document_with_file(
        tenant=ocr_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='broken.txt',
        content_bytes='Texto quebrado'.encode('utf-8'),
        content_type='text/plain',
        content='preservar conteudo',
    )

    def failing_extractor(file_bytes):
        raise ValueError('falha controlada de extracao')

    monkeypatch.setattr('ocr.services.extract_text_from_txt', failing_extractor)

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': True},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['job']['status'] == 'failed'
    assert response.data['result'] is None
    document.refresh_from_db()
    assert document.content == 'preservar conteudo'
    assert 'falha controlada de extracao' in response.data['job']['error_message']
