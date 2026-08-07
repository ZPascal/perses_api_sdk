from __future__ import annotations

import json
import logging

from .api import Api

logger = logging.getLogger(__name__)
from .model import APIEndpoints, APIModel, RequestsMethods

VALID_RESOURCE_TYPES = frozenset(
    {
        "dashboards",
        "datasources",
        "globaldatasources",
        "variables",
        "globalvariables",
    }
)


class Validate:
    """The class includes all necessary methods to access the Perses validation API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def validate(self, resource_type: str, body: dict) -> None:
        """The method includes a functionality to validate a resource body against the Perses schema

        Args:
            resource_type (str): Specify the resource type to validate against, one of dashboards, datasources, globaldatasources, variables, or globalvariables
            body (dict): Specify the resource body to validate

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call
        """
        if resource_type not in VALID_RESOURCE_TYPES:
            raise ValueError(
                f"resource_type must be one of {sorted(VALID_RESOURCE_TYPES)}, got '{resource_type}'"
            )
        if not body:
            raise ValueError("body must not be empty")
        result = self.api.call_the_api(
            APIEndpoints.VALIDATE.value.format(resource_type=resource_type),
            method=RequestsMethods.POST,
            json_complete=json.dumps(body),
        )
        if isinstance(result, dict) and result.get("code") and result["code"] >= 400:
            logger.error(f"Validation failed for {resource_type}.")
            raise TypeError(result)
