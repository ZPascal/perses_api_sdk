from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, RequestsMethods


class ResourceBase:
    """Shared CRUD for dual-scoped resources. Subclasses implement _base_path()."""

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def _base_path(self) -> str:
        raise NotImplementedError

    def _get_all(self, name: str = None) -> list:
        path = self._base_path()
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logging.error(f"Failed to retrieve resources from {self._base_path()}.")
            raise Exception(result)
        return result

    def _get_one(self, name: str) -> dict:
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(f"{self._base_path()}/{name}")
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve resource: {name}")
            raise Exception(result)
        return result

    def _create(self, body) -> dict:
        result = self.api.call_the_api(
            self._base_path(),
            method=RequestsMethods.POST,
            json_complete=body.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to create resource at {self._base_path()}.")
            raise Exception(result)
        return result

    def _update(self, name: str, body) -> dict:
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            f"{self._base_path()}/{name}",
            method=RequestsMethods.PUT,
            json_complete=body.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update resource: {name}")
            raise Exception(result)
        return result

    def _delete(self, name: str) -> None:
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(f"{self._base_path()}/{name}", method=RequestsMethods.DELETE)
