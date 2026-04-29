import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from documents.models import Document
from knowledge_base.models import DocumentChunk, KnowledgeBase
from ocr.models import OCRAuditLog, OCRJob, OCRSettings
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


def create_knowledge_base(tenant, org_key='org_b', user_key='admin_b', name='Base OCR Governance'):
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
def governance_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(governance_tenant):
    return authenticated_client(governance_tenant['admin_b'])


@pytest.fixture
def client_a(governance_tenant):
    return authenticated_client(governance_tenant['admin_a'])


@pytest.mark.django_db
def test_get_settings_creates_safe_default_per_organization(governance_tenant, client_b):
    response = client_b.get('/api/v1/ocr/settings/')

    assert response.status_code == 200
    assert response.data['advanced_ocr_enabled'] is False
    assert response.data['external_ocr_enabled'] is False
    assert response.data['allow_document_content_to_external_ocr_provider'] is False
    assert response.data['image_ocr_mode'] == 'disabled'
    assert response.data['scanned_pdf_ocr_mode'] == 'disabled'
    assert OCRSettings.objects.filter(organization=governance_tenant['org_b']).exists()


@pytest.mark.django_db
def test_user_only_sees_settings_from_own_organization(governance_tenant, client_a, client_b):
    response_a = client_a.get('/api/v1/ocr/settings/')
    response_b = client_b.get('/api/v1/ocr/settings/')

    assert response_a.status_code == 200
    assert response_b.status_code == 200
    assert response_a.data['organization'] != response_b.data['organization']
    assert OCRSettings.objects.count() == 2


@pytest.mark.django_db
def test_patch_rejects_external_ocr_without_explicit_opt_in(governance_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'external_ocr_enabled': True,
            'allow_document_content_to_external_ocr_provider': False,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'external_ocr_enabled' in response.data['details']


@pytest.mark.django_db
def test_patch_rejects_image_external_mode_without_external_ocr_enabled(governance_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'image_ocr_mode': 'external',
            'external_ocr_enabled': False,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'image_ocr_mode' in response.data['details']


@pytest.mark.django_db
def test_patch_accepts_external_configuration_only_with_explicit_opt_in(governance_tenant, client_b):
    response = client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'external_ocr_enabled': True,
            'allow_document_content_to_external_ocr_provider': True,
            'preferred_ocr_provider': 'google_vision',
            'preferred_ocr_model': 'vision-placeholder',
            'image_ocr_mode': 'external',
            'scanned_pdf_ocr_mode': 'external',
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['external_ocr_enabled'] is True
    assert response.data['allow_document_content_to_external_ocr_provider'] is True
    assert response.data['preferred_ocr_provider'] == 'google_vision'
    assert response.data['image_ocr_mode'] == 'external'


@pytest.mark.django_db
def test_advanced_run_with_advanced_disabled_creates_skipped_audit_log(
    governance_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan.png',
        content_bytes=b'\x89PNG\r\n\x1a\nfakepng',
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
    assert response.data['job']['status'] == 'failed'
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert audit_log.organization == governance_tenant['org_b']
    assert audit_log.reason == 'advanced_ocr_disabled'


@pytest.mark.django_db
def test_advanced_run_with_external_configuration_does_not_call_provider(
    governance_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='scan-external.png',
        content_bytes=b'\x89PNG\r\n\x1a\nexternal',
        content_type='image/png',
        content='nao alterar',
    )
    assert client_b.patch(
        '/api/v1/ocr/settings/',
        {
            'advanced_ocr_enabled': True,
            'external_ocr_enabled': True,
            'allow_document_content_to_external_ocr_provider': True,
            'preferred_ocr_provider': 'google_vision',
            'preferred_ocr_model': 'vision-placeholder',
            'image_ocr_mode': 'external',
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
    assert response.data['reason'] == 'external_ocr_not_implemented'
    audit_log = OCRAuditLog.objects.get(pk=response.data['audit_log']['id'])
    assert audit_log.provider == 'google_vision'
    assert audit_log.status == 'skipped'


@pytest.mark.django_db
def test_audit_logs_are_filtered_by_organization(governance_tenant, client_a, client_b, isolated_media_root):
    document_a = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='a.png',
        content_bytes=b'\x89PNG\r\n\x1a\na',
        content_type='image/png',
    )
    document_b = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='b.png',
        content_bytes=b'\x89PNG\r\n\x1a\nb',
        content_type='image/png',
    )
    assert client_a.post(f'/api/v1/ocr/documents/{document_a.id}/advanced-run/', {'mode': 'auto'}, format='json').status_code == 200
    assert client_b.post(f'/api/v1/ocr/documents/{document_b.id}/advanced-run/', {'mode': 'auto'}, format='json').status_code == 200

    response = client_b.get('/api/v1/ocr/audit-logs/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert str(response.data['results'][0]['organization']) == str(governance_tenant['org_b'].id)


@pytest.mark.django_db
def test_advanced_run_blocks_cross_tenant_document(governance_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='foreign.png',
        content_bytes=b'\x89PNG\r\n\x1a\nforeign',
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
def test_existing_local_txt_ocr_still_works(governance_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='local.txt',
        content_bytes='Texto local continua funcional.'.encode('utf-8'),
        content_type='text/plain',
        content='original',
    )

    response = client_b.post(
        f'/api/v1/ocr/documents/{document.id}/run/',
        {'update_document_content': False},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['job']['status'] == 'completed'
    assert response.data['result']['extracted_text'] == 'Texto local continua funcional.'


@pytest.mark.django_db
def test_existing_ocr_to_knowledge_base_pipeline_still_works(governance_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=governance_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='pipeline.txt',
        content_bytes='Texto para pipeline com knowledge base.'.encode('utf-8'),
        content_type='text/plain',
        content='antes',
    )
    knowledge_base = create_knowledge_base(governance_tenant)

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
    assert document.content == 'Texto para pipeline com knowledge base.'
    assert DocumentChunk.objects.filter(document=document, knowledge_document__knowledge_base=knowledge_base).exists()
