from __future__ import annotations

from ._base import ResourceBase
from .model import APIEndpoints, APIModel


class RoleBase(ResourceBase):
    """The class includes all necessary base methods to access the Perses roles API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def get_roles(self, name: str | None = None) -> list:
        """The method includes a functionality to retrieve all roles

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of role dicts
        """
        return self._get_all(name)

    def get_role(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single role by name

        Args:
            name (str): Specify the name of the role to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The role dict
        """
        return self._get_one(name)

    def create_role(self, role) -> dict:
        """The method includes a functionality to create a new role

        Args:
            role (Role | GlobalRole): Specify the role resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created role dict
        """
        return self._create(role)

    def update_role(self, name: str, role) -> dict:
        """The method includes a functionality to update an existing role by name

        Args:
            name (str): Specify the name of the role to update
            role (Role | GlobalRole): Specify the updated role resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated role dict
        """
        return self._update(name, role)

    def delete_role(self, name: str) -> None:
        """The method includes a functionality to delete a role by name

        Args:
            name (str): Specify the name of the role to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        self._delete(name)


class ProjectRole(RoleBase):
    """The class includes all necessary methods to access the Perses project-scoped roles API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information
        project_name (str): Specify the name of the project to scope role operations to

    Attributes:
        api (Api): This is where we store the api
        project_name (str): This is where we store the project_name
    """

    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.ROLES.value.format(project=self.project_name)


class GlobalRole(RoleBase):
    """The class includes all necessary methods to access the Perses global roles API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_ROLES.value
