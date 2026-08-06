from __future__ import annotations

import asyncio
import base64
import json
import logging
from typing import Any

import httpx

from .model import APIModel, RequestsMethods

logger = logging.getLogger(__name__)


class Api:
    """The class includes all necessary methods to access the Perses API

    Args:
        perses_api_model (APIModel): Inject a Perses API model object that includes all necessary values and information

    Attributes:
        perses_api_model (APIModel): This is where we store the perses_api_model
    """

    def __init__(self, perses_api_model: APIModel):
        self.perses_api_model = perses_api_model

    def call_the_api(
        self,
        api_call: str,
        method: RequestsMethods = RequestsMethods.GET,
        json_complete: str | None = None,
        response_status_code: bool = False,
    ) -> Any:
        """The method includes a functionality to execute a defined API call against the Perses endpoints

        Args:
            api_call (str): Specify the API call path relative to the host
            method (RequestsMethods): Specify the HTTP method to use (default GET)
            json_complete (str): Specify the JSON-serialised request body for POST and PUT requests (default None)
            response_status_code (bool): Specify if the HTTP status code should be injected into the response dict (default False)

        Raises:
            ValueError: Missed specifying a necessary value
            Exception: Unspecified error by executing the API call

        Returns:
            any: The API response as a parsed dict or list, or the raw httpx.Response for non-JSON responses
        """
        api_url = f"{self.perses_api_model.host}{api_call}"
        headers = dict(self.perses_api_model.headers or {})

        if self.perses_api_model.token:
            headers["Authorization"] = f"Bearer {self.perses_api_model.token}"
        elif self.perses_api_model.username and self.perses_api_model.password:
            credentials = base64.b64encode(
                f"{self.perses_api_model.username}:{self.perses_api_model.password}".encode()
            ).decode("utf-8")
            headers["Authorization"] = f"Basic {credentials}"

        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"

        http = self.create_the_http_api_client(headers)

        if self.perses_api_model.http2_support:

            async def _run():
                async with http:
                    return self._check_the_api_call_response(
                        await self._send_request(http, method, api_url, json_complete),
                        response_status_code,
                    )

            return asyncio.run(_run())

        response = self._send_request(http, method, api_url, json_complete)
        return self._check_the_api_call_response(response, response_status_code)

    def create_the_http_api_client(
        self, headers: dict | None = None
    ) -> httpx.Client | httpx.AsyncClient:
        """The method includes a functionality to create the HTTP client based on the API model configuration

        Args:
            headers (dict): Specify the HTTP headers to attach to every request (default None)

        Returns:
            Union[httpx.Client, httpx.AsyncClient]: A configured sync or async httpx client
        """
        limits = httpx.Limits(max_connections=self.perses_api_model.num_pools)

        if self.perses_api_model.http2_support:
            transport = httpx.AsyncHTTPTransport(
                retries=self.perses_api_model.retries,
                http2=True,
            )
            return httpx.AsyncClient(
                http2=True,
                limits=limits,
                timeout=self.perses_api_model.timeout,
                headers=headers,
                transport=transport,
                verify=self.perses_api_model.ssl_context or True,
                follow_redirects=self.perses_api_model.follow_redirects,
            )

        transport = httpx.HTTPTransport(
            verify=self.perses_api_model.ssl_context or True,
            retries=self.perses_api_model.retries,
        )
        return httpx.Client(
            limits=limits,
            timeout=self.perses_api_model.timeout,
            headers=headers,
            transport=transport,
            verify=self.perses_api_model.ssl_context or True,
            follow_redirects=self.perses_api_model.follow_redirects,
        )

    def _send_request(
        self,
        http: httpx.Client | httpx.AsyncClient,
        method: RequestsMethods,
        api_url: str,
        json_complete: str,
    ) -> Any:
        """The method includes a functionality to dispatch a single HTTP request using the provided client

        Args:
            http (Union[httpx.Client, httpx.AsyncClient]): Specify the httpx client to use for the request
            method (RequestsMethods): Specify the HTTP method
            api_url (str): Specify the fully-qualified request URL
            json_complete (str): Specify the JSON-serialised request body for POST and PUT (default None)

        Raises:
            ValueError: Missed specifying a necessary value for POST or PUT requests

        Returns:
            any: The raw httpx response object
        """
        if method in (RequestsMethods.GET, RequestsMethods.DELETE):
            return http.request(method.value, api_url)
        if json_complete is None:
            logger.error("Please define the json_complete.")
            raise ValueError(f"json_complete is required for {method.value}")
        return http.request(method.value, api_url, content=json_complete)

    @staticmethod
    def _check_the_api_call_response(
        response: Any, response_status_code: bool = False
    ) -> Any:
        """The method includes a functionality to parse the API response and optionally inject the HTTP status code

        Args:
            response (any): Specify the raw httpx response object
            response_status_code (bool): Specify if the HTTP status code should be injected into the response (default False)

        Returns:
            any: The parsed JSON response as dict or list, or the raw response for non-JSON bodies
        """
        if Api._check_if_valid_json(response.text):
            json_response = json.loads(response.text)
            if response_status_code:
                if isinstance(json_response, dict):
                    json_response["status"] = response.status_code
                elif isinstance(json_response, list) and json_response:
                    json_response[0]["status"] = response.status_code
            return json_response
        else:
            if response_status_code:
                return {"status": response.status_code, "data": response.text}
            return response

    @staticmethod
    def _check_if_valid_json(response: str) -> bool:
        """The method includes a functionality to check if the given string is valid JSON

        Args:
            response (str): Specify the string to validate

        Returns:
            bool: True if the string is valid JSON, False otherwise
        """
        if not response or response.strip() in ("", "null"):
            return False
        try:
            json.loads(response)
            return True
        except (TypeError, ValueError):
            return False
