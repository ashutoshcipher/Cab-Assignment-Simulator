from fastapi.testclient import TestClient
from cab_allocator.api.main import app, DRIVERS
from cab_allocator.models import Driver, VehicleCategory, DriverState


def test_e2e():
    client = TestClient(app)
    DRIVERS.clear()
    driver = Driver(id='d1', location=(0, 0), category=VehicleCategory.MINI, state=DriverState.AVAILABLE)
    client.post('/driver', json=driver.__dict__)
    resp = client.post('/request', json={
        'id': 'r1', 'pickup': [0, 0], 'dropoff': [0, 0.1], 'category': 'mini', 'surge_multiplier': 1.0
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data['request']['id'] == 'r1'
