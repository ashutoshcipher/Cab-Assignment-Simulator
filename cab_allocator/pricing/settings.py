from dataclasses import dataclass

@dataclass
class PricingSettings:
    """Configuration values for fare calculation."""

    base_fare: float = 50.0
    per_km_rate: float = 12.0
