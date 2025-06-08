from dataclasses import dataclass
from .settings import PricingSettings

@dataclass
class FareCalculator:
    settings: PricingSettings

    def calculate_fare(self, distance_km: float, surge: float) -> float:
        base = self.settings.base_fare + distance_km * self.settings.per_km_rate
        return base * surge
