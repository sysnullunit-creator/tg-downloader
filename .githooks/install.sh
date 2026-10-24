#!/usr/bin/env bash
set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "Setting up git hooks in: $REPO_ROOT"
chmod +x "$REPO_ROOT/.githooks/"*
git config core.hooksPath .githooks

echo " Git hooks enabled successfully!"
echo "Hooks will now validate:"
echo "  - Commit message format (commit-msg: Conventional Commits)"
echo "  - Branch naming format (pre-push: <type>/<description>)"
echo "  - Code linting and formatting (pre-commit: Ruff)"

