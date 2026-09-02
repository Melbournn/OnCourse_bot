from pydantic import BaseModel

"""
  - ExtractedPage is the text taken from one PDF page.
  - book_page is the page number printed in the book.
  - pdf_index is the PDF program’s zero-based page position.
  - Passage is a smaller searchable piece of book text.
  - passage_index identifies the passage’s order on a page or within a group.
  - RetrievedPassage is a search result.
  - score tells us how similar that passage is to the question.
"""


class ExtractedPage(BaseModel):
    book_page: int
    pdf_index: int
    text: str


class Passage(BaseModel):
    id: str
    book_id: str
    section_id: str
    route_chunk_id: str
    page_start: int
    page_end: int
    passage_index: int
    text: str


class RetrievedPassage(BaseModel):
    id: str
    score: float
    section_id: str
    route_chunk_id: str
    page_start: int
    page_end: int
    text: str
