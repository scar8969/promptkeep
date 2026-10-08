== curl ==
# POST /api/prompts  {"name":"summarize","template":"Summarize {text}","vars":["text"]}
# POST /api/prompts/1/versions  {"template":"…"}
# POST /api/evals  {"prompt_id":1,"models":["gpt-4o","claude"],"cases":[{"input":"…","assert":{"type":"contains","value":"key"}}]}
# GET  /api/evals/1
# CLI: promptlab run --prompt summarize --models gpt-4o claude

== session plan ==
# Session 1: prompts + versions + render → tests
# Session 2: assertions + cost → tests
# Session 3: eval runner (mock server) + api → tests
# Session 4: web templates + cli → screenshots → README → CI/Docker/Pages → tag
