"""Placeholder exporter module."""


def export_document(text: str, output_path: str) -> str:
    """Write a placeholder export stub."""
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return output_path
