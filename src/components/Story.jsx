import React from "react";

export default function Story() {
  return (
    <section className="story section-pad reveal" id="story" aria-labelledby="story-title">
      <div className="story-image-wrap">
        <img src="https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1100&q=85" alt="A sunlit restaurant table laid with fresh Mediterranean dishes" loading="lazy" />
        <div className="image-stamp" aria-hidden="true"><span>GROWN WITH</span><strong>♥</strong><span>GOODNESS</span></div>
      </div>
      <div className="story-copy">
        <p className="eyebrow">A slower kind of dining</p>
        <h2 id="story-title">Rooted in the<br /><em>sunny side</em> of life.</h2>
        <p>Inspired by long lunches along the Mediterranean coast, Aster & Olive is a neighborhood table built around the things that matter: beautiful ingredients, honest cooking, and making room for one more.</p>
        <p>Our menu follows the seasons and our growers. Everything else follows your lead.</p>
        <a className="text-link" href="#menu">Get to know our menu <svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M3 10h13m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" /></svg></a>
        <span className="story-flourish" aria-hidden="true">✳</span>
      </div>
    </section>
  );
}
