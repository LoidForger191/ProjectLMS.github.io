import React, { useEffect, useState } from "react";

function ArrowIcon() {
  return <svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M3 10h13m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" /></svg>;
}

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = () => setMenuOpen(false);
  useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === "Escape") closeMenu();
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
  return (
    <header className="site-header">
      <a className="brand" href="#home" aria-label="Aster and Olive, home" onClick={closeMenu}>
        <span className="brand-mark" aria-hidden="true">✳</span>
        <span>ASTER <i>&</i> OLIVE</span>
      </a>
      <button className="nav-toggle" type="button" aria-expanded={menuOpen} aria-controls="primary-navigation" onClick={() => setMenuOpen(!menuOpen)}>
        <span className="sr-only">{menuOpen ? "Close navigation" : "Open navigation"}</span>
        <span /><span />
      </button>
      <nav id="primary-navigation" className={`main-nav ${menuOpen ? "is-open" : ""}`} aria-label="Main navigation">
        <a href="#story" onClick={closeMenu}>Our story</a>
        <a href="#menu" onClick={closeMenu}>The menu</a>
        <a href="#gallery" onClick={closeMenu}>The space</a>
        <a href="#reservations" className="nav-cta" onClick={closeMenu}>Plan a visit <ArrowIcon /></a>
      </nav>
    </header>
  );
}
