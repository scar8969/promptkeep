# Evidence

Every claim below comes from a command that was actually run against this
exact checkout. Nothing here is inferred from the source alone.

## Commands

```sh
# from the project directory, with _tools and _tools/_vendor on PYTHONPATH
python -m pytest -q -p hosttmp_proj tests/
python -m compileall -q src
```

## Recorded results

| check | result |
| --- | --- |
| compileall | exit 0 |
| pytest | ..........................                                               [100%] |
| pytest_exit_code | 0 |
| recorded_at | 2026-10-08 |
| routes_ok | 12 |
| routes_probed | 12 |

## HTTP surface

One real GET per rule in the assembled URL map, through Flask's test
client. `ok` includes 404 on a templated path: an empty database has
no such resource, and 404 is the honest answer for that.

| method | path | rule | status | bytes | note |
| --- | --- | --- | --- | --- | --- |
| GET | `/` | `/` | 200 | 4899 | ok |
| GET | `/api/evals/demo` | `/api/evals/<int:rid>` | 404 | 51 | ok |
| GET | `/api/health` | `/api/health` | 200 | 37 | ok |
| GET | `/api/prompts` | `/api/prompts` | 200 | 15 | ok |
| GET | `/healthz` | `/healthz` | 200 | 56 | ok |
| GET | `/livez` | `/livez` | 200 | 19 | ok |
| GET | `/metrics` | `/metrics` | 200 | 304 | ok |
| GET | `/prompts/demo/editor` | `/prompts/<int:pid>/editor` | 404 | 207 | ok |
| GET | `/readyz` | `/readyz` | 200 | 31 | ok |
| GET | `/runs` | `/runs` | 200 | 4009 | ok |
| GET | `/runs/demo` | `/runs/<int:rid>` | 404 | 207 | ok |
| GET | `/version` | `/version` | 200 | 891 | ok |

## Operational endpoints

`/healthz` answered **200**:

```
{"service":"promptlab","status":"ok","version":"0.1.0"}
```

`/livez` answered **200**:

```
{"status":"alive"}
```

`/readyz` answered **200**:

```
{"checks":[],"status":"ready"}
```

`/metrics` answered **200**:

```
# TYPE http_requests_total counter
http_requests_total{method="GET",status="200"} 3
# TYPE http_request_duration_seconds_sum counter
http_request_duration_seconds_sum{method="GET"} 0.031576
http_requests_total{method="GET",status="404"} 1
# TYPE process_uptime_seconds gauge
process_uptime_seconds 0.687
```

`/version` answered **200**:

```
{"config":{"app_name":"promptlab","data_dir":".\\var","database_configured":false,"debug":false,"env":"development","host":"0.0.0.0","legacy_env_present":[],"log_json":true,"log_level":"INFO","port":8000,"secret_key_configured":false},"paths":{"data_dir":".\\var",
```

## Headers observed on /healthz

| header | value |
| --- | --- |
| X-Request-ID | 55a8bee5b7f74d8691f5b0b587d76378 |
| X-Content-Type-Options | nosniff |
| X-Frame-Options | DENY |
| Referrer-Policy | no-referrer |
| Cross-Origin-Opener-Policy | same-origin |
| Permissions-Policy | geolocation=(), microphone=(), camera=() |
| Content-Type | application/json |

## What this file does not claim

- No browser screenshot: this host denies the Chromium sandbox the renderer
  needs, so the HTTP surface is evidenced with recorded status codes instead.
- No network access: the suite is hermetic and contacts no remote host.
- No container run: the Dockerfile is reviewed, not executed, because no
  container runtime is reachable from this host.
