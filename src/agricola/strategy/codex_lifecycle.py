"""Codex-owned Decision Lifecycle Contract runtime for the C2 candidate.

The module contains no agricultural preferences.  It turns a Codex plan into
versioned decisions, commitments, verification records, reviews, and terminal
closure while enforcing the frozen C2 anti-oscillation rules.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any

FOUNDATION_CHECKPOINT = "f391ee2"
FOUNDATION_VERSION = "C2"
ENGINE_FINGERPRINT = (
    "4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d"
)

DECISION_OPEN = "DECISION_OPEN"
DEFINED = "DEFINED"
PLAN_FEASIBLE = "PLAN_FEASIBLE"
INFEASIBLE = "INFEASIBLE"
REJECTED = "REJECTED"
COMMITTED_EXECUTING = "COMMITTED_EXECUTING"
REPAIR_WITHIN_COMMITMENT = "REPAIR_WITHIN_COMMITMENT"
INVALIDATED = "INVALIDATED"
CANCELLED = "CANCELLED"
SUPERSEDED = "SUPERSEDED"
COMPLETED = "COMPLETED"
REVIEW_READY = "REVIEW_READY"
TERMINAL_CLOSED = "TERMINAL_CLOSED"

ONLINE_STATES = {
    DECISION_OPEN,
    DEFINED,
    PLAN_FEASIBLE,
    INFEASIBLE,
    REJECTED,
    COMMITTED_EXECUTING,
    REPAIR_WITHIN_COMMITMENT,
    INVALIDATED,
    CANCELLED,
    SUPERSEDED,
    COMPLETED,
    REVIEW_READY,
}


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
        # Kaggle's runner exposes the terminal state without another agent call:
        # with N environment states, the last callable observation is N - 2.
        return self.step + 2 >= self.episode_steps

    @property
    def remaining_steps(self) -> int:
        return max(0, self.episode_steps - 1 - self.step)


@dataclass(frozen=True)
class CodexSnapshot:
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
    """Validate and normalize the real Kaggriculture callable observation."""

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
            raise ValueError("observation.step is required and must be integral") from exc

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


class CodexDecisionLifecycle:
    """Append-only, deterministic realization of the frozen C2 DLC."""

    def __init__(
        self,
        *,
        run_id: str,
        episode_id: str,
        agent_id: str,
        model_spec_version: str,
    ) -> None:
        if not run_id or not episode_id:
            raise ValueError("run_id and episode_id are mandatory and distinct from seed")
        self.run_id = str(run_id)
        self.episode_id = str(episode_id)
        self.agent_id = agent_id
        self.model_spec_version = model_spec_version
        self.state = DECISION_OPEN
        self.event_sequence = 0
        self.decision_sequence = 0
        self.plan_sequence = 0
        self.commitment_sequence = 0
        self.repair_sequence = 0
        self.review_sequence = 0
        self.request_sequence = 0
        self.verify_sequence = 0
        self.terminal_sequence = 0
        self.active_commitment: dict[str, Any] | None = None
        self.pending_supersession_intent_id: str | None = None
        self.events: list[dict[str, Any]] = []
        self.feasibility_records: list[dict[str, Any]] = []
        self.repair_records: list[dict[str, Any]] = []
        self.review_records: list[dict[str, Any]] = []
        self.request_records: list[dict[str, Any]] = []
        self.outcome_records: list[dict[str, Any]] = []
        self.verify_records: list[dict[str, Any]] = []
        self.terminal_record: dict[str, Any] | None = None
        self.counts = {
            "commitment_count": 0,
            "completion_count": 0,
            "invalidation_count": 0,
            "repair_count": 0,
            "cancellation_count": 0,
            "supersession_count": 0,
            "infeasible_count": 0,
            "rejected_count": 0,
        }

    @property
    def scope_key(self) -> str:
        return f"{self.run_id}/{self.episode_id}"

    def _next_id(self, kind: str) -> str:
        self.event_sequence += 1
        return f"{self.scope_key}/{kind}-{self.event_sequence:06d}"

    def _transition(
        self,
        target: str,
        *,
        snapshot: CodexSnapshot,
        reason_code: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        source = self.state
        lifecycle_event_id = self._next_id("lifecycle")
        self.state = target
        self.events.append(
            {
                "run_id": self.run_id,
                "episode_id": self.episode_id,
                "lifecycle_event_id": lifecycle_event_id,
                "from_state": source,
                "to_state": target,
                "transition_id": snapshot.clock.step,
                "decision_boundary_id": f"boundary-{snapshot.clock.step:06d}",
                "evidence_snapshot_id": snapshot.evidence_snapshot_id,
                "reason_code": reason_code,
                "payload": deepcopy(payload or {}),
                "foundation_checkpoint": FOUNDATION_CHECKPOINT,
            }
        )

    def begin_commitment(
        self,
        snapshot: CodexSnapshot,
        *,
        intent_type: str,
        plan_payload: dict[str, Any],
        feasibility_records: list[dict[str, Any]],
        reservations: list[dict[str, Any]],
        invariants: list[str],
        invalidators: list[str],
        completion_condition: str,
        completion_invalidation_precedence_policy: str,
    ) -> bool:
        if self.state != DECISION_OPEN:
            raise RuntimeError("a new decision can only begin in DECISION_OPEN")

        self.decision_sequence += 1
        self.plan_sequence += 1
        decision_id = f"{self.scope_key}/decision-{self.decision_sequence:04d}"
        plan_id = f"{self.scope_key}/plan-{self.plan_sequence:04d}"
        decision_payload = {
            "decision_id": decision_id,
            "decision_version": 1,
            "owner_agent": self.agent_id,
            "intent_type": intent_type,
            "intent_payload": deepcopy(plan_payload.get("intent", {})),
            "created_at_transition_id": snapshot.clock.step,
            "evidence_snapshot_id": snapshot.evidence_snapshot_id,
        }
        if self.pending_supersession_intent_id is not None:
            decision_payload["supersession_intent_id"] = (
                self.pending_supersession_intent_id
            )
            decision_payload["successor_decision_id"] = decision_id
            self.pending_supersession_intent_id = None
        self._transition(
            DEFINED,
            snapshot=snapshot,
            reason_code="DEFINE_INTENT",
            payload=decision_payload,
        )

        normalized_checks: list[dict[str, Any]] = []
        failed_checks: list[dict[str, Any]] = []
        for index, record in enumerate(feasibility_records, start=1):
            normalized = {
                "feasibility_check_id": f"{plan_id}/check-{index:02d}",
                "decision_id": decision_id,
                "plan_id": plan_id,
                "snapshot_id": snapshot.evidence_snapshot_id,
                "feasibility_captured_at_transition_id": snapshot.clock.step,
                "revalidated_before_commit": True,
                **deepcopy(record),
            }
            normalized_checks.append(normalized)
            if normalized.get("check_result") == "FAIL":
                failed_checks.append(normalized)
        self.feasibility_records.extend(normalized_checks)

        if failed_checks:
            self.counts["infeasible_count"] += 1
            self._transition(
                INFEASIBLE,
                snapshot=snapshot,
                reason_code=str(
                    failed_checks[0].get(
                        "reason_code", "FEASIBILITY_CAPACITY_EXCEEDED"
                    )
                ),
                payload={
                    "decision_id": decision_id,
                    "plan_id": plan_id,
                    "failed_check_ids": [
                        check["feasibility_check_id"] for check in failed_checks
                    ],
                },
            )
            self._transition(
                DECISION_OPEN,
                snapshot=snapshot,
                reason_code="INFEASIBLE_REOPEN",
            )
            return False

        plan_fingerprint = stable_payload_hash(plan_payload)
        self._transition(
            PLAN_FEASIBLE,
            snapshot=snapshot,
            reason_code="FEASIBILITY_PASS",
            payload={
                "decision_id": decision_id,
                "plan_id": plan_id,
                "plan_version": 1,
                "plan_fingerprint": plan_fingerprint,
                "declared_reservations": deepcopy(reservations),
                "declared_invariants": list(invariants),
                "declared_invalidators": list(invalidators),
                "feasibility_valid_until": (
                    (snapshot.clock.day + 1) * snapshot.clock.turns_per_day - 1
                ),
                "revalidation_policy_version": self.model_spec_version,
                "revalidated_before_commit": True,
            },
        )

        self.commitment_sequence += 1
        commitment_id = (
            f"{self.scope_key}/commitment-{self.commitment_sequence:04d}"
        )
        self.active_commitment = {
            "commitment_id": commitment_id,
            "commitment_version": 1,
            "decision_id": decision_id,
            "decision_version": 1,
            "plan_id": plan_id,
            "plan_version": 1,
            "plan_fingerprint": plan_fingerprint,
            "plan_payload": deepcopy(plan_payload),
            "commitment_start_transition": snapshot.clock.step,
            "commitment_day": snapshot.clock.day,
            "scope": deepcopy(plan_payload.get("scope", {})),
            "declared_completion_condition": completion_condition,
            "declared_invariants": list(invariants),
            "declared_invalidators": list(invalidators),
            "completion_invalidation_precedence_policy": (
                completion_invalidation_precedence_policy
            ),
            "reservation_envelope": deepcopy(reservations),
        }
        self.counts["commitment_count"] += 1
        self._transition(
            COMMITTED_EXECUTING,
            snapshot=snapshot,
            reason_code="COMMIT",
            payload=deepcopy(self.active_commitment),
        )
        return True

    def reject_precommit(
        self, snapshot: CodexSnapshot, *, reason_code: str
    ) -> None:
        if self.state not in {DEFINED, PLAN_FEASIBLE}:
            raise RuntimeError("REJECTED is only valid before commitment")
        self.counts["rejected_count"] += 1
        self._transition(REJECTED, snapshot=snapshot, reason_code=reason_code)
        self._transition(
            DECISION_OPEN,
            snapshot=snapshot,
            reason_code="REJECTED_REOPEN",
        )

    def register_action_requests(
        self,
        snapshot: CodexSnapshot,
        requests: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            raise RuntimeError("committed actions require an active commitment")
        materialized: list[dict[str, Any]] = []
        for request in requests:
            self.request_sequence += 1
            record = {
                "action_request_id": (
                    f"{self.scope_key}/request-{self.request_sequence:07d}"
                ),
                "snapshot_eligibility_id": (
                    f"{self.scope_key}/eligibility-{self.request_sequence:07d}"
                ),
                "commitment_id": self.active_commitment["commitment_id"],
                "commitment_version": self.active_commitment[
                    "commitment_version"
                ],
                "transition_id": snapshot.clock.step,
                "source_state_id": snapshot.state_id,
                **deepcopy(request),
            }
            materialized.append(record)
        self.request_records.extend(materialized)
        return materialized

    def record_verification(
        self,
        snapshot: CodexSnapshot,
        *,
        request_records: list[dict[str, Any]],
        outcomes: list[dict[str, Any]],
        invariant_results: list[dict[str, Any]] | None = None,
        invalidator_results: list[dict[str, Any]] | None = None,
        completion_status: str = "NOT_MET",
        precedence_result: str = "CONTINUE",
    ) -> dict[str, Any]:
        self.verify_sequence += 1
        outcome_by_request = {
            outcome["action_request_id"]: outcome for outcome in outcomes
        }
        self.outcome_records.extend(deepcopy(outcomes))
        execution_outcome_ids: list[str] = []
        for request in request_records:
            outcome = outcome_by_request.get(request["action_request_id"])
            if outcome is not None:
                execution_outcome_ids.append(outcome["execution_outcome_id"])
        active = self.active_commitment or {}
        record = {
            "verify_event_id": f"{self.scope_key}/verify-{self.verify_sequence:07d}",
            "decision_id": active.get("decision_id"),
            "commitment_id": active.get("commitment_id"),
            "commitment_version": active.get("commitment_version"),
            "transition_id": snapshot.clock.step,
            "action_request_ids": [
                request["action_request_id"] for request in request_records
            ],
            "snapshot_eligibility_ids": [
                request["snapshot_eligibility_id"] for request in request_records
            ],
            "execution_outcome_ids": execution_outcome_ids,
            "post_state_evidence_id": snapshot.evidence_snapshot_id,
            "invariant_results": deepcopy(invariant_results or []),
            "invalidator_results": deepcopy(invalidator_results or []),
            "completion_status": completion_status,
            "terminal_status": (
                "TRIGGERED" if snapshot.clock.is_terminal_action else "CLEAR"
            ),
            "precedence_policy_reference": active.get(
                "completion_invalidation_precedence_policy"
            ),
            "precedence_result": precedence_result,
            "verification_result": (
                "DEVIATION"
                if any(
                    outcome.get("result") in {"NO_OP", "REJECTED"}
                    for outcome in outcomes
                )
                else "OBSERVED"
            ),
        }
        self.verify_records.append(record)
        return record

    def repair(
        self,
        snapshot: CodexSnapshot,
        *,
        trigger_evidence_snapshot_id: str,
        reason_code: str,
        succeeded: bool = True,
    ) -> None:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            return
        commitment_id = self.active_commitment["commitment_id"]
        self.repair_sequence += 1
        repair_id = f"{self.scope_key}/repair-{self.repair_sequence:05d}"
        self._transition(
            REPAIR_WITHIN_COMMITMENT,
            snapshot=snapshot,
            reason_code=reason_code,
            payload={"repair_id": repair_id, "commitment_id": commitment_id},
        )
        record = {
            "repair_id": repair_id,
            "commitment_id": commitment_id,
            "repair_attempt": sum(
                1
                for item in self.repair_records
                if item["commitment_id"] == commitment_id
            )
            + 1,
            "trigger_evidence_snapshot_id": trigger_evidence_snapshot_id,
            "repair_policy_version": self.model_spec_version,
            "plan_version_before": self.active_commitment["plan_version"],
            "plan_version_after": self.active_commitment["plan_version"],
            "repair_result": "SUCCEEDED" if succeeded else "FAILED",
        }
        self.repair_records.append(record)
        self.counts["repair_count"] += 1
        self._transition(
            COMMITTED_EXECUTING,
            snapshot=snapshot,
            reason_code="REPAIR_SUCCESSFUL" if succeeded else "REPAIR_FAILED",
            payload=record,
        )

    def close_active(
        self,
        snapshot: CodexSnapshot,
        *,
        completion: bool,
        invalidator_results: list[dict[str, Any]] | None = None,
    ) -> str:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            return self.state
        invalidators = [
            item
            for item in (invalidator_results or [])
            if bool(item.get("triggered"))
        ]
        if invalidators:
            # INVALIDATION_WINS is the pre-declared Codex conflict policy.
            target = INVALIDATED
            reason_code = str(
                invalidators[0].get(
                    "reason_code", "STATE_INVARIANT_VIOLATION"
                )
            )
            self.counts["invalidation_count"] += 1
        elif completion:
            target = COMPLETED
            reason_code = "PLAN_COMPLETED"
            self.counts["completion_count"] += 1
        else:
            return COMMITTED_EXECUTING

        self._transition(
            target,
            snapshot=snapshot,
            reason_code=reason_code,
            payload={
                "commitment_id": self.active_commitment["commitment_id"],
                "completion": completion,
                "invalidator_results": deepcopy(invalidators),
            },
        )
        self._review_and_reopen(snapshot, closure_type=target)
        return target

    def cancel(self, snapshot: CodexSnapshot, *, reason_code: str) -> None:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            raise RuntimeError("CANCELLED requires an active commitment")
        self.counts["cancellation_count"] += 1
        self._transition(
            CANCELLED,
            snapshot=snapshot,
            reason_code=reason_code,
            payload={
                "commitment_id": self.active_commitment["commitment_id"],
                "decision_boundary_id": f"boundary-{snapshot.clock.step:06d}",
                "cancellation_policy_version": self.model_spec_version,
                "authority_reference": "MODEL_SPEC_CODEX_C2_V6",
                "evidence_snapshot_id": snapshot.evidence_snapshot_id,
            },
        )
        self._review_and_reopen(snapshot, closure_type=CANCELLED)

    def supersede(
        self, snapshot: CodexSnapshot, *, supersession_reason_code: str
    ) -> str:
        if self.state != COMMITTED_EXECUTING or self.active_commitment is None:
            raise RuntimeError("SUPERSEDED requires an active commitment")
        self.counts["supersession_count"] += 1
        intent_id = self._next_id("supersession-intent")
        self.pending_supersession_intent_id = intent_id
        self._transition(
            SUPERSEDED,
            snapshot=snapshot,
            reason_code=supersession_reason_code,
            payload={
                "superseded_commitment_id": self.active_commitment[
                    "commitment_id"
                ],
                "supersession_intent_id": intent_id,
                "decision_boundary_id": f"boundary-{snapshot.clock.step:06d}",
                "supersession_policy_version": self.model_spec_version,
                "authority_reference": "MODEL_SPEC_CODEX_C2_V6",
                "supersession_evidence_snapshot_id": (
                    snapshot.evidence_snapshot_id
                ),
                "successor_decision_id": None,
            },
        )
        self._review_and_reopen(snapshot, closure_type=SUPERSEDED)
        return intent_id

    def _review_and_reopen(
        self, snapshot: CodexSnapshot, *, closure_type: str
    ) -> None:
        active = deepcopy(self.active_commitment or {})
        self._transition(
            REVIEW_READY,
            snapshot=snapshot,
            reason_code=f"{closure_type}_REVIEW_READY",
        )
        self.review_sequence += 1
        disposition = {
            COMPLETED: "MAINTAIN",
            INVALIDATED: "REDUCE",
            CANCELLED: "INCONCLUSIVE",
            SUPERSEDED: "INCONCLUSIVE",
        }.get(closure_type, "INCONCLUSIVE")
        review = {
            "review_id": f"{self.scope_key}/review-{self.review_sequence:05d}",
            "review_version": 1,
            "decision_id": active.get("decision_id"),
            "commitment_id": active.get("commitment_id"),
            "review_status": "COMPLETE",
            "closure_type": closure_type,
            "start_evidence_snapshot": active.get("commitment_start_transition"),
            "end_evidence_snapshot": snapshot.evidence_snapshot_id,
            "execution_summary": {
                "repair_count": sum(
                    1
                    for item in self.repair_records
                    if item.get("commitment_id") == active.get("commitment_id")
                )
            },
            "diagnostic_summary": "DESCRIPTIVE_DIAGNOSTICS",
            "review_disposition": disposition,
            "completed_at_transition_id": snapshot.clock.step,
        }
        self.review_records.append(review)
        self.active_commitment = None
        self._transition(
            DECISION_OPEN,
            snapshot=snapshot,
            reason_code="REVIEW_COMPLETE",
            payload={
                "review_id": review["review_id"],
                "review_status": "COMPLETE",
            },
        )

    def close_terminal(
        self,
        snapshot: CodexSnapshot,
        *,
        closure_disposition: str = "TERMINAL_PREEMPTION",
    ) -> None:
        if self.state == TERMINAL_CLOSED:
            return
        if self.state not in ONLINE_STATES:
            raise RuntimeError(f"cannot terminal-close lifecycle state {self.state}")
        previous_state = self.state
        active = deepcopy(self.active_commitment or {})
        self.terminal_sequence += 1
        self.terminal_record = {
            "terminal_closure_id": (
                f"{self.scope_key}/terminal-{self.terminal_sequence:03d}"
            ),
            "previous_lifecycle_state": previous_state,
            "decision_id": active.get("decision_id"),
            "plan_id": active.get("plan_id"),
            "commitment_id": active.get("commitment_id"),
            "terminal_transition_id": snapshot.clock.step,
            "terminal_evidence_snapshot_id": snapshot.evidence_snapshot_id,
            "closure_disposition": closure_disposition,
        }
        self._transition(
            TERMINAL_CLOSED,
            snapshot=snapshot,
            reason_code=closure_disposition,
            payload=self.terminal_record,
        )
        self.active_commitment = None

    def summary(self) -> dict[str, Any]:
        """Return JSON-serializable lifecycle telemetry for local verification."""

        return {
            "run_id": self.run_id,
            "episode_id": self.episode_id,
            "agent_id": self.agent_id,
            "model_spec_version": self.model_spec_version,
            "foundation_checkpoint": FOUNDATION_CHECKPOINT,
            "foundation_version": FOUNDATION_VERSION,
            "engine_fingerprint": ENGINE_FINGERPRINT,
            "state": self.state,
            "active_commitment": deepcopy(self.active_commitment),
            "counts": deepcopy(self.counts),
            "event_count": len(self.events),
            "request_count": len(self.request_records),
            "outcome_count": len(self.outcome_records),
            "verify_count": len(self.verify_records),
            "review_count": len(self.review_records),
            "terminal_record": deepcopy(self.terminal_record),
        }

    def export_ledger(self) -> dict[str, Any]:
        return {
            **self.summary(),
            "events": deepcopy(self.events),
            "feasibility_records": deepcopy(self.feasibility_records),
            "repair_records": deepcopy(self.repair_records),
            "review_records": deepcopy(self.review_records),
            "request_records": deepcopy(self.request_records),
            "outcome_records": deepcopy(self.outcome_records),
            "verify_records": deepcopy(self.verify_records),
            "terminal_record": deepcopy(self.terminal_record),
        }


def snapshot_asdict(snapshot: CodexSnapshot) -> dict[str, Any]:
    """Small public helper used by tests without exposing mutable internals."""

    payload = asdict(snapshot)
    payload["farm"] = deepcopy(snapshot.farm)
    payload["private"] = deepcopy(snapshot.private)
    payload["market"] = deepcopy(snapshot.market)
    return payload
