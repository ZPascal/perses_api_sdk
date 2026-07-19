import json

import pytest
from perses_api.migrate import Migrate
from perses_api.model import APIModel


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


def test_migrate_dashboard(httpx_mock, model):
    perses_dashboard = {
        "kind": "Dashboard",
        "metadata": {"name": "migrated"},
        "spec": {},
    }
    httpx_mock.add_response(json=perses_dashboard)
    client = Migrate(model)
    result = client.migrate(
        grafana_dashboard={"title": "My Grafana Dashboard", "panels": []}
    )
    assert result["kind"] == "Dashboard"


def test_migrate_with_input(httpx_mock, model):
    perses_dashboard = {
        "kind": "Dashboard",
        "metadata": {"name": "migrated"},
        "spec": {},
    }
    httpx_mock.add_response(json=perses_dashboard)
    client = Migrate(model)
    client.migrate(
        grafana_dashboard={"title": "My Dashboard", "panels": []},
        migration_input={"env": "prod"},
    )
    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["input"] == {"env": "prod"}


def test_migrate_empty_dashboard_raises(model):
    client = Migrate(model)
    with pytest.raises(ValueError):
        client.migrate(grafana_dashboard={})


def test_migrate_result_missing_kind_raises(httpx_mock, model):
    error_response = {"message": "internal server error"}
    httpx_mock.add_response(json=error_response)
    client = Migrate(model)
    with pytest.raises(Exception) as exc_info:
        client.migrate(grafana_dashboard={"title": "Test"})
    assert exc_info.value.args[0] == error_response


def test_migrate_result_missing_kind_with_message(httpx_mock, model, caplog):
    error_response = {"message": "Cue validation failed"}
    httpx_mock.add_response(json=error_response)
    client = Migrate(model)
    with pytest.raises(Exception):
        client.migrate(grafana_dashboard={"title": "Test"})
    assert "Migration failed: Cue validation failed" in caplog.text


def test_migrate_result_missing_kind_without_message(httpx_mock, model, caplog):
    error_response = {"error": "some error"}
    httpx_mock.add_response(json=error_response)
    client = Migrate(model)
    with pytest.raises(Exception) as exc_info:
        client.migrate(grafana_dashboard={"title": "Test"})
    assert "Migration failed: Unknown error" in caplog.text
    assert exc_info.value.args[0] == error_response


def test_migrate_result_with_kind_succeeds(httpx_mock, model):
    valid_response = {
        "kind": "Dashboard",
        "metadata": {"name": "test"},
        "spec": {"display": {"name": "Test"}},
    }
    httpx_mock.add_response(json=valid_response)
    client = Migrate(model)
    result = client.migrate(grafana_dashboard={"title": "Test"})
    assert result == valid_response
    assert result["kind"] == "Dashboard"
