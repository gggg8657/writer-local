#!/usr/bin/env python3
"""writer local — Fabric 스타일 패턴 글쓰기 (건배사·경조사·축사·공지 …). 로컬 LLM, 외부 의존성 없음(stdlib).

  python3 app.py                                    # http://localhost:8773
  LLM_API=openai LLM_BASE_URL=http://gpu:8000/v1 LLM_MODEL=Qwen3-32B python3 app.py
  python3 app.py --cli toast occasion=송년회 mood=유쾌하게 length=30초

패턴은 patterns/*.md 한 파일 = 한 패턴 (frontmatter: name/title/category/description/outputs/inputs, 본문 = 지시문).
"""
import datetime
import json
import os
import re
import secrets
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
WS = os.path.join(ROOT, "_workspace")
LLM_API = os.environ.get("LLM_API", "ollama")            # ollama | openai
LLM_BASE = os.environ.get("LLM_BASE_URL", "http://localhost:8000/v1" if LLM_API == "openai" else "http://localhost:11434").rstrip("/")
MODEL = os.environ.get("LLM_MODEL", "qwen3:8b")
LLM_KEY = os.environ.get("LLM_API_KEY", "")
NUM_CTX = int(os.environ.get("NUM_CTX", "8192"))
PORT = int(os.environ.get("PORT", "8773"))
HUMANIZE = os.environ.get("HUMANIZE_URL", "http://localhost:8765").rstrip("/")
TWEAKS = {"shorter": "직전 결과보다 절반 길이로.", "formal": "더 격식 있게(합쇼체, 직함 호칭).", "casual": "더 가볍고 캐주얼하게(해요체, 짧은 문장)."}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


# ── 패턴 로더 (frontmatter 전용 미니 파서 — 키: 값 / 리스트 [a, b] / inputs 블록) ────
def _val(s):
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        return [x.strip() for x in s[1:-1].split(",") if x.strip()]
    if s in ("true", "false"):
        return s == "true"
    return int(s) if re.fullmatch(r"-?\d+", s) else s


def parse_pattern(text):
    head, _, body = text.partition("\n---\n")
    meta, inputs, cur = {}, [], None
    for line in head.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - key:"):
            cur = {"key": line.split(":", 1)[1].strip()}
            inputs.append(cur)
        elif line.startswith("    ") and cur is not None:
            k, _, v = line.strip().partition(":")
            cur[k.strip()] = _val(v)
        elif line.startswith("inputs:"):
            cur = None
        else:
            k, _, v = line.partition(":")
            meta[k.strip()] = _val(v)
    meta["inputs"] = inputs
    meta["prompt"] = body.strip()
    for k in ("name", "title", "category", "description", "outputs"):
        assert k in meta, f"frontmatter에 {k} 없음"
    assert isinstance(meta["outputs"], int) and meta["outputs"] >= 1
    for i in inputs:
        assert "key" in i and "label" in i, f"input에 key/label 없음: {i}"
        i.setdefault("type", "text")
    return meta


def load_patterns():
    pats = {}
    for fn in sorted(os.listdir(os.path.join(ROOT, "patterns"))):
        if fn.endswith(".md"):
            p = parse_pattern(read(os.path.join(ROOT, "patterns", fn)))
            assert p["name"] not in pats, f"패턴 이름 중복: {p['name']}"
            pats[p["name"]] = p
    return pats


PATTERNS = load_patterns()


# ── LLM ────────────────────────────────────────────────────────────────
def _clean(out):
    out = re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip()
    out = re.sub(r"^```\w*\s*\n", "", out)
    out = re.sub(r"\n?```\s*$", "", out)
    return out.strip()


