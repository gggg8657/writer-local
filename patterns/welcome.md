name: welcome
title: 환영사
category: 행사
description: 신입·전입 직원을 맞는 말
outputs: 2
inputs:
  - key: to
    label: 새로 온 분 (이름·직함, 여러 명 가능)
    type: text
    required: true
  - key: kind
    label: 구분
    type: select
    options: [신입, 경력 입사, 전입·전보, 파견]
  - key: dept
    label: 부서와 하는 일
    type: text
    placeholder: 예) 열수력안전연구부, 실험장치 운영
  - key: length
    label: 길이
    type: select
    options: [한두 문장, 1분, 메신저 공지]
---
환영사를 쓴다. 부서가 하는 일을 한 줄로, 새 사람에게 기대하는 것보다 "도움 요청하라"는 메시지를 먼저. 선배 티 금지. "메신저 공지"면 부서 전체에 알리는 형식(이름·역할·자리·첫날 일정 자리 비워 두기 ○○).
