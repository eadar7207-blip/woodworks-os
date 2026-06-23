#!/bin/bash
# Persistent Problem Solver - tries different approaches until task succeeds

TASK="$1"
FAILURE_REASON="$2"

if [ -z "$TASK" ] || [ -z "$FAILURE_REASON" ]; then
    echo "Usage: /persistent-problem-solver \"{task}\" \"{failure_reason}\""
    echo "Example: /persistent-problem-solver \"Research 50 competitors\" \"Agent stalled (600s)\""
    exit 1
fi

# Run the solver
python3 "$(dirname "$0")/solver.py" "$TASK" "$FAILURE_REASON"
