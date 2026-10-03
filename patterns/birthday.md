name: birthday
title: 생일 축하 메시지
category: 개인
description: 동료 생일 메신저·카드
outputs: 3
inputs:
  - key: to
    label: 받는 사람 (이름, 관계)
    type: text
    required: true
  - key: trait
    label: 그 사람 특징·고마운 점 하나
    type: text
  - key: mood
    label: 분위기
    type: select
    options: [담백, 유쾌, 정중]
---
생일 메시지를 쓴다. 1~3문장. 특징·고마운 점이 있으면 그걸 중심으로. 이모지 없이. 3안.
