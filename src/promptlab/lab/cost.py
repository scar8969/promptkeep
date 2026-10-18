MODEL_COSTS = {"gpt-4o": (2.50, 10.00), "gpt-4o-mini": (0.15, 0.60), "claude-sonnet": (3.00, 15.00)}


def cost(model, tokens_in, tokens_out):
    rates = MODEL_COSTS.get(model, (2.50, 10.00))
    return tokens_in / 1e6 * rates[0] + tokens_out / 1e6 * rates[1]
