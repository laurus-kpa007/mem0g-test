# 외부 Ollama 서버 연결 가이드

이 프로젝트는 외부 PC에서 실행 중인 Ollama 서버를 사용합니다.

## 📋 사전 준비

### 1. Ollama 서버 PC에 모델 다운로드

외부 PC에서 다음 명령어를 실행하세요:

```bash
# qwen2.5:7b 다운로드 (약 4.7GB, 5-10분 소요)
ollama pull qwen2.5:7b

# bge-m3 다운로드 (약 2.2GB, 3-5분 소요)
ollama pull bge-m3

# 다운로드 확인
ollama list
```

**출력 예시:**
```
NAME              ID              SIZE
qwen2.5:7b        abc123...       4.7 GB
bge-m3           def456...       2.2 GB
```

### 2. Ollama 서버 IP 확인

외부 PC에서 IP 주소를 확인:

**Linux/Mac:**
```bash
ip addr show | grep inet
# 또는
ifconfig | grep inet
```

**Windows:**
```cmd
ipconfig
```

**예시:** `192.168.1.100`

### 3. Ollama 서버 접근 확인

다른 PC에서 Ollama 서버에 접근 가능한지 테스트:

```bash
# 메인 PC에서 실행
curl http://192.168.1.100:11434/api/version
```

정상 응답 예시:
```json
{"version":"0.x.x"}
```

❌ **연결 실패 시:**
- 방화벽 설정 확인 (11434 포트 허용)
- Ollama가 모든 인터페이스에서 수신하도록 설정

**Ollama 외부 접근 허용 (필요시):**

Linux/Mac에서 환경변수 설정:
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export OLLAMA_HOST=0.0.0.0:11434
```

또는 Ollama 실행 시:
```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## 🔧 Docker Compose 설정

### 1. .env 파일 수정

프로젝트 루트의 `.env` 파일을 열고 Ollama IP 수정:

```bash
nano .env
```

**수정 전:**
```env
OLLAMA_BASE_URL=http://YOUR_OLLAMA_SERVER_IP:11434
```

**수정 후 (예시):**
```env
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

### 2. 설정 확인

```bash
cat .env | grep OLLAMA_BASE_URL
```

올바른 IP가 표시되어야 합니다.

## 🚀 서비스 시작

### 전체 시스템 시작

```bash
docker-compose up -d
```

실행되는 서비스:
- ✅ Neo4j (그래프 DB)
- ✅ Qdrant (벡터 DB)
- ✅ Backend API (외부 Ollama 연결)
- ✅ Frontend

### 연결 확인

#### 1. 백엔드 헬스체크
```bash
curl http://localhost:8000/api/admin/health
```

**정상 응답:**
```json
{
  "status": "healthy",
  "services": {
    "mem0": "connected",
    "graph_db": "connected"
  }
}
```

#### 2. 설정 확인
```bash
curl http://localhost:8000/api/admin/config
```

**Ollama URL 확인:**
```json
{
  "ollama_base_url": "http://192.168.1.100:11434",
  "ollama_llm_model": "qwen2.5:7b",
  "ollama_embedding_model": "bge-m3"
  ...
}
```

#### 3. 로그 확인
```bash
docker-compose logs backend | grep -i ollama
```

정상 연결 시 에러가 없어야 합니다.

## 🧪 테스트

### 웹 브라우저에서 테스트

1. Frontend 접속: http://localhost:3000
2. 채팅 탭에서 메시지 입력:
   ```
   안녕하세요, 테스트 메시지입니다
   ```
3. 응답이 정상적으로 오면 성공! ✅

### API 직접 테스트

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "테스트 메시지",
    "user_id": "test_user"
  }'
```

## ❓ 문제 해결

### 문제 1: "Failed to connect to Ollama"

**증상:**
```
Error: Failed to connect to http://192.168.1.100:11434
```

**해결 방법:**

1. **Ollama 서버 실행 확인**
   ```bash
   # Ollama 서버 PC에서
   ollama list
   ```

2. **네트워크 연결 확인**
   ```bash
   # 메인 PC에서
   ping 192.168.1.100
   telnet 192.168.1.100 11434
   ```

3. **방화벽 설정**
   ```bash
   # Ollama 서버 PC (Linux)에서
   sudo ufw allow 11434/tcp

   # 또는 firewalld
   sudo firewall-cmd --permanent --add-port=11434/tcp
   sudo firewall-cmd --reload
   ```

4. **Ollama 재시작 (외부 접근 허용)**
   ```bash
   # Ollama 서버 PC에서
   pkill ollama
   OLLAMA_HOST=0.0.0.0:11434 ollama serve &
   ```

### 문제 2: "Model not found"

**증상:**
```
Error: model 'qwen2.5:7b' not found
```

**해결:**
```bash
# Ollama 서버 PC에서
ollama pull qwen2.5:7b
ollama pull bge-m3
```

### 문제 3: IP 주소 변경됨

**증상:**
Ollama 서버 IP가 동적으로 할당되어 변경됨

**해결:**
1. **Ollama 서버 PC에 고정 IP 설정** (권장)
2. 또는 `.env` 파일 수정 후 재시작:
   ```bash
   nano .env
   # OLLAMA_BASE_URL 수정
   docker-compose restart backend
   ```

## 📊 네트워크 구성도

```
┌─────────────────────────────────┐
│  Ollama 서버 PC                  │
│  IP: 192.168.1.100              │
│  Port: 11434                    │
│  ┌─────────────────────┐        │
│  │ Ollama              │        │
│  │ - qwen2.5:7b        │        │
│  │ - bge-m3            │        │
│  └─────────────────────┘        │
└────────────┬────────────────────┘
             │
             │ Network
             │
┌────────────┴────────────────────┐
│  메인 PC (Docker)                │
│  IP: 192.168.1.50               │
│  ┌──────────────────────┐       │
│  │ Docker Compose       │       │
│  │ - Neo4j    :7474     │       │
│  │ - Qdrant   :6333     │       │
│  │ - Backend  :8000 ────┼───────┼─→ Ollama 연결
│  │ - Frontend :3000     │       │
│  └──────────────────────┘       │
└─────────────────────────────────┘
```

## 💡 추가 팁

### 1. Ollama 성능 모니터링

Ollama 서버 PC에서:
```bash
# GPU 사용률 (NVIDIA)
nvidia-smi

# CPU 사용률
top | grep ollama
```

### 2. 모델 사전 로드

첫 요청이 느릴 수 있으므로 모델 미리 로드:
```bash
# Ollama 서버 PC에서
ollama run qwen2.5:7b "안녕하세요"
```

### 3. 여러 클라이언트 연결

같은 Ollama 서버를 여러 PC에서 동시 사용 가능:
- PC-A: http://192.168.1.100:11434
- PC-B: http://192.168.1.100:11434
- PC-C: http://192.168.1.100:11434

## ✅ 체크리스트

실행 전 확인사항:

- [ ] Ollama 서버 PC에서 모델 다운로드 완료
- [ ] Ollama 서버 IP 주소 확인
- [ ] `.env` 파일에 올바른 IP 설정
- [ ] 방화벽에서 11434 포트 허용
- [ ] curl로 Ollama 접근 확인
- [ ] `docker-compose up -d` 실행
- [ ] 백엔드 헬스체크 통과

---

**모든 설정이 완료되면 QUICKSTART.md의 7단계부터 진행하세요!** 🚀
