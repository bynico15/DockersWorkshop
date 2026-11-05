import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path) -> TestClient:
    with TestClient(create_app(str(tmp_path / "catalog.db"))) as test_client:
        yield test_client
