from app.cleaner.cleaner import clean_document
from app.cleaner.rules.validations import validate_output_document
from app.model.document import Document, DocumentBlock, Page


def test_output_validation_rules_normalize_document_defaults():
    page = Page(number=1, width=612, height=792)
    page.add_block(
        DocumentBlock(
            text="One  two\tthree—four\fFive",
            style={"font_name": "Arial", "font_size": "9"},
        )
    )
    document = Document(pages=[page])

    clean_document(document)

    block = page.blocks[0]
    assert block.text == "One two three--four\n\nFive"
    assert block.style == {
        "font_name": "Times New Roman",
        "font_size": "12.0",
        "text_color": "000000",
        "background_color": "FFFFFF",
    }
    assert document.properties["background_color"] == "FFFFFF"
    assert validate_output_document(document)