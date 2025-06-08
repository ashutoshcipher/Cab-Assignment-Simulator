from enum import Enum

class VehicleCategory(str, Enum):
    """Supported categories of vehicles."""
    MINI = 'mini'
    SEDAN = 'sedan'
    EV = 'ev'
    SUV = 'suv'
    AUTO = 'auto'
    BIKE = 'bike'

    def upgrade_path(self):
        """Return the next higher category, if any."""
        hierarchy = [self.MINI, self.SEDAN, self.EV, self.SUV]
        if self in hierarchy:
            idx = hierarchy.index(self)
            if idx < len(hierarchy) - 1:
                return hierarchy[idx + 1]
        return None

class DriverState(str, Enum):
    """Possible states a driver can be in."""
    AVAILABLE = 'available'
    BUSY = 'busy'
    OFFLINE = 'offline'
    TIMED_OUT = 'timed_out'
