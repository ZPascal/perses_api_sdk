from __future__ import annotations

import logging

from .api import Api

logger = logging.getLogger(__name__)
from .model import APIEndpoints, APIModel, RequestsMethods
from .model import User as UserModel


class User:
    """The class includes all necessary methods to access the Perses users API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_users(self, name: str | None = None) -> list:
        """The method includes a functionality to retrieve all users

        Args:
            name (str): Specify a name to filter the results (default None)

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of user dicts
        """
        path = APIEndpoints.USERS.value
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logger.error("Failed to retrieve users.")
            raise TypeError(result)
        return result

    def get_user(self, name: str) -> dict:
        """The method includes a functionality to retrieve a single user by name

        Args:
            name (str): Specify the name of the user to retrieve

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The user dict
        """
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(APIEndpoints.USER.value.format(name=name))
        if not isinstance(result, dict):
            logger.error(f"Failed to retrieve user: {name}")
            raise TypeError(result)
        return result

    def create_user(self, user: UserModel) -> dict:
        """The method includes a functionality to create a new user

        Args:
            user (User): Specify the user resource to create

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The created user dict
        """
        result = self.api.call_the_api(
            APIEndpoints.USERS.value,
            method=RequestsMethods.POST,
            json_complete=user.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logger.error("Failed to create user.")
            raise TypeError(result)
        return result

    def update_user(self, name: str, user: UserModel) -> dict:
        """The method includes a functionality to update an existing user by name

        Args:
            name (str): Specify the name of the user to update
            user (User): Specify the updated user resource

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The updated user dict
        """
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.USER.value.format(name=name),
            method=RequestsMethods.PUT,
            json_complete=user.model_dump_json(by_alias=True, exclude_none=True),
        )
        if not isinstance(result, dict):
            logger.error(f"Failed to update user: {name}")
            raise TypeError(result)
        return result

    def delete_user(self, name: str) -> None:
        """The method includes a functionality to delete a user by name

        Args:
            name (str): Specify the name of the user to delete

        Raises:
            ValueError: Missed specifying a necessary value
        """
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.USER.value.format(name=name),
            method=RequestsMethods.DELETE,
        )
