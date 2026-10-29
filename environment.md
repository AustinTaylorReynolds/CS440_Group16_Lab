# Environment Context (imported by CLAUDE.md)

Lab 4 environment (from the lab sheet). Cells are `(row, col)`, `(0, 0)` is the top-left.

```
start  0   0   0
  0    X   0   0
  0    0   0   0
  0   -1   0  10
```

- Start state: `(0, 0)` (top-left). Read it from `env.start_state`; never hardcode it.
- Obstacle (wall): `(1, 1)`. It is never a valid state.
- Terminal states: `(3, 1)` = trap, `-1`; `(3, 3)` = recharge spot, `+10`.
- Actions: `'N'`, `'S'`, `'E'`, `'W'`.
- Movement is stochastic: 80% the intended direction, 10% each perpendicular direction.
  Hitting a wall, the obstacle, or the grid edge leaves the agent where it is.
- `living_cost` is a constructor argument. Test values: `-0.04`, `-0.1`, `-2.0`.

## API in `GridEnvironment.py`

- `env.rows`, `env.cols`, `env.start_state`, `env.obstacle`, `env.terminal_states` (`{state: payoff}`), `env.living_cost`
- `env.get_transition(action)` -> `[(prob, direction), ...]`
- `env.get_next_state(state, direction)` -> next state

## Approved exception to "do not modify existing files"

`GridEnvironment.py` still has `start_state = (0, 3)` (and "start" at the top right of `self.grid`) from Lab 3.
The Lab 4 sheet puts the start at the top-left. Updating `start_state` to `(0, 0)` and moving the `"start"`
marker in `self.grid` is the only permitted edit to that file. Do it once, then re-run `python MDP.py`.
