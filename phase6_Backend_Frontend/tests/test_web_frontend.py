"""Test the Phase 6 web frontend."""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from phase6_Backend_Frontend.app import app, initialize_app


@pytest.fixture
def client():
    """Create test client for Flask app."""
    with app.test_client() as client:
        with app.app_context():
            # Initialize the recommendation system for testing
            success, _ = initialize_app()
            if not success:
                pytest.skip("Could not initialize recommendation system")
            yield client


class TestWebFrontend:
    """Test the web frontend functionality."""

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'message' in data

    def test_index_page(self, client):
        """Test the main index page loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Zomato AI Recommendation System' in response.data
        assert b'Find Your Perfect Restaurant' in response.data

    def test_cities_endpoint(self, client):
        """Test the cities API endpoint."""
        response = client.get('/api/cities')
        assert response.status_code == 200
        data = response.get_json()
        assert 'cities' in data
        assert isinstance(data['cities'], list)
        assert len(data['cities']) > 0

    def test_stats_endpoint(self, client):
        """Test the stats API endpoint."""
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_restaurants' in data
        assert 'available_cities' in data
        assert 'columns' in data
        assert data['total_restaurants'] > 0
        assert data['available_cities'] > 0

    def test_recommendations_endpoint_valid_input(self, client):
        """Test recommendations endpoint with valid input."""
        response = client.post('/api/recommendations', 
                           json={
                               'city': 'Bangalore',
                               'price': 800,
                               'diet': 'veg'
                           })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'recommendations' in data
        assert len(data['recommendations']) > 0

    def test_recommendations_endpoint_missing_city(self, client):
        """Test recommendations endpoint with missing city."""
        response = client.post('/api/recommendations', 
                           json={
                               'price': 800,
                               'diet': 'veg'
                           })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'City is required' in data['error']

    def test_recommendations_endpoint_invalid_price(self, client):
        """Test recommendations endpoint with invalid price."""
        response = client.post('/api/recommendations', 
                           json={
                               'city': 'Bangalore',
                               'price': -100,
                               'diet': 'veg'
                           })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Budget must be positive' in data['error']

    def test_recommendations_endpoint_invalid_diet(self, client):
        """Test recommendations endpoint with invalid diet."""
        response = client.post('/api/recommendations', 
                           json={
                               'city': 'Bangalore',
                               'price': 800,
                               'diet': 'invalid'
                           })
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Diet must be veg or non-veg' in data['error']

    def test_recommendations_endpoint_non_veg(self, client):
        """Test recommendations endpoint for non-vegetarian."""
        response = client.post('/api/recommendations', 
                           json={
                               'city': 'Bangalore',
                               'price': 1500,
                               'diet': 'non-veg'
                           })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'recommendations' in data

    def test_recommendations_endpoint_no_matches(self, client):
        """Test recommendations endpoint with criteria that won't match."""
        response = client.post('/api/recommendations', 
                           json={
                               'city': 'NonExistentCity',
                               'price': 100,
                               'diet': 'veg'
                           })
        # Should still return 200 but with no recommendations or helpful message
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'recommendations' in data
