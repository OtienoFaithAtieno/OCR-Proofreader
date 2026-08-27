"""Document cleaning pipeline and rules."""

from .cleaner import DEFAULT_RULES, clean_document, clean_text
from .rules.fonts import normalize_fonts
from .rules.paragraphs import normalize_paragraphs

__all__ = [
	"DEFAULT_RULES",
	"clean_document",
	"clean_text",
	"normalize_fonts",
	"normalize_paragraphs",
]
