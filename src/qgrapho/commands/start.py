"""qgrapho start — launch QGrapho native profile (Phase 0)."""

from __future__ import annotations

import os
import subprocess
import sys

from qgrapho.config import config_exists, has_provider_key
from qgrapho.platform import all_statuses
from qgrapho.router import write_litellm_config


def run_start() -> int:
    os.environ.setdefault("RUNTIME", "process")

    if not config_exists():
        print("Run qgrapho init first.", file=sys.stderr)
        return 1
    if not has_provider_key():
        print("Configure a provider (qgrapho provider add openai).", file=sys.stderr)
        return 1

    router_cfg = write_litellm_config()
    print("QGrapho native profile")
    print(f"  RUNTIME={os.environ['RUNTIME']}")
    print(f"  Model Router config -> {router_cfg}")

    litellm = _which("litellm")
    if litellm:
        print("\nStarting Model Router (LiteLLM proxy) on :4000 …")
        print("  Press Ctrl+C to stop.\n")
        try:
            subprocess.run(
                [litellm, "--config", str(router_cfg), "--port", "4000"],
                check=False,
            )
        except KeyboardInterrupt:
            print("\nStopped.")
        return 0

    print("\nComponent status:")
    for status in all_statuses():
        mark = "OK" if status.ok else "pending"
        print(f"  {status.name:<21} {mark} — {status.detail}")

    print("\nInstall Model Router: pip install litellm")
    print("Then re-run: qgrapho start")
    print("\nConsole + Agent Engine: set QGRAPHO_CONSOLE_BIN and QGRAPHO_AGENT_ENGINE_BIN (Phase 0 bundle)")
    return 0


def _which(name: str) -> str | None:
    from shutil import which

    return which(name)
