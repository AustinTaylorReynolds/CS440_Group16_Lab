# Q-Learning Rules (imported by CLAUDE.md)

## Model-free requirement
The lab states the agent does not have T and R as expected, so Q-learning must be **model-free**:
- The learning code must never read transition probabilities to plan or to compute expectations.
- `env.get_transition()` may be used ONLY inside the single function that simulates "the world"
  responding to an action (sampling the real outcome). That function stands in for the physical robot.
- The agent learns only from observed tuples `(state, action, reward, next_state)`.

## Update rule (the only one allowed)
`Q(s,a) <- Q(s,a) + alpha * (target - Q(s,a))`, where `target = reward + gamma * max_a' Q(s',a')`.

Reward convention (matches `MDP.py` so results are comparable): every step yields `env.living_cost`.
If `s'` is terminal, the future-value term is that state's payoff from `env.terminal_states`
instead of `max Q`.

## Q-table
Nested dict `q_table[state][action] -> float`, initialized to `0.0`, with no entry for the obstacle.
Terminal-state entries stay `0.0` and are never updated.

## Defaults (named constants, not magic numbers)
`alpha = 0.1`, `gamma = 0.9`, `epsilon` starts at `1.0` and decays to a floor of `0.05`,
`episodes = 5000`, `max_steps = 100` per episode.

## Exploration and reproducibility
- Epsilon-greedy; break ties between equal Q-values randomly.
- Sample the actual direction with `random.choices(dirs, weights=probs, k=1)[0]`, as `MDP.simulated_path` does.
- Accept an optional `seed` and call `random.seed(seed)` once at the start of training.
- An episode ends at a terminal state or after `max_steps`.
