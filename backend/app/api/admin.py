"""
관리자 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from datetime import datetime

from app.models.schemas import HealthResponse
from app.core.mem0_manager import Mem0Manager, get_mem0_manager
from app.config import settings

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/health", response_model=HealthResponse)
async def health_check(
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> HealthResponse:
    """
    헬스체크

    Returns:
        시스템 상태
    """
    try:
        services = mem0_manager.health_check()

        status = "healthy" if all(
            v in ["connected", "ok"] for v in services.values()
        ) else "degraded"

        return HealthResponse(
            status=status,
            timestamp=datetime.now(),
            services=services
        )

    except Exception as e:
        logger.error(f"헬스체크 실패: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            services={"error": str(e)}
        )


@router.get("/config")
async def get_config():
    """
    현재 설정 조회

    Returns:
        설정 정보 (민감 정보 제외)
    """
    try:
        config = {
            "ollama_base_url": settings.ollama_base_url,
            "ollama_llm_model": settings.ollama_llm_model,
            "ollama_embedding_model": settings.ollama_embedding_model,
            "graph_store_provider": settings.graph_store_provider,
            "qdrant_host": settings.qdrant_host,
            "qdrant_port": settings.qdrant_port,
            "log_level": settings.log_level
        }

        return config

    except Exception as e:
        logger.error(f"설정 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"설정 조회 실패: {str(e)}")


@router.post("/reset")
async def reset_system(
    confirm: bool = False,
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
):
    """
    시스템 초기화 (개발용)

    Args:
        confirm: 확인 플래그

    Returns:
        초기화 결과
    """
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="시스템 초기화를 위해서는 confirm=true를 전달해야 합니다"
        )

    try:
        logger.warning("시스템 초기화 시작")

        success = mem0_manager.reset()

        if success:
            return {"status": "success", "message": "시스템이 초기화되었습니다"}
        else:
            raise HTTPException(status_code=500, detail="시스템 초기화 실패")

    except Exception as e:
        logger.error(f"시스템 초기화 실패: {e}")
        raise HTTPException(status_code=500, detail=f"시스템 초기화 실패: {str(e)}")
