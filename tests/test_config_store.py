"""Config store tests."""

import os
from pathlib import Path

import pytest

from qgrapho.config_store import add_provider_preset, load_config, save_config
from qgrapho.router.litellm_config import build_litellm_config


@pytest.fixture()
def qgrapho_tmp(monkeypatch, tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("QGRAPHO_HOME", str(home))
    monkeypatch.setenv("QGRAPHO_SRC", str(Path(__file__).resolve().parents[1]))
    return home


def test_add_openai_preset(qgrapho_tmp):
    path = add_provider_preset("openai")
    assert path.is_file()
    cfg = load_config()
    assert cfg["models"]["default_provider"] == "openai"
    assert cfg["routing"]["chat"] == "openai/gpt-4o-mini"
    providers = cfg["providers"]
    assert any(p["id"] == "openai" for p in providers)


def test_litellm_config_from_openai(qgrapho_tmp, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    add_provider_preset("openai")
    data = build_litellm_config()
    assert data["model_list"]
    assert data["model_list"][0]["model_name"] == "openai/gpt-4o"


def test_replace_provider_on_readd(qgrapho_tmp):
    add_provider_preset("deepseek")
    add_provider_preset("openai")
    cfg = load_config()
    ids = [p["id"] for p in cfg["providers"]]
    assert ids.count("deepseek") == 1
    assert cfg["models"]["default_provider"] == "openai"
