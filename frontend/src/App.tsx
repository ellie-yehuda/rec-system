import { Routes, Route, Navigate } from "react-router-dom";
import Welcome from "@routes/Welcome";
import Home from "@routes/Home";
import RestaurantSelection from "@routes/RestaurantSelection";
import Rating from "@routes/Rating";

const App: React.FC = () => (
  <Routes>
    <Route path="/" element={<Welcome />} />
    <Route path="/home" element={<Home />} />
    {/*
      Now `/choose/:userId` → RestaurantSelection will read userId from URL
    */}
    <Route path="/choose/:userId" element={<RestaurantSelection />} />
    <Route path="/rate" element={<Rating />} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
);

export default App;


// import React from "react";
// import { Routes, Route, Navigate } from "react-router-dom";
// import Welcome from "@routes/Welcome";
// import Home from "@routes/Home";
// import RestaurantSelection from "@routes/RestaurantSelection";
// import Rating from "@routes/Rating";

// const App: React.FC = () => (
//   <Routes>
//     <Route path="/" element={<Welcome />} />
//     <Route path="/home" element={<Home />} />
//     <Route path="/choose" element={<RestaurantSelection />} />
//     <Route path="/rate" element={<Rating />} />
//     <Route path="*" element={<Navigate to="/" replace />} />
//   </Routes>
// );

// export default App;
