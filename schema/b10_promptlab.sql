-- 🧪 promptlab schema
CREATE TABLE prompts(id INTEGER PRIMARY KEY, name TEXT UNIQUE, current_version INTEGER DEFAULT 1, created_at DATETIME);
CREATE TABLE versions(id INTEGER PRIMARY KEY, prompt_id INTEGER REFERENCES prompts(id), version INTEGER DEFAULT 1, template TEXT, vars_json TEXT DEFAULT '[]', created_at DATETIME);
CREATE TABLE eval_runs(id INTEGER PRIMARY KEY, prompt_id INTEGER REFERENCES prompts(id), version INTEGER DEFAULT 1, models_json TEXT DEFAULT '[]', status TEXT DEFAULT 'running', started_at DATETIME);
CREATE TABLE results(id INTEGER PRIMARY KEY, run_id INTEGER REFERENCES eval_runs(id), case_id INTEGER DEFAULT 0, model TEXT, output TEXT, passed INTEGER DEFAULT 0, cost REAL DEFAULT 0, latency_ms REAL DEFAULT 0);
