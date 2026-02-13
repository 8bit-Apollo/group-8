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

    def test_unsupported_HTTP_methods(self, client):
        """Handle invalid HTTP methods"""

        # list of basic http methods
        all_http_methods = ['POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'HEAD']

        # list of supported http methods
        supported_http_methods = ['POST', 'GET', 'PUT', 'DELETE']

        # iterate through all methods and check http return status
        for method in all_http_methods:
            if method not in supported_http_methods:

                # create the request
                http_method = getattr(client, method.lower())
                result = http_method('/counters/foo')

                assert result.status_code == status.HTTP_405_METHOD_NOT_ALLOWED