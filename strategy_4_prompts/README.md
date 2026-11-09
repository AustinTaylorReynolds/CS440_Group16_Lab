works on python 3.14.3

# CS440 Group 16 Lab 4: Vacuum Robot (Q-Learning), Context Engineering Strategies 1 and 4

A vacuum robot navigates a 4x4 grid. Lab 4 will have it learn with Q-learning without knowing the transition
(T) or reward (R) models in advance. This repository is configured with context engineering
**Strategy 1** and **Strategy 4**; the Q-learning implementation itself comes later.

## Where to look

| Strategy | Location | What it is |
|----------|----------|------------|
| **Strategy 1: Write (Persistent Memory)** | [`CLAUDE.md`](./CLAUDE.md), [`context/`](./context/), [`strategy_1_user_memory/`](./strategy_1_user_memory/) | The three memory tiers from the lecture slide (see below) |
| **Strategy 4: Isolation via Sub-Agents** | [`strategy_4_prompts/`](./strategy_4_prompts/) | Orchestrator prompt, context filter, and five isolated sub-agent prompts |

### Strategy 1: the three tiers

| Tier (from the slide) | File here |
|-----------------------|-----------|
| Project Memory (`./CLAUDE.md`) | `CLAUDE.md`: architecture, code standards, workflow rules, shared via version control |
| User Memory (`~/.claude/CLAUDE.md`) | `strategy_1_user_memory/CLAUDE.md`: example of personal preferences (copy it to `~/.claude/` to use it) |
| Dynamic Imports (`@context.md`) | `context/environment.md`, `context/q_learning.md`, `context/verification.md`, imported from `CLAUDE.md` with `@` |

### Strategy 4: orchestrator, filter, sub-agents

`00_orchestrator.txt` (main agent) divides the Q-learning task. `context_filter.md` defines what each
sub-agent may see. `01`–`05` are the isolated sub-agent prompts: Q-table setup, reward logic, action
selection, Q-update rule, and training/evaluation. See `strategy_4_prompts/README.md` for the run order
and interface contract.

## Project structure

```
.
├── CLAUDE.md                          # Strategy 1, tier 1: project memory
├── README.md                          # this file
├── context/                           # Strategy 1, tier 3: dynamic imports
│   ├── environment.md
│   ├── q_learning.md
│   └── verification.md
├── strategy_1_user_memory/            # Strategy 1, tier 2: example user memory
│   └── CLAUDE.md
├── strategy_4_prompts/                # Strategy 4: isolation via sub-agents
│   ├── README.md
│   ├── 00_orchestrator.txt
│   ├── context_filter.md
│   ├── 01_q_table_setup.txt
│   ├── 02_reward_logic.txt
│   ├── 03_action_selection.txt
│   ├── 04_q_update_rule.txt
│   └── 05_training_and_evaluation.txt
├── GridEnvironment.py                 # environment (GridnEnvironment)
├── MDP.py                             # value-iteration baseline
├── hill.py                            # hill climbing (earlier lab)
└── simulated.py                       # simulated annealing (earlier lab)
```

## Running the existing code

- Hill climbing: `python hill.py`
- Simulated annealing: `python simulated.py`
  The objective function just reads the matrix because that gives the score of the location. We chose 0.8 for the cooling rate by these steps:
  - started with 0.995 to see it stay at a high temperature for long and found it ran many steps
  - halved it to 0.5 and found it was getting close but not quite
  - added 0.1 at a time and tested until 0.8, where it converged to the optimal state most of the time
- Value iteration: `python MDP.py` (living costs -0.04, -0.1, -2.0)
