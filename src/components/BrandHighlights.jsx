import React from "react";

export default function BrandHighlights() {
  return (
    <section className="brand-highlights section-pad reveal" aria-labelledby="brand-highlights-title">
      <p className="eyebrow">The Oliva feeling</p>
      <h2 id="brand-highlights-title">A little more <em>together.</em></h2>
      <div className="brand-highlights-grid">
        <article><span aria-hidden="true">✳</span><h3>Come as you are</h3><p>Neighborhood dinners, long lunches, and one more chair pulled up when you need it.</p></article>
        <article><span aria-hidden="true">✳</span><h3>Made with the season</h3><p>Thoughtful plates inspired by the market, the moment, and the pleasure of sharing.</p></article>
        <article><span aria-hidden="true">✳</span><h3>Stay a little</h3><p>Good food is only the beginning. Leave room for another story around the table.</p></article>
      </div>
    </section>
  );
}
