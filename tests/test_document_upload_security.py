import tempfile
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from documents.models import Document
from jurisai.utils import sanitize_upload_filename
from law_cases.models import LawCase
from organizations.models import Organization


# Assuncao documentada no plano de hardening: limite recomendado de 10 MB.
MAX_DOCUMENT_UPLOAD_BYTES = 10 * 1024 * 1024


def authenticate(client, email, password):
    token_response = client.post(
        reverse('token_obtain_pair'),
        {'email': email, 'password': password},
        format='json',
    )
    assert token_response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")


def build_tenant_fixture():
    org_a = Organization.objects.create(name='Org A Document Upload', plan='free')
    org_b = Organization.objects.create(name='Org B Document Upload', plan='free')

    admin_b = User.objects.create_user(
        email='admin-b-document@example.com',
        password='strongpass123',
        name='Admin B Document',
        organization=org_b,
        role='admin',
        is_staff=True,
    )
    lawyer_a = User.objects.create_user(
        email='lawyer-a-document@example.com',
        password='strongpass123',
        name='Lawyer A Document',
        organization=org_a,
        role='advogado',
    )
    client_a = User.objects.create_user(
        email='client-a-document@example.com',
        password='strongpass123',
        name='Client A Document',
        organization=org_a,
        role='cliente',
    )
    lawyer_b = User.objects.create_user(
        email='lawyer-b-document@example.com',
        password='strongpass123',
        name='Lawyer B Document',
        organization=org_b,
        role='advogado',
    )
    client_b = User.objects.create_user(
        email='client-b-document@example.com',
        password='strongpass123',
        name='Client B Document',
        organization=org_b,
        role='cliente',
    )

    case_a = LawCase.objects.create(
        title='Caso A Upload Security',
        description='Caso tenant A para upload',
        client=client_a,
        lawyer=lawyer_a,
        organization=org_a,
        status='open',
    )
    case_b = LawCase.objects.create(
        title='Caso B Upload Security',
        description='Caso tenant B para upload',
        client=client_b,
        lawyer=lawyer_b,
        organization=org_b,
        status='open',
    )

    return {
        'org_a': org_a,
        'org_b': org_b,
        'admin_b': admin_b,
        'case_a': case_a,
        'case_b': case_b,
    }


def build_upload(name, content, content_type):
    return SimpleUploadedFile(name, content, content_type=content_type)


def build_document_payload(law_case_id, uploaded_file, content='Documento de teste'):
    return {
        'law_case_id': str(law_case_id),
        'type': 'internal',
        'content': content,
        'file': uploaded_file,
    }


def get_saved_upload_name(document):
    name = Path(document.file.name).name
    return name.split('_', 1)[1] if '_' in name else name


@pytest.fixture
def authenticated_tenant_client():
    tenant = build_tenant_fixture()
    client = APIClient()
    authenticate(client, tenant['admin_b'].email, 'strongpass123')
    return client, tenant


@pytest.fixture
def isolated_media_root():
    with tempfile.TemporaryDirectory() as tmpdir:
        with override_settings(MEDIA_ROOT=tmpdir):
            yield Path(tmpdir)


@pytest.mark.django_db
def test_accept_valid_pdf_upload(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('valid.pdf', b'%PDF-1.4 secure content', 'application/pdf')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='PDF valido'),
        format='multipart',
    )

    assert response.status_code == 201
    assert Document.objects.filter(law_case=tenant['case_b'], organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_accept_valid_pdf_magic_bytes(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('magic-valid.pdf', b'%PDF-1.7\nbinary content', 'application/pdf')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='PDF magic valido'),
        format='multipart',
    )

    assert response.status_code == 201
    assert Document.objects.filter(content='PDF magic valido', organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_reject_pdf_with_invalid_magic_bytes(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('fake.pdf', b'NOTPDF binary content', 'application/pdf')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='PDF magic invalido'),
        format='multipart',
    )

    assert response.status_code == 400
    assert not Document.objects.filter(content='PDF magic invalido').exists()


@pytest.mark.django_db
def test_reject_executable_upload_extension(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('dangerous.exe', b'MZ executable payload', 'application/octet-stream')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='Executavel indevido'),
        format='multipart',
    )

    assert response.status_code == 400
    assert not Document.objects.filter(content='Executavel indevido').exists()


@pytest.mark.django_db
def test_reject_upload_above_size_limit(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload(
        'oversized.pdf',
        b'a' * (MAX_DOCUMENT_UPLOAD_BYTES + 1),
        'application/pdf',
    )

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='PDF demasiado grande'),
        format='multipart',
    )

    assert response.status_code == 400
    assert not Document.objects.filter(content='PDF demasiado grande').exists()


