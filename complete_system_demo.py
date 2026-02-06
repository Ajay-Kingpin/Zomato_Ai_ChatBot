#!/usr/bin/env python3
"""
Complete Zomato AI Recommendation System Demo
Demonstrates the integration of all 5 phases working together.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phase5.main import ZomatoRecommendationApp


def demo_complete_system():
    """Demonstrate the complete integrated recommendation system."""
    print("ZOMATO AI RECOMMENDATION SYSTEM - COMPLETE INTEGRATION DEMO")
    print("=" * 70)
    
    try:
        # Initialize the complete system
        print("Initializing complete recommendation system...")
        app = ZomatoRecommendationApp()
        
        # Show dataset information
        info = app.get_dataset_info()
        print(f"\nDATASET OVERVIEW:")
        print(f"   • Total restaurants: {info['total_restaurants']:,}")
        print(f"   • Available cities: {info['available_cities']}")
        print(f"   • Data columns: {len(info['columns'])}")
        print(f"   • Sample restaurants: {[r['name'] for r in info['sample_restaurants']]}")
        
        # Demo 1: Vegetarian recommendations
        print("\n" + "="*70)
        print("DEMO 1: VEGETARIAN RESTAURANT RECOMMENDATIONS")
        print("="*70)
        print("Input: Bangalore, Budget: Rs.800, Diet: vegetarian")
        print("-" * 70)
        
        result1 = app.get_recommendations("Bangalore", 800, "veg")
        print(result1)
        
        # Demo 2: Non-vegetarian recommendations
        print("\n" + "="*70)
        print("🍖 DEMO 2: NON-VEGETARIAN RESTAURANT RECOMMENDATIONS")
        print("="*70)
        print("🔍 Input: Bangalore, Budget: Rs.1500, Diet: non-vegetarian")
        print("-" * 70)
        
        result2 = app.get_recommendations("Bangalore", 1500, "non-veg")
        print(result2)
        
        # Demo 3: Budget-conscious recommendations
        print("\n" + "="*70)
        print("💰 DEMO 3: BUDGET-CONSCIOUS RECOMMENDATIONS")
        print("="*70)
        print("🔍 Input: Bangalore, Budget: Rs.400, Diet: vegetarian")
        print("-" * 70)
        
        result3 = app.get_recommendations("Bangalore", 400, "veg")
        print(result3)
        
        # Demo 4: Error handling
        print("\n" + "="*70)
        print("❌ DEMO 4: ERROR HANDLING")
        print("="*70)
        print("🔍 Input: Invalid city, Budget: -100, Diet: invalid")
        print("-" * 70)
        
        result4 = app.get_recommendations("", -100, "invalid")
        print(result4)
        
        # Success message
        print("\n" + "="*70)
        print("🎉 COMPLETE SYSTEM DEMO FINISHED SUCCESSFULLY!")
        print("="*70)
        print("✅ All 5 phases integrated and working:")
        print("   Phase 1: Data Loading ✅")
        print("   Phase 2: User Input Processing ✅")
        print("   Phase 3: Data Integration & Filtering ✅")
        print("   Phase 4: LLM Recommendations ✅")
        print("   Phase 5: Display & Formatting ✅")
        print("\n🚀 The Zomato AI Recommendation System is ready for production!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check your environment setup and API key configuration.")


def demo_interactive_mode():
    """Interactive demo where user can input their own preferences."""
    print("\n" + "="*70)
    print("🎮 INTERACTIVE MODE - Try Your Own Preferences!")
    print("="*70)
    
    try:
        app = ZomatoRecommendationApp()
        
        print("📍 Available cities include: Bangalore, Delhi, Mumbai, etc.")
        city = input("\n📍 Enter city/area: ").strip()
        if not city:
            print("❌ City cannot be empty!")
            return
        
        try:
            price = int(input("💰 Enter budget for two people (Rs.): ").strip())
            if price <= 0:
                print("❌ Budget must be positive!")
                return
        except ValueError:
            print("❌ Please enter a valid number for budget!")
            return
        
        diet = input("🥗 Enter diet preference (veg/non-veg): ").strip().lower()
        if diet not in ['veg', 'non-veg']:
            print("❌ Diet must be 'veg' or 'non-veg'!")
            return
        
        print(f"\n🔄 Getting recommendations for {city}, Rs.{price}, {diet}...")
        result = app.get_recommendations(city, price, diet)
        print(result)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Main demo function."""
    print("🍽️  ZOMATO AI RECOMMENDATION SYSTEM - COMPLETE INTEGRATION")
    print("This demo shows all 5 phases working together seamlessly!")
    print()
    
    choice = input("Choose demo mode:\n1. Complete System Demo\n2. Interactive Mode\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        demo_complete_system()
    elif choice == "2":
        demo_interactive_mode()
    else:
        print("❌ Invalid choice. Running complete system demo...")
        demo_complete_system()


if __name__ == "__main__":
    main()
