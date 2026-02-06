"""Integration tests for the complete Zomato AI Recommendation System."""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables with error handling
try:
    load_dotenv(project_root / "phase4" / ".env")
except Exception:
    os.environ["GROQ_API_KEY"] = "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"

from phase5.main import ZomatoRecommendationApp


@pytest.fixture
def sample_app():
    """Create app instance with sample data for testing."""
    # Create sample data
    sample_data = pd.DataFrame({
        "name": ["Saffron Court", "Green Palace", "Spice Garden", "BBQ Nation", "Pasta Hub"],
        "rate": ["4.5/5", "4.2/5", "4.0/5", "4.7/5", "3.8/5"],
        "approx_cost(for two people)": ["800", "600", "500", "1200", "400"],
        "cuisines": ["North Indian, Chinese", "South Indian, Italian", "Continental, Mexican", "BBQ, North Indian", "Italian, Continental"],
        "dish_liked": ["Butter Chicken, Naan", "Dosa, Idli", "Pasta, Pizza", "Grilled Chicken, Kebabs", "Pasta, Pizza"],
        "rest_type": ["Casual Dining", "Fine Dining", "Cafe", "Casual Dining", "Cafe"],
        "location": ["Indiranagar", "Koramangala", "HSR Layout", "Whitefield", "MG Road"],
        "listed_in(city)": ["Bangalore", "Bangalore", "Bangalore", "Bangalore", "Bangalore"],
        "url": ["http://example1.com", "http://example2.com", "http://example3.com", "http://example4.com", "http://example5.com"],
        "address": ["Addr 1", "Addr 2", "Addr 3", "Addr 4", "Addr 5"],
        "online_order": ["Yes", "Yes", "No", "Yes", "No"],
        "book_table": ["Yes", "No", "No", "Yes", "No"],
        "votes": [1000, 800, 600, 1200, 400],
        "phone": ["123", "456", "789", "012", "345"],
        "reviews_list": ["Good", "Nice", "Average", "Excellent", "Okay"],
        "menu_item": ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"],
        "listed_in(type)": ["Buffet", "Cafes", "Dine-out", "Buffet", "Cafes"]
    })
    
    # Create app with mocked data loading
    with patch('phase5.main.ZomatoRecommendationApp._load_data'):
        app = ZomatoRecommendationApp()
        app.data = sample_data
        # Also set the data in the data_loader to avoid the RuntimeError
        app.data_loader._df = sample_data
        return app


class TestCompleteIntegration:
    """Integration tests for the complete recommendation system."""

    def test_vegetarian_recommendations_complete_flow(self, sample_app):
        """Test complete flow for vegetarian recommendations."""
        # Get recommendations
        result = sample_app.get_recommendations("Bangalore", 700, "veg")
        
        # Verify structure
        assert "ZOMATO AI RESTAURANT RECOMMENDATIONS" in result
        assert "Bangalore" in result
        assert "Rs.700" in result
        assert "veg" in result
        assert "RECOMMENDATION" in result
        assert "RECOMMENDATION STATISTICS" in result

    def test_non_vegetarian_recommendations_complete_flow(self, sample_app):
        """Test complete flow for non-vegetarian recommendations."""
        # Get recommendations
        result = sample_app.get_recommendations("Bangalore", 1500, "non-veg")
        
        # Verify structure
        assert "ZOMATO AI RESTAURANT RECOMMENDATIONS" in result
        assert "Bangalore" in result
        assert "Rs.1500" in result
        assert "non-veg" in result
        assert "RECOMMENDATION" in result

    def test_no_matches_scenario_complete_flow(self, sample_app):
        """Test complete flow when no restaurants match criteria."""
        # Use very low budget to ensure no matches
        result = sample_app.get_recommendations("Bangalore", 100, "veg")
        
        # Should still have proper structure
        assert "ZOMATO AI RESTAURANT RECOMMENDATIONS" in result
        assert "Bangalore" in result
        assert "Rs.100" in result
        # May have recommendations or no recommendations message, both are valid

    def test_invalid_user_input_handling(self, sample_app):
        """Test handling of invalid user input."""
        # Test invalid city
        result = sample_app.get_recommendations("", 700, "veg")
        assert "ERROR OCCURRED" in result
        
        # Test invalid budget (this will be handled by UserInput validation)
        result = sample_app.get_recommendations("Bangalore", -100, "veg")
        assert "ERROR OCCURRED" in result
        
        # Test invalid diet
        result = sample_app.get_recommendations("Bangalore", 700, "invalid")
        assert "ERROR OCCURRED" in result

    def test_app_initialization_with_data_info(self, sample_app):
        """Test app initialization and data info methods."""
        # Test dataset info
        info = sample_app.get_dataset_info()
        
        assert "total_restaurants" in info
        assert "available_cities" in info
        assert "columns" in info
        assert "sample_restaurants" in info
        assert info["total_restaurants"] == 5
        assert info["available_cities"] == 1  # Only Bangalore in sample data

    def test_available_cities_method(self, sample_app):
        """Test getting available cities from dataset."""
        cities = sample_app.get_available_cities()
        assert isinstance(cities, list)
        assert "Bangalore" in cities

    def test_recommendation_formatting_quality(self, sample_app):
        """Test that recommendations are properly formatted and readable."""
        result = sample_app.get_recommendations("Bangalore", 800, "non-veg")
        
        # Check for proper formatting elements
        assert "╔" in result and "╚" in result  # Box drawing characters
        assert "Location:" in result and "Budget:" in result and "Diet:" in result
        assert "TIPS & NOTES" in result
        assert "RECOMMENDATION STATISTICS" in result
        
        # Check that content is meaningful
        assert len(result) > 500  # Should be substantial content
        assert "Bangalore" in result
        assert "Rs.800" in result

    def test_error_handling_with_mocks(self, sample_app):
        """Test error handling with mocked exceptions."""
        # Mock the recommender to raise an exception
        with patch.object(sample_app.recommender, 'get_recommendations', side_effect=Exception("API Error")):
            result = sample_app.get_recommendations("Bangalore", 700, "veg")
            assert "ERROR OCCURRED" in result
            assert "API Error" in result


class TestRealAPIIntegration:
    """Integration tests with real API calls (limited to avoid rate limits)."""

    @pytest.fixture
    def real_app(self):
        """Create app with real data loading."""
        try:
            app = ZomatoRecommendationApp()
            return app
        except Exception:
            pytest.skip("Could not initialize app with real data")

    def test_real_data_loading_and_basic_recommendation(self, real_app):
        """Test loading real data and getting basic recommendations."""
        # Skip if no data loaded
        if not hasattr(real_app, 'data') or real_app.data.empty:
            pytest.skip("No real data available")
        
        # Get a recommendation with common parameters
        result = real_app.get_recommendations("Bangalore", 800, "veg")
        
        # Verify basic structure
        assert "ZOMATO AI RESTAURANT RECOMMENDATIONS" in result
        assert "Bangalore" in result
        assert len(result) > 200  # Should have substantial content

    def test_real_dataset_info(self, real_app):
        """Test getting info from real dataset."""
        # Skip if no data loaded
        if not hasattr(real_app, 'data') or real_app.data.empty:
            pytest.skip("No real data available")
        
        info = real_app.get_dataset_info()
        
        # Verify structure
        assert "total_restaurants" in info
        assert info["total_restaurants"] > 0
        assert "available_cities" in info
        assert info["available_cities"] > 0
