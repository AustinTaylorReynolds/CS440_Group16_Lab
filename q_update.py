"""Model-free Q-learning temporal-difference update rule."""


def q_update(q_table, state, action, reward, next_state, alpha, gamma, terminal_value=None):
    """Update Q(state, action) in place and return the new Q-value."""
    # Why: When next_state is terminal, its fixed payoff replaces max_a' Q(s', a') to match MDP.py.
    if terminal_value is not None:
        future_value = float(terminal_value)
    else:
        future_value = max(q_table[next_state].values())

    current_q = q_table[state][action]
    target = reward + gamma * future_value
    new_q = current_q + alpha * (target - current_q)
    q_table[state][action] = new_q
    return new_q
