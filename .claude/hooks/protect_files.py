"""PreToolUse hook: block edits to the files that CLAUDE.md says must not change."""
import json
import os
import sys

# Why basenames: the rule is "reuse the environment and baseline as-is", so we
# protect by file name no matter which folder Claude tries to write from.
PROTECTED = {
    "GridEnvironment.py": "environment: imported by Q-learning, never re-implemented",
    "MDP.py": "value-iteration baseline that Q-learning is compared against",
    "hill.py": "Lab 2 code with its own dirt-score floor",
    "simulated.py": "Lab 2 code with its own dirt-score floor",
}

BLOCK_EXIT_CODE = 2  # Claude Code treats exit 2 from PreToolUse as "block and show stderr to Claude"


def main():
    """Read the hook event from stdin and return 2 if it targets a protected file."""
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # Why: a malformed event is not a reason to block the user's work.

    file_path = (event.get("tool_input") or {}).get("file_path", "")
    name = os.path.basename(file_path)

    if name in PROTECTED:
        print(
            f"BLOCKED: {name} is protected ({PROTECTED[name]}). "
            "Put new code in a new file, or ask the user to approve this edit.",
            file=sys.stderr,
        )
        return BLOCK_EXIT_CODE
    return 0


if __name__ == "__main__":
    sys.exit(main())
