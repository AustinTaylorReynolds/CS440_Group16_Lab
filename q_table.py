"""Q-table initialization and greedy action lookup for the vacuum robot."""

ACTIONS = ["N", "S", "E", "W"]


def init_q_table(env):
    """Initialize a nested Q-table with 0.0 for all non-obstacle states and actions."""
    # Why: The agent has no prior knowledge of state values, and the obstacle cannot be entered.
    q_table = {}
    for r in range(env.rows):
        for c in range(env.cols):
            state = (r, c)
            if state != env.obstacle:
                q_table[state] = {action: 0.0 for action in ACTIONS}
    return q_table


def best_actions(q_table, state):
    """Return all actions tied for the highest Q-value at the given state in ACTIONS order."""
    # Why: Preserving ACTIONS order ensures deterministic tie-breaking during policy extraction.
    state_actions = q_table[state]
    max_q = max(state_actions.values())
    return [action for action in ACTIONS if state_actions[action] == max_q]
