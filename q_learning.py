"""Integration module for training, evaluating, and comparing the Q-learning vacuum robot."""

import random
from GridEnvironment import GridnEnvironment
from MDP import MDP
from q_table import ACTIONS, init_q_table, best_actions
from rewards import step_reward, is_terminal, terminal_payoff
from action_selection import choose_action, decay_epsilon
from q_update import q_update

LIVING_COSTS = [-0.04, -0.1, -2.0]
SEED = 42

DEFAULT_EPISODES = 5000
DEFAULT_ALPHA = 0.1
DEFAULT_GAMMA = 0.9
DEFAULT_EPS_START = 1.0
DEFAULT_EPS_MIN = 0.05
DEFAULT_EPS_DECAY = 0.999
DEFAULT_MAX_STEPS = 100

ARROW_MAP = {"N": "^", "S": "v", "E": ">", "W": "<"}


def env_step(env, state, action):
    """Simulate one stochastic step in the environment and return (reward, next_state, terminal_value)."""
    # Why: This function stands in for the physical world; it is the ONLY place allowed to call get_transition.
    transitions = env.get_transition(action)
    probs = [prob for prob, _ in transitions]
    dirs = [direction for _, direction in transitions]
    actual_dir = random.choices(dirs, weights=probs, k=1)[0]

    next_state = env.get_next_state(state, actual_dir)
    reward = step_reward(env, state, action, next_state)
    terminal_value = terminal_payoff(env, next_state) if is_terminal(env, next_state) else None
    return reward, next_state, terminal_value


def train(
    env,
    episodes=DEFAULT_EPISODES,
    alpha=DEFAULT_ALPHA,
    gamma=DEFAULT_GAMMA,
    eps_start=DEFAULT_EPS_START,
    eps_min=DEFAULT_EPS_MIN,
    eps_decay=DEFAULT_EPS_DECAY,
    max_steps=DEFAULT_MAX_STEPS,
    seed=None,
):
    """Train a Q-learning agent on the environment and return the learned Q-table."""
    # Why: Seeding once at the start of training guarantees reproducible trajectories and Q-tables.
    if seed is not None:
        random.seed(seed)

    q_table = init_q_table(env)
    epsilon = eps_start

    for _ in range(episodes):
        state = env.start_state
        for _ in range(max_steps):
            if is_terminal(env, state):
                break
            action = choose_action(q_table, state, epsilon)
            reward, next_state, terminal_value = env_step(env, state, action)
            q_update(q_table, state, action, reward, next_state, alpha, gamma, terminal_value)
            state = next_state
            if is_terminal(env, state):
                break
        epsilon = decay_epsilon(epsilon, eps_decay, eps_min)

    return q_table


def extract_policy(q_table, env):
    """Extract a deterministic greedy policy mapping each non-terminal, non-obstacle state to an action."""
    # Why: Selecting the first action from best_actions breaks ties deterministically in ACTIONS order.
    policy = {}
    for r in range(env.rows):
        for c in range(env.cols):
            state = (r, c)
            if state != env.obstacle and not is_terminal(env, state):
                policy[state] = best_actions(q_table, state)[0]
    return policy


def print_policy(policy, env):
    """Print the learned policy as a 4x4 grid of directional arrows, X for obstacle, and T for terminals."""
    # Why: Visualizing the 4x4 grid allows quick inspection of the robot's navigation choices.
    for r in range(env.rows):
        row_cells = []
        for c in range(env.cols):
            state = (r, c)
            if state == env.obstacle:
                row_cells.append("X")
            elif is_terminal(env, state):
                row_cells.append("T")
            else:
                row_cells.append(ARROW_MAP[policy[state]])
        print(" ".join(row_cells))


def simulate(policy, env, max_steps=DEFAULT_MAX_STEPS):
    """Simulate one trajectory from start_state using the given policy and return visited states."""
    # Why: A single rollout illustrates how the learned policy performs under stochastic transitions.
    state = env.start_state
    visited = [state]

    for step in range(1, max_steps + 1):
        if is_terminal(env, state):
            break
        action = policy[state]
        _, next_state, _ = env_step(env, state, action)
        print(f"Step {step}: action={action} -> state={next_state}")
        state = next_state
        visited.append(state)
        if is_terminal(env, state):
            break

    if is_terminal(env, state):
        payoff = terminal_payoff(env, state)
        if payoff > 0:
            print(f"Outcome: Reached recharge spot at {state} (payoff {payoff})")
        else:
            print(f"Outcome: Reached trap at {state} (payoff {payoff})")
    else:
        print(f"Outcome: Stopped at max_steps ({max_steps}) at state {state}")

    return visited


def compare_policies(q_policy, env, gamma):
    """Compare the Q-learning policy against the MDP value iteration baseline and return differing states."""
    # Evaluation only: the MDP baseline uses true T and R models, whereas the Q-learning learner never does.
    mdp = MDP(env, discount=gamma)
    mdp.value_iteration()
    vi_policy = mdp.extract_policy()

    differing = [state for state in sorted(q_policy) if q_policy[state] != vi_policy.get(state)]
    print(f"States differing from value iteration: {len(differing)} {differing}")
    return differing


if __name__ == "__main__":
    for cost in LIVING_COSTS:
        print(f"\n=== Living Cost: {cost} ===")
        environment = GridnEnvironment(living_cost=cost)
        learned_q = train(environment, seed=SEED)
        learned_policy = extract_policy(learned_q, environment)
        print_policy(learned_policy, environment)
        compare_policies(learned_policy, environment, DEFAULT_GAMMA)
        simulate(learned_policy, environment)
