import pytest
from perses_api.dashboard import Dashboard
from perses_api.model import APIModel, Metadata, DashboardSpec
from perses_api.model import Dashboard as DashboardModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def dashboard_payload():
    return {"kind": "Dashboard", "metadata": {"name": "my-dash", "project": "my-project"}, "spec": {}}


def test_get_dashboards(httpx_mock, model, dashboard_payload):
    httpx_mock.add_response(json=[dashboard_payload])
    client = Dashboard(model)
    result = client.get_dashboards("my-project")
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "my-dash"


def test_get_dashboards_filtered(httpx_mock, model, dashboard_payload):
    httpx_mock.add_response(json=[dashboard_payload])
    client = Dashboard(model)
    result = client.get_dashboards("my-project", name="my")
    request = httpx_mock.get_requests()[0]
    assert "name=my" in str(request.url)


def test_get_dashboard(httpx_mock, model, dashboard_payload):
    httpx_mock.add_response(json=dashboard_payload)
    client = Dashboard(model)
    result = client.get_dashboard("my-project", "my-dash")
    assert result["metadata"]["name"] == "my-dash"


def test_get_dashboard_empty_args_raises(model):
    client = Dashboard(model)
    with pytest.raises(ValueError):
        client.get_dashboard("", "my-dash")
    with pytest.raises(ValueError):
        client.get_dashboard("my-project", "")


def test_create_dashboard(httpx_mock, model, dashboard_payload):
    httpx_mock.add_response(json=dashboard_payload)
    client = Dashboard(model)
    body = DashboardModel(metadata=Metadata(name="my-dash", project="my-project"), spec=DashboardSpec())
    result = client.create_dashboard("my-project", body)
    assert result["kind"] == "Dashboard"


def test_update_dashboard(httpx_mock, model, dashboard_payload):
    httpx_mock.add_response(json=dashboard_payload)
    client = Dashboard(model)
    body = DashboardModel(metadata=Metadata(name="my-dash", project="my-project"), spec=DashboardSpec())
    result = client.update_dashboard("my-project", "my-dash", body)
    assert result["metadata"]["name"] == "my-dash"


def test_delete_dashboard(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = Dashboard(model)
    client.delete_dashboard("my-project", "my-dash")


def test_delete_dashboard_empty_args_raises(model):
    client = Dashboard(model)
    with pytest.raises(ValueError):
        client.delete_dashboard("", "my-dash")
