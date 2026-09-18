"""
Tests for image classification module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.image_classifier import (
        is_image_classification_available,
        get_classification_status,
        WASTE_CLASSES,
        CLASS_TO_CATEGORY,
    )
    IMAGE_CLASSIFIER_IMPORTED = True
except ImportError as e:
    IMAGE_CLASSIFIER_IMPORTED = False
    print(f"⚠ Warning: Could not import image_classifier: {e}")


def test_image_classifier_import():
    """Test that image classifier module can be imported."""
    assert IMAGE_CLASSIFIER_IMPORTED, "Failed to import image_classifier module"
    print("✓ Image classifier module imports successfully")


def test_waste_classes_defined():
    """Test that waste classes are properly defined."""
    if not IMAGE_CLASSIFIER_IMPORTED:
        print("⚠ Skipping: image_classifier not imported")
        return
    
    assert len(WASTE_CLASSES) == 6
    assert 'cardboard' in WASTE_CLASSES
    assert 'glass' in WASTE_CLASSES
    assert 'metal' in WASTE_CLASSES
    assert 'paper' in WASTE_CLASSES
    assert 'plastic' in WASTE_CLASSES
    assert 'trash' in WASTE_CLASSES
    
    print("✓ Waste classes properly defined")


def test_class_mapping():
    """Test that classes map to correct EcoSort categories."""
    if not IMAGE_CLASSIFIER_IMPORTED:
        print("⚠ Skipping: image_classifier not imported")
        return
    
    recyclable = ['cardboard', 'glass', 'metal', 'paper', 'plastic']
    for waste_class in recyclable:
        assert CLASS_TO_CATEGORY[waste_class] == 'Dry/Recyclable'
    
    assert CLASS_TO_CATEGORY['trash'] == 'Other/Uncertain'
    
    print("✓ Class to category mapping is correct")


def test_classification_status():
    """Test classification status check."""
    if not IMAGE_CLASSIFIER_IMPORTED:
        print("⚠ Skipping: image_classifier not imported")
        return
    
    status = get_classification_status()
    
    assert 'available' in status
    assert 'reason' in status
    assert isinstance(status['available'], bool)
    
    if status['available']:
        print(f"✓ Image classification is available: {status['reason']}")
    else:
        print(f"ℹ Image classification not available: {status['reason']}")


def test_availability_check():
    """Test availability check function."""
    if not IMAGE_CLASSIFIER_IMPORTED:
        print("⚠ Skipping: image_classifier not imported")
        return
    
    available = is_image_classification_available()
    assert isinstance(available, bool)
    
    if available:
        print("✓ Image classification reports as available")
    else:
        print("ℹ Image classification reports as unavailable (expected if model not trained)")


def run_all_tests():
    """Run all image classifier tests."""
    print("\n=== Running Image Classifier Tests ===\n")
    
    test_image_classifier_import()
    
    if IMAGE_CLASSIFIER_IMPORTED:
        test_waste_classes_defined()
        test_class_mapping()
        test_classification_status()
        test_availability_check()
    
    print("\n=== Image Classifier Tests Complete ===\n")


if __name__ == "__main__":
    run_all_tests()
