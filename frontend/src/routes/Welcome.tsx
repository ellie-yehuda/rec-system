// src/routes/Welcome.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApi } from "../hooks/useApi";

const cuisines = [
  "British",
  "Asian",
  "Italian",
  "Indian",
  "Mediterranean",
  "Fast Food",
  "Seafood",
  "Cafe",
  "French",
  "Steakhouse",
  "Mexican",
  "Middle Eastern",
];

const totalSlides = 6;

const slideIcons = [
  "🌍", // Welcome
  "🏙️", // City
  "🥗", // Dietary
  "🍽️", // Cuisine
  "⭐", // Priorities
  "📶", // Wifi
];

const slideTitles = [
  "Hello, Food Explorer! 🌍🍽️",
  "Let's start with some basics!",
  "Any dietary needs we should know about?",
  "What's your go-to cuisine?",
  "Rank your dining priorities",
  "Is Wi-Fi a must in a restaurant?",
];

const Welcome: React.FC = () => {
  const [slideIndex, setSlideIndex] = useState<number>(0);
  const navigate = useNavigate();

  // form state
  const [city, setCity] = useState<string>("Rome");
  const [nickname, setNickname] = useState<string>("");
  const [dietary, setDietary] = useState<
    "Vegetarian Friendly" | "None" | ""
  >("");
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [priorities, setPriorities] = useState<string[]>([
    "food",
    "value",
    "atmosphere",
    "service",
  ]);
  const [wifiRequired, setWifiRequired] = useState<boolean | null>(null);

  const { data, loading, error, doFetch } = useApi('/api/submit');

  // navigation handlers
  const nextSlide = () => setSlideIndex((i) => Math.min(i + 1, totalSlides - 1));
  const prevSlide = () => setSlideIndex((i) => Math.max(0, i - 1));

  // Submit handler
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      city,
      nickname,
      dietary,
      cuisines: selectedCuisines,
      priorities,
      wifiRequired,
    };
    doFetch({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
  };

  if (data && data.status === 'success' && data.user_id) {
    navigate(`/choose/${data.user_id}`);
  }

  // Progress Dots Component
  const ProgressDots = () => (
    <div className="flex justify-center mb-6 space-x-2">
      {Array.from({ length: totalSlides }).map((_, i) => (
        <div
          key={i}
          className={`w-3 h-3 rounded-full transition-all duration-200 ${
            slideIndex === i
              ? "bg-blue-600 scale-125 shadow-lg"
              : "bg-blue-200"
          }`}
        />
      ))}
    </div>
  );

  // Slide Card Wrapper
  const SlideCard: React.FC<{
    children: React.ReactNode;
    icon: string;
    title: string;
    subtitle?: string;
  }> = ({ children, icon, title, subtitle }) => (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-purple-100 p-4 sm:p-6 lg:p-8 transition-all">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl bg-white bg-opacity-90 backdrop-filter backdrop-blur-lg rounded-3xl shadow-xl p-8 sm:p-10 lg:p-12 border border-gray-200 animate-fade-in-up"
      >
        <ProgressDots />
        <div className="flex flex-col items-center mb-8">
          <div className="flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-4 text-3xl shadow">
            {icon}
          </div>
          <h2 className="text-3xl font-extrabold text-gray-900 mb-2 text-center">
            {title}
          </h2>
          {subtitle && (
            <p className="text-lg text-gray-700 mb-2 text-center">{subtitle}</p>
          )}
        </div>
        {children}
      </form>
    </div>
  );

  // ---- Slides ----
  // Slide 0: Welcome
  if (slideIndex === 0)
    return (
      <SlideCard
        icon={slideIcons[0]}
        title={slideTitles[0]}
        subtitle="Your ultimate Restaurant Recommendation Adventure begins here. Discover deliciousness tailored just for you."
      >
        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
          <div className="p-4 bg-white bg-opacity-80 rounded-2xl shadow hover:shadow-lg transition-all">
            <div className="text-3xl mb-2">✨</div>
            <div className="font-semibold mb-1">Personalized Picks</div>
            <div className="text-gray-600 text-sm">
              Recommendations tailored to your unique tastes.
            </div>
          </div>
          <div className="p-4 bg-white bg-opacity-80 rounded-2xl shadow hover:shadow-lg transition-all">
            <div className="text-3xl mb-2">📍</div>
            <div className="font-semibold mb-1">Explore Local Gems</div>
            <div className="text-gray-600 text-sm">
              Find hidden culinary treasures in your city.
            </div>
          </div>
          <div className="p-4 bg-white bg-opacity-80 rounded-2xl shadow hover:shadow-lg transition-all">
            <div className="text-3xl mb-2">💬</div>
            <div className="font-semibold mb-1">Community Reviews</div>
            <div className="text-gray-600 text-sm">
              Read honest reviews and share your experiences.
            </div>
          </div>
        </div>
        {/* Testimonial */}
        <div className="bg-gray-50 rounded-2xl p-6 shadow-inner text-center mb-8">
          <p className="text-lg text-gray-800 italic leading-relaxed mb-2">
            "This app transformed my dining experience! Found my new favorite spot thanks to their amazing recommendations."
          </p>
          <div className="flex items-center justify-center">
            <span className="text-yellow-400 text-xl mr-2">⭐⭐⭐⭐⭐</span>
            <span className="font-medium text-gray-700">— Happy User</span>
          </div>
        </div>
        <button
          type="button"
          onClick={nextSlide}
          className="w-full py-3 mt-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-full shadow-lg hover:shadow-xl transition-all hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300"
        >
          Get Started →
        </button>
      </SlideCard>
    );

  // Slide 1: City & Nickname
  if (slideIndex === 1)
    return (
      <SlideCard
        icon={slideIcons[1]}
        title={slideTitles[1]}
        subtitle="Tell us a bit about yourself to get personalized results."
      >
        <div className="mb-6">
          <label htmlFor="city" className="block font-medium mb-1 text-left">
            Select City
          </label>
          <select
            id="city"
            name="city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-400 focus:ring-blue-400 focus:ring-1"
          >
            <option value="Rome">Rome</option>
            <option value="Paris">Paris</option>
            <option value="London">London</option>
          </select>
        </div>
        <div className="mb-6">
          <label htmlFor="nickname" className="block font-medium mb-1 text-left">
            Enter Nickname
          </label>
          <input
            id="nickname"
            name="nickname"
            type="text"
            required
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
            className="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-400 focus:ring-blue-400 focus:ring-1"
          />
        </div>
        <div className="flex justify-between">
          <div />
          <button
            type="button"
            onClick={nextSlide}
            className="inline-flex items-center px-6 py-2 bg-blue-600 text-white rounded-full font-semibold shadow hover:bg-blue-700 hover:scale-105 transition-all"
          >
            Next →
          </button>
        </div>
      </SlideCard>
    );

  // Slide 2: Dietary Options
  if (slideIndex === 2)
    return (
      <SlideCard
        icon={slideIcons[2]}
        title={slideTitles[2]}
        subtitle="Choose if you have a specific dietary preference."
      >
        <div className="flex flex-col md:flex-row gap-6 justify-center mb-8">
          <button
            type="button"
            onClick={() =>
              setDietary((d) => (d === "Vegetarian Friendly" ? "" : "Vegetarian Friendly"))
            }
            className={`flex-1 py-4 rounded-xl font-semibold shadow text-lg transition-all ${
              dietary === "Vegetarian Friendly"
                ? "bg-green-100 border-2 border-green-400 scale-105"
                : "bg-gray-50 border"
            }`}
          >
            🥗 Vegetarian
          </button>
          <button
            type="button"
            onClick={() => setDietary((d) => (d === "None" ? "" : "None"))}
            className={`flex-1 py-4 rounded-xl font-semibold shadow text-lg transition-all ${
              dietary === "None"
                ? "bg-blue-100 border-2 border-blue-400 scale-105"
                : "bg-gray-50 border"
            }`}
          >
            🍽️ I'm good with all
          </button>
        </div>
        <div className="flex justify-between">
          <button
            type="button"
            onClick={prevSlide}
            className="inline-flex items-center px-6 py-2 bg-gray-200 rounded-full font-semibold hover:bg-gray-300 transition-all"
          >
            ← Back
          </button>
          <button
            type="button"
            onClick={nextSlide}
            disabled={dietary === ""}
            className={`inline-flex items-center px-6 py-2 rounded-full font-semibold ${
              dietary === ""
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700 hover:scale-105 transition-all"
            }`}
          >
            Next →
          </button>
        </div>
      </SlideCard>
    );

  // Slide 3: Cuisine Selection
  if (slideIndex === 3)
    return (
      <SlideCard
        icon={slideIcons[3]}
        title={slideTitles[3]}
        subtitle="Please select up to 5 cuisines you love most."
      >
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
          {cuisines.map((c) => {
            const isChecked = selectedCuisines.includes(c);
            const toggleCuisine = () => {
              setSelectedCuisines((prev) => {
                if (isChecked) return prev.filter((x) => x !== c);
                if (prev.length < 5) return [...prev, c];
                return prev;
              });
            };
            return (
              <button
                type="button"
                key={c}
                onClick={toggleCuisine}
                className={`px-3 py-2 rounded-xl border shadow text-sm font-medium transition-all ${
                  isChecked
                    ? "bg-purple-200 border-purple-500 scale-105 text-purple-800"
                    : "bg-white border-gray-300 text-gray-800"
                }`}
              >
                {c}
              </button>
            );
          })}
        </div>
        <div className="flex justify-between">
          <button
            type="button"
            onClick={prevSlide}
            className="inline-flex items-center px-6 py-2 bg-gray-200 rounded-full font-semibold hover:bg-gray-300 transition-all"
          >
            ← Back
          </button>
          <button
            type="button"
            onClick={nextSlide}
            disabled={selectedCuisines.length === 0}
            className={`inline-flex items-center px-6 py-2 rounded-full font-semibold ${
              selectedCuisines.length === 0
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700 hover:scale-105 transition-all"
            }`}
          >
            Next →
          </button>
        </div>
      </SlideCard>
    );

  // Slide 4: Rank Priorities
  if (slideIndex === 4)
    return (
      <SlideCard
        icon={slideIcons[4]}
        title={slideTitles[4]}
        subtitle="Drag to reorder from most important to least important."
      >
        <div className="flex flex-col gap-3 mb-8">
          {priorities.map((val, idx) => (
            <div
              key={val}
              className="flex items-center gap-2 p-3 border border-gray-300 rounded-xl bg-white shadow cursor-move"
              draggable
              onDragStart={(e) => e.dataTransfer.setData("priority", val)}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                const dragged = e.dataTransfer.getData("priority");
                if (dragged && dragged !== val) {
                  const from = priorities.indexOf(dragged);
                  const to = idx;
                  const updated = [...priorities];
                  updated.splice(from, 1);
                  updated.splice(to, 0, dragged);
                  setPriorities(updated);
                }
              }}
            >
              <span className="text-lg">
                {val === "food" && "🍽️"}
                {val === "value" && "💰"}
                {val === "atmosphere" && "🎶"}
                {val === "service" && "⭐"}
              </span>
              <span className="font-medium">
                {val === "food" && "Quality of the food"}
                {val === "value" && "Value for money"}
                {val === "atmosphere" && "The atmosphere"}
                {val === "service" && "Stellar service"}
              </span>
              <span className="ml-auto text-xs text-gray-400">
                {idx === 0 && "Most important"}
                {idx === priorities.length - 1 && "Least important"}
              </span>
            </div>
          ))}
        </div>
        <div className="flex justify-between">
          <button
            type="button"
            onClick={prevSlide}
            className="inline-flex items-center px-6 py-2 bg-gray-200 rounded-full font-semibold hover:bg-gray-300 transition-all"
          >
            ← Back
          </button>
          <button
            type="button"
            onClick={nextSlide}
            className="inline-flex items-center px-6 py-2 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 hover:scale-105 transition-all"
          >
            Next →
          </button>
        </div>
      </SlideCard>
    );

  // Slide 5: Wifi
  if (slideIndex === 5)
    return (
      <SlideCard
        icon={slideIcons[5]}
        title={slideTitles[5]}
        subtitle="Let us know if a good Wi-Fi connection is a must."
      >
        <div className="flex gap-4 mb-8 justify-center">
          <button
            type="button"
            onClick={() => setWifiRequired((w) => (w === true ? null : true))}
            className={`flex-1 py-4 rounded-xl font-semibold shadow text-lg transition-all ${
              wifiRequired === true
                ? "bg-blue-100 border-2 border-blue-400 scale-105"
                : "bg-gray-50 border"
            }`}
          >
            📶 Yes!
          </button>
          <button
            type="button"
            onClick={() => setWifiRequired((w) => (w === false ? null : false))}
            className={`flex-1 py-4 rounded-xl font-semibold shadow text-lg transition-all ${
              wifiRequired === false
                ? "bg-purple-100 border-2 border-purple-400 scale-105"
                : "bg-gray-50 border"
            }`}
          >
            🍽️ Not that important
          </button>
        </div>
        <div className="flex justify-between">
          <button
            type="button"
            onClick={prevSlide}
            className="inline-flex items-center px-6 py-2 bg-gray-200 rounded-full font-semibold hover:bg-gray-300 transition-all"
          >
            ← Back
          </button>
          <button
            type="submit"
            className="inline-flex items-center px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-full shadow-lg hover:shadow-xl transition-all hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300"
          >
            Submit
          </button>
        </div>
      </SlideCard>
    );

  // fallback (should never reach)
  return null;
};

export default Welcome;