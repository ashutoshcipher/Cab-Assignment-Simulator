import time
from fastapi import FastAPI
from ..models import RideRequest, RideEstimate, Driver
from ..geo import HaversineProvider
from ..pricing import FareCalculator, PricingSettings
from ..allocation import SingleStrategy
from ..infra.settings import settings

app = FastAPI()

distance_provider = HaversineProvider()
fare_calc = FareCalculator(PricingSettings())
strategy = SingleStrategy(distance_provider, fare_calc, settings=settings)

# For demo purposes we keep in-memory drivers list
DRIVERS: list[Driver] = []

@app.post('/driver')
async def add_driver(driver: Driver):
    """Register a driver in the in-memory list used for demo purposes."""
    driver.last_ping = time.time()
    DRIVERS.append(driver)
    return {'status': 'ok'}

@app.post('/request')
async def request_ride(req: RideRequest) -> RideEstimate | None:
    """Allocate a driver for the incoming ride request."""
    if req.timestamp == 0.0:
        req.timestamp = time.time()
    estimate = strategy.allocate(req, DRIVERS)
    return estimate
