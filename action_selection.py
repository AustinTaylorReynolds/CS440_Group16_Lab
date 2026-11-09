"""Epsilon-greedy action selection and exploration decay schedule."""

import random
from q_table import ACTIONS, best_actions


def choose_action(q_table, state, epsilon):
    """Select an action using epsilon-greedy exploration with random tie-breaking."""
    # Why: Random exploration prevents premature convergence, and random tie-breaking avoids directional bias.
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    return random.choice(best_actions(q_table, state))


def decay_epsilon(epsilon, eps_decay, eps_min):
    """Decay epsilon multiplicatively down to a minimum exploration floor."""
    # Why: Gradually shifting from exploration to exploitation stabilizes Q-values over training.
    return max(float(eps_min), float(epsilon * eps_decay))
