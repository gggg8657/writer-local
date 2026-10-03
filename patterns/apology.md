name: apology
title: 사과문
category: 공문
description: 실수·지연·사고에 대한 사과
outputs: 2
inputs:
  - key: what
    label: 무슨 일이 있었나
    type: textarea
    required: true
  - key: to
    label: 사과 대상
    type: text
    required: true
  - key: fix
    label: 조치·재발 방지
    type: textarea
  - key: form
    label: 형식
    type: select
    options: [이메일, 메신저, 공식 문서]
---
사과문을 쓴다. 순서: 무엇을 잘못했는지 명확히(변명 없이) → 영향받은 분께 사과 → 한 조치와 앞으로의 조치 → 연락처·후속 안내. "불편을 드려 죄송" 같은 뭉뚱그린 표현 대신 구체적 사실. 책임 회피 문장 금지.
