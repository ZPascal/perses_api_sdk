import pytest

from perses_api.datasource import GlobalDatasource, ProjectDatasource
from perses_api.model import APIModel, DatasourceSpec, Metadata
from perses_api.model import Datasource as DatasourceModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def ds_payload():
    return {
        "kind": "Datasource",
        "metadata": {"name": "prom", "project": "my-project"},
        "spec": {"default": True, "plugin": {"kind": "PrometheusPlugin", "spec": {}}},
    }


@pytest.fixture
def global_ds_payload():
    return {
        "kind": "GlobalDatasource",
        "metadata": {"name": "global-prom"},
        "spec": {"default": True, "plugin": {"kind": "PrometheusPlugin", "spec": {}}},
    }


def test_get_project_datasources(httpx_mock, model, ds_payload):
    httpx_mock.add_response(json=[ds_payload])
    client = ProjectDatasource(model, "my-project")
    result = client.get_datasources()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "prom"


def test_get_project_datasource(httpx_mock, model, ds_payload):
    httpx_mock.add_response(json=ds_payload)
    client = ProjectDatasource(model, "my-project")
    result = client.get_datasource("prom")
    assert result["metadata"]["name"] == "prom"


def test_create_project_datasource(httpx_mock, model, ds_payload):
    httpx_mock.add_response(json=ds_payload)
    client = ProjectDatasource(model, "my-project")
    body = DatasourceModel(
        metadata=Metadata(name="prom", project="my-project"),
        spec=DatasourceSpec(
            default=True, plugin={"kind": "PrometheusPlugin", "spec": {}}
        ),
    )
    result = client.create_datasource(body)
    assert result["kind"] == "Datasource"


def test_update_project_datasource(httpx_mock, model, ds_payload):
    httpx_mock.add_response(json=ds_payload)
    client = ProjectDatasource(model, "my-project")
    body = DatasourceModel(
        metadata=Metadata(name="prom", project="my-project"),
        spec=DatasourceSpec(
            default=True, plugin={"kind": "PrometheusPlugin", "spec": {}}
        ),
    )
    result = client.update_datasource("prom", body)
    assert result["metadata"]["name"] == "prom"


def test_delete_project_datasource(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = ProjectDatasource(model, "my-project")
    client.delete_datasource("prom")


def test_project_datasource_base_path(model):
    client = ProjectDatasource(model, "my-project")
    assert client._base_path() == "/api/v1/projects/my-project/datasources"


def test_get_global_datasources(httpx_mock, model, global_ds_payload):
    httpx_mock.add_response(json=[global_ds_payload])
    client = GlobalDatasource(model)
    result = client.get_datasources()
    assert result[0]["kind"] == "GlobalDatasource"


def test_global_datasource_base_path(model):
    client = GlobalDatasource(model)
    assert client._base_path() == "/api/v1/globaldatasources"


def test_get_datasource_empty_name_raises(model):
    client = ProjectDatasource(model, "my-project")
    with pytest.raises(ValueError):
        client.get_datasource("")
