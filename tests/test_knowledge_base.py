import pytest

from documents.models import Document
from knowledge_base.models import DocumentChunk, KnowledgeBase, RetrievalQuery
from tests.legal_services_helpers import authenticated_client, build_service_tenant_fixture


def create_document(*, tenant, organization_key, case_key, content, doc_type='internal'):
    return Document.objects.create(
        law_case=tenant[case_key],
        organization=tenant[organization_key],
        type=doc_type,
        content=content,
        version=1,
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
    KnowledgeBase.objects.create(
        organization=tenant['org_a'],
        name='Base A',
        created_by=tenant['admin_a'],
    )
    KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.get('/api/v1/knowledge-base/')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['name'] == 'Base B'


@pytest.mark.django_db
def test_user_indexes_document_from_own_organization():
    tenant = build_service_tenant_fixture()
    knowledge_base = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Contrato de prestacao de servicos juridicos com clausulas de honorarios e obrigacoes.',
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/index-document/',
        {'document_id': str(document.id)},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'indexed'
    assert response.data['chunks_created'] >= 1


@pytest.mark.django_db
def test_user_cannot_index_document_from_other_organization():
    tenant = build_service_tenant_fixture()
    knowledge_base = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    foreign_document = create_document(
        tenant=tenant,
        organization_key='org_a',
        case_key='case_a',
        content='Documento sigiloso da organizacao A.',
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/index-document/',
        {'document_id': str(foreign_document.id)},
        format='json',
    )

    assert response.status_code == 400
    assert DocumentChunk.objects.count() == 0


@pytest.mark.django_db
def test_indexing_creates_document_chunks():
    tenant = build_service_tenant_fixture()
    knowledge_base = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content=('Prazo recursal para apelacao. ' * 80).strip(),
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/index-document/',
        {'document_id': str(document.id)},
        format='json',
    )

    assert response.status_code == 200
    assert DocumentChunk.objects.filter(
        organization=tenant['org_b'],
        knowledge_document__knowledge_base=knowledge_base,
    ).exists()


@pytest.mark.django_db
def test_search_returns_only_chunks_from_same_organization():
    tenant = build_service_tenant_fixture()
    base_a = KnowledgeBase.objects.create(
        organization=tenant['org_a'],
        name='Base A',
        created_by=tenant['admin_a'],
    )
    base_b = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
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
    client = authenticated_client(tenant['admin_b'])
    client_a.post(f'/api/v1/knowledge-base/{base_a.id}/index-document/', {'document_id': str(document_a.id)}, format='json')
    client.post(f'/api/v1/knowledge-base/{base_b.id}/index-document/', {'document_id': str(document_b.id)}, format='json')

    response = client.post(
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
    base_a = KnowledgeBase.objects.create(
        organization=tenant['org_a'],
        name='Base A',
        created_by=tenant['admin_a'],
    )
    base_b = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
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
    client_b = authenticated_client(tenant['admin_b'])

    assert client_b.post(
        f'/api/v1/knowledge-base/{base_a.id}/index-document/',
        {'document_id': str(document_a.id)},
        format='json',
    ).status_code == 404
    assert client_b.post(
        f'/api/v1/knowledge-base/{base_b.id}/index-document/',
        {'document_id': str(document_b.id)},
        format='json',
    ).status_code == 200

    response = client_b.post(
        f'/api/v1/knowledge-base/{base_b.id}/search/',
        {'query': 'comum', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert all(source['document_id'] == str(document_b.id) for source in response.data['sources'])


@pytest.mark.django_db
def test_ask_returns_sources_when_chunks_are_relevant():
    tenant = build_service_tenant_fixture()
    knowledge_base = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='A peticao inicial requer tutela de urgencia e juntada de documentos essenciais.',
    )
    client = authenticated_client(tenant['admin_b'])
    client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/index-document/',
        {'document_id': str(document.id)},
        format='json',
    )

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'O que a peticao inicial requer?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'completed'
    assert response.data['sources']
    assert 'base de conhecimento' in response.data['answer'].lower()


@pytest.mark.django_db
def test_ask_returns_no_sources_when_not_enough_information():
    tenant = build_service_tenant_fixture()
    knowledge_base = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    client = authenticated_client(tenant['admin_b'])

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Qual e a jurisprudencia sobre responsabilidade ambiental?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    assert response.data['status'] == 'no_sources'
    assert response.data['sources'] == []


@pytest.mark.django_db
def test_retrieval_query_is_associated_with_correct_organization():
    tenant = build_service_tenant_fixture()
    knowledge_base = KnowledgeBase.objects.create(
        organization=tenant['org_b'],
        name='Base B',
        created_by=tenant['admin_b'],
    )
    document = create_document(
        tenant=tenant,
        organization_key='org_b',
        case_key='case_b',
        content='Memorial descritivo com estrategia de defesa e honorarios.',
    )
    client = authenticated_client(tenant['admin_b'])
    client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/index-document/',
        {'document_id': str(document.id)},
        format='json',
    )

    response = client.post(
        f'/api/v1/knowledge-base/{knowledge_base.id}/ask/',
        {'query': 'Qual e a estrategia de defesa?', 'limit': 5},
        format='json',
    )

    assert response.status_code == 200
    query_record = RetrievalQuery.objects.get()
    assert query_record.organization == tenant['org_b']
    assert query_record.knowledge_base == knowledge_base
    assert query_record.created_by == tenant['admin_b']
