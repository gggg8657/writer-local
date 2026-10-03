name: award
title: 수상 소감
category: 개인
description: 상 받을 때 하는 짧은 소감
outputs: 3
inputs:
  - key: award
    label: 상 이름
    type: text
    required: true
  - key: why
    label: 수상 사유·한 일
    type: textarea
    required: true
  - key: thanks
    label: 감사할 사람
    type: text
    placeholder: 예) 팀원 3명, 부서장, 가족
  - key: length
    label: 길이
    type: select
    options: [30초, 1분, 서면 3문장]
---
수상 소감을 쓴다. 겸손 과잉("부족한 제가") 금지. 한 일을 한 문장으로 사실대로, 감사는 이름을 넣어 구체적으로, 다음에 할 일 한 문장. 3안은 시작 문장을 다르게.
