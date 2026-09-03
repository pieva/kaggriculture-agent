"""Isolation checks for the generated Codex E17.2 V4D submission."""

from __future__ import annotations

import subprocess
import sys

from scripts.build_submission_codex_e17_v4d import (
    RELEASE_ID,
    V4D_MODEL_SPEC_VERSION,
    build_submission_codex_e17_v4d,
)


def test_v4d_submission_builds_and_imports_in_isolation(tmp_path) -> None:
    target = build_submission_codex_e17_v4d(tmp_path / "submission_v4d.py")
    text = target.read_text(encoding="utf-8")
    assert RELEASE_ID in text
    assert V4D_MODEL_SPEC_VERSION in text
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            (
                "import importlib.util;"
                f"p={str(target)!r};"
                "s=importlib.util.spec_from_file_location('iso',p);"
                "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
                "assert callable(m.agent);assert callable(m.create_agent);"
                f"assert m.RELEASE_ID=={RELEASE_ID!r};"
                f"assert m.MODEL_SPEC_VERSION=={V4D_MODEL_SPEC_VERSION!r}"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
