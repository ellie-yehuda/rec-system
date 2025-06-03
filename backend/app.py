from flask import Flask, json, redirect, render_template, request, jsonify, url_for
from pymongo import MongoClient
from bson import ObjectId, errors
import utils.clustering  # Import the clustering logic
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from random import choice
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']
user_preferences_collection = db['preferences']
restaurants_collections = {
    'Rome': db['rome_restaurants'],
    'Paris': db['paris_restaurants'],
    'London': db['london_restaurants'],
}
users_collection = db['users']  # New collection for users
user_ratings_collection = db['user_ratings']  # New collection for user ratings

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

@app.route('/api/test_recommendations/<user_id>', methods=['GET'])
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

def filter_restaurants_by_preferences(user_id):
    """
    Filters restaurants based on user preferences.
    :param user_id: The user ID from the database
    :return: A list of filtered restaurants
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

def create_user_profile(user_id, selected_restaurants, city):
    """
    Creates a user profile based on the selected restaurants.
    """
    # Convert ObjectId to string for the user ID
    user_id_str = str(user_id)

    # Fetch restaurant details from the database
    restaurant_details = list(
        restaurants_collections.get(city).find(
            {"_id": {"$in": [ObjectId(rid) for rid in selected_restaurants]}}
        )
    )

    # Fields to average
    normalized_rating_fields = [
        "food_rating_norm",
        "service_rating_norm",
        "value_rating_norm",
        "atmosphere_rating_norm",
    ]
    binary_fields = []
    if restaurant_details:
        binary_fields = [key for key in restaurant_details[0] if key.startswith("is_")]

    # Initialize totals for averaging
    field_totals = {field: 0 for field in normalized_rating_fields + binary_fields}
    restaurant_count = len(restaurant_details)

    for restaurant in restaurant_details:
        for field in normalized_rating_fields:
            field_totals[field] += restaurant.get(field, 0)  # Default to 0 if missing
        for field in binary_fields:
            field_totals[field] += int(restaurant.get(field, 0))  # Convert binary

    # Calculate averages
    averages = {}
    if restaurant_count > 0:
        averages = {
            field: round(field_totals[field] / restaurant_count, 3)
            for field in normalized_rating_fields + binary_fields
        }
    else:
        # Initialize all average fields to 0.0 if no restaurants are selected
        for field in normalized_rating_fields + binary_fields:
            averages[field] = 0.0

    # Construct the profile
    profile = {
        "user_id": user_id_str,
        "city": city,
        "selected_restaurants": [str(r["_id"]) for r in restaurant_details],
        "averages": averages,
    }

    # Save the profile to the database
    users_collection = db["users"]
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"profile": profile}},
        upsert=True,
    )

    return profile


# store the user's ratings of the 4 restaurants
@app.route('/api/submit_ratings', methods=['POST'])
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


# store the user's selected restaurants in the user's sub-collection
@app.route('/api/submit_selection', methods=['POST'])
def submit_selection():
    data = request.get_json()
    # Get user ID and selected restaurants from the request
    selected_restaurants = data.get('selected_restaurants', [])
    user_id = data.get('user_id')  
    city = data.get('city')
    if not user_id or not selected_restaurants:
        return jsonify({'error': 'Missing user ID or selected restaurants'}), 400
    try:
        user_id = ObjectId(user_id)  # Ensure ObjectId type
    except Exception:
        return jsonify({'error': 'Invalid user ID format'}), 400
   # save the selected restaurants in the user's previosly "selected restaurants" sub-collection
    users_collection.update_one(
    {"_id": user_id},  # Filter: match the document by user ID
    {
        "$set": {
            "selected_restaurants": selected_restaurants,  # Update initial restaurants
            "city": city,  # Include city in the update
        }
    },
    upsert=True  # Create a new document if no match is found
    )

    try:
        profile = create_user_profile(user_id, selected_restaurants,city)
        # Sanitize the profile before sending it to the frontend
        sanitized_profile = sanitize_data(profile)
        return jsonify({"status": "success", "user_profile": sanitized_profile}), 200
    except Exception as e:
        print("Error saving selection or creating profile:", e)
        return jsonify({"error": "Failed to save selection"}), 500

def save_user_preferences(data):
    """Save user preferences to MongoDB."""
    return user_preferences_collection.insert_one(data)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/api/submit', methods=['POST'])
def submit_preferences():
    """Receive and save user preferences from the frontend."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    # Normalize fields using the helper function
    user_data = {
        'nickname': normalize_field(data.get('nickname'), str, ''),
        'city': normalize_field(data.get('city'), str, ''),
        'dietary_preferences': [data.get('dietary')] if data.get('dietary') and data.get('dietary') != 'None' else [],
        'cuisine_preferences': data.get('cuisines', []),
        'price_range': data.get('price', []),
        'dining_priority': {item: i + 1 for i, item in enumerate(data.get('priorities', []))},
        'restaurant_type': data.get('restaurantType', []),
        'wifi': ['Wifi'] if data.get('wifiRequired') is True else []
    }
    user_id = save_user_preferences(user_data).inserted_id
    return jsonify({'status': 'success', 'user_id': str(user_id)}), 200

