"""Check the Q-learning component modules against the interface contract (names, arguments, shapes)."""
import importlib
import inspect
import os
import sys
from types import SimpleNamespace

# Why this exists: the orchestrator checks ONLY the interface, never the sub-agents' internals.
CONTRACT = {
    "q_table": {"init_q_table": ["env"], "best_actions": ["q_table", "state"]},
    "rewards": {
        "step_reward": ["env", "state", "action", "next_state"],
        "is_terminal": ["env", "state"],
        "terminal_payoff": ["env", "state"],
    },
    "action_selection": {
        "choose_action": ["q_table", "state", "epsilon"],
        "decay_epsilon": ["epsilon", "eps_decay", "eps_min"],
    },
    "q_update": {
        "q_update": ["q_table", "state", "action", "reward", "next_state", "alpha", "gamma", "terminal_value"],
    },
}

STAND_IN_ENV = SimpleNamespace(
    rows=4, cols=4, obstacle=(1, 1), living_cost=-0.04, terminal_states={(3, 1): -1, (3, 3): 10}
)


def check_module(name):
    """Return a list of problems found in one component module (empty list means it passes)."""
    try:
        module = importlib.import_module(name)
    except Exception as error:  # a missing or broken file is a contract failure, not a crash
        return [f"cannot import {name}: {error}"]

    problems = []
    for func_name, expected in CONTRACT[name].items():
        func = getattr(module, func_name, None)
        if not callable(func):
            problems.append(f"{name}.{func_name} is missing")
            continue
        actual = list(inspect.signature(func).parameters)
        if actual != expected:
            problems.append(f"{name}.{func_name} arguments are {actual}, expected {expected}")

    if name == "q_table":
        if getattr(module, "ACTIONS", None) != ["N", "S", "E", "W"]:
            problems.append("q_table.ACTIONS must be ['N', 'S', 'E', 'W']")
        if not problems:
            table = module.init_q_table(STAND_IN_ENV)
            if len(table) != 15 or (1, 1) in table:
                problems.append("init_q_table must have 15 states and no obstacle entry")
            if any(v != 0.0 for row in table.values() for v in row.values()):
                problems.append("init_q_table values must all start at 0.0")
            if module.best_actions(table, (0, 0)) != ["N", "S", "E", "W"]:
                problems.append("best_actions on a fresh table must return all four actions in order")
    if name == "q_update" and not problems:
        default = inspect.signature(module.q_update).parameters["terminal_value"].default
        if default is not None:
            problems.append("q_update terminal_value must default to None")
    return problems


def main(argv):
    """Check the named modules (default: all four) and exit 1 if any fail."""
    # Why: a cached .pyc can hide a same-size edit made within the same second, and we do not want to leave
    # __pycache__ folders in the repository.
    sys.dont_write_bytecode = True
    sys.path.insert(0, os.getcwd())  # run from the repository root
    names = argv or list(CONTRACT)
    failed = False
    for name in names:
        if name not in CONTRACT:
            print(f"unknown module {name}; choose from {list(CONTRACT)}")
            failed = True
            continue
        problems = check_module(name)
        print(f"{name}: " + ("OK" if not problems else "FAIL"))
        for problem in problems:
            print(f"  - {problem}")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
