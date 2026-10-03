name: farewell
title: 송사·환송사
category: 행사
description: 퇴직·전출하는 분을 보내며 하는 말
outputs: 2
inputs:
  - key: to
    label: 떠나는 분 (이름·직함)
    type: text
    required: true
  - key: reason
    label: 사유
    type: select
    options: [정년퇴임, 전출·파견, 이직, 명예퇴직, 부서 이동]
  - key: years
    label: 함께한 기간·일화
    type: textarea
    placeholder: 예) 7년, ○○ 과제 밤샘, 늘 먼저 출근
  - key: length
    label: 길이
    type: select
    options: [1분, 2분, 메시지 카드]
---
환송사를 쓴다. 일화 하나를 중심에 두고, 그 사람이 남긴 것 한 가지, 앞날에 대한 바람 한 가지. 눈물 유도 금지, 담담하게. 길이 "메시지 카드"는 4~5문장.
