// src/components/RestaurantGrid.tsx
import React from "react";
import RestaurantCard from "./RestaurantCard";
import type { Restaurant } from "../types";

interface Props {
  restaurants: Restaurant[];
  selectedIdSet?: Set<number>;
  selectable?: boolean;
  onToggleSelect?: (r: Restaurant) => void;
}

const RestaurantGrid: React.FC<Props> = ({
  restaurants,
  selectedIdSet,
  selectable,
  onToggleSelect,
}) => (
  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 gap-12 pb-8">
    {restaurants.map((r) => (
      <RestaurantCard
        key={r.id}
        restaurant={r}
        selectable={selectable}
        selected={selectedIdSet?.has(r.id) ?? false}
        onToggleSelect={onToggleSelect}
      />
    ))}
  </div>
);

export default RestaurantGrid;
