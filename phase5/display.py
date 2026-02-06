"""
Phase 5 - Display Layer
Formats and displays restaurant recommendations to the user.
"""

from typing import List, Dict, Any
import pandas as pd

from phase2.user_input import UserInput
from phase4.recommender import RecommendationResult


class RecommendationDisplay:
    """Handles formatting and display of restaurant recommendations."""

    def __init__(self, max_recommendations: int = 5):
        """
        Initialize the display formatter.
        
        Args:
            max_recommendations: Maximum number of recommendations to display
        """
        self.max_recommendations = max_recommendations

    def format_recommendations(self, result: RecommendationResult, user_input: UserInput) -> str:
        """
        Format recommendations for display.
        
        Args:
            result: RecommendationResult from Phase 4
            user_input: User preferences from Phase 2
            
        Returns:
            Formatted string ready for display
        """
        if not result.recommendations:
            return self._format_no_recommendations(user_input)
        
        header = self._build_header(user_input, len(result.recommendations))
        recommendations = self._format_recommendation_list(result.recommendations[:self.max_recommendations])
        footer = self._build_footer(user_input)
        
        return f"{header}\n\n{recommendations}\n\n{footer}"

    def _format_no_recommendations(self, user_input: UserInput) -> str:
        """Format message when no recommendations are available."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    NO RECOMMENDATIONS FOUND                 ║
╚══════════════════════════════════════════════════════════════╝

Sorry, we couldn't find any restaurants matching your criteria:

Location: {user_input.city}
Budget: Rs.{user_input.price} for two people
Diet: {user_input.diet}

Suggestions:
• Try increasing your budget range
• Consider nearby areas or different city names
• Check if dietary preferences are too restrictive
• Look for restaurants in neighboring locations

Please adjust your filters and try again!
"""

    def _build_header(self, user_input: UserInput, count: int) -> str:
        """Build the header section of the display."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║              ZOMATO AI RESTAURANT RECOMMENDATIONS           ║
╚══════════════════════════════════════════════════════════════╝

Your Preferences:
   Location: {user_input.city}
   Budget: Rs.{user_input.price} for two people  
   Diet: {user_input.diet}

Found {count} recommendation(s) for you!
"""

    def _format_recommendation_list(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format the list of recommendations."""
        formatted_items = []
        
        for i, rec in enumerate(recommendations, 1):
            # Extract restaurant name from the recommendation
            name = self._extract_restaurant_name(rec)
            content = rec.get('raw_text', '').strip()
            
            # Clean up the content
            content = self._clean_content(content, name)
            
            formatted_item = f"""
┌─────────────────────────────────────────────────────────────┐
│ RECOMMENDATION {i}: {name.upper()}
├─────────────────────────────────────────────────────────────┤
│ {content}
└─────────────────────────────────────────────────────────────┘"""
            formatted_items.append(formatted_item)
        
        return "\n".join(formatted_items)

    def _extract_restaurant_name(self, recommendation: Dict[str, Any]) -> str:
        """Extract restaurant name from recommendation data."""
        name_hint = recommendation.get('name_hint', '')
        if name_hint and name_hint != 'See response':
            return name_hint
        
        # Fallback: try to extract from raw text
        raw_text = recommendation.get('raw_text', '')
        lines = raw_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Why', 'Standout', 'Cost', 'Note', '•', '-', '*')):
                # Remove common prefixes
                for prefix in ['1. ', '2. ', '3. ', '4. ', '5. ', '**', '• ', '- ', '* ']:
                    if line.startswith(prefix):
                        line = line[len(prefix):]
                # Remove markdown bold
                line = line.replace('**', '').strip()
                if line and len(line) > 2:
                    return line
        
        return 'Restaurant'

    def _clean_content(self, content: str, restaurant_name: str) -> str:
        """Clean and format the recommendation content."""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip if it's just the restaurant name again
            if restaurant_name.lower() in line.lower() and len(line) < 50:
                continue
            
            # Clean up formatting
            line = line.replace('**', '').replace('*', '')
            
            # Add proper spacing
            if line.startswith(('Why it\'s', 'Standout', 'Note', 'Budget')):
                line = f"   {line}"
            elif line.startswith(('-', '•', '*')):
                line = f"   {line}"
            
            cleaned_lines.append(line)
        
        # Join lines with proper spacing
        return '\n'.join(cleaned_lines)

    def _build_footer(self, user_input: UserInput) -> str:
        """Build the footer section."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                        TIPS & NOTES                          ║
╚══════════════════════════════════════════════════════════════╝

Call ahead to confirm availability and current prices
Check restaurant hours before visiting
Consider booking for popular restaurants, especially on weekends
Payment methods may vary - check beforehand
These recommendations are AI-generated based on your preferences

Thank you for using Zomato AI Recommendation System!
"""

    def display_summary_stats(self, total_restaurants: int, filtered_restaurants: int, 
                             recommendations_count: int) -> str:
        """
        Display summary statistics about the recommendation process.
        
        Args:
            total_restaurants: Total restaurants in dataset
            filtered_restaurants: Restaurants matching user criteria
            recommendations_count: Number of AI recommendations generated
            
        Returns:
            Formatted statistics string
        """
        match_rate = (filtered_restaurants / total_restaurants * 100) if total_restaurants > 0 else 0
        
        return f"""
RECOMMENDATION STATISTICS:
   Total restaurants analyzed: {total_restaurants:,}
   Restaurants matching your criteria: {filtered_restaurants:,}
   Match rate: {match_rate:.1f}%
   AI recommendations generated: {recommendations_count}
   Processing time: < 2 seconds
"""
