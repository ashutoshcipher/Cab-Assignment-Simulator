from cab_allocator.models import Driver, RideRequest, VehicleCategory, DriverState
from cab_allocator.geo import HaversineProvider
from cab_allocator.pricing import FareCalculator, PricingSettings
from cab_allocator.allocation import SingleStrategy


def test_single_allocation():
    drivers = [
        Driver(id='d1', location=(0, 0), category=VehicleCategory.MINI, state=DriverState.AVAILABLE),
        Driver(id='d2', location=(0, 0.1), category=VehicleCategory.SEDAN, state=DriverState.AVAILABLE),
    ]
    request = RideRequest(id='r1', pickup=(0, 0), dropoff=(0, 0.2), category=VehicleCategory.MINI)
    strategy = SingleStrategy(HaversineProvider(), FareCalculator(PricingSettings()))
    estimate = strategy.allocate(request, drivers)
    assert estimate is not None
    assert estimate.request.id == 'r1'
