#!/usr/bin/env python3
"""LLM 없이 검증: 패턴 로더 → 폼 스키마 → 가짜 LLM 안 분리 → CLI.  python3 selftest.py"""
import json
import os
import subprocess
import sys
import app

# 1) 패턴 전부 파싱됨, 이름 유일, 필수 필드
assert len(app.PATTERNS) >= 14, len(app.PATTERNS)
for p in app.PATTERNS.values():
    assert p["prompt"] and p["inputs"] and p["category"] in ("모임", "경조사", "행사", "공문", "개인"), p["name"]
    for i in p["inputs"]:
        assert i["type"] in ("text", "textarea", "select", "number"), i
        if i["type"] == "select":
            assert i.get("options"), i
json.dumps([{k: v for k, v in p.items() if k != "prompt"} for p in app.PATTERNS.values()])  # /api/patterns 직렬화

# 2) 가짜 LLM: 3안 분리, 입력값이 프롬프트에 들어감, 필수 입력 검사
seen = {}
def fake(system, user, model, on_token=None):
    seen["system"], seen["user"] = system, user
    out = "첫째 안\n=====\n둘째 안\n=====\n셋째 안"
    if on_token: on_token(out)
    return "```\n" + out + "\n```"
app.ollama = fake
r = app.generate("toast", {"occasion": "송년회", "mood": "유쾌하게", "length": "30초", "note": "김철수 환영"}, "fake")
assert r["variants"] == ["첫째 안", "둘째 안", "셋째 안"], r["variants"]
assert "김철수 환영" in seen["user"] and "건배사" in seen["system"] and "=====" in seen["system"]
r = app.generate("recommend", {"who": "홍길동", "strengths": "꼼꼼함"}, "fake")
assert len(r["variants"]) == 1 and "=====" in r["variants"][0]  # outputs:1 이면 분리 안 함
try:
    app.generate("speech", {"role": "부서장"}, "fake"); assert False
except ValueError as e:
    assert "행사명" in str(e)
r = app.generate("toast", {"occasion": "송년회"}, "fake", tweak="shorter", prev="이전 결과")
assert "절반" in seen["user"] and "이전 결과" in seen["user"]

# 3) CLI
env = dict(os.environ, LLM_BASE_URL="http://127.0.0.1:9")  # 연결 불가 → 에러로 끝나야 정상 경로 확인
out = subprocess.run([sys.executable, "app.py", "--cli", "nope"], capture_output=True, text=True, cwd=app.ROOT, env=env)
assert "패턴 없음" in out.stderr

print("selftest OK —", len(app.PATTERNS), "patterns, runs:", [x["run_id"] for x in app.list_runs()[:2]])
