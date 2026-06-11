import pytest
from perses_api.role import ProjectRole, GlobalRole
from perses_api.model import APIModel, Metadata, RoleSpec, Permission
from perses_api.model import Role as RoleModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def role_payload():
    return {
        "kind": "Role",
        "metadata": {"name": "editor", "project": "my-project"},
        "spec": {
            "permissions": [{"actions": ["read", "write"], "scopes": ["Dashboard"]}]
        },
    }


@pytest.fixture
def global_role_payload():
    return {
        "kind": "GlobalRole",
        "metadata": {"name": "global-admin"},
        "spec": {"permissions": [{"actions": ["*"], "scopes": ["*"]}]},
    }


def test_get_project_roles(httpx_mock, model, role_payload):
    httpx_mock.add_response(json=[role_payload])
    client = ProjectRole(model, "my-project")
    result = client.get_roles()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "editor"


def test_get_project_role(httpx_mock, model, role_payload):
    httpx_mock.add_response(json=role_payload)
    client = ProjectRole(model, "my-project")
    result = client.get_role("editor")
    assert result["kind"] == "Role"


def test_create_project_role(httpx_mock, model, role_payload):
    httpx_mock.add_response(json=role_payload)
    client = ProjectRole(model, "my-project")
    body = RoleModel(
        metadata=Metadata(name="editor", project="my-project"),
        spec=RoleSpec(permissions=[Permission(actions=["read"], scopes=["Dashboard"])]),
    )
    result = client.create_role(body)
    assert result["metadata"]["name"] == "editor"


def test_update_project_role(httpx_mock, model, role_payload):
    httpx_mock.add_response(json=role_payload)
    client = ProjectRole(model, "my-project")
    body = RoleModel(
        metadata=Metadata(name="editor", project="my-project"),
        spec=RoleSpec(permissions=[Permission(actions=["read"], scopes=["Dashboard"])]),
    )
    result = client.update_role("editor", body)
    assert result["metadata"]["name"] == "editor"


def test_delete_project_role(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = ProjectRole(model, "my-project")
    client.delete_role("editor")


def test_project_role_base_path(model):
    client = ProjectRole(model, "my-project")
    assert client._base_path() == "/api/v1/projects/my-project/roles"


def test_get_global_roles(httpx_mock, model, global_role_payload):
    httpx_mock.add_response(json=[global_role_payload])
    client = GlobalRole(model)
    result = client.get_roles()
    assert result[0]["kind"] == "GlobalRole"


def test_global_role_base_path(model):
    client = GlobalRole(model)
    assert client._base_path() == "/api/v1/globalroles"


def test_get_role_empty_name_raises(model):
    client = ProjectRole(model, "my-project")
    with pytest.raises(ValueError):
        client.get_role("")
