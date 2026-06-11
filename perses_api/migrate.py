from __future__ import annotations

import json
import logging

from .api import Api
from .model import APIModel, APIEndpoints, RequestsMethods


class Migrate:
    """The class includes all necessary methods to access the Perses migration API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        api (Api): This is where we store the api
    """

    def __init__(self, perses_api_model: APIModel):
        self.api = Api(perses_api_model)

    def migrate(self, grafana_dashboard: dict, migration_input: dict = None) -> dict:
        """The method includes a functionality to migrate a Grafana dashboard to the Perses format

        Args:
            grafana_dashboard (dict): Specify the Grafana dashboard JSON to migrate
            migration_input (dict): Specify additional migration input variables (default None)

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            dict: The migrated Perses dashboard dict
        """
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
