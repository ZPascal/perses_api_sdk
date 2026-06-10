import pytest
from perses_api.variable import ProjectVariable, GlobalVariable
from perses_api.model import APIModel, Metadata, VariableSpec
from perses_api.model import Variable as VariableModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def var_payload():
    return {
        "kind": "Variable",
        "metadata": {"name": "env", "project": "my-project"},
        "spec": {"kind": "StaticListVariable", "spec": {"values": ["prod", "dev"]}},
    }


@pytest.fixture
def global_var_payload():
    return {
        "kind": "GlobalVariable",
        "metadata": {"name": "global-env"},
        "spec": {"kind": "StaticListVariable", "spec": {"values": ["prod", "dev"]}},
    }


def test_get_project_variables(httpx_mock, model, var_payload):
    httpx_mock.add_response(json=[var_payload])
    client = ProjectVariable(model, "my-project")
    result = client.get_variables()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "env"


def test_get_project_variable(httpx_mock, model, var_payload):
    httpx_mock.add_response(json=var_payload)
    client = ProjectVariable(model, "my-project")
    result = client.get_variable("env")
    assert result["kind"] == "Variable"


def test_create_project_variable(httpx_mock, model, var_payload):
    httpx_mock.add_response(json=var_payload)
    client = ProjectVariable(model, "my-project")
    body = VariableModel(
        metadata=Metadata(name="env", project="my-project"),
        spec=VariableSpec(kind="StaticListVariable", spec={"values": ["prod", "dev"]}),
    )
    result = client.create_variable(body)
    assert result["metadata"]["name"] == "env"


def test_update_project_variable(httpx_mock, model, var_payload):
    httpx_mock.add_response(json=var_payload)
    client = ProjectVariable(model, "my-project")
    body = VariableModel(
        metadata=Metadata(name="env", project="my-project"),
        spec=VariableSpec(kind="StaticListVariable", spec={"values": ["prod"]}),
    )
    result = client.update_variable("env", body)
    assert result["metadata"]["name"] == "env"


def test_delete_project_variable(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = ProjectVariable(model, "my-project")
    client.delete_variable("env")


def test_project_variable_base_path(model):
    client = ProjectVariable(model, "my-project")
    assert client._base_path() == "/api/v1/projects/my-project/variables"


def test_get_global_variables(httpx_mock, model, global_var_payload):
    httpx_mock.add_response(json=[global_var_payload])
    client = GlobalVariable(model)
    result = client.get_variables()
    assert result[0]["kind"] == "GlobalVariable"


def test_global_variable_base_path(model):
    client = GlobalVariable(model)
    assert client._base_path() == "/api/v1/globalvariables"


def test_get_variable_empty_name_raises(model):
    client = ProjectVariable(model, "my-project")
    with pytest.raises(ValueError):
        client.get_variable("")
