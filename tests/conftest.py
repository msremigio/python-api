import pytest
from app.main import create_app


@pytest.fixture(scope='module')
def test_client(create_app):
    client = create_app()
