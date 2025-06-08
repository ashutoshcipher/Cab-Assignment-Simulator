from dataclasses import dataclass
from typing import Tuple
from .enums import VehicleCategory, DriverState

TIMEOUT_SEC = 15 * 60

@dataclass
class Driver:
    """Represents a driver available for ride allocation."""

    id: str
    location: Tuple[float, float]
    category: VehicleCategory
    state: DriverState
    ev_range_km: float = 0.0
    last_ping: float = 0.0

    def is_active(self, now: float) -> bool:
        """Return ``True`` if the driver can be allocated at ``now``."""
        if self.state == DriverState.OFFLINE:
            return False
        if now - self.last_ping > TIMEOUT_SEC:
            self.state = DriverState.TIMED_OUT
            return False
        return self.state == DriverState.AVAILABLE
