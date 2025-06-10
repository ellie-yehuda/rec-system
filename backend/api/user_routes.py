from flask import Blueprint, request, jsonify, render_template
from bson import ObjectId, errors
from services.user_service import user_service
from services.restaurant_service import restaurant_service
from database.repositories.user_repository import user_repository
from utils.data_sanitizer import sanitize_data
import ast

user_bp = Blueprint('user_bp', __name__)

"""
API routes for user preferences and selection submission.

Key Endpoints:
- /api/submit_selection: Submit selected restaurants for a user.
- /api/submit: Submit user preferences and create a new user.

Usage:
Register the user_bp blueprint in your Flask app.
"""

@user_bp.route('/api/submit_selection', methods=['POST'])
def submit_selection():
    """
    Submit the selected restaurants for a user and create a user profile.

    Returns:
        Response: JSON with status and user profile or error message.
    """
    data = request.get_json()
    selected_restaurants = data.get('selected_restaurants', [])
    user_id = data.get('user_id')

    if not user_id or not selected_restaurants:
        return jsonify({'error': 'Missing user ID or selected restaurants'}), 400

    try:
        user_prefs_doc = user_repository.get_user_preferences(user_id)
        if not user_prefs_doc:
            return jsonify({'error': 'User preferences not found for city retrieval'}), 404
        city = user_prefs_doc.get('city')
        if isinstance(city, list):
            city = city[0]
        city = city.capitalize() if city else None

        if not city:
            return jsonify({'error': 'City not found in user preferences'}), 400

    except errors.InvalidId:
        return jsonify({'error': 'Invalid user ID format'}), 400
    except Exception as e:
        return jsonify({'error': f'Preferences retrieval error: {e}'}), 400

    user_repository.add_selected_restaurants(user_id, selected_restaurants, city)

    try:
        profile = user_service.create_user_profile(ObjectId(user_id), selected_restaurants, city)
        sanitized_profile = sanitize_data(profile)
        return jsonify({"status": "success", "user_profile": sanitized_profile}), 200
    except Exception as e:
        print("Error saving selection or creating profile:", e)
        return jsonify({"error": "Failed to save selection"}), 500

@user_bp.route('/api/submit', methods=['POST'])
def submit_preferences():
    """
    Submit user preferences and create a new user.

    Returns:
        Response: JSON with status and user ID or error message.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    user_data = {
        'nickname': data.get('nickname', ''),
        'city': data.get('city', ''),
        'dietary_preferences': [data.get('dietary')] if data.get('dietary') and data.get('dietary') != 'None' else [],
        'cuisine_preferences': data.get('cuisines', []),
        'price_range': data.get('price', []),
        'dining_priority': {item: i + 1 for i, item in enumerate(data.get('priorities', []))},
        'restaurant_type': data.get('restaurantType', []),
        'wifi': ['Wifi'] if data.get('wifiRequired') is True else []
    }
    result = user_repository.save_user_preferences(user_data)
    return jsonify({'status': 'success', 'user_id': str(result.inserted_id)}), 200 