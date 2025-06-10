from bson import ObjectId
from database.repositories.user_repository import user_repository
from database.repositories.restaurant_repository import restaurant_repository

"""
Service layer for user-related business logic.

Provides methods to create user profiles, save preferences, and retrieve preferences.

Usage:
Import and use the user_service singleton for user operations.
"""

class UserService:
    def __init__(self):
        self.user_repository = user_repository
        self.restaurant_repository = restaurant_repository

    def create_user_profile(self, user_id, selected_restaurants, city):
        """
        Create a user profile based on the selected restaurants.

        Args:
            user_id (ObjectId or str): The user's unique identifier.
            selected_restaurants (list): List of restaurant IDs selected by the user.
            city (str): The city for the profile.

        Returns:
            dict: The created user profile document.
        """
        user_id_str = str(user_id)

        restaurant_details = self.restaurant_repository.find_by_ids(selected_restaurants, city)

        normalized_rating_fields = [
            "food_rating_norm", "service_rating_norm",
            "value_rating_norm", "atmosphere_rating_norm",
        ]
        binary_fields = []
        if restaurant_details:
            binary_fields = [key for key in restaurant_details[0] if key.startswith("is_")]

        field_totals = {field: 0 for field in normalized_rating_fields + binary_fields}
        restaurant_count = len(restaurant_details)

        for restaurant in restaurant_details:
            for field in normalized_rating_fields:
                field_totals[field] += restaurant.get(field, 0)
            for field in binary_fields:
                field_totals[field] += int(restaurant.get(field, 0))

        averages = {}
        if restaurant_count > 0:
            averages = {
                field: round(field_totals[field] / restaurant_count, 3)
                for field in normalized_rating_fields + binary_fields
            }
        else:
            for field in normalized_rating_fields + binary_fields:
                averages[field] = 0.0

        profile = {
            "user_id": user_id_str,
            "city": city,
            "selected_restaurants": [str(r["_id"]) for r in restaurant_details],
            "averages": averages,
        }

        self.user_repository.update_user(user_id, {"profile": profile})
        return profile

    def save_user_preferences(self, data):
        """
        Save user preferences to the database.

        Args:
            data (dict): User preferences data.

        Returns:
            InsertOneResult: Result of the insert operation.
        """
        return self.user_repository.save_user_preferences(data)

    def get_user_preferences(self, user_id):
        """
        Retrieve user preferences from the database.

        Args:
            user_id (str): The user's unique identifier.

        Returns:
            dict or None: User preferences document or None if not found.
        """
        return self.user_repository.get_user_preferences(user_id)

user_service = UserService() 