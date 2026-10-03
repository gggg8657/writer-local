name: season
title: 연말·연초 인사말
category: 개인
description: 송년·신년 메시지 (메신저·카드·부서장 인사)
outputs: 3
inputs:
  - key: when
    label: 시기
    type: select
    options: [연말, 신년, 추석, 설]
  - key: to
    label: 받는 사람
    type: select
    options: [부서원 전체, 상사, 협력기관, 지인 한 명]
  - key: year_note
    label: 올해 있었던 일 한 가지
    type: text
  - key: length
    label: 길이
    type: select
    options: [두 문장, 카드 한 장, 부서장 인사 1분]
---
시기 인사말을 쓴다. "다사다난", "희망찬 새해" 같은 관용구 금지. 올해 있었던 일 한 가지를 짚고, 받는 사람에게 구체적인 바람 하나. 3안은 톤 다르게(담백 / 따뜻 / 유쾌).
