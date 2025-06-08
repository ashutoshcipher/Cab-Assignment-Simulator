"""Geospatial distance calculations."""

import math
from typing import Tuple, Protocol

class DistanceProvider(Protocol):
    """Interface for distance calculation services."""

    def distance_km(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """Return distance in kilometres between two coordinates."""
        ...

def haversine_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Compute great-circle distance using the Haversine formula."""
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return 2 * r * math.asin(min(1, math.sqrt(h)))

class HaversineProvider:
    """Default distance provider based on the Haversine formula."""

    def distance_km(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """Return distance in kilometres between two points."""
        return haversine_distance(a, b)
