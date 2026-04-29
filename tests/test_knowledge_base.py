import pytest

from documents.models import Document
from knowledge_base.models import (
    ChunkEmbedding,
    DocumentChunk,
    EmbeddingAuditLog,
    IndexingJob,
    KnowledgeBase,
    RAGSettings,
    RetrievalQuery,
)
from knowledge_base.serializers import ChunkEmbeddingSerializer
from knowledge_base.services import index_document_for_knowledge_base, rank_chunks, search_chunks
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def create_document(*, tenant, organization_key, case_key, content, doc_type='internal'):
    law_case = tenant[case_key]
    return Document.objects.create(
        law_case=law_case,
        organization=tenant[organization_key],
        type=doc_type,
        content=content,
        version=Document.objects.filter(law_case=law_case).count() + 1,
    )


def create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B'):
    return KnowledgeBase.objects.create(
        organization=tenant[org_key],
        name=name,
        created_by=tenant[user_key],
    )


def index_document(client, knowledge_base, document):
    return client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/index-document/',
        {'document_id': str(document.id)},
        format='json',
    )


@pytest.mark.django_db
def test_user_creates_knowledge_base_only_in_own_organization():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        '/api/v1/knowledge-base/',
        {
            'name': 'Base do contencioso',
            'description': 'Jurisprudencia e pecas internas',
        },
        format='json',
    )

    assert response.status_code == 201
    knowledge_base = KnowledgeBase.objects.get(name='Base do contencioso')
    assert knowledge_base.organization == tenant['org_b']
    assert knowledge_base.created_by == tenant['admin_b']


@pytest.mark.django_db
def test_user_does_not_list_knowledge_base_from_other_organization():
    tenant = build_service_tenant_fixture()
    create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B')
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/knowledge-base/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['name'] == 'Base B'


@pytest.mark.django_db
def test_user_indexes_document_from_own_organization_and_creates_completed_job():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Contrato de prestacao de servicos juridicos com clausulas de honorarios e obrigacoes.',
    )
    client = authenticated_client(tenant['admin_b'])

    response = index_document(client, knowledge_base, document)

    assert response.status_code == 200
    assert response.data['status'] == 'indexed'
    assert response.data['chunks_created'] >= 1
    job = IndexingJob.objects.get(pk=response.data['indexing_job_id'])
    assert job.organization == tenant['org_b']
    assert job.status == 'completed'
    assert job.chunks_created >= 1
    assert job.finished_at is not None


@pytest.mark.django_db
def test_user_cannot_index_document_from_other_organization():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    foreign_document = create_document(
        tenant=tenant,
        organization_key='org_a',
        case_key='case_a',
        content='Documento sigiloso da organizacao A.',
    )
    client = authenticated_client(tenant['admin_b'])

    response = index_document(client, knowledge_base, foreign_document)

    assert response.status_code == 400
    assert DocumentChunk.objects.count() == 0
    assert IndexingJob.objects.count() == 0


@pytest.mark.django_db
def test_indexing_creates_document_chunks():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content=('Prazo recursal para apelacao. ' * 80).strip(),
    )
    client = authenticated_client(tenant['admin_b'])

    response = index_document(client, knowledge_base, document)

    assert response.status_code == 200
    assert DocumentChunk.objects.filter(
        organization=tenant['org_b'],
        knowledge_document__knowledge_base=knowledge_base,
    ).exists()


@pytest.mark.django_db
def test_indexing_job_list_respects_organization():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    base_b = create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B')
    document_a = create_document(tenant=tenant, organization_key='org_a', case_key='case_a', content='Texto A')
    document_b = create_document(tenant=tenant, organization_key='org_b', case_key='case_b', content='Texto B')
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])

    assert index_document(client_a, base_a, document_a).status_code == 200
    assert index_document(client_b, base_b, document_b).status_code == 200

    response = client_b.get('/api/v1/knowledge-base/indexing-jobs/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert str(response.data['results'][0]['knowledge_base']) == str(base_b.id)


@pytest.mark.django_db
def test_indexing_job_marks_failed_on_controlled_error(monkeypatch):
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Texto que vai falhar.',
    )
    def failing_builder(*args, **kwargs):
        raise ValueError('falha controlada')

    monkeypatch.setattr('knowledge_base.services._build_document_index_text', failing_builder)

    with pytest.raises(ValueError):
        index_document_for_knowledge_base(
            document=document,
            knowledge_base=knowledge_base,
            user=tenant['admin_b'],
        )

    job = IndexingJob.objects.get(
        organization=tenant['org_b'],
        knowledge_base=knowledge_base,
        document=document,
    )
    assert job.status == 'failed'
    assert 'falha controlada' in job.error_message


