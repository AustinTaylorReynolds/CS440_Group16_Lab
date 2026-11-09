# Verification Checklist (imported by CLAUDE.md)

Run these before claiming a task is done:

1. `python MDP.py` still runs.
2. The learned policy prints as a 4x4 grid of arrows (`^ v > <`), `X` for the obstacle, `T` for terminals.
3. For each living cost in `[-0.04, -0.1, -2.0]`, compare the Q-learning policy with `MDP.extract_policy()`
   and report how many states differ.
4. Run one simulated path per living cost from `env.start_state` and report whether it ended at `(3, 3)` or `(3, 1)`.
5. Confirm no learning code reads `env.get_transition()` (model-free check).