@app.route('/api/restaurant_selection/<user_id>')
def restaurant_selection(user_id):
    """Generate restaurant recommendations using clustering logic."""
    try:
        user_preferences = user_preferences_collection.find_one({"_id": ObjectId(user_id)})
        print(user_preferences)
    except Exception as e:
        return jsonify({'error': 'Invalid user ID format'}), 400

    if not user_preferences:
        return jsonify({'error': 'User preferences not found'}), 404

    city = user_preferences.get('city', '')
    if isinstance(city, list):  # If city is a list, take the first element
        city = city[0].strip()
    city = city.capitalize()  # Normalize capitalization
    chosen_types = user_preferences.get('cuisine_preferences', [])
    chosen_diets = user_preferences.get('dietary_preferences', [])
    chosen_features = user_preferences.get('wifi', [])
    rating_rank_dict = user_preferences.get('dining_priority', {})
    restaurants_collection = restaurants_collections.get(city)
    print("restaurants_collection:", restaurants_collection)
    if restaurants_collection is None:
        return jsonify({'error': 'Invalid city'}), 400

    # Get top restaurants based on clustering
    top_restaurants_df = utils.clustering.select_top_restaurants(
        city,
        chosen_types,
        chosen_diets,
        chosen_features,
        rating_rank_dict
    )
    top_restaurants = sanitize_data(top_restaurants_df)
    # save the top 10 restaurants generated by the clustering in the user's sub-collection
    users_collection.insert_one({
        "_id": ObjectId(user_id),
        "nickname": user_preferences.get("nickname"),
        "offered_restaurants": top_restaurants,
        "selected_restaurants": [],  # Initialize sub-collection
    })
    for restaurant in top_restaurants:
        # Apply sanitize_data to the entire restaurant object
        restaurant = sanitize_data(restaurant)

        if '_id' in restaurant:
            restaurant['_id'] = str(restaurant['_id'])
        if 'image_urls' in restaurant and isinstance(restaurant['image_urls'], str):
            try:
                # Attempt to convert the string to a list
                restaurant['image_urls'] = eval(restaurant['image_urls'], {"null": None, "nan": None})
            except (SyntaxError, ValueError, TypeError):
                # If eval fails, keep it as a single-item list
                restaurant['image_urls'] = [restaurant['image_urls']]
    return render_template('restaurant_selection.html', restaurants=top_restaurants, user_id=user_id, city=city)

def normalize_field(field, expected_type=str, default_value=None):
    """
    Normalize a field to the expected type.
    If the field is a list, use the first element.
    """
    if isinstance(field, list) and len(field) > 0:
        field = field[0]
    if isinstance(field, expected_type):
        return field.strip() if isinstance(field, str) else field
    return default_value

