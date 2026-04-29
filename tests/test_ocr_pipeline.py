from io import BytesIO
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from documents.models import Document
from knowledge_base.models import DocumentChunk, IndexingJob, KnowledgeBase, KnowledgeDocument
from ocr.models import OCRJob, OCRKnowledgeBasePipelineRun, OCRResult
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


def create_knowledge_base(tenant, org_key='org_b', user_key='admin_b', name='Base OCR KB'):
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
def ocr_pipeline_tenant():
    return build_service_tenant_fixture()


@pytest.fixture
def client_b(ocr_pipeline_tenant):
    return authenticated_client(ocr_pipeline_tenant['admin_b'])


@pytest.fixture
def client_a(ocr_pipeline_tenant):
    return authenticated_client(ocr_pipeline_tenant['admin_a'])


@pytest.mark.django_db
def test_pipeline_executes_ocr_applies_document_content_and_indexes_knowledge_base(
    ocr_pipeline_tenant, client_b, isolated_media_root
):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='pipeline.txt',
        content_bytes='Texto OCR para base de conhecimento e consulta.'.encode('utf-8'),
        content_type='text/plain',
        content='conteudo antigo',
    )
    knowledge_base = create_knowledge_base(ocr_pipeline_tenant)

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
    assert response.data['step'] == 'completed'
    assert response.data['ocr_job'] is not None
    assert response.data['ocr_result'] is not None
    assert response.data['knowledge_document'] is not None
    assert response.data['indexing_job'] is not None

    document.refresh_from_db()
    assert document.content == 'Texto OCR para base de conhecimento e consulta.'
    assert OCRJob.objects.filter(organization=ocr_pipeline_tenant['org_b'], document=document).exists()
    assert OCRResult.objects.filter(organization=ocr_pipeline_tenant['org_b'], document=document).exists()
    assert KnowledgeDocument.objects.filter(
        organization=ocr_pipeline_tenant['org_b'],
        knowledge_base=knowledge_base,
        document=document,
    ).exists()
    assert DocumentChunk.objects.filter(
        organization=ocr_pipeline_tenant['org_b'],
        document=document,
        knowledge_document__knowledge_base=knowledge_base,
    ).exists()
    assert IndexingJob.objects.filter(
        organization=ocr_pipeline_tenant['org_b'],
        knowledge_base=knowledge_base,
        document=document,
        status='completed',
    ).exists()


@pytest.mark.django_db
def test_pipeline_blocks_document_from_other_tenant(ocr_pipeline_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='foreign-doc.txt',
        content_bytes='Documento tenant A'.encode('utf-8'),
        content_type='text/plain',
    )
    knowledge_base = create_knowledge_base(ocr_pipeline_tenant)

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


@pytest.mark.django_db
def test_pipeline_blocks_knowledge_base_from_other_tenant(ocr_pipeline_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='own-doc.txt',
        content_bytes='Documento tenant B'.encode('utf-8'),
        content_type='text/plain',
    )
    foreign_base = create_knowledge_base(
        ocr_pipeline_tenant,
        org_key='org_a',
        user_key='admin_a',
        name='Base Tenant A',
    )

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(foreign_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert response.status_code == 400
    assert OCRKnowledgeBasePipelineRun.objects.count() == 0


@pytest.mark.django_db
def test_pipeline_rejects_update_document_content_false(ocr_pipeline_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='no-apply.txt',
        content_bytes='Texto sem apply'.encode('utf-8'),
        content_type='text/plain',
        content='original',
    )
    knowledge_base = create_knowledge_base(ocr_pipeline_tenant)

    response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': False,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'update_document_content' in response.data['details']
    document.refresh_from_db()
    assert document.content == 'original'
    assert OCRKnowledgeBasePipelineRun.objects.count() == 0


@pytest.mark.django_db
def test_pipeline_marks_failed_when_ocr_fails_and_does_not_create_chunks(
    ocr_pipeline_tenant, client_b, isolated_media_root, monkeypatch
):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='broken.txt',
        content_bytes='Texto com falha'.encode('utf-8'),
        content_type='text/plain',
        content='preservar',
    )
    knowledge_base = create_knowledge_base(ocr_pipeline_tenant)

    original_run_ocr = __import__('ocr.services', fromlist=['run_ocr_for_document'])

    def failing_run_ocr_for_document(document, user, update_document_content=False):
        job = OCRJob.objects.create(
            organization=document.organization,
            document=document,
            requested_by=user,
            status='failed',
            extraction_method='txt',
            error_message='falha controlada no OCR',
        )
        return job, None

    monkeypatch.setattr(original_run_ocr, 'run_ocr_for_document', failing_run_ocr_for_document)

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
    pipeline_run = OCRKnowledgeBasePipelineRun.objects.get(pk=response.data['id'])
    assert pipeline_run.status == 'failed'
    assert pipeline_run.step == 'failed'
    assert 'falha controlada no OCR' in pipeline_run.error_message
    document.refresh_from_db()
    assert document.content == 'preservar'
    assert not DocumentChunk.objects.filter(document=document).exists()


