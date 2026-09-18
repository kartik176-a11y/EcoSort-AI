from __future__ import annotations

from pathlib import Path


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def safe_read_text(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception:
        return ""
