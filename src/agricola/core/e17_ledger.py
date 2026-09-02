"""Passive requested/executed ledger for the E17 measurement-parity gate.

The wrapper calls the policy first, records a deep copy of its returned action,
and never exposes telemetry to the decision maker. Outcome attribution is
deliberately conservative: ambiguity remains ``UNKNOWN``.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable


LEDGER_SCHEMA_VERSION = "E17_LEDGER_V1"
OUTCOMES = frozenset({"EXECUTED", "NOT_EXECUTED", "UNKNOWN"})


def _plain(value: Any) -> Any:
    if isinstance(value, dict) or hasattr(value, "items"):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def canonical_json(value: Any) -> str:
    """Serialize ledger material deterministically."""

    return json.dumps(
        _plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest().upper()


def _farm(observation: dict[str, Any]) -> dict[str, Any]:
    player = int(observation.get("player", 0))
    farms = observation.get("farms", []) or []
    if 0 <= player < len(farms) and isinstance(farms[player], dict):
        return _plain(farms[player])
    return {}


def _inventory(observation: dict[str, Any]) -> dict[str, Any]:
    private = observation.get("private", {}) or {}
    return {
        "shed": _plain(private.get("shed", {})),
        "seeds": _plain(private.get("seeds", {})),
        "inventories": _plain(private.get("inventories", [])),
    }


def _positions(farm: dict[str, Any]) -> list[list[int] | None]:
    positions: list[list[int] | None] = []
    farmer = farm.get("farmer")
    positions.append(list(farmer) if isinstance(farmer, (list, tuple)) else None)
    for position in farm.get("hands", []) or []:
        positions.append(
            list(position) if isinstance(position, (list, tuple)) else None
        )
    return positions


def _tile(farm: dict[str, Any], position: list[int] | None) -> Any:
    if not position or len(position) < 2:
        return None
    x, y = int(position[0]), int(position[1])
    tiles = farm.get("tiles", []) or []
    if 0 <= y < len(tiles) and isinstance(tiles[y], list) and 0 <= x < len(tiles[y]):
        return _plain(tiles[y][x])
    return None


def _quadrant(position: list[int] | None) -> str | None:
    if not position or len(position) < 2:
        return None
    x, y = int(position[0]), int(position[1])
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def _animal_count(farm: dict[str, Any]) -> int:
    total = 0
    for row in farm.get("tiles", []) or []:
        if not isinstance(row, list):
            continue
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal"):
                total += 1
    return total


def _flatten_action(action: dict[str, Any]) -> list[dict[str, Any]]:
    commands: list[dict[str, Any]] = []
    farmer = action.get("farmer", ["PASS"])
    commands.append(
        {"family": "farmer", "family_index": 0, "unit_index": 0, "payload": farmer}
    )
    for index, payload in enumerate(action.get("hands", []) or []):
        commands.append(
            {
                "family": "hands",
                "family_index": index,
                "unit_index": index + 1,
                "payload": payload,
            }
        )
    for index, payload in enumerate(action.get("market", []) or []):
        commands.append(
            {
                "family": "market",
                "family_index": index,
                "unit_index": None,
                "payload": payload,
            }
        )
    return commands


def _command_parts(payload: Any) -> tuple[str, list[Any]]:
    if isinstance(payload, (list, tuple)) and payload:
        return str(payload[0]), _plain(list(payload[1:]))
    return "MALFORMED", [_plain(payload)]


def _expected_move(position: list[int] | None, command: str) -> list[int] | None:
    if not position or len(position) < 2:
        return None
    delta = {
        "NORTH": (0, -1),
        "SOUTH": (0, 1),
        "EAST": (1, 0),
        "WEST": (-1, 0),
    }.get(command)
    if delta is None:
        return None
    return [int(position[0]) + delta[0], int(position[1]) + delta[1]]


@dataclass
class E17CommandLedger:
    """Append-only command records plus separately typed derived events."""

    metadata: dict[str, Any]
    records: list[dict[str, Any]] = field(default_factory=list)
    derived_events: list[dict[str, Any]] = field(default_factory=list)
    action_batches: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    _pending_indices: list[int] = field(default_factory=list, init=False)
    _last_observation: dict[str, Any] | None = field(default=None, init=False)

    def record(self, observation: dict[str, Any], action: dict[str, Any]) -> None:
        """Settle the preceding batch and record a new requested batch."""

        self._settle_pending(observation)
        self._record_escape_transition(observation)
        plain_action = _plain(deepcopy(action))
        batch_hash = canonical_sha256(plain_action)
        step = int(observation.get("step", 0))
        player = int(observation.get("player", self.metadata.get("player_id", 0)))
        farm = _farm(observation)
        inventory = _inventory(observation)
        positions = _positions(farm)
        pre_fingerprint = canonical_sha256(
            {"farm": farm, "inventory": inventory, "market": observation.get("market")}
        )
        batch_entry = {
            "step": step,
            "action": plain_action,
            "action_batch_sha256": batch_hash,
        }
        self.action_batches.append(batch_entry)
        market_count = len(action.get("market", []) or [])

        self._pending_indices = []
        for batch_index, item in enumerate(_flatten_action(action)):
            command, parameters = _command_parts(item["payload"])
            unit_index = item["unit_index"]
            position = (
                positions[unit_index]
                if isinstance(unit_index, int) and unit_index < len(positions)
                else None
            )
            identity = {
                "episode_id": str(self.metadata.get("episode_id", "UNKNOWN")),
                "player_id": player,
                "step": step,
                "family": item["family"],
                "batch_index": batch_index,
                "command": command,
                "parameters": parameters,
            }
            record = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "episode_id": identity["episode_id"],
                "seed": self.metadata.get("seed"),
                "seat": self.metadata.get("seat", player),
                "player_id": player,
                "step": step,
                "observation_step_received": step,
                "day": int(observation.get("day", step // 24)),
                "hour": int(observation.get("hour", step % 24)),
                "unit_id": (
                    "farmer"
                    if item["family"] == "farmer"
                    else (
                        f"hand:{item['family_index']}"
                        if item["family"] == "hands"
                        else f"market:{item['family_index']}"
                    )
                ),
                "command_id": canonical_sha256(identity),
                "batch_index": batch_index,
                "action_batch_sha256": batch_hash,
                "command_family": item["family"],
                "requested_command": command,
                "requested_parameters": parameters,
                "requested_quantity": self._requested_quantity(command, parameters),
                "executed_quantity": None,
                "pre_state_fingerprint": pre_fingerprint,
                "post_state_fingerprint": None,
                "cash_before": float(farm.get("money", 0.0)),
                "cash_after": None,
                "inventory_before": deepcopy(inventory),
                "inventory_after": None,
                "tile_or_asset_before": {
                    "position": deepcopy(position),
                    "tile": _tile(farm, position),
                },
                "tile_or_asset_after": None,
                "outcome": "UNKNOWN",
                "outcome_evidence_code": "PENDING_POST_STATE",
                "outcome_evidence": "Awaiting the next observation for this player.",
                "quadrant_slot": _quadrant(position),
                "policy_version": self.metadata.get("policy_version"),
                "source_hash": self.metadata.get("source_hash"),
                "config_hash": self.metadata.get("config_hash"),
                "routine_hash": self.metadata.get("routine_hash"),
                "market_batch_size": market_count,
            }
            self.records.append(record)
            self._pending_indices.append(len(self.records) - 1)
        self._last_observation = deepcopy(_plain(observation))

    @staticmethod
    def _requested_quantity(command: str, parameters: list[Any]) -> int | float | None:
        if command in {"BUY_PRODUCT", "BUY_SEED", "SELL"} and len(parameters) >= 2:
            value = parameters[-1]
            return value if isinstance(value, (int, float)) else None
        return 1

    def _settle_pending(self, observation: dict[str, Any]) -> None:
        if not self._pending_indices:
            return
        farm = _farm(observation)
        inventory = _inventory(observation)
        positions = _positions(farm)
        post_fingerprint = canonical_sha256(
            {"farm": farm, "inventory": inventory, "market": observation.get("market")}
        )
        for index in self._pending_indices:
            record = self.records[index]
            record["post_state_fingerprint"] = post_fingerprint
            record["cash_after"] = float(farm.get("money", 0.0))
            record["inventory_after"] = deepcopy(inventory)
            family = record["command_family"]
            unit_index = None
            if family == "farmer":
                unit_index = 0
            elif family == "hands":
                unit_index = int(str(record["unit_id"]).split(":", 1)[1]) + 1
            post_position = (
                positions[unit_index]
                if isinstance(unit_index, int) and unit_index < len(positions)
                else None
            )
            record["tile_or_asset_after"] = {
                "position": deepcopy(post_position),
                "tile": _tile(farm, record["tile_or_asset_before"]["position"]),
            }
            outcome, code, evidence, quantity = self._classify(record)
            record["outcome"] = outcome
            record["outcome_evidence_code"] = code
            record["outcome_evidence"] = evidence
            record["executed_quantity"] = quantity
        self._pending_indices = []

    @staticmethod
    def _classify(record: dict[str, Any]) -> tuple[str, str, str, int | float | None]:
        command = record["requested_command"]
        before_asset = record["tile_or_asset_before"]
        after_asset = record["tile_or_asset_after"]
        if command == "PASS":
            return "EXECUTED", "EXPLICIT_PASS", "The requested command is PASS.", 1
        expected = _expected_move(before_asset.get("position"), command)
        if expected is not None:
            actual = after_asset.get("position")
            if actual == expected:
                return "EXECUTED", "EXPECTED_POSITION_DELTA", "Unit reached the requested adjacent tile.", 1
            if actual == before_asset.get("position"):
                return "NOT_EXECUTED", "POSITION_UNCHANGED", "Unit position did not change.", 0
            return "UNKNOWN", "UNEXPECTED_POSITION_DELTA", "Observed movement is not uniquely attributable.", None
        if record["command_family"] == "market":
            if int(record.get("market_batch_size", 0)) != 1:
                return "UNKNOWN", "MULTI_ORDER_ATTRIBUTION", "Multiple market orders share the same state delta.", None
            changed = (
                record["cash_before"] != record["cash_after"]
                or record["inventory_before"] != record["inventory_after"]
            )
            if changed:
                return "EXECUTED", "UNIQUE_MARKET_STATE_DELTA", "The single market order produced an observable delta.", record["requested_quantity"]
            return "NOT_EXECUTED", "NO_MARKET_STATE_DELTA", "The single market order produced no observable delta.", 0
        # Unit commands are attributed only through their own position/tile.
        # Global inventory can also change because of market orders in the
        # same step and is therefore not univocal evidence for a unit command.
        changed = before_asset != after_asset
        if changed:
            return "EXECUTED", "UNIT_RELEVANT_STATE_DELTA", "Relevant unit/tile or inventory state changed.", 1
        return "NOT_EXECUTED", "NO_RELEVANT_STATE_DELTA", "No relevant unit/tile or inventory change was observed.", 0

    def _record_escape_transition(self, observation: dict[str, Any]) -> None:
        if self._last_observation is None:
            return
        previous_day = int(self._last_observation.get("day", 0))
        current_day = int(observation.get("day", previous_day))
        if current_day <= previous_day:
            return
        before = _animal_count(_farm(self._last_observation))
        after = _animal_count(_farm(observation))
        escaped = max(0, before - after)
        if escaped:
            self.derived_events.append(
                {
                    "schema_version": LEDGER_SCHEMA_VERSION,
                    "event_type": "DERIVED_EOD_ESCAPE",
                    "epistemic_role": "DERIVED",
                    "episode_id": str(self.metadata.get("episode_id", "UNKNOWN")),
                    "seed": self.metadata.get("seed"),
                    "seat": self.metadata.get("seat"),
                    "step": int(observation.get("step", 0)),
                    "day_before": previous_day,
                    "day_after": current_day,
                    "animal_count_before": before,
                    "animal_count_after": after,
                    "derived_escape_count": escaped,
                    "extractor_version": LEDGER_SCHEMA_VERSION,
                }
            )

    def finalize(self, final_observation: dict[str, Any] | None = None) -> None:
        if final_observation is not None:
            self._settle_pending(final_observation)
            self._record_escape_transition(final_observation)
        for index in self._pending_indices:
            record = self.records[index]
            record["outcome_evidence_code"] = "NO_POST_STATE"
            record["outcome_evidence"] = "No later observation was available."
        self._pending_indices = []

    @property
    def action_sequence_sha256(self) -> str:
        return canonical_sha256([entry["action"] for entry in self.action_batches])

    def metrics(self) -> dict[str, Any]:
        total = len(self.records)
        emitted = sum(
            len(_flatten_action(entry["action"])) for entry in self.action_batches
        )
        classified = sum(record["outcome"] != "UNKNOWN" for record in self.records)
        market = [record for record in self.records if record["command_family"] == "market"]
        market_classified = sum(record["outcome"] != "UNKNOWN" for record in market)
        return {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "ledger_records": total,
            "emitted_commands": emitted,
            "ledger_record_coverage": total / emitted if emitted else 0.0,
            "classified_outcome_coverage": classified / total if total else 0.0,
            "market_records": len(market),
            "market_classified_outcome_coverage": (
                market_classified / len(market) if market else 1.0
            ),
            "market_outcome_counts": {
                outcome: sum(record["outcome"] == outcome for record in market)
                for outcome in sorted(OUTCOMES)
            },
            "outcome_counts": {
                outcome: sum(record["outcome"] == outcome for record in self.records)
                for outcome in sorted(OUTCOMES)
            },
            "derived_eod_escape_count": sum(
                int(event["derived_escape_count"]) for event in self.derived_events
            ),
            "derived_escape_events": len(self.derived_events),
            "action_batches": len(self.action_batches),
            "action_sequence_sha256": self.action_sequence_sha256,
            "technical_errors": len(self.errors),
        }


def instrument_policy(
    policy: Callable[[dict[str, Any], Any], dict[str, Any]],
    ledger: E17CommandLedger,
) -> Callable[[dict[str, Any], Any], dict[str, Any]]:
    """Wrap a policy without allowing ledger failures to affect its action."""

    def wrapped(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        action = policy(observation, configuration)
        try:
            ledger.record(observation, action)
        except Exception as exc:  # telemetry is fail-open by design
            ledger.errors.append(f"{type(exc).__name__}: {exc}")
        return action

    wrapped.e17_ledger = ledger
    wrapped.e17_inner_policy = policy
    wrapped.__name__ = f"e17_instrumented_{getattr(policy, '__name__', 'policy')}"
    return wrapped


__all__ = [
    "E17CommandLedger",
    "LEDGER_SCHEMA_VERSION",
    "canonical_json",
    "canonical_sha256",
    "instrument_policy",
]
