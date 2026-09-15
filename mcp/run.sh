#!/bin/bash
# Launch the read-only MCP server from the kit folder (creates its own venv on first run).
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -x .venv-mcp/bin/python ]; then
  python3 -m venv .venv-mcp >&2
  .venv-mcp/bin/pip install --quiet -r mcp/requirements.txt >&2
fi
exec .venv-mcp/bin/python mcp/technocore_readonly_mcp.py
