from flask import Blueprint, jsonify, render_template, request
from bson import ObjectId, errors
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from random import choice
import math
import json
import ast # Import the ast module
from utils.data_sanitizer import sanitize_data
from database.connection import db_connection
from services.user_service import user_service

recommendations_bp = Blueprint('recommendations', __name__)

"""
This module provides recommendation logic and API endpoints for restaurant selection based on user preferences, ratings, and clustering.

Key Functions:
- init_recommendations: Initializes MongoDB collections for recommendations.
- filter_restaurants_by_preferences: Filters restaurants by user preferences.
- get_positive_restaurants: Returns top-rated restaurants by positive feedback.
- get_random_restaurants: Returns random restaurants for a city.
- sanitize_top_pairs: Sanitizes top pairs data for output.
- Flask routes for recommendations and ratings.

Usage:
Import and register the recommendations_bp blueprint in your Flask app.
"""

# MongoDB collections (will be initialized via init_recommendations)
user_preferences_collection = None
restaurants_collections = {}
users_collection = None
user_ratings_collection = None
db = None # Added db global variable

def init_recommendations(db_object):
    """
    Initialize MongoDB collections for recommendations.

    Args:
        db_object (Database): The database connection object.
    """
    global user_preferences_collection, restaurants_collections, users_collection, user_ratings_collection, db
    db = db_connection.get_db()
    user_preferences_collection = db['preferences']
    restaurants_collections = {
        'Rome': db['rome_restaurants'],
        'Paris': db['paris_restaurants'],
        'London': db['london_restaurants'],
    }
    users_collection = db['users']
    user_ratings_collection = db['user_ratings']
    db = db_object # Assign db_object to the global db variable

# Define binary and normalized float fields globally
binary_float_columns = [
    "food_rating_norm",
    "service_rating_norm",
    "value_rating_norm",
    "atmosphere_rating_norm",
    "is_price_$",
    "is_price_$$",
    "is_price_$$$",
    "is_price_$$$$",
    "is_british",
    "is_asian",
    "is_italian",
    "is_indian",
    "is_mediterranean",
    "is_fast_food",
    "is_seafood",
    "is_cafe",
    "is_french",
    "is_steakhouse",
    "is_mexican",
    "is_middle_eastern",
    "is_vegan_options",
    "is_gluten_free_options",
    "is_vegetarian_friendly",
    "is_free_wifi"
]

# Mapping dictionary for user preferences to restaurant fields
FIELD_MAPPING = {
    # Cuisine preferences
    "British": "is_british",
    "Mediterranean": "is_mediterranean",
    "French": "is_french",
    "Asian": "is_asian",
    "FastFood": "is_fast_food",
    "Cafe": "is_cafe",
    "Seafood": "is_seafood",
    "Italian": "is_italian",
    "Indian": "is_indian",
    "Steakhouse": "is_steakhouse",
    "Mexican": "is_mexican",
    "MiddleEastern": "is_middle_eastern",
    
    # Dietary preferences
    "Vegan": "is_vegan_options",
    "Vegetarian": "is_vegetarian_friendly",
    "GlutenFree": "is_gluten_free_options",

    # WiFi preference
    "Wifi": "is_free_wifi"
}

def filter_restaurants_by_preferences(user_id):
    """
    Filter restaurants based on user preferences.

    Args:
        user_id (str): The user ID from the database.

    Returns:
        list: A list of filtered restaurants matching user preferences.

    Raises:
        ValueError: If user preferences or city are not found.
    """
    # Fetch user preferences
    user_preferences = user_preferences_collection.find_one({"_id": ObjectId(user_id)})
    if not user_preferences:
        raise ValueError("User preferences not found.")

    city = user_preferences.get('city')
    if not city:
        raise ValueError("City is not specified in user preferences.")

    # Fetch restaurants in the same city
    city_restaurants = list(restaurants_collections.get(city).find())
    # Extract preferences
    cuisine_preferences = user_preferences.get('cuisine_preferences', [])
    dietary_preferences = user_preferences.get('dietary_preferences', [])
    wifi_preference = user_preferences.get('wifi',[])
    print("wifi_preference:", wifi_preference)
    # Collect corresponding fields for preferences
    cuisine_fields = {FIELD_MAPPING.get(cuisine) for cuisine in cuisine_preferences if FIELD_MAPPING.get(cuisine)}
    dietary_fields = {FIELD_MAPPING.get(diet) for diet in dietary_preferences if FIELD_MAPPING.get(diet)}
    wifi_field = FIELD_MAPPING.get(wifi_preference)
    # Filter restaurants
    filtered_restaurants = [
        restaurant for restaurant in city_restaurants
        if (
            # Match cuisine preferences
            any(restaurant.get(field, 0) == 1 for field in cuisine_fields) and
            # Match dietary preferences
            all(restaurant.get(field, 0) == 1 for field in dietary_fields) 
            # Match WiFi preference
            and (restaurant.get(wifi_field, 0) == 1 if wifi_field else True)

        )
    ]
    for restaurant in filtered_restaurants:
        restaurant["_id"] = str(restaurant["_id"])
    return sanitize_data(filtered_restaurants)

