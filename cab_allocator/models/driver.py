"""Data models for drivers."""

from dataclasses import dataclass
from typing import Tuple
from .enums import VehicleCategory, DriverState

@dataclass
class Driver:
    """A driver with current state and vehicle information."""
    id: str
    location: Tuple[float, float]
    category: VehicleCategory
    state: DriverState
    ev_range_km: float = 0.0
