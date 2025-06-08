from cab_allocator.pricing import FareCalculator, PricingSettings


def test_fare():
    calc = FareCalculator(PricingSettings(base_fare=50, per_km_rate=10))
    fare = calc.calculate_fare(10, surge=1.5)
    assert fare == 225.0
