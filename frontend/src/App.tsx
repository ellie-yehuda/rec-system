/**
 * Main application component that handles routing.
 * 
 * Defines the following routes:
 * - /: Welcome page for new users
 * - /choose/:userId: Restaurant selection page
 * - /home/:userId: User's home page
 * - *: Redirects to welcome page
 */
import { Routes, Route, Navigate } from "react-router-dom";
import Welcome from "@routes/Welcome";
import Home from "@routes/Home";
import RestaurantSelection from "@routes/RestaurantSelection";
// import Rating from "@routes/Rating";

const App: React.FC = () => (
  <Routes>
    {/* Welcome page - entry point for new users */}
    <Route path="/" element={<Welcome />} />
    
    {/* Restaurant selection page - users choose their preferred restaurants */}
    <Route path="/choose/:userId" element={<RestaurantSelection />} />
    
    {/* Home page - displays user's personalized content */}
    <Route path="/home/:userId" element={<Home />} />
    
    {/* Fallback route - redirects all unmatched paths to welcome page */}
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
);

export default App;
