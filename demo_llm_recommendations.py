#!/usr/bin/env python3
"""
Demo script to test LLM recommendations with real API calls.
This script demonstrates the complete Phase 4 recommendation system working.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables with error handling
try:
    load_dotenv(project_root / "phase4" / ".env")
except Exception:
    # Fallback: set environment variable directly if .env loading fails
    os.environ["GROQ_API_KEY"] = "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"

import pandas as pd
from phase2.user_input import UserInput
from phase3.integrator import IntegrationContext, Integrator
from phase4.recommender import Recommender


def create_sample_data():
    """Create sample restaurant data for demonstration."""
    return pd.DataFrame({
        "name": ["Saffron Court", "Green Palace", "Spice Garden", "BBQ Nation", "Pasta Hub"],
        "rate": ["4.5/5", "4.2/5", "4.0/5", "4.7/5", "3.8/5"],
        "approx_cost(for two people)": ["800", "600", "500", "1200", "400"],
        "cuisines": ["North Indian, Chinese", "South Indian, Italian", "Continental, Mexican", "BBQ, North Indian", "Italian, Continental"],
        "dish_liked": ["Butter Chicken, Naan", "Dosa, Idli", "Pasta, Pizza", "Grilled Chicken, Kebabs", "Pasta, Pizza"],
        "rest_type": ["Casual Dining", "Fine Dining", "Cafe", "Casual Dining", "Cafe"],
        "location": ["Indiranagar", "Koramangala", "HSR Layout", "Whitefield", "MG Road"],
        "listed_in(city)": ["Bangalore", "Bangalore", "Bangalore", "Bangalore", "Bangalore"]
    })


def demo_vegetarian_recommendations():
    """Demo vegetarian recommendations within budget."""
    print("\n" + "="*60)
    print("DEMO: Vegetarian Restaurant Recommendations (Budget: Rs.700)")
    print("="*60)
    
    # Create sample data
    df = create_sample_data()
    
    # Create user input
    user_input = UserInput(city="Bangalore", price=700, diet="veg")
    
    # Filter data
    integrator = Integrator()
    context = integrator.prepare_context(df, user_input)
    
    print(f"Found {context.total_matches} restaurants matching criteria:")
    if not context.filtered_df.empty:
        for _, row in context.filtered_df.iterrows():
            print(f"  - {row['name']} (Rs.{row['approx_cost(for two people)']}, {row['cuisines']})")
    
    # Get recommendations
    recommender = Recommender()
    result = recommender.get_recommendations(context)
    
    print(f"\nAI Recommendations:")
    print("-" * 40)
    print(result.raw_response)


def demo_non_vegetarian_recommendations():
    """Demo non-vegetarian recommendations with higher budget."""
    print("\n" + "="*60)
    print("DEMO: Non-Vegetarian Restaurant Recommendations (Budget: Rs.1500)")
    print("="*60)
    
    # Create sample data
    df = create_sample_data()
    
    # Create user input
    user_input = UserInput(city="Bangalore", price=1500, diet="non-veg")
    
    # Filter data
    integrator = Integrator()
    context = integrator.prepare_context(df, user_input)
    
    print(f"Found {context.total_matches} restaurants matching criteria:")
    if not context.filtered_df.empty:
        for _, row in context.filtered_df.iterrows():
            print(f"  - {row['name']} (Rs.{row['approx_cost(for two people)']}, {row['cuisines']})")
    
    # Get recommendations
    recommender = Recommender()
    result = recommender.get_recommendations(context)
    
    print(f"\nAI Recommendations:")
    print("-" * 40)
    print(result.raw_response)


def demo_no_matches():
    """Demo when no restaurants match criteria."""
    print("\n" + "="*60)
    print("DEMO: No Matching Restaurants (Very Low Budget)")
    print("="*60)
    
    # Create sample data
    df = create_sample_data()
    
    # Create user input with very low budget
    user_input = UserInput(city="Bangalore", price=200, diet="veg")
    
    # Filter data
    integrator = Integrator()
    context = integrator.prepare_context(df, user_input)
    
    print(f"Found {context.total_matches} restaurants matching criteria")
    
    # Get recommendations
    recommender = Recommender()
    result = recommender.get_recommendations(context)
    
    print(f"\nAI Response:")
    print("-" * 40)
    print(result.raw_response)


def main():
    """Run all demonstrations."""
    print("Zomato AI Recommendation System - LLM Demo")
    print("=" * 60)
    
    # Check API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not found in environment variables!")
        print("Please set up the .env file with your Groq API key.")
        return
    
    print(f"Groq API key configured: {api_key[:10]}...")
    
    try:
        # Run demonstrations
        demo_vegetarian_recommendations()
        demo_non_vegetarian_recommendations()
        demo_no_matches()
        
        print("\n" + "="*60)
        print("All demos completed successfully!")
        print("The LLM recommendation system is working properly.")
        print("="*60)
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("Please check your API key and internet connection.")


if __name__ == "__main__":
    main()
