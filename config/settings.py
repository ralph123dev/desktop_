import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".starklog"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "theme": "dark",
    "chart_style": "curve",
    "username": None,
    "user_id": None,
}

class Settings:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        self.config_dir.mkdir(exist_ok=True)

    def load(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = DEFAULT_CONFIG.copy()
            self.save()

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

settings = Settings()
