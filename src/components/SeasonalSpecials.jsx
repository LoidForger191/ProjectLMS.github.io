import React from "react";
import { menuItems } from "../menu.js";

const specials = [
  { dish: menuItems.find((item) => item.id === "whipped-feta"), note: "A favorite to share" },
  { dish: menuItems.find((item) => item.id === "saffron-chicken"), note: "From the market" },
  { dish: menuItems.find((item) => item.id === "olive-oil-cake"), note: "Save a little room" },
];

export default function SeasonalSpecials({ onDishOpen }) {
  return (
    <section className="specials-section section-pad reveal" aria-labelledby="specials-title">
      <div className="specials-heading">
        <div><p className="eyebrow">A few things we're loving</p><h2 id="specials-title">A taste of <em>the season.</em></h2></div>
        <p>Plates to start a conversation, made for passing around.</p>
      </div>
      <div className="specials-grid">
        {specials.map(({ dish, note }) => (
          <button className="special-card reveal" type="button" key={dish.id} onClick={() => onDishOpen(dish)}>
            <span className="special-image"><img src={`https://images.unsplash.com/${dish.image}?auto=format&fit=crop&w=800&q=85`} alt="" loading="lazy" /><span>{note}</span></span>
            <span className="special-title"><strong>{dish.name}</strong><span>{dish.price}</span></span>
            <span className="special-description">{dish.description}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
