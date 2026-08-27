"""Heading normalization rules."""

from app.model.document import BlockType


def normalize_headings(document):
    """Ensure heading blocks have a heading style marker."""
    for page in document.pages:
        for block in page.blocks:
            if block.type is BlockType.HEADING:
                block.style.setdefault("name", "Heading 1")
    return document
