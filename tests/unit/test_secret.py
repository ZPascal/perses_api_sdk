import pytest
from perses_api.secret import ProjectSecret, GlobalSecret
from perses_api.model import APIModel, Metadata, SecretSpec
from perses_api.model import Secret as SecretModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def secret_payload():
    return {
        "kind": "Secret",
        "metadata": {"name": "my-secret", "project": "my-project"},
        "spec": {"kind": "BasicAuth", "spec": {"username": "user", "password": "pass"}},
    }


@pytest.fixture
def global_secret_payload():
    return {
        "kind": "GlobalSecret",
        "metadata": {"name": "global-secret"},
        "spec": {"kind": "BasicAuth", "spec": {"username": "user", "password": "pass"}},
    }


def test_get_project_secrets(httpx_mock, model, secret_payload):
    httpx_mock.add_response(json=[secret_payload])
    client = ProjectSecret(model, "my-project")
    result = client.get_secrets()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "my-secret"


def test_get_project_secret(httpx_mock, model, secret_payload):
    httpx_mock.add_response(json=secret_payload)
    client = ProjectSecret(model, "my-project")
    result = client.get_secret("my-secret")
    assert result["kind"] == "Secret"


def test_create_project_secret(httpx_mock, model, secret_payload):
    httpx_mock.add_response(json=secret_payload)
    client = ProjectSecret(model, "my-project")
    body = SecretModel(
        metadata=Metadata(name="my-secret", project="my-project"),
        spec=SecretSpec(
            kind="BasicAuth", spec={"username": "user", "password": "pass"}
        ),
    )
    result = client.create_secret(body)
    assert result["metadata"]["name"] == "my-secret"


def test_update_project_secret(httpx_mock, model, secret_payload):
    httpx_mock.add_response(json=secret_payload)
    client = ProjectSecret(model, "my-project")
    body = SecretModel(
        metadata=Metadata(name="my-secret", project="my-project"),
        spec=SecretSpec(
            kind="BasicAuth", spec={"username": "user", "password": "pass"}
        ),
    )
    result = client.update_secret("my-secret", body)
    assert result["metadata"]["name"] == "my-secret"


def test_delete_project_secret(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = ProjectSecret(model, "my-project")
    client.delete_secret("my-secret")


def test_project_secret_base_path(model):
    client = ProjectSecret(model, "my-project")
    assert client._base_path() == "/api/v1/projects/my-project/secrets"


def test_get_global_secrets(httpx_mock, model, global_secret_payload):
    httpx_mock.add_response(json=[global_secret_payload])
    client = GlobalSecret(model)
    result = client.get_secrets()
    assert result[0]["kind"] == "GlobalSecret"


def test_global_secret_base_path(model):
    client = GlobalSecret(model)
    assert client._base_path() == "/api/v1/globalsecrets"


def test_get_secret_empty_name_raises(model):
    client = ProjectSecret(model, "my-project")
    with pytest.raises(ValueError):
        client.get_secret("")
