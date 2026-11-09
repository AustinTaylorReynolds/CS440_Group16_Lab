# Context Filter

The Context Filter sits between the orchestrator and every sub-agent. It prevents the full conversation
history from leaking, so each agent's knowledge is limited to its own task and it cannot get confused by
unrelated details (context confusion).

| Sub-agent | Receives ONLY | Withheld |
|-----------|---------------|----------|
| 01 Q-table setup | Its prompt; grid size, obstacle, action list | Rewards, update rule, training, hyperparameters |
| 02 Reward logic | Its prompt; `env.living_cost`, `env.terminal_states`, reward convention | Q-table layout, action selection, learning code |
| 03 Action selection | Its prompt; Q-table shape (nested dict) | Environment, rewards, update rule, training |
| 04 Q-update rule | Its prompt; Q-table shape, reward convention, `alpha`/`gamma` | Action selection, episode loop, evaluation |
| 05 Training + evaluation | Its prompt; signatures of components 01–04 | The internals of components 01–04 |

## Filter rules

1. Pass the prompt file verbatim. Do not add chat history or commentary.
2. Never pass another sub-agent's prompt or source code. Only signatures may cross the boundary.
3. Never pass the lab handout, grading criteria, or earlier failed attempts.
4. A sub-agent that needs information it was not given must say so, not guess.
5. Each sub-agent runs in its own fresh session.
