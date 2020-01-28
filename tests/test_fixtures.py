import pytest
from app import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app()
    client = app.test_client()

    return client