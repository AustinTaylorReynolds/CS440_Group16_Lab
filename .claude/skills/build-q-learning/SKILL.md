---
name: build-q-learning
description: Orchestrates the Lab 4 build of the Q-learning vacuum robot by delegating its five components (q_table.py, rewards.py, action_selection.py, q_update.py, q_learning.py) to isolated sub-agents, checking each against the interface contract, then integrating. Use whenever the user asks to build, implement, generate, or rebuild the Q-learning code, to run the orchestrator, or to dispatch the sub-agents, even if they do not name the individual files.
---

# Build Q-learning with isolated sub-agents

You are the ORCHESTRATOR. You receive the complex task, divide it, and hand each piece to a sub-agent. You do
not write component code yourself, and you are the only agent that sees the whole task.

Complex task: implement Q-learning for a vacuum robot on a 4x4 grid with a stochastic (80/10/10) movement
model, a living cost, a trap (-1) and a recharge spot (+10). The robot does not have T and R in advance.
Compare the learned policy with the value-iteration policy in `MDP.py` for living costs -0.04, -0.1, -2.0.

## 1. Divide

| Component | Sub-agent | File |
|-----------|-----------|------|
| Q-table setup | `q-table-setup` | `q_table.py` |
| Reward logic | `reward-logic` | `rewards.py` |
| Action selection | `action-selection` | `action_selection.py` |
| Q-learning update rule | `q-update-rule` | `q_update.py` |
| Training and evaluation | `training-evaluation` | `q_learning.py` |

The interface contract between them is in `strategy_4_prompts/README.md`.

## 2. Dispatch (the Context Filter)

Delegate to the first four sub-agents in one batch, so they run in parallel. They share only the contract, not
code, so none of them has to wait for another. Each delegation message is exactly:

> Implement your component as described in your instructions.

Add nothing else: no chat history, no other component's spec, no lab text. Each agent's definition file in
`.claude/agents/` already holds everything it is allowed to know, and anything you add leaks context.

## 3. Collect and check

For each returned reply, check only the interface, never the internals:

1. `python <file>` runs the module's built-in self-checks.
2. `python .claude/skills/build-q-learning/check_contract.py <module>` (for example `q_table`) checks names,
   arguments, and shapes. Run it from the repository root.

If an agent fails a check, fix that one agent's definition file, then re-dispatch only that agent. Never patch one
component by editing another's file. Record which agents needed a re-run.

## 4. Integrate

When all four modules pass, delegate to `training-evaluation` (same one-line message). Then run
`python q_learning.py` and run the `verify-lab` skill.

Report: which living cost produced which policy, how many states differ from value iteration (and which), and any
sub-agent that needed a re-run.

## Rules

- Keep your own context small: store file paths and signatures, not code listings.
- `GridEnvironment.py`, `MDP.py`, `hill.py`, and `simulated.py` are protected by a hook. Do not try to edit them.
