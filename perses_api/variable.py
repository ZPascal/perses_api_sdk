from __future__ import annotations

from ._base import ResourceBase
from .model import APIEndpoints, APIModel


class VariableBase(ResourceBase):
    """The class includes all necessary base methods to access the Perses variables API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def get_variables(self, name: str | None = None) -> list:
        """The method includes a functionality to retrieve all variables

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of variable dicts
        """
        return self._get_all(name)

    def get_variable(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single variable by name

        Args:
            name (str): Specify the name of the variable to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The variable dict
        """
        return self._get_one(name)

    def create_variable(self, variable) -> dict:
        """The method includes a functionality to create a new variable

        Args:
            variable (Variable | GlobalVariable): Specify the variable resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created variable dict
        """
        return self._create(variable)

    def update_variable(self, name: str, variable) -> dict:
        """The method includes a functionality to update an existing variable by name

        Args:
            name (str): Specify the name of the variable to update
            variable (Variable | GlobalVariable): Specify the updated variable resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated variable dict
        """
        return self._update(name, variable)

    def delete_variable(self, name: str) -> None:
        """The method includes a functionality to delete a variable by name

        Args:
            name (str): Specify the name of the variable to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        self._delete(name)


class ProjectVariable(VariableBase):
    """The class includes all necessary methods to access the Perses project-scoped variables API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information
        project_name (str): Specify the name of the project to scope variable operations to

    Attributes:
        api (Api): This is where we store the api
        project_name (str): This is where we store the project_name
    """

    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.VARIABLES.value.format(project=self.project_name)


class GlobalVariable(VariableBase):
    """The class includes all necessary methods to access the Perses global variables API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_VARIABLES.value
