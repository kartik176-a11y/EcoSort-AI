import re


CATEGORIES = {
    "Wet/Biodegradable": {
        "keywords": [
            "banana peel", "fruit peel", "food waste", "food leftovers", "leftover food",
            "vegetable waste", "vegetable scrap", "organic waste", "wet waste", "compost",
            "garden waste", "food scrap",
        ],
        "reason": "The description matches organic material suitable for a wet-waste or composting stream.",
    },
    "Dry/Recyclable": {
        "keywords": [
            "plastic bottle", "plastic wrapper", "newspaper", "cardboard box", "cardboard",
            "paper", "glass bottle", "metal can", "tin can", "aluminium can", "carton",
        ],
        "reason": "The description matches a dry material commonly separated for recycling.",
    },
    "Hazardous/Special waste": {
        "keywords": [
            "used battery", "battery", "paint", "chemical", "bleach", "solvent", "motor oil",
            "pesticide", "expired medicine", "medication", "spray can",
        ],
        "reason": "The description matches potentially hazardous or special waste that needs separate handling.",
    },
    "E-waste": {
        "keywords": [
            "mobile phone", "cell phone", "smartphone", "old phone", "laptop", "computer",
            "charger", "electronic", "electronics", "cable", "keyboard", "headphones", "mouse",
            "pen drive",
        ],
        "reason": "The description matches an electrical or electronic item that should not enter ordinary waste.",
    },
}


def normalize_text(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def classify_text_item(item_text):
    original = str(item_text or "").strip()
    if not original:
        return {
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": "No item description was supplied.",
            "detected_item": "Unknown",
        }

    text = normalize_text(original)
    matches = []
    for category, definition in CATEGORIES.items():
        for keyword in definition["keywords"]:
            if normalize_text(keyword) in text:
                matches.append((len(normalize_text(keyword)), category, keyword, definition["reason"]))

    if not matches:
        return {
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": "No reliable match was found for the supplied description.",
            "detected_item": original,
        }

    _, category, keyword, reason = max(matches, key=lambda match: match[0])
    return {
        "category": category,
        "confidence": "High" if len(keyword.split()) > 1 else "Medium",
        "reason": reason,
        "detected_item": original,
    }
