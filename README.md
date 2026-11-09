works on python 3.14.3

# CS440 Group 16 Lab 4: Vacuum Robot (Q-Learning)

A vacuum robot navigates a 4x4 grid with a stochastic (80/10/10) movement model, a living cost, a trap (-1) and a
recharge spot (+10). It does not know the transition (T) or reward (R) models in advance, so it learns a policy
with **Q-learning** from experience only. We compare the learned policy with the value-iteration policy in
`MDP.py` for living costs -0.04, -0.1, and -2.0.

The repository is set up with context engineering **Strategy 1** and **Strategy 4**, and uses three Claude Code
features: **hooks, skills, and sub-agents** (MCP is not used).

## Claude Code features used

| Feature | Location | What it does |
|---------|----------|--------------|
| **Hook** | `.claude/settings.json`, `.claude/hooks/protect_files.py` | A PreToolUse hook blocks edits to `GridEnvironment.py`, `MDP.py`, `hill.py`, and `simulated.py`, which turns the "do not modify existing files" rule into something enforced |
| **Skills** | `.claude/skills/build-q-learning/`, `.claude/skills/verify-lab/` | `/build-q-learning` is the orchestrator: it delegates the components, checks each against the interface contract, and integrates. `/verify-lab` runs the verification checklist and reports how many states differ from value iteration |
| **Sub-agents** | `.claude/agents/` | One isolated agent per component: `q-table-setup`, `reward-logic`, `action-selection`, `q-update-rule`, `training-evaluation` |

## Context engineering (Strategies 1 and 4)

| Strategy | Location | What it is |
|----------|----------|------------|
| **Strategy 1: Write (Persistent Memory)** | [`CLAUDE.md`](./CLAUDE.md), [`context/`](./context/), [`strategy_1_user_memory/`](./strategy_1_user_memory/) | The three memory tiers from the lecture slide |
| **Strategy 4: Isolation via Sub-Agents** | [`.claude/agents/`](./.claude/agents/), [`strategy_4_prompts/`](./strategy_4_prompts/) | The isolated sub-agents, plus the orchestrator plan, context filter, and interface contract |

| Tier (from the slide) | File here |
|-----------------------|-----------|
| Project Memory (`./CLAUDE.md`) | `CLAUDE.md`: architecture, code standards, workflow rules, shared via version control |
| User Memory (`~/.claude/CLAUDE.md`) | `strategy_1_user_memory/CLAUDE.md`: example of personal preferences (copy it to `~/.claude/` to use it) |
| Dynamic Imports (`@context.md`) | `context/environment.md`, `context/q_learning.md`, `context/verification.md`, imported from `CLAUDE.md` with `@` |

See `strategy_4_prompts/README.md` for the run order and the interface contract between the components.

## Project structure

```
.
├── CLAUDE.md                          # Strategy 1, tier 1: project memory
├── README.md                          # this file
├── .claude/                           # Claude Code features
│   ├── settings.json                  # registers the hook
│   ├── hooks/protect_files.py         # blocks edits to protected files
│   ├── skills/
│   │   ├── build-q-learning/          # orchestrator (SKILL.md, check_contract.py)
│   │   └── verify-lab/                # verification checklist (SKILL.md)
│   └── agents/                        # isolated sub-agents
│       ├── q-table-setup.md
│       ├── reward-logic.md
│       ├── action-selection.md
│       ├── q-update-rule.md
│       └── training-evaluation.md
├── context/                           # Strategy 1, tier 3: dynamic imports
│   ├── environment.md
│   ├── q_learning.md
│   └── verification.md
├── strategy_1_user_memory/            # Strategy 1, tier 2: example user memory
│   └── CLAUDE.md
├── strategy_4_prompts/                # Strategy 4 design notes
│   ├── README.md                      # run order and interface contract
│   ├── 00_orchestrator.txt
│   └── context_filter.md
├── GridEnvironment.py                 # environment (GridnEnvironment)
├── MDP.py                             # value-iteration baseline
├── q_table.py                         # written by the q-table-setup agent
├── rewards.py                         # written by the reward-logic agent
├── action_selection.py                # written by the action-selection agent
├── q_update.py                        # written by the q-update-rule agent
├── q_learning.py                      # written by the training-evaluation agent
├── hill.py                            # hill climbing (earlier lab)
└── simulated.py                       # simulated annealing (earlier lab)
```

## How to run

- Q-learning (all three living costs, with the comparison against value iteration): `python q_learning.py`
- Value iteration: `python MDP.py` (living costs -0.04, -0.1, -2.0)
- Rebuild the Q-learning code with Claude Code: start it in the repository root, run `/build-q-learning`, then `/verify-lab`.
- Hill climbing: `python hill.py`
- Simulated annealing: `python simulated.py`
  The objective function just reads the matrix because that gives the score of the location. We chose 0.8 for the cooling rate by these steps:
  - started with 0.995 to see it stay at a high temperature for long and found it ran many steps
  - halved it to 0.5 and found it was getting close but not quite
  - added 0.1 at a time and tested until 0.8, where it converged to the optimal state most of the time

## Hyperparameters

| Parameter | Value | Why |
|-----------|-------|-----|
| Living cost | -0.04, -0.1, -2.0 | The same test values as the value-iteration lab, so the two methods are directly comparable |
| Discount factor (gamma) | 0.9 | Matches the discount in `MDP.py`, so both methods optimise the same objective |
| Learning rate (alpha) | 0.1 | The 80/10/10 slips make each sample noisy, so small steps average the noise out |
| Epsilon | starts at 1.0, floor 0.05, multiplied by 0.999 each episode | Explore fully at first, then mostly exploit. The floor is reached after about 3,000 of the 5,000 episodes and keeps 5% exploration |
| Episodes, max steps | 5000, 100 | Enough episodes for every state to be visited many times. The step cap stops a run that wanders when the living cost is mild |
| Seed | 42 | Makes the recorded run reproducible |
