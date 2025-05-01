import pytest
from app.main import create_app


@pytest.fixture(scope='module')
def test_client():
    client = create_app()
    with client.test_client() as test_client:
        with client.app_context():
            yield test_client
