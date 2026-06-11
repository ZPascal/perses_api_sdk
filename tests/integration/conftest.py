import os

import httpx
import pytest

from perses_api import APIModel


def pytest_collection_modifyitems(items):
    """Auto-mark every test collected from tests/integration/ as integration."""
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


def _obtain_token(host: str, username: str, password: str) -> str:
    """Exchange native credentials for a bearer token via the Perses auth endpoint."""
    response = httpx.post(
        f"{host}/api/auth/providers/native/login",
        json={"login": username, "password": password},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def perses_client():
    host = os.environ.get("PERSES_HOST", "http://localhost:8080")
    token = os.environ.get("PERSES_TOKEN")
    username = os.environ.get("PERSES_USERNAME")
    password = os.environ.get("PERSES_PASSWORD")

    if not token and username and password:
        token = _obtain_token(host, username, password)

    return APIModel(host=host, token=token)
