"""Isolation checks for the productive Codex E17.3 6-6-2 submission."""

from __future__ import annotations

import subprocess
import sys

from scripts.build_submission_codex_e17_topology_662 import (
    RELEASE_ID,
    TOPOLOGY_662_MODEL_SPEC_VERSION,
    build_submission_codex_e17_topology_662,
)


def test_topology_662_submission_builds_and_imports_in_isolation(tmp_path) -> None:
    target = build_submission_codex_e17_topology_662(
        tmp_path / "submission_topology_662.py"
    )
    text = target.read_text(encoding="utf-8")
    assert RELEASE_ID in text
    assert TOPOLOGY_662_MODEL_SPEC_VERSION in text
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
                "assert m.MODEL_SPEC_VERSION=="
                f"{TOPOLOGY_662_MODEL_SPEC_VERSION!r};"
                "i=m.create_agent().codex_e17_topology_662_instance;"
                "assert i.q2_pasture_cap==2;"
                "assert len(i.pasture_targets)==14;"
                "assert len(i.reclaimed_crop_targets)==5;"
                "assert i.livestock_resource_cap==15"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
