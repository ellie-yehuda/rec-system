import math
from bson import ObjectId

"""
Utility for sanitizing data for JSON serialization.

Provides a recursive function to clean data structures for safe JSON output.

Usage:
Call sanitize_data on any data before returning as JSON.
"""

def sanitize_data(data):
    """
    Recursively sanitize data for JSON serialization.

    Args:
        data (Any): The data to sanitize (dict, list, ObjectId, float, str, etc.).

    Returns:
        Any: Sanitized data suitable for JSON serialization.
    """
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(v) for v in data]
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, float) and math.isnan(data):
        return None  # Replace NaN with None (or any default value like 0 or "N/A")
    elif isinstance(data, str) and (data.lower() == "nan" or data.lower() == "none"):
        return None # Convert string "nan" or "none" to None
    else:
        return data 