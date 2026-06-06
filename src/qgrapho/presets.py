"""Provider preset discovery and routing defaults."""

from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from qgrapho.paths import presets_dir

KNOWN_PRESETS = (
    "openai",
    "deepseek",
    "moonshot",
    "grok",
    "ollama",
    "openrouter",
    "qgrapho-cloud",
)

ROUTING_BY_PRESET: dict[str, dict[str, str]] = {
    "openai": {
        "chat": "openai/gpt-4o-mini",
        "fast": "openai/gpt-4o-mini",
        "code": "openai/gpt-4o",
        "plan": "openai/gpt-4o",
        "agent": "openai/gpt-4o",
        "reason": "openai/gpt-4o",
        "vision": "openai/gpt-4o",
        "doc": "openai/gpt-4o",
        "embed": "openai/text-embedding-3-small",
    },
    "deepseek": {
        "chat": "deepseek/deepseek-v4-flash",
        "fast": "deepseek/deepseek-v4-flash",
        "code": "deepseek/deepseek-v4-pro",
        "plan": "deepseek/deepseek-v4-pro",
        "agent": "deepseek/deepseek-v4-pro",
        "reason": "deepseek/deepseek-v4-pro",
    },
    "moonshot": {
        "chat": "moonshot/kimi-k2.6",
        "plan": "moonshot/kimi-k2.6",
        "agent": "moonshot/kimi-k2.6",
        "doc": "moonshot/kimi-k2.6",
        "diagram": "moonshot/kimi-k2.6",
    },
    "grok": {
        "chat": "grok/grok-4.3",
        "agent": "grok/grok-4.3",
        "code": "grok/grok-4.3",
    },
    "ollama": {
        "chat": "ollama/llama3.2",
        "fast": "ollama/llama3.2",
        "code": "ollama/qwen2.5-coder:7b",
    },
    "openrouter": {
        "chat": "openrouter/openai/gpt-4o-mini",
        "code": "openrouter/openai/gpt-4o-mini",
    },
    "qgrapho-cloud": {
        "chat": "qgrapho-cloud/qgrapho-default",
        "code": "qgrapho-cloud/qgrapho-default",
    },
}

DEFAULT_MODEL_BY_PRESET: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "deepseek": "deepseek-v4-flash",
    "moonshot": "kimi-k2.6",
    "grok": "grok-4.3",
    "ollama": "llama3.2",
    "openrouter": "openai/gpt-4o-mini",
    "qgrapho-cloud": "qgrapho-default",
}


def list_preset_ids() -> list[str]:
    directory = presets_dir()
    if not directory:
        return list(KNOWN_PRESETS)
    found = sorted(p.stem for p in directory.glob("*.toml") if p.stem != "README")
    return found or list(KNOWN_PRESETS)


def load_preset(preset_id: str) -> dict:
    directory = presets_dir()
    if not directory:
        raise FileNotFoundError("Preset directory not found. Set QGRAPHO_SRC to your clone.")
    path = directory / f"{preset_id}.toml"
    if not path.is_file():
        raise FileNotFoundError(f"Unknown preset: {preset_id}")
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    providers = data.get("providers")
    if not providers:
        raise ValueError(f"Preset {preset_id} has no [[providers]] block")
    if isinstance(providers, dict):
        providers = [providers]
    return {"providers": providers}
