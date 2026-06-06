"""Graph Intelligence MCP configuration."""

from __future__ import annotations

import json
from pathlib import Path

from qgrapho.paths import graphs_dir, mcp_dir


def write_mcp_config() -> Path:
    mcp_dir().mkdir(parents=True, exist_ok=True)
    graphs_dir().mkdir(parents=True, exist_ok=True)
    target = mcp_dir() / "graph-intelligence.json"

    payload = {
        "name": "qgrapho-graph-intelligence",
        "description": "QGrapho Graph Intelligence — index and query the four graphs",
        "command": "${QGRAPHO_GRAPH_MCP_COMMAND}",
        "env": {
            "QGRAPHO_HOME": str(mcp_dir().parent),
            "QGRAPHO_GRAPHS_DIR": str(graphs_dir()),
        },
        "notes": "Set QGRAPHO_GRAPH_MCP_COMMAND to your MCP server launch command (Phase 0).",
    }
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target
