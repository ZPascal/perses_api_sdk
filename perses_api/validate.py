from __future__ import annotations

import json
import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods

VALID_RESOURCE_TYPES = frozenset({
    "dashboards",
    "datasources",
    "globaldatasources",
    "variables",
    "globalvariables",
})


class Validate:
    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def validate(self, resource_type: str, body: dict) -> None:
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
            logging.error(f"Validation failed for {resource_type}.")
            raise Exception(result)
