"""Independent document-cleaning rules."""

from .fonts import normalize_fonts
from .paragraphs import normalize_paragraphs
from .validations import normalize_output_rules, validate_output_document

__all__ = [
    "normalize_fonts",
    "normalize_output_rules",
    "normalize_paragraphs",
    "validate_output_document",
]