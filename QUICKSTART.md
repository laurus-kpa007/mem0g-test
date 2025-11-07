# 🚀 Mem0g 테스트 플랫폼 - 5분 빠른 시작 가이드

완전 초보자도 따라할 수 있는 단계별 가이드입니다.

---

## 📋 1단계: 사전 준비

### 필수 프로그램 설치

#### 1-1. Docker Desktop 설치

**Windows/Mac 사용자:**
1. [Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop/)
2. 설치 후 Docker Desktop 실행
3. 우측 하단 Docker 아이콘이 초록색이 되면 준비 완료

**Linux 사용자:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
newgrp docker
```

#### 1-2. Docker 확인

터미널(또는 명령 프롬프트)을 열고:

```bash
docker --version
docker-compose --version
```

버전 정보가 나오면 성공! ✅

---

## 📥 2단계: 프로젝트 다운로드

### 방법 1: Git 사용 (권장)

```bash
# 프로젝트 클론
git clone <repository-url> mem0g-test
cd mem0g-test
```

### 방법 2: 이미 다운로드된 경우

```bash
# 프로젝트 폴더로 이동
cd /path/to/mem0g-test
```

### 폴더 확인

```bash
ls -la
```

다음 파일들이 보여야 합니다:
- `docker-compose.yml`
- `backend/`
- `frontend/`
- `.env.example`

---

## 🔧 3단계: 환경 설정

### .env 파일 생성

**Windows (명령 프롬프트):**
```cmd
copy .env.example .env
```

**Mac/Linux (터미널):**
```bash
cp .env.example .env
```

> 💡 **참고**: 기본 설정을 그대로 사용해도 됩니다. 나중에 수정 가능합니다.

---

## 🐳 4단계: Docker로 전체 시스템 시작

### 4-1. 모든 서비스 시작

```bash
docker-compose up -d
```

**이 명령어가 하는 일:**
- Neo4j (그래프 DB) 시작
- Qdrant (벡터 DB) 시작
- Ollama (LLM 서버) 시작
- Backend API 서버 시작
- Frontend 웹 서버 시작

⏱️ **소요 시간**: 처음 실행 시 5-10분 (Docker 이미지 다운로드)

### 4-2. 실행 상태 확인

```bash
docker-compose ps
```

**정상 상태:**
```
NAME                 STATUS
mem0g-neo4j          Up (healthy)
mem0g-qdrant         Up (healthy)
mem0g-ollama         Up
mem0g-backend        Up (healthy)
mem0g-frontend       Up
```

모든 서비스가 `Up`이면 성공! ✅

### 4-3. 로그 확인 (문제 발생 시)

```bash
# 전체 로그 보기
docker-compose logs -f

# 특정 서비스 로그만 보기
docker-compose logs -f backend
```

(Ctrl+C로 로그 보기 종료)

---

## 🤖 5단계: AI 모델 다운로드 (중요!)

### 5-1. Ollama 컨테이너 접속

```bash
docker exec -it mem0g-ollama bash
```

프롬프트가 `root@xxx:/#`로 바뀌면 성공!

### 5-2. 한국어 최적화 모델 다운로드

```bash
# 메인 LLM 모델 (약 4.7GB, 5-10분 소요)
ollama pull qwen2.5:7b

# 임베딩 모델 (약 2.2GB, 3-5분 소요)
ollama pull bge-m3
```

**다운로드 진행 표시:**
```
pulling manifest
pulling 8934d96d3f08... 100% ▕████████████▏ 4.7 GB
...
success
```

### 5-3. 모델 다운로드 확인

```bash
ollama list
```

**정상 출력:**
```
NAME              ID              SIZE
qwen2.5:7b        abc123...       4.7 GB
bge-m3           def456...       2.2 GB
```

### 5-4. 컨테이너 나가기

```bash
exit
```

프롬프트가 원래대로 돌아오면 성공!

---

## 🌐 6단계: 웹 브라우저로 접속

### 6-1. Frontend 접속

웹 브라우저를 열고:

```
http://localhost:3000
```

**보이는 화면:**
```
🧠 Mem0g Testing Platform
그래프 기반 메모리 테스트 플랫폼 (한국어 최적화)
✅ API 연결됨

[💬 채팅] [🕸️ 그래프] [📚 메모리] [🧪 테스트]
```

### 6-2. API 문서 접속 (선택)

```
http://localhost:8000/docs
```

