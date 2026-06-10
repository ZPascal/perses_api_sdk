from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods
from .model import Project as ProjectModel


class Project:
    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_projects(self, name: str = None) -> list:
        path = APIEndpoints.PROJECTS.value
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logging.error("Failed to retrieve projects.")
            raise Exception(result)
        return result

    def get_project(self, name: str) -> dict:
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(APIEndpoints.PROJECT.value.format(project=name))
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve project: {name}")
            raise Exception(result)
        return result

    def create_project(self, project: ProjectModel) -> dict:
        result = self.api.call_the_api(
            APIEndpoints.PROJECTS.value,
            method=RequestsMethods.POST,
            json_complete=project.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error("Failed to create project.")
            raise Exception(result)
        return result

    def update_project(self, name: str, project: ProjectModel) -> dict:
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.PROJECT.value.format(project=name),
            method=RequestsMethods.PUT,
            json_complete=project.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update project: {name}")
            raise Exception(result)
        return result

    def delete_project(self, name: str) -> None:
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.PROJECT.value.format(project=name),
            method=RequestsMethods.DELETE,
        )
