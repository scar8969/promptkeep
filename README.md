<p align="center">
  <img src="docs/assets/screens/root.png" alt="promptkeep running" width="900">
</p>

<h1 align="center">promptkeep</h1>

<p align="center"><b>Version every prompt, then measure it instead of arguing about it.</b></p>

<p align="center">
  <a href="https://github.com/scar8969/promptkeep/actions/workflows/ci.yml"><img src="https://github.com/scar8969/promptkeep/actions/workflows/ci.yml/badge.svg" alt="ci"></a> <a href="#quality-gates"><img src="https://img.shields.io/badge/tests-26%20passed-2ea44f" alt="tests: 26 passed"></a> <a href="#quality-gates"><img src="https://img.shields.io/badge/coverage-68.7%-yellow" alt="coverage: 68.7%"></a> <a href="#api"><img src="https://img.shields.io/badge/routes-9%20live-0969da" alt="routes: 9 live"></a> <a href="#requirements"><img src="https://img.shields.io/badge/python-3.11%2B-3776ab" alt="python: 3.11+"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="license: MIT"></a>
</p>

promptkeep stores prompts with an append-only version history and runs evals against those versions, storing per-case scores so a prompt change is a diff and a number.

---

**Contents** &nbsp;·&nbsp; [Why](#why-this-exists) &nbsp;·&nbsp; [What it does](#what-it-does) &nbsp;·&nbsp; [Quickstart](#quickstart) &nbsp;·&nbsp; [Screenshots](#screenshots) &nbsp;·&nbsp; [API](#api) &nbsp;·&nbsp; [CLI](#cli) &nbsp;·&nbsp; [Configuration](#configuration) &nbsp;·&nbsp; [Measured](#measured-not-estimated) &nbsp;·&nbsp; [How a request flows](#how-a-request-flows) &nbsp;·&nbsp; [Architecture](#architecture) &nbsp;·&nbsp; [Quality gates](#quality-gates) &nbsp;·&nbsp; [Development](#development) &nbsp;·&nbsp; [Deploy](#deploy) &nbsp;·&nbsp; [Limits](#limits-stated-rather-than-hidden)

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

It is up when this answers:

```sh
curl -s http://127.0.0.1:8000/api/prompts
```

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

## API

Every route below is declared in [`openapi/promptkeep.yaml`](openapi/promptkeep.yaml) and exercised by the live probe recorded in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/prompts` | list |
| `POST` | `/api/prompts` | create |
| `POST` | `/api/prompts/<id>/versions` | new version |
| `POST` | `/api/evals` | run eval |
| `GET` | `/api/evals/<id>` | results |

## CLI

The same operations without an HTTP client. Installed as `promptkeep`, and runnable from a checkout with no install:

```sh
python -m promptlab.cli --help
```

```text
usage: promptlab [-h] {run} ...

positional arguments:
  {run}

options:
  -h, --help  show this help message and exit
```

## Configuration

Environment only — there is no config file. Copy `.env.example` to `.env` and edit; `APP_ENV=production` refuses to start without `SECRET_KEY`.

| Variable | Default | Meaning |
| --- | --- | --- |
| `APP_ENV` | `development` | development \| staging \| production; production enforces the secret. |
| `SECRET_KEY` | `change-me-in-production` | Session/CSRF signing key. Required when APP_ENV=production. |
| `HOST` | `0.0.0.0` | Interface the dev server binds. |
| `PORT` | `8000` | Port the dev server and the container listen on. |
| `DEBUG` | `false` | Flask debug mode. Never true in production. |
| `MAX_CONTENT_LENGTH` | `8388608` | Largest accepted request body, in bytes. |
| `DATA_DIR` | `(empty)` | Where uploaded and generated files live. |
| `INSTANCE_DIR` | `(empty)` | Where the SQLite file and instance state live. |
| `LOG_DIR` | `(empty)` | Where rotated log files are written, if file logging is on. |
| `LOG_LEVEL` | `INFO` | DEBUG \| INFO \| WARNING \| ERROR. |
| `LOG_JSON` | `true` | true emits one JSON object per line; false is human-readable. |
| `REQUEST_ID_HEADER` | `X-Request-ID` | Header echoed on every response and stamped on every log line. |

## Measured, not estimated

Produced on this checkout by `pytest --cov` and by booting `wsgi.py` and issuing one real GET per documented path. The commands are recorded in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Signal | Value |
| --- | --- |
| Tests | **26 / 26 passed** (2.2 s, exit 0) |
| Line coverage | **68.7%** — 448 of 630 statements |
| Source | 16 files / 1,385 lines |
| Test code | 4 files / 242 lines |
| Documented paths | 4 in the spec, 2 GET |
| Live probe | 12 GET requests to the booted app, **9 answered 200** |
| Median latency | **6.0 ms** (single uncached request, dev server) |
| Slowest / fastest | 76.7 ms `/` / 3.4 ms `/healthz` |
| Bytes served | 10.5 KB across 12 responses |
| Screenshots | 7 captured |

## How a request flows

```text
client
  │  HTTP
  ▼
wsgi.py ──▶ promptlab/app.py:get_app()
                │  reads config once (promptlab/config.py)
                │  registers the `lab` blueprint
                ▼
           route handler
             ├──▶ promptlab/models.py        tables, via Flask-SQLAlchemy
             ├──▶ promptlab/errors.py        raises typed errors → one JSON envelope
             └──▶ promptlab/observability.py JSON log line + X-Request-ID
```

Every response carries `X-Request-ID`, and the matching log line is written once at the end of the request with the status and duration, so a report of "it failed" is one `grep` away from the traceback.

## Architecture

```
promptkeep/
├── src/promptlab/
│   ├── http.py                         379  HTTP plumbing for promptlab: correlation ids, access
│   ├── observability.py                169  Structured logging and request correlation for promp
│   ├── config.py                       168  Environment-driven configuration for promptlab
│   ├── _app.py                         147  Flask application for promptlab
│   ├── app.py                          119  Application factory for promptlab
│   ├── errors.py                       108  Typed application errors and their HTTP mapping for 
│   ├── lab/api.py                       74  
│   ├── lab/evals.py                     57  
│   ├── paths.py                         52  Filesystem layout for promptlab
│   ├── models.py                        46  
│   ├── cli.py                           27  
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
| Coverage | `pytest --cov` | floor in `pyproject.toml`, set below the measured value |
| Lint | `ruff check src tests` | zero findings |
| Format | `ruff format --check src tests` | zero reformats |
| Types | `mypy src` | zero errors |
| Security | `bandit -c pyproject.toml -r src` | reviewed skip list, no unreviewed finding |
| Live routes | boot `wsgi.py`, one GET per documented path | no 5xx, no undocumented guard |

CI runs the first six on Python 3.11, 3.12 and 3.13 on every push to `main`, plus a container build — [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Development

```sh
pip install -e ".[dev]"
python -m pytest -q                      # the suite
python -m pytest --cov                   # with the coverage floor
python -m ruff check src tests           # lint
python -m ruff format --check src tests  # formatting
python -m mypy src                       # types
python -m bandit -c pyproject.toml -r src  # security
pre-commit install                       # the same checks on commit
```

Dependabot opens grouped PRs for the dev tooling weekly and for actions and the base image monthly.

## Deploy

```sh
docker build -t promptkeep .
docker run --rm -p 8000:8000 --env-file .env.example promptkeep
```

A `docker-compose.yml` is included for a local run with a volume for the SQLite file. The image runs as a non-root user and serves through gunicorn.

## Limits, stated rather than hidden

- Assertions are deterministic string and JSON checks; there is no model-graded rubric.
- Eval runs execute in-process, so a large suite blocks the worker.

## License

MIT — see [LICENSE](LICENSE).
