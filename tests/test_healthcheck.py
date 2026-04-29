import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_healthcheck_returns_ok_without_authentication():
    client = APIClient()

    response = client.get('/health/')
    payload = response.json()

    assert response.status_code == 200
    assert payload['status'] == 'ok'
    assert payload['service'] == 'jurisai'
    assert payload['version'] == 'v0.11.0'


@pytest.mark.django_db
def test_legacy_api_healthcheck_route_still_works():
    client = APIClient()

    response = client.get('/api/v1/health/')
    payload = response.json()

    assert response.status_code == 200
    assert payload['status'] == 'ok'
    assert payload['service'] == 'jurisai'
