import requests
import pytest
import pprint
import pydantic
import json
from category_service.schemas import PostCategory, Category
from product_service.schemas import Product, PostProduct


@pytest.fixture()
def base_url():
    port = '8080'
    api_version = 'v1'
    final_url = f'http://localhost:{port}/{api_version}'
    return final_url


@pytest.mark.parametrize('endpoint, schemas', [
    ('products', Product),
    ('categories', Category),
])
def test_get_endpoints(endpoint, schemas, base_url):
    response = requests.get(f'{base_url}/{endpoint}')
    assert response.status_code == 200
    output = 'output.txt'
    data = json.loads(response.content.decode())
    with open(output, 'a') as file:
        pprint.pprint(data, stream=file)

    collection = data[endpoint]
    if collection:
        for element in collection:
            assert schemas.validate(element)


@pytest.mark.parametrize('endpoint, schemas, body', [
    ('products/add', PostProduct, PostProduct(name='some name', description='some description', price=100)),
    # ('categories/add', Category),
])
def test_post_endpoints(endpoint, schemas, body, base_url):
    response = requests.post(
        f'{base_url}/{endpoint}',
        json=body.dict()
    )
    assert response.status_code == 200
    output = 'output.txt'
    data = json.loads(response.content.decode())
    with open(output, 'a') as file:
        pprint.pprint(data, stream=file)

    assert schemas.validate(data)
