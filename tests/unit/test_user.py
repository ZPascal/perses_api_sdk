import pytest

from perses_api.model import APIModel, Metadata, UserSpec
from perses_api.model import User as UserModel
from perses_api.user import User


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def user_payload():
    return {
        "kind": "User",
        "metadata": {"name": "alice"},
        "spec": {"first_name": "Alice", "last_name": "Smith"},
    }


def test_get_users(httpx_mock, model, user_payload):
    httpx_mock.add_response(json=[user_payload])
    client = User(model)
    result = client.get_users()
    assert isinstance(result, list)
    assert result[0]["metadata"]["name"] == "alice"


def test_get_users_filtered(httpx_mock, model, user_payload):
    httpx_mock.add_response(json=[user_payload])
    client = User(model)
    client.get_users(name="ali")
    request = httpx_mock.get_requests()[0]
    assert "name=ali" in str(request.url)


def test_get_user(httpx_mock, model, user_payload):
    httpx_mock.add_response(json=user_payload)
    client = User(model)
    result = client.get_user("alice")
    assert result["metadata"]["name"] == "alice"


def test_get_user_empty_name_raises(model):
    client = User(model)
    with pytest.raises(ValueError):
        client.get_user("")


def test_create_user(httpx_mock, model, user_payload):
    httpx_mock.add_response(json=user_payload)
    client = User(model)
    body = UserModel(
        metadata=Metadata(name="alice"),
        spec=UserSpec(first_name="Alice", last_name="Smith"),
    )
    result = client.create_user(body)
    assert result["metadata"]["name"] == "alice"


def test_update_user(httpx_mock, model, user_payload):
    httpx_mock.add_response(json=user_payload)
    client = User(model)
    body = UserModel(
        metadata=Metadata(name="alice"),
        spec=UserSpec(first_name="Alice", last_name="Jones"),
    )
    result = client.update_user("alice", body)
    assert result["metadata"]["name"] == "alice"


def test_update_user_empty_name_raises(model):
    client = User(model)
    body = UserModel(metadata=Metadata(name="alice"), spec=UserSpec())
    with pytest.raises(ValueError):
        client.update_user("", body)


def test_delete_user(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    client = User(model)
    client.delete_user("alice")


def test_delete_user_empty_name_raises(model):
    client = User(model)
    with pytest.raises(ValueError):
        client.delete_user("")
