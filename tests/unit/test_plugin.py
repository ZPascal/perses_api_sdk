import pytest

from perses_api.model import APIModel
from perses_api.plugin import Plugin


@pytest.fixture
def model():
    return APIModel(host="http://localhost:8080", token="test-token")


def test_get_plugins(httpx_mock, model):
    httpx_mock.add_response(
        json=[
            {
                "kind": "PluginModule",
                "metadata": {"name": "prometheus", "version": "1.0.0"},
                "spec": {"plugins": []},
            }
        ]
    )
    client = Plugin(model)
    result = client.get_plugins()
    assert isinstance(result, list)
    assert result[0]["kind"] == "PluginModule"
