import React, { useState } from "react";
import { menuItems } from "../menu.js";
import SectionHeading from "./SectionHeading.jsx";

export default function MenuSection({ onDishOpen }) {
  const [category, setCategory] = useState("All plates");
  const [diet, setDiet] = useState("All");
  const categories = ["All plates", "Small plates", "From the kitchen", "Something sweet"];
  const diets = ["All", "Vegetarian", "Gluten-free"];
  const visibleItems = menuItems.filter((item) =>
    (category === "All plates" || item.category === category) &&
    (diet === "All" || item.diets.includes(diet)),
  );
  return (
    <section className="menu-section section-pad reveal" id="menu" aria-labelledby="menu-title">
      <div className="menu-top">
        <SectionHeading eyebrow="Made for passing around" titleId="menu-title" title={<>A little of this,<br /><em>a little of that.</em></>} copy="A seasonal menu inspired by the shores of the Mediterranean and whatever looks lovely at the market today." />
        <div className="menu-aside"><span className="menu-aside-icon">✳</span><p>Cooked with the seasons.<br />Served with a little sunshine.</p></div>
      </div>
      <div className="menu-controls">
        <div className="category-tabs" role="group" aria-label="Filter menu by course">
          {categories.map((item) => <button key={item} type="button" className={category === item ? "active" : ""} aria-pressed={category === item} onClick={() => setCategory(item)}>{item}</button>)}
        </div>
        <label className="diet-select">Dietary
          <select value={diet} onChange={(event) => setDiet(event.target.value)} aria-label="Filter by dietary preference">
            {diets.map((item) => <option key={item}>{item}</option>)}
          </select>
        </label>
      </div>
      <div className="menu-grid" aria-live="polite">
        {visibleItems.map((item) => <article className="menu-card reveal" key={item.id}>
          <button type="button" className="dish-image-button" onClick={() => onDishOpen(item)} aria-label={`View details for ${item.name}`}>
            <img src={`https://images.unsplash.com/${item.image}?auto=format&fit=crop&w=700&q=85`} alt="" loading="lazy" />
            <span className="dish-open" aria-hidden="true">+</span>
          </button>
          <div className="dish-heading"><h3>{item.name}</h3><span>{item.price}</span></div>
          {item.recommended && <span className="recommendation">A house favorite</span>}
          <p className="dish-description">{item.description}</p>
          <div className="dish-footer">
            <div className="diet-tags">{item.diets.map((tag) => <span key={tag}>{tag}</span>)}</div>
            <button type="button" className="detail-link" onClick={() => onDishOpen(item)}>Details <svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M3 10h13m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" /></svg></button>
          </div>
          <p className="allergen-inline">Contains: {item.allergens.length ? item.allergens.join(", ") : "No listed major allergens"}</p>
        </article>)}
      </div>
      {visibleItems.length === 0 && <p className="empty-menu">No plates match those filters. Try another combination.</p>}
      <p className="menu-footnote">Allergens and cross-contact: please ask our team before ordering. Menu and prices may change with the season.</p>
    </section>
  );
}