def get_positive_restaurants(limit, city):
    """
    Return a list of top-rated restaurants, sanitized for JSON output.

    Args:
        limit (int): Number of restaurants to return.
        city (str): City name.

    Returns:
        list: List of top-rated restaurant documents.
    """
    print(f"DEBUG: get_positive_restaurants called for city: {city}")
    # Get the collection for the city
    city_collection = restaurants_collections.get(city)
    if city_collection is None:
        print(f"DEBUG: No collection found for positive restaurants for city: {city}")
        return []

    # Query the collection to find restaurants with the highest number of positive expressions
    positive_restaurants = []
    try:
        # Fetch all restaurants in the city
        restaurants_cursor = city_collection.find()
        restaurant_scores = []

        for restaurant in restaurants_cursor:
            # Safely parse the `top_pairs_total` field
            feedback = []
            try:
                if 'top_pairs_total' in restaurant and isinstance(restaurant['top_pairs_total'], str):
                    # Use ast.literal_eval for safe parsing of Python literals
                    feedback_raw = ast.literal_eval(restaurant['top_pairs_total'])

                    # Ensure the list contains only valid items and convert count/sentiment to numbers
                    for item in feedback_raw:
                        if isinstance(item, (list, tuple)) and len(item) == 3:
                            try:
                                # Explicitly convert count to int and sentiment to float
                                phrase = item[0]
                                count = int(item[1]) if item[1] is not None else 0
                                sentiment = float(item[2]) if item[2] is not None else 0.0
                                feedback.append([phrase, count, sentiment])
                            except (ValueError, TypeError):
                                # If conversion fails, default to 0 for count and 0.0 for sentiment
                                feedback.append([item[0], 0, 0.0])
                        # else, skip or handle invalid feedback items as needed
            except (ValueError, SyntaxError) as e: # Catch errors from ast.literal_eval
                print(f"Error parsing feedback for restaurant {restaurant.get('_id')}: {e}")
                continue

            # Count the number of positive expressions
            positive_count = sum(
                1 for item in feedback if isinstance(item, list) and item[1] >= 2 and item[2] > 0.15
            )

            # Append the restaurant and its positive count
            restaurant_scores.append((restaurant, positive_count))

        # Sort restaurants by the number of positive expressions in descending order
        restaurant_scores.sort(key=lambda x: x[1], reverse=True)

        # Select the top `limit` restaurants
        positive_restaurants = [restaurant[0] for restaurant in restaurant_scores[:limit]]
        print(f"DEBUG: get_positive_restaurants returning {len(positive_restaurants)} restaurants.")
        return positive_restaurants

    except Exception as e:
        print(f"Error fetching positive restaurants for city {city}: {e}")

    return sanitize_data(positive_restaurants)

# return {limit} random restaurants
def get_random_restaurants(limit, city):
    """
    Return a list of random restaurants for a given city.

    Args:
        limit (int): Number of restaurants to return.
        city (str): City name.

    Returns:
        list: List of randomly selected restaurant documents.
    """
    print(f"DEBUG: get_random_restaurants called for city: {city}")
    city_collection = restaurants_collections.get(city)
    if city_collection is None:
        print(f"DEBUG: No collection found for random restaurants for city: {city}")
        return []

    # Fetch a sample of random restaurants from the collection
    restaurants_cursor = city_collection.aggregate([{'$sample': {'size': limit}}])
    random_restaurants = list(restaurants_cursor)
    print(f"DEBUG: get_random_restaurants returning {len(random_restaurants)} restaurants.")
    return random_restaurants

# sanitize the data for JSON compatibility    
def sanitize_top_pairs(restaurant):
    """Sanitize the `top_pairs_total` field to ensure it's valid JSON."""
    if 'top_pairs_total' in restaurant and isinstance(restaurant['top_pairs_total'], str):
        try:
            # Replace invalid Python-specific constructs with JSON-compatible ones
            sanitized_string = restaurant['top_pairs_total'] \
                .replace("None", "null") \
                .replace("none", "null") \
                .replace("'", '"') \
                .replace("(", "[") \
                .replace(")", "]")
            
            # Attempt to parse the sanitized string into a valid list
            sanitized_list_raw = eval(sanitized_string, {"null": None, "NaN": None, "none": None, "nan": None})

            # Ensure the list contains only valid items and convert count/sentiment to numbers
            sanitized_list = []
            for item in sanitized_list_raw:
                if isinstance(item, (list, tuple)) and len(item) == 3:
                    try:
                        phrase = item[0]
                        count = int(item[1]) if item[1] is not None else 0
                        sentiment = float(item[2]) if item[2] is not None else 0.0
                        sanitized_list.append([phrase, count, sentiment])
                    except (ValueError, TypeError):
                        sanitized_list.append([item[0], 0, 0.0]) # Fallback for invalid numbers
                else:
                    pass # Skip invalid entries

            restaurant['top_pairs_total'] = sanitized_list
        except (SyntaxError, ValueError, TypeError) as e:
            print(f"Error sanitizing top_pairs_total for restaurant {restaurant.get('_id')}: {e}")
            restaurant['top_pairs_total'] = []  # Fallback to an empty list
    return restaurant


