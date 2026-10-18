from flask import Blueprint, jsonify, request

from ..models import EvalRun, Prompt, Result, Version, db
from .evals import run_eval

bp = Blueprint("lab", __name__)


@bp.post("/api/prompts")
def add_prompt():
    d = request.get_json(force=True, silent=True) or {}
    p = Prompt(name=d.get("name", ""))
    db.session.add(p)
    db.session.flush()
    db.session.add(
        Version(
            prompt_id=p.id,
            version=1,
            template=d.get("template", ""),
            vars_json=str(d.get("vars", [])),
        )
    )
    db.session.commit()
    return jsonify({"id": p.id})


@bp.get("/api/prompts")
def list_prompts():
    return jsonify(
        {
            "prompts": [
                {"id": p.id, "name": p.name, "version": p.current_version}
                for p in Prompt.query.all()
            ]
        }
    )


@bp.post("/api/prompts/<int:pid>/versions")
def new_version(pid):
    d = request.get_json(force=True, silent=True) or {}
    p = Prompt.query.get_or_404(pid)
    p.current_version += 1
    db.session.add(
        Version(prompt_id=pid, version=p.current_version, template=d.get("template", ""))
    )
    db.session.commit()
    return jsonify({"version": p.current_version})


@bp.post("/api/evals")
def start_eval():
    d = request.get_json(force=True, silent=True) or {}
    if not d.get("cases"):
        return jsonify({"error": "cases required"}), 400
    run_id = run_eval(d.get("prompt_id", 0), d.get("models", ["gpt-4o"]), d["cases"])
    return jsonify({"run_id": run_id, "status": "running"})


@bp.get("/api/evals/<int:rid>")
def eval_result(rid):
    run = EvalRun.query.get_or_404(rid)
    results = Result.query.filter_by(run_id=rid).all()
    by_model = {}
    for r in results:
        m = by_model.setdefault(r.model, {"pass": 0, "total": 0, "cost": 0.0, "latency": 0.0})
        m["total"] += 1
        m["pass"] += r.passed
        m["cost"] += r.cost
        m["latency"] = max(m["latency"], r.latency_ms)
    return jsonify({"status": run.status, "results": by_model})
