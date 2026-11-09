---
name: verify-lab
description: Runs the Lab 4 verification checklist for the Q-learning vacuum robot and reports how each learned policy compares with value iteration. Use whenever the user asks to verify, check, validate, or compare the Q-learning results, asks whether Lab 4 is done, or has just changed q_learning.py or any component module (q_table, rewards, action_selection, q_update), even if they never mention the checklist.
---

# Verify Lab 4

The checklist itself lives in `context/verification.md`. This skill is the procedure for running it and the
format for reporting. Run the steps in order and report; do not fix anything you find, because the fix may
belong to a different component and the orchestrator decides which sub-agent to re-run.

## Steps

1. **Baseline still runs.** `python MDP.py` must finish without errors. It is the reference we compare against.
2. **Training runs.** `python q_learning.py` must finish for living costs -0.04, -0.1, and -2.0. Keep the output.
3. **Policy grids are well formed.** Each printed grid is 4x4, arrows (`^ v > <`) appear only on
   non-terminal, non-obstacle cells, `X` is at (1, 1), and `T` is at (3, 1) and (3, 3). At living cost -0.04 the
   arrow at (3, 2) must be `>`.
4. **Compare with value iteration.** `q_learning.py` prints `States differing from value iteration: N [...]` for
   each living cost (from `compare_policies`). Record N and the states. If those lines are missing, run this
   without editing any project file:

   ```python
   from GridEnvironment import GridnEnvironment
   from q_learning import train, extract_policy, compare_policies

   for cost in (-0.04, -0.1, -2.0):
       env = GridnEnvironment(living_cost=cost)
       compare_policies(extract_policy(train(env, seed=42), env), env, 0.9)
   ```
5. **Simulated paths.** Confirm each living cost has one simulated run from `env.start_state` and note whether it
   ended at (3, 3) (recharge) or (3, 1) (trap). The dynamics are stochastic, so one run is an example, not a result.
6. **Model-free check.** Run `grep -n "get_transition" *.py`. The only acceptable hits are the definition in
   `GridEnvironment.py`, the baseline in `MDP.py`, and the single `env_step` helper in `q_learning.py`. A hit in
   `q_table.py`, `rewards.py`, `action_selection.py`, or `q_update.py` is a failure.

## Report format

Finish with one table, then a short list of anything that failed or looked odd:

| Living cost | Simulated run ended at | States differing from value iteration | Which states |
|-------------|------------------------|---------------------------------------|--------------|

A few disagreements are normal. Q-learning estimates action values from noisy samples, so two actions with nearly
equal values can swap places between runs. Say which differing states look like close calls if you can tell.
If steps 1 to 6 all pass, say so plainly.
