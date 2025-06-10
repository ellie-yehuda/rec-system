from utils.data_sanitizer import sanitize_data
from database.connection import db_connection
import ast

# MongoDB setup
db = db_connection.get_db()

"""
Clustering utilities for restaurant recommendation system.

Provides logic to select top restaurants based on precomputed clustering combinations and user preferences.

Usage:
Call select_top_restaurants to retrieve top matches for a user.
"""

def select_top_restaurants(city, chosen_types, chosen_diets, chosen_features, rating_rank_dict):
    """
    Retrieve the top 10 restaurants matching a specific combination key.

    Args:
        city (str): City name.
        chosen_types (list): List of cuisine types selected by the user.
        chosen_diets (list): List of dietary preferences selected by the user.
        chosen_features (list): List of additional features selected by the user.
        rating_rank_dict (dict): Dictionary of rating priorities.

    Returns:
        list: List of top restaurant documents matching the combination.
    """
    # Ensure inputs are lists, not strings
    if isinstance(chosen_diets, str):
        chosen_diets = [chosen_diets] if chosen_diets.strip() else []
    if isinstance(chosen_features, str):
        chosen_features = [chosen_features] if chosen_features.strip() else []

    # Sort and format inputs correctly
    sorted_types = ', '.join(sorted(chosen_types))  # Sort and join types
    sorted_diets = ', '.join(sorted(chosen_diets)) if chosen_diets else "None"

    processed_features = []
    for feature in chosen_features:
        if feature == 'Wifi':
            processed_features.append('Free Wifi')
        else:
            processed_features.append(feature)
    sorted_features = ', '.join(sorted(processed_features)) if processed_features else "None"

    # Convert ranking dictionary to string, sorted by rank (value)
    ranking_str = ','.join([f"{key}:{value}" for key, value in sorted(rating_rank_dict.items(), key=lambda item: item[1])])

    # Construct the combination key
    combination_data = {
        "types": sorted_types,
        "diets": sorted_diets,
        "features": sorted_features,
        "ranking": ranking_str,
    }
    combination_key = str(combination_data)  # Use str() to match the database's Python dictionary string format
    print(f"DEBUG: Generated combination_key: {combination_key}")

    # Connect to the city-specific collection
    city_collection_name = f"{city.lower()}_combinations"
    city_collection = db[city_collection_name]
    print(f"DEBUG: Searching in collection: {city_collection_name}")

    query = {"combination": combination_key}
    document = city_collection.find_one(query)
    print(f"DEBUG: Document found: {document}")

    if document and "restaurant_links" in document:
    # Parse the stringified list into a Python list
        restaurant_links = ast.literal_eval(document["restaurant_links"])
        print(f"DEBUG: Parsed restaurant_links: {restaurant_links}")
    else:
        restaurant_links = []  # Default to an empty list if no document or field is found
        print("DEBUG: No document found or 'restaurant_links' not in document, setting empty list.")
    restaurant_list = []
    for link in restaurant_links:
        # Debugging: Print the link being searched for
        print(f"DEBUG: Searching for restaurant_link: {link}")
        # Add single quotes around the link to match the database's stored format
        query = {"restaurant_link": f"'{link}'"}
        print(f"DEBUG: Constructed restaurant query: {query}")
        restaurant = db[city.lower() + "_restaurants"].find_one(query)
        if restaurant:
            restaurant_list.append(sanitize_data(restaurant)) # Sanitize each restaurant
    # Return the matched restaurants
    return restaurant_list