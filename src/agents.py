from pathlib import Path

from src.classifier import classify_text_item, normalize_text
from src.llm import generate_response
from src.rag import RAGPipeline

# Try to import image classifier
try:
    from src.image_classifier import classify_image, is_image_classification_available
    IMAGE_CLASSIFIER_AVAILABLE = True
except ImportError:
    IMAGE_CLASSIFIER_AVAILABLE = False


UNAVAILABLE_GUIDANCE = (
    "Reliable guidance was not found in the current knowledge base. "
    "Please verify disposal instructions with the local municipal authority."
)


def _classification(item, image_file):
    """
    Classify waste from text input and/or image.
    
    Priority:
    1. If image is uploaded AND image classification is available, use image classifier
    2. Otherwise use text classifier
    3. Clearly state which method was used
    """
    # Try image classification first if available
    if image_file is not None and IMAGE_CLASSIFIER_AVAILABLE:
        if is_image_classification_available():
            # Real image classification
            result = classify_image(image_file)
            if item and str(item).strip():
                # User also provided text; mention both
                result["reason"] += f" User also provided text: '{item}'"
            return result
        else:
            # Image classifier module exists but model not trained
            if item and str(item).strip():
                # Fall back to text classification
                result = classify_text_item(item)
                result["reason"] += " Image uploaded but trained model weights not available; used text classification."
                return result
            else:
                # No text and no trained model
                return {
                    "category": "Other/Uncertain",
                    "confidence": "Low",
                    "reason": "Image uploaded but trained model weights are not available. Provide text description for classification.",
                    "detected_item": "Image upload (no model)",
                }
    
    # Image uploaded but TensorFlow not installed
    if image_file is not None and not IMAGE_CLASSIFIER_AVAILABLE:
        if item and str(item).strip():
            # Fall back to text
            result = classify_text_item(item)
            result["reason"] += " Image uploaded but TensorFlow not installed; used text classification only."
            return result
        else:
            # No text and no TensorFlow
            return {
                "category": "Other/Uncertain",
                "confidence": "Low",
                "reason": "Image uploaded but TensorFlow is not installed. Provide text description for classification.",
                "detected_item": "Image upload (no TensorFlow)",
            }
    
    # No image, use text classification
    result = classify_text_item(item)
    return result


def run_waste_workflow(item, image_file=None, rag_pipeline=None):
    """
    Complete waste analysis workflow.
    
    Steps:
    1. Classification (image or text)
    2. RAG retrieval
    3. LLM generation (IBM Granite or local fallback)
    4. Return comprehensive result
    """
    if not str(item or "").strip() and image_file is None:
        return {
            "detected_item": "Unknown", "category": "Other/Uncertain", "confidence": "Low",
            "reason": "No item description or image was supplied.", 
            "recommendation": "Enter a waste item or upload an image.",
            "grounded_guidance": UNAVAILABLE_GUIDANCE, "sources": [],
            "retrieved_context": "No retrieval performed because the input was empty.",
            "disclaimer": "Please verify disposal instructions with the local municipal authority.",
            "demo_label": "Local fallback mode",
        }

    # Step 1: Classification
    classification = _classification(item, image_file)
    
    # Step 2: RAG Retrieval
    pipeline = rag_pipeline or RAGPipeline(Path(__file__).resolve().parent.parent / "data")
    
    # Use detected item or original text for retrieval
    query_text = classification.get("detected_item", item) or item or "general waste"
    retrieval = pipeline.retrieve(query_text, top_k=3)
    
    # Step 3: LLM Generation
    guidance, mode = generate_response(query_text, retrieval["context"])

    # Step 4: Build recommendation based on category
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
        "detected_item": classification["detected_item"], 
        "category": category,
        "confidence": classification["confidence"], 
        "reason": classification["reason"],
        "recommendation": recommendation, 
        "grounded_guidance": guidance,
        "sources": retrieval["sources"], 
        "retrieved_context": retrieval["context"],
        "disclaimer": disclaimer, 
        "demo_label": f"{mode} mode",
    }