@pytest.mark.django_db
def test_search_returns_only_chunks_from_same_organization():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    base_b = create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B')
    document_a = create_document(
        tenant=tenant,
        organization_key='org_a',
        case_key='case_a',
        content='Honorarios de sucesso e estrategia do tenant A.',
    )
    document_b = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Honorarios de sucesso e estrategia do tenant B.',
    )
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])
    assert index_document(client_a, base_a, document_a).status_code == 200
    assert index_document(client_b, base_b, document_b).status_code == 200

    response = client_b.post(
        f'/api/v1/knowledge-base/{base_b.id}/search/',
        {'query': 'honorarios sucesso estrategia', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['sources']
    assert all(source['title'].find('Caso B Expanded') >= 0 for source in response.data['sources'])


@pytest.mark.django_db
def test_search_does_not_return_chunks_from_other_tenant_even_with_same_term():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    base_b = create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B')
    document_a = create_document(
        tenant=tenant,
        organization_key='org_a',
        case_key='case_a',
        content='Segredo processual alfa comum.',
    )
    document_b = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Segredo processual beta comum.',
    )
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])

    assert index_document(client_a, base_a, document_a).status_code == 200
    assert index_document(client_b, base_b, document_b).status_code == 200

    response = client_b.post(
        f'/api/v1/knowledge-base/{base_b.id}/search/',
        {'query': 'comum', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert all(source['document_id'] == str(document_b.id) for source in response.data['sources'])


@pytest.mark.django_db
def test_ranking_prioritizes_exact_phrase():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    exact_document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='A expressao tutela de urgencia antecedente consta integralmente neste documento.',
    )
    partial_document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Este texto menciona tutela, urgencia e antecedente em partes separadas.',
    )
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, exact_document).status_code == 200
    assert index_document(client, knowledge_base, partial_document).status_code == 200

    results = search_chunks(
        organization=tenant['org_b'],
        query='tutela de urgencia antecedente',
        knowledge_base=knowledge_base,
        limit=5,
    )

    assert results
    assert results[0].chunk.document_id == exact_document.id
    assert results[0].score >= results[1].score


@pytest.mark.django_db
def test_ranking_filters_out_irrelevant_chunks():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Documento sobre contratos civis e obrigacoes gerais.',
    )
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, document).status_code == 200

    results = search_chunks(
        organization=tenant['org_b'],
        query='jurisprudencia ambiental maritima',
        knowledge_base=knowledge_base,
        limit=5,
    )

    assert results == []


@pytest.mark.django_db
def test_ranking_limit_is_respected():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    client = authenticated_client(tenant['admin_b'])

    for index in range(7):
        document = create_document(
            tenant=tenant,
            organization_key='org_b',
            case_key='case_b',
            content=f'Termo comum repetido numero {index}. Termo comum repetido.',
        )
        assert index_document(client, knowledge_base, document).status_code == 200

    results = search_chunks(
        organization=tenant['org_b'],
        query='termo comum repetido',
        knowledge_base=knowledge_base,
        limit=3,
    )

    assert len(results) == 3


@pytest.mark.django_db
def test_ask_returns_sources_when_chunks_are_relevant():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='A peticao inicial requer tutela de urgencia e juntada de documentos essenciais.',
    )
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, document).status_code == 200

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'O que a peticao inicial requer tutela de urgencia?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['sources']
    assert response.data['retrieval_method'] == 'textual'
    assert response.data['sources_count'] == len(response.data['sources'])
    assert response.data['confidence'] in {'medium', 'high'}
    assert 'Resposta baseada nos trechos encontrados' in response.data['answer']


@pytest.mark.django_db
def test_ask_returns_no_sources_when_not_enough_information():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Qual e a jurisprudencia sobre responsabilidade ambiental?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'no_sources'
    assert response.data['sources'] == []
    assert response.data['retrieval_method'] == 'textual'
    assert response.data['sources_count'] == 0
    assert response.data['confidence'] == 'low'


