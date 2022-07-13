"""Webflow tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_webflow.streams import (
    WebflowStream,
    SitesStream,
    DomainsStream,
    CollectionsStream,
    ItemsStream
)

STREAM_TYPES = [
    SitesStream,
    DomainsStream,
    CollectionsStream,
    ItemsStream
]


class TapWebflow(Tap):
    """Webflow tap class."""
    name = "tap-webflow"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The key to authenticate against the API service"
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
