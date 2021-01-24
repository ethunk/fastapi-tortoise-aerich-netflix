import asyncio
import logging

import pytest
from app.main import app
from app.models import Content
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

log = logging.getLogger(__name__)

LOOP = asyncio.get_event_loop()
TEST_DATA_1 =     {
        'type': 'Movie',
        'title': 'The Count of Monte Cristo',
        'date_added': '2021-01-19',
        'release_year': '2003',
        'rating': 'TV-PG',
        'duration': 109,
        'description': 'Edmond Dantes is The Count.',
    }
TEST_DATA_2 =     {
        'type': 'Show',
        'title': 'The Office',
        'date_added': '2021-01-19',
        'release_year': 2003,
        'rating': 'TV-PG',
        'duration': 109,
        'description': 'Most watched show of 2020',
    }

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
def client(event_loop):
    initializer(['app.models'])
    with TestClient(app) as client:
        yield client
    finalizer()

@pytest.mark.asyncio
def test_create_content(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    """Successful response contains id of newly created object"""
    response = client.post('/content', json=TEST_DATA_1)
    new_content_id = response.json().get('id')

    assert response.status_code == 200
    assert type(new_content_id) is int

    async def delete_content_by(id):
        return await Content.get(id=id).delete()

    event_loop.run_until_complete(delete_content_by(new_content_id))


@pytest.mark.asyncio
def test_retrieve_content(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    """GET on '/contents' retrieves list of content"""
    response = client.get('/content')

    assert response.status_code == 200
    assert type(response.json()['items']) is list
    assert len(response.json()['items']) > 0


@pytest.mark.asyncio
def test_retrieve_content(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    """GET on '/contents/{id}' retrieves a single instance of Content"""
    response = client.post('/content', json=TEST_DATA_1)
    content_id = response.json().get('id')

    response = client.get(f'/content/{content_id}')

    for key in TEST_DATA_1.keys():
        assert key in list(response.json().keys())

    async def delete_content_by(id):
        return await Content.get(id=id).delete()

    event_loop.run_until_complete(delete_content_by(content_id))


@pytest.mark.asyncio
def test_update_content(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    """PATCH on '/contents/{id}' updates a existing content"""
    response = client.post("/content", json=TEST_DATA_1)
    content_id = response.json().get('id')
    response = client.patch(f'/content/{content_id}', json=TEST_DATA_2)

    assert response.status_code == 200
    updated_content = response.json()
    for key, value in TEST_DATA_2.items():
        assert updated_content[key] == value

    async def delete_content_by(id):
        return await Content.get(id=id).delete()

    event_loop.run_until_complete(delete_content_by(updated_content['id']))
