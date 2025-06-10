// import React, { useEffect, useState } from "react";
// import { DragDropContext, Droppable, Draggable, type DropResult } from "@hello-pangea/dnd";
// import { useNavigate } from "react-router-dom";
// import RestaurantCard from "@components/RestaurantCard";
// import type { Restaurant } from "../types";

// const Rating: React.FC = () => {
//   const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
//   const navigate = useNavigate();

//   useEffect(() => {
//     fetch("/api/selection")
//       .then((res) => res.json())
//       .then((data: Restaurant[]) => setRestaurants(data))
//       .catch(console.error);
//   }, []);

//   const handleDragEnd = (result: DropResult) => {
//     if (!result.destination) return;
//     const newArray = Array.from(restaurants);
//     const [moved] = newArray.splice(result.source.index, 1);
//     newArray.splice(result.destination.index, 0, moved);
//     setRestaurants(newArray);
//   };

//   const handleSubmit = async () => {
//     await fetch("/api/rate", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ ordered_ids: restaurants.map((r) => r.id) }),
//     });
//     navigate("/");
//   };

//   return (
//     <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-8">
//       <h1 className="text-3xl font-bold mb-6">Drag the Restaurants to Rank Them</h1>

//       <DragDropContext onDragEnd={handleDragEnd}>
//         <Droppable droppableId="rankings">
//           {(provided: any) => (
//             <div ref={provided.innerRef} {...provided.droppableProps} className="space-y-4 w-full max-w-xl">
//               {restaurants.map((r, idx) => (
//                 <Draggable key={r.id} draggableId={r.id.toString()} index={idx}>
//                   {(p: any) => (
//                     <div ref={p.innerRef} {...p.draggableProps} {...p.dragHandleProps}>
//                       <RestaurantCard restaurant={r} draggable />
//                     </div>
//                   )}
//                 </Draggable>
//               ))}
//               {provided.placeholder}
//             </div>
//           )}
//         </Droppable>
//       </DragDropContext>

//       <button onClick={handleSubmit} className="mt-10 px-8 py-3 rounded-lg font-semibold text-white bg-primary">
//         Save Ranking
//       </button>
//     </div>
//   );
// };
// export default Rating; 