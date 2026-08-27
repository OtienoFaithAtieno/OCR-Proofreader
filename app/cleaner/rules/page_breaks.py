"""Page-break normalization rules."""


def normalize_page_breaks(document):
    """Record explicit page boundaries for downstream exporters."""
    for page in document.pages:
        page.metadata["page_break_before"] = "true" if page.number > 1 else "false"
    return document
