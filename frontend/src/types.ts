// src/types.ts

/**
 * The minimal “base” Restaurant shape returned by your backend.
 * Include whatever properties your API actually sends.
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
