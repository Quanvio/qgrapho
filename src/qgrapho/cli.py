"""QGrapho command-line interface."""

from __future__ import annotations

import argparse
import sys

from qgrapho import __version__
from qgrapho.commands.doctor import run_doctor
from qgrapho.commands.init_cmd import run_init
from qgrapho.commands.index import run_index
from qgrapho.commands.mcp_cmd import run_mcp_init
from qgrapho.commands.provider import run_provider_add, run_provider_list
from qgrapho.commands.start import run_start


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qgrapho",
        description="QGrapho — graph-native autonomous engineering",
    )
    parser.add_argument("--version", action="version", version=f"qgrapho {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="First-time setup — provider and workspace")
    sub.add_parser("doctor", help="Verify installation and configuration")
    p_index = sub.add_parser("index", help="Index workspace into Graph Intelligence")
    p_index.add_argument("path", nargs="?", default=".", help="Path to index")
    sub.add_parser("start", help="Launch native profile (Model Router + components)")
    sub.add_parser("upgrade", help="Upgrade QGrapho installation")
    sub.add_parser("uninstall", help="Remove CLI shim (keeps data)")

    p_provider = sub.add_parser("provider", help="Manage model providers")
    p_provider_sub = p_provider.add_subparsers(dest="provider_cmd")
    p_provider_sub.add_parser("list", help="List providers and presets")
    p_add = p_provider_sub.add_parser("add", help="Add a provider preset")
    p_add.add_argument("preset", help="Preset id (openai, deepseek, ollama, …)")

    p_mcp = sub.add_parser("mcp", help="Graph Intelligence MCP helpers")
    p_mcp_sub = p_mcp.add_subparsers(dest="mcp_cmd")
    p_mcp_sub.add_parser("init", help="Write MCP config under ~/.qgrapho/mcp/")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cmd = args.command or "help"

    if cmd == "init":
        return run_init()
    if cmd == "doctor":
        return run_doctor()
    if cmd == "index":
        return run_index(args.path)
    if cmd == "start":
        return run_start()
    if cmd == "upgrade":
        print("Re-run scripts/install.sh or scripts/install.ps1 to upgrade.")
        return 0
    if cmd == "uninstall":
        print("Remove ~/.qgrapho/bin from PATH and delete the qgrapho entry point.")
        return 0
    if cmd == "provider":
        if args.provider_cmd == "list":
            return run_provider_list()
        if args.provider_cmd == "add":
            return run_provider_add(args.preset)
        parser.parse_args(["provider", "--help"])
        return 0
    if cmd == "mcp":
        if args.mcp_cmd == "init":
            return run_mcp_init()
        parser.parse_args(["mcp", "--help"])
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
