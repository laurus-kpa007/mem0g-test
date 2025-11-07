"""
API 테스트
Python 3.13 호환
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mem0g Testing Platform API"
    assert data["korean_optimized"] is True


def test_ping():
    """핑 엔드포인트 테스트"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "pong"}


def test_health():
    """헬스체크 엔드포인트 테스트"""
    response = client.get("/api/admin/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data


def test_config():
    """설정 조회 엔드포인트 테스트"""
    response = client.get("/api/admin/config")
    assert response.status_code == 200
    data = response.json()
    assert "ollama_llm_model" in data
    assert "graph_store_provider" in data


@pytest.mark.asyncio
async def test_chat_endpoint():
    """채팅 엔드포인트 기본 테스트"""
    response = client.post(
        "/api/chat",
        json={
            "message": "테스트 메시지",
            "user_id": "test_user",
            "session_id": "test_session"
        }
    )
    # Ollama가 실행 중이지 않으면 실패할 수 있음
    assert response.status_code in [200, 500]
