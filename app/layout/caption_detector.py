"""Caption detection helpers."""


def detect_captions(page):
    """Return blocks explicitly marked as captions."""
    return [block for block in page.blocks if block.metadata.get("role") == "caption"]
