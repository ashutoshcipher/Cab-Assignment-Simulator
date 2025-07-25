from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

from ..infra.settings import Settings

from ..models import Driver, RideRequest, RideEstimate, VehicleCategory
from ..geo import DistanceProvider
from ..pricing import FareCalculator


def _category_satisfies(driver_cat: VehicleCategory, request_cat: VehicleCategory) -> bool:
    """Return ``True`` if ``driver_cat`` can serve ``request_cat`` or a higher category."""

    cat = request_cat
    while cat is not None:
        if cat == driver_cat:
            return True
        cat = cat.upgrade_path()
    return False

# Average minutes required to travel one kilometre (~30 km/h).
ETA_PER_KM_MIN = 2.0

class AllocationStrategy(ABC):
    """Base class for ride allocation strategies."""

    def __init__(
        self,
        dist_provider: DistanceProvider,
        fare_calc: FareCalculator,
        settings: Settings | None = None,
        max_eta_km: float = 5.0,
    ):
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
        self.settings = settings
        self.max_eta_km = max_eta_km

    def _get_max_eta_km(self, timestamp: float) -> float:
        if self.settings is not None:
            return self.settings.max_eta_km_for(timestamp)
        return self.max_eta_km

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
            if not d.is_active(request.timestamp):
                continue
            if d.category in [VehicleCategory.AUTO, VehicleCategory.BIKE] and d.category != request.category:
                continue
            if not _category_satisfies(d.category, request.category):
                continue
            if d.category == VehicleCategory.EV and d.ev_range_km < ride_distance:
                continue
            eta = self.dist.distance_km(d.location, request.pickup)
            if eta > self._get_max_eta_km(request.timestamp):
                continue
            candidates.append((eta, d))
        if not candidates:
            return None
        eta, chosen = min(candidates, key=lambda x: x[0])
        fare = self.fare.calculate_fare(ride_distance, request.surge_multiplier)
        eta_min = eta * ETA_PER_KM_MIN
        return RideEstimate(request=request, distance_km=ride_distance, eta_min=eta_min, fare=fare)
