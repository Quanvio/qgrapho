"""Generate LiteLLM proxy config from QGrapho config."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from qgrapho.config_store import load_config
from qgrapho.paths import litellm_config_path


def _litellm_model_name(provider_id: str, model_id: str) -> str:
    return f"{provider_id}/{model_id}"


def build_litellm_config(cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    config = cfg if cfg is not None else load_config()
    model_list: list[dict[str, Any]] = []

    for provider in config.get("providers") or []:
        if not provider.get("enabled", True):
            continue
        provider_id = provider.get("id", "")
        base_url = provider.get("base_url", "")
        api_key_env = provider.get("api_key_env") or ""
        for model in provider.get("models") or []:
            model_id = model.get("id", "")
            if not provider_id or not model_id:
                continue
            params: dict[str, Any] = {
                "model": _litellm_model_name(provider_id, model_id),
            }
            if base_url:
                params["api_base"] = base_url
            if api_key_env:
                params["api_key"] = f"os.environ/{api_key_env}"
            model_list.append(
                {
                    "model_name": _litellm_model_name(provider_id, model_id),
                    "litellm_params": params,
                }
            )

    routing = config.get("routing") or {}
    default_provider = (config.get("models") or {}).get("default_provider", "")
    default_model = (config.get("models") or {}).get("default_model", "")
    master = f"{default_provider}/{default_model}" if default_provider and default_model else None

    payload: dict[str, Any] = {
        "model_list": model_list,
        "general_settings": {"master_key": os.environ.get("QGRAPHO_ROUTER_KEY", "qgrapho-local-dev")},
    }
    if master:
        payload["router_settings"] = {"default_model": master}
    if routing:
        payload["qgrapho_routing"] = routing
    return payload


def write_litellm_config(path: Path | None = None) -> Path:
    target = path or litellm_config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    data = build_litellm_config()
    with target.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)
    return target
