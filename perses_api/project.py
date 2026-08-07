from __future__ import annotations

import logging

from .api import Api

logger = logging.getLogger(__name__)
from .model import APIEndpoints, APIModel, RequestsMethods
from .model import Project as ProjectModel


class Project:
    """The class includes all necessary methods to access the Perses projects API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_projects(self, name: str | None = None) -> list:
        """The method includes a functionality to retrieve all projects

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of project dicts
        """
        path = APIEndpoints.PROJECTS.value
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logger.error("Failed to retrieve projects.")
            raise TypeError(result)
        return result

    def get_project(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single project by name

        Args:
            name (str): Specify the name of the project to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The project dict
        """
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(APIEndpoints.PROJECT.value.format(project=name))
        if not isinstance(result, dict):
            logger.error(f"Failed to retrieve project: {name}")
            raise TypeError(result)
        return result

    def create_project(self, project: ProjectModel) -> dict:
        """The method includes a functionality to create a new project

        Args:
            project (Project): Specify the project resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created project dict
        """
        result = self.api.call_the_api(
            APIEndpoints.PROJECTS.value,
            method=RequestsMethods.POST,
            json_complete=project.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logger.error("Failed to create project.")
            raise TypeError(result)
        return result

    def update_project(self, name: str, project: ProjectModel) -> dict:
        """The method includes a functionality to update an existing project by name

        Args:
            name (str): Specify the name of the project to update
            project (Project): Specify the updated project resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated project dict
        """
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.PROJECT.value.format(project=name),
            method=RequestsMethods.PUT,
            json_complete=project.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logger.error(f"Failed to update project: {name}")
            raise TypeError(result)
        return result

    def delete_project(self, name: str) -> None:
        """The method includes a functionality to delete a project by name

        Args:
            name (str): Specify the name of the project to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.PROJECT.value.format(project=name),
            method=RequestsMethods.DELETE,
        )
