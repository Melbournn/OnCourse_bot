from typing import Literal

from pydantic import BaseModel, Field

from app.domain.routing import RoutingDecision
from app.domain.sources import BookSource, WebSource

"""
SufficiencyResult answers:

Do the retrieved book passages contain enough evidence?

- can_answer=True means the book is sufficient.
- confidence must be between 0 and 1.
- reason_code is a short auditable label, not hidden reasoning.

AnswerResult contains:

- the final answer text;
- whether evidence came from the book, web, or both;
- the routing decision;
- source metadata;
- whether web research was used.

unresolved means the system could not find enough reliable evidence.
"""


class SufficiencyResult(BaseModel):
    can_answer: bool
    confidence: float = Field(ge=0, le=1)
    reason_code: str


class AnswerResult(BaseModel):
    answer: str
    source_type: Literal[
        "book",
        "book+web",
        "web",
        "unresolved",
    ]
    route: RoutingDecision
    sources: list[BookSource | WebSource]
    used_web: bool
