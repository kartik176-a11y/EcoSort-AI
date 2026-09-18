from pathlib import Path

from src.classifier import classify_text_item, normalize_text
from src.llm import generate_response
from src.rag import RAGPipeline


UNAVAILABLE_GUIDANCE = (
    "Reliable guidance was not found in the current knowledge base. "
    "Please verify disposal instructions with the local municipal authority."
)


def _classification(item, image_file):
    result = classify_text_item(item)
    if image_file is not None:
        # Uploads are preview-only. Filename hints are deliberately not used as CV classification.
        result["reason"] += " The uploaded image is preview-only; no computer-vision classification was performed."
    return result


def run_waste_workflow(item, image_file=None, rag_pipeline=None):
    if not str(item or "").strip():
        return {
            "detected_item": "Unknown", "category": "Other/Uncertain", "confidence": "Low",
            "reason": "No item description was supplied.", "recommendation": "Enter a waste item or question.",
            "grounded_guidance": UNAVAILABLE_GUIDANCE, "sources": [],
            "retrieved_context": "No retrieval performed because the input was empty.",
            "disclaimer": "Please verify disposal instructions with the local municipal authority.",
            "demo_label": "Local fallback mode",
        }

    classification = _classification(item, image_file)
    pipeline = rag_pipeline or RAGPipeline(Path(__file__).resolve().parent.parent / "data")
    retrieval = pipeline.retrieve(item, top_k=3)
    guidance, mode = generate_response(item, retrieval["context"])

    category = classification["category"]
    if category in {"Hazardous/Special waste", "E-waste"}:
        recommendation = "Do not place it in ordinary household waste. Use an authorized special-waste or e-waste route and verify locally."
        disclaimer = "Special or hazardous waste requires verification with authorized local authorities."
    elif category == "Wet/Biodegradable":
        recommendation = "Keep it separate in the wet/organic stream for composting or municipal collection."
        disclaimer = "This is general guidance; check current municipal instructions."
    elif category == "Dry/Recyclable":
        recommendation = "Keep it separate in the dry/recyclable stream and clean it where practical."
        disclaimer = "This is general guidance; check current municipal instructions."
    else:
        recommendation = "Do not guess; verify the correct route with the local municipal authority."
        disclaimer = "The item is uncertain. Verify disposal instructions before acting."

    return {
        "detected_item": classification["detected_item"], "category": category,
        "confidence": classification["confidence"], "reason": classification["reason"],
        "recommendation": recommendation, "grounded_guidance": guidance,
        "sources": retrieval["sources"], "retrieved_context": retrieval["context"],
        "disclaimer": disclaimer, "demo_label": f"{mode} mode",
    }
