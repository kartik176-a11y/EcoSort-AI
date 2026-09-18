"""Backward-compatible Granite module.

The active adapter lives in src.llm. This module intentionally contains no RAG code.
"""

from src.llm import fallback_response, generate_response, llm_is_configured

__all__ = ["fallback_response", "generate_response", "llm_is_configured"]
