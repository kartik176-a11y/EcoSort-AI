import os
from pathlib import Path

from src.classifier import classify_waste
from src.granite import GraniteAdapter
from src.rag import RAGPipeline


def _safe_sources(sources):
    if not sources:
        return ["No source available in the current demo context."]
    return sources


def run_waste_workflow(item: str, image_file=None, rag_pipeline: RAGPipeline = None):
    if not item or not item.strip():
        return {
            "detected_item": "Unknown",
            "category": "Other/Uncertain",
            "confidence": "Low",
            "reason": "No item description was supplied.",
            "recommendation": "Please enter a waste item or question.",
            "grounded_guidance": "Reliable guidance was not found in the current knowledge base. Please verify disposal instructions with the local municipal authority.",
            "sources": ["Local knowledge base unavailable"],
            "retrieved_context": "No retrieval performed because the input was empty.",
            "disclaimer": "The system should communicate uncertainty rather than confidently guessing.",
            "demo_label": "Demo/reference mode",
        }

    classification = classify_waste(item, image_file)
    rag = rag_pipeline or RAGPipeline(data_dir=Path(__file__).resolve().parent.parent / "data")
    retrieval = rag.retrieve(item, top_k=3)

    adapter = GraniteAdapter()
    advisory = adapter.generate_advisory(
        item=item,
        category=classification["category"],
        reason=classification["reason"],
        context=retrieval["context"],
        demo_mode=True,
    )

    if classification["category"] in ["Hazardous/Special waste", "E-waste"]:
        disclaimer = "This item may require special handling. Do not place it in ordinary household waste. Verify with authorized local authorities or designated collection points."
    elif classification["category"] == "Other/Uncertain":
        disclaimer = "The item is uncertain. Please verify disposal instructions with the local municipal authority."
    else:
        disclaimer = "This guidance is designed to support civic awareness and should be checked against current local municipal instructions."

    recommended_action = advisory["recommendation"]
    source_list = _safe_sources(retrieval.get("sources", []))

    return {
        "detected_item": classification.get("detected_item", item),
        "category": classification["category"],
        "confidence": classification["confidence"],
        "reason": classification["reason"],
        "recommendation": recommended_action,
        "grounded_guidance": advisory["answer"],
        "sources": source_list,
        "retrieved_context": retrieval["context"],
        "disclaimer": disclaimer,
        "demo_label": advisory.get("demo_label", "Demo/reference mode"),
    }
