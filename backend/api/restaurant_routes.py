from flask import Blueprint, jsonify, render_template
from bson import ObjectId, errors
from services.restaurant_service import restaurant_service
from database.repositories.user_repository import user_repository
import ast

restaurant_bp = Blueprint('restaurant_bp', __name__)

"""
API routes for restaurant selection, home, and search endpoints.

Key Endpoints:
- /api/restaurant_selection/<user_id>: Render restaurant selection for a user.
- /api/home/<user_id>: Render home page for a user.
- /api/search: Search for restaurants by name and city.

Usage:
Register the restaurant_bp blueprint in your Flask app.
"""

@restaurant_bp.route('/api/restaurant_selection/<user_id>')
def restaurant_selection(user_id):
    """
    Render the restaurant selection page for a user based on their preferences.

    Args:
        user_id (str): The user ID from the database.

    Returns:
        Response: Rendered HTML template with top restaurant recommendations.
    """
    try:
        user_preferences = user_repository.get_user_preferences(user_id)
    except errors.InvalidId:
        return jsonify({'error': 'Invalid user ID format'}), 400

    if not user_preferences:
        return jsonify({'error': 'User preferences not found'}), 404

    city = user_preferences.get('city', '')
    if isinstance(city, list):
        city = city[0].strip()
    city = city.capitalize()
    
    top_restaurants = restaurant_service.get_top_restaurants(
        city,
        user_preferences.get('cuisine_preferences', []),
        user_preferences.get('dietary_preferences', []),
        user_preferences.get('wifi', []),
        user_preferences.get('dining_priority', {})
    )

    user_repository.add_offered_restaurants(user_id, user_preferences.get("nickname"), top_restaurants)

    for restaurant in top_restaurants:
        if '_id' in restaurant:
            restaurant['_id'] = str(restaurant['_id'])
        if 'image_urls' in restaurant and isinstance(restaurant['image_urls'], str):
            try:
                restaurant['image_urls'] = ast.literal_eval(restaurant['image_urls'])
            except (SyntaxError, ValueError, TypeError):
                restaurant['image_urls'] = [restaurant['image_urls']]
    return render_template('restaurant_selection.html', restaurants=top_restaurants, user_id=user_id, city=city)

@restaurant_bp.route('/api/home/<user_id>')
def home(user_id):
    """
    Render the home page for a user.

    Args:
        user_id (str): The user ID from the database.

    Returns:
        Response: Rendered HTML template with user data or error message.
    """
    # This route needs to be refactored to use services and repositories
    # For now, I'm moving it as is
    try:
        user_object_id = ObjectId(user_id)
    except errors.InvalidId:
        return "Invalid user ID", 400

    user_data = user_repository.users_collection.find_one({"_id": user_object_id})

    if not user_data:
        return "User not found", 404

    return render_template('home.html', user_data=user_data)

@restaurant_bp.route('/api/search', methods=['GET'])
def search_restaurants():
    """
    Search for restaurants by name and city.

    Returns:
        Response: JSON list of matching restaurants.
    """
    # This route needs to be refactored to use services and repositories
    # For now, I'm moving it as is
    query = request.args.get('q', '')
    city = request.args.get('city', 'Rome').capitalize()
    
    restaurants_collection = db.get_collection(f"{city.lower()}_restaurants")
    
    restaurants = list(restaurants_collection.find(
        {"restaurant_name": {"$regex": query, "$options": "i"}},
        limit=10
    ))
    
    for r in restaurants:
        r['_id'] = str(r['_id'])

    return jsonify(restaurants) 