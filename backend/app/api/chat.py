"""
채팅 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from app.models.schemas import ChatRequest, ChatResponse
from app.core.mem0_manager import Mem0Manager, get_mem0_manager

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> ChatResponse:
    """
    채팅 메시지 처리 및 메모리 저장

    Args:
        request: 채팅 요청

    Returns:
        채팅 응답 (메모리, 엔티티, 관계 포함)
    """
    try:
        logger.info(f"채팅 요청 - User: {request.user_id}, Message: {request.message[:50]}...")

        # 메모리에 메시지 추가
        add_result = mem0_manager.add_memory(
            data=request.message,
            user_id=request.user_id,
            metadata={
                "session_id": request.session_id,
                "timestamp": "now"
            }
        )

        # 관련 메모리 검색
        related_memories = mem0_manager.search_memory(
            query=request.message,
            user_id=request.user_id,
            limit=5
        )

        # 응답 구성
        response = ChatResponse(
            message=f"메시지를 저장하고 {len(related_memories)}개의 관련 메모리를 찾았습니다.",
            memories=related_memories,
            entities=[],  # Mem0가 자동으로 처리
            relationships=[]  # Mem0가 자동으로 처리
        )

        logger.success(f"채팅 처리 완료 - User: {request.user_id}")
        return response

    except Exception as e:
        logger.error(f"채팅 처리 실패: {e}")
        raise HTTPException(status_code=500, detail=f"채팅 처리 실패: {str(e)}")
