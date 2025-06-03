from pymongo import MongoClient
import json
import ast
from app import sanitize_data

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']  # Main database for restaurants

def select_top_restaurants(city, chosen_types, chosen_diets, chosen_features, rating_rank_dict):
    """
    Retrieve the top 10 restaurants matching a specific combination key (the clustering logic is calculated beforehand)
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

    # Convert ranking dictionary to string, sorted by key
    ranking_str = ','.join([f"{key}:{value}" for key, value in sorted(rating_rank_dict.items())])

    # Construct the combination key
    combination_key = repr({
        "types": sorted_types,
        "diets": sorted_diets,
        "features": sorted_features,
        "ranking": ranking_str,
    })
    print(f"DEBUG: Generated combination_key: {combination_key}")

    # Connect to the city-specific collection
    city_collection_name = f"{city.lower()}_combinations"
    city_collection = db[city_collection_name]

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
        query = {"restaurant_link": link}
        print(f"DEBUG: Constructed restaurant query: {query}")
        restaurant = db[city.lower() + "_restaurants"].find_one(query)
        if restaurant:
            restaurant_list.append(sanitize_data(restaurant)) # Sanitize each restaurant
    # Return the matched restaurants
    return restaurant_list