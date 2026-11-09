"""Reward lookup and terminal state checks matching the MDP baseline convention."""


def step_reward(env, state, action, next_state):
    """Return the immediate per-step living cost from the environment."""
    # Why: Every step incurs env.living_cost so Q-learning values match MDP.py conventions.
    return float(env.living_cost)


def is_terminal(env, state):
    """Return True if the given state is a terminal state in the environment."""
    return state in env.terminal_states


def terminal_payoff(env, state):
    """Return the terminal payoff for a terminal state, or raise KeyError if non-terminal."""
    # Why: Raising KeyError on non-terminal states catches logic bugs in caller modules early.
    if state not in env.terminal_states:
        raise KeyError(f"State {state} is not a terminal state.")
    return float(env.terminal_states[state])
