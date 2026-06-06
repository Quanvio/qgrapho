"""qgrapho doctor — verify installation."""

from __future__ import annotations

from qgrapho import __version__
from qgrapho.config import config_exists, has_provider_key, load_config
from qgrapho.paths import config_path, graphs_dir, qgrapho_home, litellm_config_path, repo_root
from qgrapho.platform import all_statuses


def run_doctor() -> int:
    home = qgrapho_home()
    home.mkdir(parents=True, exist_ok=True)
    graphs_dir().mkdir(parents=True, exist_ok=True)

    cfg_ok = config_exists()
    cfg = load_config() if cfg_ok else {}
    product = cfg.get("product", {}).get("name", "QGrapho")
    ok_count = 0
    check_count = 0

    print(f"QGrapho Doctor v{__version__}\n")
    print(f"  Home ................. {home}")
    root = repo_root()
    print(f"  Source ............... {root or 'set QGRAPHO_SRC to clone'}")
    print(f"  Product .............. {product}")
    print(f"  Config ............... {config_path() if cfg_ok else 'missing — run qgrapho init'}")

    for status in all_statuses():
        check_count += 1
        mark = "OK" if status.ok else "—"
        if status.ok:
            ok_count += 1
        print(f"  {status.name:<21} {mark} ({status.detail})")

    keys_ok = has_provider_key(cfg) if cfg_ok else False
    check_count += 1
    if keys_ok:
        ok_count += 1
    print(f"  Provider credentials . {'OK' if keys_ok else '—'} (env vars or Ollama local)")

    if litellm_config_path().is_file():
        print(f"  Router config ........ {litellm_config_path()}")

    print()
    print(f"Phase 0: {ok_count}/{check_count} checks passing")
    print("Next: qgrapho provider add openai · qgrapho mcp init · qgrapho start")

    if not cfg_ok or not keys_ok:
        return 1
    return 0 if ok_count >= 3 else 1
