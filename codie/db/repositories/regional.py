"""Repositories for regional metrics."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class RegionalRepository(BaseRepository):
    def create_commander_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "commander_signature", "updated_at"))
        return self.insert("regional_commander_metrics", metric)

    def create_card_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "oracle_id", "updated_at"))
        return self.insert("regional_card_metrics", metric)

    def create_package_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "package_id", "updated_at"))
        return self.insert("regional_package_metrics", metric)
