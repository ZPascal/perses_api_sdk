from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, RequestsMethods


class ResourceBase:
    """The class includes all necessary base methods to access dual-scoped Perses resources

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def _base_path(self) -> str:
        """The method returns the base API path for the resource type

        Raises:
            NotImplementedError: Subclasses must implement this method

        Returns:
            str: The base API path
        """
        raise NotImplementedError

    def _get_all(self, name: str = None) -> list:
        """The method includes a functionality to retrieve all resources, optionally filtered by name

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of resource dicts
        """
        path = self._base_path()
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logging.error(f"Failed to retrieve resources from {self._base_path()}.")
            raise Exception(result)
        return result

    def _get_one(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single resource by name

        Args:
            name (str): Specify the name of the resource to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The resource dict
        """
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(f"{self._base_path()}/{name}")
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve resource: {name}")
            raise Exception(result)
        return result

    def _create(self, body) -> dict:
        """The method includes a functionality to create a new resource

        Args:
            body (BaseModel): Specify the resource body as a Pydantic model instance

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created resource dict
        """
        result = self.api.call_the_api(
            self._base_path(),
            method=RequestsMethods.POST,
            json_complete=body.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to create resource at {self._base_path()}.")
            raise Exception(result)
        return result

    def _update(self, name: str, body) -> dict:
        """The method includes a functionality to update an existing resource by name

        Args:
            name (str): Specify the name of the resource to update
            body (BaseModel): Specify the updated resource body as a Pydantic model instance

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated resource dict
        """
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            f"{self._base_path()}/{name}",
            method=RequestsMethods.PUT,
            json_complete=body.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update resource: {name}")
            raise Exception(result)
        return result

    def _delete(self, name: str) -> None:
        """The method includes a functionality to delete a resource by name

        Args:
            name (str): Specify the name of the resource to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            f"{self._base_path()}/{name}", method=RequestsMethods.DELETE
        )
