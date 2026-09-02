from pydantic import BaseModel, Field

"""
- TopicHint is one indexed topic and its printed book page.
- RouteChunk is a predefined page range containing related topics.
- Section is a large book section containing route chunks.
- RoutingCatalog is the complete parsed routing index.
- RoutingDecision is the router’s final choice for one question.
"""


class TopicHint(BaseModel):
    name: str
    page: int


class RouteChunk(BaseModel):
    id: str
    name: str
    start_page: int
    end_page: int
    route_when: str
    specific_topics: list[TopicHint] = Field(default_factory=list)


class Section(BaseModel):
    id: str
    name: str
    start_page: int
    end_page: int
    chunks: list[RouteChunk] = Field(default_factory=list)


class RoutingCatalog(BaseModel):
    sections: list[Section]

    def section_map(self) -> dict[str, Section]:
        return {section.id: section for section in self.sections}

    def chunk_map(self) -> dict[str, RouteChunk]:
        return {chunk.id: chunk for section in self.sections for chunk in section.chunks}


class RoutingDecision(BaseModel):
    section_id: str
    section_name: str
    chunk_id: str
    chunk_name: str
    chunk_pages: tuple[int, int]

    specific_topic: str | None = None
    specific_topic_page: int | None = None

    confidence: float = Field(ge=0, le=1)
    secondary_chunk_id: str | None = None
    classification_label: str | None = None
