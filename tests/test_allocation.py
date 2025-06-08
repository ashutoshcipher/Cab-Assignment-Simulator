from cab_allocator.models import Driver, RideRequest, VehicleCategory, DriverState
from cab_allocator.geo import HaversineProvider
from cab_allocator.pricing import FareCalculator, PricingSettings
from cab_allocator.allocation import SingleStrategy
from cab_allocator.infra.settings import Settings
import time


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


def test_driver_timeout():
    drivers = [
        Driver(
            id='d1',
            location=(0, 0),
            category=VehicleCategory.MINI,
            state=DriverState.AVAILABLE,
            last_ping=0.0,
        )
    ]
    request = RideRequest(
        id='r2',
        pickup=(0, 0),
        dropoff=(0, 0.1),
        category=VehicleCategory.MINI,
        timestamp=16 * 60,
    )
    strategy = SingleStrategy(HaversineProvider(), FareCalculator(PricingSettings()))
    estimate = strategy.allocate(request, drivers)
    assert estimate is None
    assert drivers[0].state == DriverState.TIMED_OUT


def test_dynamic_eta_radius():
    drivers = [
        Driver(id='d1', location=(0, 0.06), category=VehicleCategory.MINI, state=DriverState.AVAILABLE, last_ping=time.time()),
    ]
    settings = Settings(max_eta_day_km=5.0, max_eta_night_km=8.0)
    strategy = SingleStrategy(HaversineProvider(), FareCalculator(PricingSettings()), settings=settings)
    day_request = RideRequest(id='rd', pickup=(0, 0), dropoff=(0, 0.1), category=VehicleCategory.MINI, timestamp=time.mktime(time.strptime('12:00', '%H:%M')))
    night_request = RideRequest(id='rn', pickup=(0, 0), dropoff=(0, 0.1), category=VehicleCategory.MINI, timestamp=time.mktime(time.strptime('23:00', '%H:%M')))
    assert strategy.allocate(day_request, drivers) is None
    assert strategy.allocate(night_request, drivers) is not None


def test_upgrade_path():
    strategy = SingleStrategy(HaversineProvider(), FareCalculator(PricingSettings()))

    sedan_driver = Driver(id='sd', location=(0, 0), category=VehicleCategory.SEDAN, state=DriverState.AVAILABLE)
    mini_request = RideRequest(id='rm', pickup=(0, 0), dropoff=(0, 0.1), category=VehicleCategory.MINI)
    assert strategy.allocate(mini_request, [sedan_driver]) is not None

    mini_driver = Driver(id='md', location=(0, 0), category=VehicleCategory.MINI, state=DriverState.AVAILABLE)
    sedan_request = RideRequest(id='rs', pickup=(0, 0), dropoff=(0, 0.1), category=VehicleCategory.SEDAN)
    assert strategy.allocate(sedan_request, [mini_driver]) is None
