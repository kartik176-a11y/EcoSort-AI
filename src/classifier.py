import re

CATEGORY_DEFINITIONS = {
    "Wet/Biodegradable": {
        "keywords": [
            "banana peel", "food waste", "fruit peel", "vegetable waste", "leftover food",
            "compost", "organic waste", "wet waste", "spoiled food", "garden waste"
        ],
        "reason": "This item is likely organic and suitable for composting or wet-waste streams.",
    },
    "Dry/Recyclable": {
        "keywords": [
            "plastic bottle", "newspaper", "cardboard", "paper", "glass bottle", "metal can",
            "tin can", "aluminium can", "plastic wrapper", "carton", "packaging"
        ],
        "reason": "This item is likely dry waste or recyclable material that can be collected separately.",
    },
    "E-waste": {
        "keywords": [
            "old phone", "mobile phone", "laptop", "charger", "battery", "cable", "electronics",
            "keyboard", "mouse", "pen drive", "usb cable", "headphones"
        ],
        "reason": "This item is electronic or contains electrical components that should not enter ordinary waste bins.",
    },
    "Hazardous/Special waste": {
        "keywords": [
            "used battery", "paint", "chemical", "bleach", "solvent", "motor oil",
            "pesticide", "medication", "expired medicine", "spray can"
        ],
        "reason": "This item may contain hazardous or toxic material and requires special handling.",
    },
    "Other/Uncertain": {
        "keywords": [],
        "reason": "The item is ambiguous and may require local municipal verification before disposal.",
    },
}


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9\s]+", " ", (value or "").lower()).strip()


def classify_text_item(item_text: str) -> dict:
    text = normalize_text(item_text)
    if not text:
        return {
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": "No item description was supplied.",
            "detected_item": "Unknown",
        }

    for category, config in CATEGORY_DEFINITIONS.items():
        if category == "Other/Uncertain":
            continue
        for keyword in config["keywords"]:
            if keyword in text:
                confidence = "High" if len(keyword.split()) > 1 else "Medium"
                return {
                    "category": category,
                    "confidence": confidence,
                    "reason": config["reason"],
                    "detected_item": item_text.strip(),
                }

    return {
        "category": "Other/Uncertain",
        "confidence": "Low",
        "reason": "No reliable match was found for the supplied description.",
        "detected_item": item_text.strip(),
    }
