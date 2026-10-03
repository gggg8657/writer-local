name: speech
title: 축사
category: 행사
description: 행사에서 역할자로 하는 축사 원고
outputs: 2
inputs:
  - key: event
    label: 행사명
    type: text
    required: true
    placeholder: 예) 2026 원자력 안전 워크숍 개회식
  - key: role
    label: 내 역할
    type: select
    options: [부서장, 기관 대표 대독, 주관 부서 담당, 초청 인사]
  - key: audience
    label: 청중
    type: text
    placeholder: 예) 연구원·외부 참석자 150명
  - key: minutes
    label: 길이(분)
    type: number
    placeholder: 2
  - key: points
    label: 꼭 넣을 내용
    type: textarea
    placeholder: 예) 올해 3회째, 참여 기관 12곳, 감사할 사람
---
축사 원고를 쓴다. 분당 300자 기준으로 길이를 맞춘다. 구조: 인사와 자리 확인(짧게) → 행사의 의미를 구체적 사실 하나로 → 참석자·준비한 사람에게 감사 → 바라는 점 한 가지 → 마무리 인사. 미사여구 대신 "꼭 넣을 내용"의 사실을 쓴다. 2안은 격식 정도를 달리.
