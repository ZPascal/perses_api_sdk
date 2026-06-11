from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods
from .model import EphemeralDashboard as EphemeralDashboardModel


class EphemeralDashboard:
    """The class includes all necessary methods to access the Perses ephemeral dashboards API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_ephemeral_dashboards(self, project_name: str, name: str = None) -> list:
        """The method includes a functionality to retrieve all ephemeral dashboards within a project

        Args:
            project_name (str): Specify the name of the project to list ephemeral dashboards for
            name (str): Specify a name to filter the results (default None)

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of ephemeral dashboard dicts
        """
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
        """The method includes a functionality to retrieve a single ephemeral dashboard by name

        Args:
            project_name (str): Specify the name of the project the ephemeral dashboard belongs to
            name (str): Specify the name of the ephemeral dashboard to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The ephemeral dashboard dict
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARD.value.format(
                project=project_name, name=name
            )
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve ephemeral dashboard: {name}")
            raise Exception(result)
        return result

    def create_ephemeral_dashboard(
        self, project_name: str, ephemeral_dashboard: EphemeralDashboardModel
    ) -> dict:
        """The method includes a functionality to create a new ephemeral dashboard within a project

        Args:
            project_name (str): Specify the name of the project to create the ephemeral dashboard in
            ephemeral_dashboard (EphemeralDashboard): Specify the ephemeral dashboard resource to create

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created ephemeral dashboard dict
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARDS.value.format(project=project_name),
            method=RequestsMethods.POST,
            json_complete=ephemeral_dashboard.model_dump_json(
                by_alias=True, exclude_none=True
            ),
        )
        if not isinstance(result, dict):
            logging.error("Failed to create ephemeral dashboard.")
            raise Exception(result)
        return result

    def update_ephemeral_dashboard(
        self, project_name: str, name: str, ephemeral_dashboard: EphemeralDashboardModel
    ) -> dict:
        """The method includes a functionality to update an existing ephemeral dashboard by name

        Args:
            project_name (str): Specify the name of the project the ephemeral dashboard belongs to
            name (str): Specify the name of the ephemeral dashboard to update
            ephemeral_dashboard (EphemeralDashboard): Specify the updated ephemeral dashboard resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated ephemeral dashboard dict
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARD.value.format(
                project=project_name, name=name
            ),
            method=RequestsMethods.PUT,
            json_complete=ephemeral_dashboard.model_dump_json(
                by_alias=True, exclude_none=True
            ),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update ephemeral dashboard: {name}")
            raise Exception(result)
        return result

    def delete_ephemeral_dashboard(self, project_name: str, name: str) -> None:
        """The method includes a functionality to delete an ephemeral dashboard by name

        Args:
            project_name (str): Specify the name of the project the ephemeral dashboard belongs to
            name (str): Specify the name of the ephemeral dashboard to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        if not project_name:
            raise ValueError("project_name must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.EPHEMERAL_DASHBOARD.value.format(
                project=project_name, name=name
            ),
            method=RequestsMethods.DELETE,
        )
