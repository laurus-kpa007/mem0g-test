# Mem0g Testing Platform

🧠 그래프 기반 메모리 테스트 플랫폼 (한국어 최적화)

## 프로젝트 개요

Mem0의 그래프 메모리 기능을 완전히 활용하는 대화형 테스트 플랫폼입니다.

### 주요 특징

- ✅ **그래프 기반 메모리**: Neo4j/Kuzu를 사용한 엔티티-관계 저장
- ✅ **로컬 LLM**: Ollama를 통한 완전한 오프라인 실행
- ✅ **한국어 최적화**: Qwen2.5 + BGE-M3 모델 사용
- ✅ **WebUI**: React 기반 직관적인 인터페이스
- ✅ **완전한 Mem0g 활용**: 엔티티 추출, 관계 감지, 시맨틱 검색

## 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.13)
- **Memory**: Mem0 0.1.34
- **LLM**: Ollama (Qwen2.5:7b)
- **Embedding**: BGE-M3 via Ollama
- **Graph DB**: Neo4j 5.15 / Kuzu
- **Vector DB**: Qdrant

### Frontend
- **Framework**: React 18 + TypeScript
- **HTTP Client**: Axios
- **Graph Viz**: Cytoscape.js (준비됨)

## 빠른 시작

### 1. 사전 요구사항

- Docker & Docker Compose
- Python 3.13 (로컬 개발 시)
- Node.js 20+ (프론트엔드 개발 시)

### 2. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# 필요시 설정 수정
nano .env
```

### 3. Docker Compose로 실행

```bash
# 전체 스택 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

서비스가 시작되면:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
- **Qdrant Dashboard**: http://localhost:6333/dashboard

### 4. Ollama 모델 다운로드

```bash
# Ollama 컨테이너에 접속
docker exec -it mem0g-ollama bash

# 모델 다운로드
ollama pull qwen2.5:7b
ollama pull bge-m3

# 확인
ollama list

# 컨테이너 나가기
exit
```

### 5. 사용 방법

1. 웹 브라우저에서 http://localhost:3000 접속
2. **채팅** 탭에서 메시지 입력 (예: "나는 서울에 살아요")
3. **그래프** 탭에서 사용자 ID로 그래프 시각화
4. **메모리** 탭에서 저장된 메모리 조회/검색
5. **테스트** 탭에서 엔티티 추출 및 벤치마크 실행

## 로컬 개발

### Backend 개발

```bash
cd backend

# 가상환경 생성 (Python 3.13)
python3.13 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
python -m app.main
```

### Frontend 개발

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

### 테스트 실행

```bash
# Backend 테스트
cd backend
pytest

# Frontend 테스트
cd frontend
npm test
```

## API 엔드포인트

### 채팅
- `POST /api/chat` - 메시지 전송 및 메모리 저장

### 메모리
- `POST /api/memories/search` - 메모리 검색
- `GET /api/memories` - 모든 메모리 조회
- `DELETE /api/memories/{id}` - 메모리 삭제
- `DELETE /api/memories` - 모든 메모리 삭제

### 그래프
- `GET /api/graph/stats` - 그래프 통계
- `GET /api/graph/visualize` - 그래프 시각화 데이터

### 테스트
- `POST /api/test/entity-extraction` - 엔티티 추출 테스트
- `GET /api/test/benchmark` - 성능 벤치마크

### 관리자
- `GET /api/admin/health` - 헬스체크
- `GET /api/admin/config` - 설정 조회
- `POST /api/admin/reset` - 시스템 초기화 (개발용)

## 프로젝트 구조

```
mem0g-test/
├── backend/
│   ├── app/
│   │   ├── api/          # API 엔드포인트
│   │   ├── core/         # 핵심 로직 (Mem0 관리자)
│   │   ├── models/       # Pydantic 스키마
│   │   ├── tests/        # 테스트
│   │   ├── config.py     # 설정 관리
│   │   └── main.py       # FastAPI 앱
│   ├── requirements.txt  # Python 의존성
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React 컴포넌트
│   │   ├── services/     # API 클라이언트
│   │   └── App.tsx       # 메인 앱
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml    # Docker Compose 설정
├── DESIGN.md            # 상세 설계 문서
└── README.md            # 이 파일
```

## 문제 해결

### Ollama 연결 실패
```bash
# Ollama 상태 확인
docker logs mem0g-ollama

# Ollama 재시작
docker-compose restart ollama
```

### Neo4j 연결 실패
```bash
# Neo4j 로그 확인
docker logs mem0g-neo4j

# Neo4j 브라우저에서 수동 확인
# http://localhost:7474 접속
# Username: neo4j, Password: password
```

### 메모리 부족
```bash
# Docker 리소스 확인
docker stats

# 사용하지 않는 컨테이너 정리
docker system prune -a
```

## 성능 최적화

### LLM 모델 크기 조정

RAM이 부족한 경우 더 작은 모델 사용:

```bash
# .env 파일에서 변경
OLLAMA_LLM_MODEL=qwen2.5:3b    # 대신 7b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text  # 대신 bge-m3
```

### 그래프 DB 변경

Neo4j 대신 경량 Kuzu 사용:

```bash
# .env 파일에서 변경
GRAPH_STORE_PROVIDER=kuzu
```

## 라이선스

이 프로젝트는 테스트 목적으로 만들어졌습니다.

## 참고 자료

- [Mem0 공식 문서](https://docs.mem0.ai/)
- [Ollama 공식 사이트](https://ollama.ai/)
- [Neo4j 문서](https://neo4j.com/docs/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [설계 문서](./DESIGN.md)

## 기여

이슈와 PR은 언제나 환영입니다!

---

**Powered by Mem0 + Ollama + Neo4j + Qdrant** 🚀
