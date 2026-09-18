#!/usr/bin/env python3
"""
Run all EcoSort AI tests.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import test modules
from tests import test_classifier, test_rag, test_image_classifier


def main():
    """Run all test suites."""
    print("\n" + "="*60)
    print("EcoSort AI - Test Suite")
    print("="*60)
    
    all_passed = True
    
    try:
        test_classifier.run_all_tests()
    except Exception as e:
        print(f"\n✗ Classifier tests failed: {e}\n")
        all_passed = False
    
    try:
        test_rag.run_all_tests()
    except Exception as e:
        print(f"\n✗ RAG tests failed: {e}\n")
        all_passed = False
    
    try:
        test_image_classifier.run_all_tests()
    except Exception as e:
        print(f"\n✗ Image classifier tests failed: {e}\n")
        all_passed = False
    
    print("="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*60 + "\n")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("="*60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
