from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

from ..models import Driver, RideRequest, RideEstimate, VehicleCategory
from ..geo import DistanceProvider
from ..pricing import FareCalculator

class AllocationStrategy(ABC):
    """Base class for ride allocation strategies."""

    def __init__(self, dist_provider: DistanceProvider, fare_calc: FareCalculator, max_eta_km: float = 5.0):
        """Create a new strategy instance.

        Parameters
        ----------
        dist_provider:
            Component used to compute geographic distances.
        fare_calc:
            Fare calculator used for pricing rides.
        max_eta_km:
            Maximum driver ETA in kilometres before a driver is ignored.
        """
        self.dist = dist_provider
        self.fare = fare_calc
        self.max_eta_km = max_eta_km

    @abstractmethod
    def allocate(self, request: RideRequest, drivers: List[Driver]) -> Optional[RideEstimate]:
        """Return an estimate for the request or ``None`` when no driver fits."""
        ...

class SingleStrategy(AllocationStrategy):
    """Simple allocation strategy that chooses the closest suitable driver."""

    def allocate(self, request: RideRequest, drivers: List[Driver]) -> Optional[RideEstimate]:
        """Allocate a single driver that meets all requirements."""
        ride_distance = self.dist.distance_km(request.pickup, request.dropoff)
        candidates = []
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
        return RideEstimate(request=request, distance_km=ride_distance, eta_min=eta*2, fare=fare)
