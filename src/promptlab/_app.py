"""Flask application for promptlab.

The wiring a blueprint cannot express lives here: an absolute template folder, an instance folder that
exists before SQLAlchemy resolves the relative sqlite path, and the HTML pages
(prompts, editor, runs) that read and write the real tables.

Nothing here calls lab.evals.run_eval(): that function performs outbound
urllib.request calls to api.openai.com with a 60 s timeout, so it stays behind
the JSON route POST /api/evals where a caller has opted into waiting for it.
The HTML "queue eval" form only records an EvalRun row.
"""

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from . import paths
from .lab.api import bp
from .models import EvalRun, Prompt, Result, Version, db

paths.ensure_runtime_dirs()


def build_app():
    """Build the application: configuration, database, then routes."""
    app = Flask(
        __name__, template_folder=str(paths.TEMPLATES_DIR), instance_path=str(paths.INSTANCE_DIR)
    )
    app.secret_key = "promptlab-dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(paths.INSTANCE_DIR / "promptlab.db")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(bp)

    @app.get("/")
    def index():
        prompts = Prompt.query.order_by(Prompt.id).all()
        runs = EvalRun.query.order_by(EvalRun.id.desc()).limit(10).all()
        return render_template("index.html", prompts=prompts, runs=runs)

    @app.post("/prompts")
    def prompt_create():
        """HTML equivalent of POST /api/prompts (which needs a JSON body)."""
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("name required", "no")
            return redirect(url_for("index"))
        if Prompt.query.filter_by(name=name).first():
            flash("prompt %s already exists" % name, "no")
            return redirect(url_for("index"))
        p = Prompt(name=name)
        db.session.add(p)
        db.session.flush()
        db.session.add(
            Version(
                prompt_id=p.id,
                version=1,
                template=request.form.get("template") or "",
                vars_json=str(
                    [v.strip() for v in (request.form.get("vars") or "").split(",") if v.strip()]
                ),
            )
        )
        db.session.commit()
        flash("created prompt %s (v1)" % name)
        return redirect(url_for("prompt_editor", pid=p.id))

    @app.get("/prompts/<int:pid>/editor")
    def prompt_editor(pid):
        p = Prompt.query.get_or_404(pid)
        versions = Version.query.filter_by(prompt_id=pid).order_by(Version.version.desc()).all()
        latest = versions[0] if versions else None
        runs = EvalRun.query.filter_by(prompt_id=pid).order_by(EvalRun.id.desc()).limit(10).all()
        return render_template("editor.html", prompt=p, versions=versions, latest=latest, runs=runs)

    @app.post("/prompts/<int:pid>/versions")
    def version_create(pid):
        """HTML equivalent of POST /api/prompts/<id>/versions."""
        p = Prompt.query.get_or_404(pid)
        p.current_version += 1
        db.session.add(
            Version(
                prompt_id=pid,
                version=p.current_version,
                template=request.form.get("template") or "",
            )
        )
        db.session.commit()
        flash("saved v%d" % p.current_version)
        return redirect(url_for("prompt_editor", pid=pid))

    @app.post("/prompts/<int:pid>/eval")
    def eval_queue(pid):
        """Record an eval run.  Execution stays on POST /api/evals because
        lab.evals.run_eval() calls the model APIs over the network."""
        p = Prompt.query.get_or_404(pid)
        models = [m.strip() for m in (request.form.get("models") or "").split(",") if m.strip()]
        cases = request.form.get("cases", type=int) or 0
        run = EvalRun(
            prompt_id=pid,
            version=p.current_version,
            models_json=str(models or ["gpt-4o"]),
            status="queued",
        )
        db.session.add(run)
        db.session.commit()
        flash(
            "queued eval #%d for %d case(s) — run POST /api/evals to execute it" % (run.id, cases)
        )
        return redirect(url_for("run_detail", rid=run.id))

    @app.get("/runs")
    def runs():
        rows = EvalRun.query.order_by(EvalRun.id.desc()).all()
        counts = {r.id: Result.query.filter_by(run_id=r.id).count() for r in rows}
        return render_template("runs.html", runs=rows, counts=counts)

    @app.get("/runs/<int:rid>")
    def run_detail(rid):
        run = EvalRun.query.get_or_404(rid)
        results = Result.query.filter_by(run_id=rid).all()
        by_model = {}
        for r in results:
            m = by_model.setdefault(
                r.model or "-", {"pass": 0, "total": 0, "cost": 0.0, "latency": 0.0}
            )
            m["total"] += 1
            m["pass"] += r.passed or 0
            m["cost"] += r.cost or 0.0
            m["latency"] = max(m["latency"], r.latency_ms or 0.0)
        return render_template("run.html", run=run, results=results, by_model=by_model)

    @app.get("/api/health")
    def health():
        return jsonify(
            {"status": "ok", "prompts": Prompt.query.count(), "runs": EvalRun.query.count()}
        )

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000)

    return app


app = build_app()
