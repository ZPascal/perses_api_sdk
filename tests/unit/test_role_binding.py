import pytest
from perses_api.role_binding import ProjectRoleBinding, GlobalRoleBinding
from perses_api.model import APIModel, Metadata, RoleBindingSpec, Subject
from perses_api.model import RoleBinding as RoleBindingModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def rb_payload():
    return {
        "kind": "RoleBinding",
        "metadata": {"name": "rb-1", "project": "my-project"},
        "spec": {"role": "editor", "subjects": [{"kind": "User", "name": "alice"}]},
    }


@pytest.fixture
def global_rb_payload():
    return {
        "kind": "GlobalRoleBinding",
        "metadata": {"name": "grb-1"},
        "spec": {"role": "global-admin", "subjects": [{"kind": "User", "name": "bob"}]},
    }


def test_get_project_role_bindings(httpx_mock, model, rb_payload):
    httpx_mock.add_response(json=[rb_payload])
    client = ProjectRoleBinding(model, "my-project")
    result = client.get_role_bindings()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "rb-1"


def test_get_project_role_binding(httpx_mock, model, rb_payload):
    httpx_mock.add_response(json=rb_payload)
    client = ProjectRoleBinding(model, "my-project")
    result = client.get_role_binding("rb-1")
    assert result["kind"] == "RoleBinding"


def test_create_project_role_binding(httpx_mock, model, rb_payload):
    httpx_mock.add_response(json=rb_payload)
    client = ProjectRoleBinding(model, "my-project")
    body = RoleBindingModel(
        metadata=Metadata(name="rb-1", project="my-project"),
        spec=RoleBindingSpec(role="editor", subjects=[Subject(kind="User", name="alice")]),
    )
    result = client.create_role_binding(body)
    assert result["metadata"]["name"] == "rb-1"


def test_update_project_role_binding(httpx_mock, model, rb_payload):
    httpx_mock.add_response(json=rb_payload)
    client = ProjectRoleBinding(model, "my-project")
    body = RoleBindingModel(
        metadata=Metadata(name="rb-1", project="my-project"),
        spec=RoleBindingSpec(role="editor", subjects=[Subject(kind="User", name="alice")]),
    )
    result = client.update_role_binding("rb-1", body)
    assert result["metadata"]["name"] == "rb-1"


def test_delete_project_role_binding(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = ProjectRoleBinding(model, "my-project")
    client.delete_role_binding("rb-1")


def test_project_role_binding_base_path(model):
    client = ProjectRoleBinding(model, "my-project")
    assert client._base_path() == "/api/v1/projects/my-project/rolebindings"


def test_get_global_role_bindings(httpx_mock, model, global_rb_payload):
    httpx_mock.add_response(json=[global_rb_payload])
    client = GlobalRoleBinding(model)
    result = client.get_role_bindings()
    assert result[0]["kind"] == "GlobalRoleBinding"


def test_global_role_binding_base_path(model):
    client = GlobalRoleBinding(model)
    assert client._base_path() == "/api/v1/globalrolebindings"


def test_get_role_binding_empty_name_raises(model):
    client = ProjectRoleBinding(model, "my-project")
    with pytest.raises(ValueError):
        client.get_role_binding("")
