"""
애플리케이션 설정 관리
Python 3.13 호환
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from app.prompts.korean_memory_extraction import (
    KOREAN_FACT_RETRIEVAL_PROMPT,
    KOREAN_UPDATE_MEMORY_PROMPT
)


class Settings(BaseSettings):
    """애플리케이션 설정"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Ollama 설정 - 역할별 분리
    ollama_llm_url: str = "http://localhost:11434"  # LLM 전용 서버
    ollama_embedding_url: str = "http://localhost:11435"  # Embedding 전용 서버
    ollama_llm_model: str = "qwen2.5:7b"
    ollama_embedding_model: str = "bge-m3"

    # 레거시 호환성 (ollama_base_url이 설정되면 우선 사용)
    ollama_base_url: str = ""

    # LM Studio / OpenAI 호환 임베딩 설정
    use_openai_embedding: bool = False  # True면 OpenAI 형식 사용
    openai_embedding_url: str = "http://localhost:1234/v1"
    openai_embedding_model: str = "text-embedding-bge-m3"
    openai_api_key: str = "lm-studio"  # LM Studio는 더미 키 필요

    # Neo4j 설정
    neo4j_url: str = "neo4j://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "password"
    neo4j_database: str = "neo4j"

    # Qdrant 설정
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "mem0g_korean"

    # 그래프 스토어 선택
    graph_store_provider: Literal["neo4j", "kuzu"] = "neo4j"

    # Kuzu 설정
    kuzu_db_path: str = "./data/mem0g.kuzu"

    # API 설정
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # 로그 레벨
    log_level: str = "INFO"

    def get_mem0_config(self) -> dict:
        """Mem0 설정 생성"""
        # LLM URL 결정 (레거시 호환성)
        llm_url = self.ollama_base_url if self.ollama_base_url else self.ollama_llm_url

        config = {
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": self.ollama_llm_model,
                    "ollama_base_url": llm_url,
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            },
            "embedder": None,  # 아래에서 조건부로 설정
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "host": self.qdrant_host,
                    "port": self.qdrant_port,
                    "collection_name": self.qdrant_collection,
                    "embedding_model_dims": 1024  # bge-m3 dimension
                }
            },
            "version": "v1.1"
        }

        # 임베딩 설정 (OpenAI 또는 Ollama)
        if self.use_openai_embedding:
            # LM Studio / OpenAI 호환 임베딩
            config["embedder"] = {
                "provider": "openai",
                "config": {
                    "model": self.openai_embedding_model,
                    "api_key": self.openai_api_key,
                    "openai_api_base": self.openai_embedding_url
                }
            }
        else:
            # Ollama 임베딩
            embedding_url = self.ollama_base_url if self.ollama_base_url else self.ollama_embedding_url
            config["embedder"] = {
                "provider": "ollama",
                "config": {
                    "model": self.ollama_embedding_model,
                    "ollama_base_url": embedding_url
                }
            }

        # 그래프 스토어 설정 추가 (mem0ai 1.0.0+)
        if self.graph_store_provider == "neo4j":
            config["graph_store"] = {
                "provider": "neo4j",
                "config": {
                    "url": self.neo4j_url,
                    "username": self.neo4j_username,
                    "password": self.neo4j_password,
                    "database": self.neo4j_database
                }
            }
        elif self.graph_store_provider == "kuzu":
            config["graph_store"] = {
                "provider": "kuzu",
                "config": {
                    "db_path": self.kuzu_db_path
                }
            }

        # 한국어 메모리 추출을 위한 커스텀 프롬프트 추가
        config["custom_fact_extraction_prompt"] = KOREAN_FACT_RETRIEVAL_PROMPT
        config["custom_update_memory_prompt"] = KOREAN_UPDATE_MEMORY_PROMPT

        return config


# 전역 설정 인스턴스
settings = Settings()
