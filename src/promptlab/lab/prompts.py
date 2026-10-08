import re

def render(template, vars):
    def _sub(m):
        return str(vars.get(m.group(1), ""))
    return re.sub(r"\{(\w+)\}", _sub, template)
