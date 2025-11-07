"""
Pydantic 스키마 정의
Python 3.13 호환
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """채팅 요청"""
    message: str = Field(..., description="사용자 메시지")
    user_id: str = Field(..., description="사용자 ID")
    session_id: Optional[str] = Field(None, description="세션 ID")

    model_config = {"json_schema_extra": {
        "example": {
            "message": "나는 서울에 살고 있어",
            "user_id": "user123",
            "session_id": "session456"
        }
    }}


class ChatResponse(BaseModel):
    """채팅 응답"""
    message: str = Field(..., description="응답 메시지")
    memories: List[Dict[str, Any]] = Field(default_factory=list, description="관련 메모리")
    entities: List[Dict[str, Any]] = Field(default_factory=list, description="추출된 엔티티")
    relationships: List[Dict[str, Any]] = Field(default_factory=list, description="추출된 관계")

    model_config = {"json_schema_extra": {
        "example": {
            "message": "서울 거주 정보를 저장했습니다.",
            "memories": [{"text": "사용자는 서울에 거주"}],
            "entities": [{"name": "서울", "type": "Place"}],
            "relationships": [{"source": "user123", "target": "서울", "type": "lives_in"}]
        }
    }}


class MemorySearchRequest(BaseModel):
    """메모리 검색 요청"""
    query: str = Field(..., description="검색 쿼리")
    user_id: str = Field(..., description="사용자 ID")
    limit: int = Field(default=10, ge=1, le=100, description="결과 개수")

    model_config = {"json_schema_extra": {
        "example": {
            "query": "서울에 사는 사람",
            "user_id": "user123",
            "limit": 10
        }
    }}


class MemorySearchResponse(BaseModel):
    """메모리 검색 응답"""
    results: List[Dict[str, Any]] = Field(..., description="검색 결과")
    count: int = Field(..., description="결과 개수")

    model_config = {"json_schema_extra": {
        "example": {
            "results": [
                {
                    "memory": "사용자는 서울에 거주",
                    "score": 0.95,
                    "metadata": {"created_at": "2025-01-01T00:00:00"}
                }
            ],
            "count": 1
        }
    }}


class GraphNode(BaseModel):
    """그래프 노드"""
    id: str = Field(..., description="노드 ID")
    type: str = Field(..., description="노드 타입")
    name: str = Field(..., description="노드 이름")
    properties: Dict[str, Any] = Field(default_factory=dict, description="노드 속성")

    model_config = {"json_schema_extra": {
        "example": {
            "id": "node_123",
            "type": "Person",
            "name": "Alice",
            "properties": {"age": 30, "city": "서울"}
        }
    }}


class GraphEdge(BaseModel):
    """그래프 엣지"""
    source: str = Field(..., description="출발 노드 ID")
    target: str = Field(..., description="도착 노드 ID")
    type: str = Field(..., description="관계 타입")
    properties: Dict[str, Any] = Field(default_factory=dict, description="엣지 속성")

    model_config = {"json_schema_extra": {
        "example": {
            "source": "node_123",
            "target": "node_456",
            "type": "knows",
            "properties": {"since": "2020"}
        }
    }}


class GraphVisualizationResponse(BaseModel):
    """그래프 시각화 응답"""
    nodes: List[GraphNode] = Field(..., description="노드 리스트")
    edges: List[GraphEdge] = Field(..., description="엣지 리스트")

    model_config = {"json_schema_extra": {
        "example": {
            "nodes": [
                {"id": "node_123", "type": "Person", "name": "Alice", "properties": {}},
                {"id": "node_456", "type": "Place", "name": "서울", "properties": {}}
            ],
            "edges": [
                {"source": "node_123", "target": "node_456", "type": "lives_in", "properties": {}}
            ]
        }
    }}


class GraphStatsResponse(BaseModel):
    """그래프 통계 응답"""
    node_count: int = Field(..., description="노드 개수")
    edge_count: int = Field(..., description="엣지 개수")
    node_types: Dict[str, int] = Field(..., description="노드 타입별 개수")
    edge_types: Dict[str, int] = Field(..., description="엣지 타입별 개수")

    model_config = {"json_schema_extra": {
        "example": {
            "node_count": 100,
            "edge_count": 50,
            "node_types": {"Person": 30, "Place": 20, "Event": 50},
            "edge_types": {"knows": 20, "located_at": 30}
        }
    }}


class EntityExtractionRequest(BaseModel):
    """엔티티 추출 테스트 요청"""
    text: str = Field(..., description="분석할 텍스트")

    model_config = {"json_schema_extra": {
        "example": {
            "text": "Alice는 서울에서 Bob을 만났다."
        }
    }}


class EntityExtractionResponse(BaseModel):
    """엔티티 추출 응답"""
    entities: List[Dict[str, Any]] = Field(..., description="추출된 엔티티")
    relationships: List[Dict[str, Any]] = Field(..., description="추출된 관계")

    model_config = {"json_schema_extra": {
        "example": {
            "entities": [
                {"name": "Alice", "type": "Person"},
                {"name": "Bob", "type": "Person"},
                {"name": "서울", "type": "Place"}
            ],
            "relationships": [
                {"source": "Alice", "target": "Bob", "type": "met"},
                {"source": "Alice", "target": "서울", "type": "located_at"}
            ]
        }
    }}


class HealthResponse(BaseModel):
    """헬스체크 응답"""
    status: str = Field(..., description="상태")
    timestamp: datetime = Field(default_factory=datetime.now, description="타임스탬프")
    services: Dict[str, str] = Field(default_factory=dict, description="서비스 상태")

    model_config = {"json_schema_extra": {
        "example": {
            "status": "healthy",
            "timestamp": "2025-01-01T00:00:00",
            "services": {
                "ollama": "connected",
                "neo4j": "connected",
                "qdrant": "connected"
            }
        }
    }}
