// src/routes/Home.tsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import RestaurantGrid from "@components/RestaurantGrid";
import type { Restaurant } from "../types";

interface HomeResponse {
  personalized: Restaurant[];
  positive: Restaurant[];
  nickname?: string;
}

const popularCuisines = [
  { label: "Italian", value: "italian" },
  { label: "Asian", value: "asian" },
  { label: "Mediterranean", value: "mediterranean" },
  { label: "Mexican", value: "mexican" },
  { label: "Seafood", value: "seafood" },
  { label: "Vegetarian", value: "vegetarian friendly" },
  { label: "Fast Food", value: "fast food" },
];

const Home: React.FC = () => {
  const [personalized, setPersonalized] = useState<Restaurant[]>([]);
  const [positive, setPositive] = useState<Restaurant[]>([]);
  const [query, setQuery] = useState("");
  const [nick, setNick] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/home");
        const json = (await res.json()) as HomeResponse;
        setPersonalized(json.personalized);
        setPositive(json.positive);
        if (json.nickname) {
          setNick(json.nickname);
        }
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    navigate(`/search?query=${encodeURIComponent(query.trim())}`);
  };

  const handleCuisineClick = (cuisine: string) => {
    navigate(`/search?query=${encodeURIComponent(cuisine)}`);
  };

  const handleRandomPick = () => {
    const combined = [...personalized, ...positive];
    if (combined.length === 0) return;
    const random = combined[Math.floor(Math.random() * combined.length)];
    navigate(`/restaurant/${random.id}`); // assuming you have a detail page
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* NavBar */}
      <nav className="bg-white shadow-md">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-primary cursor-pointer" onClick={() => navigate("/")}>
            🍽️ DineGuide
          </div>
          <ul className="flex space-x-6">
            <li>
              <button
                onClick={() => navigate("/")}
                className="text-gray-700 hover:text-primary transition"
              >
                Home
              </button>
            </li>
            <li>
              <button
                onClick={() => navigate("/choose")}
                className="text-gray-700 hover:text-primary transition"
              >
                Choose
              </button>
            </li>
            <li>
              <button
                onClick={() => navigate("/rate")}
                className="text-gray-700 hover:text-primary transition"
              >
                Rate
              </button>
            </li>
          </ul>
          <div className="text-gray-600 text-sm">
            {nick ? `Hello, ${nick}!` : "Welcome!"}
          </div>
        </div>
      </nav>

      {/* Hero / Search Section */}
      <header
        className="relative flex items-center justify-center h-96 bg-cover bg-center"
        style={{ backgroundImage: "url(/static/images/cuisines4.gif)" }}
      >
        <div className="absolute inset-0 bg-black/40" />
        <div className="relative z-10 text-center text-white px-4">
          <h1 className="text-5xl font-extrabold mb-4 drop-shadow-lg">
            Discover Amazing Restaurants
          </h1>
          <p className="mb-6 text-lg drop-shadow-md">
            Personalized picks and trending spots in your city.
          </p>
          <form
            onSubmit={handleSearch}
            className="flex justify-center items-center gap-2 max-w-lg mx-auto"
          >
            <input
              type="text"
              placeholder="Search by cuisine or name..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full px-4 py-2 rounded-l-lg outline-none text-gray-800"
            />
            <button
              type="submit"
              className="px-6 py-2 rounded-r-lg bg-primary hover:bg-primary/80 transition"
            >
              Search
            </button>
          </form>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-10 flex-1">
        {/* Popular Cuisines */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">
            Popular Cuisines
          </h2>
          <div className="flex space-x-3 overflow-x-auto pb-2">
            {popularCuisines.map((c) => (
              <button
                key={c.value}
                onClick={() => handleCuisineClick(c.value)}
                className="flex-shrink-0 px-4 py-2 bg-gray-100 hover:bg-primary hover:text-white rounded-lg transition"
              >
                {c.label}
              </button>
            ))}
            <button
              onClick={handleRandomPick}
              className="flex-shrink-0 px-4 py-2 bg-yellow-400 hover:bg-yellow-500 text-white rounded-lg transition flex items-center space-x-1"
            >
              <span>🎲</span>
              <span>Random Pick</span>
            </button>
          </div>
        </section>

        {/* Personalized Section */}
        <section className="mb-16">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-gray-800">
              Personalized For You
            </h2>
            <button
              onClick={() => navigate("/choose")}
              className="text-sm text-primary hover:underline"
            >
              Edit Preferences
            </button>
          </div>
          {personalized.length === 0 ? (
            <p className="text-gray-600">Loading personalized picks…</p>
          ) : (
            <RestaurantGrid restaurants={personalized} />
          )}
        </section>

        {/* Trending Section */}
        <section className="mb-16">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-gray-800">
              Trending Around You
            </h2>
            <button
              onClick={() => navigate("/rate")}
              className="text-sm text-primary hover:underline"
            >
              Rate Restaurants
            </button>
          </div>
          {positive.length === 0 ? (
            <p className="text-gray-600">Loading trending spots…</p>
          ) : (
            <RestaurantGrid restaurants={positive} />
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 py-6">
        <div className="container mx-auto px-6 text-center">
          <p className="text-sm text-gray-600">
            © {new Date().getFullYear()} DineGuide. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
