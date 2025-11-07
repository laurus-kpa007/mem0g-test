# 📚 Mem0g 테스트 플랫폼 - 실전 예제 모음

다양한 사용 시나리오와 예제를 통해 Mem0g의 강력함을 경험해보세요!

---

## 🎯 기본 예제

### 예제 1: 개인 정보 저장

**입력:**
```
나는 김철수이고, 서울 강남구에 살고 있어요.
직업은 소프트웨어 개발자이고, Python과 JavaScript를 주로 사용합니다.
```

**추출되는 정보:**
- **엔티티**:
  - 김철수 (Person)
  - 서울 강남구 (Place)
  - 소프트웨어 개발자 (Occupation)
  - Python (Technology)
  - JavaScript (Technology)

- **관계**:
  - 김철수 → lives_in → 서울 강남구
  - 김철수 → works_as → 소프트웨어 개발자
  - 김철수 → uses → Python
  - 김철수 → uses → JavaScript

**검색 테스트:**
- "강남에 사는 개발자는?" → 김철수 찾기
- "Python 쓰는 사람은?" → 김철수 찾기

---

### 예제 2: 인간 관계 네트워크

**입력 시퀀스:**

**1단계:**
```
Alice는 Bob의 동료입니다.
```

**2단계:**
```
Bob은 Charlie의 상사이고, 둘 다 구글에서 일해요.
```

**3단계:**
```
Charlie는 Diana와 결혼했습니다.
```

**생성되는 그래프:**
```
Alice ---[colleague]---> Bob
  ↓                       ↓
[works_at]          [works_at]
  ↓                       ↓
Google <---- [works_at] --- Bob
                           ↓
                     [manager_of]
                           ↓
                       Charlie ---[married_to]---> Diana
                           ↓
                      [works_at]
                           ↓
                        Google
```

**검색 테스트:**
- "구글에서 일하는 사람들은?" → Alice, Bob, Charlie
- "Bob의 부하 직원은?" → Charlie
- "Charlie의 배우자는?" → Diana

---

### 예제 3: 이벤트와 시간

**입력:**
```
2024년 3월에 팀 워크샵을 제주도에서 했어요.
참석자는 Alice, Bob, Charlie였고, 프로젝트 킥오프 미팅도 진행했습니다.
```

**추출 정보:**
- **엔티티**:
  - 팀 워크샵 (Event)
  - 제주도 (Place)
  - Alice, Bob, Charlie (Person)
  - 프로젝트 킥오프 미팅 (Event)

- **시간 정보**: 2024년 3월

- **관계**:
  - 워크샵 → held_at → 제주도
  - Alice → attended → 워크샵
  - Bob → attended → 워크샵
  - Charlie → attended → 워크샵

**검색 테스트:**
- "제주도 이벤트는?" → 팀 워크샵
- "워크샵 참석자는?" → Alice, Bob, Charlie
- "2024년 3월에 뭐 했지?" → 팀 워크샵, 킥오프 미팅

---

## 🔥 고급 예제

### 예제 4: 다단계 추론

**입력 시퀀스:**

**대화 1:**
```
서울에는 강남구, 종로구, 마포구가 있어요.
```

**대화 2:**
```
강남구에 삼성역, 역삼역이 있고, 종로구에는 광화문이 있어요.
```

**대화 3:**
```
Alice는 삼성역 근처 스타벅스에서 일해요.
```

**가능한 추론:**
- Alice는 강남구에서 일한다
- Alice의 직장은 서울에 있다
- Alice는 역삼역에서도 가깝다

**검색 테스트:**
```
질문: "서울에서 일하는 사람은?"
→ Alice (간접 추론)

질문: "스타벅스 직원은?"
→ Alice

질문: "강남구에 있는 장소는?"
→ 삼성역, 역삼역, Alice의 직장
```

---

### 예제 5: 모순 감지

