name: thanks
title: 감사 편지
category: 개인
description: 도움 준 사람·기관에 보내는 감사 글
outputs: 2
inputs:
  - key: to
    label: 받는 분
    type: text
    required: true
  - key: what
    label: 어떤 도움이었나
    type: textarea
    required: true
  - key: result
    label: 그 덕에 어떻게 됐나
    type: text
  - key: form
    label: 형식
    type: select
    options: [이메일, 손편지, 메신저]
---
감사 편지를 쓴다. 무엇을 해 줬는지와 그 결과를 구체적으로 적는 것이 전부다. 과한 수식 금지. 이메일이면 제목 줄 포함, 손편지면 날짜·이름 자리, 메신저면 3문장 이내.
