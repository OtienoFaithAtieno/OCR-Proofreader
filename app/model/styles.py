"""Formatting definitions used by document blocks and DOCX export."""

from dataclasses import dataclass


@dataclass(slots=True)
class TextStyle:
    """Editable formatting attached to a paragraph or heading."""

    name: str = "Normal"
    font_name: str = "Calibri"
    font_size: float = 11.0
    bold: bool = False
    italic: bool = False
    alignment: str = "left"


NORMAL_STYLE = TextStyle()
HEADING_STYLE = TextStyle(name="Heading 1", font_size=16.0, bold=True)
