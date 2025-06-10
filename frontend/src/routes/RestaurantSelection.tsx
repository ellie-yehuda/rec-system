// src/routes/RestaurantSelection.tsx
import React, { useEffect, useState } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import RestaurantGrid from "@components/RestaurantGrid";
import type { Restaurant } from "../types";
import { useApi } from "../hooks/useApi";

type FullRestaurant = Restaurant & {
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

const RestaurantSelection: React.FC = () => {
  const navigate = useNavigate();
  const { userId } = useParams<{ userId: string }>();
  const { data, loading, error } = useApi<{ restaurants: Restaurant[] }>(
    `/api/restaurants/${userId}`
  );

  const [selected, setSelected] = useState<Restaurant[]>([]);

  const handleToggleSelect = (r: Restaurant) => {
    setSelected((prev) =>
      prev.some((pr) => pr.id === r.id)
        ? prev.filter((pr) => pr.id !== r.id)
        : [...prev, r]
    );
  };

  const { doFetch: submitSelection } = useApi(`/api/submit_selection`);

  const handleSubmit = () => {
    submitSelection({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        selected_restaurants: selected.map((r) => r.id),
      }),
    });
    navigate(`/home/${userId}`);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div
      className="
        relative flex flex-col items-center 
        min-h-screen bg-cover bg-center font-sans
      "
      style={{
        backgroundImage: "url(/static/images/cuisines4.gif)",
      }}
    >
      {/* semi-transparent overlay (Glassmorphism effect) */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/80 to-white/60 backdrop-blur-lg"></div>

      {/* Hero/Banner Section */}
      <div className="relative z-10 w-full text-center py-20 px-4 bg-gradient-to-br from-teal-500 to-green-600 shadow-lg">
        <h1 className="text-6xl font-extrabold text-white mb-6 drop-shadow-md">
          Discover Your Next Favorite Meal
        </h1>
        <p className="text-2xl font-light text-white text-opacity-90 max-w-3xl mx-auto">
          Hand-picked restaurants just for you. Select 3 to personalize your recommendations!
        </p>
      </div>

      {/* “container” white card */}
      <div className="relative bg-white/80 backdrop-blur-md rounded-xl p-10 my-12 mx-auto shadow-xl w-full max-w-7xl z-10">
        {/* Header above grid with selection count and submit button */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-gray-800">
            Your Selections:
            <span className={`ml-2 text-3xl font-bold ${selected.length === 3 ? "text-teal-600" : "text-gray-400"}`}>
              {selected.length}/3
            </span>
          </h2>
          <button
            onClick={handleSubmit}
            disabled={selected.length !== 3}
            className="
              px-6 py-3 rounded-full font-bold text-white text-lg
              bg-teal-600 hover:bg-teal-700 transition duration-300 transform hover:-translate-y-1 hover:shadow-lg
              disabled:bg-gray-300 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none
            "
          >
            Submit ({selected.length}/3)
          </button>
        </div>

        {/* Restaurant grid */}
        <RestaurantGrid
          restaurants={data?.restaurants || []}
          selectable
          selectedRestaurants={selected}
          onToggleSelect={handleToggleSelect}
        />
      </div>
    </div>
  );
};

export default RestaurantSelection;
