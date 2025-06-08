"""Ride fare computation utilities."""

from dataclasses import dataclass
from .settings import PricingSettings

@dataclass
class FareCalculator:
    """Compute fares using configurable pricing settings."""

    settings: PricingSettings

    def calculate_fare(self, distance_km: float, surge: float) -> float:
        """Return the ride fare for the given distance and surge."""
        base = self.settings.base_fare + distance_km * self.settings.per_km_rate
        return base * surge
