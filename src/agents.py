import os
from pathlib import Path

from src.classifier import classify_text_item
from src.utils import normalize_text


def classify_waste(item_text: str, uploaded_image=None) -> dict:
    classification = classify_text_item(item_text)

    if uploaded_image is not None:
        filename = getattr(uploaded_image, "name", "") or ""
        if filename:
            image_text = normalize_text(filename)
            if "battery" in image_text or "phone" in image_text or "device" in image_text:
                classification["category"] = "Hazardous/Special waste" if "battery" in image_text else "E-waste"
                classification["confidence"] = "Medium"
                classification["reason"] = "The uploaded image file suggests an item that may require special handling or e-waste routing."

    return classification
