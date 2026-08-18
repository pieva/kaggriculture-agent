"""Integration smoke test for Kaggle submission bundle generation and validity."""

import sys
from pathlib import Path
import pytest
import kaggle_environments

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.build_submission import build_submission


# --- INTEGRATION SMOKE TESTS ---

def test_build_and_run_submission_smoke():
    """Integration Smoke Test: Build standalone submission.py and run short 24-step match to verify compatibility."""
    sub_path = Path("submission/submission.py")
    build_submission(str(sub_path))
    assert sub_path.exists()

    # Verify submission file is executable by kaggle_environments engine
    env = kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 24})
    env.run([str(sub_path), "pass"])

    assert len(env.steps) == 24
    assert env.steps[-1][0]["status"] == "DONE"
    assert env.steps[-1][0]["reward"] is not None
