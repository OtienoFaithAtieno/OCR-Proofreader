"""Independent document-cleaning rules."""

from .fonts import normalize_fonts
from .paragraphs import normalize_paragraphs

__all__ = ["normalize_fonts", "normalize_paragraphs"]



""""
a typical should look like this

def remove_extra_spaces(document):
    for page in document.pages:
        for block in page.blocks:
            block.text = " ".join(block.text.split())

    return document

Then add it to the ordered list in cleaner.py

DEFAULT_RULES = (
    normalize_paragraphs,
    remove_extra_spaces,
    normalize_headings,
    normalize_fonts,
    normalize_page_breaks,
)

"""