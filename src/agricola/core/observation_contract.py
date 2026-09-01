"""Policy-neutral observation contract for Kaggriculture controllers.

This module validates and normalizes callable observations.  It deliberately
contains no decision states, planning phases, commitments, or agent policy.
The ``Codex*`` class names are compatibility-stable data type names inherited
from the first implementation; their contract is shared and strategy-neutral.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any

FOUNDATION_VERSION = "C2.1"
ENGINE_FINGERPRINT = (
    "4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d"
)


def _configuration_value(configuration: Any, name: str, default: Any) -> Any:
    if isinstance(configuration, dict):
        return configuration.get(name, default)
    return getattr(configuration, name, default)


def stable_payload_hash(payload: Any) -> str:
    """Return a deterministic SHA-256 over a JSON-compatible payload."""

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class CodexClock:
    """Canonical engine clock; the legacy name is kept for API stability."""

    step: int
    day: int
    hour: int
    turns_per_day: int
    episode_steps: int

    @property
    def is_eod(self) -> bool:
        return self.hour == self.turns_per_day - 1

    @property
    def is_terminal_action(self) -> bool:
        # Kaggle exposes the terminal state without another agent call: with N
        # environment states, the last callable observation is N - 2.
        return self.step + 2 >= self.episode_steps

    @property
    def remaining_steps(self) -> int:
        return max(0, self.episode_steps - 1 - self.step)


@dataclass(frozen=True)
class CodexSnapshot:
    """Immutable, policy-neutral snapshot of the bound player's observation."""

    clock: CodexClock
    player: int
    farm: dict[str, Any]
    private: dict[str, Any]
    market: dict[str, Any]
    evidence_snapshot_id: str
    state_id: str
    configuration_snapshot: dict[str, Any]
    configuration_hash: str
    snapshot_fingerprint: str


class CodexObservationAdapter:
    """Validate and normalize a real Kaggriculture callable observation."""

    @staticmethod
    def parse(
        observation: dict[str, Any],
        configuration: Any,
        *,
        fallback_turns_per_day: int,
        fallback_episode_steps: int,
    ) -> CodexSnapshot:
        if not isinstance(observation, dict):
            raise TypeError("observation must be a mapping")

        try:
            step = int(observation["step"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "observation.step is required and must be integral"
            ) from exc

        turns_per_day = int(
            _configuration_value(
                configuration, "turnsPerDay", fallback_turns_per_day
            )
        )
        episode_steps = int(
            _configuration_value(
                configuration, "episodeSteps", fallback_episode_steps
            )
        )
        if turns_per_day <= 0 or episode_steps <= 0:
            raise ValueError("turnsPerDay and episodeSteps must be positive")

        day = int(observation.get("day", step // turns_per_day))
        hour = int(observation.get("hour", step % turns_per_day))
        if step != day * turns_per_day + hour:
            raise ValueError("clock violates step == day * turnsPerDay + hour")
        if not 0 <= hour < turns_per_day:
            raise ValueError("observation.hour is outside the configured day")

        try:
            player = int(observation.get("player", 0))
        except (TypeError, ValueError) as exc:
            raise ValueError("observation.player must be integral") from exc
        farms = observation.get("farms")
        if not isinstance(farms, (list, tuple)) or not 0 <= player < len(farms):
            raise ValueError("observation.farms does not contain the bound player")
        farm = farms[player]
        private = observation.get("private", {}) or {}
        market = observation.get("market", {}) or {}
        if not isinstance(farm, dict) or not isinstance(private, dict):
            raise TypeError("farm and private payloads must be mappings")
        if not isinstance(market, dict):
            market = {}

        configuration_snapshot = {
            "turnsPerDay": turns_per_day,
            "episodeSteps": episode_steps,
            "boardSize": int(
                _configuration_value(configuration, "boardSize", 10)
            ),
            "shedCapacity": int(
                _configuration_value(configuration, "shedCapacity", 100)
            ),
            "maxMarketOrdersPerTurn": int(
                _configuration_value(configuration, "maxMarketOrdersPerTurn", 10)
            ),
        }
        configuration_hash = stable_payload_hash(configuration_snapshot)
        snapshot_payload = {
            "step": step,
            "day": day,
            "hour": hour,
            "player": player,
            "farm": farm,
            "private": private,
            "market": market,
            "configuration_hash": configuration_hash,
        }
        snapshot_fingerprint = stable_payload_hash(snapshot_payload)
        state_id = f"state-{step:06d}"
        return CodexSnapshot(
            clock=CodexClock(
                step=step,
                day=day,
                hour=hour,
                turns_per_day=turns_per_day,
                episode_steps=episode_steps,
            ),
            player=player,
            farm=farm,
            private=private,
            market=market,
            evidence_snapshot_id=f"evidence-{step:06d}-{snapshot_fingerprint[:12]}",
            state_id=state_id,
            configuration_snapshot=configuration_snapshot,
            configuration_hash=configuration_hash,
            snapshot_fingerprint=snapshot_fingerprint,
        )


def snapshot_asdict(snapshot: CodexSnapshot) -> dict[str, Any]:
    """Return a detached, JSON-serializable representation of a snapshot."""

    payload = asdict(snapshot)
    payload["farm"] = deepcopy(snapshot.farm)
    payload["private"] = deepcopy(snapshot.private)
    payload["market"] = deepcopy(snapshot.market)
    return payload


__all__ = [
    "CodexClock",
    "CodexObservationAdapter",
    "CodexSnapshot",
    "ENGINE_FINGERPRINT",
    "FOUNDATION_VERSION",
    "snapshot_asdict",
    "stable_payload_hash",
]
