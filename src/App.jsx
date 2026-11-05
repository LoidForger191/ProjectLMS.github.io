import React, { useEffect, useState } from "react";
import Header from "./components/Header.jsx";
import Hero from "./components/Hero.jsx";
import Story from "./components/Story.jsx";
import SeasonalSpecials from "./components/SeasonalSpecials.jsx";
import MenuSection from "./components/MenuSection.jsx";
import Gallery from "./components/Gallery.jsx";
import ReservationSection from "./components/ReservationSection.jsx";
import VisitSection from "./components/VisitSection.jsx";
import Footer from "./components/Footer.jsx";
import BrandHighlights from "./components/BrandHighlights.jsx";
import MediaDialog from "./components/MediaDialog.jsx";
import { galleryImages } from "./menu.js";

export default function App() {
  const [media, setMedia] = useState(null);
  useEffect(() => {
    const targets = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      targets.forEach((target) => target.classList.add("is-visible"));
      return undefined;
    }
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });
    targets.forEach((target) => observer.observe(target));
    return () => observer.disconnect();
  }, []);

  return (
    <>
      <a className="skip-link" href="#main-content">Skip to content</a>
      <Header />
      <main id="main-content">
        <Hero />
        <Story />
        <SeasonalSpecials onDishOpen={(item) => setMedia({ type: "dish", item })} />
        <MenuSection onDishOpen={(item) => setMedia({ type: "dish", item })} />
        <BrandHighlights />
        <Gallery onImageOpen={(index) => setMedia({ type: "gallery", index })} />
        <ReservationSection />
        <VisitSection />
      </main>
      <Footer />
      <MediaDialog
        media={media}
        onClose={() => setMedia(null)}
        onGalleryStep={(direction) => setMedia((current) => ({
          ...current,
          index: (current.index + direction + galleryImages.length) % galleryImages.length,
        }))}
      />
    </>
  );
}
