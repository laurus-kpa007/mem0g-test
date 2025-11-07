"""
그래프 관련 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from loguru import logger

from app.models.schemas import GraphVisualizationResponse, GraphStatsResponse, GraphNode, GraphEdge
from app.core.mem0_manager import Mem0Manager, get_mem0_manager

router = APIRouter(prefix="/api/graph", tags=["graph"])


@router.get("/stats", response_model=GraphStatsResponse)
async def get_graph_stats(
    user_id: str = Query(None, description="사용자 ID (선택)"),
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> GraphStatsResponse:
    """
    그래프 통계 조회

    Args:
        user_id: 사용자 ID (선택)

    Returns:
        그래프 통계
    """
    try:
        logger.info(f"그래프 통계 조회 - User: {user_id or 'all'}")

        stats = mem0_manager.get_graph_stats(user_id)

        return GraphStatsResponse(**stats)

    except Exception as e:
        logger.error(f"통계 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")


@router.get("/visualize", response_model=GraphVisualizationResponse)
async def visualize_graph(
    user_id: str = Query(..., description="사용자 ID"),
    limit: int = Query(100, ge=1, le=1000, description="노드 개수 제한"),
    mem0_manager: Mem0Manager = Depends(get_mem0_manager)
) -> GraphVisualizationResponse:
    """
    그래프 시각화 데이터 조회

    Args:
        user_id: 사용자 ID
        limit: 노드 개수 제한

    Returns:
        그래프 노드 및 엣지
    """
    try:
        logger.info(f"그래프 시각화 데이터 조회 - User: {user_id}")

        # 메모리에서 노드와 엣지 추출 (간단한 구현)
        memories = mem0_manager.get_all_memories(user_id, limit=limit)

        # 메모리를 노드로 변환
        nodes = []
        edges = []

        for i, memory in enumerate(memories):
            memory_id = memory.get('id', f"node_{i}")
            memory_text = memory.get('memory', memory.get('text', 'Unknown'))

            node = GraphNode(
                id=memory_id,
                type="Memory",
                name=memory_text[:50],  # 처음 50자만
                properties={
                    "full_text": memory_text,
                    "created_at": memory.get('created_at', 'unknown')
                }
            )
            nodes.append(node)

        logger.success(f"시각화 데이터 생성 완료: {len(nodes)}개 노드")

        return GraphVisualizationResponse(
            nodes=nodes,
            edges=edges
        )

    except Exception as e:
        logger.error(f"시각화 데이터 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"시각화 데이터 조회 실패: {str(e)}")
