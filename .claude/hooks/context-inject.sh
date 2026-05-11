#!/bin/bash
# =============================================================================
# Context Injection Hook — SessionStart
# Shows git state + project info at session start
# =============================================================================

OUTPUT=""

# Git context
if git rev-parse --is-inside-work-tree &>/dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
    COMMITS=$(git log --oneline -5 2>/dev/null || echo "no commits")
    CHANGED=$(git diff --stat HEAD 2>/dev/null | tail -1)
    STAGED=$(git diff --cached --stat 2>/dev/null | tail -1)

    OUTPUT+="Git: branch=$BRANCH"
    [ -n "$CHANGED" ] && OUTPUT+=" | unstaged: $CHANGED"
    [ -n "$STAGED" ] && OUTPUT+=" | staged: $STAGED"
    OUTPUT+=$'\n'"Recent commits:"$'\n'"$COMMITS"
fi

# Project type detection
TYPES=""
[ -f "package.json" ] && TYPES+="node "
[ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ] && TYPES+="python "
[ -f "vite.config.js" ] && TYPES+="vite "
[ -d "n8n" ] && TYPES+="n8n "
[ -n "$TYPES" ] && OUTPUT+=$'\n'"Stack: $TYPES"

# Show pending TODOs from CLAUDE.md
if [ -f "CLAUDE.md" ]; then
    TODOS=$(grep -c "TODO\|FIXME\|HACK\|XXX" CLAUDE.md 2>/dev/null || echo "0")
    [ "$TODOS" -gt 0 ] && OUTPUT+=$'\n'"TODOs in CLAUDE.md: $TODOS"
fi

[ -n "$OUTPUT" ] && echo "$OUTPUT"
exit 0
