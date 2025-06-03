// src/routes/RestaurantSelection.tsx
import React, { useEffect, useState } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import RestaurantGrid from "@components/RestaurantGrid";
import type { Restaurant } from "../types";

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
  const [restaurants, setRestaurants] = useState<FullRestaurant[]>([]);
  const [selected, setSelected] = useState<FullRestaurant[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const navigate = useNavigate();
  const location = useLocation();
  const { userId } = useParams<{ userId: string }>();

  useEffect(() => {
    if (!userId) {
      navigate('/'); // Redirect to welcome if no user_id
      return;
    }
    fetch(`http://127.0.0.1:5000/api/restaurants/${userId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Error ${res.status}`);
        }
        return res.json();
      })
      .then((data: FullRestaurant[]) => {
        const processedData = data.map(r => ({
          ...r,
          is_italian: !!r.is_italian,
          is_asian: !!r.is_asian,
          is_french: !!r.is_french,
          is_mediterranean: !!r.is_mediterranean,
          is_fast_food: !!r.is_fast_food,
          is_indian: !!r.is_indian,
          is_seafood: !!r.is_seafood,
          is_steakhouse: !!r.is_steakhouse,
          is_middle_eastern: !!r.is_middle_eastern,
          is_mexican: !!r.is_mexican,
          is_british: !!r.is_british,
          is_cafe: !!r.is_cafe,
          is_vegan_options: !!r.is_vegan_options,
          is_vegetarian_friendly: !!r.is_vegetarian_friendly,
          is_gluten_free_options: !!r.is_gluten_free_options,
          is_price_$: !!r.is_price_$,
          is_price_$$: !!r.is_price_$$,
          is_price_$$$: !!r.is_price_$$$,
          is_price_$$$$: !!r.is_price_$$$$,
          is_free_wifi: !!r.is_free_wifi,
        }));
        console.log("Fetched restaurant data:", processedData);
        setRestaurants(processedData);
        console.log("Fetched restaurant IDs:", processedData.map(r => r.id));
      })
      .catch(console.error);
  }, [location.search, navigate, userId]); // Added userId to dependencies

  const toggleSelect = (r: FullRestaurant) => {
    setSelected((prev) => {
      const exists = prev.some((x) => x.id === r.id);
      if (exists) return prev.filter((x) => x.id !== r.id);
      if (prev.length < 3) return [...prev, r];
      return prev;
    });
  };

  const handleSubmit = async () => {
    try {
      await fetch("/api/selection", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ids: selected.map((r) => r.id) }),
      });
      navigate(`/rate/${userId}`); // Changed navigation to include userId
    } catch (err) {
      console.error(err);
    }
  };

  const filteredRestaurants = restaurants.filter((r) =>
    r.restaurant_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // If userId is missing or no restaurants loaded yet, you can show a loading state
  if (restaurants.length === 0) return <p>Loading restaurants…</p>;

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
          restaurants={filteredRestaurants} // Use filtered restaurants
          selectable
          selectedIdSet={new Set(selected.map((r) => r.id))}
          onToggleSelect={toggleSelect}
        />
      </div>
    </div>
  );
};

export default RestaurantSelection;
