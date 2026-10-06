# writer-local — 건배사·경조사·축사·공지를 패턴으로 쓰는 로컬 LLM 글쓰기

> **한 줄 요약** — 직장에서 자주 쓰지만 매번 막막한 글(건배사·경조사 문구·축사·환송사·감사 편지·추천서·공지·사과문·방송 멘트 등 17종)을
> "패턴 = 마크다운 파일 하나"로 묶어 로컬 LLM이 써 주는 패키지입니다. [Fabric](https://github.com/danielmiessler/Fabric)의 패턴 방식을
> 공공기관·연구소 한국어 글쓰기에 맞춰 새로 썼고, 파이썬 표준 라이브러리만 써서 폴더 복사로 배포됩니다. 폼에 사실만 넣으면 여러 안이 나오고,
> "더 짧게·더 격식·더 캐주얼" 버튼으로 고치며, humanize-kr-local 이 떠 있으면 "AI 티 제거"까지 한 번에 됩니다.
>
> - **의존성**: 없음. Python 3.9+.
> - **패턴 추가**: `patterns/이름.md` 한 파일 추가하면 끝(아래 참고). 코드 수정 없음.
> - **모델**: 한국어 되는 아무거나. Ollama·vLLM 등 OpenAI 호환 서버를 환경변수로 전환.

## 실행

```bash
bash setup.sh                     # OS 감지 → Python → LLM 탐색/세팅 → selftest → http://localhost:8773
python3 app.py                    # 수동
LLM_API=openai LLM_BASE_URL=http://gpu:8000/v1 LLM_MODEL=Qwen3-32B python3 app.py
python3 app.py --cli toast occasion=송년회 mood=유쾌하게 length=30초 "note=신입 김민수 환영"
python3 selftest.py               # LLM 없이 패턴 로더·안 분리·CLI 검증
```

| 환경변수 | 기본 | 설명 |
|---|---|---|
| `LLM_API` | `ollama` | `ollama` 또는 `openai` |
| `LLM_BASE_URL` | `http://localhost:11434` / `http://localhost:8000/v1` | 서버 주소 |
| `LLM_MODEL` | `qwen3:8b` | 기본 모델 (UI에서 변경 가능) |
| `LLM_API_KEY` | (없음) | OpenAI 호환 서버 키 |
| `NUM_CTX` | `8192` | Ollama 컨텍스트 |
| `HUMANIZE_URL` | `http://localhost:8765` | humanize-kr-local 서버. 떠 있으면 "AI 티 제거" 버튼 활성 |
| `PORT` | `8773` | |

## 패턴 (17)

모임: 건배사 · 회식/행사 안내문 — 경조사: 축하 문구 · 조의 문구 — 행사: 축사 · 송사/환송사 · 환영사 · 발표 오프닝 — 공문: 추천서 · 사내 공지 · 사과문 · 방송 멘트 — 개인: 수상 소감 · 감사 편지 · 자기소개 · 연말연초 인사 · 생일 메시지

## 패턴 추가

`patterns/xxx.md`:

```
name: xxx            # 고유 이름 (CLI 에서 씀)
title: 제목
category: 모임|경조사|행사|공문|개인
description: 한 줄 설명
outputs: 3           # 안 개수
inputs:
  - key: occasion
    label: 모임 성격
    type: select     # text | textarea | select | number
    options: [회식, 송년회]
  - key: note
    label: 넣고 싶은 말
    type: text
    placeholder: 예) …
    required: true
---
여기부터 이 패턴의 지시문(시스템 프롬프트). 공통 규칙은 goal-prompt.md 에 있어 반복할 필요 없음.
```

결과는 `_workspace/<run>.json` 에 남고 UI 하단 기록에서 다시 불러올 수 있습니다.

### ✍ 윤문하기
결과 아래에 "윤문하기" 막대(가볍게·보통·적극). kordoc-local 의 글 윤문 API(`KORDOC_URL`, 기본 `http://localhost:8766`)를 부르며, kordoc 이 안 떠 있으면 막대가 숨는다. 숫자·날짜·고유 표기가 바뀐 곳은 원문 유지, "바뀐 곳 보기"로 어절 단위 비교.
