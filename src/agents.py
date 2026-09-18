from pathlib import Path

from src.classifier import classify_text_item, normalize_text
from src.llm import generate_response
from src.rag import RAGPipeline

# Lazy import for image classifier to avoid TensorFlow overhead when not needed
try:
    from src.image_classifier import classify_waste_image, is_available as image_classifier_available
    IMAGE_CLASSIFICATION_AVAILABLE = image_classifier_available()
except ImportError:
    IMAGE_CLASSIFICATION_AVAILABLE = False
    classify_waste_image = None


UNAVAILABLE_GUIDANCE = (
    "Reliable guidance was not found in the current knowledge base. "
    "Please verify disposal instructions with the local municipal authority."
)


def _classification(item, image_file):
    """
    Classify waste using text and optionally image classification.
    
    Priority:
    1. If image is provided and image classifier is available, use image classification
    2. If text is provided, use text classification
    3. Combine both if both are available
    """
    text_result = classify_text_item(item) if str(item or "").strip() else None
    image_result = None
    
    # Try image classification if available
    if image_file is not None and IMAGE_CLASSIFICATION_AVAILABLE:
        try:
            image_result = classify_waste_image(image_file)
        except Exception as e:
            # If image classification fails, fall back to text
            image_result = {
                'success': False,
                'error': str(e),
                'category': 'Other/Uncertain'
            }
    
    # Decide which classification to use
    if image_result and image_result.get('success'):
        # Use image classification result
        result = {
            "detected_item": image_result['predicted_class'],
            "category": image_result['category'],
            "confidence": image_result['confidence'],
            "reason": f"Image classification: {image_result['explanation']}",
            "classification_method": "image",
            "image_details": {
                "top_predictions": image_result.get('top_predictions', []),
                "model": image_result.get('model', 'Unknown')
            }
        }
        
        # If text classification also suggests a specific category, mention it
        if text_result and text_result['category'] != 'Other/Uncertain':
            if text_result['category'] == image_result['category']:
                result["reason"] += f" Text classification confirms: {text_result['category']}."
            else:
                result["reason"] += f" Note: Text classification suggests {text_result['category']}, but image classification is more specific."
        
        return result
    
    elif image_file is not None and not IMAGE_CLASSIFICATION_AVAILABLE:
        # Image provided but classifier not available
        if text_result:
            text_result["reason"] += " The uploaded image is preview-only; image classification requires TensorFlow (install with: pip install tensorflow)."
        return text_result or {
            "detected_item": "Unknown",
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": "Image classification is not available. Install TensorFlow to enable image classification.",
            "classification_method": "none"
        }
    
    elif image_file is not None and image_result and not image_result.get('success'):
        # Image classification failed
        if text_result:
            text_result["reason"] += f" Image classification failed: {image_result.get('error', 'Unknown error')}."
        return text_result or {
            "detected_item": "Unknown",
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": f"Image classification failed: {image_result.get('error', 'Unknown error')}.",
            "classification_method": "none"
        }
    
    else:
        # Text-only classification
        return text_result or {
            "detected_item": "Unknown",
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": "No item description was supplied.",
            "classification_method": "none"
        }


def run_waste_workflow(item, image_file=None, rag_pipeline=None):
    if not str(item or "").strip() and image_file is None:
        return {
            "detected_item": "Unknown", "category": "Other/Uncertain", "confidence": "Low",
            "reason": "No item description or image was supplied.", "recommendation": "Enter a waste item or upload an image.",
            "grounded_guidance": UNAVAILABLE_GUIDANCE, "sources": [],
            "retrieved_context": "No retrieval performed because the input was empty.",
            "disclaimer": "Please verify disposal instructions with the local municipal authority.",
            "demo_label": "Local fallback mode",
            "classification_method": "none"
        }

    classification = _classification(item, image_file)
    
    # Use detected item for RAG retrieval
    retrieval_query = classification.get("detected_item", item) or item
    pipeline = rag_pipeline or RAGPipeline(Path(__file__).resolve().parent.parent / "data")
    retrieval = pipeline.retrieve(retrieval_query, top_k=3)
    guidance, mode = generate_response(retrieval_query, retrieval["context"])

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

    result = {
        "detected_item": classification["detected_item"], "category": category,
        "confidence": classification["confidence"], "reason": classification["reason"],
        "recommendation": recommendation, "grounded_guidance": guidance,
        "sources": retrieval["sources"], "retrieved_context": retrieval["context"],
        "disclaimer": disclaimer, "demo_label": f"{mode} mode",
        "classification_method": classification.get("classification_method", "text")
    }
    
    # Add image details if available
    if "image_details" in classification:
        result["image_details"] = classification["image_details"]
    
    return result
