from __future__ import annotations

import logging

from .api import Api
from .model import APIModel, APIEndpoints


class Plugin:
    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_plugins(self) -> list:
        result = self.api.call_the_api(APIEndpoints.PLUGINS.value)
        if not isinstance(result, list):
            logging.error("Failed to retrieve plugins.")
            raise Exception(result)
        return result
