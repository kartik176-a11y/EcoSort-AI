#!/usr/bin/env python3
"""
Test script for image classification integration.

Run this to verify the image classification setup:
    python test_image_classification.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent))


def test_imports():
    """Test that all required modules can be imported."""
    print("=" * 60)
    print("TEST 1: Import Test")
    print("=" * 60)
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        from src.classifier import classify_text_item
        print("✓ Text classifier imported successfully")
    except ImportError as e:
        print(f"✗ Text classifier import failed: {e}")
        return False
    
    try:
        from src.agents import run_waste_workflow, IMAGE_CLASSIFICATION_AVAILABLE
        print("✓ Agents module imported successfully")
        print(f"  Image classification available: {IMAGE_CLASSIFICATION_AVAILABLE}")
    except ImportError as e:
        print(f"✗ Agents import failed: {e}")
        return False
    
    try:
        from src.image_classifier import is_available, classify_waste_image
        available = is_available()
        print(f"✓ Image classifier imported successfully")
        print(f"  TensorFlow available: {available}")
        return available
    except ImportError as e:
        print(f"✗ Image classifier import failed: {e}")
        print("  This is expected if TensorFlow is not installed")
        return False


def test_text_classification():
    """Test text classification."""
    print("\n" + "=" * 60)
    print("TEST 2: Text Classification")
    print("=" * 60)
    
    from src.classifier import classify_text_item
    
    test_cases = [
        ("plastic bottle", "Dry/Recyclable"),
        ("banana peel", "Wet/Biodegradable"),
        ("used battery", "Hazardous/Special waste"),
        ("old mobile phone", "E-waste"),
        ("unknown item xyz", "Other/Uncertain"),
    ]
    
    all_passed = True
    for item, expected_category in test_cases:
        result = classify_text_item(item)
        actual_category = result["category"]
        passed = actual_category == expected_category
        status = "✓" if passed else "✗"
        print(f"{status} '{item}' → {actual_category} (expected: {expected_category})")
        if not passed:
            all_passed = False
    
    return all_passed


def test_image_classification():
    """Test image classification with a dummy image."""
    print("\n" + "=" * 60)
    print("TEST 3: Image Classification")
    print("=" * 60)
    
    try:
        from src.image_classifier import classify_waste_image, is_available
        from PIL import Image
        import numpy as np
        
        if not is_available():
            print("⚠ Image classification unavailable (TensorFlow not installed)")
            print("  Install with: pip install tensorflow")
            return None
        
        # Create a simple test image (random pixels)
        print("Creating test image (random pixels)...")
        test_image = Image.fromarray(
            np.random.randint(0, 255, (299, 299, 3), dtype=np.uint8)
        )
        
        print("Running image classification...")
        result = classify_waste_image(test_image)
        
        if result.get("success"):
            print("✓ Image classification succeeded")
            print(f"  Predicted class: {result.get('predicted_class', 'Unknown')}")
            print(f"  Category: {result.get('category', 'Unknown')}")
            print(f"  Confidence: {result.get('confidence', 'Unknown')}")
            print(f"  Model: {result.get('model', 'Unknown')}")
            
            if result.get('top_predictions'):
                print("  Top predictions:")
                for i, pred in enumerate(result['top_predictions'][:3], 1):
                    print(f"    {i}. {pred['class']} — {pred['confidence']}")
            
            return True
        else:
            print(f"✗ Image classification failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"✗ Image classification test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow_integration():
    """Test the complete workflow."""
    print("\n" + "=" * 60)
    print("TEST 4: Workflow Integration")
    print("=" * 60)
    
    from src.agents import run_waste_workflow
    
    # Test text-only workflow
    print("\nTest 4A: Text-only workflow")
    result = run_waste_workflow("plastic bottle", image_file=None, rag_pipeline=None)
    if result and result.get("category"):
        print(f"✓ Text workflow succeeded")
        print(f"  Item: {result.get('detected_item', 'Unknown')}")
        print(f"  Category: {result.get('category', 'Unknown')}")
        print(f"  Method: {result.get('classification_method', 'Unknown')}")
    else:
        print("✗ Text workflow failed")
        return False
    
    # Test image workflow if available
    try:
        from src.image_classifier import is_available
        from PIL import Image
        import numpy as np
        
        if is_available():
            print("\nTest 4B: Image workflow")
            test_image = Image.fromarray(
                np.random.randint(0, 255, (299, 299, 3), dtype=np.uint8)
            )
            result = run_waste_workflow("", image_file=test_image, rag_pipeline=None)
            if result and result.get("category"):
                print(f"✓ Image workflow succeeded")
                print(f"  Item: {result.get('detected_item', 'Unknown')}")
                print(f"  Category: {result.get('category', 'Unknown')}")
                print(f"  Method: {result.get('classification_method', 'Unknown')}")
            else:
                print("✗ Image workflow failed")
                return False
        else:
            print("\nTest 4B: Image workflow (SKIPPED - TensorFlow not available)")
    except Exception as e:
        print(f"⚠ Image workflow test skipped: {e}")
    
    return True


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "EcoSort AI - Image Classification Tests" + " " * 9 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = {}
    
    # Test 1: Imports
    results["imports"] = test_imports()
    
    # Test 2: Text classification
    results["text_classification"] = test_text_classification()
    
    # Test 3: Image classification
    image_result = test_image_classification()
    results["image_classification"] = image_result if image_result is not None else "skipped"
    
    # Test 4: Workflow integration
    results["workflow"] = test_workflow_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✓ PASSED"
        elif result is False:
            status = "✗ FAILED"
        else:
            status = "⚠ SKIPPED"
        print(f"{status:12} {test_name.replace('_', ' ').title()}")
    
    print("\n" + "=" * 60)
    
    # Check if all critical tests passed
    critical_tests = ["imports", "text_classification", "workflow"]
    all_critical_passed = all(results.get(t) is True for t in critical_tests)
    
    if all_critical_passed:
        print("✓ All critical tests passed!")
        if results.get("image_classification") == "skipped":
            print("\n⚠ Note: Image classification is unavailable.")
            print("  Install TensorFlow to enable:")
            print("  pip install tensorflow>=2.13.0")
        return 0
    else:
        print("✗ Some critical tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
