import json

from app.core import config


def test_load_config_updates_previous_ollama_default(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps({"provider": "ollama", "model": "llama3.1:8b"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(config, "_settings_path", lambda: settings_path)

    loaded = config.load_config()

    assert loaded["model"] == "llama3:latest"


def test_load_config_preserves_custom_ollama_model(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps({"provider": "ollama", "model": "llama3.2:3b"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(config, "_settings_path", lambda: settings_path)

    loaded = config.load_config()

    assert loaded["model"] == "llama3.2:3b"
