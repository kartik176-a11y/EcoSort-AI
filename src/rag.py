from pathlib import Path
import re

try:
    from pypdf import PdfReader
except ImportError:  # Optional PDF support; text files still work without it.
    PdfReader = None


UNAVAILABLE_GUIDANCE = (
    "Reliable guidance was not found in the current knowledge base. "
    "Please verify disposal instructions with the local municipal authority."
)


class RAGPipeline:
    """Small offline retriever over .txt and, when available, .pdf files."""

    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.documents = self._load_documents()
        self.chunks = self._make_chunks()

    def _read_pdf(self, path):
        if PdfReader is None:
            return ""
        try:
            reader = PdfReader(str(path))
            return "\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception:
            return ""

    def _load_documents(self):
        documents = []
        if not self.data_dir.is_dir():
            return documents
        for path in sorted(self.data_dir.rglob("*")):
            if not path.is_file():
                continue
            try:
                if path.suffix.lower() == ".txt":
                    text = path.read_text(encoding="utf-8", errors="ignore")
                elif path.suffix.lower() == ".pdf":
                    text = self._read_pdf(path)
                else:
                    continue
            except OSError:
                continue
            if text and text.strip():
                documents.append({"source": path.relative_to(self.data_dir.parent).as_posix(), "text": text})
        return documents

    def _make_chunks(self):
        chunks = []
        for document in self.documents:
            pieces = re.split(r"\n\s*\n|\n(?=\[)", document["text"])
            for piece in pieces:
                text = re.sub(r"\s+", " ", piece).strip()
                if text:
                    chunks.append({"source": document["source"], "text": text})
        return chunks

    def retrieve(self, query, top_k=3):
        words = set(re.findall(r"[a-z0-9]+", str(query or "").lower()))
        words = {word for word in words if len(word) > 2}
        if not words or not self.chunks:
            return {"context": UNAVAILABLE_GUIDANCE, "sources": []}

        scored = []
        for chunk in self.chunks:
            text = chunk["text"].lower()
            score = sum(text.count(word) for word in words)
            if score:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        selected = [chunk for _, chunk in scored[: max(1, int(top_k))]]
        if not selected:
            return {"context": UNAVAILABLE_GUIDANCE, "sources": []}
        return {
            "context": "\n\n".join(chunk["text"] for chunk in selected),
            "sources": list(dict.fromkeys(chunk["source"] for chunk in selected)),
        }
