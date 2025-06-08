from enum import Enum

class VehicleCategory(str, Enum):
    MINI = 'mini'
    SEDAN = 'sedan'
    EV = 'ev'
    SUV = 'suv'
    AUTO = 'auto'
    BIKE = 'bike'

    def upgrade_path(self):
        hierarchy = [self.MINI, self.SEDAN, self.EV, self.SUV]
        if self in hierarchy:
            idx = hierarchy.index(self)
            if idx < len(hierarchy) - 1:
                return hierarchy[idx + 1]
        return None

class DriverState(str, Enum):
    AVAILABLE = 'available'
    BUSY = 'busy'
    OFFLINE = 'offline'
    TIMED_OUT = 'timed_out'
