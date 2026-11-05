import React from "react";

export default function SectionHeading({ eyebrow, title, copy, light = false, titleId }) {
  return (
    <div className={`section-heading reveal ${light ? "section-heading-light" : ""}`}>
      <p className="eyebrow">{eyebrow}</p>
      <h2 id={titleId}>{title}</h2>
      {copy && <p className="section-copy">{copy}</p>}
    </div>
  );
}
