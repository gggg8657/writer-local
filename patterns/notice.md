name: notice
title: 사내 공지문
category: 공문
description: 게시판·메신저용 공지
outputs: 2
inputs:
  - key: title
    label: 제목
    type: text
    required: true
  - key: body
    label: 내용 (사실만)
    type: textarea
    required: true
  - key: when
    label: 일정
    type: text
    placeholder: 예) 2026. 10. 15.(수) 14:00
  - key: to
    label: 대상
    type: text
    placeholder: 예) 전 직원 / ○○부 연구원
  - key: action
    label: 요청 사항
    type: text
    placeholder: 예) 10. 10.까지 설문 제출
---
공지문을 쓴다. 첫 줄 제목, 둘째 줄부터 본문. 결론(무엇을·언제·누가) 먼저, 이유는 그다음. 항목이 셋 이상이면 "-" 목록. 날짜 표기는 2026. 10. 15.(수) 꼴. 요청 사항은 마지막 줄에 "~해 주시기 바랍니다."로. 2안은 하나는 게시판용(격식), 하나는 메신저용(짧게).
