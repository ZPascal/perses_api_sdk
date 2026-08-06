from __future__ import annotations

from ._base import ResourceBase
from .model import APIEndpoints, APIModel


class DatasourceBase(ResourceBase):
    """The class includes all necessary base methods to access the Perses datasources API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def get_datasources(self, name: str | None = None) -> list:
        """The method includes a functionality to retrieve all datasources

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of datasource dicts
        """
        return self._get_all(name)

    def get_datasource(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single datasource by name

        Args:
            name (str): Specify the name of the datasource to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The datasource dict
        """
        return self._get_one(name)

    def create_datasource(self, datasource) -> dict:
        """The method includes a functionality to create a new datasource

        Args:
            datasource (Datasource | GlobalDatasource): Specify the datasource resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created datasource dict
        """
        return self._create(datasource)

    def update_datasource(self, name: str, datasource) -> dict:
        """The method includes a functionality to update an existing datasource by name

        Args:
            name (str): Specify the name of the datasource to update
            datasource (Datasource | GlobalDatasource): Specify the updated datasource resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated datasource dict
        """
        return self._update(name, datasource)

    def delete_datasource(self, name: str) -> None:
        """The method includes a functionality to delete a datasource by name

        Args:
            name (str): Specify the name of the datasource to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        self._delete(name)


class ProjectDatasource(DatasourceBase):
    """The class includes all necessary methods to access the Perses project-scoped datasources API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information
        project_name (str): Specify the name of the project to scope datasource operations to

    Attributes:
        api (Api): This is where we store the api
        project_name (str): This is where we store the project_name
    """

    def __init__(self, perses_api_model: APIModel, project_name: str):
        super().__init__(perses_api_model)
        self.project_name = project_name

    def _base_path(self) -> str:
        return APIEndpoints.DATASOURCES.value.format(project=self.project_name)


class GlobalDatasource(DatasourceBase):
    """The class includes all necessary methods to access the Perses global datasources API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def _base_path(self) -> str:
        return APIEndpoints.GLOBAL_DATASOURCES.value
