from pymongo import MongoClient
from config.database import db_config

"""
Database connection singleton for MongoDB.

Provides a single shared MongoClient and database instance for the application.

Usage:
Import and use db_connection.get_db() to access the database.
"""

class DBConnection:
    _instance = None

    def __new__(cls):
        """
        Create or return the singleton instance of DBConnection.

        Returns:
            DBConnection: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.client = MongoClient(db_config.MONGODB_URI)
            cls._instance.db = cls._instance.client[db_config.DATABASE_NAME]
        return cls._instance

    def get_db(self):
        """
        Get the MongoDB database instance.

        Returns:
            Database: The MongoDB database object.
        """
        return self.db

db_connection = DBConnection() 