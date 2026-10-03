name: intro
title: 자기소개
category: 개인
description: 부서 발표·첫 회의에서 하는 자기소개
outputs: 2
inputs:
  - key: name
    label: 이름·직함
    type: text
    required: true
  - key: work
    label: 하는 일·경력
    type: textarea
    required: true
  - key: personal
    label: 사적인 한 가지 (취미 등, 선택)
    type: text
  - key: length
    label: 길이
    type: select
    options: [30초, 1분]
---
자기소개를 쓴다. 이름 → 지금 하는 일(한 문장) → 이전에 한 일 중 지금 일과 이어지는 것 하나 → 사적인 한 가지(있으면) → 도움 요청·협업 바람 한 문장. 자화자찬 금지.
