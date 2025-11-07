"""
테스트 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from app.models.schemas import EntityExtractionRequest, EntityExtractionResponse
from app.core.mem0_manager import Mem0Manager, get_mem0_manager

router = APIRouter(prefix="/api/test", tags=["test"])


@router.post("/entity-extraction", response_model=EntityExtractionResponse)
async def test_entity_extraction(
    request: EntityExtractionRequest,
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> EntityExtractionResponse:
    """
    엔티티 추출 테스트

    Args:
        request: 테스트 요청

    Returns:
        추출된 엔티티 및 관계
    """
    try:
        logger.info(f"엔티티 추출 테스트 - Text: {request.text[:50]}...")

        # 임시 사용자 ID로 메모리 추가
        test_user_id = "test_entity_extraction"
        result = mem0_manager.add_memory(
            data=request.text,
            user_id=test_user_id
        )

        # 결과 파싱
        entities = []
        relationships = []

        # Mem0 결과에서 정보 추출
        if 'results' in result:
            for item in result['results']:
                if 'entities' in item:
                    entities.extend(item['entities'])
                if 'relationships' in item:
                    relationships.extend(item['relationships'])

        # 테스트 메모리 정리
        try:
            mem0_manager.delete_all_memories(test_user_id)
        except:
            pass

        logger.success(f"엔티티 추출 완료: {len(entities)}개 엔티티, {len(relationships)}개 관계")

        return EntityExtractionResponse(
            entities=entities,
            relationships=relationships
        )

    except Exception as e:
        logger.error(f"엔티티 추출 실패: {e}")
        raise HTTPException(status_code=500, detail=f"엔티티 추출 실패: {str(e)}")


@router.get("/benchmark")
async def run_benchmark(
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
):
    """
    성능 벤치마크 실행

    Returns:
        벤치마크 결과
    """
    try:
        logger.info("벤치마크 시작")

        import time

        # 메모리 추가 벤치마크
        start = time.time()
        test_user_id = "test_benchmark"
        mem0_manager.add_memory(
            data="이것은 벤치마크 테스트입니다.",
            user_id=test_user_id
        )
        add_time = time.time() - start

        # 메모리 검색 벤치마크
        start = time.time()
        mem0_manager.search_memory(
            query="벤치마크",
            user_id=test_user_id,
            limit=10
        )
        search_time = time.time() - start

        # 정리
        try:
            mem0_manager.delete_all_memories(test_user_id)
        except:
            pass

        results = {
            "add_memory_ms": round(add_time * 1000, 2),
            "search_memory_ms": round(search_time * 1000, 2),
            "status": "completed"
        }

        logger.success(f"벤치마크 완료: {results}")
        return results

    except Exception as e:
        logger.error(f"벤치마크 실패: {e}")
        raise HTTPException(status_code=500, detail=f"벤치마크 실패: {str(e)}")
