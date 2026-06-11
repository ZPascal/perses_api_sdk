from __future__ import annotations

from ._base import ResourceBase
from .model import APIModel, APIEndpoints


class SecretBase(ResourceBase):
    """The class includes all necessary base methods to access the Perses secrets API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def get_secrets(self, name: str = None) -> list:
        """The method includes a functionality to retrieve all secrets

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of secret dicts
        """
        return self._get_all(name)

    def get_secret(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single secret by name

        Args:
            name (str): Specify the name of the secret to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The secret dict
        """
        return self._get_one(name)

    def create_secret(self, secret) -> dict:
        """The method includes a functionality to create a new secret

        Args:
            secret (Secret | GlobalSecret): Specify the secret resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created secret dict
        """
        return self._create(secret)

    def update_secret(self, name: str, secret) -> dict:
        """The method includes a functionality to update an existing secret by name

        Args:
            name (str): Specify the name of the secret to update
            secret (Secret | GlobalSecret): Specify the updated secret resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated secret dict
        """
        return self._update(name, secret)

    def delete_secret(self, name: str) -> None:
        """The method includes a functionality to delete a secret by name

        Args:
            name (str): Specify the name of the secret to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        self._delete(name)


class ProjectSecret(SecretBase):
    """The class includes all necessary methods to access the Perses project-scoped secrets API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information
        project_name (str): Specify the name of the project to scope secret operations to

    Attributes:
        api (Api): This is where we store the api
        project_name (str): This is where we store the project_name
    """

    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.SECRETS.value.format(project=self.project_name)


class GlobalSecret(SecretBase):
    """The class includes all necessary methods to access the Perses global secrets API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_SECRETS.value
