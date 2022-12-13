import requests
import pytest
import pprint
import pydantic
import json
from product_service.schemas import Product, PostProduct


@pytest.fixture
def service_url():
    port = '8001'
    api_version = 'v1'
    final_url = f'http://localhost:{port}/{api_version}'
    return final_url


@pytest.fixture
def api_gateway_url():
    port = '8080'
    api_version = 'v1'
    final_url = f'http://localhost:{port}/{api_version}'
    return final_url


@pytest.mark.parametrize('endpoint, schemas', [
    ('products', Product),
])
def test_get_endpoints(endpoint, schemas, service_url):
    response = requests.get(f'{service_url}/{endpoint}')
    assert response.status_code == 200
    data = json.loads(response.content.decode())
    collection = data
    if collection:
        for element in collection:
            assert schemas.validate(element)


@pytest.mark.parametrize('endpoint, schemas', [
    ('products', Product),
])
def test_protected_get_endpoints(endpoint, schemas, api_gateway_url):
    headers = {
        'accept': 'application/json',
    }

    data = {
        'grant_type': '',
        'username': 'alex',
        'password': '1234',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }

    urls = {
        'login': f'{api_gateway_url}/login',
        'products': f'{api_gateway_url}/products',
    }

    response = requests.post(urls['login'], headers=headers, data=data)
    assert response.status_code == 200
    user_access_token = json.loads(response.content.decode())['access_token']
    assert user_access_token != ''
    headers['Authorization'] = f'Bearer {user_access_token}'

    response = requests.get(urls['products'])
    assert response.status_code == 401

    response = requests.get(urls['products'], headers=headers)
    assert response.status_code == 200


@pytest.mark.parametrize('endpoint, schemas, body', [
    ('products/add', PostProduct, PostProduct(name='some name', description='some description', price=100)),
])
def test_post_endpoints(endpoint, schemas, body, service_url):
    response = requests.post(
        f'{service_url}/{endpoint}',
        json=body.dict()
    )
    assert response.status_code == 201
    data = json.loads(response.content.decode())
    assert schemas.validate(data)


