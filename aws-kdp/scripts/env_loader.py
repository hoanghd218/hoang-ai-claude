"""Minimal .env loader so every script can `from env_loader import env`."""

from __future__ import annotations

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_PATH = HERE.parent / "config" / ".env"

_loaded = False


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    global _loaded
    data: dict[str, str] = {}
    if not path.exists():
        _loaded = True
        return data
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        data[key] = val
        os.environ.setdefault(key, val)
    _loaded = True
    return data


def env(key: str, default: str | None = None) -> str | None:
    if not _loaded:
        load_env()
    return os.environ.get(key, default)


if __name__ == "__main__":
    print(load_env())
