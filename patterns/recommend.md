name: recommend
title: 추천서 초안
category: 공문
description: 포상·진학·이직·과제 참여용 추천서
outputs: 1
inputs:
  - key: who
    label: 피추천인 (이름·직함·소속)
    type: text
    required: true
  - key: relation
    label: 추천인과의 관계·기간
    type: text
    placeholder: 예) 3년간 같은 과제 수행, 직속 상급자
  - key: strengths
    label: 강점과 근거 사례
    type: textarea
    required: true
  - key: purpose
    label: 용도
    type: select
    options: [포상 추천, 대학원 진학, 이직·채용, 과제 책임자 선정, 해외 연수]
  - key: length
    label: 길이
    type: select
    options: [반 쪽, 한 쪽]
---
추천서 초안을 쓴다. 구조: 추천인과 피추천인의 관계(사실) → 강점 2~3개, 각각 근거 사례 하나 → 용도에 맞는 적합성 → 추천 문장. 형용사 나열 금지, 사례가 형용사를 대신한다. 맨 아래 날짜·추천인 서명 자리(○○○).
