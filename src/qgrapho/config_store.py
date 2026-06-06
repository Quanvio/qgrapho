"""Read and write ~/.qgrapho/config.toml."""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w

from qgrapho.paths import config_path, repo_config_example
from qgrapho.presets import DEFAULT_MODEL_BY_PRESET, ROUTING_BY_PRESET, load_preset


def load_config(path: Path | None = None) -> dict[str, Any]:
    target = path or config_path()
    if not target.is_file():
        return {}
    with target.open("rb") as fh:
        return tomllib.load(fh)


def save_config(config: dict[str, Any], path: Path | None = None) -> Path:
    target = path or config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as fh:
        tomli_w.dump(config, fh)
    return target


def ensure_config_file() -> Path:
    target = config_path()
    if target.is_file():
        return target
    example = repo_config_example()
    if example:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(example.read_bytes())
        return target
    save_config({"product": {"name": "QGrapho"}, "models": {}, "routing": {}, "providers": []})
    return target


def _provider_id(provider: dict[str, Any]) -> str:
    return str(provider.get("id", ""))


def add_provider_preset(preset_id: str, *, make_default: bool = True) -> Path:
    ensure_config_file()
    config = load_config()
    preset = load_preset(preset_id)
    incoming = preset["providers"]
    if isinstance(incoming, dict):
        incoming = [incoming]

    providers: list[dict[str, Any]] = list(config.get("providers") or [])
    incoming_ids = {_provider_id(p) for p in incoming}
    providers = [p for p in providers if _provider_id(p) not in incoming_ids]
    providers.extend(incoming)
    config["providers"] = providers

    if make_default and preset_id in DEFAULT_MODEL_BY_PRESET:
        models = dict(config.get("models") or {})
        models["default_provider"] = preset_id
        models["default_model"] = DEFAULT_MODEL_BY_PRESET[preset_id]
        config["models"] = models

    routing = dict(config.get("routing") or {})
    routing.update(ROUTING_BY_PRESET.get(preset_id, {}))
    config["routing"] = routing

    product = dict(config.get("product") or {})
    product.setdefault("name", "QGrapho")
    config["product"] = product

    return save_config(config)


def list_enabled_providers(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    cfg = config if config is not None else load_config()
    providers = cfg.get("providers") or []
    return [p for p in providers if p.get("enabled", True)]
