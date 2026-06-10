from __future__ import annotations

from ._base import ResourceBase
from .model import APIModel, APIEndpoints


class DatasourceBase(ResourceBase):
    def get_datasources(self, name: str = None) -> list:
        return self._get_all(name)

    def get_datasource(self, name: str) -> dict:
        return self._get_one(name)

    def create_datasource(self, datasource) -> dict:
        return self._create(datasource)

    def update_datasource(self, name: str, datasource) -> dict:
        return self._update(name, datasource)

    def delete_datasource(self, name: str) -> None:
        self._delete(name)


class ProjectDatasource(DatasourceBase):
    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.DATASOURCES.value.format(project=self.project_name)


class GlobalDatasource(DatasourceBase):
    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_DATASOURCES.value