**입력 1:**
```
Bob은 채식주의자입니다.
```

**입력 2 (나중에):**
```
Bob은 오늘 점심으로 삼겹살을 먹었어요.
```

**Mem0g의 동작:**
- 두 메모리 모두 저장
- 검색 시 최신 정보 우선
- 시간적 문맥 유지

**검색 결과:**
```
질문: "Bob의 식습관은?"
→ [최근] Bob은 삼겹살을 먹었다
→ [과거] Bob은 채식주의자다
```

---

### 예제 6: 복잡한 비즈니스 시나리오

**입력:**
```
우리 회사는 Acme Corp이고 CEO는 John Smith입니다.
서울 본사와 부산 지사가 있어요.
서울에는 개발팀과 디자인팀이 있고, 부산에는 영업팀이 있습니다.
개발팀 팀장은 Alice이고, 팀원으로 Bob과 Charlie가 있어요.
```

**생성되는 구조:**
```
Acme Corp
  ↓ [CEO]
John Smith
  ↓
[has_office]
  ├─→ 서울 본사
  │     ↓ [has_team]
  │     ├─→ 개발팀 (팀장: Alice, 팀원: Bob, Charlie)
  │     └─→ 디자인팀
  └─→ 부산 지사
        ↓ [has_team]
        └─→ 영업팀
```

**복잡한 검색:**
```
"Alice의 상사는?" → John Smith (CEO)
"서울에서 일하는 개발자는?" → Alice, Bob, Charlie
"Acme Corp의 조직 구조는?" → 전체 그래프 반환
"Bob은 어느 팀?" → 개발팀
"개발팀은 어디 있어?" → 서울
```

---

## 🌍 다국어 예제

### 예제 7: 한영 혼합

**입력:**
```
Alice는 Google에서 Software Engineer로 일하고,
주요 skill은 Machine Learning과 딥러닝입니다.
```

**추출:**
- Alice (Person)
- Google (Organization)
- Software Engineer (Occupation)
- Machine Learning (Skill)
- 딥러닝 (Skill)

---

## 🧪 성능 테스트 예제

### 예제 8: 대량 데이터

**스크립트로 여러 대화 입력:**

```python
messages = [
    "Alice는 Bob의 친구다",
    "Bob은 Charlie를 알고 있다",
    "Charlie는 Diana와 같은 회사에 다닌다",
    # ... 100개 메시지
]

for msg in messages:
    # POST /api/chat
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": msg, "user_id": "test_user"}
    )
```

**벤치마크 결과:**
```
총 메시지: 100개
평균 처리 시간: 1.2초/메시지
그래프 노드 수: 150개
관계 수: 120개
```

---

## 🎨 실전 활용 시나리오

### 시나리오 1: 고객 관리 (CRM)

**대화 기록:**
```
고객: 저는 김영희입니다. 지난번에 A 제품을 구매했었는데...
상담원: [시스템이 자동으로 기억]
  - 고객명: 김영희
  - 구매 이력: A 제품
  - 이전 대화 기록 검색
```

### 시나리오 2: 의료 기록

**의사 노트:**
```
환자 홍길동, 고혈압 진단.
Lisinopril 10mg 처방, 식이요법 권고.
다음 방문: 2주 후
```

**자동 추출:**
- 환자: 홍길동
- 진단: 고혈압
- 처방: Lisinopril 10mg
- 치료: 식이요법
- 일정: 2주 후 재방문

### 시나리오 3: 학습 노트

**학생의 학습 기록:**
```
오늘은 Python의 decorators를 배웠어.
특히 @staticmethod와 @classmethod의 차이를 이해했고,
실전 예제로 로깅 decorator를 만들어봤다.
```

**지식 그래프:**
```
Python
  ↓
decorators
  ├─→ @staticmethod
  ├─→ @classmethod
  └─→ 실전 예제
        └─→ 로깅 decorator
```

---

## 🔬 API 직접 호출 예제