@pytest.mark.django_db
def test_retrieval_query_is_associated_with_correct_organization_and_new_payload_fields():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Memorial descritivo com estrategia de defesa e honorarios.',
    )
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, document).status_code == 200

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Qual e a estrategia de defesa e honorarios?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    query_record = RetrievalQuery.objects.get()
    assert query_record.organization == tenant['org_b']
    assert query_record.knowledge_base == knowledge_base
    assert query_record.created_by == tenant['admin_b']
    assert query_record.retrieval_method == 'textual'
    assert query_record.sources_count == len(query_record.sources_payload['sources'])
    assert query_record.sources_payload['retrieval_method'] == 'textual'
    assert 'confidence' in query_record.sources_payload


@pytest.mark.django_db
def test_stats_return_correct_counts():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    doc_one = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Texto indexado um.',
    )
    doc_two = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Texto indexado dois.',
    )
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, doc_one).status_code == 200
    assert index_document(client, knowledge_base, doc_two).status_code == 200
    assert client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'texto indexado', 'limit': 5},
        format='json',
    ).status_code == 200

    response = client.get(f'/api/v1/knowledge-base/{knowledge_base.id}/stats/')

    assert response.status_code == 200
    assert response.data['total_documents'] == 2
    assert response.data['indexed_documents'] == 2
    assert response.data['failed_documents'] == 0
    assert response.data['total_chunks'] >= 2
    assert response.data['total_queries'] == 1
    assert response.data['last_indexed_at'] is not None
    assert response.data['last_query_at'] is not None


@pytest.mark.django_db
def test_stats_do_not_mix_tenants():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    base_b = create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B')
    doc_a = create_document(tenant=tenant, organization_key='org_a', case_key='case_a', content='Texto A')
    doc_b = create_document(tenant=tenant, organization_key='org_b', case_key='case_b', content='Texto B')
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])
    assert index_document(client_a, base_a, doc_a).status_code == 200
    assert index_document(client_b, base_b, doc_b).status_code == 200

    response = client_b.get(f'/api/v1/knowledge-base/{base_b.id}/stats/')

    assert response.status_code == 200
    assert response.data['total_documents'] == 1
    assert response.data['indexed_documents'] == 1


@pytest.mark.django_db
def test_user_cannot_access_stats_from_other_tenant():
    tenant = build_service_tenant_fixture()
    foreign_base = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    client = authenticated_client(tenant['admin_b'])

    response = client.get(f'/api/v1/knowledge-base/{foreign_base.id}/stats/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_reindex_removes_old_chunks_and_creates_new_ones():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Texto inicial muito longo. ' * 90,
    )
    client = authenticated_client(tenant['admin_b'])
    first_response = index_document(client, knowledge_base, document)
    first_chunk_count = DocumentChunk.objects.filter(document=document).count()

    document.content = 'Texto atualizado curto mas ainda relevante.'
    document.save(update_fields=['content', 'updated_at'])

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/reindex-document/',
        {'document_id': str(document.id)},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['chunks_deleted'] == first_chunk_count
    assert response.data['chunks_created'] >= 1
    assert DocumentChunk.objects.filter(document=document).count() == response.data['chunks_created']
    assert response.data['chunks_created'] != 0
    assert response.data['indexing_job_id'] != first_response.data['indexing_job_id']


@pytest.mark.django_db
def test_reindex_does_not_affect_other_tenant_documents():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    base_b = create_base(tenant, org_key='org_b', user_key='admin_b', name='Base B')
    document_a = create_document(tenant=tenant, organization_key='org_a', case_key='case_a', content='Texto A longo ' * 50)
    document_b = create_document(tenant=tenant, organization_key='org_b', case_key='case_b', content='Texto B longo ' * 50)
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])
    assert index_document(client_a, base_a, document_a).status_code == 200
    assert index_document(client_b, base_b, document_b).status_code == 200
    original_chunks_a = DocumentChunk.objects.filter(document=document_a).count()

    document_b.content = 'Texto B atualizado.'
    document_b.save(update_fields=['content', 'updated_at'])
    response = client_b.post(
        f'/api/v1/knowledge-base/{base_b.id}/reindex-document/',
        {'document_id': str(document_b.id)},
        format='json',
    )

    assert response.status_code == 200
    assert DocumentChunk.objects.filter(document=document_a).count() == original_chunks_a