# Sanitize data for JSON compatibility
def sanitize_data(data):
    """Recursively sanitize data for JSON serialization."""
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
@app.route('/api/restaurants/<user_id>')
def api_restaurants(user_id):
    """Return top_restaurants as JSON for the given user_id."""
    try:
        user_preferences = user_preferences_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return jsonify({'error': 'Invalid user ID format'}), 400

    if not user_preferences:
        return jsonify({'error': 'User preferences not found'}), 404

    city = user_preferences.get('city', '')
    if isinstance(city, list):
        city = city[0].strip()
    city = city.capitalize()

    restaurants_collection = restaurants_collections.get(city)
    if restaurants_collection is None:
        return jsonify({'error': 'Invalid city'}), 400

    try:
        # Get top restaurants based on clustering
        top_restaurants_df = utils.clustering.select_top_restaurants(
            city,
            user_preferences.get('cuisine_preferences', []),
            user_preferences.get('dietary_preferences', []),
            user_preferences.get('wifi', []),
            user_preferences.get('dining_priority', {})
        )
        top_restaurants = top_restaurants_df
        
        # Fallback if clustering returns no restaurants
        if not top_restaurants:
            print(f"DEBUG: Clustering returned no restaurants for user {user_id}. Falling back to positive restaurants.")
            fallback_restaurants = get_positive_restaurants(10, city) # Get 10 positive restaurants as fallback
            if not fallback_restaurants:
                print(f"DEBUG: Positive restaurants fallback also returned no restaurants for user {user_id}. Falling back to random restaurants.")
                fallback_restaurants = get_random_restaurants(10, city) # Get 10 random restaurants as final fallback
            top_restaurants = fallback_restaurants

    except Exception as e:
        print(f"Error during clustering or fallback: {e}")
        return jsonify({'error': 'Failed to generate recommendations. Please try again.'}), 500

    # Pre-process top_pairs_total (feedback) and ensure numerical types *before* generic sanitization
    for restaurant in top_restaurants:
        if 'top_pairs_total' in restaurant and isinstance(restaurant['top_pairs_total'], str):
            processed_feedback = []
            try:
                sanitized_string = restaurant['top_pairs_total'] \
                    .replace("None", "null") \
                    .replace("none", "null") \
                    .replace("'", '"') \
                    .replace("(", "[") \
                    .replace(")", "]")
                feedback_raw = eval(sanitized_string, {"null": None, "NaN": None, "none": None, "nan": None})

                for item in feedback_raw:
                    if isinstance(item, (list, tuple)) and len(item) == 3:
                        try:
                            phrase = item[0]
                            count = int(item[1]) if item[1] is not None else 0
                            sentiment = float(item[2]) if item[2] is not None else 0.0
                            processed_feedback.append([phrase, count, sentiment])
                        except (ValueError, TypeError):
                            processed_feedback.append([item[0], 0, 0.0])
            except Exception as e:
                print(f"Error sanitizing `top_pairs_total` for {restaurant.get('_id')}: {e}")
                processed_feedback = [] # Fallback to empty list on error

            restaurant['top_pairs_total'] = processed_feedback # Update the original field
        else:
            restaurant['top_pairs_total'] = [] # Ensure feedback field always exists as a list

    # Sanitize each restaurant for JSON
    sanitized = []
    for restaurant in top_restaurants: # Use the modified top_restaurants list
        # Apply sanitize_data to the entire restaurant object
        sanitized_restaurant = sanitize_data(restaurant)
        
        # Explicitly map _id to id and ensure it's a string, then remove _id
        if '_id' in sanitized_restaurant:
            sanitized_restaurant['id'] = str(sanitized_restaurant['_id'])
            del sanitized_restaurant['_id']
        
        # Manual handling for image_urls to ensure it's a list
        if 'image_urls' in sanitized_restaurant and isinstance(sanitized_restaurant['image_urls'], str):
            try:
                sanitized_restaurant['image_urls'] = eval(sanitized_restaurant['image_urls'], {"null": None, "nan": None})
            except:
                sanitized_restaurant['image_urls'] = []
        
        # Ensure image_urls is always a list, even if it was None after sanitization or parsing failures
        if not isinstance(sanitized_restaurant.get('image_urls'), list):
            sanitized_restaurant['image_urls'] = []

        # Rename 'top_pairs_total' to 'feedback' for frontend compatibility
        if 'top_pairs_total' in sanitized_restaurant:
            sanitized_restaurant['feedback'] = sanitized_restaurant['top_pairs_total']
            del sanitized_restaurant['top_pairs_total']

        sanitized.append(sanitized_restaurant)

    return jsonify(sanitized)

