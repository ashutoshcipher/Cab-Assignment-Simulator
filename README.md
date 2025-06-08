# Cab Assignment Simulator

This project simulates cab allocation for a ride hailing service in India.

## Assumptions
- Distance computation uses the Haversine formula by default.
- Kafka-based location feeds, Redis-Geo storage and dynamic `max_eta_km` are
  planned future features. See [docs/HLD.md](docs/HLD.md) for more detail.

## Local Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```
Run the API:
```bash
uvicorn cab_allocator.api.main:app --reload
```

## Development
Use `make dev` to install dependencies.
Run tests with:
```bash
pytest --cov=cab_allocator
```

## Optimisation Objective
Minimise pickup ETA and ride cost while maximising driver revenue. We model fare as:
```
fare = base_fare + distance_km * per_km_rate
fare *= surge_multiplier
```
The allocation strategy selects the nearest eligible driver within `max_eta_km`.

## Extending Strategies
Implement the `AllocationStrategy` interface and register it in the API or service
layer. Distance providers can be swapped by implementing the `DistanceProvider`
protocol.

