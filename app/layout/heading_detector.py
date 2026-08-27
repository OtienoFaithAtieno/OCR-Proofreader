"""Heading detection helpers."""

from app.model.document import BlockType


def detect_headings(page):
    """Mark likely headings based on short, standalone text blocks."""
    headings = []
    for block in page.blocks:
        words = block.text.split()
        if 0 < len(words) <= 12 and block.text.strip().endswith((":", "?")):
            block.type = BlockType.HEADING
            headings.append(block)
    return headings
