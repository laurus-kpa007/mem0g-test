"""
채팅 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from loguru import logger
import time

from app.models.schemas import ChatRequest, ChatResponse
from app.core.mem0_manager import Mem0Manager, get_mem0_manager

router = APIRouter(prefix="/api/chat", tags=["chat"])


def save_conversation_to_memory(
    mem0_manager: Mem0Manager,
    conversation: str,
    user_id: str,
    session_id: str | None
):
    """백그라운드에서 메모리 저장"""
    try:
        t_start = time.time()
        logger.info(f"🔄 백그라운드 메모리 저장 시작 - User: {user_id}")

        add_result = mem0_manager.add_memory(
            data=conversation,
            user_id=user_id,
            metadata={
                "session_id": session_id,
                "timestamp": "now",
                "type": "conversation"
            }
        )

        elapsed = time.time() - t_start
        logger.success(f"✅ 백그라운드 메모리 저장 완료 - User: {user_id}, 소요시간: {elapsed:.2f}초")

    except Exception as e:
        logger.error(f"❌ 백그라운드 메모리 저장 실패 - User: {user_id}: {e}")


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
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
        start_time = time.time()
        logger.info(f"채팅 요청 - User: {request.user_id}, Message: {request.message[:50]}...")

        # 1. 관련 메모리 먼저 검색 (컨텍스트로 사용)
        t1 = time.time()
        memories_list = mem0_manager.search_memory(
            query=request.message,
            user_id=request.user_id,
            limit=5
        )
        logger.info(f"⏱️ 메모리 검색 시간: {time.time() - t1:.2f}초")

        # 2. LLM으로 대화형 응답 생성
        t2 = time.time()
        llm_response = mem0_manager.generate_response(
            message=request.message,
            user_id=request.user_id,
            memories=memories_list
        )
        logger.info(f"⏱️ LLM 응답 생성 시간: {time.time() - t2:.2f}초")

        # 3. 메모리 저장을 백그라운드 태스크로 등록
        conversation = f"User: {request.message}\nAssistant: {llm_response}"
        background_tasks.add_task(
            save_conversation_to_memory,
            mem0_manager=mem0_manager,
            conversation=conversation,
            user_id=request.user_id,
            session_id=request.session_id
        )
        logger.info(f"🚀 메모리 저장을 백그라운드로 예약 - User: {request.user_id}")

        # 4. 즉시 응답 반환 (메모리 저장 전)
        response = ChatResponse(
            message=llm_response,  # LLM 응답
            memories=memories_list,  # 기존 메모리 (방금 추가된 메모리는 제외)
            entities=[],  # Mem0가 자동으로 처리
            relationships=[]  # 백그라운드 처리로 인해 즉시 반환 불가
        )

        total_time = time.time() - start_time
        logger.success(f"✅ 채팅 처리 완료 - User: {request.user_id}, 총 소요시간: {total_time:.2f}초")
        return response

    except Exception as e:
        logger.error(f"채팅 처리 실패: {e}")
        raise HTTPException(status_code=500, detail=f"채팅 처리 실패: {str(e)}")
