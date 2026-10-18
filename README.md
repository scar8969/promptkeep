<p align="center">
  <img src="docs/assets/screens/root.png" alt="promptkeep running" width="900">
</p>

<h1 align="center">promptkeep</h1>

<p align="center"><b>Version every prompt, then measure it instead of arguing about it.</b></p>

<p align="center">
  <a href="#quality-gates"><img src="https://img.shields.io/badge/tests-26%20passed-2ea44f" alt="tests: 26 passed"></a> <a href="#quality-gates"><img src="https://img.shields.io/badge/coverage-68.7%-yellow" alt="coverage: 68.7%"></a> <a href="#api"><img src="https://img.shields.io/badge/routes-9%20answered-0969da" alt="routes: 9 answered"></a> <a href="#requirements"><img src="https://img.shields.io/badge/python-3.11%2B-3776ab" alt="python: 3.11+"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="license: MIT"></a>
</p>

promptkeep stores prompts with an append-only version history and runs evals against those versions, storing per-case scores so a prompt change is a diff and a number.

---

**Contents** &nbsp;·&nbsp; [Why](#why-this-exists) &nbsp;·&nbsp; [What it does](#what-it-does) &nbsp;·&nbsp; [Quickstart](#quickstart) &nbsp;·&nbsp; [API](#api) &nbsp;·&nbsp; [Screenshots](#screenshots) &nbsp;·&nbsp; [Measured](#measured-not-estimated) &nbsp;·&nbsp; [Architecture](#architecture) &nbsp;·&nbsp; [Quality gates](#quality-gates) &nbsp;·&nbsp; [Deploy](#deploy) &nbsp;·&nbsp; [Limits](#limits-stated-rather-than-hidden)

## Why this exists

Prompt work happens in chat windows and gets lost. Keeping each revision as a row and each eval as scored cases turns "this feels better" into a comparison you can rerun.

## What it does

| Capability | How it works |
| --- | --- |
| **Append-only versions** | Every save creates a version; nothing is overwritten. |
| **Evals per version** | An eval run applies per-case assertions — contains, equals, regex or JSON path — and stores one result per case against a specific version. |
| **Comparison** | Results are queryable per eval, so two versions can be put side by side. |
| **HTML view** | The panel lists prompts and their latest scores. |

## Quickstart

```sh
git clone https://github.com/scar8969/promptkeep.git
cd promptkeep
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python wsgi.py                                 # http://127.0.0.1:8000
```

The same work from the CLI:

```sh
python -m promptlab.cli --help
```

Commands: `run`.

A first request:

```sh
curl -s http://127.0.0.1:8000/api/prompts | head
```

## Requirements

- Python **3.11+** — CI runs 3.11, 3.12 and 3.13.
- Runtime dependencies: `Flask>=3.0`, `Flask-SQLAlchemy>=3.1`, `SQLAlchemy>=2.0`, `PyYAML>=6.0`.
- No JavaScript build step: every page is server-rendered Jinja.

## API

Every route below is in [`openapi/promptkeep.yaml`](openapi/promptkeep.yaml) and is exercised by the live probe recorded in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/prompts` | list |
| `POST` | `/api/prompts` | create |
| `POST` | `/api/prompts/<id>/versions` | new version |
| `POST` | `/api/evals` | run eval |
| `GET` | `/api/evals/<id>` | results |

## Screenshots

Captured from the running service with headless Chromium at 1440×900, one image per page, committed under [`docs/assets/screens/`](docs/assets/screens/).

<table>
<tr>
<td width="50%"><img src="docs/assets/screens/runs.png" alt="/runs" width="100%"><br><sub><code>/runs</code> &middot; 16.0 KB</sub></td>
<td width="50%"><img src="docs/assets/screens/healthz.png" alt="/healthz" width="100%"><br><sub><code>/healthz</code> &middot; 8.3 KB</sub></td>
</tr>
</table>

<table>
<tr>
<td width="50%"><img src="docs/assets/screens/livez.png" alt="/livez" width="100%"><br><sub><code>/livez</code> &middot; 7.3 KB</sub></td>
<td width="50%"><img src="docs/assets/screens/metrics.png" alt="/metrics" width="100%"><br><sub><code>/metrics</code> &middot; 14.8 KB</sub></td>
</tr>
</table>

<table>
<tr>
<td width="50%"><img src="docs/assets/screens/readyz.png" alt="/readyz" width="100%"><br><sub><code>/readyz</code> &middot; 7.7 KB</sub></td>
<td width="50%"><img src="docs/assets/screens/version.png" alt="/version" width="100%"><br><sub><code>/version</code> &middot; 25.4 KB</sub></td>
</tr>
</table>

## Measured, not estimated

These numbers were produced on this checkout by `pytest --cov` and by booting `wsgi.py` and issuing one real GET per documented path. The commands are in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Signal | Value |
| --- | --- |
| Tests | **26 / 26 passed** (2.2 s, exit 0) |
| Line coverage | **68.7%** — 448 of 630 statements |
| Source | 16 files / 1,384 lines |
| Test code | 4 files / 242 lines |
| Documented paths | 4 in the spec, 2 GET |
| Live probe | 12 GET requests to the booted app, **9 answered 200** |
| Median latency | **6.0 ms** (single uncached request, dev server) |
| Slowest / fastest | 76.7 ms `/` / 3.4 ms `/healthz` |
| Bytes served | 10.5 KB across 12 responses |
| Screenshots | 7 captured |

## Architecture

```
promptkeep/
├── src/promptlab/
│   ├── http.py                         379  HTTP plumbing for promptlab: correlation ids, access
│   ├── config.py                       171  Environment-driven configuration for promptlab
│   ├── observability.py                169  Structured logging and request correlation for promp
│   ├── _app.py                         147  Flask application for promptlab
│   ├── app.py                          119  Application factory for promptlab
│   ├── errors.py                       108  Typed application errors and their HTTP mapping for 
│   ├── lab/api.py                       74  
│   ├── lab/evals.py                     57  
│   ├── paths.py                         52  Filesystem layout for promptlab
│   ├── models.py                        46  
│   ├── cli.py                           23  
│   ├── lab/assertions.py                23  
├── openapi/promptkeep.yaml                the contract of record
├── schema/promptkeep.sql                  the DDL
├── tests/                       the suite that has to stay green
├── docs/EVIDENCE.md             the recorded live route walk
├── Dockerfile                   multi-stage build
└── wsgi.py                      entry point
```

The package keeps one shape across the service: `config.py` reads the environment once, `observability.py` emits structured JSON logs carrying a request id, `errors.py` turns exceptions into a single JSON envelope, `models.py` holds the tables, and the `lab/` package holds the routes.

## Quality gates

| Gate | Command | Threshold |
| --- | --- | --- |
| Suite | `pytest -q` | all green |
| Coverage | `pytest --cov` | floor set in `pyproject.toml` from the measured value |
| Lint | `ruff check src tests` | zero findings |
| Format | `ruff format --check src tests` | zero reformats |
| Types | `mypy src` | zero errors |
| Security | `bandit -c pyproject.toml -r src` | reviewed skip list, no unreviewed finding |
| Live routes | boot `wsgi.py`, one GET per documented path | no 5xx, no undocumented guard |

CI runs the first six on Python 3.11, 3.12 and 3.13 for every push to `main`, plus a container build. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Deploy

```sh
docker build -t promptkeep .
docker run --rm -p 8000:8000 --env-file .env.example promptkeep
```

Configuration is environment-only — every variable is documented in [`.env.example`](.env.example), and the service refuses to start with a production secret missing.

## Limits, stated rather than hidden

- Assertions are deterministic string and JSON checks; there is no model-graded rubric.
- Eval runs execute in-process, so a large suite blocks the worker.

## License

MIT — see [LICENSE](LICENSE).