FastAPI 자동 생성 API 문서를 볼 수 있습니다.

### 6-3. Neo4j 브라우저 접속 (선택)

```
http://localhost:7474
```

**로그인 정보:**
- Username: `neo4j`
- Password: `password`

그래프 데이터베이스를 직접 조회할 수 있습니다.

---

## 🎮 7단계: 실제 사용해보기

### 테스트 시나리오 1: 간단한 대화

1. **채팅 탭 클릭**

2. **메시지 입력:**
   ```
   나는 서울에 살고 있어요
   ```

3. **Enter 키 또는 '전송' 버튼 클릭**

4. **결과 확인:**
   - AI가 메시지를 저장했다는 응답
   - 추출된 엔티티: "서울" (Place)
   - 관계: "user → lives_in → 서울"

### 테스트 시나리오 2: 관계 추출

1. **새 메시지 입력:**
   ```
   Alice는 Bob의 친구이고 둘 다 개발자야
   ```

2. **결과 확인:**
   - 엔티티: Alice (Person), Bob (Person)
   - 관계: Alice → friend_of → Bob
   - 직업 정보 저장

### 테스트 시나리오 3: 메모리 검색

1. **메모리 탭 클릭**

2. **사용자 ID 입력:**
   ```
   user_1234567890  (채팅 탭에서 확인 가능)
   ```

3. **'전체 조회' 버튼 클릭**

4. **결과:** 저장된 모든 메모리 표시

5. **검색 테스트:**
   - 검색어: `서울`
   - '검색' 버튼 클릭
   - 서울 관련 메모리만 표시

### 테스트 시나리오 4: 그래프 시각화

1. **그래프 탭 클릭**

2. **사용자 ID 입력 후 '그래프 로드'**

3. **결과:**
   - 노드 개수 통계
   - 엣지 개수 통계
   - 노드 목록 표시

### 테스트 시나리오 5: 엔티티 추출 테스트

1. **테스트 탭 클릭**

2. **텍스트 입력:**
   ```
   김철수는 강남역에서 이영희를 만났고 함께 삼성동으로 갔다
   ```

3. **'엔티티 추출' 버튼 클릭**

4. **결과 확인:**
   - 추출된 엔티티: 김철수, 이영희, 강남역, 삼성동
   - 관계: 김철수 → met → 이영희, 김철수 → went_to → 삼성동

### 테스트 시나리오 6: 성능 벤치마크

1. **테스트 탭에서 '벤치마크 실행' 클릭**

2. **결과:**
   ```
   메모리 추가: 1,234ms
   메모리 검색: 456ms
   상태: completed
   ```

---

## 🔍 8단계: Neo4j에서 실제 그래프 확인

### 8-1. Neo4j 브라우저 접속

```
http://localhost:7474
```

로그인: `neo4j` / `password`

### 8-2. 그래프 조회 쿼리

**모든 노드와 관계 보기:**
```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 50
```

**특정 사용자의 그래프:**
```cypher
MATCH (n {user_id: "user_1234567890"})
RETURN n
```

**엔티티 타입별 개수:**
```cypher
MATCH (n)
RETURN labels(n) as type, count(*) as count
```

### 8-3. 시각화

쿼리 실행 후 그래프 아이콘을 클릭하면 시각적으로 표시됩니다!

---

## 🛠️ 9단계: 문제 해결

### 문제 1: "포트가 이미 사용 중입니다"

**증상:**
```
Error: Port 8000 is already in use
```

**해결:**
```bash
# 사용 중인 포트 찾기 (Linux/Mac)
lsof -i :8000

# 사용 중인 포트 찾기 (Windows)
netstat -ano | findstr :8000

# Docker 컨테이너 모두 중지
docker-compose down

# 다시 시작
docker-compose up -d
```

### 문제 2: "Ollama 연결 실패"

**증상:**
```
Error: Failed to connect to Ollama
```

**해결:**
```bash
# Ollama 상태 확인
docker logs mem0g-ollama

# Ollama 재시작
docker-compose restart ollama

# 모델 다시 다운로드
docker exec -it mem0g-ollama bash
ollama pull qwen2.5:7b
ollama pull bge-m3
exit
```

### 문제 3: "메모리 부족"

**증상:**
```
Error: Out of memory
```

**해결:**

1. **Docker Desktop 설정에서 메모리 증가**
   - Docker Desktop → Settings → Resources
   - Memory를 8GB 이상으로 설정

