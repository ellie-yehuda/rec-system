// src/components/ImageSlider.tsx
import React, { useState } from "react";

/**
 * Props for the ImageSlider component
 * 
 * @property images - Array of image URLs to display
 * @property altText - Optional alt text for accessibility (falls back to "Slide N")
 */
interface ImageSliderProps {
  images: string[];
  altText?: string;
}

/**
 * A responsive image slider that displays images in a carousel format.
 * Features:
 * - Circular navigation (wraps around at ends)
 * - Fade transition between images
 * - Accessible navigation controls
 * - Responsive image sizing
 */
const ImageSlider: React.FC<ImageSliderProps> = ({ images, altText }) => {
  // Track current image index
  const [idx, setIdx] = useState(0);
  
  // Don't render if no images provided
  if (images.length === 0) return null;

  // Navigate to previous image with wraparound
  const prev = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent event bubbling
    setIdx((i) => (i - 1 + images.length) % images.length);
  };

  // Navigate to next image with wraparound
  const next = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent event bubbling
    setIdx((i) => (i + 1) % images.length);
  };

  return (
    <div className="relative w-full h-36 overflow-hidden rounded-md mb-2">
      {/* Render all images, showing only the current one */}
      {images.map((src, i) => (
        <img
          key={i}
          src={src}
          alt={altText || `Slide ${i + 1}`}
          className={`absolute inset-0 object-cover w-full h-full transition-opacity duration-300 ${
            i === idx ? "opacity-100" : "opacity-0"
          }`}
        />
      ))}

      {/* Navigation buttons */}
      <button
        onClick={prev}
        className="absolute top-1/2 left-2 transform -translate-y-1/2 bg-black/50 text-white px-2 py-1 rounded-full"
      >
        ←
      </button>
      <button
        onClick={next}
        className="absolute top-1/2 right-2 transform -translate-y-1/2 bg-black/50 text-white px-2 py-1 rounded-full"
      >
        →
      </button>
    </div>
  );
};

export default ImageSlider;
