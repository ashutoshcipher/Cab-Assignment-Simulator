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

### Current Single-Driver Strategy
The default `SingleStrategy` processes one request at a time:
1. Compute ride distance and filter out inactive drivers.
2. Reject Auto/Bike drivers if the category does not match the request.
3. Verify EVs have enough range for the trip.
4. Sort remaining drivers by ETA and pick the closest under `max_eta_km`.
5. Calculate fare based on distance and surge.
This keeps the algorithm simple and pricing predictable, but a rejected offer
means the passenger must retry, increasing wait time.

### Alternative Strategies
#### Batch allocation
| Pros | Cons |
| --- | --- |
| Lower rejection risk and faster acceptance | More network chatter and idle time for drivers who lose the batch |
| Can reduce passenger ETA | Requires extra logic to track pending offers |

Batching sends the request to several nearby drivers simultaneously. The first
to accept gets the ride. ETAs usually drop, pricing remains unchanged, and
drivers may earn less per hour if they frequently miss out while waiting.

#### Multicast for Auto/Bike
| Pros | Cons |
| --- | --- |
| Keeps short-trip ETAs small for low-cost categories | Drivers compete for the same ride, potentially lowering revenue |
| Encourages quick acceptance | Higher cancellation rates if multiple drivers respond |

Multicasting broadcasts to all autos or bikes within range. Pricing stays the
same, but heavy competition can push individual driver earnings down.

## Extending Strategies
Implement the `AllocationStrategy` interface and register it in the API or service
layer. Distance providers can be swapped by implementing the `DistanceProvider`
protocol.

