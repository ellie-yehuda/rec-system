from utils.clustering import select_top_restaurants
from utils.data_sanitizer import sanitize_data

"""
Service layer for restaurant-related business logic.

Provides methods to retrieve top restaurants based on clustering and user preferences.

Usage:
Import and use the restaurant_service singleton for restaurant operations.
"""

class RestaurantService:
    def get_top_restaurants(self, city, chosen_types, chosen_diets, chosen_features, rating_rank_dict):
        """
        Retrieve the top restaurants for a city based on user-selected types, diets, features, and ranking priorities.

        Args:
            city (str): The city name.
            chosen_types (list): List of cuisine types selected by the user.
            chosen_diets (list): List of dietary preferences selected by the user.
            chosen_features (list): List of additional features selected by the user.
            rating_rank_dict (dict): Dictionary of rating priorities.

        Returns:
            list: Sanitized list of top restaurant documents.
        """
        top_restaurants_df = select_top_restaurants(
            city,
            chosen_types,
            chosen_diets,
            chosen_features,
            rating_rank_dict
        )
        return sanitize_data(top_restaurants_df)

restaurant_service = RestaurantService() 