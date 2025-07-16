#!/bin/bash
# Test runner for src-style Python projects
# Ensures src is on PYTHONPATH so imports like 'from src.llms...' work

set -e
PROJECT_ROOT="$(dirname "$0")"
echo $PROJECT_ROOT
export PYTHONPATH="$PROJECT_ROOT/src"
pytest tests/ "$@"
