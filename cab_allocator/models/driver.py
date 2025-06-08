from dataclasses import dataclass
from typing import Tuple
from .enums import VehicleCategory, DriverState

@dataclass
class Driver:
    """Represents a driver available for ride allocation."""
    id: str
    location: Tuple[float, float]
    category: VehicleCategory
    state: DriverState
    ev_range_km: float = 0.0
