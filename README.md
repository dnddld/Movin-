
# 🎬 AI 기반 캐릭터의 영화 추천 시스템 🎬

GPT와 TMDB API를 활용하여, 영화 속 캐릭터의 시선으로 영화를 추천받는 커뮤니티 서비스입니다.

---
## 프로젝트 실행 방법
```bash
# Backend
$ cd backend
$ python -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py loaddata genre.json
$ python manage.py load_actors
$ python manage.py load_movies
$ python manage.py runserver

#Frontend
$ cd frontend
$ npm i
$ npm run dev

#.env에 해당하는 API Key 입력
backend/.env #OPENAI_API_KEY
frontend/.env #VITE_TMDB_API_KEY,VITE_YOUTUBE_API_KEY,VITE_API_URL=http://localhost:8000
```


## 👥 팀원 정보 및 업무 분담

| 이름     | 역할         | 주요 담당 |
|----------|--------------|-----------|
| [정의환](https://github.com/justicehwan)   | 팀장, 프론트엔드 | Vue.js 기반 전체 UI/UX 개발, 상태관리(Pinia), API 연동, GPT 추천 결과 시각화 |
| [최지웅](https://github.com/dnddld)   | 팀원, 백엔드     | Django 서버 구축, 모델링 및 DB 설계, REST API 개발, OpenAI 통신 로직 구현 |
---

## 🎯 목표 서비스 구현 및 실제 구현 정도

### 목표
- 캐릭터를 선택하면 해당 인물의 가치관 및 성격에 맞는 영화를 추천
- 캐릭터를 선택하면 해당 캐릭터가 우측 하단에 나타나며 챗봇 기능 및 사이트 어시스턴트 기능
- 추천 결과를 GPT 기반 자연어 분석으로 생성
- 추천/비추천 영화 각각에 대해 이유와 점수를 출력
- 사용자 간 팔로우, 리뷰, 좋아요, 북마크 기능 제공
- 영화 관련 미니게임 제공

### 실제 구현 완료 목록
- TMDB 영화 10,000편 DB 구축
- 사용자 회원가입/로그인 및 마이페이지, 프로필 페이지 구현
- 리뷰/좋아요/북마크 기능 완전 구현
- 캐릭터 선택 → GPT 추천 결과 생성 및 출력 완료
- 캐릭터별 추천 영화 10편 + 비추천 영화 5편 JSON 파싱 완료

---

## 🗂 설계
- [ERD](https://github.com/user-attachments/assets/8b437916-c091-4fe3-9db8-15d85aaaaeaa)
- [REST API](https://github.com/user-attachments/assets/4176dbcd-f478-47d4-9fe2-5226427d815a)



---

## 🧠 영화 추천 알고리즘 (GPT 기반)

### 🎭 입력
사용자가 선택한 캐릭터 (예: '어벤져스 - 아이언맨')

### 🧾 프롬프트 예시
```text
당신은 '어벤져스 - 아이언맨' 캐릭터입니다.

다음 조건에 따라 '어벤져스 - 아이언맨'의 관점에서 영화 추천을 해주세요:

- 반드시 **실제로 존재하는 영화**만 추천하세요.
- 추천 영화는 **TMDB에 등록된 영화**여야 하며, **한글 제목으로** 응답하세요.
- **영문 제목이 아닌, TMDB에서 사용하는 한국어 제목**을 그대로 써 주세요.
- 존재하지 않는 영화나 가상의 영화는 절대 포함하지 마세요.
- 추천 영화는 TMDB에 등록된 영화 제목과 일치해야 합니다.
- 당신이 좋아할 만한 영화 10개를 추천하세요 (Top 10)
- 각 영화의 추천 이유를 8줄로 서술하세요
- 각 영화에 대해 10점 만점 기준의 평점을 부여하세요 (정수로 표현하세요)
- 당신이 싫어할 영화도 5개 추천하세요 (Bottom 5)
- 각 비추천 영화에 대해서도 8줄로 설명하세요
- 작성 어투를 진짜 영화 속 당신의 말투 처럼 바꿔서 설명을 적어주세요 (나이나 살았던 시대의 말투도 반영하세요)
- 비어 있거나, 값이 없거나, 문법이 틀린 JSON 응답 을 절대 작성하지 마세요

응답은 아래와 같은 JSON 형식으로만 출력하세요. 주석이나 설명은 절대 포함하지 마세요:
{{
  "top": [
    {{ "title": "한글 영화 제목", "score": 9, "reason": "추천 이유 8줄" }},
    ... (10개)
  ],
  "bottom": [
    {{ "title": "한글 영화 제목", "score": 2, "reason": "비추천 이유 8줄" }},
    ... (5개)
  ]
}}
```

### 📤 출력
GPT는 JSON 형식으로 Top 10 / Bottom 5 리스트 응답  

→ 프론트에서 탭 형태로 파싱 및 시각화하여 표시

![추천예](/uploads/7b21cc65f7cdc0e59488d2409135f3c9/추천예.png)
---

## 💡 핵심 기능

- **캐릭터 기반 영화 추천**  
  사용자가 선택한 캐릭터 입장에서 영화를 추천하는 완전히 새로운 UX

- **TMDB 기반 대규모 영화 데이터 관리**  
  20,000편 이상의 영화, 장르, 배우 데이터 구축

- **리뷰 및 평가 시스템**  
  사용자 리뷰, 별점 평가, 좋아요, 정렬 기능 지원

- **유저 커뮤니티 기능**  
  프로필 방문, 좋아요/북마크한 영화 열람

- **동적 추천 UI**  
  GPT 응답 JSON 파싱 후 Vue 컴포넌트로 실시간 추천 출력

---

## 🤖 생성형 AI 활용

- OpenAI GPT-4o-mini API 사용
- 캐릭터 말투와 성격 반영된 영화 평가 텍스트 생성
- GPT 응답은 JSON 포맷 강제 → 구조화된 데이터로 파싱 가능
- 실제 TMDB에 등록된 한글 영화 제목만 추천하도록 필터링된 프롬프트 작성

---

## 💬 느낀점 및 후기


> Django ORM으로 대규모 데이터를 관리하면서 성능과 정합성을 유지하는 법을 배웠고, TMDB API와 OpenAI GPT API를 동시에 다루며 외부 API 통신과 보안 처리도 경험했습니다. 특히 GPT의 출력 형태를 JSON으로 강제하고 구조화된 데이터를 받기 위해 프롬프트 튜닝을 반복했고, 프론트엔드와의 통신 구조를 협업하면서 RESTful 설계와 명확한 응답 포맷의 중요성을 느꼈습니다. 사용자 인증, 리뷰 좋아요 등도 실용적인 기능으로 안정적으로 구현했습니다.

---

## 🛠 기술 스택

- **Frontend**: Vue.js 3, Pinia, Bootstrap, Axios
- **Backend**: Django, Django REST Framework, SQLite
- **AI 추천**: OpenAI GPT-4o-mini
- **데이터**: TMDB API 기반 영화/배우/장르
- **개발툴**: VSCode, Postman

---

## 📞 사용 API
- OpenAI API
- TMDB API
- Youtube Data API