def openai_chat(system, user, model, on_token=None):
    body = {"model": model, "stream": True, "temperature": 0.7,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    hdr = {"Content-Type": "application/json", **({"Authorization": f"Bearer {LLM_KEY}"} if LLM_KEY else {})}
    req = urllib.request.Request(LLM_BASE + "/chat/completions", json.dumps(body).encode(), hdr)
    buf = []
    try:
        with urllib.request.urlopen(req, timeout=3600) as r:
            for line in r:
                line = line.decode().strip()
                if not line.startswith("data:") or line == "data: [DONE]":
                    continue
                tok = (json.loads(line[5:])["choices"][0].get("delta") or {}).get("content") or ""
                if tok:
                    buf.append(tok)
                    if on_token:
                        on_token(tok)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"LLM HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
    return "".join(buf)


def ollama(system, user, model, on_token=None):
    """Ollama /api/chat 스트리밍. think:false 미지원 모델이면 자동 재시도. LLM_API=openai 면 OpenAI 호환."""
    if LLM_API == "openai":
        return openai_chat(system, user, model, on_token)
    body = {"model": model, "stream": True, "think": False,
            "options": {"temperature": 0.7, "num_ctx": NUM_CTX},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    for attempt in (0, 1):
        try:
            req = urllib.request.Request(LLM_BASE + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
            buf = []
            with urllib.request.urlopen(req, timeout=3600) as r:
                for line in r:
                    if not line.strip():
                        continue
                    j = json.loads(line)
                    if "error" in j:
                        raise RuntimeError(j["error"])
                    tok = j.get("message", {}).get("content", "")
                    if tok:
                        buf.append(tok)
                        if on_token:
                            on_token(tok)
                    if j.get("done"):
                        break
            return "".join(buf)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if attempt == 0 and "think" in msg:
                body.pop("think")
                continue
            raise RuntimeError(f"Ollama HTTP {e.code}: {msg[:300]}")


def models():
    if LLM_API == "openai":
        req = urllib.request.Request(LLM_BASE + "/models", headers={"Authorization": f"Bearer {LLM_KEY}"} if LLM_KEY else {})
        with urllib.request.urlopen(req, timeout=10) as r:
            return [m["id"] for m in json.load(r)["data"]]
    with urllib.request.urlopen(LLM_BASE + "/api/tags", timeout=10) as r:
        return [m["name"] for m in json.load(r)["models"]]


def humanize(text, genre="essay"):
    """humanize-kr-local 서버에 윤문 요청 (SSE → 마지막 done.output)."""
    req = urllib.request.Request(HUMANIZE + "/api/humanize", json.dumps({"text": text, "genre": genre}).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=3600) as r:
        for line in r:
            if line.startswith(b"data: "):
                ev = json.loads(line[6:])
                if "done" in ev:
                    return ev["done"]["output"]
                if "error" in ev:
                    raise RuntimeError(ev["error"])
    raise RuntimeError("humanize 응답 없음")


# ── 생성 ────────────────────────────────────────────────────────────────
def split_variants(text, n):
    parts = [p.strip() for p in re.split(r"^\s*={3,}\s*$", text, flags=re.M) if p.strip()]
    return parts[:n] if n > 1 else [text.strip()]


def generate(name, values, model=MODEL, tweak=None, prev=None, emit=lambda ev: None):
    p = PATTERNS.get(name)
    if not p:
        raise ValueError(f"패턴 없음: {name} (있는 것: {', '.join(PATTERNS)})")
    for i in p["inputs"]:
        if i.get("required") and not str(values.get(i["key"], "")).strip():
            raise ValueError(f"필수 입력: {i['label']}")
    n = p["outputs"]
    system = (read(os.path.join(ROOT, "goal-prompt.md")) + f"\n\n[패턴: {p['title']}]\n{p['prompt']}\n"
              + (f"\n{n}개의 안을 쓴다. 안 사이는 `=====` 한 줄로만 구분한다." if n > 1 else "\n한 개만 쓴다."))
    user = "[입력]\n" + "\n".join(f"- {i['label']}: {values.get(i['key']) or '○○○'}" for i in p["inputs"])
    if tweak in TWEAKS and prev:
        user += f"\n\n[직전 결과]\n{prev}\n\n[수정 지시] {TWEAKS[tweak]} 같은 입력으로 다시 쓴다."
    emit({"stage": "llm", "msg": f"{model} · {p['title']}", "reset": True})
    out = _clean(ollama(system, user, model, on_token=lambda t: emit({"token": t})))
    if not out:  # ponytail: think 블록만 내고 끝나는 모델 대비 1회 재시도
        out = _clean(ollama(system, user, model, on_token=lambda t: emit({"token": t})))
    run_id = f"{datetime.datetime.now():%Y-%m-%d-%H%M%S}-{secrets.token_hex(1)}"  # 시각 포함 → 목록이 시간순
    result = {"run_id": run_id, "pattern": name, "title": p["title"], "model": model, "values": values, "tweak": tweak,
              "variants": split_variants(out, n), "raw": out, "ts": datetime.datetime.now().isoformat(timespec="seconds")}
    os.makedirs(WS, exist_ok=True)
    write(os.path.join(WS, run_id + ".json"), json.dumps(result, ensure_ascii=False, indent=1))
    return result


def list_runs():
    if not os.path.isdir(WS):
        return []
    out = []
    for fn in sorted(os.listdir(WS), reverse=True)[:50]:
        try:
            j = json.load(open(os.path.join(WS, fn), encoding="utf-8"))
            out.append({k: j[k] for k in ("run_id", "title", "model", "ts")} | {"head": j["variants"][0][:40]})
        except Exception:
            pass
    return out


# ── HTTP ───────────────────────────────────────────────────────────────
HTML = read(os.path.join(ROOT, "ui.html")) if os.path.exists(os.path.join(ROOT, "ui.html")) else "ui.html 없음"


class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        if "/api/generate" in (a[0] if a else ""):
            super().log_message(fmt, *a)

    def _send(self, body, ctype="application/json", code=200):
        b = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        try:
            if self.path == "/api/patterns":
                return self._send([{k: v for k, v in p.items() if k != "prompt"} for p in PATTERNS.values()])
            if self.path == "/api/models":
                return self._send(models())
            if self.path == "/api/runs":
                return self._send(list_runs())
            m = re.fullmatch(r"/api/runs/(\d{4}-\d{2}-\d{2}-\d{6}-[0-9a-f]{2})", self.path)
            if m:
                return self._send(read(os.path.join(WS, m.group(1) + ".json")).encode())
            if self.path == "/api/humanize_ok":
                try:
                    urllib.request.urlopen(HUMANIZE + "/api/models", timeout=2)
                    return self._send({"ok": True})
                except Exception:
                    return self._send({"ok": False})
            self._send(HTML.replace("%MODEL%", json.dumps(MODEL)).encode(), "text/html; charset=utf-8")
        except FileNotFoundError:
            self._send({"error": "없음"}, code=404)
        except Exception as e:
            self._send({"error": f"{type(e).__name__}: {e}"}, code=500)

    def do_POST(self):
        if self.path not in ("/api/generate", "/api/humanize"):
            return self._send({"error": "not found"}, code=404)
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.path == "/api/humanize":
            try:
                return self._send({"output": humanize(req.get("text", ""), req.get("genre") or "essay")})
            except Exception as e:
                return self._send({"error": f"{type(e).__name__}: {e}"}, code=502)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        def emit(ev):
            self.wfile.write(f"data: {json.dumps(ev, ensure_ascii=False)}\n\n".encode())
            self.wfile.flush()

        try:
            emit({"done": generate(req.get("pattern", ""), req.get("values") or {}, req.get("model") or MODEL,
                                   req.get("tweak"), req.get("prev"), emit)})
        except Exception as e:
            emit({"error": f"{type(e).__name__}: {e}"})


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        values = dict(a.split("=", 1) for a in sys.argv[3:] if "=" in a)
        r = generate(name, values, MODEL, emit=lambda ev: print(f"[{ev['stage']}] {ev['msg']}", file=sys.stderr) if "stage" in ev else None)
        print("\n\n=====\n\n".join(r["variants"]))
        sys.exit(0)
    print(f"writer local → http://localhost:{PORT}  (model={MODEL}, llm={LLM_API} {LLM_BASE}, patterns={len(PATTERNS)})")
    ThreadingHTTPServer(("", PORT), H).serve_forever()
