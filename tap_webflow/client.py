"""REST client handling, including WebflowStream base class."""

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

import requests
from memoization import cached
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class WebflowStream(RESTStream):
    """Webflow stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    records_jsonpath = "$[*]"
    has_pagination = True
    _LOG_REQUEST_METRIC_URLS = True
    backoff_max_tries = 10

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        return BearerTokenAuthenticator.create_for_stream(
            self, token=self.config.get("api_key"))

    @property
    def page_size(self) -> int:
        if "page_size" in self.config:
            return self.config.get("page_size")

        return 100

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(self, response: requests.Response,
                            previous_token: Optional[Any]) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if not self.has_pagination:
            return None

        len_path = self.records_jsonpath.replace("[*]", "") + ".`len`"

        all_matches = extract_jsonpath(len_path, response.json())
        len = next(iter(all_matches), None)

        if len > 0:
            return (previous_token or 0) + self.page_size

        return None

    def get_url_params(self, context: Optional[dict],
                       next_page_token: Optional[Any]) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["offset"] = next_page_token
            params["limit"] = self.page_size
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params
