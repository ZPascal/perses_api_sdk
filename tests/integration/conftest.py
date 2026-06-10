import os
import pytest
from perses_api import APIModel


@pytest.fixture(scope="session")
def perses_client():
    host = os.environ.get("PERSES_HOST")
    token = os.environ.get("PERSES_TOKEN")
    if not host or not token:
        pytest.skip("PERSES_HOST and PERSES_TOKEN required for integration tests")
    return APIModel(host=host, token=token)
