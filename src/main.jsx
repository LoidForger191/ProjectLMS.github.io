import React from "react";
import { createRoot } from "react-dom/client";
import "./components/styles/base.css";
import "./components/styles/header.css";
import "./components/styles/hero.css";
import "./components/styles/story.css";
import "./components/styles/section-heading.css";
import "./components/styles/seasonal-specials.css";
import "./components/styles/menu.css";
import "./components/styles/brand-highlights.css";
import "./components/styles/gallery.css";
import "./components/styles/reservation.css";
import "./components/styles/visit.css";
import "./components/styles/footer.css";
import "./components/styles/media-dialog.css";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
