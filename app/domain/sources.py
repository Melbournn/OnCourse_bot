from typing import Literal

from pydantic import BaseModel


class BookSource(BaseModel):
  type: Literal["book"] = "book"
  book_id: str
  section_id: str
  chunk_id: str
  page_start: int
  page_end: int
  specific_topic: str | None = None


class WebSource(BaseModel):
  type: Literal["web"] = "web"
  title: str
  url: str