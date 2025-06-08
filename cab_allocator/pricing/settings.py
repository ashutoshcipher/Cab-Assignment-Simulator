"""Settings for pricing models."""

from dataclasses import dataclass

@dataclass
class PricingSettings:
    """Base fare and per-kilometre rate."""
    base_fare: float = 50.0
    per_km_rate: float = 12.0
