from __future__ import annotations

from ._base import ResourceBase
from .model import APIModel, APIEndpoints


class RoleBase(ResourceBase):
    def get_roles(self, name: str = None) -> list:
        return self._get_all(name)

    def get_role(self, name: str) -> dict:
        return self._get_one(name)

    def create_role(self, role) -> dict:
        return self._create(role)

    def update_role(self, name: str, role) -> dict:
        return self._update(name, role)

    def delete_role(self, name: str) -> None:
        self._delete(name)


class ProjectRole(RoleBase):
    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.ROLES.value.format(project=self.project_name)


class GlobalRole(RoleBase):
    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_ROLES.value
