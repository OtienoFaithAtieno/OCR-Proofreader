"""File-related helper utilities."""

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not already exist."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
