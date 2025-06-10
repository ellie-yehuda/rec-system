// src/types.ts

/**
 * Type definitions for the restaurant recommendation system.
 * 
 * Contains interfaces and types used throughout the frontend application.
 */

/**
 * Restaurant interface representing a restaurant entity.
 * Contains all properties returned by the backend API.
 * 
 * @property id - Unique identifier for the restaurant
 * @property restaurant_name - Name of the restaurant
 * @property location - Optional physical location/address
 * @property image_urls - Array of image URLs for the restaurant
 * @property general_rating - Optional overall rating (0-5)
 * @property food_rating - Optional food quality rating (0-5)
 * @property value_rating - Optional value for money rating (0-5)
 * @property atmosphere_rating - Optional ambiance rating (0-5)
 * @property service_rating - Optional service quality rating (0-5)
 * 
 * Cuisine type flags (boolean):
 * @property is_italian - Italian cuisine
 * @property is_asian - Asian cuisine
 * @property is_french - French cuisine
 * @property is_mediterranean - Mediterranean cuisine
 * @property is_fast_food - Fast food
 * @property is_indian - Indian cuisine
 * @property is_seafood - Seafood
 * @property is_steakhouse - Steakhouse
 * @property is_middle_eastern - Middle Eastern cuisine
 * @property is_mexican - Mexican cuisine
 * @property is_british - British cuisine
 * @property is_cafe - Café
 * 
 * Dietary flags (boolean):
 * @property is_vegan_options - Has vegan options
 * @property is_vegetarian_friendly - Vegetarian friendly
 * @property is_gluten_free_options - Has gluten-free options
 * 
 * Price range flags (boolean):
 * @property is_price_$ - Budget friendly
 * @property is_price_$$ - Moderate
 * @property is_price_$$$ - Expensive
 * @property is_price_$$$$ - Very expensive
 * 
 * Amenities (boolean):
 * @property is_free_wifi - Offers free WiFi
 * 
 * @property feedback - Array of feedback tuples [phrase, count, sentimentScore]
 */
export interface Restaurant {
  id: number;
  restaurant_name: string;
  location?: string;

  // If your API already returns image URLs in a field called `image_urls`, include that here:
  image_urls: string[];

  // If your API returns an overall (general) rating:
  general_rating?: number;

  // If your API returns detailed sub-ratings:
  food_rating?: number;
  value_rating?: number;
  atmosphere_rating?: number;
  service_rating?: number;

  // Flags for cuisine/diet/price/amenity tags (set `true` if applicable):
  is_italian?: boolean;
  is_asian?: boolean;
  is_french?: boolean;
  is_mediterranean?: boolean;
  is_fast_food?: boolean;
  is_indian?: boolean;
  is_seafood?: boolean;
  is_steakhouse?: boolean;
  is_middle_eastern?: boolean;
  is_mexican?: boolean;
  is_british?: boolean;
  is_cafe?: boolean;

  is_vegan_options?: boolean;
  is_vegetarian_friendly?: boolean;
  is_gluten_free_options?: boolean;

  is_price_$?: boolean;
  is_price_$$?: boolean;
  is_price_$$$?: boolean;
  is_price_$$$$?: boolean;

  is_free_wifi?: boolean;

  // Feedback array: each entry is [phrase, count, sentimentScore]
  feedback?: [string, number, number][];
}
