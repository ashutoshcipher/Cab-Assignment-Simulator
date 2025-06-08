"""Driver allocation strategies."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

from ..models import Driver, RideRequest, RideEstimate, VehicleCategory
from ..geo import DistanceProvider
from ..pricing import FareCalculator

class AllocationStrategy(ABC):
    """Base class for all driver allocation strategies."""

    def __init__(self, dist_provider: DistanceProvider, fare_calc: FareCalculator, max_eta_km: float = 5.0) -> None:
        """Create a strategy.

        Parameters
        ----------
        dist_provider:
            Service used to compute distances.
        fare_calc:
            Calculator to compute ride fares.
        max_eta_km:
            Maximum driver pick-up distance in kilometres.
        """
        self.dist = dist_provider
        self.fare = fare_calc
        self.max_eta_km = max_eta_km

    @abstractmethod
    def allocate(self, request: RideRequest, drivers: List[Driver]) -> Optional[RideEstimate]:
        """Allocate a driver to the request if possible."""
        ...

class SingleStrategy(AllocationStrategy):
    """Select the nearest eligible driver for each request."""

    def allocate(self, request: RideRequest, drivers: List[Driver]) -> Optional[RideEstimate]:
        """Return the best ride estimate for the given request."""
        ride_distance = self.dist.distance_km(request.pickup, request.dropoff)
        candidates: list[tuple[float, Driver]] = []
        for d in drivers:
            if d.state.value != 'available':
                continue
            if d.category in [VehicleCategory.AUTO, VehicleCategory.BIKE] and d.category != request.category:
                continue
            if d.category == VehicleCategory.EV and d.ev_range_km < ride_distance:
                continue
            eta = self.dist.distance_km(d.location, request.pickup)
            if eta > self.max_eta_km:
                continue
            candidates.append((eta, d))
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[0])
        eta, chosen = candidates[0]
        fare = self.fare.calculate_fare(ride_distance, request.surge_multiplier)
        return RideEstimate(request=request, distance_km=ride_distance, eta_min=eta * 2, fare=fare)
