from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods
from .model import Dashboard as DashboardModel


class Dashboard:
    """The class includes all necessary methods to access the Perses dashboards API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_dashboards(self, project_name: str, name: str = None) -> list:
        """The method includes a functionality to retrieve all dashboards within a project

        Args:
            project_name (str): Specify the name of the project to list dashboards for
            name (str): Specify a name to filter the results (default None)

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of dashboard dicts
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        path = APIEndpoints.DASHBOARDS.value.format(project=project_name)
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logging.error("Failed to retrieve dashboards.")
            raise Exception(result)
        return result

    def get_dashboard(self, project_name: str, name: str) -> dict:
        """The method includes a functionality to retrieve a single dashboard by name

        Args:
            project_name (str): Specify the name of the project the dashboard belongs to
            name (str): Specify the name of the dashboard to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The dashboard dict
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.DASHBOARD.value.format(project=project_name, name=name)
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve dashboard: {name}")
            raise Exception(result)
        return result

    def create_dashboard(self, project_name: str, dashboard: DashboardModel) -> dict:
        """The method includes a functionality to create a new dashboard within a project

        Args:
            project_name (str): Specify the name of the project to create the dashboard in
            dashboard (Dashboard): Specify the dashboard resource to create

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created dashboard dict
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.DASHBOARDS.value.format(project=project_name),
            method=RequestsMethods.POST,
            json_complete=dashboard.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logging.error("Failed to create dashboard.")
            raise Exception(result)
        return result

    def update_dashboard(
        self, project_name: str, name: str, dashboard: DashboardModel
    ) -> dict:
        """The method includes a functionality to update an existing dashboard by name

        Args:
            project_name (str): Specify the name of the project the dashboard belongs to
            name (str): Specify the name of the dashboard to update
            dashboard (Dashboard): Specify the updated dashboard resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated dashboard dict
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.DASHBOARD.value.format(project=project_name, name=name),
            method=RequestsMethods.PUT,
            json_complete=dashboard.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update dashboard: {name}")
            raise Exception(result)
        return result

    def delete_dashboard(self, project_name: str, name: str) -> None:
        """The method includes a functionality to delete a dashboard by name

        Args:
            project_name (str): Specify the name of the project the dashboard belongs to
            name (str): Specify the name of the dashboard to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.DASHBOARD.value.format(project=project_name, name=name),
            method=RequestsMethods.DELETE,
        )