### cURL 예제

#### 1. 메모리 추가
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "나는 서울에 살아요",
    "user_id": "user_123"
  }'
```

#### 2. 메모리 검색
```bash
curl -X POST http://localhost:8000/api/memories/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "서울",
    "user_id": "user_123",
    "limit": 10
  }'
```

#### 3. 그래프 통계
```bash
curl http://localhost:8000/api/graph/stats?user_id=user_123
```

#### 4. 벤치마크
```bash
curl http://localhost:8000/api/test/benchmark
```

### Python 예제

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. 대화 저장
def send_message(message, user_id):
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "message": message,
            "user_id": user_id
        }
    )
    return response.json()

# 2. 메모리 검색
def search_memories(query, user_id):
    response = requests.post(
        f"{BASE_URL}/api/memories/search",
        json={
            "query": query,
            "user_id": user_id,
            "limit": 10
        }
    )
    return response.json()

# 사용 예
user_id = "alice_123"

# 여러 대화 저장
messages = [
    "나는 Alice이고 서울에 살아요",
    "Python 개발자로 일하고 있습니다",
    "취미는 등산과 독서예요"
]

for msg in messages:
    result = send_message(msg, user_id)
    print(f"저장됨: {result['message']}")

# 검색
results = search_memories("Alice의 취미", user_id)
print(f"검색 결과: {results}")
```

### JavaScript 예제

```javascript
const BASE_URL = 'http://localhost:8000';

// 1. 메시지 전송
async function sendMessage(message, userId) {
  const response = await fetch(`${BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      user_id: userId
    })
  });
  return response.json();
}

// 2. 메모리 검색
async function searchMemories(query, userId) {
  const response = await fetch(`${BASE_URL}/api/memories/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: query,
      user_id: userId,
      limit: 10
    })
  });
  return response.json();
}

// 사용 예
(async () => {
  const userId = 'bob_456';

  // 메시지 저장
  await sendMessage('나는 부산에 살아요', userId);
  await sendMessage('좋아하는 음식은 해물파전이에요', userId);

  // 검색
  const results = await searchMemories('부산', userId);
  console.log('검색 결과:', results);
})();
```

---

## 🎓 학습 팁

### 팁 1: 명확한 문장 사용
❌ **나쁜 예:**
```
그거 있잖아, 저번에 말한 그거...
```

✅ **좋은 예:**
```
지난주에 강남역에서 만난 김철수씨...
```

### 팁 2: 관계 명시
❌ **나쁜 예:**
```
Alice, Bob
```

✅ **좋은 예:**
```
Alice는 Bob의 동료입니다
```

### 팁 3: 구체적인 정보 제공
❌ **나쁜 예:**
```
그는 개발자다
```

✅ **좋은 예:**
```
김철수는 Python 백엔드 개발자이고 5년 경력이다
```

---

## 📊 예상 결과

### 처리 시간
- 짧은 문장 (10-20단어): 0.5-1초
- 중간 문장 (30-50단어): 1-2초
- 긴 문장 (100단어 이상): 2-5초

### 정확도
- 명확한 엔티티: 95%+
- 복잡한 관계: 80-90%
- 다단계 추론: 70-85%

---

## 🚀 도전 과제

스스로 테스트해보세요!

### 🥉 초급
1. 자신의 프로필 저장하기
2. 3명의 친구 관계 만들기
3. 검색으로 친구 찾기

### 🥈 중급
1. 회사 조직도 만들기 (5명 이상)
2. 시간 정보 포함한 이벤트 저장
3. Neo4j에서 그래프 시각화

### 🥇 고급
1. 100개 이상의 대화 저장
2. 다단계 추론 쿼리 성공시키기
3. API를 사용한 자동화 스크립트 작성

---

**즐거운 테스팅 되세요!** 🎉

더 많은 예제가 필요하시면 GitHub Issues에 요청해주세요!
