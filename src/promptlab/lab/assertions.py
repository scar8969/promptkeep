import json
import re


def check(output, assertion):
    t = assertion.get("type")
    v = assertion.get("value")
    if t == "contains":
        return v in output
    if t == "equals":
        return v == output
    if t == "regex":
        return bool(re.search(v, output))
    if t == "jsonpath":
        try:
            data = json.loads(output)
            for part in v.split("."):
                data = data[part]
            return True
        except Exception:
            return False
    return False