@recommendations_bp.route('/api/test_recommendations/<user_id>', methods=['GET'])
def test_recommendations(user_id):
    """
    Generate the 4 test restaurants and render the test page.
    """
    try:
        # Fetch the user document
        user_document = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_document or "profile" not in user_document:
            return jsonify({'error': 'User profile not found'}), 404
        # Extract user profile
        user_profile = user_document["profile"]
        city = user_profile.get("city")
        city_collection = restaurants_collections.get(city)
        selected_ids = user_profile.get("selected_restaurants", [])
        if selected_ids:
            selected_restaurants = list(city_collection.find({"_id": {"$in": [ObjectId(id) for id in selected_ids]}}))
        else:
            selected_restaurants = []
        # Normalize the user profile vector
        user_vector = np.array([
            user_profile["averages"].get(col, 0) for col in binary_float_columns
        ]).reshape(1, -1)
        filtered_restaurants = filter_restaurants_by_preferences(user_id)
        filtered_restaurants = [
                r for r in filtered_restaurants 
            if ObjectId(r["_id"]) not in {selected["_id"] for selected in selected_restaurants}]  
        similarity_scores = []
        #  compute cosine similarity for all filtered restaurants
        for restaurant in filtered_restaurants:
            restaurant_vector = np.array([
                restaurant.get(col, 0) for col in binary_float_columns
            ]).reshape(1, -1)
            similarity = cosine_similarity(user_vector, restaurant_vector)[0][0]
            similarity_scores.append((restaurant, similarity))
        # sort by similarity and select top 2 restaurants
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_2_restaurants = [score[0] for score in similarity_scores[:2]]
        # save 4 closet restaurant in a new field in the user entry in the collection to show in home page
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"4_rec_restaurants": [score[0] for score in similarity_scores[:4]]}}
        )
        exculded_restaurants = top_2_restaurants + selected_restaurants
        print("Excluded restaurants:", len(exculded_restaurants))
        excluded_ids = {ObjectId(r["_id"]) for r in exculded_restaurants} 
        random_restaurant = None
        top_rated_restaurant = None
        if city_collection is not None:
            # Fetch all restaurants in the city excluding top_2_restaurants and previously selected restaurants of the user
            candidates = list(city_collection.find({"_id": {"$nin": list(excluded_ids)}}))
            
            # Select a random restaurant from the remaining candidates
            random_restaurant = choice(candidates) if candidates else None
            
            # Select the top-rated restaurant from the same candidate pool
            highly_rated_candidates = [r for r in candidates if r.get("general_rating") == 5]

            # Pick a random restaurant with a rating of 5
            top_rated_restaurant = choice(highly_rated_candidates) if highly_rated_candidates else None
    
        # Combine the 4 restaurants
        matching_restaurants = top_2_restaurants
        if random_restaurant and random_restaurant not in matching_restaurants:
            matching_restaurants.append(random_restaurant)
        if top_rated_restaurant and top_rated_restaurant not in matching_restaurants:
            matching_restaurants.append(top_rated_restaurant)

        # Assign categories to the restaurants
        categories = ["our_recommendation", "our_recommendation", "random", "high_rated"]
        # Sanitize data for JSON compatibility
        matching_restaurants = sanitize_data(matching_restaurants)
        for restaurant in matching_restaurants:
            restaurant['_id'] = str(restaurant['_id'])
            if isinstance(restaurant.get("image_urls"), str):
                try:
                    restaurant["image_urls"] = eval(restaurant["image_urls"], {"null": None, "nan": None})
                except Exception:
                    restaurant["image_urls"] = []  # Fallback to an empty list if parsing fails

        # Render the test page with the selected restaurants
        return render_template(
            'rating_page.html',
            restaurants=matching_restaurants,
            categories=categories,  # Pass categories to the front end
            user_id=user_id
        )
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print("Error generating test recommendations:", e)
        return jsonify({'error': 'An unexpected error occurred'}), 500

# store the user's ratings of the 4 restaurants
@recommendations_bp.route('/api/submit_ratings', methods=['POST'])
def submit_ratings():
    data = request.get_json()
    user_id = data.get('user_id')
    rankings = data.get('rankings')
    print("Rankings:", rankings)
    if not user_id or not rankings:
        return jsonify({'error': 'Missing user_id or rankings'}), 400

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Add ratings to a new sub-collection
    user_ratings_collection.insert_one({
        "user_id": user_id,
        "rated_restaurants": rankings
    })

    return jsonify({'status': 'success'}) 