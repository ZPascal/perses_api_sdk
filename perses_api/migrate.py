from __future__ import annotations

import json
import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods


class Migrate:
    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def migrate(self, grafana_dashboard: dict, migration_input: dict = None) -> dict:
        if not grafana_dashboard:
            raise ValueError("grafana_dashboard must not be empty")
        body = {"grafanaDashboard": grafana_dashboard}
        if migration_input is not None:
            body["input"] = migration_input
        result = self.api.call_the_api(
            APIEndpoints.MIGRATE.value,
            method=RequestsMethods.POST,
            json_complete=json.dumps(body),
        )
        if not isinstance(result, dict):
            logging.error("Migration failed.")
            raise Exception(result)
        return result