# Route to the home page
@app.route('/api/home/<user_id>')
def home(user_id):
    try:
        # Validate and convert user_id to ObjectId
        try:
            user_object_id = ObjectId(user_id)
        except errors.InvalidId:
            return jsonify({'error': 'Invalid user ID'}), 400

        # Fetch the user's city from the database
        user_doc = user_preferences_collection.find_one({"_id": user_object_id})
        if not user_doc:
            return jsonify({'error': 'User not found'}), 404

        city = user_doc.get('city')
        if not city:
            return jsonify({'error': 'City not found in user preferences'}), 404

        print("City:", city)

        # Fetch recommended restaurants
        reccomended_restaurants = get_positive_restaurants(4, city)

        # Fetch top-rated restaurants
        city_collection = restaurants_collections.get(city)
        if city_collection is None:
            return jsonify({'error': f'No restaurant collection found for city: {city}'}), 404

        top_restaurants_cursor = city_collection.find({'general_rating': {'$gt': 4.5}}).limit(4)
        top_restaurants = list(top_restaurants_cursor)
        personlized_restaurants = users_collection.find_one({"_id": user_object_id}).get("4_rec_restaurants", [])
        # Sanitize data for JSON compatibility
        reccomended_restaurants = sanitize_data(reccomended_restaurants)
        top_restaurants = sanitize_data(top_restaurants)
        personlized_restaurants = sanitize_data(personlized_restaurants)
        # Safely handle `image_urls`
        for restaurant in reccomended_restaurants + top_restaurants + personlized_restaurants:
            if 'image_urls' in restaurant and isinstance(restaurant['image_urls'], str):
                try:
                    # Attempt to convert the string to a list
                    restaurant['image_urls'] = eval(restaurant['image_urls'], {"null": None, "nan": None})
                except (SyntaxError, ValueError, TypeError):
                    # If eval fails, keep it as a single-item list
                    restaurant['image_urls'] = [restaurant['image_urls']]
            # Ensure image_urls is always a list
            if not isinstance(restaurant.get('image_urls'), list):
                restaurant['image_urls'] = []
        return render_template(
            'home.html',
            restaurants=reccomended_restaurants,
            high_rated=top_restaurants, user_city=city,
            personalized = personlized_restaurants
        )
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An unexpected error occurred'}), 500

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

# return top 4 restaurants with the highest number of positive expressions
def get_positive_restaurants(limit, city):
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
                    sanitized_string = restaurant['top_pairs_total'] \
                        .replace("None", "null") \
                        .replace("none", "null") \
                        .replace("'", '"') \
                        .replace("(", "[") \
                        .replace(")", "]")
                    
                    feedback_raw = eval(sanitized_string, {"null": None, "NaN": None, "none": None, "nan": None})

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
            except Exception as e:
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

# Route to the search page for future implementation
@app.route('/api/search', methods=['GET'])
def search_restaurants():
    query = request.args.get('query', '').lower()
    city = request.args.get('city', '')  # Assume city is passed as a query parameter
    
    # Validate query
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Get the city collection
    city_collection = restaurants_collections.get(city)
    if city_collection is None:
        return jsonify({'error': f'No data available for city: {city}'}), 404

    # Build the query for search
    restaurant_type_fields = [
        f'restaurant_types_{query}', f'special_diets_{query}', f'price_range_{query}'
    ]
    
    try:
        # Search for restaurants matching the query
        search_results = list(city_collection.find({
            '$or': [
                {'restaurant_name': {'$regex': query, '$options': 'i'}},
                {'cuisine_preference': {'$regex': query, '$options': 'i'}},
                *[{field: 1} for field in restaurant_type_fields]
            ]
        }).limit(10))
        
        # Prepare the results for the frontend
        for restaurant in search_results:
            # Handle `top_pairs_total` field for compatibility
            if 'top_pairs_total' in restaurant and isinstance(restaurant['top_pairs_total'], str):
                try:
                    sanitized_string = restaurant['top_pairs_total'] \
                        .replace("None", "null") \
                        .replace("none", "null") \
                        .replace("'", '"') \
                        .replace("(", "[") \
                        .replace(")", "]")
                    restaurant['top_pairs_total'] = eval(sanitized_string, {"null": None, "NaN": None, "none": None, "nan": None})
                except Exception as e:
                    print(f"Error sanitizing `top_pairs_total` for {restaurant['_id']}: {e}")
                    restaurant['top_pairs_total'] = []

            # Convert ObjectId to string for JSON serialization
            restaurant['_id'] = str(restaurant['_id'])
            # Apply comprehensive sanitization to the entire restaurant object
            restaurant = sanitize_data(restaurant)

        # Return results as JSON
        return jsonify({'searchResults': search_results})

    except Exception as e:
        print(f"Error fetching search results: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)