from bson import ObjectId
from database.connection import db_connection

"""
Repository for restaurant data access.

Provides methods to retrieve restaurant documents by IDs and city.

Usage:
Import and use the restaurant_repository singleton for database operations.
"""

class RestaurantRepository:
    def __init__(self):
        self.db = db_connection.get_db()
        self.restaurants_collections = {
            'Rome': self.db['rome_restaurants'],
            'Paris': self.db['paris_restaurants'],
            'London': self.db['london_restaurants'],
        }

    def find_by_ids(self, restaurant_ids, city):
        """
        Find restaurants by a list of IDs for a specific city.

        Args:
            restaurant_ids (list): List of restaurant ID strings.
            city (str): City name.

        Returns:
            list: List of restaurant documents.
        """
        return list(
            self.restaurants_collections.get(city).find(
                {"_id": {"$in": [ObjectId(rid) for rid in restaurant_ids]}}
            )
        )

restaurant_repository = RestaurantRepository() 