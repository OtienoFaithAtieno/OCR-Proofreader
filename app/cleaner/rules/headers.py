"""Header cleanup rules."""


def remove_headers(document):
    """Remove blocks explicitly marked as headers."""
    for page in document.pages:
        page.blocks[:] = [block for block in page.blocks if block.metadata.get("role") != "header"]
    return document
