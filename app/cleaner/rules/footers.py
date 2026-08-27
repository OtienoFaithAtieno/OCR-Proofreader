"""Footer cleanup rules."""


def remove_footers(document):
    """Remove blocks explicitly marked as footers."""
    for page in document.pages:
        page.blocks[:] = [block for block in page.blocks if block.metadata.get("role") != "footer"]
    return document
