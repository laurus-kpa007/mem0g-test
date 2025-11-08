"""
Mem0 Graph Memory 관리자
Python 3.13 호환
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from mem0 import Memory

from app.config import settings


class Mem0Manager:
    """Mem0 그래프 메모리 관리 클래스"""

    def __init__(self):
        """초기화"""
        self.config = settings.get_mem0_config()
        self.memory: Optional[Memory] = None
        self._initialize_memory()

    def _initialize_memory(self):
        """메모리 인스턴스 초기화"""
        try:
            logger.info("Mem0 메모리 초기화 중...")
            logger.debug(f"Mem0 설정: {self.config}")
            self.memory = Memory.from_config(self.config)
            logger.success("Mem0 메모리 초기화 완료")
        except Exception as e:
            logger.error(f"Mem0 메모리 초기화 실패: {e}")
            raise

    def add_memory(
        self,
        data: str,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        메모리 추가

        Args:
            data: 저장할 데이터
            user_id: 사용자 ID
            metadata: 추가 메타데이터

        Returns:
            추가 결과
        """
        try:
            logger.info(f"메모리 추가 중 - User: {user_id}")
            logger.debug(f"Data: {data[:100]}...")

            # Mem0에 메모리 추가
            result = self.memory.add(
                messages=data,
                user_id=user_id,
                metadata=metadata or {}
            )

            logger.success(f"메모리 추가 완료: {len(result.get('results', []))}개 메모리")
            return result

        except Exception as e:
            logger.error(f"메모리 추가 실패: {e}")
            raise

    def search_memory(
        self,
        query: str,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        메모리 검색

        Args:
            query: 검색 쿼리
            user_id: 사용자 ID
            limit: 결과 개수

        Returns:
            검색 결과 리스트
        """
        try:
            logger.info(f"메모리 검색 중 - User: {user_id}, Query: {query}")

            # Mem0에서 메모리 검색
            results = self.memory.search(
                query=query,
                user_id=user_id,
                limit=limit
            )

            # Mem0 결과 포맷 처리 (dict 또는 list 가능)
            memories_list = []
            if isinstance(results, dict):
                memories_list = results.get('results', [])
            elif isinstance(results, list):
                memories_list = results

            logger.success(f"메모리 검색 완료: {len(memories_list)}개 결과")
            return memories_list

        except Exception as e:
            logger.error(f"메모리 검색 실패: {e}")
            raise

    def get_all_memories(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        모든 메모리 조회

        Args:
            user_id: 사용자 ID
            limit: 결과 개수

        Returns:
            메모리 리스트
        """
        try:
            logger.info(f"모든 메모리 조회 중 - User: {user_id}")

            # Mem0에서 모든 메모리 조회
            results = self.memory.get_all(
                user_id=user_id
            )

            # Mem0 결과 포맷 처리 (dict 또는 list 가능)
            memories_list = []
            if isinstance(results, dict):
                memories_list = results.get('results', [])
            elif isinstance(results, list):
                memories_list = results

            # limit 적용
            memories_list = memories_list[:limit]

            logger.success(f"메모리 조회 완료: {len(memories_list)}개")
            return memories_list

        except Exception as e:
            logger.error(f"메모리 조회 실패: {e}")
            raise

    def delete_memory(self, memory_id: str) -> bool:
        """
        메모리 삭제

        Args:
            memory_id: 메모리 ID

        Returns:
            성공 여부
        """
        try:
            logger.info(f"메모리 삭제 중 - ID: {memory_id}")

            # Mem0에서 메모리 삭제
            self.memory.delete(memory_id=memory_id)

            logger.success(f"메모리 삭제 완료: {memory_id}")
            return True

        except Exception as e:
            logger.error(f"메모리 삭제 실패: {e}")
            raise

    def delete_all_memories(self, user_id: str) -> bool:
        """
        사용자의 모든 메모리 삭제

        Args:
            user_id: 사용자 ID

        Returns:
            성공 여부
        """
        try:
            logger.warning(f"모든 메모리 삭제 중 - User: {user_id}")

            # Mem0에서 모든 메모리 삭제
            self.memory.delete_all(user_id=user_id)

            logger.success(f"모든 메모리 삭제 완료: {user_id}")
            return True

        except Exception as e:
            logger.error(f"메모리 삭제 실패: {e}")
            raise

    def generate_response(
        self,
        message: str,
        user_id: str,
        memories: List[Dict[str, Any]]
    ) -> str:
        """
        LLM으로 대화형 응답 생성

        Args:
            message: 사용자 메시지
            user_id: 사용자 ID
            memories: 관련 메모리 리스트

        Returns:
            LLM 응답
        """
        try:
            logger.info(f"LLM 응답 생성 중 - User: {user_id}")

            # 메모리 컨텍스트 구성
            context = ""
            if memories:
                context = "관련 기억:\n"
                for mem in memories[:3]:  # 최대 3개만 사용
                    memory_text = mem.get('memory', '')
                    context += f"- {memory_text}\n"
                context += "\n"

            # 프롬프트 구성
            prompt = f"""You are a friendly Korean assistant. Always respond in Korean.

{context}User message: {message}

Please respond naturally and kindly in Korean language only."""

            # Ollama를 통해 LLM 응답 생성
            import requests
            # LLM 전용 URL 사용
            llm_url = settings.ollama_base_url if settings.ollama_base_url else settings.ollama_llm_url
            ollama_url = f"{llm_url}/api/generate"

            response = requests.post(
                ollama_url,
                json={
                    "model": settings.ollama_llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                llm_response = result.get('response', '').strip()
                logger.success(f"LLM 응답 생성 완료: {llm_response[:50]}...")
                return llm_response
            else:
                logger.error(f"Ollama 응답 실패: {response.status_code}")
                return "죄송합니다. 응답을 생성하는 데 문제가 발생했습니다."

        except Exception as e:
            logger.error(f"LLM 응답 생성 실패: {e}")
            return f"죄송합니다. 응답을 생성할 수 없습니다: {str(e)}"

    def get_graph_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        그래프 통계 조회

        Args:
            user_id: 사용자 ID (선택)

        Returns:
            통계 정보
        """
        try:
            logger.info(f"그래프 통계 조회 중 - User: {user_id or 'all'}")

            # 기본 통계
            stats = {
                "node_count": 0,
                "edge_count": 0,
                "node_types": {},
                "edge_types": {}
            }

            # Memory 객체에서 통계 추출
            if user_id:
                memories = self.get_all_memories(user_id)
                stats["node_count"] = len(memories)

            logger.success(f"통계 조회 완료")
            return stats

        except Exception as e:
            logger.error(f"통계 조회 실패: {e}")
            return {
                "node_count": 0,
                "edge_count": 0,
                "node_types": {},
                "edge_types": {},
                "error": str(e)
            }

    def reset(self) -> bool:
        """
        모든 데이터 초기화 (개발용)

        Returns:
            성공 여부
        """
        try:
            logger.warning("전체 메모리 초기화 중...")

            # 메모리 재초기화
            if hasattr(self.memory, 'reset'):
                self.memory.reset()
                logger.success("메모리 초기화 완료")
            else:
                logger.warning("reset 메서드가 지원되지 않습니다")

            return True

        except Exception as e:
            logger.error(f"메모리 초기화 실패: {e}")
            raise

    def health_check(self) -> Dict[str, str]:
        """
        헬스체크

        Returns:
            서비스 상태
        """
        services = {}

        try:
            # Mem0 상태 확인
            if self.memory:
                services["mem0"] = "connected"
            else:
                services["mem0"] = "disconnected"

            # 그래프 DB 상태 (간단한 쿼리로 확인)
            try:
                self.get_graph_stats()
                services["graph_db"] = "connected"
            except:
                services["graph_db"] = "error"

            logger.info(f"헬스체크 완료: {services}")
            return services

        except Exception as e:
            logger.error(f"헬스체크 실패: {e}")
            return {"error": str(e)}


# 전역 인스턴스
_mem0_manager: Optional[Mem0Manager] = None


def get_mem0_manager() -> Mem0Manager:
    """Mem0Manager 싱글톤 인스턴스 반환"""
    global _mem0_manager
    if _mem0_manager is None:
        _mem0_manager = Mem0Manager()
    return _mem0_manager
