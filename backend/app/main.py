"""
FastAPI 메인 애플리케이션
Python 3.13 호환
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.config import settings
from app.api import chat, memory, graph, test, admin

# 로거 설정
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level
)

# FastAPI 앱 생성
app = FastAPI(
    title="Mem0g Testing Platform API",
    description="그래프 기반 메모리 테스트 플랫폼 (한국어 최적화)",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(chat.router)
app.include_router(memory.router)
app.include_router(graph.router)
app.include_router(test.router)
app.include_router(admin.router)


@app.on_event("startup")
async def startup_event():
    """앱 시작 이벤트"""
    logger.info("=" * 60)
    logger.info("🚀 Mem0g Testing Platform 시작")
    logger.info("=" * 60)
    logger.info(f"LLM 모델: {settings.ollama_llm_model}")
    logger.info(f"임베딩 모델: {settings.ollama_embedding_model}")
    logger.info(f"그래프 DB: {settings.graph_store_provider}")
    logger.info(f"벡터 DB: Qdrant ({settings.qdrant_host}:{settings.qdrant_port})")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료 이벤트"""
    logger.info("👋 Mem0g Testing Platform 종료")


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "name": "Mem0g Testing Platform API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "korean_optimized": True,
        "models": {
            "llm": settings.ollama_llm_model,
            "embedding": settings.ollama_embedding_model,
            "graph_db": settings.graph_store_provider
        }
    }


@app.get("/ping")
async def ping():
    """간단한 핑 엔드포인트"""
    return {"status": "pong"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
