from __future__ import annotations

from ._base import ResourceBase
from .model import APIModel, APIEndpoints


class VariableBase(ResourceBase):
    def get_variables(self, name: str = None) -> list:
        return self._get_all(name)

    def get_variable(self, name: str) -> dict:
        return self._get_one(name)

    def create_variable(self, variable) -> dict:
        return self._create(variable)

    def update_variable(self, name: str, variable) -> dict:
        return self._update(name, variable)

    def delete_variable(self, name: str) -> None:
        self._delete(name)


class ProjectVariable(VariableBase):
    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.VARIABLES.value.format(project=self.project_name)


class GlobalVariable(VariableBase):
    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_VARIABLES.value
