import pytest
from pydantic import ValidationError

from app.domain.answers import AnswerResult, SufficiencyResult
from app.domain.routing import (
    RouteChunk,
    RoutingCatalog,
    RoutingDecision,
    Section,
    TopicHint,
)
from app.domain.sources import BookSource

"""
- Catalog lookup maps return the correct objects.
- Different chunks do not share the same topic list.
- Invalid confidence values are rejected.
- Book-source metadata survives inside a final answer.
"""


def _make_route(confidence: float = 0.95) -> RoutingDecision:
    return RoutingDecision(
        section_id="TAZALYQ",
        section_name="Тазалық",
        chunk_id="TAZALYQ_04",
        chunk_name="Дәрет",
        chunk_pages=(55, 90),
        specific_topic="Ұйқы және дәрет",
        specific_topic_page=83,
        confidence=confidence,
        classification_label="exact_topic_match",
    )


def test_catalog_creates_section_and_chunk_maps() -> None:
    topic = TopicHint(name="Ұйқы және дәрет", page=83)
    chunk = RouteChunk(
        id="TAZALYQ_04",
        name="Дәрет",
        start_page=55,
        end_page=90,
        route_when="Ablution question",
        specific_topics=[topic],
    )
    section = Section(
        id="TAZALYQ",
        name="Тазалық",
        start_page=29,
        end_page=126,
        chunks=[chunk],
    )
    catalog = RoutingCatalog(sections=[section])

    assert catalog.section_map()["TAZALYQ"].name == "Тазалық"
    assert catalog.chunk_map()["TAZALYQ_04"].specific_topics == [topic]


def test_route_chunk_lists_are_not_shared() -> None:
    first = RouteChunk(
        id="FIRST",
        name="First",
        start_page=1,
        end_page=10,
        route_when="First topic",
    )
    second = RouteChunk(
        id="SECOND",
        name="Second",
        start_page=11,
        end_page=20,
        route_when="Second topic",
    )

    first.specific_topics.append(TopicHint(name="Example", page=5))

    assert second.specific_topics == []


def test_confidence_rejects_values_outside_zero_and_one() -> None:
    with pytest.raises(ValidationError):
        _make_route(confidence=1.01)

    with pytest.raises(ValidationError):
        SufficiencyResult(
            can_answer=False,
            confidence=-0.01,
            reason_code="insufficient_evidence",
        )


def test_book_only_answer_preserves_source_information() -> None:
    source = BookSource(
        book_id="islam_gylymhaly_2015",
        section_id="TAZALYQ",
        chunk_id="TAZALYQ_04",
        page_start=83,
        page_end=83,
    )
    result = AnswerResult(
        answer="Sample answer",
        source_type="book",
        route=_make_route(),
        sources=[source],
        used_web=False,
    )

    assert result.source_type == "book"
    assert result.used_web is False
    assert result.sources[0].type == "book"
