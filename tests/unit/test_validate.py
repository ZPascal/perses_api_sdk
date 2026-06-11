import pytest
from perses_api.validate import Validate
from perses_api.model import APIModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


def test_validate_dashboard(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = Validate(model)
    client.validate(
        "dashboards", {"kind": "Dashboard", "metadata": {"name": "d"}, "spec": {}}
    )


def test_validate_datasource(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = Validate(model)
    client.validate(
        "datasources", {"kind": "Datasource", "metadata": {"name": "ds"}, "spec": {}}
    )


def test_validate_invalid_resource_type_raises(model):
    client = Validate(model)
    with pytest.raises(ValueError):
        client.validate("unsupported", {})


def test_validate_empty_body_raises(model):
    client = Validate(model)
    with pytest.raises(ValueError):
        client.validate("dashboards", {})
