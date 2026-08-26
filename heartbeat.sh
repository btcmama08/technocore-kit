#!/bin/bash
# Weekly liveness for the launchd job (or run by hand). Passphrase comes from the macOS Keychain.
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') heartbeat"
  .venv/bin/python technocore_agent.py --keychain heartbeat --touch-note
  echo "exit=$?"
} >> logs/heartbeat.log 2>&1
