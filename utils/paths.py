from __future__ import annotations

import sys
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return get_project_root()


def get_app_data_dir() -> Path:
    data_dir = get_runtime_root() / "database"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
