// src/components/RestaurantGrid.tsx
import React from "react";
import RestaurantCard from "./RestaurantCard";
import type { Restaurant } from "../types";

/**
 * Props for the RestaurantGrid component
 * 
 * @property restaurants - Array of restaurant objects to display
 * @property selectable - Whether restaurants can be selected (optional)
 * @property selectedRestaurants - Array of currently selected restaurants (optional)
 * @property onToggleSelect - Callback when a restaurant is selected/deselected (optional)
 */
interface Props {
  restaurants: Restaurant[];
  selectable?: boolean;
  selectedRestaurants?: Restaurant[];
  onToggleSelect?: (r: Restaurant) => void;
}

/**
 * Renders a responsive grid of restaurant cards.
 * Grid layout adjusts based on screen size:
 * - Mobile: 1 column
 * - Tablet: 2 columns
 * - Desktop: 3 columns
 */
const RestaurantGrid: React.FC<Props> = ({
  restaurants,
  selectable,
  selectedRestaurants = [],
  onToggleSelect,
}) => {
  // Create a Set of selected restaurant IDs for efficient lookup
  const selectedIdSet = new Set(selectedRestaurants.map((r) => r.id));

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {restaurants.map((r) => (
        <RestaurantCard
          key={r.id}
          restaurant={r}
          selectable={selectable}
          selected={selectedIdSet.has(r.id)}
          onToggleSelect={() => onToggleSelect?.(r)}
        />
      ))}
    </div>
  );
};

export default RestaurantGrid;
