name: invite
title: 회식·행사 안내문
category: 모임
description: 참석 독려하는 안내
outputs: 2
inputs:
  - key: what
    label: 무슨 모임
    type: text
    required: true
    placeholder: 예) 하반기 부서 회식
  - key: when
    label: 일시
    type: text
    required: true
  - key: where
    label: 장소
    type: text
  - key: cost
    label: 비용·회비
    type: text
    placeholder: 예) 부서 경비 / 1인 2만원
  - key: rsvp
    label: 참석 회신 방법·기한
    type: text
---
안내문을 쓴다. 일시·장소·비용·회신을 보기 좋게 줄 단위로, 앞에 한두 문장만 가볍게. 강요하는 말투 금지("필참" 대신 "가능하신 분은"). 2안 중 하나는 더 짧게.
