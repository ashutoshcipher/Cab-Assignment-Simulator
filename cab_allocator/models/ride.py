from dataclasses import dataclass
from typing import Tuple
from .enums import VehicleCategory

@dataclass
class RideRequest:
    """Input data describing a requested ride."""
    id: str
    pickup: Tuple[float, float]
    dropoff: Tuple[float, float]
    category: VehicleCategory
    surge_multiplier: float = 1.0
    timestamp: float = 0.0

@dataclass
class RideEstimate:
    """Output produced after a ride has been allocated."""
    request: RideRequest
    distance_km: float
    eta_min: float
    fare: float
