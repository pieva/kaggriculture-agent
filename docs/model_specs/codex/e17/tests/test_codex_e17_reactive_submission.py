from __future__ import annotations

import importlib.util
from pathlib import Path

from scripts.build_submission_codex_e17_reactive import (
    build_submission_codex_e17_reactive,
)


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("codex_e17_reactive_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reactive_builder_preserves_existing_submission(tmp_path) -> None:
    existing = Path.cwd() / "submission" / "submission_codex.py"
    before = existing.read_bytes()
    target = build_submission_codex_e17_reactive(tmp_path / "reactive.py")
    assert target.exists()
    assert existing.read_bytes() == before


def test_reactive_submission_is_standalone_and_identified(tmp_path) -> None:
    target = build_submission_codex_e17_reactive(tmp_path / "reactive.py")
    text = target.read_text(encoding="utf-8")
    assert "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1" in text
    assert "WHEAT_FEED_SERVICEABILITY" in text
    assert "agricola." not in text
    module = _load(target)
    assert callable(module.agent)
    assert callable(module.create_agent)
