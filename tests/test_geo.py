from cab_allocator.geo import HaversineProvider


def test_haversine():
    provider = HaversineProvider()
    dist = provider.distance_km((0, 0), (0, 1))
    assert round(dist, 1) == 111.2
