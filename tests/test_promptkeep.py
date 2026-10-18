"""B10 promptlab — tests. Run: pytest test_promptkeep.py"""

import pytest


def test_render():
    from promptlab.lab.prompts import render

    assert (
        render("Summarize {text} in {n} words", {"text": "hi", "n": 10})
        == "Summarize hi in 10 words"
    )


def test_render_missing_key_empty():
    from promptlab.lab.prompts import render

    assert render("Hello {name}", {}) == "Hello "


def test_assert_contains():
    from promptlab.lab.assertions import check

    assert check("the quick brown fox", {"type": "contains", "value": "brown"})
    assert not check("the quick fox", {"type": "contains", "value": "brown"})


def test_assert_equals():
    from promptlab.lab.assertions import check

    assert check("exact", {"type": "equals", "value": "exact"})


def test_assert_regex():
    from promptlab.lab.assertions import check

    assert check("price: $42.50", {"type": "regex", "value": r"\$\d+\.\d+"})


def test_cost():
    from promptlab.lab.cost import cost

    assert cost("gpt-4o", 1000, 500) == pytest.approx(2.5 * 0.001 + 10.0 * 0.0005)
