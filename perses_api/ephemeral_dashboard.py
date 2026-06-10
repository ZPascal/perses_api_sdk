from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods
from .model import EphemeralDashboard as EphemeralDashboardModel


class EphemeralDashboard:
    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_ephemeral_dashboards(self, project_name: str, name: str = None) -> list:
        if not project_name:
            raise ValueError("project_name must not be empty")
        path = APIEndpoints.EPHEMERAL_DASHBOARDS.value.format(project=project_name)
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logging.error("Failed to retrieve ephemeral dashboards.")
            raise Exception(result)
        return result

    def get_ephemeral_dashboard(self, project_name: str, name: str) -> dict:
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARD.value.format(project=project_name, name=name)
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve ephemeral dashboard: {name}")
            raise Exception(result)
        return result

    def create_ephemeral_dashboard(
        self, project_name: str, ephemeral_dashboard: EphemeralDashboardModel
    ) -> dict:
        if not project_name:
            raise ValueError("project_name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARDS.value.format(project=project_name),
            method=RequestsMethods.POST,
            json_complete=ephemeral_dashboard.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error("Failed to create ephemeral dashboard.")
            raise Exception(result)
        return result

    def update_ephemeral_dashboard(
        self, project_name: str, name: str, ephemeral_dashboard: EphemeralDashboardModel
    ) -> dict:
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARD.value.format(project=project_name, name=name),
            method=RequestsMethods.PUT,
            json_complete=ephemeral_dashboard.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update ephemeral dashboard: {name}")
            raise Exception(result)
        return result

    def delete_ephemeral_dashboard(self, project_name: str, name: str) -> None:
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARD.value.format(project=project_name, name=name),
            method=RequestsMethods.DELETE,
        )
