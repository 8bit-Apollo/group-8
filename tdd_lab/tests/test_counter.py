"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status
from src.counter import COUNTERS

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED


    def test_get_existing_counter_returns_value(self, client):
        """
        Test retrieving an existing counter via GET /counters/<name>.

        Verifies that:
        - When a counter exists, the API returns HTTP 200
        - The response JSON includes the counter name and its current value
        """
        # Arrange: create a counter in memory
        COUNTERS["visits"] = 3

        # Act: retrieve it
        resp = client.get("/counters/visits")

        # Assert
        assert resp.status_code == status.HTTP_200_OK
        assert resp.get_json() == {"visits": 3}