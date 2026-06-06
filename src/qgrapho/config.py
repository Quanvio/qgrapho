"""Load and validate QGrapho config.toml."""

from __future__ import annotations

import os

from qgrapho.config_store import load_config, save_config  # noqa: F401
from qgrapho.paths import config_path


def config_exists() -> bool:
    return config_path().is_file()


def has_provider_key(cfg: dict | None = None) -> bool:
    from qgrapho.config_store import list_enabled_providers

    config = cfg if cfg is not None else load_config()
    keys = (
        "OPENAI_API_KEY",
        "DEEPSEEK_API_KEY",
        "MOONSHOT_API_KEY",
        "XAI_API_KEY",
        "OPENROUTER_API_KEY",
        "ANTHROPIC_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "QGRAPHO_CLOUD_API_KEY",
    )
    if any(os.environ.get(k) for k in keys):
        return True
    for provider in list_enabled_providers(config):
        env_name = provider.get("api_key_env") or ""
        if env_name and os.environ.get(env_name):
            return True
        if provider.get("id") == "ollama":
            return True
    return False