@pytest.mark.django_db
def test_chunk_embedding_serializer_allows_manual_same_tenant_registration():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(tenant=tenant, organization_key='org_b', case_key='case_b', content='Texto para embedding.')
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, document).status_code == 200
    chunk = DocumentChunk.objects.filter(document=document).first()

    serializer = ChunkEmbeddingSerializer(
        data={
            'chunk_id': str(chunk.id),
            'provider': 'manual',
            'model': 'test-vector',
            'vector': [0.1, 0.2, 0.3],
            'status': 'generated',
        },
        context={'request': type('Req', (), {'user': tenant['admin_b']})(), 'organization': tenant['org_b']},
    )

    assert serializer.is_valid(), serializer.errors
    embedding = serializer.save()
    assert embedding.organization == tenant['org_b']
    assert embedding.chunk == chunk
    assert embedding.status == 'generated'


@pytest.mark.django_db
def test_chunk_embedding_serializer_rejects_cross_tenant_chunk():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    document_a = create_document(tenant=tenant, organization_key='org_a', case_key='case_a', content='Texto A embedding.')
    client_a = authenticated_client(tenant['admin_a'])
    assert index_document(client_a, base_a, document_a).status_code == 200
    chunk_a = DocumentChunk.objects.filter(document=document_a).first()

    serializer = ChunkEmbeddingSerializer(
        data={
            'chunk_id': str(chunk_a.id),
            'provider': 'manual',
            'model': 'test-vector',
            'vector': [0.1],
            'status': 'generated',
        },
        context={'request': type('Req', (), {'user': tenant['admin_b']})(), 'organization': tenant['org_b']},
    )

    assert not serializer.is_valid()
    assert 'chunk_id' in serializer.errors


@pytest.mark.django_db
def test_get_settings_creates_safe_default_per_organization():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['lawyer_b'])

    response = client.get('/api/v1/knowledge-base/settings/')

    assert response.status_code == 200
    assert response.data['retrieval_mode'] == 'textual'
    assert response.data['external_embeddings_enabled'] is False
    assert response.data['allow_document_content_to_external_provider'] is False
    assert RAGSettings.objects.filter(organization=tenant['org_b']).exists()


@pytest.mark.django_db
def test_user_only_sees_settings_from_own_organization():
    tenant = build_service_tenant_fixture()
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])

    response_a = client_a.get('/api/v1/knowledge-base/settings/')
    response_b = client_b.get('/api/v1/knowledge-base/settings/')

    assert response_a.status_code == 200
    assert response_b.status_code == 200
    assert response_a.data['organization'] != response_b.data['organization']
    assert RAGSettings.objects.count() == 2


