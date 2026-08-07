import pytest

from perses_api.ephemeral_dashboard import EphemeralDashboard
from perses_api.model import APIModel, EphemeralDashboardSpec, Metadata
from perses_api.model import EphemeralDashboard as EphemeralDashboardModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def payload():
    return {
        "kind": "EphemeralDashboard",
        "metadata": {"name": "ed-1", "project": "my-project"},
        "spec": {"ttl": "1h"},
    }


def test_get_ephemeral_dashboards(httpx_mock, model, payload):
    httpx_mock.add_response(json=[payload])
    client = EphemeralDashboard(model)
    result = client.get_ephemeral_dashboards("my-project")
    assert isinstance(result, list)
    assert result[0]["spec"]["ttl"] == "1h"


def test_get_ephemeral_dashboard(httpx_mock, model, payload):
    httpx_mock.add_response(json=payload)
    client = EphemeralDashboard(model)
    result = client.get_ephemeral_dashboard("my-project", "ed-1")
    assert result["metadata"]["name"] == "ed-1"


def test_get_ephemeral_dashboard_empty_args_raises(model):
    client = EphemeralDashboard(model)
    with pytest.raises(ValueError):
        client.get_ephemeral_dashboard("", "ed-1")
    with pytest.raises(ValueError):
        client.get_ephemeral_dashboard("my-project", "")


def test_create_ephemeral_dashboard(httpx_mock, model, payload):
    httpx_mock.add_response(json=payload)
    client = EphemeralDashboard(model)
    body = EphemeralDashboardModel(
        metadata=Metadata(name="ed-1", project="my-project"),
        spec=EphemeralDashboardSpec(ttl="1h"),
    )
    result = client.create_ephemeral_dashboard("my-project", body)
    assert result["kind"] == "EphemeralDashboard"


def test_update_ephemeral_dashboard(httpx_mock, model, payload):
    httpx_mock.add_response(json=payload)
    client = EphemeralDashboard(model)
    body = EphemeralDashboardModel(
        metadata=Metadata(name="ed-1", project="my-project"),
        spec=EphemeralDashboardSpec(ttl="2h"),
    )
    result = client.update_ephemeral_dashboard("my-project", "ed-1", body)
    assert result["metadata"]["name"] == "ed-1"


def test_delete_ephemeral_dashboard(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = EphemeralDashboard(model)
    client.delete_ephemeral_dashboard("my-project", "ed-1")


def test_delete_ephemeral_dashboard_empty_args_raises(model):
    client = EphemeralDashboard(model)
    with pytest.raises(ValueError):
        client.delete_ephemeral_dashboard("", "ed-1")
