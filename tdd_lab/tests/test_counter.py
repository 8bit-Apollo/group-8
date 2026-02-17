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
        assert result.get_json() == {"foo": 0}

    #===========================
    # Test: Retrieve an existing counter
    # Author: Richard Sserunjogi
    # Date: 2026-02-16
    # Description: Ensure that an existing counter can be retrieved and its value is correct.
    # ===========================
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
     

    def test_get_nonexistent_counter(self, client):
        """It should return 404 if counter does not exist"""

        result = client.get('/counters/ghost')

        assert result.status_code == status.HTTP_404_NOT_FOUND
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
    # ===========================
    # Test: Delete a counter
    # Author: Thomas Feng
    # Date: 2026-02-16
    # Description: Ensure that a counter can be deleted and will no longer exist after deletion.
    # ===========================
    def test_delete_counter(self, client):
        """It should delete a counter"""

        # create a counter to delete
        result = client.post('/counters/delete-test')
        assert result.status_code == status.HTTP_201_CREATED

        # delete the counter
        result = client.delete('/counters/delete-test')
        assert result.status_code == status.HTTP_204_NO_CONTENT

    # ===========================
    # Test: Prevent duplicate counter
    # Author: Nevryk Soliven
    # Date: 2026-02-16
    # Description: Ensure duplicate counters raise a conflict error.
    # ===========================
    def test_post_prevent_duplicate_counter(self, client):
        """Prevent duplicate counter"""
        result = client.post('/counters/foo_dupe_test')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/foo_dupe_test')
        assert result.status_code == status.HTTP_409_CONFLICT
        
    # ===========================
    # Test: List all counters
    # Author: Matthew Jackson
    # Date: 2026-02-16
    # Description: List and Check all the counter available.
    # ===========================
    def test_List_All_Counters(self, client):
        # create counters to get
        client.post('/counters/foo')
        client.post('/counters/bar')
        
        result = client.get('/counters') #test retrieving counters
        
        assert result.status_code == status.HTTP_200_OK
        data = result.get_json()
        #list and check counters
        assert 'foo' in data
        assert 'bar' in data
        assert len(data) == 3
