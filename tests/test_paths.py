from __future__ import annotations

from pathlib import Path

import utils.paths as paths


def test_app_data_dir_uses_project_database_for_source_run(monkeypatch, tmp_path) -> None:
    project_root = tmp_path / "project"
    monkeypatch.setattr(paths, "get_project_root", lambda: project_root)
    monkeypatch.setattr(paths.sys, "frozen", False, raising=False)

    assert paths.get_app_data_dir() == project_root / "database"
    assert (project_root / "database").is_dir()


def test_app_data_dir_uses_executable_folder_for_frozen_run(monkeypatch, tmp_path) -> None:
    exe_path = tmp_path / "SecurePass" / "SecurePass.exe"
    exe_path.parent.mkdir()
    exe_path.write_text("", encoding="utf-8")

    monkeypatch.setattr(paths.sys, "frozen", True, raising=False)
    monkeypatch.setattr(paths.sys, "executable", str(exe_path))

    assert paths.get_app_data_dir() == exe_path.parent / "database"
    assert (exe_path.parent / "database").is_dir()
