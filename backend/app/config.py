"""
애플리케이션 설정 관리
Python 3.13 호환
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """애플리케이션 설정"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Ollama 설정
    ollama_base_url: str = "http://localhost:11434"
    ollama_llm_model: str = "qwen2.5:7b"
    ollama_embedding_model: str = "bge-m3"

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
        config = {
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": self.ollama_llm_model,
                    "base_url": self.ollama_base_url,
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "num_ctx": 8192
                }
            },
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": self.ollama_embedding_model
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "host": self.qdrant_host,
                    "port": self.qdrant_port,
                    "collection_name": self.qdrant_collection
                }
            },
            "version": "v1.1"
        }

        # 그래프 스토어 설정 추가
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

        return config


# 전역 설정 인스턴스
settings = Settings()
