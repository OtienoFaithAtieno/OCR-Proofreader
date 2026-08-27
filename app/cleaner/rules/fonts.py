"""Font normalization rules."""


def normalize_fonts(document, font_name: str = "Times New Roman", font_size: float = 12.0):
    """Apply a consistent font to every document block."""
    for page in document.pages:
        for block in page.blocks:
            block.style["font_name"] = font_name
            block.style["font_size"] = str(font_size)
    return document
