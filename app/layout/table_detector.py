"""Table detection helpers."""


def detect_tables(page):
    """Return existing table objects detected for a page."""
    return list(page.tables)
