import json
import pytest
from perses_api.api import Api
from perses_api.model import APIModel, RequestsMethods


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


@pytest.fixture
def basic_auth_model():
    return APIModel(host="http://localhost:8080", username="admin", password="secret")


def test_get_request_returns_json(httpx_mock, model):
    httpx_mock.add_response(
        json={"kind": "Project", "metadata": {"name": "p1"}, "spec": {}}
    )
    api = Api(model)
    result = api.call_the_api("/api/v1/projects/p1")
    assert result["kind"] == "Project"


def test_post_request_sends_body(httpx_mock, model):
    httpx_mock.add_response(
        json={"kind": "Project", "metadata": {"name": "new"}, "spec": {}}
    )
    api = Api(model)
    body = json.dumps({"kind": "Project", "metadata": {"name": "new"}, "spec": {}})
    result = api.call_the_api(
        "/api/v1/projects", method=RequestsMethods.POST, json_complete=body
    )
    assert result["metadata"]["name"] == "new"


def test_put_request(httpx_mock, model):
    httpx_mock.add_response(
        json={"kind": "Project", "metadata": {"name": "p1"}, "spec": {}}
    )
    api = Api(model)
    body = json.dumps({"kind": "Project", "metadata": {"name": "p1"}, "spec": {}})
    result = api.call_the_api(
        "/api/v1/projects/p1", method=RequestsMethods.PUT, json_complete=body
    )
    assert result["metadata"]["name"] == "p1"


def test_delete_request(httpx_mock, model):
    httpx_mock.add_response(status_code=200, text="")
    api = Api(model)
    result = api.call_the_api("/api/v1/projects/p1", method=RequestsMethods.DELETE)
    assert result is not None


def test_bearer_auth_header(httpx_mock, model):
    httpx_mock.add_response(json={})
    api = Api(model)
    api.call_the_api("/api/v1/projects")
    request = httpx_mock.get_requests()[0]
    assert request.headers["authorization"] == "Bearer test-token"


def test_basic_auth_header(httpx_mock, basic_auth_model):
    httpx_mock.add_response(json={})
    api = Api(basic_auth_model)
    api.call_the_api("/api/v1/projects")
    request = httpx_mock.get_requests()[0]
    assert request.headers["authorization"].startswith("Basic ")


def test_response_status_code_included(httpx_mock, model):
    httpx_mock.add_response(json={"kind": "Project"}, status_code=201)
    api = Api(model)
    result = api.call_the_api("/api/v1/projects", response_status_code=True)
    assert result["status"] == 201


def test_post_without_body_raises(model):
    api = Api(model)
    with pytest.raises(Exception):
        api.call_the_api(
            "/api/v1/projects", method=RequestsMethods.POST, json_complete=None
        )


def test_non_json_response_returned_as_response(httpx_mock, model):
    httpx_mock.add_response(status_code=204, text="")
    api = Api(model)
    result = api.call_the_api("/api/v1/projects/p1", method=RequestsMethods.DELETE)
    assert result is not None
