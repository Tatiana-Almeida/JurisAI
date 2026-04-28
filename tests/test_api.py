import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from organizations.models import Organization
from accounts.models import User
from law_cases.models import LawCase

@pytest.mark.django_db
def test_jwt_login_refresh_and_protected_endpoint():
    org = Organization.objects.create(name='Escritorio Demo', plan='free')
    admin = User.objects.create_user(
        email='admin@example.com',
        password='strongpass123',
        name='Administrador',
        organization=org,
        role='admin',
        is_staff=True,
    )

    client = APIClient()
    token_response = client.post(reverse('token_obtain_pair'), {'email': admin.email, 'password': 'strongpass123'}, format='json')
    assert token_response.status_code == 200
    assert 'access' in token_response.data
    assert 'refresh' in token_response.data

    refresh_response = client.post(reverse('token_refresh'), {'refresh': token_response.data['refresh']}, format='json')
    assert refresh_response.status_code == 200
    assert 'access' in refresh_response.data

    access_token = refresh_response.data['access']
    protected = client.get('/api/v1/users/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert protected.status_code == 200

@pytest.mark.django_db
def test_create_and_list_cases_for_organization():
    org = Organization.objects.create(name='Escritorio Demo', plan='free')
    admin = User.objects.create_user(
        email='admin@example.com',
        password='strongpass123',
        name='Administrador',
        organization=org,
        role='admin',
        is_staff=True,
    )
    lawyer = User.objects.create_user(
        email='lawyer@example.com',
        password='strongpass123',
        name='Advogado',
        organization=org,
        role='advogado',
    )
    client_user = User.objects.create_user(
        email='cliente@example.com',
        password='strongpass123',
        name='Cliente',
        organization=org,
        role='cliente',
    )

    client = APIClient()
    token_response = client.post(reverse('token_obtain_pair'), {'email': admin.email, 'password': 'strongpass123'}, format='json')
    access_token = token_response.data['access']

    case_response = client.post(
        '/api/v1/cases/',
        {
            'title': 'Ação Trabalhista',
            'description': 'Reclamação de horas extras',
            'client_id': str(client_user.id),
            'lawyer_id': str(lawyer.id),
            'organization_id': str(org.id),
            'status': 'open',
        },
        HTTP_AUTHORIZATION=f'Bearer {access_token}',
        format='json'
    )
    assert case_response.status_code == 201
    assert case_response.data['title'] == 'Ação Trabalhista'

    list_response = client.get('/api/v1/cases/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert list_response.status_code == 200
    assert list_response.data['count'] == 1
    assert list_response.data['results'][0]['organization_id'] == str(org.id)

@pytest.mark.django_db
def test_tenant_isolation_between_organizations():
    org_a = Organization.objects.create(name='Org A', plan='free')
    org_b = Organization.objects.create(name='Org B', plan='free')

    admin_a = User.objects.create_user(
        email='admin_a@example.com',
        password='strongpass123',
        name='Admin A',
        organization=org_a,
        role='admin',
        is_staff=True,
    )
    admin_b = User.objects.create_user(
        email='admin_b@example.com',
        password='strongpass123',
        name='Admin B',
        organization=org_b,
        role='admin',
        is_staff=True,
    )
    lawyer_a = User.objects.create_user(
        email='lawyer_a@example.com',
        password='strongpass123',
        name='Advogado A',
        organization=org_a,
        role='advogado',
    )
    client_a = User.objects.create_user(
        email='cliente_a@example.com',
        password='strongpass123',
        name='Cliente A',
        organization=org_a,
        role='cliente',
    )

    LawCase.objects.create(
        title='Caso Org A',
        description='Processo exclusivo Org A',
        client=client_a,
        lawyer=lawyer_a,
        organization=org_a,
        status='open',
    )

    client = APIClient()
    token_response = client.post(reverse('token_obtain_pair'), {'email': admin_b.email, 'password': 'strongpass123'}, format='json')
    access_b = token_response.data['access']

    list_response = client.get('/api/v1/cases/', HTTP_AUTHORIZATION=f'Bearer {access_b}')
    assert list_response.status_code == 200
    assert list_response.data['count'] == 0

@pytest.mark.django_db
def test_user_profile_endpoint():
    org = Organization.objects.create(name='Escritorio Demo', plan='free')
    user = User.objects.create_user(
        email='user@example.com',
        password='strongpass123',
        name='Usuário',
        organization=org,
        role='admin',
    )

    client = APIClient()
    token_response = client.post(reverse('token_obtain_pair'), {'email': user.email, 'password': 'strongpass123'}, format='json')
    access_token = token_response.data['access']

    profile_response = client.get('/api/v1/users/profile/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert profile_response.status_code == 200
    assert profile_response.data['email'] == user.email

    update_response = client.patch(
        '/api/v1/users/profile/',
        {'name': 'Usuário Atualizado'},
        HTTP_AUTHORIZATION=f'Bearer {access_token}',
        format='json'
    )
    assert update_response.status_code == 200
    assert update_response.data['name'] == 'Usuário Atualizado'

@pytest.mark.django_db
def test_ai_history_route():
    org = Organization.objects.create(name='Juris AI', plan='free')
    admin = User.objects.create_user(
        email='admin-juris@example.com',
        password='strongpass123',
        name='Admin Juris',
        organization=org,
        role='admin',
        is_staff=True,
    )
    from ai_assistant.models import AIRequest

    AIRequest.objects.create(
        user=admin,
        organization=org,
        prompt='Teste de IA',
        response='Resposta de teste',
    )

    client = APIClient()
    token_response = client.post(reverse('token_obtain_pair'), {'email': admin.email, 'password': 'strongpass123'}, format='json')
    access_token = token_response.data['access']

    history_response = client.get('/api/v1/ai/history/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert history_response.status_code == 200
    assert history_response.data['count'] == 1
