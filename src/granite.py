from __future__ import annotations

import os
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


class RAGPipeline:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.documents = self._load_documents()
        self.chunks = self._chunk_documents()

    def _extract_pdf_text(self, file_path: Path) -> str:
        if PdfReader is None:
            return ""
        try:
            reader = PdfReader(str(file_path))
            pages = []
            for page in reader.pages:
                text = page.extract_text() or ""
                pages.append(text)
            return "\n".join(pages)
        except Exception:
            return ""

    def _load_documents(self):
        docs = []
        if not self.data_dir.exists():
            return docs

        for path in sorted(self.data_dir.rglob('*')):
            if path.is_dir():
                continue
            if path.suffix.lower() in {".txt"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                docs.append({"source": str(path.relative_to(self.data_dir.parent)), "text": text})
            elif path.suffix.lower() == ".pdf":
                text = self._extract_pdf_text(path)
                if text.strip():
                    docs.append({"source": str(path.relative_to(self.data_dir.parent)), "text": text})

        if not docs:
            fallback_text = """
            [GVMC municipal guidance]
            Waste segregation at home should separate wet waste, dry waste, and special waste streams. Organic waste such as banana peels and food leftovers should be segregated for composting or wet-waste collection.

            [Swachh Bharat Mission guidance]
            Recyclable dry waste such as plastic bottles, newspapers, cardboard, and paper should be kept separate from wet waste. Hazardous products such as used batteries and electronic devices should be handled through special collection systems.

            [Waste management reference]
            E-waste, batteries, paints, solvents, and chemical waste should not be placed in ordinary household waste. Local authorities or authorized collection points should be consulted for special handling.
            """
            docs.append({"source": "data/official_guidance.txt", "text": fallback_text})

        return docs

    def _chunk_documents(self):
        chunks = []
        for doc in self.documents:
            text = doc.get("text", "")
            pieces = re.split(r"\n\s*\n|\n(?=\[)", text)
            for piece in pieces:
                cleaned = re.sub(r"\s+", " ", piece).strip()
                if cleaned:
                    chunks.append({"source": doc["source"], "text": cleaned})
        return chunks

    def retrieve(self, query: str, top_k: int = 3):
        q = re.sub(r"[^a-z0-9\s]", " ", (query or "").lower())
        q_words = {w for w in q.split() if len(w) > 2}

        if not q_words:
            context = "Reliable guidance was not found in the current knowledge base. Please verify disposal instructions with the local municipal authority."
            return {"context": context, "sources": ["No relevant retrieval"]}

        scored = []
        for chunk in self.chunks:
            chunk_text = chunk["text"].lower()
            score = 0
            for word in q_words:
                if word in chunk_text:
                    score += chunk_text.count(word)
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = scored[:top_k]

        if not selected:
            context = "Reliable guidance was not found in the current knowledge base. Please verify disposal instructions with the local municipal authority."
            return {"context": context, "sources": ["No relevant local guidance found"]}

        context_chunks = [item[1]["text"] for item in selected]
        sources = [item[1]["source"] for item in selected]
        context = "\n\n".join(context_chunks)
        return {"context": context, "sources": sources}

