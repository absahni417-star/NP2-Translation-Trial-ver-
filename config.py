"""
config.py - Load and save configuration for NP2 Translator
"""

import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "api_key": "",
    "hotkey_toggle": "f1",
    "hotkey_refresh": "f2",
    "hotkey_quit": "esc",
    "overlay_opacity": 0.92,
    "font_size": 9
}


def load_config() -> dict:
    """Load config from file, falling back to defaults."""
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Merge with defaults for any missing keys
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        return merged
    except Exception as e:
        print(f"[config] Failed to load config: {e}. Using defaults.")
        return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Save config dict to file."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[config] Failed to save config: {e}")
