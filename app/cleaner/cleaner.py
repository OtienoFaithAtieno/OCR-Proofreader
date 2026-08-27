"""Document cleaning pipeline."""

from collections.abc import Callable, Iterable

from app.cleaner.rules.fonts import normalize_fonts
from app.cleaner.rules.headings import normalize_headings
from app.cleaner.rules.page_breaks import normalize_page_breaks
from app.cleaner.rules.paragraphs import normalize_paragraphs


DocumentRule = Callable[[object], object]

# Add the remaining rules here in their required execution order.
DEFAULT_RULES: tuple[DocumentRule, ...] = (
    normalize_paragraphs,
    normalize_headings,
    normalize_fonts,
    normalize_page_breaks,
)


def clean_text(text: str) -> str:
    """Normalize a standalone text value."""
    return text.strip()


def clean_document(
    document,
    rules: Iterable[DocumentRule] = DEFAULT_RULES,
):
    """Apply document rules in order and return the updated model."""
    for rule in rules:
        document = rule(document)
    return document
