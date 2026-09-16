"""Simple lexical retrieval over the local sustainability knowledge base."""
from pathlib import Path
import re

KNOWLEDGE_PATH = Path(__file__).resolve().parent.parent / "data" / "waste_knowledge.txt"


def load_knowledge():
    return KNOWLEDGE_PATH.read_text(encoding="utf-8").strip() if KNOWLEDGE_PATH.exists() else ""


def split_knowledge(text):
    return [part.strip() for part in re.split(r"\n(?=\[.+\])", text) if part.strip()]


def retrieve(query, knowledge, limit=3):
    if not knowledge:
        return "No local knowledge is available."
    words = {word for word in re.findall(r"[a-z]+", query.lower()) if len(word) > 2}
    sections = split_knowledge(knowledge)
    ranked = sorted(sections, key=lambda section: sum(word in section.lower() for word in words), reverse=True)
    selected = [section for section in ranked if any(word in section.lower() for word in words)][:limit]
    return "\n\n".join(selected or sections[:limit])
