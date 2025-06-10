from bson import ObjectId
from database.connection import db_connection

"""
Repository for user data access.

Provides methods to retrieve, save, and update user and preference documents.

Usage:
Import and use the user_repository singleton for database operations.
"""

class UserRepository:
    def __init__(self):
        self.db = db_connection.get_db()
        self.users_collection = self.db['users']
        self.user_preferences_collection = self.db['preferences']

    def get_user_preferences(self, user_id):
        """
        Retrieve user preferences by user ID.

        Args:
            user_id (str): The user's unique identifier.

        Returns:
            dict or None: User preferences document or None if not found.
        """
        return self.user_preferences_collection.find_one({"_id": ObjectId(user_id)})

    def save_user_preferences(self, data):
        """
        Save user preferences to the database.

        Args:
            data (dict): User preferences data.

        Returns:
            InsertOneResult: Result of the insert operation.
        """
        return self.user_preferences_collection.insert_one(data)

    def update_user(self, user_id, data):
        """
        Update a user document with new data.

        Args:
            user_id (str): The user's unique identifier.
            data (dict): Data to update in the user document.

        Returns:
            UpdateResult: Result of the update operation.
        """
        return self.users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data}, upsert=True)

    def add_offered_restaurants(self, user_id, nickname, restaurants):
        """
        Add offered restaurants to a user document.

        Args:
            user_id (str): The user's unique identifier.
            nickname (str): User's nickname.
            restaurants (list): List of offered restaurant documents.

        Returns:
            UpdateResult: Result of the update operation.
        """
        return self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "nickname": nickname,
                    "offered_restaurants": restaurants
                },
                "$setOnInsert": {
                    "selected_restaurants": []
                }
            },
            upsert=True
        )

    def add_selected_restaurants(self, user_id, restaurant_ids, city):
        """
        Add selected restaurants and city to a user document.

        Args:
            user_id (str): The user's unique identifier.
            restaurant_ids (list): List of selected restaurant IDs.
            city (str): City name.

        Returns:
            UpdateResult: Result of the update operation.
        """
        return self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "selected_restaurants": restaurant_ids,
                    "city": city,
                }
            },
            upsert=True
        )

user_repository = UserRepository() 