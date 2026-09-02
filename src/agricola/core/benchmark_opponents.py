"""Neutral benchmark opponents shared by experiment harnesses.

These callables contain no candidate strategy. They exist so experiment
manifests can identify and hash an exact opponent implementation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


SAFE_PASS_ACTION: dict[str, Any] = {
    "farmer": ["PASS"],
    "hands": [],
    "market": [],
}


def inert_pass_policy(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    """Return a fresh all-pass action without inspecting the observation."""

    del observation, configuration
    return deepcopy(SAFE_PASS_ACTION)
