from fastapi import FastAPI
from ..models import RideRequest, RideEstimate, Driver
from ..geo import HaversineProvider
from ..pricing import FareCalculator, PricingSettings
from ..allocation import SingleStrategy

app = FastAPI()

distance_provider = HaversineProvider()
fare_calc = FareCalculator(PricingSettings())
strategy = SingleStrategy(distance_provider, fare_calc)

# For demo purposes we keep in-memory drivers list
DRIVERS: list[Driver] = []

@app.post('/driver')
async def add_driver(driver: Driver):
    DRIVERS.append(driver)
    return {'status': 'ok'}

@app.post('/request')
async def request_ride(req: RideRequest) -> RideEstimate | None:
    estimate = strategy.allocate(req, DRIVERS)
    return estimate
