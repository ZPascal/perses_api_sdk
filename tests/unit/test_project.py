import pytest

from perses_api.model import APIModel, Metadata, ProjectSpec
from perses_api.model import Project as ProjectModel
from perses_api.project import Project


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def project_payload():
    return {"kind": "Project", "metadata": {"name": "my-project"}, "spec": {}}


def test_get_projects(httpx_mock, model, project_payload):
    httpx_mock.add_response(json=[project_payload])
    client = Project(model)
    result = client.get_projects()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "my-project"


def test_get_projects_filtered_by_name(httpx_mock, model, project_payload):
    httpx_mock.add_response(json=[project_payload])
    client = Project(model)
    client.get_projects(name="my")
    request = httpx_mock.get_requests()[0]
    assert "name=my" in str(request.url)


def test_get_project(httpx_mock, model, project_payload):
    httpx_mock.add_response(json=project_payload)
    client = Project(model)
    result = client.get_project("my-project")
    assert result["metadata"]["name"] == "my-project"


def test_get_project_empty_name_raises(model):
    client = Project(model)
    with pytest.raises(ValueError):
        client.get_project("")


def test_create_project(httpx_mock, model, project_payload):
    httpx_mock.add_response(json=project_payload)
    client = Project(model)
    body = ProjectModel(metadata=Metadata(name="my-project"), spec=ProjectSpec())
    result = client.create_project(body)
    assert result["metadata"]["name"] == "my-project"


def test_update_project(httpx_mock, model, project_payload):
    httpx_mock.add_response(json=project_payload)
    client = Project(model)
    body = ProjectModel(metadata=Metadata(name="my-project"), spec=ProjectSpec())
    result = client.update_project("my-project", body)
    assert result["metadata"]["name"] == "my-project"


def test_update_project_empty_name_raises(model):
    client = Project(model)
    body = ProjectModel(metadata=Metadata(name="x"), spec=ProjectSpec())
    with pytest.raises(ValueError):
        client.update_project("", body)


def test_delete_project(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = Project(model)
    client.delete_project("my-project")


def test_delete_project_empty_name_raises(model):
    client = Project(model)
    with pytest.raises(ValueError):
        client.delete_project("")
