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
