"""qgrapho mcp — MCP configuration helpers."""

from __future__ import annotations

from qgrapho.mcp_setup import write_mcp_config


def run_mcp_init() -> int:
    path = write_mcp_config()
    print(f"Graph Intelligence MCP config: {path}")
    print("Set QGRAPHO_GRAPH_MCP_COMMAND to your MCP server command, then qgrapho doctor")
    return 0
