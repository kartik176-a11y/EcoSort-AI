"""Transparent keyword classifier used when no trained model is configured."""
import re

EXAMPLES = ["Plastic water bottle", "Plastic wrapper", "Newspaper", "Cardboard", "Banana peel", "Food waste", "Vegetable waste", "Glass bottle", "Aluminium can", "Steel can", "Old phone", "Laptop", "Charger", "Battery", "Headphones", "Old clothes", "Mixed waste", "Unknown object"]

DETAILS = {
    "Recyclable": ("Follow local dry-recycling rules; empty and clean the item where practical.", "Recycling can reduce raw-material and landfill use.", "Keep accepted recyclables separate."),
    "Organic/Wet Waste": ("Use an appropriate organic-waste or composting stream.", "Composting can divert organics from landfill and return nutrients to soil.", "Prevent food waste, then compost suitable material."),
    "E-Waste": ("Keep electronics out of ordinary bins and use an authorized e-waste route where available.", "Responsible handling can recover materials and reduce pollution risks.", "Repair, reuse, donate, or recycle through an appropriate channel."),
    "Hazardous Waste": ("Do not burn, pour out, open, or mix it. Follow local hazardous-waste guidance.", "Safe handling protects people and the environment from harmful substances.", "Keep it safely contained and seek local guidance."),
    "Glass": ("Separate container glass where accepted and handle broken glass carefully.", "Glass can often be recycled repeatedly.", "Reuse suitable jars or use the correct glass stream."),
    "Metal": ("Empty and rinse containers where practical, then use the appropriate metal stream.", "Metal recycling preserves minerals and energy.", "Reuse containers when safe and recycle accepted metal."),
    "Textile": ("Repair or donate usable textiles; use a textile collection route when available.", "Reuse reduces textile waste and demand for new fibers.", "Repair, share, donate, or repurpose first."),
    "Non-Recyclable/Residual Waste": ("Reduce or reuse it if possible; otherwise use the residual stream according to local guidance.", "Reducing residual waste limits landfill burden.", "Choose durable alternatives and avoid unnecessary single-use items."),
    "Uncertain": ("The item needs more information. Check local guidance before disposal.", "Correct identification reduces contamination.", "Verify with a local waste service before acting."),
}

RULES = [("Hazardous Waste", ["battery", "paint", "pesticide", "solvent", "bleach", "chemical"]), ("E-Waste", ["old phone", "mobile phone", "smartphone", "laptop", "computer", "charger", "cable", "headphone", "electronic"]), ("Organic/Wet Waste", ["banana peel", "food waste", "food leftover", "vegetable", "fruit peel", "compost", "coffee grounds", "leaves"]), ("Glass", ["glass bottle", "glass jar", "broken glass", "glass"]), ("Metal", ["aluminium", "aluminum", "steel can", "tin can", "metal can", "metal"]), ("Textile", ["old clothes", "clothing", "shirt", "jeans", "fabric", "textile", "shoes"]), ("Recyclable", ["plastic bottle", "water bottle", "newspaper", "cardboard", "paper", "magazine"]), ("Non-Recyclable/Residual Waste", ["plastic wrapper", "chips packet", "plastic bag", "sachet", "diaper", "styrofoam", "mixed waste"])]


def _normalise(value):
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def classify_waste(description):
    if not description or not description.strip():
        category, confidence, reason = "Uncertain", "Low", "No description was provided."
    else:
        text = _normalise(description)
        category, confidence, reason = "Uncertain", "Low", "No clear material or item pattern matched the description."
        for candidate, keywords in RULES:
            matches = [word for word in keywords if _normalise(word) in text]
            if matches:
                term = max(matches, key=len)
                category = candidate
                confidence = "High" if " " in term or len(matches) > 1 else "Medium"
                reason = f"The description contains '{term}', which matches the {candidate.lower()} rule."
                break
    guidance, impact, action = DETAILS[category]
    return {"category": category, "confidence": confidence, "reason": reason, "guidance": guidance, "impact": impact, "action": action}
