from __future__ import annotations

from ._base import ResourceBase
from .model import APIModel, APIEndpoints


class RoleBindingBase(ResourceBase):
    def get_role_bindings(self, name: str = None) -> list:
        return self._get_all(name)

    def get_role_binding(self, name: str) -> dict:
        return self._get_one(name)

    def create_role_binding(self, role_binding) -> dict:
        return self._create(role_binding)

    def update_role_binding(self, name: str, role_binding) -> dict:
        return self._update(name, role_binding)

    def delete_role_binding(self, name: str) -> None:
        self._delete(name)


class ProjectRoleBinding(RoleBindingBase):
    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.ROLE_BINDINGS.value.format(project=self.project_name)


class GlobalRoleBinding(RoleBindingBase):
    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_ROLE_BINDINGS.value
