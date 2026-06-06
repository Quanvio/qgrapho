"""Detect QGrapho platform components (Phase 0)."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from qgrapho.config_store import load_config
from qgrapho.paths import mcp_dir, repo_root, vendor_dir


@dataclass
class ComponentStatus:
    name: str
    ok: bool
    detail: str


def _bin_from_env(env_var: str) -> Path | None:
    raw = os.environ.get(env_var, "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    return path if path.exists() else None


def _which(name: str) -> str | None:
    return shutil.which(name)


def console_status() -> ComponentStatus:
    path = _bin_from_env("QGRAPHO_CONSOLE_BIN")
    if path:
        return ComponentStatus("Console", True, str(path))
    root = repo_root()
    if root and (root / "vendor").exists():
        return ComponentStatus("Console", False, "vendor/ present — run bootstrap (Phase 0)")
    return ComponentStatus("Console", False, "set QGRAPHO_CONSOLE_BIN or install Phase 0 bundle")


def agent_engine_status() -> ComponentStatus:
    path = _bin_from_env("QGRAPHO_AGENT_ENGINE_BIN")
    runtime = os.environ.get("RUNTIME", "process")
    if path:
        return ComponentStatus("Agent Engine", True, f"{path} (RUNTIME={runtime})")
    return ComponentStatus("Agent Engine", False, f"set QGRAPHO_AGENT_ENGINE_BIN (RUNTIME={runtime})")


def graph_intelligence_status() -> ComponentStatus:
    mcp_cmd = os.environ.get("QGRAPHO_GRAPH_MCP_COMMAND", "").strip()
    cfg = mcp_dir() / "graph-intelligence.json"
    if mcp_cmd:
        return ComponentStatus("Graph Intelligence", True, mcp_cmd)
    if cfg.is_file():
        return ComponentStatus("Graph Intelligence", True, str(cfg))
    return ComponentStatus("Graph Intelligence", False, "run qgrapho mcp init")


def model_router_status() -> ComponentStatus:
    if _which("litellm"):
        return ComponentStatus("Model Router", True, "litellm in PATH")
    cfg = load_config()
    providers = [p for p in cfg.get("providers") or [] if p.get("enabled", True)]
    if providers:
        return ComponentStatus("Model Router", False, "providers configured — install litellm (`pip install litellm`)")
    return ComponentStatus("Model Router", False, "run qgrapho init")


def vendor_status() -> ComponentStatus:
    root = repo_root()
    vend = vendor_dir()
    if vend and any(vend.iterdir()):
        count = sum(1 for p in vend.iterdir() if p.is_dir())
        return ComponentStatus("Vendor tree", True, f"{count} submodule(s) under vendor/")
    if root:
        return ComponentStatus("Vendor tree", False, "vendor/ empty — Phase 0 bootstrap pending")
    return ComponentStatus("Vendor tree", False, "clone repo and set QGRAPHO_SRC")


def all_statuses() -> list[ComponentStatus]:
    return [
        console_status(),
        agent_engine_status(),
        graph_intelligence_status(),
        model_router_status(),
        vendor_status(),
    ]
