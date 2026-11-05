import React from "react";
import { galleryImages } from "../menu.js";
import SectionHeading from "./SectionHeading.jsx";

export default function Gallery({ onImageOpen }) {
  return (
    <section className="gallery-section section-pad reveal" id="gallery" aria-labelledby="gallery-title">
      <SectionHeading eyebrow="A seat at our table" titleId="gallery-title" title={<>The little moments<br /><em>are the big ones.</em></>} copy="A glimpse of the good things waiting around the table." />
      <div className="gallery-grid">
        {galleryImages.map((image, index) => <button className={`gallery-tile ${image.className}`} key={image.src} type="button" onClick={() => onImageOpen(index)} aria-label={`View image: ${image.alt}`}>
          <img src={`https://images.unsplash.com/${image.src}?auto=format&fit=crop&w=900&q=85`} alt={image.alt} loading="lazy" />
          <span className="gallery-zoom" aria-hidden="true">↗</span>
        </button>)}
      </div>
    </section>
  );
}
