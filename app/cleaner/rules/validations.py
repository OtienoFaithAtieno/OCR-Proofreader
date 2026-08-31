"""Output validation and normalization rules for the editable DOCX."""

from __future__ import annotations

import re

from app.model.document import BlockType

DEFAULT_FONT_NAME = "Times New Roman"
DEFAULT_FONT_SIZE = 12.0
DEFAULT_TEXT_COLOR = "000000"
DEFAULT_BACKGROUND_COLOR = "FFFFFF"
DEFAULT_PARAGRAPH_STYLE = "Normal"
FIELD_PROTECTION_SHORTCUT = "Ctrl+Shift+F9"


def normalize_output_rules(document):
    """Apply the default rules that govern the final DOCX output.

    Rules applied:
    - Use Times New Roman, size 12, black text, and a white background.
    - Replace tab characters with normal spaces.
    - Replace form-feed page breaks with two blank text entries.
    - Collapse repeated spaces to one space.
    - Replace dot-space-dot sequences with double dots.
    - Replace em dashes with two hyphens.
    - Keep the document in a typical Word Normal paragraph style.
    """
    document.properties["background_color"] = DEFAULT_BACKGROUND_COLOR
    document.properties["style"] = DEFAULT_PARAGRAPH_STYLE
    document.properties["page_number_protection"] = FIELD_PROTECTION_SHORTCUT

    for page in document.pages:
        for block in page.blocks:
            block.text = _normalize_text(block.text)
            block.style.update(
                {
                    "font_name": DEFAULT_FONT_NAME,
                    "font_size": str(DEFAULT_FONT_SIZE),
                    "text_color": DEFAULT_TEXT_COLOR,
                    "background_color": DEFAULT_BACKGROUND_COLOR,
                    "style": DEFAULT_PARAGRAPH_STYLE,
                }
            )

    return document


def _normalize_text(text: str) -> str:
    """Normalize text without removing intentional line boundaries."""
    text = text.replace("\t", " ")
    text = text.replace("\u2014", "--")
    text = text.replace("\f", "\n\n")
    text = re.sub(r"\.\s+\.", "..", text)
    text = re.sub(r" {2,}", " ", text)
    return text


def validate_output_document(document) -> bool:
    """Return whether every output block has the required defaults."""
    return all(
        block.style.get("font_name") == DEFAULT_FONT_NAME
        and block.style.get("font_size") == str(DEFAULT_FONT_SIZE)
        and block.style.get("text_color") == DEFAULT_TEXT_COLOR
        and block.style.get("background_color") == DEFAULT_BACKGROUND_COLOR
        and block.style.get("style") == DEFAULT_PARAGRAPH_STYLE
        for page in document.pages
        for block in page.blocks
    )
