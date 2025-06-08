from dataclasses import dataclass
from .settings import PricingSettings

@dataclass
class FareCalculator:
    """Calculate ride fares using configured pricing settings."""

    settings: PricingSettings

    def calculate_fare(self, distance_km: float, surge: float) -> float:
        """Return the fare for a ride of ``distance_km`` kilometres."""
        base = self.settings.base_fare + distance_km * self.settings.per_km_rate
        return base * surge
