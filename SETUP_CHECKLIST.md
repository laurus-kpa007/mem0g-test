# ✅ 외부 Ollama 서버 설정 체크리스트

간단한 단계별 체크리스트로 빠르게 설정하세요!

---

## 🖥️ Ollama 서버 PC (고성능 PC)

### [ ] 1단계: Ollama 설치 확인
```bash
ollama --version
```
✅ 버전 정보가 나오면 OK

❌ 설치 안된 경우: https://ollama.ai/download

---

### [ ] 2단계: 모델 다운로드
```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```
⏱️ 소요 시간: 10-15분 (인터넷 속도에 따라)

**확인:**
```bash
ollama list
```

**결과:**
```
NAME              ID              SIZE
qwen2.5:7b        abc123...       4.7 GB  ✅
bge-m3           def456...       2.2 GB  ✅
```

---

### [ ] 3단계: IP 주소 확인

**Linux/Mac:**
```bash
hostname -I
```

**Windows:**
```cmd
ipconfig
```

**예시:** `192.168.1.100`

📝 **메모:** _____________________ (나중에 사용)

---

### [ ] 4단계: 외부 접근 허용 (중요!)

**방법 1: 환경변수 설정 (권장)**

Linux/Mac:
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export OLLAMA_HOST=0.0.0.0:11434' >> ~/.bashrc
source ~/.bashrc

# Ollama 재시작
pkill ollama
ollama serve &
```

Windows:
```cmd
setx OLLAMA_HOST "0.0.0.0:11434"
# 컴퓨터 재시작 또는 Ollama 재시작
```

**방법 2: 실행 시 설정**
```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

---

### [ ] 5단계: 방화벽 설정

**Linux (UFW):**
```bash
sudo ufw allow 11434/tcp
sudo ufw status
```

**Linux (firewalld):**
```bash
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --reload
```

**Windows:**
1. 제어판 → Windows Defender 방화벽
2. 고급 설정 → 인바운드 규칙
3. 새 규칙 → 포트 → TCP 11434
4. 연결 허용

---

### [ ] 6단계: 로컬 테스트
```bash
curl http://localhost:11434/api/version
```

**성공 시:**
```json
{"version":"0.x.x"}
```

---

## 💻 Docker 메인 PC

### [ ] 7단계: 프로젝트 다운로드
```bash
cd ~
git clone <repository-url> mem0g-test
cd mem0g-test
```

---

### [ ] 8단계: Ollama 연결 테스트

**Ollama 서버 IP로 교체** (예: 192.168.1.100)
```bash
curl http://192.168.1.100:11434/api/version
```

✅ **성공:** JSON 응답
❌ **실패:**
- IP 주소 확인
- 방화벽 설정 확인
- Ollama 서버 실행 확인

---

### [ ] 9단계: .env 파일 설정

```bash
# .env 파일 생성
cp .env.example .env

# 편집기로 열기
nano .env
```

**수정:**
```env
# 수정 전
OLLAMA_BASE_URL=http://YOUR_OLLAMA_SERVER_IP:11434

# 수정 후 (예시: 192.168.1.100)
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

**확인:**
```bash
cat .env | grep OLLAMA_BASE_URL
```

---

### [ ] 10단계: Docker 서비스 시작
```bash
docker-compose up -d
```

⏱️ 소요 시간: 5-10분 (첫 실행 시)

**확인:**
```bash
docker-compose ps
```

**정상 상태:**
```
NAME                 STATUS
mem0g-neo4j          Up (healthy)  ✅
mem0g-qdrant         Up (healthy)  ✅
mem0g-backend        Up (healthy)  ✅
mem0g-frontend       Up            ✅
```

---

### [ ] 11단계: 백엔드 연결 확인
```bash
curl http://localhost:8000/api/admin/health
```

**성공 시:**
```json
{
  "status": "healthy",
  "services": {
    "mem0": "connected",
    "graph_db": "connected"
  }
}
```

---

### [ ] 12단계: Ollama 설정 확인
```bash
curl http://localhost:8000/api/admin/config | grep ollama
```

**확인 사항:**
- `ollama_base_url`: 올바른 IP
- `ollama_llm_model`: "qwen2.5:7b"
- `ollama_embedding_model`: "bge-m3"

---

### [ ] 13단계: 웹 UI 접속

**브라우저에서:**
```
http://localhost:3000
```

**확인:**
- ✅ API 연결됨 표시
- ✅ 채팅 탭 보임
- ✅ 그래프 탭 보임
- ✅ 메모리 탭 보임
- ✅ 테스트 탭 보임

---

### [ ] 14단계: 최종 테스트

**채팅 탭에서:**
```
안녕하세요, 테스트 메시지입니다
```

**전송 버튼 클릭**

✅ **성공:** AI가 응답
❌ **실패:** 로그 확인
```bash
docker-compose logs backend | tail -50
```

---

## 🔧 문제 해결 빠른 가이드

### ❌ "Connection refused"
```bash
# Ollama 서버 PC에서
ping localhost
curl http://localhost:11434/api/version

# Ollama 재시작
pkill ollama
OLLAMA_HOST=0.0.0.0:11434 ollama serve &
```

### ❌ "Model not found"
```bash
# Ollama 서버 PC에서
ollama list
ollama pull qwen2.5:7b
ollama pull bge-m3
```

### ❌ "Timeout"
```bash
# 방화벽 확인 (Ollama 서버 PC)
sudo ufw status
sudo ufw allow 11434/tcp

# 네트워크 연결 확인 (Docker PC)
ping 192.168.1.100
telnet 192.168.1.100 11434
```

---

## 📊 설정 요약

완료된 설정:

| 항목 | 값 | 확인 |
|------|------|------|
| **Ollama 서버 IP** | ___________________ | [ ] |
| **모델 다운로드** | qwen2.5:7b, bge-m3 | [ ] |
| **방화벽 11434** | 허용됨 | [ ] |
| **.env 파일** | IP 설정됨 | [ ] |
| **Docker 실행** | 4개 서비스 Up | [ ] |
| **헬스체크** | healthy | [ ] |
| **Web UI** | 접속 가능 | [ ] |
| **채팅 테스트** | 정상 응답 | [ ] |

---

## 🎉 모든 체크 완료!

✅ 14/14 단계 완료

**다음 할 일:**
- [EXAMPLES.md](./EXAMPLES.md)에서 다양한 예제 테스트
- [QUICKSTART.md](./QUICKSTART.md)의 7단계부터 진행

**고급 설정:**
- [EXTERNAL_OLLAMA.md](./EXTERNAL_OLLAMA.md) 참조

---

## 💡 유용한 명령어

```bash
# 로그 실시간 보기
docker-compose logs -f backend

# 서비스 재시작
docker-compose restart backend

# 전체 재시작
docker-compose down && docker-compose up -d

# IP 변경 시
nano .env
docker-compose restart backend

# Ollama 서버 상태 (Ollama PC에서)
ollama list
ps aux | grep ollama
```

---

**준비 완료!** 🚀

이제 http://localhost:3000 에서 Mem0g를 테스트하세요!
