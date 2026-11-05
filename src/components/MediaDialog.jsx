import React, { useEffect, useRef } from "react";
import { galleryImages } from "../menu.js";

const imageUrl = (id, width = 900) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${width}&q=85`;

export default function MediaDialog({ media, onClose, onGalleryStep }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (media && !dialog.open) dialog.showModal();
    if (!media && dialog.open) dialog.close();
  }, [media]);

  function close() {
    dialogRef.current?.close();
    onClose();
  }

  function handleKeyDown(event) {
    if (media?.type !== "gallery") return;
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      onGalleryStep(-1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      onGalleryStep(1);
    }
  }

  return (
    <dialog
      className={`media-dialog ${media?.type === "dish" ? "dish-dialog" : ""}`}
      ref={dialogRef}
      onClose={onClose}
      onKeyDown={handleKeyDown}
      aria-labelledby={media?.type === "dish" ? "dish-dialog-title" : undefined}
      onClick={(event) => {
        if (event.target === dialogRef.current) close();
      }}
      aria-label={media?.type === "dish" ? undefined : "Gallery image"}
    >
      <button className="dialog-close" type="button" onClick={close} aria-label="Close dialog">×</button>
      {media?.type === "dish" && (
        <div className="dish-modal-content">
          <img src={imageUrl(media.item.image, 1000)} alt={media.item.name} />
          <div>
            <p className="eyebrow">{media.item.category}</p>
            <h2 id="dish-dialog-title">{media.item.name}</h2>
            <p>{media.item.detail}</p>
            <div className="dish-modal-bottom">
              <span>{media.item.diets.join(" · ")}</span>
              <strong>{media.item.price}</strong>
            </div>
            <p className="allergen-note">
              Contains: {media.item.allergens?.length ? media.item.allergens.join(", ") : "No listed major allergens"}.
              Ingredients may change and cross-contact is possible; please confirm with our team.
            </p>
          </div>
        </div>
      )}
      {media?.type === "gallery" && (
        <div className="gallery-lightbox-content">
          <button type="button" className="lightbox-step lightbox-previous" onClick={() => onGalleryStep(-1)} aria-label="Previous photo">←</button>
          <img className="gallery-modal-image" src={imageUrl(galleryImages[media.index].src, 1600)} alt={galleryImages[media.index].alt} />
          <button type="button" className="lightbox-step lightbox-next" onClick={() => onGalleryStep(1)} aria-label="Next photo">→</button>
          <p className="lightbox-caption">{galleryImages[media.index].alt}</p>
        </div>
      )}
    </dialog>
  );
}
