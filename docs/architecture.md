# SustainAI architecture

User input is processed by the transparent classifier or the chat retrieval flow. The retrieval module splits the local text knowledge base into sections, scores sections by matching query words, and returns the most relevant context. That context is passed to the optional LLM adapter. Without credentials, a clearly labelled local RAG fallback displays the retrieved knowledge.

This is a beginner-friendly lexical RAG implementation; it does not use embeddings. Local waste rules should always be checked.
