from __future__ import annotations

from ._base import ResourceBase
from .model import APIModel, APIEndpoints


class SecretBase(ResourceBase):
    def get_secrets(self, name: str = None) -> list:
        return self._get_all(name)

    def get_secret(self, name: str) -> dict:
        return self._get_one(name)

    def create_secret(self, secret) -> dict:
        return self._create(secret)

    def update_secret(self, name: str, secret) -> dict:
        return self._update(name, secret)

    def delete_secret(self, name: str) -> None:
        self._delete(name)


class ProjectSecret(SecretBase):
    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.SECRETS.value.format(project=self.project_name)


class GlobalSecret(SecretBase):
    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_SECRETS.value
