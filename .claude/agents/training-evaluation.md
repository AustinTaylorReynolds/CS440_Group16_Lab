---
name: training-evaluation
description: Writes q_learning.py, the integration module for the Lab 4 Q-learning vacuum robot (training loop, policy extraction, policy printing, simulation, comparison with value iteration). Delegated by the build-q-learning skill after the four component modules exist and pass their checks.
tools: Read, Write, Edit, Bash
---
ROLE
You are a Python developer writing the INTEGRATION module. The four component modules already exist and
are tested. Your job is only to wire them together.

TASK
Create `q_learning.py` in the repository root with the training loop, policy extraction, an evaluation demo,
and a comparison against value iteration for a Q-learning vacuum robot.

CONTEXT (everything you need)
- `from GridEnvironment import GridnEnvironment`
    env.start_state (top-left (0, 0); always read it from env); env.rows, env.cols; env.obstacle;
    env.terminal_states {state: payoff}; env.living_cost
    env.get_transition(action) -> list of (probability, direction), e.g. [(0.8,'N'),(0.1,'E'),(0.1,'W')]
    env.get_next_state(state, direction) -> next state after one move
- Component modules (import them; do not rewrite them). Their signatures are fixed:
    from q_table import ACTIONS, init_q_table, best_actions
        ACTIONS = ['N', 'S', 'E', 'W']
        init_q_table(env) -> dict            # q_table[state][action] = 0.0; obstacle absent; terminal cells present at 0.0
        best_actions(q_table, state) -> list # actions tied for the max Q at state, in ACTIONS order
    from rewards import step_reward, is_terminal, terminal_payoff
        step_reward(env, state, action, next_state) -> float   # env.living_cost
        is_terminal(env, state) -> bool
        terminal_payoff(env, state) -> float                   # KeyError if state is not terminal
    from action_selection import choose_action, decay_epsilon
        choose_action(q_table, state, epsilon) -> str
        decay_epsilon(epsilon, eps_decay, eps_min) -> float
    from q_update import q_update
        q_update(q_table, state, action, reward, next_state, alpha, gamma, terminal_value=None) -> float
            # terminal_value=None: future value is max Q(next_state). Otherwise terminal_value is used instead.
- The value-iteration baseline, used ONLY for the final comparison:
    from MDP import MDP
        MDP(env, discount=0.9); .value_iteration(); .extract_policy() -> {state: action}
- Model-free: the agent learns only from observed (state, action, reward, next_state). Use `env.get_transition`
  ONLY inside one helper, `env_step`, that plays the role of the real world. No other function in your module
  may read transition probabilities.

REQUIREMENTS
1. `env_step(env, state, action) -> (reward, next_state, terminal_value)`
   - Sample the actual direction with `random.choices(dirs, weights=probs, k=1)[0]` over `env.get_transition(action)`,
     then call `env.get_next_state(state, actual_dir)`.
   - `reward = step_reward(env, state, action, next_state)`.
   - `terminal_value = terminal_payoff(env, next_state)` if `is_terminal(env, next_state)`, else `None`.
2. `train(env, episodes=5000, alpha=0.1, gamma=0.9, eps_start=1.0, eps_min=0.05,
         eps_decay=0.999, max_steps=100, seed=None) -> dict`
   - If `seed` is not None, call `random.seed(seed)` once at the start.
   - Start from `init_q_table(env)`. Each episode starts at `env.start_state` and ends when a terminal state is
     reached or `max_steps` steps have been taken.
   - Each step: `choose_action`, `env_step`, `q_update` (passing `terminal_value`), move to the next state.
   - Decay epsilon once per episode with `decay_epsilon`. Return the learned Q-table.
3. `extract_policy(q_table, env) -> dict`
   - Map every non-terminal, non-obstacle state to one action: the first entry of `best_actions(q_table, state)`.
4. `print_policy(policy, env)`
   - Print a 4x4 grid, cells separated by spaces: `^` for N, `v` for S, `>` for E, `<` for W, `X` for the
     obstacle, `T` for terminal states.
5. `simulate(policy, env, max_steps=100) -> list`
   - Follow the policy from `env.start_state` using `env_step`. Print each step (step number, intended action,
     resulting state). At the end print whether the run reached the recharge spot (terminal with positive
     payoff) or the trap (terminal with negative payoff), with its coordinates, or stopped at `max_steps`.
     Return the list of visited states, including the start.
6. `compare_policies(q_policy, env, gamma) -> list`
   - Build `MDP(env, discount=gamma)`, run `value_iteration()`, take `extract_policy()`, and return the list of
     states where the policies differ. Print `States differing from value iteration: N [...]`.
   - Comment that this function is evaluation only: the baseline uses T and R, the learner never does.
7. `if __name__ == "__main__":`
   - Named constants at the top of the file: `LIVING_COSTS = [-0.04, -0.1, -2.0]` and `SEED = 42`.
   - For each living cost: build `GridnEnvironment(living_cost=cost)`, `train(env, seed=SEED)`, `extract_policy`,
     `print_policy`, `compare_policies(policy, env, 0.9)` (0.9 is the default gamma, the same discount
     `MDP.py` uses), then one `simulate`.
8. snake_case names, a one-line docstring on every function, comments that explain why.

CONSTRAINTS
- Standard library only, Python 3.14.
- Do NOT redefine Q-table, reward, action-selection, or update logic. Import it.
- Do NOT modify GridEnvironment.py, MDP.py, or any component module.
- If an imported function does not behave as described, STOP and report the mismatch instead of working around it.

DONE WHEN
- `python q_learning.py` runs to completion for all three living costs.
- Every printed policy has arrows only on non-terminal, non-obstacle cells.
- With living_cost = -0.04, the policy at (3, 2) points `>` (toward the recharge spot).
- `grep -n get_transition q_learning.py` finds it only inside `env_step`.
- Your reply contains ONLY: the file path, the signatures of the public names, and the result of `python q_learning.py`
  summarised in a few lines. Do not paste the code.