@pytest.mark.django_db
def test_pipeline_list_respects_organization(ocr_pipeline_tenant, client_a, client_b, isolated_media_root):
    document_a = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='a-pipeline.txt',
        content_bytes='Texto pipeline A'.encode('utf-8'),
        content_type='text/plain',
        content='A',
    )
    document_b = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='b-pipeline.txt',
        content_bytes='Texto pipeline B'.encode('utf-8'),
        content_type='text/plain',
        content='B',
    )
    base_a = create_knowledge_base(ocr_pipeline_tenant, org_key='org_a', user_key='admin_a', name='Base A')
    base_b = create_knowledge_base(ocr_pipeline_tenant, org_key='org_b', user_key='admin_b', name='Base B')

    assert client_a.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {'document_id': str(document_a.id), 'knowledge_base_id': str(base_a.id), 'update_document_content': True},
        format='json',
    ).status_code == 200
    assert client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {'document_id': str(document_b.id), 'knowledge_base_id': str(base_b.id), 'update_document_content': True},
        format='json',
    ).status_code == 200

    response = client_b.get('/api/v1/ocr/pipelines/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['organization'] == str(ocr_pipeline_tenant['org_b'].id)


@pytest.mark.django_db
def test_pipeline_detail_cross_tenant_returns_404(ocr_pipeline_tenant, client_a, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_a',
        case_key='case_a',
        filename='detail-foreign.txt',
        content_bytes='Texto detail A'.encode('utf-8'),
        content_type='text/plain',
        content='A',
    )
    knowledge_base = create_knowledge_base(
        ocr_pipeline_tenant,
        org_key='org_a',
        user_key='admin_a',
        name='Base Detail A',
    )
    create_response = client_a.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {'document_id': str(document.id), 'knowledge_base_id': str(knowledge_base.id), 'update_document_content': True},
        format='json',
    )

    response = client_b.get(f"/api/v1/ocr/pipelines/{create_response.data['id']}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_ask_returns_source_after_successful_pipeline(ocr_pipeline_tenant, client_b, isolated_media_root):
    document = create_document_with_file(
        tenant=ocr_pipeline_tenant,
        organization_key='org_b',
        case_key='case_b',
        filename='ask-pipeline.txt',
        content_bytes='Clausula arbitral com competencia e foro escolhido pelas partes.'.encode('utf-8'),
        content_type='text/plain',
        content='vazio',
    )
    knowledge_base = create_knowledge_base(ocr_pipeline_tenant)

    pipeline_response = client_b.post(
        '/api/v1/ocr/pipelines/knowledge-base/',
        {
            'document_id': str(document.id),
            'knowledge_base_id': str(knowledge_base.id),
            'update_document_content': True,
        },
        format='json',
    )

    assert pipeline_response.status_code == 200

    ask_response = client_b.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Qual e a clausula arbitral e o foro escolhido?', 'limit': 5},
        format='json',
    )

    assert ask_response.status_code == 200
    assert ask_response.data['status'] == 'completed'
    assert ask_response.data['sources']
    assert any(source['document_id'] == str(document.id) for source in ask_response.data['sources'])
