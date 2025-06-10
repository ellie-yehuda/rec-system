// src/components/RestaurantCard.tsx
import React, { useState, useRef } from "react";
import ImageSlider from "./ImageSlider";
import type { Restaurant } from "../types";

/**
 * Props for the RestaurantCard component
 * 
 * @property restaurant - Restaurant object with extended properties
 * @property selectable - Whether the card is selectable
 * @property selected - Whether the restaurant is currently selected
 * @property onToggleSelect - Callback when selection state changes
 */
interface Props {
  restaurant: Restaurant & {
    image_urls: string[];
    general_rating?: number;
    food_rating?: number;
    value_rating?: number;
    atmosphere_rating?: number;
    service_rating?: number;
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
    feedback?: [string, number, number][];
  };
  selectable?: boolean;
  selected?: boolean;
  onToggleSelect?: (r: Restaurant) => void;
}

/**
 * Star rating component that displays a rating out of 5 stars.
 * Supports half stars and handles undefined ratings.
 */
const StarRating: React.FC<{ rating?: number }> = ({ rating }) => {
  if (rating === undefined) return <span className="text-gray-400">N/A</span>;
  const fullStars = Math.floor(rating);
  const halfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
  return (
    <div className="flex items-center space-x-0.5">
      {[...Array(fullStars)].map((_, i) => (
        <svg key={`full-${i}`} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.986 6.095a1 1 0 00.95.691h6.417c.969 0 1.371 1.24.588 1.81l-5.188 3.774a1 1 0 00-.364 1.118l1.987 6.095c.3.921-.755 1.683-1.543 1.118l-5.188-3.774a1 1 0 00-1.176 0l-5.188 3.774c-.788.565-1.843-.2-1.543-1.118l1.987-6.095a1 1 0 00-.364-1.118L2.05 11.523c-.783-.57-.381-1.81.588-1.81h6.417a1 1 0 00.95-.691l1.986-6.095z" />
        </svg>
      ))}
      {halfStar && (
        <svg className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <defs>
            <linearGradient id="half-star-gradient">
              <stop offset="50%" stopColor="#FACC15" />
              <stop offset="50%" stopColor="#D1D5DB" />
            </linearGradient>
          </defs>
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.986 6.095a1 1 0 00.95.691h6.417c.969 0 1.371 1.24.588 1.81l-5.188 3.774a1 1 0 00-.364 1.118l1.987 6.095c.3.921-.755 1.683-1.543 1.118l-5.188-3.774a1 1 0 00-1.176 0l-5.188 3.774c-.788.565-1.843-.2-1.543-1.118l1.987-6.095a1 1 0 00-.364-1.118L2.05 11.523c-.783-.57-.381-1.81.588-1.81h6.417a1 1 0 00.95-.691l1.986-6.095z" fill="url(#half-star-gradient)" />
        </svg>
      )}
      {[...Array(emptyStars)].map((_, i) => (
        <svg key={`empty-${i}`} className="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.986 6.095a1 1 0 00.95.691h6.417c.969 0 1.371 1.24.588 1.81l-5.188 3.774a1 1 0 00-.364 1.118l1.987 6.095c.3.921-.755 1.683-1.543 1.118l-5.188-3.774a1 1 0 00-1.176 0l-5.188 3.774c-.788.565-1.843-.2-1.543-1.118l1.987-6.095a1 1 0 00-.364-1.118L2.05 11.523c-.783-.57-.381-1.81.588-1.81h6.417a1 1 0 00.95-.691l1.986-6.095z" />
        </svg>
      ))}
    </div>
  );
};

/**
 * Feedback popover component that displays user feedback in a floating tooltip.
 * Shows sentiment analysis with emojis and feedback counts.
 */
const FeedbackPopover: React.FC<{
  feedback: [string, number, number][];
  onOpenChange?: (open: boolean) => void;
}> = ({ feedback, onOpenChange }) => {
  const [open, setOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Notify parent of open state change
  React.useEffect(() => {
    onOpenChange?.(open);
  }, [open, onOpenChange]);

  // Helper function to determine feedback sentiment class
  const getFeedbackClass = (sentiment: number) => {
    if (sentiment > 0.15) return "bg-green-100 text-green-800";
    if (sentiment < -0.15) return "bg-red-100 text-red-700";
    return "bg-blue-100 text-blue-700";
  };

  // Helper function to determine feedback sentiment emoji
  const getFeedbackIcon = (sentiment: number) => {
    if (sentiment > 0.15) return "👍";
    if (sentiment < -0.15) return "👎";
    return "😐";
  };

  return (
    <div className="relative inline-block">
      <button
        type="button"
        className="px-3 py-1 text-xs rounded-full bg-gray-100 hover:bg-gray-200 border shadow transition-all duration-200 font-semibold text-gray-700 animate-glow animate-bounce hover:scale-105"
        onMouseEnter={() => {
          timerRef.current = setTimeout(() => setOpen(true), 80);
        }}
        onMouseLeave={() => {
          if (timerRef.current) clearTimeout(timerRef.current);
          setOpen(false);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
      >
        🗣️ People are saying…
      </button>
      {open && (
        <div
          className="absolute left-1/2 -translate-x-1/2 z-20 top-full mt-2 min-w-[200px] max-w-xs bg-white bg-opacity-90 backdrop-blur-lg border border-gray-200 shadow-xl rounded-xl px-4 py-3 animate-fade-in text-gray-900"
          style={{ pointerEvents: "none" }}
        >
          <div className="mb-2 font-semibold text-gray-700 text-xs">Top feedback:</div>
          <div className="flex flex-wrap gap-2">
            {feedback.length === 0 && (
              <span className="text-gray-400 text-xs">No recent comments</span>
            )}
            {feedback.map(([phrase, count, sentiment], i) => (
              <span
                key={i}
                className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getFeedbackClass(
                  sentiment
                )} shadow-sm`}
              >
                {getFeedbackIcon(sentiment)} {phrase}
                <span className="ml-1 opacity-60">({count})</span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

/**
 * Main RestaurantCard component that displays restaurant information
 * in a card format with image slider, ratings, and feedback.
 */
const RestaurantCard: React.FC<Props> = ({
  restaurant,
  selectable = false,
  selected = false,
  onToggleSelect,
}) => {
  const [isFeedbackPopoverOpen, setIsFeedbackPopoverOpen] = useState(false);

  // Filter feedback to show only items with 2+ mentions, limited to top 3
  const filteredFeedback = (restaurant.feedback || [])
    .filter((item) => item[1] >= 2)
    .slice(0, 3);

  return (
    <div
      className={`
        relative bg-white rounded-xl shadow-lg p-4 flex flex-col items-center text-center 
        max-w-2xl transition-all duration-300 transform
        ${
          selected
            ? "ring-4 ring-teal-400 scale-105 shadow-xl"
            : "hover:-translate-y-2 hover:shadow-xl hover:ring-2 hover:ring-teal-200"
        }
        ${selectable ? "cursor-pointer" : ""} 
        ${isFeedbackPopoverOpen ? "z-30" : ""}
      `}
    >
      {selected && (
        <div className="absolute top-2 right-2 bg-teal-500 text-white rounded-full p-2 text-xs font-bold z-40">
          ✓ Selected
        </div>
      )}

      {/* Image slider */}
      <div className="w-full h-40 rounded-lg overflow-hidden mb-4 shadow-md">
        <ImageSlider images={restaurant.image_urls} altText={restaurant.restaurant_name} />
      </div>

      {/* Name + location */}
      <div className="restaurant-details mb-3 flex-grow">
        <h2 className="font-bold text-xl text-gray-800">{restaurant.restaurant_name}</h2>
        {restaurant.location && (
          <p className="text-gray-500 text-sm">{restaurant.location}</p>
        )}
      </div>

      {/* General rating bubble with stars */}
      <div className="flex items-center bg-teal-50 text-teal-700 font-semibold rounded-full px-4 py-2 text-md mb-3 shadow-sm">
        <span className="mr-2">Overall:</span>
        <StarRating rating={restaurant.general_rating} />
        <span className="ml-2 text-sm">({restaurant.general_rating?.toFixed(1) ?? "N/A"}/5)</span>
      </div>

      {/* Feedback Popover Button (compact) */}
      {filteredFeedback.length > 0 && (
        <div className="flex justify-center mb-3 w-full">
          <FeedbackPopover feedback={filteredFeedback} onOpenChange={setIsFeedbackPopoverOpen} />
        </div>
      )}

      {/* Cuisine/Price/Amenities tags */}
      <div className="flex flex-wrap gap-2 justify-center mb-3 w-full">
        {restaurant.is_italian && (
          <span className="bg-red-100 text-red-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🍝 Italian</span>
        )}
        {restaurant.is_asian && (
          <span className="bg-purple-100 text-purple-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🍜 Asian</span>
        )}
        {restaurant.is_french && (
          <span className="bg-yellow-100 text-yellow-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🥖 French</span>
        )}
        {restaurant.is_mediterranean && (
          <span className="bg-blue-100 text-blue-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🥗 Mediterranean</span>
        )}
        {restaurant.is_fast_food && (
          <span className="bg-orange-100 text-orange-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🍔 Fast Food</span>
        )}
        {restaurant.is_indian && (
          <span className="bg-pink-100 text-pink-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🥘 Indian</span>
        )}
        {restaurant.is_seafood && (
          <span className="bg-teal-100 text-teal-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🦞 Seafood</span>
        )}
        {restaurant.is_steakhouse && (
          <span className="bg-orange-100 text-orange-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🥩 Steakhouse</span>
        )}
        {restaurant.is_middle_eastern && (
          <span className="bg-teal-100 text-teal-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🥙 Middle Eastern</span>
        )}
        {restaurant.is_mexican && (
          <span className="bg-lime-100 text-lime-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🌮 Mexican</span>
        )}
        {restaurant.is_british && (
          <span className="bg-violet-100 text-violet-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🇬🇧 British</span>
        )}
        {restaurant.is_cafe && (
          <span className="bg-yellow-100 text-yellow-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">☕ Cafe</span>
        )}
        {restaurant.is_vegan_options && (
          <span className="bg-green-100 text-green-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🌱 Vegan Options</span>
        )}
        {restaurant.is_vegetarian_friendly && (
          <span className="bg-green-100 text-green-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🥗 Vegetarian Friendly</span>
        )}
        {restaurant.is_gluten_free_options && (
          <span className="bg-yellow-100 text-yellow-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">🌾 Gluten-Free</span>
        )}
        {restaurant.is_price_$ && (
          <span className="bg-gray-100 text-gray-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">$</span>
        )}
        {restaurant.is_price_$$ && (
          <span className="bg-gray-200 text-gray-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">$$</span>
        )}
        {restaurant.is_price_$$$ && (
          <span className="bg-gray-300 text-gray-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">$$$</span>
        )}
        {restaurant.is_price_$$$$ && (
          <span className="bg-gray-400 text-gray-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">$$$$</span>
        )}
        {restaurant.is_free_wifi && (
          <span className="bg-indigo-100 text-indigo-700 text-xs font-medium px-3 py-1 rounded-full shadow-sm">📶 Free Wi-Fi</span>
        )}
      </div>

      {/* Select Button */}
      {selectable && (
        <button
          onClick={() => onToggleSelect?.(restaurant)}
          className={`
            w-full py-2 rounded-full font-semibold text-white 
            transition duration-300 transform
            ${
              selected
                ? "bg-red-500 hover:bg-red-600"
                : "bg-teal-600 hover:bg-teal-700 hover:-translate-y-0.5 shadow-md"
            }
          `}
        >
          {selected ? "Deselect" : "Select"}
        </button>
      )}
    </div>
  );
};

export default RestaurantCard;
