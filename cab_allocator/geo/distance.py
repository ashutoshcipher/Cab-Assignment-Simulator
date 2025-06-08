import math
from typing import Tuple, Protocol

class DistanceProvider(Protocol):
    """Protocol for objects capable of computing distance in kilometres."""

    def distance_km(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """Return the distance in kilometres between two points."""
        ...

def haversine_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Compute the great circle distance using the haversine formula."""
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
    """Distance provider that uses the haversine formula."""

    def distance_km(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """Return the haversine distance between ``a`` and ``b``."""
        return haversine_distance(a, b)
