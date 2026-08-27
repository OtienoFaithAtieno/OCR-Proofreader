"""Paragraph normalization rules."""


def normalize_paragraphs(document):
    """Trim whitespace and remove empty blocks."""
    for page in document.pages:
        for block in page.blocks:
            block.text = " ".join(block.text.split())
        page.blocks[:] = [block for block in page.blocks if block.text]
    return document
