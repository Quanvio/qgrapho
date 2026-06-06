"""Smoke tests for QGrapho CLI."""

import pytest

from qgrapho.cli import main


def test_help_exits_zero():
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_version_exits_zero():
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0


def test_doctor_runs():
    code = main(["doctor"])
    assert code in (0, 1)


def test_provider_list():
    assert main(["provider", "list"]) == 0


def test_mcp_init(tmp_path, monkeypatch):
    monkeypatch.setenv("QGRAPHO_HOME", str(tmp_path / "qgrapho"))
    monkeypatch.setenv("QGRAPHO_SRC", str(__import__("pathlib").Path(__file__).resolve().parents[1]))
    assert main(["mcp", "init"]) == 0
    assert (tmp_path / "qgrapho" / "mcp" / "graph-intelligence.json").is_file()
