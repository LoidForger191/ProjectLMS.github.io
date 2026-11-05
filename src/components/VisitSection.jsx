import React from "react";

export default function VisitSection() {
  return (
    <section className="visit-section section-pad reveal" id="visit" aria-labelledby="visit-title">
      <div className="visit-intro">
        <p className="eyebrow">A little more together</p>
        <h2 id="visit-title">Good things happen<br /><em>around the table.</em></h2>
      </div>
      <div className="visit-detail">
        <h3>Made for sharing</h3>
        <p>Seasonal Mediterranean cooking, long lunches, and evenings worth lingering over.</p>
      </div>
      <div className="visit-detail">
        <h3>Take your time</h3>
        <p>Come for something to share. Leave room for one more story around the table.</p>
      </div>
      <a href="#home" className="back-top" aria-label="Back to top">↑</a>
    </section>
  );
}
