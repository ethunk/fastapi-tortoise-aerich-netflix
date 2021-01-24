# Test Post
from starlette.testclient import TestClient
from app.main import create_application

TEST_BASE_URL = 'http://127.0.0.1:8000/'

client = TestClient(create_application())
show = {'type': 'Movie',
 'title': 'Norm of the North: King Sized Adventure',
 'date_added': '2021-01-19',
 'release_year': '2019',
 'rating': 'TV-PG',
 'duration': 90,
 'description': 'This is a test'}

assert client.post(url=TEST_BASE_URL + 'shows', json=show).ok is True
