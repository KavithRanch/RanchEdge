import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture(scope="session")
def ev_endpoint() -> str:
    return "/api/v1/ev-opportunities"