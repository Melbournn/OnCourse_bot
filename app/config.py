from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      extra="ignore",
  )

  telegram_bot_token: str = ""

  openai_api_key: str = ""
  router_model: str = "gpt-5.6-luna"
  sufficiency_model: str = "gpt-5.6-luna"
  answer_model: str = "gpt-5.6-terra"
  embedding_model: str = "text-embedding-3-small"

  book_id: str = "islam_gylymhaly_2015"
  book_pdf_path: str = "data/Ислам-ғылымхалы-жасыл-кітап.pdf"
  router_index_path: str = "data/islam_gylymhaly_llm_router_index.txt"
  book_page_offset: int = 0

  passage_max_tokens: int = 600
  passage_overlap_tokens: int = 100

  rag_top_k: int = 5
  rag_secondary_top_k: int = 8
  router_high_confidence: float = 0.80
  router_medium_confidence: float = 0.55
  allow_whole_book_fallback: bool = False

  qdrant_url: str = "http://localhost:6333"
  qdrant_api_key: str | None = None
  qdrant_collection: str = "islam_gylymhaly"

  mcp_server_url: str = "http://localhost:8100/mcp"

  brave_search_api_key: str = ""
  brave_search_count: int = 5
  web_search_scope_suffix: str = "Hanafi fiqh"

  web_fetch_timeout_seconds: float = 15.0
  web_fetch_max_bytes: int = 2_000_000

  log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
  return Settings()