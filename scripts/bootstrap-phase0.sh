#!/usr/bin/env bash
# Phase 0 vendor bootstrap — Quanvio maintainers only.
# Reads vendor.lock and adds git submodules under vendor/
# See internal .qgrapho.md for upstream mapping.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f vendor.lock ]]; then
  echo "vendor.lock not found"
  exit 1
fi

mkdir -p vendor

echo "Phase 0 vendor bootstrap"
echo "Add submodules manually per vendor.lock, then:"
echo "  git submodule update --init --recursive"
echo "  qgrapho doctor"
echo ""
echo "Public repo never names upstream engines — see .qgrapho.md (local only)."
