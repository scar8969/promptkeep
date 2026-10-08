from .lab.evals import run_eval

import argparse

def cmd_run(args):
    cases = [{"input": "…", "assert": {"type": "contains", "value": "key"}}]
    run_id = run_eval(args.prompt, args.models, cases)
    print(f"[promptlab] run #{run_id} started")

def main():
    p = argparse.ArgumentParser(prog="promptlab")
    sub = p.add_subparsers(dest="cmd")
    r = sub.add_parser("run"); r.add_argument("--prompt", required=True)
    r.add_argument("--models", nargs="+", default=["gpt-4o"])
    args = p.parse_args()
    if args.cmd == "run":
        return cmd_run(args)
    p.print_help()
    return 1
