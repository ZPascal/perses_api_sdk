from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods
from .model import User as UserModel


class User:
    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_users(self, name: str = None) -> list:
        path = APIEndpoints.USERS.value
        if name:
            path = f"{path}?name={name}"
        result = self.api.call_the_api(path)
        if not isinstance(result, list):
            logging.error("Failed to retrieve users.")
            raise Exception(result)
        return result

    def get_user(self, name: str) -> dict:
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(APIEndpoints.USER.value.format(name=name))
        if not isinstance(result, dict):
            logging.error(f"Failed to retrieve user: {name}")
            raise Exception(result)
        return result

    def create_user(self, user: UserModel) -> dict:
        result = self.api.call_the_api(
            APIEndpoints.USERS.value,
            method=RequestsMethods.POST,
            json_complete=user.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error("Failed to create user.")
            raise Exception(result)
        return result

    def update_user(self, name: str, user: UserModel) -> dict:
        if not name:
            raise ValueError("name must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.USER.value.format(name=name),
            method=RequestsMethods.PUT,
            json_complete=user.model_dump_json(),
        )
        if not isinstance(result, dict):
            logging.error(f"Failed to update user: {name}")
            raise Exception(result)
        return result

    def delete_user(self, name: str) -> None:
        if not name:
            raise ValueError("name must not be empty")
        self.api.call_the_api(
            APIEndpoints.USER.value.format(name=name),
            method=RequestsMethods.DELETE,
        )