@pytest.mark.django_db
def test_reject_upload_with_mismatched_content_type(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('spoofed.pdf', b'pretend pdf', 'application/x-msdownload')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='Content type incompatível'),
        format='multipart',
    )

    assert response.status_code == 400
    assert not Document.objects.filter(content='Content type incompatível').exists()


@pytest.mark.django_db
def test_accept_valid_png_magic_bytes(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload(
        'image-valid.png',
        b'\x89PNG\r\n\x1a\nresto-do-ficheiro',
        'image/png',
    )

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='PNG magic valido'),
        format='multipart',
    )

    assert response.status_code == 201
    assert Document.objects.filter(content='PNG magic valido', organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_reject_png_with_invalid_magic_bytes(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('fake.png', b'NOTPNG binary content', 'image/png')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='PNG magic invalido'),
        format='multipart',
    )

    assert response.status_code == 400
    assert not Document.objects.filter(content='PNG magic invalido').exists()


@pytest.mark.django_db
def test_accept_valid_jpeg_magic_bytes(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('image-valid.jpg', b'\xff\xd8\xff\xe0jpeg-data', 'image/jpeg')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='JPEG magic valido'),
        format='multipart',
    )

    assert response.status_code == 201
    assert Document.objects.filter(content='JPEG magic valido', organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_reject_jpeg_with_invalid_magic_bytes(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('fake.jpeg', b'NOTJPEG binary content', 'image/jpeg')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='JPEG magic invalido'),
        format='multipart',
    )

    assert response.status_code == 400
    assert not Document.objects.filter(content='JPEG magic invalido').exists()


@pytest.mark.django_db
def test_same_tenant_upload_remains_valid(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('tenant-safe.pdf', b'%PDF-1.4 tenant document', 'application/pdf')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='Mesmo tenant continua valido'),
        format='multipart',
    )

    assert response.status_code == 201
    assert Document.objects.filter(content='Mesmo tenant continua valido', organization=tenant['org_b']).count() == 1


@pytest.mark.django_db
def test_cross_tenant_upload_remains_blocked(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('cross-tenant.pdf', b'%PDF-1.4 forbidden tenant', 'application/pdf')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_a'].id, upload, content='Documento cross-tenant'),
        format='multipart',
    )

    assert response.status_code in (400, 403)
    assert not Document.objects.filter(law_case=tenant['case_a']).exists()


@pytest.mark.django_db
def test_path_traversal_filename_is_rejected_or_sanitized(authenticated_tenant_client, isolated_media_root):
    client, tenant = authenticated_tenant_client
    upload = build_upload('../../evil.pdf', b'%PDF-1.4 traversal attempt', 'application/pdf')

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content='Nome com traversal'),
        format='multipart',
    )

    assert response.status_code == 201

    document = Document.objects.get(content='Nome com traversal')
    saved_name = get_saved_upload_name(document)
    assert saved_name.endswith('.pdf')
    assert '..' not in document.file.name
    assert '../' not in document.file.name
    assert '..\\' not in document.file.name
    assert '/' not in saved_name
    assert '\\' not in saved_name
    assert ' ' not in saved_name


def test_sanitize_filename_normalizes_spaces_and_special_characters():
    assert sanitize_upload_filename('Relatorio Final 2026 @#$%.pdf') == 'Relatorio_Final_2026.pdf'


def test_sanitize_filename_truncates_long_basename_and_preserves_extension():
    long_name = f"{'a' * 120}.pdf"
    assert sanitize_upload_filename(long_name) == f"{'a' * 80}.pdf"


def test_sanitize_filename_keeps_valid_extension_and_sanitizes_multiple_dots():
    assert sanitize_upload_filename('report.final.v2.pdf') == 'report_final_v2.pdf'


@pytest.mark.parametrize(
    ('filename', 'content_type', 'content', 'marker'),
    [
        ('current.doc', 'application/msword', b'DOC legacy content', 'DOC continua aceite'),
        ('current.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', b'PK\x03\x04docx-like', 'DOCX continua aceite'),
        ('current.txt', 'text/plain', b'text file content', 'TXT continua aceite'),
    ],
)
@pytest.mark.django_db
def test_doc_docx_and_txt_keep_current_behavior_this_phase(
    authenticated_tenant_client,
    isolated_media_root,
    filename,
    content_type,
    content,
    marker,
):
    client, tenant = authenticated_tenant_client
    upload = build_upload(filename, content, content_type)

    response = client.post(
        '/api/v1/documents/',
        build_document_payload(tenant['case_b'].id, upload, content=marker),
        format='multipart',
    )

    assert response.status_code == 201
    assert Document.objects.filter(content=marker, organization=tenant['org_b']).count() == 1
