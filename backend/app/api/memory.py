"""
메모리 관리 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from loguru import logger
from typing import List, Dict, Any

from app.models.schemas import MemorySearchRequest, MemorySearchResponse
from app.core.mem0_manager import Mem0Manager, get_mem0_manager

router = APIRouter(prefix="/api/memories", tags=["memory"])


@router.post("/search", response_model=MemorySearchResponse)
async def search_memories(
    request: MemorySearchRequest,
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> MemorySearchResponse:
    """
    메모리 검색

    Args:
        request: 검색 요청

    Returns:
        검색 결과
    """
    try:
        logger.info(f"메모리 검색 - User: {request.user_id}, Query: {request.query}")

        results = mem0_manager.search_memory(
            query=request.query,
            user_id=request.user_id,
            limit=request.limit
        )

        return MemorySearchResponse(
            results=results,
            count=len(results)
        )

    except Exception as e:
        logger.error(f"메모리 검색 실패: {e}")
        raise HTTPException(status_code=500, detail=f"메모리 검색 실패: {str(e)}")


@router.get("", response_model=List[Dict[str, Any]])
async def get_memories(
    user_id: str = Query(..., description="사용자 ID"),
    limit: int = Query(100, ge=1, le=1000, description="결과 개수"),
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> List[Dict[str, Any]]:
    """
    사용자의 모든 메모리 조회

    Args:
        user_id: 사용자 ID
        limit: 결과 개수

    Returns:
        메모리 리스트
    """
    try:
        logger.info(f"메모리 조회 - User: {user_id}")

        memories = mem0_manager.get_all_memories(
            user_id=user_id,
            limit=limit
        )

        return memories

    except Exception as e:
        logger.error(f"메모리 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"메모리 조회 실패: {str(e)}")


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: str,
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> Dict[str, str]:
    """
    메모리 삭제

    Args:
        memory_id: 메모리 ID

    Returns:
        삭제 결과
    """
    try:
        logger.info(f"메모리 삭제 - ID: {memory_id}")

        success = mem0_manager.delete_memory(memory_id)

        if success:
            return {"status": "success", "message": f"메모리 {memory_id} 삭제 완료"}
        else:
            raise HTTPException(status_code=404, detail="메모리를 찾을 수 없습니다")

    except Exception as e:
        logger.error(f"메모리 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=f"메모리 삭제 실패: {str(e)}")


@router.delete("")
async def delete_all_memories(
    user_id: str = Query(..., description="사용자 ID"),
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> Dict[str, str]:
    """
    사용자의 모든 메모리 삭제

    Args:
        user_id: 사용자 ID

    Returns:
        삭제 결과
    """
    try:
        logger.warning(f"모든 메모리 삭제 - User: {user_id}")

        success = mem0_manager.delete_all_memories(user_id)

        if success:
            return {"status": "success", "message": f"사용자 {user_id}의 모든 메모리 삭제 완료"}
        else:
            raise HTTPException(status_code=500, detail="메모리 삭제 실패")

    except Exception as e:
        logger.error(f"메모리 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=f"메모리 삭제 실패: {str(e)}")
