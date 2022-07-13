"""Stream type classes for tap-webflow."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_webflow.client import WebflowStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class SitesStream(WebflowStream):
    name = "sites"
    path = "/sites"
    primary_keys = ["_id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    schema_filepath = SCHEMAS_DIR / "sites.json"
    has_pagination = False

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"site_id": record["_id"]}

class DomainsStream(WebflowStream):
    name = "domains"
    path = "/sites/{site_id}/domains"
    primary_keys = ["_id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    schema_filepath = SCHEMAS_DIR / "domains.json"
    parent_stream_type = SitesStream
    ignore_parent_replication_keys = True
    has_pagination = False

class CollectionsStream(WebflowStream):
    name = "collections"
    path = "/sites/{site_id}/collections"
    primary_keys = ["_id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    schema_filepath = SCHEMAS_DIR / "collections.json"
    parent_stream_type = SitesStream
    ignore_parent_replication_keys = True
    has_pagination = False
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"collection_id": record["_id"]}

class ItemsStream(WebflowStream):
    name = "items"
    path = "/collections/{collection_id}/items"
    records_jsonpath = "$.items[*]"
    primary_keys = ["_id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    schema_filepath = SCHEMAS_DIR / "items.json"
    parent_stream_type = CollectionsStream
    ignore_parent_replication_keys = True
    has_pagination = True