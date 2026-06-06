"""qgrapho provider — manage model providers."""

from __future__ import annotations

import sys

from qgrapho.config_store import add_provider_preset, ensure_config_file, list_enabled_providers, load_config
from qgrapho.presets import list_preset_ids


def run_provider_list() -> int:
    ensure_config_file()
    cfg = load_config()
    enabled = list_enabled_providers(cfg)
    print("Configured providers:")
    if not enabled:
        print("  (none — run: qgrapho provider add openai)")
    for provider in enabled:
        pid = provider.get("id", "?")
        label = provider.get("label", pid)
        models = provider.get("models") or []
        print(f"  • {pid} — {label} ({len(models)} model(s))")
    print("\nAvailable presets:")
    for preset_id in list_preset_ids():
        print(f"  • {preset_id}")
    return 0


def run_provider_add(preset_id: str) -> int:
    try:
        path = add_provider_preset(preset_id)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Added preset '{preset_id}' -> {path}")
    print("Run: qgrapho doctor")
    return 0
