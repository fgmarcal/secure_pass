from __future__ import annotations

from pathlib import Path

import app as app_module


def test_main_builds_expected_layout(monkeypatch) -> None:
    class FakeWindow:
        def __init__(self) -> None:
            self.title_value = None
            self.geometry_value = None
            self.withdraw_called = 0
            self.deiconify_called = 0
            self.mainloop_called = 0
            self.destroy_called = 0

        def title(self, value: str) -> None:
            self.title_value = value

        def geometry(self, value: str) -> None:
            self.geometry_value = value

        def withdraw(self) -> None:
            self.withdraw_called += 1

        def deiconify(self) -> None:
            self.deiconify_called += 1

        def destroy(self) -> None:
            self.destroy_called += 1

        def mainloop(self) -> None:
            self.mainloop_called += 1

    class FakeCanvas:
        last_instance = None

        def __init__(self, parent, **kwargs) -> None:
            self.parent = parent
            self.kwargs = kwargs
            self.create_image_calls = []
            self.pack_calls = []
            FakeCanvas.last_instance = self

        def create_image(self, x: int, y: int, image) -> None:
            self.create_image_calls.append((x, y, image))

        def pack(self, **kwargs) -> None:
            self.pack_calls.append(kwargs)

    class FakePhotoImage:
        last_instance = None

        def __init__(self, file: str) -> None:
            self.file = file
            self.subsample_calls = []
            FakePhotoImage.last_instance = self

        def subsample(self, x: int, y: int):
            self.subsample_calls.append((x, y))
            return ("subsampled-image", x, y)

    class FakeRoundedNotebook:
        last_instance = None

        def __init__(self, parent) -> None:
            self.parent = parent
            self.pack_calls = []
            FakeRoundedNotebook.last_instance = self

        def pack(self, **kwargs) -> None:
            self.pack_calls.append(kwargs)

    class FakeSavedTab:
        last_instance = None

        def __init__(self, tab_control) -> None:
            self.tab_control = tab_control
            FakeSavedTab.last_instance = self

    class FakeMainTab:
        last_call = None

        def __init__(self, tab_control, saved_tab) -> None:
            FakeMainTab.last_call = (tab_control, saved_tab)

    class FakeSettingsTab:
        last_arg = None

        def __init__(self, tab_control) -> None:
            FakeSettingsTab.last_arg = tab_control

    fake_window = FakeWindow()
    translations = {
        "app_title": "Password Manager",
        "app_warning_master_required_title": "Warning",
        "app_warning_master_required_msg": "Master password required.",
    }

    monkeypatch.setattr(app_module.tk, "Tk", lambda: fake_window)
    monkeypatch.setattr(app_module, "Canvas", FakeCanvas)
    monkeypatch.setattr(app_module, "PhotoImage", FakePhotoImage)
    monkeypatch.setattr(app_module, "RoundedNotebook", FakeRoundedNotebook)
    monkeypatch.setattr(app_module, "SavedTab", FakeSavedTab)
    monkeypatch.setattr(app_module, "MainTab", FakeMainTab)
    monkeypatch.setattr(app_module, "SettingsTab", FakeSettingsTab)
    monkeypatch.setattr(app_module, "init_db", lambda: None)
    monkeypatch.setattr(app_module.lang, "init", lambda: None)
    monkeypatch.setattr(app_module.lang, "t", lambda key: translations[key])
    monkeypatch.setattr(app_module, "apply_theme", lambda _window: None)
    monkeypatch.setattr(app_module, "prompt_master_password", lambda _window: True)
    monkeypatch.setattr(app_module.messagebox, "showwarning", lambda *args, **kwargs: None)

    app_module.main()

    assert fake_window.title_value == "Password Manager"
    assert fake_window.geometry_value == "520x600"
    assert fake_window.withdraw_called == 1
    assert fake_window.deiconify_called == 1
    assert fake_window.mainloop_called == 1
    assert fake_window.destroy_called == 0

    canvas = FakeCanvas.last_instance
    assert canvas is not None
    assert canvas.parent is fake_window
    assert canvas.kwargs["width"] == 80
    assert canvas.kwargs["height"] == 80
    assert canvas.kwargs["bg"] == app_module.BG
    assert canvas.kwargs["highlightthickness"] == 0
    assert canvas.pack_calls == [{"pady": (12, 0)}]
    assert len(canvas.create_image_calls) == 1
    assert canvas.create_image_calls[0][0:2] == (40, 40)
    assert canvas.create_image_calls[0][2] == ("subsampled-image", 2, 2)

    photo = FakePhotoImage.last_instance
    assert photo is not None
    assert photo.subsample_calls == [(2, 2)]
    assert Path(photo.file).name == "logo.png"
    assert Path(photo.file).parent.name == "assets"

    notebook = FakeRoundedNotebook.last_instance
    assert notebook is not None
    assert notebook.parent is fake_window
    assert notebook.pack_calls == [{"expand": 1, "fill": "both", "padx": 0, "pady": (8, 0)}]

    saved_tab = FakeSavedTab.last_instance
    assert saved_tab is not None
    assert saved_tab.tab_control is notebook
    assert FakeMainTab.last_call == (notebook, saved_tab)
    assert FakeSettingsTab.last_arg is notebook
