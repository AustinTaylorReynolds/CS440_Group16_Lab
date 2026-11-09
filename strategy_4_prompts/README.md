# Strategy 4: Isolation via Sub-Agents

The Q-learning task is split into five components. Each is built by a sub-agent that knows only its own job,
so no agent can be confused by details that belong to another component (context confusion).

## Where things live

| What | Location |
|------|----------|
| The five isolated sub-agents (their whole spec is the file) | `.claude/agents/` |
| The orchestrator (main agent) | `.claude/skills/build-q-learning/SKILL.md` |
| Contract checker the orchestrator runs | `.claude/skills/build-q-learning/check_contract.py` |
| Design notes: original orchestrator plan and what each agent may see | `00_orchestrator.txt`, `context_filter.md` (this folder) |

`00_orchestrator.txt` is the original plan. The skill supersedes it in one way: the update rule (04) now runs
in parallel with 01 to 03, because the contract below fixes everything it needs.

## Run order

In Claude Code, started from the repository root: `/build-q-learning`, then `/verify-lab`.

1. Delegate 01, 02, 03, and 04 in one batch (parallel).
2. Check each result: run its `__main__` self-checks, then `python .claude/skills/build-q-learning/check_contract.py <module>`.
3. Delegate 05 once 01 to 04 pass.
4. Run `python q_learning.py` and the verification checklist.

If an agent fails a check, fix that agent's definition file and re-run only that agent.

## Components

| # | Sub-agent (`.claude/agents/`) | Writes | Sees |
|---|-------------------------------|--------|------|
| 01 | `q-table-setup` | `q_table.py` | grid size, obstacle, action list |
| 02 | `reward-logic` | `rewards.py` | `env.living_cost`, `env.terminal_states`, reward convention |
| 03 | `action-selection` | `action_selection.py` | Q-table shape only |
| 04 | `q-update-rule` | `q_update.py` | Q-table shape, reward convention, alpha and gamma |
| 05 | `training-evaluation` | `q_learning.py` | the signatures below, not the internals of 01 to 04 |

The Context Filter is enforced by construction: each definition file holds only what its row allows, and the
orchestrator's delegation message is the fixed line "Implement your component as described in your instructions."

## Interface contract

A state is a `(row, col)` tuple. The Q-table is a nested dict `q_table[state][action] -> float`.

| Module | Name | Signature | Meaning |
|--------|------|-----------|---------|
| `q_table.py` | `ACTIONS` | `['N', 'S', 'E', 'W']` | the only definition of the action list |
| | `init_q_table` | `(env) -> dict` | every cell except the obstacle, all actions at `0.0`; terminal cells present |
| | `best_actions` | `(q_table, state) -> list` | actions tied for the max Q at `state`, in `ACTIONS` order |
| `rewards.py` | `step_reward` | `(env, state, action, next_state) -> float` | `env.living_cost` on every step |
| | `is_terminal` | `(env, state) -> bool` | state is in `env.terminal_states` |
| | `terminal_payoff` | `(env, state) -> float` | payoff of a terminal state; `KeyError` otherwise |
| `action_selection.py` | `choose_action` | `(q_table, state, epsilon) -> str` | epsilon-greedy, random tie-break |
| | `decay_epsilon` | `(epsilon, eps_decay, eps_min) -> float` | `max(eps_min, epsilon * eps_decay)` |
| `q_update.py` | `q_update` | `(q_table, state, action, reward, next_state, alpha, gamma, terminal_value=None) -> float` | one Q-learning update; `terminal_value` replaces `max Q(next_state)` when the next state is terminal |
| `q_learning.py` | `env_step` | `(env, state, action) -> (reward, next_state, terminal_value)` | the simulated "real world" |
| | `train`, `extract_policy`, `print_policy`, `simulate`, `compare_policies` | see `.claude/agents/training-evaluation.md` | |

## Model-free rule

The learner only sees observed `(state, action, reward, next_state)` tuples. `env.get_transition()` is read in
exactly one place, `env_step` in `q_learning.py`, which stands in for the physical robot. `compare_policies`
uses `MDP.py` (which does use T and R) for evaluation only.
