"""
Tests for text-based waste classification.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.classifier import classify_text_item, normalize_text


def test_normalize_text():
    """Test text normalization."""
    assert normalize_text("Banana Peel") == "banana peel"
    assert normalize_text("plastic-bottle!!!") == "plastic bottle"
    assert normalize_text("  multiple   spaces  ") == "multiple spaces"
    print("✓ Text normalization works")


def test_wet_waste_classification():
    """Test wet/biodegradable waste classification."""
    test_cases = [
        "banana peel",
        "food leftovers",
        "vegetable scraps",
        "fruit peel",
        "organic waste",
    ]
    
    for item in test_cases:
        result = classify_text_item(item)
        assert result["category"] == "Wet/Biodegradable", f"Failed for: {item}"
        assert result["confidence"] in ["High", "Medium", "Low"]
        assert result["detected_item"] == item
    
    print("✓ Wet waste classification works")


def test_dry_recyclable_classification():
    """Test dry/recyclable waste classification."""
    test_cases = [
        "plastic bottle",
        "newspaper",
        "cardboard box",
        "glass bottle",
        "metal can",
        "aluminium can",
    ]
    
    for item in test_cases:
        result = classify_text_item(item)
        assert result["category"] == "Dry/Recyclable", f"Failed for: {item}"
        assert result["confidence"] in ["High", "Medium", "Low"]
    
    print("✓ Dry recyclable classification works")


def test_hazardous_waste_classification():
    """Test hazardous/special waste classification."""
    test_cases = [
        "used battery",
        "paint can",
        "expired medicine",
        "chemical cleaner",
        "pesticide",
    ]
    
    for item in test_cases:
        result = classify_text_item(item)
        assert result["category"] == "Hazardous/Special waste", f"Failed for: {item}"
    
    print("✓ Hazardous waste classification works")


def test_ewaste_classification():
    """Test e-waste classification."""
    test_cases = [
        "old mobile phone",
        "laptop",
        "charger",
        "smartphone",
        "keyboard",
        "headphones",
    ]
    
    for item in test_cases:
        result = classify_text_item(item)
        assert result["category"] == "E-waste", f"Failed for: {item}"
    
    print("✓ E-waste classification works")


def test_uncertain_classification():
    """Test uncertain/unknown items."""
    test_cases = [
        "",
        "unknown object",
        "mystery item",
        "xyzabc",
    ]
    
    for item in test_cases:
        result = classify_text_item(item)
        assert result["category"] == "Other/Uncertain", f"Failed for: {item}"
        assert result["confidence"] == "Low"
    
    print("✓ Uncertain classification works")


def test_empty_input():
    """Test empty input handling."""
    result = classify_text_item("")
    assert result["category"] == "Other/Uncertain"
    assert result["confidence"] == "Low"
    assert "No item description" in result["reason"]
    
    result = classify_text_item(None)
    assert result["category"] == "Other/Uncertain"
    
    print("✓ Empty input handling works")


def test_case_insensitivity():
    """Test that classification is case-insensitive."""
    items = ["BANANA PEEL", "Banana Peel", "banana peel", "BaNaNa PeEl"]
    
    categories = [classify_text_item(item)["category"] for item in items]
    assert all(cat == "Wet/Biodegradable" for cat in categories)
    
    print("✓ Case insensitivity works")


def run_all_tests():
    """Run all classifier tests."""
    print("\n=== Running Classifier Tests ===\n")
    
    test_normalize_text()
    test_wet_waste_classification()
    test_dry_recyclable_classification()
    test_hazardous_waste_classification()
    test_ewaste_classification()
    test_uncertain_classification()
    test_empty_input()
    test_case_insensitivity()
    
    print("\n=== All Classifier Tests Passed ✓ ===\n")


if __name__ == "__main__":
    run_all_tests()
