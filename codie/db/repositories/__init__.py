"""Repository layer for all Codie persistence."""

from .analytics import AnalyticsRepository
from .canonical import CanonicalRepository
from .core import CoreRepository
from .curated import CuratedRepository
from .recommendations import RecommendationRepository
from .regional import RegionalRepository
from .simulation import SimulationRepository
from .source import SourceRepository
from .user import UserRepository

__all__ = [
    "AnalyticsRepository",
    "CanonicalRepository",
    "CoreRepository",
    "CuratedRepository",
    "RecommendationRepository",
    "RegionalRepository",
    "SimulationRepository",
    "SourceRepository",
    "UserRepository",
]
