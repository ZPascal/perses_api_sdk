from __future__ import annotations

from ._base import ResourceBase
from .model import APIEndpoints, APIModel


class RoleBindingBase(ResourceBase):
    """The class includes all necessary base methods to access the Perses role bindings API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def get_role_bindings(self, name: str | None = None) -> list:
        """The method includes a functionality to retrieve all role bindings

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of role binding dicts
        """
        return self._get_all(name)

    def get_role_binding(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single role binding by name

        Args:
            name (str): Specify the name of the role binding to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The role binding dict
        """
        return self._get_one(name)

    def create_role_binding(self, role_binding) -> dict:
        """The method includes a functionality to create a new role binding

        Args:
            role_binding (RoleBinding | GlobalRoleBinding): Specify the role binding resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created role binding dict
        """
        return self._create(role_binding)

    def update_role_binding(self, name: str, role_binding) -> dict:
        """The method includes a functionality to update an existing role binding by name

        Args:
            name (str): Specify the name of the role binding to update
            role_binding (RoleBinding | GlobalRoleBinding): Specify the updated role binding resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated role binding dict
        """
        return self._update(name, role_binding)

    def delete_role_binding(self, name: str) -> None:
        """The method includes a functionality to delete a role binding by name

        Args:
            name (str): Specify the name of the role binding to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        self._delete(name)


class ProjectRoleBinding(RoleBindingBase):
    """The class includes all necessary methods to access the Perses project-scoped role bindings API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information
        project_name (str): Specify the name of the project to scope role binding operations to

    Attributes:
        api (Api): This is where we store the api
        project_name (str): This is where we store the project_name
    """

    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.ROLE_BINDINGS.value.format(project=self.project_name)


class GlobalRoleBinding(RoleBindingBase):
    """The class includes all necessary methods to access the Perses global role bindings API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_ROLE_BINDINGS.value
