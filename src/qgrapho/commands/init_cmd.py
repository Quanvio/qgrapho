"""qgrapho init — first-time setup."""

from __future__ import annotations

import os

from qgrapho.commands.mcp_cmd import run_mcp_init
from qgrapho.commands.provider import run_provider_add
from qgrapho.config_store import ensure_config_file
from qgrapho.paths import config_path, qgrapho_home


PROVIDERS = (
    ("1", "OpenAI", "OPENAI_API_KEY", "openai"),
    ("2", "DeepSeek (v4-flash / v4-pro)", "DEEPSEEK_API_KEY", "deepseek"),
    ("3", "Moonshot / Kimi", "MOONSHOT_API_KEY", "moonshot"),
    ("4", "Grok / xAI", "XAI_API_KEY", "grok"),
    ("5", "Ollama (local, no key)", None, "ollama"),
    ("6", "OpenRouter", "OPENROUTER_API_KEY", "openrouter"),
    ("7", "Custom URL", None, "custom"),
    ("8", "QGrapho Cloud (optional)", "QGRAPHO_CLOUD_API_KEY", "qgrapho-cloud"),
)


def run_init() -> int:
    home = qgrapho_home()
    home.mkdir(parents=True, exist_ok=True)
    (home / "data" / "graphs").mkdir(parents=True, exist_ok=True)
    ensure_config_file()

    print("QGrapho setup — pick a model provider\n")
    for num, label, _, _ in PROVIDERS:
        print(f"  {num}) {label}")
    choice = input("\nChoice [1-8]: ").strip() or "1"

    selected = next((p for p in PROVIDERS if p[0] == choice), PROVIDERS[0])
    _, label, env_key, preset = selected
    print(f"\nSelected: {label}")

    if preset == "custom":
        print(f"Edit {config_path()} — add [[providers]] with your base_url")
    elif preset == "qgrapho-cloud":
        print("Enable when https://qgrapho.quanvio.com/v1 is live.")
        if env_key and not os.environ.get(env_key):
            key = input(f"{env_key}: ").strip()
            if key:
                print(f"Set {env_key} in your shell profile (qgrapho does not store keys).")
        run_provider_add("qgrapho-cloud")
    elif preset == "ollama":
        run_provider_add("ollama")
        print("Start local models: ollama serve")
    else:
        if env_key and not os.environ.get(env_key):
            key = input(f"{env_key}: ").strip()
            if key:
                print(f"Set {env_key} in your shell profile (qgrapho does not store keys).")
        if run_provider_add(preset) != 0:
            return 1

    run_mcp_init()
    print(f"\nConfig: {config_path()}")
    print("Run:   qgrapho doctor")
    print("Run:   qgrapho start")
    return 0
