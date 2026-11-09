# CLAUDE.md — Project Memory (Strategy 1: Write / Persistent Memory)

Tier 1 of the Strategy 1 memory architecture: architecture, code standards, and business rules,
shared with the whole team through version control. Claude Code reads this file at the start of every session.

## Project

CS 440 Lab 4, Group 16: a vacuum robot that learns to navigate a 4x4 grid with **Q-learning**
(reinforcement learning). The robot does NOT know the transition model (T) or reward model (R) in advance.
It must learn a policy only from experience, by acting in the environment and observing what happens.
The Q-learning implementation itself comes later; this repository holds the context-engineering setup
(Strategies 1 and 4) used to build it.

## File Map

| File | Purpose |
|------|---------|
| `GridEnvironment.py` | Environment (`GridnEnvironment`): grid layout, slip model, movement logic |
| `MDP.py` | Value-iteration baseline (it uses T and R, so it is the reference to compare against) |
| `hill.py`, `simulated.py` | Earlier labs (separate dirt-score floor); do not touch |
| `context/` | Tier 3: dedicated context files imported below |
| `strategy_1_user_memory/` | Tier 2: example of a personal `~/.claude/CLAUDE.md` |
| `strategy_4_prompts/` | Strategy 4: orchestrator, context filter, and isolated sub-agent prompts |

## Dynamic Imports (Tier 3: dedicated context files)

Detailed, task-specific context lives in separate files and is imported here instead of being pasted in.

@context/environment.md
@context/q_learning.md
@context/verification.md

## Code Standards

1. **Do not modify existing files** unless the user asks. New code goes in new files.
   (One approved exception is listed in `context/environment.md`.)
2. **Reuse the environment.** Import `GridnEnvironment`; never re-implement grid movement or slip logic.
3. **Keep the class name `GridnEnvironment`** (including the spelling).
4. **Python 3.14.3**, standard library only. No numpy, pandas, or RL libraries.
5. State is a `(row, col)` tuple; actions are the list `['N', 'S', 'E', 'W']`, defined once and imported.
6. snake_case names, a one-line docstring on every function, and comments that explain *why*, not *what*.

## Workflow Rules

- Make small changes and run the code after each one.
- If a requirement is ambiguous, ask instead of guessing.
- Do not add unrequested features (GUI, plotting libraries, deep Q-networks).
- Keep `README.md` current whenever files are added, renamed, or removed.

## Strategy Map

- **Strategy 1 (Write):** this file (tier 1), `strategy_1_user_memory/` (tier 2), `context/` (tier 3).
- **Strategy 4 (Isolation):** `strategy_4_prompts/`, where `00_orchestrator.txt` splits the work and
  `context_filter.md` controls what each sub-agent may see.
