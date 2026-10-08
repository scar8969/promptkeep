import json, time, urllib.request

def run_eval(prompt_id, models, cases):
    from ..models import EvalRun, Result, Version, Prompt, db
    from .prompts import render
    from .assertions import check
    from .cost import cost
    prompt = Prompt.query.get(prompt_id)
    version = Version.query.filter_by(prompt_id=prompt_id, version=prompt.current_version).first()
    run = EvalRun(prompt_id=prompt_id, version=prompt.current_version,
                  models_json=str(models))
    db.session.add(run)
    db.session.flush()
    for case in cases:
        prompt_text = render(version.template, case.get("vars", {}))
        for model in models:
            try:
                out, tin, tout, lat = _call_model(model, case.get("api_key", ""), prompt_text)
                passed = all(check(out, a) for a in case.get("assert", []))
            except Exception:
                out, tin, tout, lat, passed = "ERROR", 0, 0, 0, False
            db.session.add(Result(run_id=run.id, case_id=case.get("id", 0), model=model,
                                  output=out, passed=1 if passed else 0,
                                  cost=cost(model, tin, tout), latency_ms=lat))
    run.status = "done"
    db.session.commit()
    return run.id

def _call_model(model, api_key, prompt):
    payload = json.dumps({"model": model,
                          "messages": [{"role": "user", "content": prompt}],
                          "max_tokens": 256}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
                                 data=payload, headers={"Content-Type": "application/json",
                                                        "Authorization": f"Bearer {api_key}"})
    s = time.perf_counter()
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    latency = (time.perf_counter() - s) * 1000
    out = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return out, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), latency
