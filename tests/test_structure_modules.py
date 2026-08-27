from app.cleaner.rules.fonts import normalize_fonts
from app.cleaner.cleaner import clean_document
from app.cleaner.rules.headings import normalize_headings
from app.cleaner.rules.page_breaks import normalize_page_breaks
from app.cleaner.rules.paragraphs import normalize_paragraphs
from app.layout.heading_detector import detect_headings
from app.layout.table_detector import detect_tables
from app.model.document import BlockType, Document, DocumentBlock, Page


def test_requested_model_cleaner_and_layout_modules_work():
    page = Page(number=1, width=600, height=800)
    page.add_block(DocumentBlock(text="Section:", type=BlockType.PARAGRAPH))
    page.add_block(DocumentBlock(text="  Body   text  ", type=BlockType.PARAGRAPH))
    document = Document(pages=[page])

    clean_document(document, (
        normalize_paragraphs,
        normalize_fonts,
        normalize_headings,
        normalize_page_breaks,
    ))
    headings = detect_headings(page)

    assert page.blocks[0].type is BlockType.HEADING
    assert page.blocks[1].text == "Body text"
    assert page.blocks[1].style["font_name"] == "Times New Roman"
    assert len(headings) == 1
    assert detect_tables(page) == []