2. **또는 더 작은 모델 사용**
   ```bash
   # .env 파일 수정
   OLLAMA_LLM_MODEL=qwen2.5:3b  # 7b 대신
   OLLAMA_EMBEDDING_MODEL=nomic-embed-text  # bge-m3 대신
   ```

### 문제 4: "Frontend가 백엔드에 연결 안됨"

**증상:**
Frontend에서 "❌ API 연결 실패"

**해결:**
```bash
# 백엔드 로그 확인
docker-compose logs backend

# 백엔드 재시작
docker-compose restart backend

# 헬스체크
curl http://localhost:8000/ping
```

### 문제 5: "모델 다운로드가 느립니다"

**정상입니다!**
- qwen2.5:7b는 4.7GB로 인터넷 속도에 따라 5-20분 소요
- 한 번만 다운로드하면 영구 저장됩니다

**진행 상태 확인:**
```bash
docker exec -it mem0g-ollama bash
ollama list  # 다운로드된 모델 확인
```

---

## 🧹 10단계: 정리 (사용 후)

### 일시 중지 (나중에 다시 시작 가능)

```bash
docker-compose stop
```

### 완전 삭제 (데이터도 모두 삭제)

```bash
# 컨테이너와 네트워크 삭제
docker-compose down

# 볼륨(데이터)까지 모두 삭제
docker-compose down -v
```

### 다시 시작할 때

```bash
docker-compose start
```

또는

```bash
docker-compose up -d
```

---

## 📊 시스템 요구사항

### 최소 사양
- **RAM**: 8GB 이상
- **디스크**: 15GB 여유 공간
- **CPU**: 듀얼코어 이상

### 권장 사양
- **RAM**: 16GB 이상 (qwen2.5:7b 사용 시)
- **디스크**: 30GB 여유 공간
- **CPU**: 쿼드코어 이상
- **GPU**: 선택사항 (없어도 작동)

---

## 🎓 추가 학습 자료

### 더 자세한 문서
- **DESIGN.md**: 전체 시스템 아키텍처
- **README.md**: 프로젝트 개요 및 고급 설정
- **VERIFICATION.md**: 자체 검증 보고서

### API 문서
- http://localhost:8000/docs - 대화형 API 문서
- http://localhost:8000/redoc - API 레퍼런스

### 예제 쿼리
```bash
# 채팅 API 직접 호출
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "테스트 메시지",
    "user_id": "user_test"
  }'

# 헬스체크
curl http://localhost:8000/api/admin/health

# 설정 조회
curl http://localhost:8000/api/admin/config
```

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: 인터넷 연결 없이 작동하나요?
**A**: 네! 모델을 한 번 다운로드하면 완전히 오프라인으로 작동합니다.

### Q2: 한국어만 지원하나요?
**A**: 아니요. Qwen2.5는 다국어를 지원하지만, 한국어 성능이 특히 우수합니다.

### Q3: 데이터는 어디에 저장되나요?
**A**: Docker 볼륨에 저장됩니다. `docker-compose down -v`로 삭제 가능합니다.

### Q4: GPU가 없어도 되나요?
**A**: 네! CPU만으로도 작동합니다. GPU가 있으면 더 빠릅니다.

### Q5: 프로덕션에서 사용할 수 있나요?
**A**: 이 프로젝트는 테스트 플랫폼입니다. 프로덕션 사용 시 인증/인가를 추가해야 합니다.

---

## 🎉 성공!

축하합니다! 이제 Mem0g 테스트 플랫폼을 완전히 사용할 수 있습니다.

### 다음 단계 제안
1. 🗣️ **다양한 대화 테스트** - 복잡한 문장으로 엔티티 추출 테스트
2. 🔍 **검색 기능 활용** - 의미론적 검색의 강력함 체험
3. 📊 **그래프 분석** - Neo4j에서 실제 지식 그래프 탐색
4. ⚡ **성능 측정** - 벤치마크로 시스템 성능 확인
5. 🔧 **설정 변경** - 다른 모델 시도 (llama3, gemma2 등)

---

## 💬 도움이 필요하신가요?

- 문제 발생 시 로그 확인: `docker-compose logs -f`
- GitHub Issues에 문의하기
- DESIGN.md에서 상세 아키텍처 확인

---

**제작**: Claude AI Assistant
**업데이트**: 2025-11-07
**버전**: 1.0.0

즐거운 테스팅 되세요! 🚀
