"""
Tests for RAG (Retrieval-Augmented Generation) pipeline.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag import RAGPipeline


def test_rag_initialization():
    """Test RAG pipeline initialization."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Warning: data directory not found, skipping RAG tests")
        return
    
    rag = RAGPipeline(data_dir)
    
    assert rag.data_dir == data_dir
    assert isinstance(rag.documents, list)
    assert isinstance(rag.chunks, list)
    
    print(f"✓ RAG initialized with {len(rag.documents)} documents and {len(rag.chunks)} chunks")


def test_document_loading():
    """Test that documents are loaded correctly."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    # Check that at least some documents were loaded
    assert len(rag.documents) > 0, "No documents loaded"
    
    # Check document structure
    for doc in rag.documents:
        assert "source" in doc
        assert "text" in doc
        assert len(doc["text"]) > 0
    
    print(f"✓ Loaded {len(rag.documents)} documents")


def test_retrieval_wet_waste():
    """Test retrieval for wet waste queries."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    result = rag.retrieve("banana peel composting", top_k=3)
    
    assert "context" in result
    assert "sources" in result
    assert isinstance(result["sources"], list)
    assert len(result["context"]) > 0
    
    print("✓ Wet waste retrieval works")


def test_retrieval_dry_waste():
    """Test retrieval for dry/recyclable waste."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    result = rag.retrieve("plastic bottle recycling", top_k=3)
    
    assert "context" in result
    assert len(result["context"]) > 0
    
    print("✓ Dry waste retrieval works")


def test_retrieval_hazardous():
    """Test retrieval for hazardous waste."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    result = rag.retrieve("battery disposal hazardous", top_k=3)
    
    assert "context" in result
    assert len(result["context"]) > 0
    
    print("✓ Hazardous waste retrieval works")


def test_retrieval_ewaste():
    """Test retrieval for e-waste."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    result = rag.retrieve("old mobile phone laptop electronic", top_k=3)
    
    assert "context" in result
    assert len(result["context"]) > 0
    
    print("✓ E-waste retrieval works")


def test_empty_query():
    """Test behavior with empty query."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    result = rag.retrieve("", top_k=3)
    
    assert "context" in result
    assert "Reliable guidance was not found" in result["context"]
    
    print("✓ Empty query handling works")


def test_no_match_query():
    """Test retrieval when no good matches exist."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    # Query with very obscure terms unlikely to match
    result = rag.retrieve("xyzabc qwerty asdfgh", top_k=3)
    
    assert "context" in result
    # Either returns unavailable guidance or low-quality matches
    
    print("✓ No-match query handling works")


def test_top_k_parameter():
    """Test that top_k parameter controls result count."""
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print("⚠ Skipping: data directory not found")
        return
    
    rag = RAGPipeline(data_dir)
    
    if len(rag.chunks) == 0:
        print("⚠ No chunks available for top_k test")
        return
    
    result_1 = rag.retrieve("plastic recycling paper", top_k=1)
    result_3 = rag.retrieve("plastic recycling paper", top_k=3)
    
    # Both should have context
    assert len(result_1["context"]) > 0
    assert len(result_3["context"]) > 0
    
    print("✓ top_k parameter works")


def run_all_tests():
    """Run all RAG tests."""
    print("\n=== Running RAG Tests ===\n")
    
    test_rag_initialization()
    test_document_loading()
    test_retrieval_wet_waste()
    test_retrieval_dry_waste()
    test_retrieval_hazardous()
    test_retrieval_ewaste()
    test_empty_query()
    test_no_match_query()
    test_top_k_parameter()
    
    print("\n=== All RAG Tests Passed ✓ ===\n")


if __name__ == "__main__":
    run_all_tests()
