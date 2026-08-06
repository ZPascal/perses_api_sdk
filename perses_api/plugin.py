from __future__ import annotations

import logging

from .api import Api

logger = logging.getLogger(__name__)
from .model import APIEndpoints, APIModel


class Plugin:
    """The class includes all necessary methods to access the Perses plugins API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def get_plugins(self) -> list:
        """The method includes a functionality to retrieve all available plugin modules

        Raises:
            Exception: Unspecified error by executing the API call

        Returns:
            list: A list of plugin module dicts
        """
        result = self.api.call_the_api(APIEndpoints.PLUGINS.value)
        if not isinstance(result, list):
            logger.error("Failed to retrieve plugins.")
            raise TypeError(result)
        return result
