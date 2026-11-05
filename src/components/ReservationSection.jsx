import React, { useState } from "react";

const today = new Date();
const minDate = [
  today.getFullYear(),
  String(today.getMonth() + 1).padStart(2, "0"),
  String(today.getDate()).padStart(2, "0"),
].join("-");

export default function ReservationSection() {
  const [message, setMessage] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    setMessage("No reservation was made. Online booking is not connected, and your details were not sent or stored.");
  }

  return (
    <section className="reservation-section reveal" id="reservations" aria-labelledby="reservation-title">
      <div className="reservation-image">
        <img src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=85" alt="A candlelit table ready for dinner" loading="lazy" />
      </div>
      <div className="reservation-content">
        <p className="eyebrow">There's always room at the table</p>
        <h2 id="reservation-title">Make an evening<br />of <em>it.</em></h2>
        <p className="reservation-intro">Online booking is not available yet. The form below is a local preview only; it will not check availability, send your details, or create a reservation.</p>
        <form className="reservation-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <label>Your name<input name="name" autoComplete="name" placeholder="How should we greet you?" required maxLength={100} /></label>
            <label>Email address<input name="email" type="email" autoComplete="email" placeholder="you@example.com" required maxLength={254} /></label>
          </div>
          <div className="form-row">
            <label>Preferred date<input name="date" type="date" min={minDate} required /></label>
            <label>Preferred time
              <select name="time" defaultValue="" required>
                <option value="" disabled>Choose a preference</option>
                {["5:30 pm", "6:00 pm", "6:30 pm", "7:00 pm", "7:30 pm", "8:00 pm", "8:30 pm"].map((time) => <option key={time}>{time}</option>)}
              </select>
            </label>
          </div>
          <div className="form-row">
            <label>Party size
              <select name="party" defaultValue="2">
                {[1, 2, 3, 4, 5, 6, 7, 8].map((number) => <option key={number} value={number}>{number} {number === 1 ? "guest" : "guests"}</option>)}
              </select>
            </label>
            <label>Anything we should know?<input name="notes" maxLength={300} placeholder="Optional note for the team" /></label>
          </div>
          <button className="button button-dark" type="submit">Preview reservation request</button>
          <p className="form-notice" role="status" aria-live="polite">
            {message || "Preferred times are not live availability. Submitting will not send or store your details."}
          </p>
        </form>
      </div>
    </section>
  );
}
