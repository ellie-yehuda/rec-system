import React, { useEffect, useState } from "react";
import RestaurantGrid from "@components/RestaurantGrid";
import type { Restaurant } from "../types";

interface HomeResponse {
  personalized: Restaurant[];
  positive: Restaurant[];
}

const Home: React.FC = () => {
  const [personalized, setPersonalized] = useState<Restaurant[]>([]);
  const [positive, setPositive] = useState<Restaurant[]>([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/home");
        const json = (await res.json()) as HomeResponse;
        setPersonalized(json.personalized);
        setPositive(json.positive);
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    window.location.href = `/search?query=${encodeURIComponent(query)}`;
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: "url(/static/images/cuisines4.gif)" }}
    >
      <div className="bg-white/80 backdrop-blur-md p-10 rounded-2xl w-full max-w-6xl space-y-12">
        <h1 className="text-4xl font-bold text-center">
          Welcome to Your Restaurant Guide
        </h1>

        <form onSubmit={handleSearch} className="flex justify-center gap-4 max-w-xl mx-auto">
          <input
            type="text"
            placeholder="Search by cuisine or restaurant name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring focus:ring-primary/50"
          />
          <button
            type="submit"
            className="px-6 py-2 rounded-lg bg-primary text-white font-semibold hover:bg-primary/80 transition"
          >
            Search
          </button>
        </form>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Personalized Restaurants For You</h2>
          <RestaurantGrid restaurants={personalized} />
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Hot Restaurants Around You</h2>
          <RestaurantGrid restaurants={positive} />
        </section>
      </div>
    </div>
  );
};
export default Home; 