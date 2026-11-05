import React from "react";

export default function Footer() {
  return (
    <footer className="site-footer">
      <a className="brand brand-footer" href="#home" aria-label="Aster and Olive, home"><span className="brand-mark" aria-hidden="true">✳</span><span>ASTER <i>&</i> OLIVE</span></a>
      <p>A good meal is a little celebration.</p>
      <nav className="footer-nav" aria-label="Footer navigation">
        <a href="#story">Our story</a>
        <a href="#menu">The menu</a>
        <a href="#gallery">Gallery</a>
        <a href="#reservations">Reservations</a>
      </nav>
      <span>© {new Date().getFullYear()} Aster & Olive</span>
    </footer>
  );
}
