name: broadcast
title: 사내 방송 멘트
category: 공문
description: 구내 방송·안내 멘트 (읽는 원고)
outputs: 2
inputs:
  - key: what
    label: 안내 내용
    type: textarea
    required: true
  - key: when
    label: 시각·일정
    type: text
  - key: repeat
    label: 반복 여부
    type: select
    options: [1회, 2회 반복]
---
방송 멘트를 쓴다. 귀로 듣는 글: 짧은 문장, 숫자는 또박또박(14시 → 오후 두 시), 핵심을 먼저 말하고 마지막에 한 번 더 요약. "안내 말씀 드립니다."로 시작, "감사합니다."로 끝. 2회 반복이면 두 번째는 요약본.
