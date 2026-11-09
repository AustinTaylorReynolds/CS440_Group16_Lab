# CLAUDE.md — Project Memory (Strategy 1: Write / Persistent Memory)

Tier 1 of the Strategy 1 memory architecture: architecture, code standards, and business rules,
shared with the whole team through version control. Claude Code reads this file at the start of every session.

## Project

CS 440 Lab 4, Group 16: a vacuum robot that learns to navigate a 4x4 grid with **Q-learning**
(reinforcement learning). The robot does NOT know the transition model (T) or reward model (R) in advance.
It must learn a policy only from experience, by acting in the environment and observing what happens.
The Q-learning code is built by five isolated sub-agents (`.claude/agents/`) and its policies are compared
with the value-iteration baseline in `MDP.py`.

## File Map

| File | Purpose |
|------|---------|
| `GridEnvironment.py` | Environment (`GridnEnvironment`): grid layout, slip model, movement logic |
| `MDP.py` | Value-iteration baseline (it uses T and R, so it is the reference to compare against) |
| `hill.py`, `simulated.py` | Earlier labs (separate dirt-score floor); do not touch |
| `q_table.py`, `rewards.py`, `action_selection.py`, `q_update.py`, `q_learning.py` | Q-learning components, written by the sub-agents. The interface contract is in `strategy_4_prompts/README.md` |
| `context/` | Tier 3: dedicated context files imported below |
| `strategy_1_user_memory/` | Tier 2: example of a personal `~/.claude/CLAUDE.md` |
| `strategy_4_prompts/` | Strategy 4 design notes: orchestrator plan, context filter, interface contract |
| `.claude/` | Claude Code features: a hook, two skills, five sub-agents |

## Dynamic Imports (Tier 3: dedicated context files)

Detailed, task-specific context lives in separate files and is imported here instead of being pasted in.

@context/environment.md
@context/q_learning.md
@context/verification.md

## Code Standards

1. **Do not modify existing files** unless the user asks. New code goes in new files.
   A hook (`.claude/settings.json`) blocks edits to `GridEnvironment.py`, `MDP.py`, `hill.py`, and `simulated.py`.
2. **Reuse the environment.** Import `GridnEnvironment`; never re-implement grid movement or slip logic.
3. **Keep the class name `GridnEnvironment`** (including the spelling).
4. **Python 3.14.3**, standard library only. No numpy, pandas, or RL libraries.
5. State is a `(row, col)` tuple; actions are the list `['N', 'S', 'E', 'W']`, defined once in `q_table.py` and imported.
6. snake_case names, a one-line docstring on every function, and comments that explain *why*, not *what*.

## Workflow Rules

- Make small changes and run the code after each one.
- If a requirement is ambiguous, ask instead of guessing.
- Do not add unrequested features (GUI, plotting libraries, deep Q-networks).
- Keep `README.md` current whenever files are added, renamed, or removed.
- Build the Q-learning code with `/build-q-learning`. Check it with `/verify-lab`.

## Claude Code Features (Lab 4, part 2)

- **Hook:** `.claude/hooks/protect_files.py`, registered in `.claude/settings.json`, blocks edits to the protected files.
- **Skills:** `build-q-learning` (the orchestrator) and `verify-lab` (the verification checklist), in `.claude/skills/`.
- **Sub-agents:** one per component, in `.claude/agents/`.

## Strategy Map

- **Strategy 1 (Write):** this file (tier 1), `strategy_1_user_memory/` (tier 2), `context/` (tier 3).
- **Strategy 4 (Isolation):** `.claude/agents/` holds the isolated sub-agents, `.claude/skills/build-q-learning/`
  is the orchestrator, and `strategy_4_prompts/` documents the design and the interface contract.
