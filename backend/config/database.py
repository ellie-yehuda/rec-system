import os

"""
Database configuration for MongoDB connection.

Provides configuration values for MongoDB URI and database name.

Usage:
Import db_config to access database settings.
"""

class DatabaseConfig:
    """
    Configuration class for MongoDB connection settings.
    """
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DB_NAME', 'restaurant_db')

db_config = DatabaseConfig() 