@pytest.mark.django_db
def test_patch_settings_rejects_external_embeddings_without_document_opt_in():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.patch(
        '/api/v1/knowledge-base/settings/',
        {
            'external_embeddings_enabled': True,
            'allow_document_content_to_external_provider': False,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'external_embeddings_enabled' in response.data['details']


@pytest.mark.django_db
def test_patch_settings_rejects_embeddings_mode_without_provider():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.patch(
        '/api/v1/knowledge-base/settings/',
        {
            'retrieval_mode': 'embeddings',
            'allow_document_content_to_external_provider': True,
            'external_embeddings_enabled': True,
            'embedding_provider': '',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'embedding_provider' in response.data['details']


@pytest.mark.django_db
def test_patch_settings_accepts_hybrid_with_provider_and_explicit_opt_in():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['admin_b'])

    response = client.patch(
        '/api/v1/knowledge-base/settings/',
        {
            'retrieval_mode': 'hybrid',
            'external_embeddings_enabled': True,
            'allow_document_content_to_external_provider': True,
            'embedding_provider': 'openai',
            'embedding_model': 'text-embedding-placeholder',
            'max_sources_per_answer': 3,
            'min_confidence_threshold': 'medium',
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['retrieval_mode'] == 'hybrid'
    assert response.data['external_embeddings_enabled'] is True
    assert response.data['allow_document_content_to_external_provider'] is True
    assert response.data['embedding_provider'] == 'openai'
    assert response.data['max_sources_per_answer'] == 3


@pytest.mark.django_db
def test_non_admin_cannot_update_rag_settings():
    tenant = build_service_tenant_fixture()
    client = authenticated_client(tenant['lawyer_b'])

    response = client.patch(
        '/api/v1/knowledge-base/settings/',
        {'retrieval_mode': 'hybrid'},
        format='json',
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_prepare_embeddings_creates_skipped_audit_log_when_provider_disabled():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(tenant=tenant, organization_key='org_b', case_key='case_b', content='Texto para placeholder.')
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, document).status_code == 200
    knowledge_document = knowledge_base.documents.get(document=document)

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/prepare-embeddings/',
        {'knowledge_document_id': str(knowledge_document.id)},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'skipped'
    assert response.data['reason'] == 'external_embeddings_disabled'
    audit_log = EmbeddingAuditLog.objects.get(pk=response.data['audit_log_id'])
    assert audit_log.organization == tenant['org_b']
    assert audit_log.knowledge_document == knowledge_document
    assert audit_log.provider == ''


@pytest.mark.django_db
def test_embedding_audit_logs_are_filtered_by_organization():
    tenant = build_service_tenant_fixture()
    EmbeddingAuditLog.objects.create(
        organization=tenant['org_a'],
        action='skipped',
        status='skipped',
        reason='external_embeddings_disabled',
        created_by=tenant['admin_a'],
    )
    EmbeddingAuditLog.objects.create(
        organization=tenant['org_b'],
        action='skipped',
        status='skipped',
        reason='external_embeddings_disabled',
        created_by=tenant['admin_b'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/knowledge-base/embedding-audit-logs/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert str(response.data['results'][0]['organization']) == str(tenant['org_b'].id)


@pytest.mark.django_db
def test_ask_uses_textual_fallback_when_hybrid_requested_but_not_effective():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='A contestacao apresenta argumentos defensivos e documentos anexos.',
    )
    client = authenticated_client(tenant['admin_b'])
    assert index_document(client, knowledge_base, document).status_code == 200
    assert client.patch(
        '/api/v1/knowledge-base/settings/',
        {
            'retrieval_mode': 'hybrid',
            'embedding_provider': 'openai',
            'external_embeddings_enabled': False,
            'allow_document_content_to_external_provider': False,
        },
        format='json',
    ).status_code == 200

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Quais argumentos defensivos a contestacao apresenta?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['retrieval_method'] == 'textual'
    assert response.data['effective_retrieval_mode'] == 'textual'
    assert response.data['fallback_used'] is True
    assert response.data['fallback_reason'] == 'external_embeddings_disabled'
    assert response.data['sources']


@pytest.mark.django_db
def test_max_sources_per_answer_limits_ask_sources():
    tenant = build_service_tenant_fixture()
    knowledge_base = create_base(tenant)
    client = authenticated_client(tenant['admin_b'])
    assert client.patch(
        '/api/v1/knowledge-base/settings/',
        {'max_sources_per_answer': 2},
        format='json',
    ).status_code == 200

    for index in range(5):
        document = create_document(
            tenant=tenant,
            organization_key='org_b',
            case_key='case_b',
            content=f'Clausula contratual relevante numero {index}. Clausula contratual relevante.',
        )
        assert index_document(client, knowledge_base, document).status_code == 200

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'clausula contratual relevante', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['sources_count'] == 2
    assert len(response.data['sources']) == 2


@pytest.mark.django_db
def test_prepare_embeddings_respects_tenant_isolation():
    tenant = build_service_tenant_fixture()
    base_a = create_base(tenant, org_key='org_a', user_key='admin_a', name='Base A')
    document_a = create_document(tenant=tenant, organization_key='org_a', case_key='case_a', content='Texto A para prepare.')
    client_a = authenticated_client(tenant['admin_a'])
    client_b = authenticated_client(tenant['admin_b'])
    assert index_document(client_a, base_a, document_a).status_code == 200
    knowledge_document_a = base_a.documents.get(document=document_a)

    response = client_b.post(
        f'/api/v1/knowledge-base/{base_a.id}/prepare-embeddings/',
        {'knowledge_document_id': str(knowledge_document_a.id)},
        format='json',
    )

    assert response.status_code == 404
