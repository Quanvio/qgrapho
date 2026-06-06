"""QGrapho filesystem paths."""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path


def qgrapho_home() -> Path:
    raw = os.environ.get("QGRAPHO_HOME", "")
    if raw:
        return Path(raw).expanduser()
    return Path.home() / ".qgrapho"


def config_path() -> Path:
    return qgrapho_home() / "config.toml"


def data_dir() -> Path:
    return qgrapho_home() / "data"


def graphs_dir() -> Path:
    return data_dir() / "graphs"


def mcp_dir() -> Path:
    return qgrapho_home() / "mcp"


def runtime_dir() -> Path:
    return qgrapho_home() / "runtime"


def litellm_config_path() -> Path:
    return qgrapho_home() / "litellm.config.yaml"


@lru_cache(maxsize=1)
def repo_root() -> Path | None:
    src = os.environ.get("QGRAPHO_SRC")
    if src:
        root = Path(src).expanduser()
        if (root / "pyproject.toml").is_file():
            return root
    module = Path(__file__).resolve()
    for parent in module.parents:
        if (parent / "pyproject.toml").is_file() and (parent / "config").is_dir():
            return parent
    return None


def repo_config_example() -> Path | None:
    root = repo_root()
    if not root:
        return None
    candidate = root / "config" / "qgrapho.example.toml"
    return candidate if candidate.is_file() else None


def presets_dir() -> Path | None:
    root = repo_root()
    if not root:
        return None
    candidate = root / "config" / "presets"
    return candidate if candidate.is_dir() else None


def deploy_profile_path(name: str = "dev-native") -> Path | None:
    root = repo_root()
    if not root:
        return None
    candidate = root / "deploy" / "profiles" / f"{name}.yaml"
    return candidate if candidate.is_file() else None


def vendor_dir() -> Path | None:
    root = repo_root()
    if not root:
        return None
    candidate = root / "vendor"
    return candidate if candidate.is_dir() else None
