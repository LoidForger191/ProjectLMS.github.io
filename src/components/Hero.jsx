import React from "react";

function ArrowIcon() {
  return <svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M3 10h13m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" /></svg>;
}

export default function Hero() {
  return (
    <section className="hero" id="home" aria-labelledby="hero-title">
      <img className="hero-image" src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=2200&q=85" alt="An intimate restaurant dining room glowing in the evening" fetchPriority="high" />
      <div className="hero-shade" aria-hidden="true" />
      <div className="hero-content">
        <p className="hero-kicker"><span /> A little taste of the Mediterranean <span /></p>
        <h1 id="hero-title">A table for<br /><em>the good life.</em></h1>
        <p className="hero-description">Seasonal plates, a generous pour, and a seat saved just for you.</p>
        <div className="hero-actions">
          <a className="button button-light" href="#menu">Explore the menu <ArrowIcon /></a>
          <a className="button button-outline" href="#reservations">Plan a visit</a>
        </div>
      </div>
      <a className="hero-scroll" href="#story"><span>Scroll to discover</span><span className="scroll-line" /></a>
      <div className="hero-note">GOOD FOOD, GOOD COMPANY<br /><span>MADE FOR SHARING</span></div>
    </section>
  );
}
