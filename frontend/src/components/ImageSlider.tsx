// src/components/ImageSlider.tsx
import React, { useState } from "react";

interface ImageSliderProps {
  images: string[];
  altText?: string; // fallback alt
}

const ImageSlider: React.FC<ImageSliderProps> = ({ images, altText }) => {
  const [idx, setIdx] = useState(0);
  if (images.length === 0) return null;

  const prev = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIdx((i) => (i - 1 + images.length) % images.length);
  };
  const next = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIdx((i) => (i + 1) % images.length);
  };

  return (
    <div className="relative w-full h-36 overflow-hidden rounded-md mb-2">
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
