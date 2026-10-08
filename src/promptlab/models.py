from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prompt(db.Model):
    __tablename__ = "prompts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    current_version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Version(db.Model):
    __tablename__ = "versions"
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.id"))
    version = db.Column(db.Integer, default=1)
    template = db.Column(db.Text, default="")
    vars_json = db.Column(db.Text, default="[]")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EvalRun(db.Model):
    __tablename__ = "eval_runs"
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.id"))
    version = db.Column(db.Integer, default=1)
    models_json = db.Column(db.Text, default="[]")
    status = db.Column(db.String(16), default="running")
    started_at = db.Column(db.DateTime, default=datetime.utcnow)

class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("eval_runs.id"))
    case_id = db.Column(db.Integer, default=0)
    model = db.Column(db.String(64), default="")
    output = db.Column(db.Text, default="")
    passed = db.Column(db.Integer, default=0)
    cost = db.Column(db.Float, default=0.0)
    latency_ms = db.Column(db.Float, default=0.0)
