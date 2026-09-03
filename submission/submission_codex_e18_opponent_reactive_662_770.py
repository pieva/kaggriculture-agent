"""Standalone Codex E17.2 V4D D28 Kaggle candidate.

Generated from hash-verified sources.  The embedded private module namespace
keeps the complete source policy behavior without repository dependencies.
"""

import sys as _sys
import types as _types
from copy import deepcopy as _deepcopy

RELEASE_ID = 'CODEX-E17.2-V4D-D28-KAGGLE-CANDIDATE-V1'
MODEL_SPEC_VERSION = 'CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28'
ROUTINE_SHA256 = 'C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4'
BUILD_METADATA = {'release_id': 'CODEX-E17.2-V4D-D28-KAGGLE-CANDIDATE-V1',
 'model_spec_version': 'CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28',
 'routine_sha256': 'C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4',
 'source_sha256': {'observation_contract': '3E7509888B09103C79B86FD058984651337CBFC32AB60CD934E6351A4F2A81A9',
                   'v9': '4D99C919B59DAE9B307C403FCF3198763B08FB9D15324AB8C937C4FC2B32090E',
                   'guarded': '4B9F1FE9BD839F284D25030B39292CEF77F9195C6CA29711CF908EE5D2968607',
                   'true_reactive': '9CD72CA9512B62DB6354CC998EDBCF55AF697989ED92C6806D51EBE329F4B07E',
                   'routing_core': 'DDF736DF8E40ADC5CE3F6983CCD516F97AE72E5A385A58A2200A816AD314AEDB',
                   'routing_v3': '80D909104402473503E1945A6F9EE200DF1CEA5ABA9C66B43C5F6A8AA61A6E91',
                   'routing_v4': '9350F8B327B972C703136EB6411F03C74B2A80F6A75A9D99C3E4CA614A60B2A4',
                   'routine_data': 'AC5819014EBB85ED86BA5D25D4F01DE46F9E4760465B7188DF11E69C8812F774'},
 'config_sha256': {'v9': '44DD0EC2F33C9EEEE74AE5676580DC833325AB969D8A9D262EC870FEAAAC6C99',
                   'guarded': '5B4D4B24C4791E42A08937F9CCD7F7BCE5B4B05BA960E7FE8F066DA4C6BED5A0',
                   'true_reactive': '2CC7F1900AFEBC09F971E76FCC0CCC801FF1F54CE65CECB2E979B95456EB42ED',
                   'routing_core': '43FFD984C17F61F21932AB08433DB652DB07E09BFC9AA781FC961D0AC8D48749',
                   'routing_v3': 'AD2A79602A610D35C2D44F200AEA36B9949F41D1EA67EC43EAB873B007A2EF8D',
                   'routing_v4': 'CA7A6E13CF991185E823325D8220E0682388AC18EB446BB206C0A30ACAB45595'}}
_SOURCES = {'observation_contract': '"""Policy-neutral observation contract for Kaggriculture controllers.\n'
                         '\n'
                         'This module validates and normalizes callable observations.  It deliberately\n'
                         'contains no decision states, planning phases, commitments, or agent policy.\n'
                         'The ``Codex*`` class names are compatibility-stable data type names inherited\n'
                         'from the first implementation; their contract is shared and strategy-neutral.\n'
                         '"""\n'
                         '\n'
                         'from __future__ import annotations\n'
                         '\n'
                         'import hashlib\n'
                         'import json\n'
                         'from copy import deepcopy\n'
                         'from dataclasses import asdict, dataclass\n'
                         'from typing import Any\n'
                         '\n'
                         'FOUNDATION_VERSION = "C2.1"\n'
                         'ENGINE_FINGERPRINT = (\n'
                         '    "4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d"\n'
                         ')\n'
                         '\n'
                         '\n'
                         'def _configuration_value(configuration: Any, name: str, default: Any) -> Any:\n'
                         '    if isinstance(configuration, dict):\n'
                         '        return configuration.get(name, default)\n'
                         '    return getattr(configuration, name, default)\n'
                         '\n'
                         '\n'
                         'def stable_payload_hash(payload: Any) -> str:\n'
                         '    """Return a deterministic SHA-256 over a JSON-compatible payload."""\n'
                         '\n'
                         '    encoded = json.dumps(\n'
                         '        payload,\n'
                         '        sort_keys=True,\n'
                         '        separators=(",", ":"),\n'
                         '        default=str,\n'
                         '    ).encode("utf-8")\n'
                         '    return hashlib.sha256(encoded).hexdigest()\n'
                         '\n'
                         '\n'
                         '@dataclass(frozen=True)\n'
                         'class CodexClock:\n'
                         '    """Canonical engine clock; the legacy name is kept for API stability."""\n'
                         '\n'
                         '    step: int\n'
                         '    day: int\n'
                         '    hour: int\n'
                         '    turns_per_day: int\n'
                         '    episode_steps: int\n'
                         '\n'
                         '    @property\n'
                         '    def is_eod(self) -> bool:\n'
                         '        return self.hour == self.turns_per_day - 1\n'
                         '\n'
                         '    @property\n'
                         '    def is_terminal_action(self) -> bool:\n'
                         '        # Kaggle exposes the terminal state without another agent call: with N\n'
                         '        # environment states, the last callable observation is N - 2.\n'
                         '        return self.step + 2 >= self.episode_steps\n'
                         '\n'
                         '    @property\n'
                         '    def remaining_steps(self) -> int:\n'
                         '        return max(0, self.episode_steps - 1 - self.step)\n'
                         '\n'
                         '\n'
                         '@dataclass(frozen=True)\n'
                         'class CodexSnapshot:\n'
                         '    """Immutable, policy-neutral snapshot of the bound player\'s observation."""\n'
                         '\n'
                         '    clock: CodexClock\n'
                         '    player: int\n'
                         '    farm: dict[str, Any]\n'
                         '    private: dict[str, Any]\n'
                         '    market: dict[str, Any]\n'
                         '    evidence_snapshot_id: str\n'
                         '    state_id: str\n'
                         '    configuration_snapshot: dict[str, Any]\n'
                         '    configuration_hash: str\n'
                         '    snapshot_fingerprint: str\n'
                         '\n'
                         '\n'
                         'class CodexObservationAdapter:\n'
                         '    """Validate and normalize a real Kaggriculture callable observation."""\n'
                         '\n'
                         '    @staticmethod\n'
                         '    def parse(\n'
                         '        observation: dict[str, Any],\n'
                         '        configuration: Any,\n'
                         '        *,\n'
                         '        fallback_turns_per_day: int,\n'
                         '        fallback_episode_steps: int,\n'
                         '    ) -> CodexSnapshot:\n'
                         '        if not isinstance(observation, dict):\n'
                         '            raise TypeError("observation must be a mapping")\n'
                         '\n'
                         '        try:\n'
                         '            step = int(observation["step"])\n'
                         '        except (KeyError, TypeError, ValueError) as exc:\n'
                         '            raise ValueError(\n'
                         '                "observation.step is required and must be integral"\n'
                         '            ) from exc\n'
                         '\n'
                         '        turns_per_day = int(\n'
                         '            _configuration_value(\n'
                         '                configuration, "turnsPerDay", fallback_turns_per_day\n'
                         '            )\n'
                         '        )\n'
                         '        episode_steps = int(\n'
                         '            _configuration_value(\n'
                         '                configuration, "episodeSteps", fallback_episode_steps\n'
                         '            )\n'
                         '        )\n'
                         '        if turns_per_day <= 0 or episode_steps <= 0:\n'
                         '            raise ValueError("turnsPerDay and episodeSteps must be positive")\n'
                         '\n'
                         '        day = int(observation.get("day", step // turns_per_day))\n'
                         '        hour = int(observation.get("hour", step % turns_per_day))\n'
                         '        if step != day * turns_per_day + hour:\n'
                         '            raise ValueError("clock violates step == day * turnsPerDay + hour")\n'
                         '        if not 0 <= hour < turns_per_day:\n'
                         '            raise ValueError("observation.hour is outside the configured day")\n'
                         '\n'
                         '        try:\n'
                         '            player = int(observation.get("player", 0))\n'
                         '        except (TypeError, ValueError) as exc:\n'
                         '            raise ValueError("observation.player must be integral") from exc\n'
                         '        farms = observation.get("farms")\n'
                         '        if not isinstance(farms, (list, tuple)) or not 0 <= player < len(farms):\n'
                         '            raise ValueError("observation.farms does not contain the bound player")\n'
                         '        farm = farms[player]\n'
                         '        private = observation.get("private", {}) or {}\n'
                         '        market = observation.get("market", {}) or {}\n'
                         '        if not isinstance(farm, dict) or not isinstance(private, dict):\n'
                         '            raise TypeError("farm and private payloads must be mappings")\n'
                         '        if not isinstance(market, dict):\n'
                         '            market = {}\n'
                         '\n'
                         '        configuration_snapshot = {\n'
                         '            "turnsPerDay": turns_per_day,\n'
                         '            "episodeSteps": episode_steps,\n'
                         '            "boardSize": int(\n'
                         '                _configuration_value(configuration, "boardSize", 10)\n'
                         '            ),\n'
                         '            "shedCapacity": int(\n'
                         '                _configuration_value(configuration, "shedCapacity", 100)\n'
                         '            ),\n'
                         '            "maxMarketOrdersPerTurn": int(\n'
                         '                _configuration_value(configuration, "maxMarketOrdersPerTurn", 10)\n'
                         '            ),\n'
                         '        }\n'
                         '        configuration_hash = stable_payload_hash(configuration_snapshot)\n'
                         '        snapshot_payload = {\n'
                         '            "step": step,\n'
                         '            "day": day,\n'
                         '            "hour": hour,\n'
                         '            "player": player,\n'
                         '            "farm": farm,\n'
                         '            "private": private,\n'
                         '            "market": market,\n'
                         '            "configuration_hash": configuration_hash,\n'
                         '        }\n'
                         '        snapshot_fingerprint = stable_payload_hash(snapshot_payload)\n'
                         '        state_id = f"state-{step:06d}"\n'
                         '        return CodexSnapshot(\n'
                         '            clock=CodexClock(\n'
                         '                step=step,\n'
                         '                day=day,\n'
                         '                hour=hour,\n'
                         '                turns_per_day=turns_per_day,\n'
                         '                episode_steps=episode_steps,\n'
                         '            ),\n'
                         '            player=player,\n'
                         '            farm=farm,\n'
                         '            private=private,\n'
                         '            market=market,\n'
                         '            evidence_snapshot_id=f"evidence-{step:06d}-{snapshot_fingerprint[:12]}",\n'
                         '            state_id=state_id,\n'
                         '            configuration_snapshot=configuration_snapshot,\n'
                         '            configuration_hash=configuration_hash,\n'
                         '            snapshot_fingerprint=snapshot_fingerprint,\n'
                         '        )\n'
                         '\n'
                         '\n'
                         'def snapshot_asdict(snapshot: CodexSnapshot) -> dict[str, Any]:\n'
                         '    """Return a detached, JSON-serializable representation of a snapshot."""\n'
                         '\n'
                         '    payload = asdict(snapshot)\n'
                         '    payload["farm"] = deepcopy(snapshot.farm)\n'
                         '    payload["private"] = deepcopy(snapshot.private)\n'
                         '    payload["market"] = deepcopy(snapshot.market)\n'
                         '    return payload\n'
                         '\n'
                         '\n'
                         '__all__ = [\n'
                         '    "CodexClock",\n'
                         '    "CodexObservationAdapter",\n'
                         '    "CodexSnapshot",\n'
                         '    "ENGINE_FINGERPRINT",\n'
                         '    "FOUNDATION_VERSION",\n'
                         '    "snapshot_asdict",\n'
                         '    "stable_payload_hash",\n'
                         ']\n',
 'v9': '"""Codex V9.0 standalone-source 3Q high-density routine controller."""\n'
       '\n'
       'from __future__ import annotations\n'
       '\n'
       'import json\n'
       'from collections import Counter\n'
       'from copy import deepcopy\n'
       'from pathlib import Path\n'
       'from typing import Any\n'
       '\n'
       'from _codex_bundle.agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256\n'
       '\n'
       'REPO_ROOT = Path(__file__).resolve().parents[4]\n'
       'DEFAULT_V9_CONFIG_PATH = (\n'
       '    REPO_ROOT\n'
       '    / "docs"\n'
       '    / "model_specs"\n'
       '    / "codex"\n'
       '    / "configs"\n'
       '    / "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json"\n'
       ')\n'
       'V9_MODEL_SPEC_VERSION = "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY"\n'
       '_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}\n'
       '\n'
       'Q2_SHEEP_PASTURES: tuple[tuple[int, int], ...] = (\n'
       '    (3, 5),\n'
       '    (4, 5),\n'
       '    (3, 6),\n'
       '    (4, 6),\n'
       '    (4, 7),\n'
       ')\n'
       'Q2_CROP_POSITIONS: tuple[tuple[int, int], ...] = tuple(\n'
       '    (x, y)\n'
       '    for y in range(5, 10)\n'
       '    for x in range(5)\n'
       '    if (x, y) not in set(Q2_SHEEP_PASTURES)\n'
       ')\n'
       '\n'
       '\n'
       'def load_v9_config(path: Path | str | None = None) -> dict[str, Any]:\n'
       '    """Load and validate the immutable V9 execution envelope."""\n'
       '\n'
       '    config_path = Path(path) if path is not None else DEFAULT_V9_CONFIG_PATH\n'
       '    config = json.loads(config_path.read_text(encoding="utf-8"))\n'
       '    if config.get("candidate_id") != "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY":\n'
       '        raise ValueError("unexpected V9 candidate_id")\n'
       '    if config.get("model_spec_version") != V9_MODEL_SPEC_VERSION:\n'
       '        raise ValueError("unexpected V9 model_spec_version")\n'
       '    if int(config.get("quadrants_owned", 0)) != 3:\n'
       '        raise ValueError("V9 requires three quadrants")\n'
       '    if int(config.get("workforce_total", 0)) != 13:\n'
       '        raise ValueError("V9 requires farmer plus twelve hands")\n'
       '    return deepcopy(config)\n'
       '\n'
       '\n'
       'class CodexThreeQDistilledRoutineAgent:\n'
       '    """Execute the frozen 719-step routine and collect passive telemetry."""\n'
       '\n'
       '    PRODUCTIVE = frozenset(\n'
       '        {\n'
       '            "PLANT",\n'
       '            "WATER",\n'
       '            "HARVEST",\n'
       '            "DIG",\n'
       '            "BUILD_PASTURE",\n'
       '            "FEED",\n'
       '            "CARE",\n'
       '            "COLLECT_FERTILIZER",\n'
       '            "FERTILIZE",\n'
       '        }\n'
       '    )\n'
       '    MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})\n'
       '\n'
       '    def __init__(self, *, run_context: dict[str, Any] | None = None) -> None:\n'
       '        context = deepcopy(run_context or {})\n'
       '        self.candidate_id = "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY"\n'
       '        self.model_spec_version = V9_MODEL_SPEC_VERSION\n'
       '        self.run_id = str(context.get("run_id", "codex-v9-distilled-routine"))\n'
       '        self.episode_id = str(context.get("episode_id", "codex-v9-episode"))\n'
       '        self.seed = context.get("seed")\n'
       '        self.player_position = context.get("player_position")\n'
       '        self.error_count = 0\n'
       '        self.fallback_count = 0\n'
       '        self.last_exception: str | None = None\n'
       '        self.final_money = 0.0\n'
       '        self.q1_activation_day: int | None = None\n'
       '        self.q2_activation_day: int | None = None\n'
       '        self.q2_full_module_day: int | None = None\n'
       '        self.q2_first_output_day: int | None = None\n'
       '        self.animal_escapes = 0\n'
       '        self.action_counts: Counter[str] = Counter()\n'
       '        self.production_units: Counter[str] = Counter()\n'
       '        self.sale_requests: Counter[str] = Counter()\n'
       '        self.max_hands = 0\n'
       '        self.max_quadrants = 1\n'
       '        self.max_active_animals = 0\n'
       '        self.max_active_crops = 0\n'
       '        self._last_day: int | None = None\n'
       '        self._last_animal_count = 0\n'
       '\n'
       '    @staticmethod\n'
       '    def _farm(observation: dict[str, Any]) -> dict[str, Any]:\n'
       '        player = int(observation.get("player", 0))\n'
       '        farms = observation.get("farms", []) or []\n'
       '        return farms[player] if 0 <= player < len(farms) else {}\n'
       '\n'
       '    @staticmethod\n'
       '    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:\n'
       '        x, y = position\n'
       '        tiles = farm.get("tiles", []) or []\n'
       '        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):\n'
       '            return tiles[y][x]\n'
       '        return None\n'
       '\n'
       '    def _observe_state(self, observation: dict[str, Any]) -> dict[str, Any]:\n'
       '        farm = self._farm(observation)\n'
       '        day = int(observation.get("day", 0))\n'
       '        quadrants = len(farm.get("unlocked_quadrants", []) or [])\n'
       '        hands = len(farm.get("hands", []) or [])\n'
       '        animals = 0\n'
       '        crops = 0\n'
       '        q2_animals = 0\n'
       '        for y, row in enumerate(farm.get("tiles", []) or []):\n'
       '            for x, tile in enumerate(row):\n'
       '                if not isinstance(tile, dict):\n'
       '                    continue\n'
       '                if tile.get("animal"):\n'
       '                    animals += 1\n'
       '                    if x < 5 and y >= 5:\n'
       '                        q2_animals += 1\n'
       '                if tile.get("kind") == "PLANT":\n'
       '                    crops += 1\n'
       '\n'
       '        if self._last_day is not None and day > self._last_day:\n'
       '            self.animal_escapes += max(0, self._last_animal_count - animals)\n'
       '        self._last_day = day\n'
       '        self._last_animal_count = animals\n'
       '        self.final_money = float(farm.get("money", 0.0))\n'
       '        self.max_hands = max(self.max_hands, hands)\n'
       '        self.max_quadrants = max(self.max_quadrants, quadrants)\n'
       '        self.max_active_animals = max(self.max_active_animals, animals)\n'
       '        self.max_active_crops = max(self.max_active_crops, crops)\n'
       '        if quadrants >= 2 and self.q1_activation_day is None:\n'
       '            self.q1_activation_day = day\n'
       '        if quadrants >= 3 and self.q2_activation_day is None:\n'
       '            self.q2_activation_day = day\n'
       '        if q2_animals >= 5 and self.q2_full_module_day is None:\n'
       '            self.q2_full_module_day = day\n'
       '        return farm\n'
       '\n'
       '    def _attribute_action(\n'
       '        self,\n'
       '        observation: dict[str, Any],\n'
       '        farm: dict[str, Any],\n'
       '        action: dict[str, Any],\n'
       '    ) -> None:\n'
       '        positions = [\n'
       '            tuple(farm.get("farmer", [4, 4])),\n'
       '            *(tuple(position) for position in farm.get("hands", []) or []),\n'
       '        ]\n'
       '        unit_actions = [\n'
       '            action.get("farmer", ["PASS"]),\n'
       '            *(action.get("hands", []) or []),\n'
       '        ]\n'
       '        for worker_id, unit_action in enumerate(unit_actions):\n'
       '            if not unit_action:\n'
       '                continue\n'
       '            opcode = str(unit_action[0])\n'
       '            self.action_counts[opcode] += 1\n'
       '            if opcode != "HARVEST" or worker_id >= len(positions):\n'
       '                if opcode == "FEED":\n'
       '                    self.production_units["WHEAT_CONSUMED"] += 1\n'
       '                elif opcode == "COLLECT_FERTILIZER":\n'
       '                    self.production_units["FERTILIZER_COLLECTED"] += 1\n'
       '                continue\n'
       '            tile = self._tile(farm, positions[worker_id])\n'
       '            if not isinstance(tile, dict):\n'
       '                continue\n'
       '            units = int(tile.get("yield_units", 0))\n'
       '            item = tile.get("crop")\n'
       '            animal = tile.get("animal")\n'
       '            if animal == "COW":\n'
       '                item = "MILK"\n'
       '            elif animal == "SHEEP":\n'
       '                item = "WOOL"\n'
       '            elif animal == "GOOSE":\n'
       '                item = "EGG"\n'
       '            if item and units > 0:\n'
       '                self.production_units[str(item)] += units\n'
       '                x, y = positions[worker_id]\n'
       '                if x < 5 and y >= 5 and self.q2_first_output_day is None:\n'
       '                    self.q2_first_output_day = int(observation.get("day", 0))\n'
       '\n'
       '        for order in action.get("market", []) or []:\n'
       '            if len(order) >= 3 and order[0] == "SELL":\n'
       '                self.sale_requests[str(order[1])] += int(order[2])\n'
       '\n'
       '    def __call__(\n'
       '        self, observation: dict[str, Any], configuration: Any = None\n'
       '    ) -> dict[str, Any]:\n'
       '        del configuration\n'
       '        step = int(observation.get("step", 0))\n'
       '        farm = self._observe_state(observation)\n'
       '        action = (\n'
       '            deepcopy(ROUTINE_ACTIONS[step])\n'
       '            if 0 <= step < len(ROUTINE_ACTIONS)\n'
       '            else deepcopy(_SAFE_PASS)\n'
       '        )\n'
       '        if step == 195:\n'
       '            for order in action.get("market", []) or []:\n'
       '                if order[:2] == ["BUY_PRODUCT", "WHEAT"]:\n'
       '                    order[2] = max(4, int(order[2]))\n'
       '                    break\n'
       '            action["market"] = [\n'
       '                order\n'
       '                for order in action.get("market", []) or []\n'
       '                if order[:2] != ["BUY_ANIMAL", "COW"]\n'
       '            ]\n'
       '        self._attribute_action(observation, farm, action)\n'
       '        return action\n'
       '\n'
       '    def telemetry_snapshot(self) -> dict[str, Any]:\n'
       '        productive = sum(self.action_counts[opcode] for opcode in self.PRODUCTIVE)\n'
       '        moves = sum(self.action_counts[opcode] for opcode in self.MOVES)\n'
       '        return {\n'
       '            "agent_version": self.model_spec_version,\n'
       '            "routine_sha256": ROUTINE_SHA256,\n'
       '            "FINAL_MONEY": self.final_money,\n'
       '            "Q1_activation_day": self.q1_activation_day,\n'
       '            "Q1_full_module_day": None,\n'
       '            "Q1_first_output_day": None,\n'
       '            "Q2_activation_day": self.q2_activation_day,\n'
       '            "Q2_full_module_day": self.q2_full_module_day,\n'
       '            "Q2_first_output_day": self.q2_first_output_day,\n'
       '            "Q2_activation_records": [],\n'
       '            "MILK_units": int(self.production_units["MILK"]),\n'
       '            "WOOL_units": int(self.production_units["WOOL"]),\n'
       '            "MELON_units": int(self.production_units["MELON"]),\n'
       '            "STRAWBERRY_units": int(self.production_units["STRAWBERRY"]),\n'
       '            "WHEAT_sold": int(self.sale_requests["WHEAT"]),\n'
       '            "WHEAT_consumed": int(self.production_units["WHEAT_CONSUMED"]),\n'
       '            "fertilizer_collected": int(\n'
       '                self.production_units["FERTILIZER_COLLECTED"]\n'
       '            ),\n'
       '            "productive_actions": productive,\n'
       '            "MOVE_actions": moves,\n'
       '            "PASS_actions": int(self.action_counts["PASS"]),\n'
       '            "MOVE_PER_PRODUCTIVE_ACTION": (\n'
       '                moves / productive if productive else None\n'
       '            ),\n'
       '            "ANIMAL_ESCAPE": self.animal_escapes,\n'
       '            "max_hands": self.max_hands,\n'
       '            "max_quadrants": self.max_quadrants,\n'
       '            "max_active_animals": self.max_active_animals,\n'
       '            "max_active_crops": self.max_active_crops,\n'
       '            "sale_requests": dict(self.sale_requests),\n'
       '            "action_requests_by_opcode": dict(self.action_counts),\n'
       '        }\n'
       '\n'
       '\n'
       'def create_v9_agent(\n'
       '    run_context: dict[str, Any] | None = None,\n'
       '    config_path: Path | str | None = None,\n'
       '):\n'
       '    """Create the fail-closed Kaggle-compatible V9 policy."""\n'
       '\n'
       '    load_v9_config(config_path)\n'
       '    instance = CodexThreeQDistilledRoutineAgent(run_context=run_context)\n'
       '\n'
       '    def policy(\n'
       '        observation: dict[str, Any], configuration: Any = None\n'
       '    ) -> dict[str, Any]:\n'
       '        try:\n'
       '            action = instance(observation, configuration)\n'
       '            policy.codex_v9_last_error = None\n'
       '            return action\n'
       '        except (KeyboardInterrupt, SystemExit):\n'
       '            raise\n'
       '        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary\n'
       '            instance.error_count += 1\n'
       '            instance.fallback_count += 1\n'
       '            instance.last_exception = f"{type(exc).__name__}: {exc}"\n'
       '            policy.codex_v9_last_error = instance.last_exception\n'
       '            return deepcopy(_SAFE_PASS)\n'
       '\n'
       '    policy.codex_v9_instance = instance\n'
       '    policy.codex_v9_last_error = None\n'
       '    policy.__name__ = "codex_v9_3q_mixed_high_density_policy"\n'
       '    return policy\n'
       '\n'
       '\n'
       '__all__ = [\n'
       '    "CodexThreeQDistilledRoutineAgent",\n'
       '    "Q2_CROP_POSITIONS",\n'
       '    "Q2_SHEEP_PASTURES",\n'
       '    "V9_MODEL_SPEC_VERSION",\n'
       '    "create_v9_agent",\n'
       '    "load_v9_config",\n'
       ']\n',
 'guarded': '"""E17.1 reactive guard layered over the frozen Codex V9 3Q routine.\n'
            '\n'
            'The V9 action remains the default provider.  This module changes it only for\n'
            'one causal family: animal feed serviceability under observed WHEAT scarcity or\n'
            'critical hunger.  Every changed batch is retained in an auditable override\n'
            'record; the frozen V9 source and the Kaggle submission are never mutated.\n'
            '"""\n'
            '\n'
            'from __future__ import annotations\n'
            '\n'
            'import json\n'
            'from collections import Counter\n'
            'from copy import deepcopy\n'
            'from pathlib import Path\n'
            'from typing import Any\n'
            '\n'
            'from _codex_bundle.agricola.core.observation_contract import (\n'
            '    CodexObservationAdapter,\n'
            '    stable_payload_hash,\n'
            ')\n'
            'from _codex_bundle.agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent\n'
            '\n'
            'REPO_ROOT = Path(__file__).resolve().parents[4]\n'
            'DEFAULT_REACTIVE_CONFIG_PATH = (\n'
            '    REPO_ROOT\n'
            '    / "experiments"\n'
            '    / "e17"\n'
            '    / "configs"\n'
            '    / "codex"\n'
            '    / "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1.json"\n'
            ')\n'
            'REACTIVE_MODEL_SPEC_VERSION = "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1"\n'
            '_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}\n'
            '\n'
            '\n'
            'def load_reactive_config(path: Path | str | None = None) -> dict[str, Any]:\n'
            '    """Load the bounded E17.1 guard configuration."""\n'
            '\n'
            '    config_path = Path(path) if path is not None else DEFAULT_REACTIVE_CONFIG_PATH\n'
            '    config = json.loads(config_path.read_text(encoding="utf-8"))\n'
            '    if config.get("candidate_id") != "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1":\n'
            '        raise ValueError("unexpected E17.1 candidate_id")\n'
            '    if config.get("model_spec_version") != REACTIVE_MODEL_SPEC_VERSION:\n'
            '        raise ValueError("unexpected E17.1 model_spec_version")\n'
            '    if config.get("base_policy") != "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY":\n'
            '        raise ValueError("E17.1 must use the frozen Codex V9 as default provider")\n'
            '    if config.get("causal_family") != "WHEAT_FEED_SERVICEABILITY":\n'
            '        raise ValueError("E17.1 is restricted to WHEAT/feed serviceability")\n'
            '    for key in (\n'
            '        "turns_per_day",\n'
            '        "episode_steps",\n'
            '        "feed_reserve_rounds",\n'
            '        "critical_unfed_threshold",\n'
            '        "max_extra_wheat_per_step",\n'
            '        "operating_cash_floor",\n'
            '    ):\n'
            '        if int(config.get(key, -1)) < 0:\n'
            '            raise ValueError(f"{key} must be non-negative")\n'
            '    if int(config["turns_per_day"]) <= 0 or int(config["episode_steps"]) <= 0:\n'
            '        raise ValueError("clock dimensions must be positive")\n'
            '    return deepcopy(config)\n'
            '\n'
            '\n'
            'def _unit_actions(action: dict[str, Any]) -> list[list[Any]]:\n'
            '    return [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]\n'
            '\n'
            '\n'
            'def _wheat_total(private: dict[str, Any]) -> int:\n'
            '    total = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)\n'
            '    for inventory in private.get("inventories", []) or []:\n'
            '        if isinstance(inventory, dict):\n'
            '            total += int(inventory.get("WHEAT", 0) or 0)\n'
            '    return total\n'
            '\n'
            '\n'
            'def _market_quantity(action: dict[str, Any], opcode: str, item: str) -> int:\n'
            '    total = 0\n'
            '    for order in action.get("market", []) or []:\n'
            '        if isinstance(order, list) and len(order) >= 3 and order[:2] == [opcode, item]:\n'
            '            try:\n'
            '                total += max(0, int(order[2]))\n'
            '            except (TypeError, ValueError):\n'
            '                continue\n'
            '    return total\n'
            '\n'
            '\n'
            'class CodexE17ReactiveGuardedAgent:\n'
            '    """State-reactive WHEAT/feed guard with immutable V9 defaults."""\n'
            '\n'
            '    def __init__(\n'
            '        self,\n'
            '        *,\n'
            '        run_context: dict[str, Any] | None = None,\n'
            '        config_path: Path | str | None = None,\n'
            '    ) -> None:\n'
            '        self.config = load_reactive_config(config_path)\n'
            '        self.run_context = deepcopy(run_context or {})\n'
            '        self.base_policy = create_v9_agent(run_context=self.run_context)\n'
            '        self.candidate_id = str(self.config["candidate_id"])\n'
            '        self.model_spec_version = REACTIVE_MODEL_SPEC_VERSION\n'
            '        self.error_count = 0\n'
            '        self.fallback_count = 0\n'
            '        self.last_exception: str | None = None\n'
            '        self.override_count = 0\n'
            '        self.override_reasons: Counter[str] = Counter()\n'
            '        self.override_records: list[dict[str, Any]] = []\n'
            '        self.observation_count = 0\n'
            '        self.detected_unfilled_wheat_units = 0\n'
            '        self._pending_wheat_buy: dict[str, int] | None = None\n'
            '\n'
            '    @staticmethod\n'
            '    def _animal_features(farm: dict[str, Any]) -> dict[str, Any]:\n'
            '        animals: list[dict[str, Any]] = []\n'
            '        for y, row in enumerate(farm.get("tiles", []) or []):\n'
            '            for x, tile in enumerate(row):\n'
            '                if not isinstance(tile, dict) or not tile.get("animal"):\n'
            '                    continue\n'
            '                animals.append(\n'
            '                    {\n'
            '                        "position": (x, y),\n'
            '                        "animal": str(tile["animal"]),\n'
            '                        "fed_today": bool(tile.get("fed_today", False)),\n'
            '                        "consecutive_unfed": int(tile.get("consecutive_unfed", 0) or 0),\n'
            '                    }\n'
            '                )\n'
            '        return {\n'
            '            "animals": animals,\n'
            '            "active_animals": len(animals),\n'
            '        }\n'
            '\n'
            '    @staticmethod\n'
            '    def _positions_and_inventories(\n'
            '        farm: dict[str, Any], private: dict[str, Any]\n'
            '    ) -> tuple[list[tuple[int, int]], list[dict[str, Any]]]:\n'
            '        positions = [\n'
            '            tuple(farm.get("farmer", [4, 4])),\n'
            '            *(tuple(value) for value in farm.get("hands", []) or []),\n'
            '        ]\n'
            '        raw_inventories = private.get("inventories", []) or []\n'
            '        inventories = [\n'
            '            value if isinstance(value, dict) else {} for value in raw_inventories\n'
            '        ]\n'
            '        if len(inventories) < len(positions):\n'
            '            inventories.extend({} for _ in range(len(positions) - len(inventories)))\n'
            '        return positions, inventories\n'
            '\n'
            '    def _apply_critical_feed_overrides(\n'
            '        self,\n'
            '        action: dict[str, Any],\n'
            '        farm: dict[str, Any],\n'
            '        private: dict[str, Any],\n'
            '        critical_positions: set[tuple[int, int]],\n'
            '    ) -> list[str]:\n'
            '        if not self.config["allow_critical_feed_override"] or not critical_positions:\n'
            '            return []\n'
            '        positions, inventories = self._positions_and_inventories(farm, private)\n'
            '        actions = _unit_actions(action)\n'
            '        reasons: list[str] = []\n'
            '        for worker_id, position in enumerate(positions):\n'
            '            if worker_id >= len(actions) or position not in critical_positions:\n'
            '                continue\n'
            '            inventory = inventories[worker_id]\n'
            '            if int(inventory.get("WHEAT", 0) or 0) <= 0:\n'
            '                continue\n'
            '            unit_action = actions[worker_id]\n'
            '            if unit_action and unit_action[0] == "FEED":\n'
            '                continue\n'
            '            if worker_id == 0:\n'
            '                action["farmer"] = ["FEED"]\n'
            '            else:\n'
            '                hands = action.setdefault("hands", [])\n'
            '                while len(hands) < worker_id:\n'
            '                    hands.append(["PASS"])\n'
            '                hands[worker_id - 1] = ["FEED"]\n'
            '            reasons.append("CRITICAL_FEED_OVERRIDE")\n'
            '            critical_positions.remove(position)\n'
            '            if not critical_positions:\n'
            '                break\n'
            '        return reasons\n'
            '\n'
            '    @staticmethod\n'
            '    def _scheduled_feed_positions(\n'
            '        action: dict[str, Any], farm: dict[str, Any]\n'
            '    ) -> set[tuple[int, int]]:\n'
            '        positions = [\n'
            '            tuple(farm.get("farmer", [4, 4])),\n'
            '            *(tuple(value) for value in farm.get("hands", []) or []),\n'
            '        ]\n'
            '        return {\n'
            '            positions[index]\n'
            '            for index, unit_action in enumerate(_unit_actions(action))\n'
            '            if index < len(positions) and unit_action and unit_action[0] == "FEED"\n'
            '        }\n'
            '\n'
            '    def _settle_previous_wheat_buy(self, wheat_total: int, step: int) -> int:\n'
            '        """Conservatively infer an unfilled WHEAT quantity from the next state.\n'
            '\n'
            '        Requested FEED and WHEAT sales are subtracted even when they may have\n'
            '        failed.  WHEAT harvests are not imputed.  Both choices bias the result\n'
            '        against false claims of market non-execution.\n'
            '        """\n'
            '\n'
            '        pending = self._pending_wheat_buy\n'
            '        self._pending_wheat_buy = None\n'
            '        if not self.config["market_fill_tracking"] or pending is None:\n'
            '            return 0\n'
            '        if step <= pending["step"]:\n'
            '            return 0\n'
            '        expected_without_buy = max(\n'
            '            0,\n'
            '            pending["wheat_total"]\n'
            '            - pending["feed_requests"]\n'
            '            - pending["wheat_sell_requests"],\n'
            '        )\n'
            '        observed_gain = max(0, wheat_total - expected_without_buy)\n'
            '        inferred_fill = min(pending["requested"], observed_gain)\n'
            '        shortfall = max(0, pending["requested"] - inferred_fill)\n'
            '        self.detected_unfilled_wheat_units += shortfall\n'
            '        return shortfall\n'
            '\n'
            '    def _remember_wheat_buy(\n'
            '        self, action: dict[str, Any], *, wheat_total: int, step: int\n'
            '    ) -> None:\n'
            '        requested = _market_quantity(action, "BUY_PRODUCT", "WHEAT")\n'
            '        if requested <= 0:\n'
            '            self._pending_wheat_buy = None\n'
            '            return\n'
            '        self._pending_wheat_buy = {\n'
            '            "step": step,\n'
            '            "requested": requested,\n'
            '            "wheat_total": wheat_total,\n'
            '            "feed_requests": sum(\n'
            '                1\n'
            '                for unit_action in _unit_actions(action)\n'
            '                if unit_action and unit_action[0] == "FEED"\n'
            '            ),\n'
            '            "wheat_sell_requests": _market_quantity(action, "SELL", "WHEAT"),\n'
            '        }\n'
            '\n'
            '    def _apply_market_guard(\n'
            '        self,\n'
            '        action: dict[str, Any],\n'
            '        *,\n'
            '        active_animals: int,\n'
            '        wheat_total: int,\n'
            '        money: float,\n'
            '        wheat_price: float,\n'
            '        max_orders: int,\n'
            '        detected_unfilled_wheat: int,\n'
            '        critical_eod: bool,\n'
            '    ) -> list[str]:\n'
            '        if active_animals <= 0 or not (detected_unfilled_wheat or critical_eod):\n'
            '            return []\n'
            '        reasons: list[str] = []\n'
            '        feed_requests = sum(\n'
            '            1 for unit_action in _unit_actions(action)\n'
            '            if unit_action and unit_action[0] == "FEED"\n'
            '        )\n'
            '        target = active_animals * int(self.config["feed_reserve_rounds"])\n'
            '        buys = _market_quantity(action, "BUY_PRODUCT", "WHEAT")\n'
            '        sells = _market_quantity(action, "SELL", "WHEAT")\n'
            '        projected = wheat_total - feed_requests + buys - sells\n'
            '        shortfall = max(detected_unfilled_wheat, target - projected, 0)\n'
            '        market = action.setdefault("market", [])\n'
            '\n'
            '        if shortfall and sells and self.config["allow_wheat_sale_reduction"]:\n'
            '            remaining = shortfall\n'
            '            new_market: list[list[Any]] = []\n'
            '            for order in market:\n'
            '                if (\n'
            '                    remaining > 0\n'
            '                    and isinstance(order, list)\n'
            '                    and len(order) >= 3\n'
            '                    and order[:2] == ["SELL", "WHEAT"]\n'
            '                ):\n'
            '                    quantity = max(0, int(order[2]))\n'
            '                    reduction = min(quantity, remaining)\n'
            '                    quantity -= reduction\n'
            '                    remaining -= reduction\n'
            '                    if quantity > 0:\n'
            '                        new_market.append([*order[:2], quantity, *order[3:]])\n'
            '                    reasons.append("WHEAT_SALE_REDUCED")\n'
            '                else:\n'
            '                    new_market.append(order)\n'
            '            action["market"] = market = new_market\n'
            '            shortfall = remaining\n'
            '\n'
            '        if shortfall:\n'
            '            price = max(1.0, float(wheat_price or 1.0))\n'
            '            spendable = max(0.0, float(money) - int(self.config["operating_cash_floor"]))\n'
            '            affordable_total = int(spendable // price)\n'
            '            existing_buys = _market_quantity(action, "BUY_PRODUCT", "WHEAT")\n'
            '            affordable_extra = max(0, affordable_total - existing_buys)\n'
            '            extra = min(\n'
            '                shortfall,\n'
            '                int(self.config["max_extra_wheat_per_step"]),\n'
            '                affordable_extra,\n'
            '            )\n'
            '            if extra > 0:\n'
            '                purchase_added = False\n'
            '                for order in market:\n'
            '                    if (\n'
            '                        isinstance(order, list)\n'
            '                        and len(order) >= 3\n'
            '                        and order[:2] == ["BUY_PRODUCT", "WHEAT"]\n'
            '                    ):\n'
            '                        order[2] = int(order[2]) + extra\n'
            '                        reasons.append("WHEAT_BUY_INCREASED")\n'
            '                        purchase_added = True\n'
            '                        break\n'
            '                else:\n'
            '                    if self.config["allow_market_buy_append"] and len(market) < max_orders:\n'
            '                        market.append(["BUY_PRODUCT", "WHEAT", extra])\n'
            '                        reasons.append("WHEAT_BUY_APPENDED")\n'
            '                        purchase_added = True\n'
            '                if purchase_added:\n'
            '                    shortfall -= extra\n'
            '\n'
            '        if shortfall and self.config["allow_animal_purchase_deferral"]:\n'
            '            filtered = [\n'
            '                order\n'
            '                for order in market\n'
            '                if not (\n'
            '                    isinstance(order, list)\n'
            '                    and len(order) >= 2\n'
            '                    and order[0] == "BUY_ANIMAL"\n'
            '                )\n'
            '            ]\n'
            '            if len(filtered) != len(market):\n'
            '                action["market"] = filtered\n'
            '                reasons.append("ANIMAL_PURCHASE_DEFERRED")\n'
            '        return reasons\n'
            '\n'
            '    def __call__(\n'
            '        self, observation: dict[str, Any], configuration: Any = None\n'
            '    ) -> dict[str, Any]:\n'
            '        snapshot = CodexObservationAdapter.parse(\n'
            '            observation,\n'
            '            configuration,\n'
            '            fallback_turns_per_day=int(self.config["turns_per_day"]),\n'
            '            fallback_episode_steps=int(self.config["episode_steps"]),\n'
            '        )\n'
            '        baseline = self.base_policy(observation, configuration)\n'
            '        action = deepcopy(baseline)\n'
            '        features = self._animal_features(snapshot.farm)\n'
            '        wheat_total = _wheat_total(snapshot.private)\n'
            '        detected_unfilled_wheat = self._settle_previous_wheat_buy(\n'
            '            wheat_total,\n'
            '            snapshot.clock.step,\n'
            '        )\n'
            '        threshold = int(self.config["critical_unfed_threshold"])\n'
            '        critical_positions = {\n'
            '            entry["position"]\n'
            '            for entry in features["animals"]\n'
            '            if not entry["fed_today"] and entry["consecutive_unfed"] >= threshold\n'
            '        }\n'
            '        critical_animal_count = len(critical_positions)\n'
            '        critical_positions.difference_update(\n'
            '            self._scheduled_feed_positions(action, snapshot.farm)\n'
            '        )\n'
            '        uncovered_critical_count = len(critical_positions)\n'
            '        reasons: list[str] = []\n'
            '        if snapshot.clock.is_eod:\n'
            '            reasons.extend(\n'
            '                self._apply_critical_feed_overrides(\n'
            '                    action,\n'
            '                    snapshot.farm,\n'
            '                    snapshot.private,\n'
            '                    critical_positions,\n'
            '                )\n'
            '            )\n'
            '        prices = snapshot.market.get("prices", {}) or {}\n'
            '        reasons.extend(\n'
            '            self._apply_market_guard(\n'
            '                action,\n'
            '                active_animals=int(features["active_animals"]),\n'
            '                wheat_total=wheat_total,\n'
            '                money=float(snapshot.farm.get("money", 0.0) or 0.0),\n'
            '                wheat_price=float(prices.get("WHEAT", 1.0) or 1.0),\n'
            '                max_orders=int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"]),\n'
            '                detected_unfilled_wheat=detected_unfilled_wheat,\n'
            '                critical_eod=snapshot.clock.is_eod and uncovered_critical_count > 0,\n'
            '            )\n'
            '        )\n'
            '        self._remember_wheat_buy(\n'
            '            action,\n'
            '            wheat_total=wheat_total,\n'
            '            step=snapshot.clock.step,\n'
            '        )\n'
            '        self.observation_count += 1\n'
            '        if action != baseline:\n'
            '            self.override_count += 1\n'
            '            self.override_reasons.update(reasons or ["UNCLASSIFIED_OVERRIDE"])\n'
            '            self.override_records.append(\n'
            '                {\n'
            '                    "step": snapshot.clock.step,\n'
            '                    "day": snapshot.clock.day,\n'
            '                    "hour": snapshot.clock.hour,\n'
            '                    "state_id": snapshot.state_id,\n'
            '                    "snapshot_fingerprint": snapshot.snapshot_fingerprint,\n'
            '                    "active_animals": int(features["active_animals"]),\n'
            '                    "critical_animals": critical_animal_count,\n'
            '                    "uncovered_critical_animals": uncovered_critical_count,\n'
            '                    "detected_unfilled_wheat": detected_unfilled_wheat,\n'
            '                    "wheat_total": wheat_total,\n'
            '                    "reasons": sorted(set(reasons)),\n'
            '                    "baseline_action_sha256": stable_payload_hash(baseline),\n'
            '                    "emitted_action_sha256": stable_payload_hash(action),\n'
            '                }\n'
            '            )\n'
            '        return action\n'
            '\n'
            '    def telemetry_snapshot(self) -> dict[str, Any]:\n'
            '        base = self.base_policy.codex_v9_instance.telemetry_snapshot()\n'
            '        return {\n'
            '            **base,\n'
            '            "agent_version": self.model_spec_version,\n'
            '            "base_agent_version": base["agent_version"],\n'
            '            "observations": self.observation_count,\n'
            '            "reactive_override_batches": self.override_count,\n'
            '            "reactive_override_reasons": dict(self.override_reasons),\n'
            '            "reactive_override_records": deepcopy(self.override_records),\n'
            '            "detected_unfilled_wheat_units": self.detected_unfilled_wheat_units,\n'
            '        }\n'
            '\n'
            '\n'
            'def create_codex_e17_reactive_agent(\n'
            '    run_context: dict[str, Any] | None = None,\n'
            '    config_path: Path | str | None = None,\n'
            '):\n'
            '    """Create a fail-closed Kaggle-compatible E17.1 reactive policy."""\n'
            '\n'
            '    instance = CodexE17ReactiveGuardedAgent(\n'
            '        run_context=run_context,\n'
            '        config_path=config_path,\n'
            '    )\n'
            '\n'
            '    def policy(\n'
            '        observation: dict[str, Any], configuration: Any = None\n'
            '    ) -> dict[str, Any]:\n'
            '        try:\n'
            '            action = instance(observation, configuration)\n'
            '            policy.codex_e17_last_error = None\n'
            '            return action\n'
            '        except (KeyboardInterrupt, SystemExit):\n'
            '            raise\n'
            '        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary\n'
            '            instance.error_count += 1\n'
            '            instance.fallback_count += 1\n'
            '            instance.last_exception = f"{type(exc).__name__}: {exc}"\n'
            '            policy.codex_e17_last_error = instance.last_exception\n'
            '            return deepcopy(_SAFE_PASS)\n'
            '\n'
            '    policy.codex_e17_instance = instance\n'
            '    policy.codex_e17_last_error = None\n'
            '    policy.__name__ = "codex_e17_1_3q_reactive_guarded_policy"\n'
            '    return policy\n'
            '\n'
            '\n'
            '__all__ = [\n'
            '    "DEFAULT_REACTIVE_CONFIG_PATH",\n'
            '    "REACTIVE_MODEL_SPEC_VERSION",\n'
            '    "CodexE17ReactiveGuardedAgent",\n'
            '    "create_codex_e17_reactive_agent",\n'
            '    "load_reactive_config",\n'
            ']\n',
 'true_reactive': '"""E17 Codex market-regime adaptation over the frozen guarded candidate.\n'
                  '\n'
                  'Unlike the V1 emergency-only guard, this candidate can change emitted market\n'
                  'orders in normal gameplay when observed prices, liquidity, feed coverage, or\n'
                  'deferred inventory cross preregistered bounds.  Unit routing and the frozen V9\n'
                  'routine remain untouched so the first experiment changes one causal family.\n'
                  '"""\n'
                  '\n'
                  'from __future__ import annotations\n'
                  '\n'
                  'import json\n'
                  'from collections import Counter\n'
                  'from copy import deepcopy\n'
                  'from pathlib import Path\n'
                  'from typing import Any\n'
                  '\n'
                  'from _codex_bundle.agricola.core.observation_contract import (\n'
                  '    CodexObservationAdapter,\n'
                  '    stable_payload_hash,\n'
                  ')\n'
                  'from _codex_bundle.agricola.strategy.codex.codex_e17_reactive_guarded import (\n'
                  '    create_codex_e17_reactive_agent,\n'
                  ')\n'
                  '\n'
                  'REPO_ROOT = Path(__file__).resolve().parents[4]\n'
                  'DEFAULT_TRUE_REACTIVE_CONFIG_PATH = (\n'
                  '    REPO_ROOT\n'
                  '    / "experiments"\n'
                  '    / "e17"\n'
                  '    / "configs"\n'
                  '    / "codex"\n'
                  '    / "CODEX_E17_1_TRUE_REACTIVE_V2.json"\n'
                  ')\n'
                  'TRUE_REACTIVE_MODEL_SPEC_VERSION = "CODEX-E17.1-TRUE-REACTIVE-V2"\n'
                  '_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}\n'
                  '\n'
                  '\n'
                  'def load_true_reactive_config(path: Path | str | None = None) -> dict[str, Any]:\n'
                  '    """Load and validate the bounded market-regime configuration."""\n'
                  '\n'
                  '    config_path = Path(path) if path is not None else DEFAULT_TRUE_REACTIVE_CONFIG_PATH\n'
                  '    config = json.loads(config_path.read_text(encoding="utf-8"))\n'
                  '    expected = {\n'
                  '        "candidate_id": "CODEX_E17_1_TRUE_REACTIVE_V2",\n'
                  '        "model_spec_version": TRUE_REACTIVE_MODEL_SPEC_VERSION,\n'
                  '        "base_policy": "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1",\n'
                  '        "causal_family": "MARKET_REGIME_ADAPTATION",\n'
                  '    }\n'
                  '    for key, value in expected.items():\n'
                  '        if config.get(key) != value:\n'
                  '            raise ValueError(f"unexpected {key}: {config.get(key)!r}")\n'
                  '    for key in (\n'
                  '        "turns_per_day",\n'
                  '        "episode_steps",\n'
                  '        "emergency_cash_floor",\n'
                  '        "feed_reserve_per_animal",\n'
                  '        "max_deferral_steps",\n'
                  '        "max_opportunistic_sale_units",\n'
                  '    ):\n'
                  '        if int(config.get(key, -1)) < 0:\n'
                  '            raise ValueError(f"{key} must be non-negative")\n'
                  '    for key in (\n'
                  '        "low_output_price_ratio",\n'
                  '        "high_output_price_ratio",\n'
                  '        "wheat_scarcity_price_ratio",\n'
                  '        "price_recovery_ratio",\n'
                  '        "shed_pressure_ratio",\n'
                  '    ):\n'
                  '        if float(config.get(key, 0.0)) <= 0:\n'
                  '            raise ValueError(f"{key} must be positive")\n'
                  '    if not 0 < float(config["shed_pressure_ratio"]) <= 1:\n'
                  '        raise ValueError("shed_pressure_ratio must be in (0, 1]")\n'
                  '    if not config.get("reference_prices") or not config.get("sellable_products"):\n'
                  '        raise ValueError("reference prices and sellable products are required")\n'
                  '    return deepcopy(config)\n'
                  '\n'
                  '\n'
                  'def _market_orders(action: dict[str, Any]) -> list[Any]:\n'
                  '    market = action.get("market", [])\n'
                  '    return list(market) if isinstance(market, list) else []\n'
                  '\n'
                  '\n'
                  'def _private_item_total(private: dict[str, Any], item: str) -> int:\n'
                  '    total = int((private.get("shed", {}) or {}).get(item, 0) or 0)\n'
                  '    for inventory in private.get("inventories", []) or []:\n'
                  '        if isinstance(inventory, dict):\n'
                  '            total += int(inventory.get(item, 0) or 0)\n'
                  '    return total\n'
                  '\n'
                  '\n'
                  'def _active_animal_count(farm: dict[str, Any]) -> int:\n'
                  '    return sum(\n'
                  '        1\n'
                  '        for row in farm.get("tiles", []) or []\n'
                  '        for tile in row\n'
                  '        if isinstance(tile, dict) and tile.get("animal")\n'
                  '    )\n'
                  '\n'
                  '\n'
                  'def _shed_total(private: dict[str, Any]) -> int:\n'
                  '    return sum(int(value or 0) for value in (private.get("shed", {}) or {}).values())\n'
                  '\n'
                  '\n'
                  'def _sell_quantity(orders: list[Any], item: str) -> int:\n'
                  '    return sum(\n'
                  '        max(0, int(order[2]))\n'
                  '        for order in orders\n'
                  '        if isinstance(order, list) and len(order) >= 3 and order[:2] == ["SELL", item]\n'
                  '    )\n'
                  '\n'
                  '\n'
                  'class CodexE17TrueReactiveAgent:\n'
                  '    """Bounded state-reactive market arbiter with an immutable default provider."""\n'
                  '\n'
                  '    def __init__(\n'
                  '        self,\n'
                  '        *,\n'
                  '        run_context: dict[str, Any] | None = None,\n'
                  '        config_path: Path | str | None = None,\n'
                  '    ) -> None:\n'
                  '        self.config = load_true_reactive_config(config_path)\n'
                  '        self.run_context = deepcopy(run_context or {})\n'
                  '        self.base_policy = create_codex_e17_reactive_agent(run_context=self.run_context)\n'
                  '        self.candidate_id = str(self.config["candidate_id"])\n'
                  '        self.model_spec_version = TRUE_REACTIVE_MODEL_SPEC_VERSION\n'
                  '        self.error_count = 0\n'
                  '        self.fallback_count = 0\n'
                  '        self.last_exception: str | None = None\n'
                  '        self.observation_count = 0\n'
                  '        self.override_count = 0\n'
                  '        self.regime_counts: Counter[str] = Counter()\n'
                  '        self.override_reasons: Counter[str] = Counter()\n'
                  '        self.override_records: list[dict[str, Any]] = []\n'
                  '        self.deferred_since: dict[str, int] = {}\n'
                  '        self._pending_record_index: int | None = None\n'
                  '\n'
                  '    def _price_ratio(self, item: str, prices: dict[str, Any]) -> float:\n'
                  '        reference = float(self.config["reference_prices"].get(item, 0.0) or 0.0)\n'
                  '        current = float(prices.get(item, 0.0) or 0.0)\n'
                  '        return current / reference if reference > 0 and current > 0 else 1.0\n'
                  '\n'
                  '    def _settle_previous_override(self, snapshot: Any) -> None:\n'
                  '        index = self._pending_record_index\n'
                  '        self._pending_record_index = None\n'
                  '        if index is None:\n'
                  '            return\n'
                  '        record = self.override_records[index]\n'
                  '        record["post_state"] = {\n'
                  '            "step": snapshot.clock.step,\n'
                  '            "cash": float(snapshot.farm.get("money", 0.0) or 0.0),\n'
                  '            "shed": deepcopy(snapshot.private.get("shed", {}) or {}),\n'
                  '            "snapshot_fingerprint": snapshot.snapshot_fingerprint,\n'
                  '        }\n'
                  '        record["outcome_evidence"] = (\n'
                  '            "Observed next-state delta; individual market-order attribution remains "\n'
                  '            "UNKNOWN when the emitted batch contains multiple orders."\n'
                  '        )\n'
                  '\n'
                  '    def _feed_reserve(self, farm: dict[str, Any]) -> int:\n'
                  '        return _active_animal_count(farm) * int(self.config["feed_reserve_per_animal"])\n'
                  '\n'
                  '    def _adapt_market(\n'
                  '        self,\n'
                  '        action: dict[str, Any],\n'
                  '        *,\n'
                  '        snapshot: Any,\n'
                  '    ) -> tuple[list[str], list[str], dict[str, Any]]:\n'
                  '        prices = snapshot.market.get("prices", {}) or {}\n'
                  '        private = snapshot.private\n'
                  '        farm = snapshot.farm\n'
                  '        money = float(farm.get("money", 0.0) or 0.0)\n'
                  '        shed_capacity = int(snapshot.configuration_snapshot["shedCapacity"])\n'
                  '        max_orders = int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"])\n'
                  '        shed_utilization = _shed_total(private) / max(1, shed_capacity)\n'
                  '        feed_reserve = self._feed_reserve(farm)\n'
                  '        wheat_total = _private_item_total(private, "WHEAT")\n'
                  '        terminal = snapshot.clock.is_terminal_action\n'
                  '        reasons: list[str] = []\n'
                  '        regimes: set[str] = set()\n'
                  '        retained_orders: list[Any] = []\n'
                  '        original_orders = _market_orders(action)\n'
                  '\n'
                  '        for raw_order in original_orders:\n'
                  '            if not isinstance(raw_order, list) or len(raw_order) < 3:\n'
                  '                retained_orders.append(raw_order)\n'
                  '                continue\n'
                  '            opcode, item = raw_order[:2]\n'
                  '            if opcode != "SELL" or item not in self.config["reference_prices"]:\n'
                  '                retained_orders.append(raw_order)\n'
                  '                continue\n'
                  '            try:\n'
                  '                quantity = max(0, int(raw_order[2]))\n'
                  '            except (TypeError, ValueError):\n'
                  '                retained_orders.append(raw_order)\n'
                  '                continue\n'
                  '            if quantity <= 0:\n'
                  '                continue\n'
                  '\n'
                  '            if (\n'
                  '                item == "WHEAT"\n'
                  '                and self.config["allow_wheat_reserve_protection"]\n'
                  '                and not terminal\n'
                  '            ):\n'
                  '                surplus = max(0, wheat_total - feed_reserve)\n'
                  '                protected_quantity = min(quantity, surplus)\n'
                  '                if protected_quantity < quantity:\n'
                  '                    reasons.append("WHEAT_RESERVE_PROTECTED")\n'
                  '                    regimes.add("INPUT_SCARCITY")\n'
                  '                quantity = protected_quantity\n'
                  '                if quantity <= 0:\n'
                  '                    continue\n'
                  '\n'
                  '            item_ratio = self._price_ratio(str(item), prices)\n'
                  '            deferred_at = self.deferred_since.get(str(item))\n'
                  '            max_deferral_reached = (\n'
                  '                deferred_at is not None\n'
                  '                and snapshot.clock.step - deferred_at\n'
                  '                >= int(self.config["max_deferral_steps"])\n'
                  '            )\n'
                  '            may_defer = (\n'
                  '                self.config["allow_low_price_sale_deferral"]\n'
                  '                and not terminal\n'
                  '                and money >= float(self.config["emergency_cash_floor"])\n'
                  '                and shed_utilization < float(self.config["shed_pressure_ratio"])\n'
                  '                and item_ratio <= float(self.config["low_output_price_ratio"])\n'
                  '                and not max_deferral_reached\n'
                  '            )\n'
                  '            if may_defer:\n'
                  '                self.deferred_since.setdefault(str(item), snapshot.clock.step)\n'
                  '                reasons.append("LOW_PRICE_SALE_DEFERRED")\n'
                  '                regimes.add("OUTPUT_PRESSURE")\n'
                  '                continue\n'
                  '\n'
                  '            retained_orders.append([*raw_order[:2], quantity, *raw_order[3:]])\n'
                  '            if item_ratio >= float(self.config["price_recovery_ratio"]):\n'
                  '                self.deferred_since.pop(str(item), None)\n'
                  '\n'
                  '        action["market"] = retained_orders\n'
                  '\n'
                  '        wheat_scarce = self._price_ratio("WHEAT", prices) >= float(\n'
                  '            self.config["wheat_scarcity_price_ratio"]\n'
                  '        )\n'
                  '        if wheat_scarce:\n'
                  '            regimes.add("INPUT_SCARCITY")\n'
                  '        planned_animals = sum(\n'
                  '            max(0, int(order[2]))\n'
                  '            for order in action["market"]\n'
                  '            if isinstance(order, list) and len(order) >= 3 and order[0] == "BUY_ANIMAL"\n'
                  '        )\n'
                  '        projected_feed_reserve = feed_reserve + planned_animals * int(\n'
                  '            self.config["feed_reserve_per_animal"]\n'
                  '        )\n'
                  '        feed_short = wheat_total < projected_feed_reserve\n'
                  '        if (\n'
                  '            wheat_scarce\n'
                  '            and feed_short\n'
                  '            and self.config["allow_scarcity_animal_deferral"]\n'
                  '            and not terminal\n'
                  '        ):\n'
                  '            filtered = [\n'
                  '                order\n'
                  '                for order in action["market"]\n'
                  '                if not (isinstance(order, list) and order and order[0] == "BUY_ANIMAL")\n'
                  '            ]\n'
                  '            if len(filtered) != len(action["market"]):\n'
                  '                action["market"] = filtered\n'
                  '                reasons.append("SCARCITY_ANIMAL_PURCHASE_DEFERRED")\n'
                  '                regimes.add("INPUT_SCARCITY")\n'
                  '\n'
                  '        if (\n'
                  '            self.config["allow_high_price_opportunistic_sale"]\n'
                  '            and not terminal\n'
                  '            and len(action["market"]) < max_orders\n'
                  '        ):\n'
                  '            scheduled_items = {\n'
                  '                str(order[1])\n'
                  '                for order in action["market"]\n'
                  '                if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL"\n'
                  '            }\n'
                  '            candidates: list[tuple[int, float, str, int, str]] = []\n'
                  '            shed = private.get("shed", {}) or {}\n'
                  '            for item in self.config["sellable_products"]:\n'
                  '                if item in scheduled_items:\n'
                  '                    continue\n'
                  '                quantity = int(shed.get(item, 0) or 0)\n'
                  '                if item == "WHEAT":\n'
                  '                    quantity = min(quantity, max(0, wheat_total - feed_reserve))\n'
                  '                if quantity <= 0:\n'
                  '                    continue\n'
                  '                item_ratio = self._price_ratio(item, prices)\n'
                  '                recovered_deferred = (\n'
                  '                    item in self.deferred_since\n'
                  '                    and item_ratio >= float(self.config["price_recovery_ratio"])\n'
                  '                )\n'
                  '                forced_release = (\n'
                  '                    item in self.deferred_since\n'
                  '                    and snapshot.clock.step - self.deferred_since[item]\n'
                  '                    >= int(self.config["max_deferral_steps"])\n'
                  '                )\n'
                  '                if (\n'
                  '                    item_ratio >= float(self.config["high_output_price_ratio"])\n'
                  '                    or recovered_deferred\n'
                  '                    or forced_release\n'
                  '                ):\n'
                  '                    candidates.append(\n'
                  '                        (\n'
                  '                            int(forced_release),\n'
                  '                            float(prices.get(item, 0.0) or 0.0),\n'
                  '                            item,\n'
                  '                            quantity,\n'
                  '                            "DEFERRED_SALE_RELEASED"\n'
                  '                            if forced_release\n'
                  '                            else "HIGH_PRICE_OPPORTUNISTIC_SALE",\n'
                  '                        )\n'
                  '                    )\n'
                  '            if candidates:\n'
                  '                _, _, item, available, sale_reason = max(candidates)\n'
                  '                quantity = min(\n'
                  '                    available,\n'
                  '                    int(self.config["max_opportunistic_sale_units"]),\n'
                  '                )\n'
                  '                action["market"].append(["SELL", item, quantity])\n'
                  '                self.deferred_since.pop(item, None)\n'
                  '                reasons.append(sale_reason)\n'
                  '                regimes.add(\n'
                  '                    "OUTPUT_RELEASE"\n'
                  '                    if sale_reason == "DEFERRED_SALE_RELEASED"\n'
                  '                    else "OUTPUT_OPPORTUNITY"\n'
                  '                )\n'
                  '\n'
                  '        if money < float(self.config["emergency_cash_floor"]):\n'
                  '            regimes.add("LIQUIDITY_STRESS")\n'
                  '        if not regimes:\n'
                  '            regimes.add("NORMAL")\n'
                  '        facts = {\n'
                  '            "money": money,\n'
                  '            "shed_utilization": round(shed_utilization, 6),\n'
                  '            "active_animals": _active_animal_count(farm),\n'
                  '            "feed_reserve": feed_reserve,\n'
                  '            "planned_animals": planned_animals,\n'
                  '            "projected_feed_reserve": projected_feed_reserve,\n'
                  '            "wheat_total": wheat_total,\n'
                  '            "wheat_price_ratio": round(self._price_ratio("WHEAT", prices), 6),\n'
                  '            "deferred_items": dict(sorted(self.deferred_since.items())),\n'
                  '            "market_orders_before": len(original_orders),\n'
                  '            "market_orders_after": len(action["market"]),\n'
                  '        }\n'
                  '        return sorted(regimes), reasons, facts\n'
                  '\n'
                  '    def __call__(\n'
                  '        self, observation: dict[str, Any], configuration: Any = None\n'
                  '    ) -> dict[str, Any]:\n'
                  '        snapshot = CodexObservationAdapter.parse(\n'
                  '            observation,\n'
                  '            configuration,\n'
                  '            fallback_turns_per_day=int(self.config["turns_per_day"]),\n'
                  '            fallback_episode_steps=int(self.config["episode_steps"]),\n'
                  '        )\n'
                  '        self._settle_previous_override(snapshot)\n'
                  '        provider_action = self.base_policy(observation, configuration)\n'
                  '        action = deepcopy(provider_action)\n'
                  '        regimes, reasons, facts = self._adapt_market(action, snapshot=snapshot)\n'
                  '        self.observation_count += 1\n'
                  '        self.regime_counts.update(regimes)\n'
                  '        if action != provider_action:\n'
                  '            self.override_count += 1\n'
                  '            self.override_reasons.update(reasons or ["UNCLASSIFIED_OVERRIDE"])\n'
                  '            record = {\n'
                  '                "step": snapshot.clock.step,\n'
                  '                "day": snapshot.clock.day,\n'
                  '                "hour": snapshot.clock.hour,\n'
                  '                "state_id": snapshot.state_id,\n'
                  '                "snapshot_fingerprint": snapshot.snapshot_fingerprint,\n'
                  '                "regimes": regimes,\n'
                  '                "reasons": sorted(set(reasons)),\n'
                  '                "facts": facts,\n'
                  '                "provider_action_sha256": stable_payload_hash(provider_action),\n'
                  '                "emitted_action_sha256": stable_payload_hash(action),\n'
                  '                "provider_market": deepcopy(provider_action.get("market", [])),\n'
                  '                "emitted_market": deepcopy(action.get("market", [])),\n'
                  '                "pre_state": {\n'
                  '                    "cash": float(snapshot.farm.get("money", 0.0) or 0.0),\n'
                  '                    "shed": deepcopy(snapshot.private.get("shed", {}) or {}),\n'
                  '                },\n'
                  '                "post_state": None,\n'
                  '                "outcome_evidence": "PENDING_NEXT_OBSERVATION",\n'
                  '            }\n'
                  '            self.override_records.append(record)\n'
                  '            self._pending_record_index = len(self.override_records) - 1\n'
                  '        return action\n'
                  '\n'
                  '    def telemetry_snapshot(self) -> dict[str, Any]:\n'
                  '        provider = self.base_policy.codex_e17_instance.telemetry_snapshot()\n'
                  '        return {\n'
                  '            **provider,\n'
                  '            "agent_version": self.model_spec_version,\n'
                  '            "base_agent_version": provider["agent_version"],\n'
                  '            "observations": self.observation_count,\n'
                  '            "true_reactive_override_batches": self.override_count,\n'
                  '            "true_reactive_override_reasons": dict(self.override_reasons),\n'
                  '            "market_regime_counts": dict(self.regime_counts),\n'
                  '            "true_reactive_override_records": deepcopy(self.override_records),\n'
                  '            "deferred_items_open": dict(sorted(self.deferred_since.items())),\n'
                  '        }\n'
                  '\n'
                  '\n'
                  'def create_codex_e17_true_reactive_agent(\n'
                  '    run_context: dict[str, Any] | None = None,\n'
                  '    config_path: Path | str | None = None,\n'
                  '):\n'
                  '    """Create a fail-closed Kaggle-compatible true-reactive policy."""\n'
                  '\n'
                  '    instance = CodexE17TrueReactiveAgent(\n'
                  '        run_context=run_context,\n'
                  '        config_path=config_path,\n'
                  '    )\n'
                  '\n'
                  '    def policy(\n'
                  '        observation: dict[str, Any], configuration: Any = None\n'
                  '    ) -> dict[str, Any]:\n'
                  '        try:\n'
                  '            action = instance(observation, configuration)\n'
                  '            policy.codex_e17_true_reactive_last_error = None\n'
                  '            return action\n'
                  '        except (KeyboardInterrupt, SystemExit):\n'
                  '            raise\n'
                  '        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary\n'
                  '            instance.error_count += 1\n'
                  '            instance.fallback_count += 1\n'
                  '            instance.last_exception = f"{type(exc).__name__}: {exc}"\n'
                  '            policy.codex_e17_true_reactive_last_error = instance.last_exception\n'
                  '            return deepcopy(_SAFE_PASS)\n'
                  '\n'
                  '    policy.codex_e17_true_reactive_instance = instance\n'
                  '    policy.codex_e17_true_reactive_last_error = None\n'
                  '    policy.__name__ = "codex_e17_1_true_reactive_v2_policy"\n'
                  '    return policy\n'
                  '\n'
                  '\n'
                  '__all__ = [\n'
                  '    "DEFAULT_TRUE_REACTIVE_CONFIG_PATH",\n'
                  '    "TRUE_REACTIVE_MODEL_SPEC_VERSION",\n'
                  '    "CodexE17TrueReactiveAgent",\n'
                  '    "create_codex_e17_true_reactive_agent",\n'
                  '    "load_true_reactive_config",\n'
                  ']\n',
 'routing_core': '"""State-driven E17.2 unit execution for the Codex 3Q target topology.\n'
                 '\n'
                 'Market, acquisitions, hires and land unlocks remain owned by the E17.1 V2\n'
                 'provider.  Unit commands are rebuilt from the current observation on every\n'
                 'turn, so routing does not inherit coordinates from an open-loop schedule.\n'
                 '"""\n'
                 '\n'
                 'from __future__ import annotations\n'
                 '\n'
                 'import json\n'
                 'from collections import Counter\n'
                 'from copy import deepcopy\n'
                 'from dataclasses import dataclass\n'
                 'from pathlib import Path\n'
                 'from typing import Any\n'
                 '\n'
                 'from _codex_bundle.agricola.core.observation_contract import (\n'
                 '    CodexObservationAdapter,\n'
                 '    stable_payload_hash,\n'
                 ')\n'
                 'from _codex_bundle.agricola.core.state import CROPS\n'
                 'from _codex_bundle.agricola.strategy.codex.codex_e17_true_reactive import (\n'
                 '    create_codex_e17_true_reactive_agent,\n'
                 ')\n'
                 '\n'
                 'REPO_ROOT = Path(__file__).resolve().parents[4]\n'
                 'DEFAULT_CORE_CONFIG_PATH = (\n'
                 '    REPO_ROOT\n'
                 '    / "experiments/e17/configs/codex/"\n'
                 '    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2.json"\n'
                 ')\n'
                 'CORE_MODEL_SPEC_VERSION = "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2"\n'
                 '_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}\n'
                 '_MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}\n'
                 '_ANIMALS = ("COW", "SHEEP", "GOOSE")\n'
                 '\n'
                 '\n'
                 '@dataclass(frozen=True)\n'
                 'class CoreTask:\n'
                 '    kind: str\n'
                 '    target: tuple[int, int]\n'
                 '    action: tuple[Any, ...]\n'
                 '    priority: int\n'
                 '    allowed_workers: tuple[int, ...] | None = None\n'
                 '    resource: str | None = None\n'
                 '\n'
                 '    @property\n'
                 '    def identity(self) -> tuple[str, tuple[int, int], tuple[Any, ...]]:\n'
                 '        return self.kind, self.target, self.action\n'
                 '\n'
                 '\n'
                 'def load_core_config(path: Path | str | None = None) -> dict[str, Any]:\n'
                 '    config_path = Path(path) if path is not None else DEFAULT_CORE_CONFIG_PATH\n'
                 '    config = json.loads(config_path.read_text(encoding="utf-8"))\n'
                 '    expected = {\n'
                 '        "candidate_id": "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2",\n'
                 '        "model_spec_version": CORE_MODEL_SPEC_VERSION,\n'
                 '        "base_policy": "CODEX-E17.1-TRUE-REACTIVE-V2",\n'
                 '        "causal_family": "REACTIVE_SERVICE_AND_ROUTING_CORE",\n'
                 '    }\n'
                 '    for key, value in expected.items():\n'
                 '        if config.get(key) != value:\n'
                 '            raise ValueError(f"unexpected {key}: {config.get(key)!r}")\n'
                 '    if int(config.get("turns_per_day", 0)) <= 0:\n'
                 '        raise ValueError("turns_per_day must be positive")\n'
                 '    if int(config.get("episode_steps", 0)) <= 0:\n'
                 '        raise ValueError("episode_steps must be positive")\n'
                 '    if int(config.get("activation_day", -1)) < 0:\n'
                 '        raise ValueError("activation_day must be non-negative")\n'
                 '    if not config.get("pasture_targets") or not config.get("task_priority"):\n'
                 '        raise ValueError("topology and task priorities are required")\n'
                 '    return deepcopy(config)\n'
                 '\n'
                 '\n'
                 'def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:\n'
                 '    return [\n'
                 '        tuple(farm.get("farmer", [4, 4])),\n'
                 '        *(tuple(pos) for pos in farm.get("hands", []) or []),\n'
                 '    ]\n'
                 '\n'
                 '\n'
                 'def _inventories(private: dict[str, Any], count: int) -> list[dict[str, Any]]:\n'
                 '    inventories = [\n'
                 '        inv if isinstance(inv, dict) else {}\n'
                 '        for inv in (private.get("inventories", []) or [])\n'
                 '    ]\n'
                 '    inventories.extend({} for _ in range(max(0, count - len(inventories))))\n'
                 '    return inventories[:count]\n'
                 '\n'
                 '\n'
                 'def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:\n'
                 '    x, y = position\n'
                 '    rows = farm.get("tiles", []) or []\n'
                 '    if not 0 <= y < len(rows) or not 0 <= x < len(rows[y]):\n'
                 '        return "OUT_OF_BOUNDS"\n'
                 '    return rows[y][x]\n'
                 '\n'
                 '\n'
                 'def _distance(source: tuple[int, int], target: tuple[int, int]) -> int:\n'
                 '    return abs(source[0] - target[0]) + abs(source[1] - target[1])\n'
                 '\n'
                 '\n'
                 'def _move(source: tuple[int, int], target: tuple[int, int]) -> list[str]:\n'
                 '    sx, sy = source\n'
                 '    tx, ty = target\n'
                 '    if sx < tx:\n'
                 '        return ["EAST"]\n'
                 '    if sx > tx:\n'
                 '        return ["WEST"]\n'
                 '    if sy < ty:\n'
                 '        return ["SOUTH"]\n'
                 '    if sy > ty:\n'
                 '        return ["NORTH"]\n'
                 '    return ["PASS"]\n'
                 '\n'
                 '\n'
                 'def _shed_access(board_size: int) -> tuple[tuple[int, int], ...]:\n'
                 '    half = board_size // 2\n'
                 '    return (\n'
                 '        (half - 1, half - 1),\n'
                 '        (half, half - 1),\n'
                 '        (half - 1, half),\n'
                 '        (half, half),\n'
                 '    )\n'
                 '\n'
                 '\n'
                 'def _owned(position: tuple[int, int], farm: dict[str, Any]) -> bool:\n'
                 '    return _tile(farm, position) != "LOCKED"\n'
                 '\n'
                 '\n'
                 'def _animal_tiles(farm: dict[str, Any]) -> list[tuple[tuple[int, int], dict[str, Any]]]:\n'
                 '    return [\n'
                 '        ((x, y), tile)\n'
                 '        for y, row in enumerate(farm.get("tiles", []) or [])\n'
                 '        for x, tile in enumerate(row)\n'
                 '        if isinstance(tile, dict) and tile.get("animal")\n'
                 '    ]\n'
                 '\n'
                 '\n'
                 'def _crop_tiles(farm: dict[str, Any]) -> list[tuple[tuple[int, int], dict[str, Any]]]:\n'
                 '    return [\n'
                 '        ((x, y), tile)\n'
                 '        for y, row in enumerate(farm.get("tiles", []) or [])\n'
                 '        for x, tile in enumerate(row)\n'
                 '        if isinstance(tile, dict) and tile.get("kind") == "PLANT"\n'
                 '    ]\n'
                 '\n'
                 '\n'
                 'class CodexE17ReactiveServiceRoutingCore:\n'
                 '    """Replan all unit work from the immutable Foundation snapshot."""\n'
                 '\n'
                 '    def __init__(\n'
                 '        self,\n'
                 '        *,\n'
                 '        run_context: dict[str, Any] | None = None,\n'
                 '        config_path: Path | str | None = None,\n'
                 '    ) -> None:\n'
                 '        self.config = load_core_config(config_path)\n'
                 '        self.run_context = deepcopy(run_context or {})\n'
                 '        self.base_policy = create_codex_e17_true_reactive_agent(\n'
                 '            run_context=self.run_context\n'
                 '        )\n'
                 '        self.candidate_id = str(self.config["candidate_id"])\n'
                 '        self.model_spec_version = CORE_MODEL_SPEC_VERSION\n'
                 '        self.last_assignments: dict[int, tuple[str, tuple[int, int], tuple[Any, ...]]] = {}\n'
                 '        self.observations = 0\n'
                 '        self.error_count = 0\n'
                 '        self.fallback_count = 0\n'
                 '        self.last_exception: str | None = None\n'
                 '        self.action_counts: Counter[str] = Counter()\n'
                 '        self.task_counts: Counter[str] = Counter()\n'
                 '        self.routing_commands = 0\n'
                 '        self.service_commands = 0\n'
                 '        self.market_mutations = 0\n'
                 '        self.records: list[dict[str, Any]] = []\n'
                 '        self.execution_outcomes: Counter[str] = Counter()\n'
                 '        self.ledger_records: list[dict[str, Any]] = []\n'
                 '        self._pending_ledger: list[int] = []\n'
                 '\n'
                 '    def _priority(self, kind: str) -> int:\n'
                 '        return int(self.config["task_priority"][kind])\n'
                 '\n'
                 '    def _settle_pending(self, snapshot: Any) -> None:\n'
                 '        positions = _positions(snapshot.farm)\n'
                 '        inventories = _inventories(snapshot.private, len(positions))\n'
                 '        for index in self._pending_ledger:\n'
                 '            record = self.ledger_records[index]\n'
                 '            worker_id = int(record["worker_id"])\n'
                 '            if worker_id >= len(positions):\n'
                 '                outcome = "UNKNOWN"\n'
                 '            else:\n'
                 '                action = record["requested"]\n'
                 '                op = str(action[0]) if action else "PASS"\n'
                 '                source = tuple(record["source"])\n'
                 '                target = tuple(record["target"])\n'
                 '                tile = _tile(snapshot.farm, target)\n'
                 '                inventory = inventories[worker_id]\n'
                 '                if op in _MOVES:\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if positions[worker_id] == target\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "PASS":\n'
                 '                    outcome = "UNKNOWN"\n'
                 '                elif op == "WATER":\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if isinstance(tile, dict)\n'
                 '                        and tile.get("kind") == "PLANT"\n'
                 '                        and (\n'
                 '                            bool(tile.get("watered_today", False))\n'
                 '                            or int(tile.get("consecutive_unwatered", 0) or 0) == 0\n'
                 '                        )\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "FEED":\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if isinstance(tile, dict)\n'
                 '                        and tile.get("animal")\n'
                 '                        and (\n'
                 '                            bool(tile.get("fed_today", False))\n'
                 '                            or int(tile.get("consecutive_unfed", 0) or 0) == 0\n'
                 '                        )\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "HARVEST":\n'
                 '                    after_yield = (\n'
                 '                        int(tile.get("yield_units", 0) or 0)\n'
                 '                        if isinstance(tile, dict)\n'
                 '                        else 0\n'
                 '                    )\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if after_yield < int(record["yield_before"])\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "PLANT":\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if isinstance(tile, dict)\n'
                 '                        and tile.get("kind") == "PLANT"\n'
                 '                        and len(action) >= 2\n'
                 '                        and tile.get("crop") == action[1]\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op in {"BUILD_PASTURE", "BUILD_COOP"}:\n'
                 '                    expected = op.removeprefix("BUILD_")\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if isinstance(tile, dict) and tile.get("kind") == expected\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "PLACE" and len(action) >= 2:\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if isinstance(tile, dict) and tile.get("animal") == action[1]\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "DIG":\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if stable_payload_hash(tile) != record["tile_before_sha256"]\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "PICKUP" and len(action) >= 2:\n'
                 '                    item = str(action[1])\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if int(inventory.get(item, 0) or 0)\n'
                 '                        > int(record["inventory_before"].get(item, 0) or 0)\n'
                 '                        else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                elif op == "DROP":\n'
                 '                    before_total = sum(\n'
                 '                        int(value or 0)\n'
                 '                        for value in record["inventory_before"].values()\n'
                 '                    )\n'
                 '                    after_total = sum(int(value or 0) for value in inventory.values())\n'
                 '                    outcome = "EXECUTED" if after_total < before_total else "NOT_EXECUTED"\n'
                 '                elif op == "CARE":\n'
                 '                    outcome = (\n'
                 '                        "EXECUTED"\n'
                 '                        if isinstance(tile, dict) and bool(tile.get("cared_today", False))\n'
                 '                        else "UNKNOWN" if snapshot.clock.hour == 0 else "NOT_EXECUTED"\n'
                 '                    )\n'
                 '                else:\n'
                 '                    outcome = "UNKNOWN"\n'
                 '                record["observed_position"] = list(positions[worker_id])\n'
                 '                record["source_position_unchanged"] = positions[worker_id] == source\n'
                 '            record["outcome"] = outcome\n'
                 '            record["post_state_id"] = snapshot.state_id\n'
                 '            record["post_snapshot_fingerprint"] = snapshot.snapshot_fingerprint\n'
                 '            self.execution_outcomes[outcome] += 1\n'
                 '        self._pending_ledger = []\n'
                 '\n'
                 '    def _task(\n'
                 '        self,\n'
                 '        kind: str,\n'
                 '        target: tuple[int, int],\n'
                 '        action: tuple[Any, ...],\n'
                 '        *,\n'
                 '        allowed_workers: tuple[int, ...] | None = None,\n'
                 '        resource: str | None = None,\n'
                 '    ) -> CoreTask:\n'
                 '        return CoreTask(\n'
                 '            kind,\n'
                 '            target,\n'
                 '            action,\n'
                 '            self._priority(kind),\n'
                 '            allowed_workers,\n'
                 '            resource,\n'
                 '        )\n'
                 '\n'
                 '    def _structure_tasks(\n'
                 '        self,\n'
                 '        farm: dict[str, Any],\n'
                 '        private: dict[str, Any],\n'
                 '        inventories: list[dict[str, Any]],\n'
                 '    ) -> list[CoreTask]:\n'
                 '        tasks: list[CoreTask] = []\n'
                 '        pasture_targets = [tuple(value) for value in self.config["pasture_targets"]]\n'
                 '        coop_targets = [tuple(value) for value in self.config["coop_targets"]]\n'
                 '        placed = Counter(tile["animal"] for _pos, tile in _animal_tiles(farm))\n'
                 '        shed = private.get("shed", {}) or {}\n'
                 '        held = Counter()\n'
                 '        for inventory in inventories:\n'
                 '            for animal in _ANIMALS:\n'
                 '                held[animal] += int(inventory.get(animal, 0) or 0)\n'
                 '        owned = Counter(\n'
                 '            {\n'
                 '                animal: placed[animal] + int(shed.get(animal, 0) or 0) + held[animal]\n'
                 '                for animal in _ANIMALS\n'
                 '            }\n'
                 '        )\n'
                 '\n'
                 '        structure_sets = {\n'
                 '            "PASTURE": pasture_targets,\n'
                 '            "COOP": coop_targets,\n'
                 '        }\n'
                 '        needed = {"PASTURE": owned["COW"] + owned["SHEEP"], "COOP": owned["GOOSE"]}\n'
                 '        for structure, targets in structure_sets.items():\n'
                 '            existing = sum(\n'
                 '                1\n'
                 '                for target in targets\n'
                 '                if isinstance(_tile(farm, target), dict)\n'
                 '                and _tile(farm, target).get("kind") == structure\n'
                 '            )\n'
                 '            remaining = max(0, needed[structure] - existing)\n'
                 '            for target in targets:\n'
                 '                if remaining <= 0 or not _owned(target, farm):\n'
                 '                    continue\n'
                 '                tile = _tile(farm, target)\n'
                 '                if tile is None:\n'
                 '                    tasks.append(\n'
                 '                        self._task(\n'
                 '                            "BUILD_STRUCTURE",\n'
                 '                            target,\n'
                 '                            (f"BUILD_{structure}",),\n'
                 '                        )\n'
                 '                    )\n'
                 '                    remaining -= 1\n'
                 '                elif isinstance(tile, dict) and tile.get("kind") == "WEED":\n'
                 '                    tasks.append(self._task("DIG_TARGET", target, ("DIG",)))\n'
                 '\n'
                 '        empty_structures = [\n'
                 '            (target, tile.get("kind"))\n'
                 '            for target in pasture_targets + coop_targets\n'
                 '            if isinstance((tile := _tile(farm, target)), dict)\n'
                 '            and tile.get("kind") in {"PASTURE", "COOP"}\n'
                 '            and not tile.get("animal")\n'
                 '        ]\n'
                 '        for target, structure in empty_structures:\n'
                 '            species = ("GOOSE",) if structure == "COOP" else ("COW", "SHEEP")\n'
                 '            for animal in species:\n'
                 '                carriers = tuple(\n'
                 '                    worker_id\n'
                 '                    for worker_id, inventory in enumerate(inventories)\n'
                 '                    if int(inventory.get(animal, 0) or 0) > 0\n'
                 '                )\n'
                 '                if carriers:\n'
                 '                    tasks.append(\n'
                 '                        self._task(\n'
                 '                            "PLACE_ANIMAL",\n'
                 '                            target,\n'
                 '                            ("PLACE", animal, 1),\n'
                 '                            allowed_workers=carriers,\n'
                 '                            resource=animal,\n'
                 '                        )\n'
                 '                    )\n'
                 '\n'
                 '        capacity = {\n'
                 '            "COW": sum(1 for _target, kind in empty_structures if kind == "PASTURE"),\n'
                 '            "SHEEP": sum(1 for _target, kind in empty_structures if kind == "PASTURE"),\n'
                 '            "GOOSE": sum(1 for _target, kind in empty_structures if kind == "COOP"),\n'
                 '        }\n'
                 '        accesses = _shed_access(len(farm.get("tiles", []) or []))\n'
                 '        for animal in _ANIMALS:\n'
                 '            count = min(int(shed.get(animal, 0) or 0), capacity[animal] + 1)\n'
                 '            for index in range(count):\n'
                 '                target = accesses[index % len(accesses)]\n'
                 '                tasks.append(\n'
                 '                    self._task(\n'
                 '                        "PICKUP_ANIMAL",\n'
                 '                        target,\n'
                 '                        ("PICKUP", animal, 1),\n'
                 '                        resource=animal,\n'
                 '                    )\n'
                 '                )\n'
                 '        return tasks\n'
                 '\n'
                 '    def _service_tasks(\n'
                 '        self,\n'
                 '        farm: dict[str, Any],\n'
                 '        private: dict[str, Any],\n'
                 '        inventories: list[dict[str, Any]],\n'
                 '        board_size: int,\n'
                 '        day: int,\n'
                 '    ) -> list[CoreTask]:\n'
                 '        tasks: list[CoreTask] = []\n'
                 '        for position, tile in _crop_tiles(farm):\n'
                 '            crop = str(tile.get("crop", ""))\n'
                 '            mature = day - int(tile.get("planted_day", day)) >= int(\n'
                 '                CROPS.get(crop, {}).get("first_yield_day", 10**6)\n'
                 '            )\n'
                 '            if mature and int(tile.get("yield_units", 0) or 0) > 0:\n'
                 '                tasks.append(self._task("HARVEST", position, ("HARVEST",)))\n'
                 '            if day + 1 >= int(self.config["episode_steps"]) // int(\n'
                 '                self.config["turns_per_day"]\n'
                 '            ):\n'
                 '                continue\n'
                 '            if not bool(tile.get("watered_today", False)):\n'
                 '                kind = (\n'
                 '                    "CRITICAL_WATER"\n'
                 '                    if int(tile.get("consecutive_unwatered", 0) or 0)\n'
                 '                    >= int(self.config["critical_unwatered_threshold"])\n'
                 '                    else "WATER"\n'
                 '                )\n'
                 '                tasks.append(self._task(kind, position, ("WATER",)))\n'
                 '\n'
                 '        unfed = []\n'
                 '        for position, tile in _animal_tiles(farm):\n'
                 '            if int(tile.get("yield_units", 0) or 0) > 0:\n'
                 '                tasks.append(self._task("HARVEST", position, ("HARVEST",)))\n'
                 '            if day + 1 >= int(self.config["episode_steps"]) // int(\n'
                 '                self.config["turns_per_day"]\n'
                 '            ):\n'
                 '                continue\n'
                 '            critical = (\n'
                 '                not bool(tile.get("fed_today", False))\n'
                 '                and int(tile.get("consecutive_unfed", 0) or 0)\n'
                 '                >= int(self.config["critical_unfed_threshold"])\n'
                 '            )\n'
                 '            if critical:\n'
                 '                unfed.append(position)\n'
                 '                carriers = tuple(\n'
                 '                    worker_id\n'
                 '                    for worker_id, inventory in enumerate(inventories)\n'
                 '                    if int(inventory.get("WHEAT", 0) or 0) > 0\n'
                 '                )\n'
                 '                if carriers:\n'
                 '                    tasks.append(\n'
                 '                        self._task(\n'
                 '                            "CRITICAL_FEED",\n'
                 '                            position,\n'
                 '                            ("FEED",),\n'
                 '                            allowed_workers=carriers,\n'
                 '                            resource="WHEAT",\n'
                 '                        )\n'
                 '                    )\n'
                 '        carried_wheat = sum(int(inv.get("WHEAT", 0) or 0) for inv in inventories)\n'
                 '        shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)\n'
                 '        desired = min(\n'
                 '            len(unfed),\n'
                 '            int(self.config["wheat_carrier_target"])\n'
                 '            * int(self.config["wheat_pickup_batch"]),\n'
                 '        )\n'
                 '        shortage = max(0, desired - carried_wheat)\n'
                 '        accesses = _shed_access(board_size)\n'
                 '        pickup_count = min(\n'
                 '            int(self.config["wheat_carrier_target"]),\n'
                 '            (min(shortage, shed_wheat) + int(self.config["wheat_pickup_batch"]) - 1)\n'
                 '            // int(self.config["wheat_pickup_batch"]),\n'
                 '        )\n'
                 '        remaining_wheat = shed_wheat\n'
                 '        for index in range(pickup_count):\n'
                 '            quantity = min(int(self.config["wheat_pickup_batch"]), remaining_wheat)\n'
                 '            if quantity <= 0:\n'
                 '                break\n'
                 '            tasks.append(\n'
                 '                self._task(\n'
                 '                    "PICKUP_WHEAT",\n'
                 '                    accesses[index % len(accesses)],\n'
                 '                    ("PICKUP", "WHEAT", quantity),\n'
                 '                    resource="WHEAT",\n'
                 '                )\n'
                 '            )\n'
                 '            remaining_wheat -= quantity\n'
                 '        return tasks\n'
                 '\n'
                 '    def _terminal_drop_tasks(\n'
                 '        self,\n'
                 '        *,\n'
                 '        inventories: list[dict[str, Any]],\n'
                 '        positions: list[tuple[int, int]],\n'
                 '        board_size: int,\n'
                 '        day: int,\n'
                 '    ) -> list[CoreTask]:\n'
                 '        if day + 1 < int(self.config["episode_steps"]) // int(\n'
                 '            self.config["turns_per_day"]\n'
                 '        ):\n'
                 '            return []\n'
                 '        accesses = _shed_access(board_size)\n'
                 '        tasks: list[CoreTask] = []\n'
                 '        for worker_id, inventory in enumerate(inventories):\n'
                 '            sellable = sum(\n'
                 '                int(quantity or 0)\n'
                 '                for item, quantity in inventory.items()\n'
                 '                if item not in _ANIMALS and item != "WHEAT"\n'
                 '            )\n'
                 '            if sellable <= 0:\n'
                 '                continue\n'
                 '            target = min(\n'
                 '                accesses,\n'
                 '                key=lambda value: (_distance(positions[worker_id], value), value),\n'
                 '            )\n'
                 '            tasks.append(\n'
                 '                self._task(\n'
                 '                    "DROP_INVENTORY",\n'
                 '                    target,\n'
                 '                    ("DROP",),\n'
                 '                    allowed_workers=(worker_id,),\n'
                 '                )\n'
                 '            )\n'
                 '        return tasks\n'
                 '\n'
                 '    def _crop_choice(\n'
                 '        self,\n'
                 '        target: tuple[int, int],\n'
                 '        *,\n'
                 '        day: int,\n'
                 '        available_seeds: dict[str, int],\n'
                 '    ) -> str | None:\n'
                 '        wheat_targets = {tuple(value) for value in self.config["wheat_crop_targets"]}\n'
                 '        if target in wheat_targets and int(available_seeds.get("WHEAT", 0) or 0) > 0:\n'
                 '            return "WHEAT"\n'
                 '        for crop in ("MELON", "STRAWBERRY", "TOMATO", "CARROT", "WHEAT"):\n'
                 '            if day <= int(self.config["crop_cutoffs"][crop]) and int(\n'
                 '                available_seeds.get(crop, 0) or 0\n'
                 '            ) > 0:\n'
                 '                return crop\n'
                 '        return None\n'
                 '\n'
                 '    def _crop_setup_tasks(\n'
                 '        self,\n'
                 '        *,\n'
                 '        farm: dict[str, Any],\n'
                 '        private: dict[str, Any],\n'
                 '        day: int,\n'
                 '    ) -> list[CoreTask]:\n'
                 '        if day > int(self.config["plant_cutoff_day"]):\n'
                 '            return []\n'
                 '        livestock = {\n'
                 '            *(tuple(value) for value in self.config["pasture_targets"]),\n'
                 '            *(tuple(value) for value in self.config["coop_targets"]),\n'
                 '        }\n'
                 '        seeds = dict(private.get("seeds", {}) or {})\n'
                 '        tasks: list[CoreTask] = []\n'
                 '        for y, row in enumerate(farm.get("tiles", []) or []):\n'
                 '            for x, tile in enumerate(row):\n'
                 '                target = (x, y)\n'
                 '                if target in livestock or tile == "LOCKED":\n'
                 '                    continue\n'
                 '                if isinstance(tile, dict) and tile.get("kind") == "WEED":\n'
                 '                    tasks.append(self._task("DIG_TARGET", target, ("DIG",)))\n'
                 '                    continue\n'
                 '                if tile is not None:\n'
                 '                    continue\n'
                 '                crop = self._crop_choice(target, day=day, available_seeds=seeds)\n'
                 '                if crop is not None:\n'
                 '                    tasks.append(\n'
                 '                        self._task(\n'
                 '                            "PLANT",\n'
                 '                            target,\n'
                 '                            ("PLANT", crop),\n'
                 '                            resource=crop,\n'
                 '                        )\n'
                 '                    )\n'
                 '        return tasks\n'
                 '\n'
                 '    def _assign(\n'
                 '        self,\n'
                 '        tasks: list[CoreTask],\n'
                 '        positions: list[tuple[int, int]],\n'
                 '        private: dict[str, Any],\n'
                 '    ) -> dict[int, CoreTask]:\n'
                 '        assignments: dict[int, CoreTask] = {}\n'
                 '        available_workers = set(range(len(positions)))\n'
                 '        reserved_targets: set[tuple[str, tuple[int, int]]] = set()\n'
                 '        remaining_seeds = Counter(private.get("seeds", {}) or {})\n'
                 '        remaining_shed = Counter(private.get("shed", {}) or {})\n'
                 '        remaining_tasks = list(tasks)\n'
                 '        while available_workers and remaining_tasks:\n'
                 '            candidates: list[tuple[int, int, int, int]] = []\n'
                 '            for task_index, task in enumerate(remaining_tasks):\n'
                 '                target_key = (task.kind, task.target)\n'
                 '                if target_key in reserved_targets:\n'
                 '                    continue\n'
                 '                if task.kind == "PLANT" and remaining_seeds[str(task.resource)] <= 0:\n'
                 '                    continue\n'
                 '                if task.kind in {"PICKUP_WHEAT", "PICKUP_ANIMAL"}:\n'
                 '                    quantity = int(task.action[2]) if len(task.action) >= 3 else 1\n'
                 '                    if remaining_shed[str(task.resource)] < quantity:\n'
                 '                        continue\n'
                 '                eligible = available_workers\n'
                 '                if task.allowed_workers is not None:\n'
                 '                    eligible = available_workers.intersection(task.allowed_workers)\n'
                 '                for worker_id in eligible:\n'
                 '                    candidates.append(\n'
                 '                        (\n'
                 '                            task.priority,\n'
                 '                            _distance(positions[worker_id], task.target)\n'
                 '                            - (\n'
                 '                                3\n'
                 '                                if self.last_assignments.get(worker_id) == task.identity\n'
                 '                                else 0\n'
                 '                            ),\n'
                 '                            worker_id,\n'
                 '                            task_index,\n'
                 '                        )\n'
                 '                    )\n'
                 '            if not candidates:\n'
                 '                break\n'
                 '            _priority, _distance_score, worker_id, task_index = min(candidates)\n'
                 '            task = remaining_tasks.pop(task_index)\n'
                 '            target_key = (task.kind, task.target)\n'
                 '            assignments[worker_id] = task\n'
                 '            available_workers.remove(worker_id)\n'
                 '            reserved_targets.add(target_key)\n'
                 '            if task.kind == "PLANT":\n'
                 '                remaining_seeds[str(task.resource)] -= 1\n'
                 '            elif task.kind in {"PICKUP_WHEAT", "PICKUP_ANIMAL"}:\n'
                 '                remaining_shed[str(task.resource)] -= (\n'
                 '                    int(task.action[2]) if len(task.action) >= 3 else 1\n'
                 '                )\n'
                 '        return assignments\n'
                 '\n'
                 '    def __call__(\n'
                 '        self, observation: dict[str, Any], configuration: Any = None\n'
                 '    ) -> dict[str, Any]:\n'
                 '        snapshot = CodexObservationAdapter.parse(\n'
                 '            observation,\n'
                 '            configuration,\n'
                 '            fallback_turns_per_day=int(self.config["turns_per_day"]),\n'
                 '            fallback_episode_steps=int(self.config["episode_steps"]),\n'
                 '        )\n'
                 '        self._settle_pending(snapshot)\n'
                 '        provider = self.base_policy(observation, configuration)\n'
                 '        if snapshot.clock.day < int(self.config["activation_day"]):\n'
                 '            self.observations += 1\n'
                 '            return deepcopy(provider)\n'
                 '        farm = snapshot.farm\n'
                 '        private = snapshot.private\n'
                 '        positions = _positions(farm)\n'
                 '        inventories = _inventories(private, len(positions))\n'
                 '        board_size = int(snapshot.configuration_snapshot["boardSize"])\n'
                 '        tasks = [\n'
                 '            *self._service_tasks(\n'
                 '                farm,\n'
                 '                private,\n'
                 '                inventories,\n'
                 '                board_size,\n'
                 '                snapshot.clock.day,\n'
                 '            ),\n'
                 '            *self._terminal_drop_tasks(\n'
                 '                inventories=inventories,\n'
                 '                positions=positions,\n'
                 '                board_size=board_size,\n'
                 '                day=snapshot.clock.day,\n'
                 '            ),\n'
                 '        ]\n'
                 '        if snapshot.clock.day + 1 < int(self.config["episode_steps"]) // int(\n'
                 '            self.config["turns_per_day"]\n'
                 '        ):\n'
                 '            tasks.extend(self._structure_tasks(farm, private, inventories))\n'
                 '            tasks.extend(\n'
                 '                self._crop_setup_tasks(\n'
                 '                    farm=farm,\n'
                 '                    private=private,\n'
                 '                    day=snapshot.clock.day,\n'
                 '                )\n'
                 '            )\n'
                 '        assignments = self._assign(tasks, positions, private)\n'
                 '        unit_actions: list[list[Any]] = []\n'
                 '        next_assignments: dict[int, tuple[str, tuple[int, int], tuple[Any, ...]]] = {}\n'
                 '        for worker_id, position in enumerate(positions):\n'
                 '            task = assignments.get(worker_id)\n'
                 '            if task is None:\n'
                 '                emitted = ["PASS"]\n'
                 '            elif position == task.target:\n'
                 '                emitted = list(task.action)\n'
                 '            else:\n'
                 '                emitted = _move(position, task.target)\n'
                 '            unit_actions.append(emitted)\n'
                 '            self.action_counts[str(emitted[0])] += 1\n'
                 '            if emitted[0] in _MOVES:\n'
                 '                self.routing_commands += 1\n'
                 '            elif emitted[0] != "PASS":\n'
                 '                self.service_commands += 1\n'
                 '            if task is not None:\n'
                 '                self.task_counts[task.kind] += 1\n'
                 '                next_assignments[worker_id] = task.identity\n'
                 '            source_tile = _tile(farm, position)\n'
                 '            if emitted[0] in _MOVES:\n'
                 '                target = tuple(\n'
                 '                    value + delta\n'
                 '                    for value, delta in zip(\n'
                 '                        position,\n'
                 '                        {\n'
                 '                            "NORTH": (0, -1),\n'
                 '                            "SOUTH": (0, 1),\n'
                 '                            "EAST": (1, 0),\n'
                 '                            "WEST": (-1, 0),\n'
                 '                        }[str(emitted[0])],\n'
                 '                        strict=True,\n'
                 '                    )\n'
                 '                )\n'
                 '            else:\n'
                 '                target = position\n'
                 '            self.ledger_records.append(\n'
                 '                {\n'
                 '                    "step": snapshot.clock.step,\n'
                 '                    "day": snapshot.clock.day,\n'
                 '                    "hour": snapshot.clock.hour,\n'
                 '                    "worker_id": worker_id,\n'
                 '                    "state_id": snapshot.state_id,\n'
                 '                    "snapshot_fingerprint": snapshot.snapshot_fingerprint,\n'
                 '                    "source": list(position),\n'
                 '                    "target": list(target),\n'
                 '                    "requested": deepcopy(emitted),\n'
                 '                    "task_kind": task.kind if task is not None else "IDLE",\n'
                 '                    "tile_before_sha256": stable_payload_hash(source_tile),\n'
                 '                    "yield_before": (\n'
                 '                        int(source_tile.get("yield_units", 0) or 0)\n'
                 '                        if isinstance(source_tile, dict)\n'
                 '                        else 0\n'
                 '                    ),\n'
                 '                    "inventory_before": deepcopy(inventories[worker_id]),\n'
                 '                    "outcome": "PENDING_NEXT_OBSERVATION",\n'
                 '                }\n'
                 '            )\n'
                 '            self._pending_ledger.append(len(self.ledger_records) - 1)\n'
                 '        action = {\n'
                 '            "farmer": unit_actions[0] if unit_actions else ["PASS"],\n'
                 '            "hands": unit_actions[1:],\n'
                 '            "market": deepcopy(provider.get("market", [])),\n'
                 '        }\n'
                 '        if action["market"] != provider.get("market", []):\n'
                 '            self.market_mutations += 1\n'
                 '        self.last_assignments = next_assignments\n'
                 '        self.observations += 1\n'
                 '        if len(self.records) < 24 and action != provider:\n'
                 '            self.records.append(\n'
                 '                {\n'
                 '                    "step": snapshot.clock.step,\n'
                 '                    "day": snapshot.clock.day,\n'
                 '                    "hour": snapshot.clock.hour,\n'
                 '                    "state_id": snapshot.state_id,\n'
                 '                    "snapshot_fingerprint": snapshot.snapshot_fingerprint,\n'
                 '                    "provider_action_sha256": stable_payload_hash(provider),\n'
                 '                    "emitted_action_sha256": stable_payload_hash(action),\n'
                 '                    "task_count": len(tasks),\n'
                 '                    "assignments": {\n'
                 '                        str(worker_id): {\n'
                 '                            "kind": task.kind,\n'
                 '                            "target": list(task.target),\n'
                 '                            "action": list(task.action),\n'
                 '                        }\n'
                 '                        for worker_id, task in sorted(assignments.items())\n'
                 '                    },\n'
                 '                }\n'
                 '            )\n'
                 '        return action\n'
                 '\n'
                 '    def telemetry_snapshot(self) -> dict[str, Any]:\n'
                 '        for index in self._pending_ledger:\n'
                 '            self.ledger_records[index]["outcome"] = "UNKNOWN"\n'
                 '            self.execution_outcomes["UNKNOWN"] += 1\n'
                 '        self._pending_ledger = []\n'
                 '        provider = self.base_policy.codex_e17_true_reactive_instance.telemetry_snapshot()\n'
                 '        productive = self.service_commands\n'
                 '        return {\n'
                 '            "agent_version": self.model_spec_version,\n'
                 '            "base_agent_version": provider["agent_version"],\n'
                 '            "observations": self.observations,\n'
                 '            "routing_commands": self.routing_commands,\n'
                 '            "service_commands": self.service_commands,\n'
                 '            "move_per_service": self.routing_commands / productive if productive else None,\n'
                 '            "market_mutations": self.market_mutations,\n'
                 '            "action_counts": dict(self.action_counts),\n'
                 '            "task_counts": dict(self.task_counts),\n'
                 '            "execution_outcomes": dict(self.execution_outcomes),\n'
                 '            "ledger_record_count": len(self.ledger_records),\n'
                 '            "ledger_records": deepcopy(self.ledger_records),\n'
                 '            "decision_samples": deepcopy(self.records),\n'
                 '            "provider": provider,\n'
                 '        }\n'
                 '\n'
                 '\n'
                 'def create_codex_e17_reactive_service_routing_core(\n'
                 '    run_context: dict[str, Any] | None = None,\n'
                 '    config_path: Path | str | None = None,\n'
                 '):\n'
                 '    instance = CodexE17ReactiveServiceRoutingCore(\n'
                 '        run_context=run_context,\n'
                 '        config_path=config_path,\n'
                 '    )\n'
                 '\n'
                 '    def policy(\n'
                 '        observation: dict[str, Any], configuration: Any = None\n'
                 '    ) -> dict[str, Any]:\n'
                 '        try:\n'
                 '            action = instance(observation, configuration)\n'
                 '            policy.codex_e17_service_routing_core_last_error = None\n'
                 '            return action\n'
                 '        except (KeyboardInterrupt, SystemExit):\n'
                 '            raise\n'
                 '        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary\n'
                 '            instance.error_count += 1\n'
                 '            instance.fallback_count += 1\n'
                 '            instance.last_exception = f"{type(exc).__name__}: {exc}"\n'
                 '            policy.codex_e17_service_routing_core_last_error = instance.last_exception\n'
                 '            return deepcopy(_SAFE_PASS)\n'
                 '\n'
                 '    policy.codex_e17_service_routing_core_instance = instance\n'
                 '    policy.codex_e17_service_routing_core_last_error = None\n'
                 '    policy.__name__ = "codex_e17_2_reactive_service_routing_core_v2_policy"\n'
                 '    return policy\n'
                 '\n'
                 '\n'
                 '__all__ = [\n'
                 '    "CORE_MODEL_SPEC_VERSION",\n'
                 '    "CodexE17ReactiveServiceRoutingCore",\n'
                 '    "CoreTask",\n'
                 '    "create_codex_e17_reactive_service_routing_core",\n'
                 '    "load_core_config",\n'
                 ']\n',
 'routing_v3': '"""E17.2 D28 handoff with state-driven service and terminal cash-out.\n'
               '\n'
               "The V3 keeps the E17.1 provider's acquisition and market schedule until the\n"
               'terminal liquidation window.  From day 28 it owns all unit routing, prepares\n'
               'the last biological production cycle, and on day 29 sells products that are\n'
               'already in the shed or are deposited by a unit earlier in the same batch.\n'
               '"""\n'
               '\n'
               'from __future__ import annotations\n'
               '\n'
               'import json\n'
               'from collections import Counter\n'
               'from copy import deepcopy\n'
               'from pathlib import Path\n'
               'from typing import Any\n'
               '\n'
               'from _codex_bundle.agricola.core.observation_contract import (\n'
               '    CodexObservationAdapter,\n'
               '    stable_payload_hash,\n'
               ')\n'
               'from _codex_bundle.agricola.core.state import CROPS\n'
               'from _codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_core import (\n'
               '    CodexE17ReactiveServiceRoutingCore,\n'
               '    CoreTask,\n'
               '    _animal_tiles,\n'
               '    _crop_tiles,\n'
               '    _distance,\n'
               '    _inventories,\n'
               '    _positions,\n'
               '    _shed_access,\n'
               ')\n'
               '\n'
               'REPO_ROOT = Path(__file__).resolve().parents[4]\n'
               'DEFAULT_V3_CONFIG_PATH = (\n'
               '    REPO_ROOT\n'
               '    / "experiments/e17/configs/codex/"\n'
               '    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28.json"\n'
               ')\n'
               'V3_MODEL_SPEC_VERSION = "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28"\n'
               '_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}\n'
               '_ANIMALS = {"COW", "SHEEP", "GOOSE"}\n'
               '_ANIMAL_PRODUCTS = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}\n'
               '_MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}\n'
               '\n'
               '\n'
               'def load_v3_config(path: Path | str | None = None) -> dict[str, Any]:\n'
               '    """Load the causally bounded D28 service/liquidation configuration."""\n'
               '\n'
               '    config_path = Path(path) if path is not None else DEFAULT_V3_CONFIG_PATH\n'
               '    config = json.loads(config_path.read_text(encoding="utf-8"))\n'
               '    expected = {\n'
               '        "candidate_id": "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28",\n'
               '        "model_spec_version": V3_MODEL_SPEC_VERSION,\n'
               '        "base_policy": "CODEX-E17.1-TRUE-REACTIVE-V2",\n'
               '        "causal_family": "REACTIVE_SERVICE_ROUTING_AND_TERMINAL_LIQUIDATION",\n'
               '        "activation_day": 28,\n'
               '        "liquidation_day": 29,\n'
               '    }\n'
               '    for key, value in expected.items():\n'
               '        if config.get(key) != value:\n'
               '            raise ValueError(f"unexpected {key}: {config.get(key)!r}")\n'
               '    if int(config.get("turns_per_day", 0)) <= 0:\n'
               '        raise ValueError("turns_per_day must be positive")\n'
               '    if int(config.get("episode_steps", 0)) <= 0:\n'
               '        raise ValueError("episode_steps must be positive")\n'
               '    if not config.get("sellable_products") or not config.get("task_priority"):\n'
               '        raise ValueError("sellable products and task priorities are required")\n'
               '    return deepcopy(config)\n'
               '\n'
               '\n'
               'class CodexE17ReactiveServiceRoutingV3(CodexE17ReactiveServiceRoutingCore):\n'
               '    """Own D28+ unit work and complete same-batch terminal liquidation."""\n'
               '\n'
               '    def __init__(\n'
               '        self,\n'
               '        *,\n'
               '        run_context: dict[str, Any] | None = None,\n'
               '        config_path: Path | str | None = None,\n'
               '    ) -> None:\n'
               '        # Initialize the stable provider and telemetry without changing the\n'
               '        # frozen V2 loader, then bind the independently validated V3 config.\n'
               '        super().__init__(run_context=run_context)\n'
               '        self.config = load_v3_config(config_path)\n'
               '        self.candidate_id = str(self.config["candidate_id"])\n'
               '        self.model_spec_version = V3_MODEL_SPEC_VERSION\n'
               '        self.coordinated_market_batches = 0\n'
               '        self.coordinated_sell_orders = 0\n'
               '        self.coordinated_sell_units_requested = 0\n'
               '        self.non_sell_preservation_failures = 0\n'
               '        self.market_execution_outcomes: Counter[str] = Counter()\n'
               '        self.market_ledger_records: list[dict[str, Any]] = []\n'
               '        self._pending_market_ledger: list[int] = []\n'
               '        self._routing_clock: Any = None\n'
               '        self._routing_board_size = 10\n'
               '        self._routing_farm: dict[str, Any] = {}\n'
               '        self._routing_prices: dict[str, float] = {}\n'
               '        self._routing_private: dict[str, Any] = {}\n'
               '        self._routing_shed_capacity = 100\n'
               '\n'
               '    def _settle_pending(self, snapshot: Any) -> None:\n'
               '        pending = list(self._pending_ledger)\n'
               '        super()._settle_pending(snapshot)\n'
               '        for index in pending:\n'
               '            record = self.ledger_records[index]\n'
               '            requested = record.get("requested", [])\n'
               '            if (\n'
               '                record.get("hour") == int(self.config["turns_per_day"]) - 1\n'
               '                and requested\n'
               '                and requested[0] in _MOVES\n'
               '                and record.get("outcome") == "NOT_EXECUTED"\n'
               '            ):\n'
               '                # EOD resets every worker to the shed before the next callback;\n'
               '                # the post-state cannot distinguish an executed move from a no-op.\n'
               '                record["outcome"] = "UNKNOWN"\n'
               '                record["outcome_note"] = "EOD_POSITION_RESET_OBSCURES_MOVE"\n'
               '                self.execution_outcomes["NOT_EXECUTED"] -= 1\n'
               '                self.execution_outcomes["UNKNOWN"] += 1\n'
               '\n'
               '    def _structure_tasks(\n'
               '        self,\n'
               '        farm: dict[str, Any],\n'
               '        private: dict[str, Any],\n'
               '        inventories: list[dict[str, Any]],\n'
               '    ) -> list[CoreTask]:\n'
               '        del farm, private, inventories\n'
               '        return []\n'
               '\n'
               '    def _crop_setup_tasks(\n'
               '        self,\n'
               '        *,\n'
               '        farm: dict[str, Any],\n'
               '        private: dict[str, Any],\n'
               '        day: int,\n'
               '    ) -> list[CoreTask]:\n'
               '        del farm, private, day\n'
               '        return []\n'
               '\n'
               '    def _service_tasks(\n'
               '        self,\n'
               '        farm: dict[str, Any],\n'
               '        private: dict[str, Any],\n'
               '        inventories: list[dict[str, Any]],\n'
               '        board_size: int,\n'
               '        day: int,\n'
               '    ) -> list[CoreTask]:\n'
               '        tasks: list[CoreTask] = []\n'
               '        final_day = int(self.config["episode_steps"]) // int(\n'
               '            self.config["turns_per_day"]\n'
               '        ) - 1\n'
               '        terminal_day = day >= final_day\n'
               '\n'
               '        for position, tile in _crop_tiles(farm):\n'
               '            crop = str(tile.get("crop", ""))\n'
               '            planted_day = int(tile.get("planted_day", day))\n'
               '            mature = day - planted_day >= int(\n'
               '                CROPS.get(crop, {}).get("first_yield_day", 10**6)\n'
               '            )\n'
               '            if mature and int(tile.get("yield_units", 0) or 0) > 0:\n'
               '                tasks.append(self._task("HARVEST", position, ("HARVEST",)))\n'
               '            if terminal_day or bool(tile.get("watered_today", False)):\n'
               '                continue\n'
               '            kind = (\n'
               '                "CRITICAL_WATER"\n'
               '                if int(tile.get("consecutive_unwatered", 0) or 0)\n'
               '                >= int(self.config["critical_unwatered_threshold"])\n'
               '                else "WATER"\n'
               '            )\n'
               '            tasks.append(self._task(kind, position, ("WATER",)))\n'
               '\n'
               '        unfed: list[tuple[int, int]] = []\n'
               '        carriers = tuple(\n'
               '            worker_id\n'
               '            for worker_id, inventory in enumerate(inventories)\n'
               '            if int(inventory.get("WHEAT", 0) or 0) > 0\n'
               '        )\n'
               '        for position, tile in _animal_tiles(farm):\n'
               '            if int(tile.get("yield_units", 0) or 0) > 0:\n'
               '                tasks.append(self._task("HARVEST", position, ("HARVEST",)))\n'
               '            if terminal_day:\n'
               '                continue\n'
               '            if not bool(tile.get("fed_today", False)):\n'
               '                unfed.append(position)\n'
               '                kind = (\n'
               '                    "CRITICAL_FEED"\n'
               '                    if int(tile.get("consecutive_unfed", 0) or 0)\n'
               '                    >= int(self.config["critical_unfed_threshold"])\n'
               '                    else "FEED"\n'
               '                )\n'
               '                if carriers:\n'
               '                    tasks.append(\n'
               '                        self._task(\n'
               '                            kind,\n'
               '                            position,\n'
               '                            ("FEED",),\n'
               '                            allowed_workers=carriers,\n'
               '                            resource="WHEAT",\n'
               '                        )\n'
               '                    )\n'
               '            if bool(tile.get("fertilizer_available", False)):\n'
               '                tasks.append(\n'
               '                    self._task(\n'
               '                        "COLLECT_FERTILIZER",\n'
               '                        position,\n'
               '                        ("COLLECT_FERTILIZER",),\n'
               '                    )\n'
               '                )\n'
               '\n'
               '        if terminal_day:\n'
               '            return tasks\n'
               '\n'
               '        carried_wheat = sum(int(inv.get("WHEAT", 0) or 0) for inv in inventories)\n'
               '        shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)\n'
               '        desired = min(\n'
               '            len(unfed),\n'
               '            int(self.config["wheat_carrier_target"])\n'
               '            * int(self.config["wheat_pickup_batch"]),\n'
               '        )\n'
               '        shortage = max(0, desired - carried_wheat)\n'
               '        accesses = _shed_access(board_size)\n'
               '        pickup_count = min(\n'
               '            int(self.config["wheat_carrier_target"]),\n'
               '            (min(shortage, shed_wheat) + int(self.config["wheat_pickup_batch"]) - 1)\n'
               '            // int(self.config["wheat_pickup_batch"]),\n'
               '        )\n'
               '        remaining_wheat = shed_wheat\n'
               '        for index in range(pickup_count):\n'
               '            quantity = min(int(self.config["wheat_pickup_batch"]), remaining_wheat)\n'
               '            if quantity <= 0:\n'
               '                break\n'
               '            tasks.append(\n'
               '                self._task(\n'
               '                    "PICKUP_WHEAT",\n'
               '                    accesses[index % len(accesses)],\n'
               '                    ("PICKUP", "WHEAT", quantity),\n'
               '                    resource="WHEAT",\n'
               '                )\n'
               '            )\n'
               '            remaining_wheat -= quantity\n'
               '        return tasks\n'
               '\n'
               '    def _terminal_drop_tasks(\n'
               '        self,\n'
               '        *,\n'
               '        inventories: list[dict[str, Any]],\n'
               '        positions: list[tuple[int, int]],\n'
               '        board_size: int,\n'
               '        day: int,\n'
               '    ) -> list[CoreTask]:\n'
               '        if day < int(self.config["activation_day"]):\n'
               '            return []\n'
               '        sellable = set(self.config["sellable_products"])\n'
               '        if day < int(self.config["liquidation_day"]):\n'
               '            sellable.discard("WHEAT")\n'
               '        accesses = _shed_access(board_size)\n'
               '        tasks: list[CoreTask] = []\n'
               '        for worker_id, inventory in enumerate(inventories):\n'
               '            if (\n'
               '                day < int(self.config["liquidation_day"])\n'
               '                and int(inventory.get("WHEAT", 0) or 0) > 0\n'
               '            ):\n'
               '                continue\n'
               '            if not any(\n'
               '                item in sellable and int(quantity or 0) > 0\n'
               '                for item, quantity in inventory.items()\n'
               '            ):\n'
               '                continue\n'
               '            target = min(\n'
               '                accesses,\n'
               '                key=lambda value: (\n'
               '                    abs(positions[worker_id][0] - value[0])\n'
               '                    + abs(positions[worker_id][1] - value[1]),\n'
               '                    value,\n'
               '                ),\n'
               '            )\n'
               '            tasks.append(\n'
               '                self._task(\n'
               '                    "DROP_INVENTORY",\n'
               '                    target,\n'
               '                    ("DROP",),\n'
               '                    allowed_workers=(worker_id,),\n'
               '                )\n'
               '            )\n'
               '        return tasks\n'
               '\n'
               '    def _assign(\n'
               '        self,\n'
               '        tasks: list[CoreTask],\n'
               '        positions: list[tuple[int, int]],\n'
               '        private: dict[str, Any],\n'
               '    ) -> dict[int, CoreTask]:\n'
               '        if self._routing_clock is None or self._routing_clock.day < int(\n'
               '            self.config["liquidation_day"]\n'
               '        ):\n'
               '            assignments = super()._assign(tasks, positions, private)\n'
               '            for task in tasks:\n'
               '                if task.kind != "DROP_INVENTORY" or not task.allowed_workers:\n'
               '                    continue\n'
               '                worker_id = task.allowed_workers[0]\n'
               '                assignments[worker_id] = task\n'
               '            return assignments\n'
               '\n'
               '        assignments: dict[int, CoreTask] = {}\n'
               '        available_workers = set(range(len(positions)))\n'
               '        reserved_targets: set[tuple[Any, ...]] = set()\n'
               '        remaining_tasks = list(tasks)\n'
               '        remaining_actions = max(\n'
               '            0,\n'
               '            int(self.config["episode_steps"]) - 1 - self._routing_clock.step,\n'
               '        )\n'
               '        accesses = _shed_access(self._routing_board_size)\n'
               '        while available_workers and remaining_tasks:\n'
               '            candidates: list[tuple[int, int, int, int, int]] = []\n'
               '            for task_index, task in enumerate(remaining_tasks):\n'
               '                target_key = (\n'
               '                    (task.kind, task.target, task.allowed_workers)\n'
               '                    if task.kind == "DROP_INVENTORY"\n'
               '                    else (task.kind, task.target)\n'
               '                )\n'
               '                if target_key in reserved_targets:\n'
               '                    continue\n'
               '                eligible = available_workers\n'
               '                if task.allowed_workers is not None:\n'
               '                    eligible = available_workers.intersection(task.allowed_workers)\n'
               '                for worker_id in eligible:\n'
               '                    required = 1\n'
               '                    if task.kind == "HARVEST":\n'
               '                        return_distance = min(\n'
               '                            _distance(task.target, access) for access in accesses\n'
               '                        )\n'
               '                        required = (\n'
               '                            _distance(positions[worker_id], task.target)\n'
               '                            + return_distance\n'
               '                            + 2\n'
               '                        )\n'
               '                        if required > remaining_actions:\n'
               '                            continue\n'
               '                    value_score = 0\n'
               '                    if task.kind == "HARVEST":\n'
               '                        x, y = task.target\n'
               '                        tile = self._routing_farm["tiles"][y][x]\n'
               '                        item = str(tile.get("crop", ""))\n'
               '                        if tile.get("animal"):\n'
               '                            item = _ANIMAL_PRODUCTS[str(tile["animal"])]\n'
               '                        gross = float(self._routing_prices.get(item, 0.0) or 0.0) * int(\n'
               '                            tile.get("yield_units", 0) or 0\n'
               '                        )\n'
               '                        value_score = -int(1000 * gross / max(1, required))\n'
               '                    candidates.append(\n'
               '                        (\n'
               '                            task.priority,\n'
               '                            value_score,\n'
               '                            _distance(positions[worker_id], task.target)\n'
               '                            - (\n'
               '                                3\n'
               '                                if self.last_assignments.get(worker_id)\n'
               '                                == task.identity\n'
               '                                else 0\n'
               '                            ),\n'
               '                            worker_id,\n'
               '                            task_index,\n'
               '                        )\n'
               '                    )\n'
               '            if not candidates:\n'
               '                break\n'
               '            _priority, _value_score, _distance_score, worker_id, task_index = min(\n'
               '                candidates\n'
               '            )\n'
               '            task = remaining_tasks.pop(task_index)\n'
               '            assignments[worker_id] = task\n'
               '            available_workers.remove(worker_id)\n'
               '            reserved_targets.add(\n'
               '                (task.kind, task.target, task.allowed_workers)\n'
               '                if task.kind == "DROP_INVENTORY"\n'
               '                else (task.kind, task.target)\n'
               '            )\n'
               '        return assignments\n'
               '\n'
               '    def _predicted_drop(\n'
               '        self,\n'
               '        *,\n'
               '        action: dict[str, Any],\n'
               '        snapshot: Any,\n'
               '    ) -> Counter[str]:\n'
               '        positions = _positions(snapshot.farm)\n'
               '        inventories = _inventories(snapshot.private, len(positions))\n'
               '        unit_actions = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]\n'
               '        accesses = set(_shed_access(int(snapshot.configuration_snapshot["boardSize"])))\n'
               '        sellable = set(self.config["sellable_products"])\n'
               '        shed = Counter(snapshot.private.get("shed", {}) or {})\n'
               '        room = max(\n'
               '            0,\n'
               '            int(snapshot.configuration_snapshot["shedCapacity"])\n'
               '            - sum(int(value or 0) for value in shed.values()),\n'
               '        )\n'
               '        predicted: Counter[str] = Counter()\n'
               '        for worker_id, unit_action in enumerate(unit_actions):\n'
               '            if (\n'
               '                worker_id >= len(positions)\n'
               '                or not isinstance(unit_action, list)\n'
               '                or not unit_action\n'
               '                or unit_action[0] != "DROP"\n'
               '                or positions[worker_id] not in accesses\n'
               '            ):\n'
               '                continue\n'
               '            for item, quantity in inventories[worker_id].items():\n'
               '                amount = min(max(0, int(quantity or 0)), room)\n'
               '                if amount <= 0:\n'
               '                    continue\n'
               '                room -= amount\n'
               '                if item in sellable:\n'
               '                    predicted[item] += amount\n'
               '        return predicted\n'
               '\n'
               '    def _settle_market_pending(self, snapshot: Any) -> None:\n'
               '        post_shed = Counter(snapshot.private.get("shed", {}) or {})\n'
               '        for index in self._pending_market_ledger:\n'
               '            record = self.market_ledger_records[index]\n'
               '            requested = Counter(record["requested_sell_quantities"])\n'
               '            expected = Counter(record["expected_available_after_drop"])\n'
               '            observed_sold: dict[str, int] = {}\n'
               '            complete = True\n'
               '            any_observed = False\n'
               '            for item, quantity in requested.items():\n'
               '                target = min(int(quantity), int(expected[item]))\n'
               '                sold = max(0, int(expected[item]) - int(post_shed[item]))\n'
               '                observed_sold[item] = sold\n'
               '                any_observed = any_observed or sold > 0\n'
               '                complete = complete and sold >= target\n'
               '            outcome = "EXECUTED" if complete else "UNKNOWN" if any_observed else "NOT_EXECUTED"\n'
               '            record["outcome"] = outcome\n'
               '            record["observed_sold_units"] = observed_sold\n'
               '            record["post_state_id"] = snapshot.state_id\n'
               '            record["post_snapshot_fingerprint"] = snapshot.snapshot_fingerprint\n'
               '            self.market_execution_outcomes[outcome] += 1\n'
               '        self._pending_market_ledger = []\n'
               '\n'
               '    def _market_coordination_active(\n'
               '        self,\n'
               '        *,\n'
               '        snapshot: Any,\n'
               '        action: dict[str, Any],\n'
               '    ) -> bool:\n'
               '        del action\n'
               '        return snapshot.clock.day >= int(self.config["liquidation_day"])\n'
               '\n'
               '    def _desired_sale_quantities(\n'
               '        self,\n'
               '        *,\n'
               '        snapshot: Any,\n'
               '        provider_sell: Counter[str],\n'
               '        expected_available: Counter[str],\n'
               '    ) -> Counter[str]:\n'
               '        del snapshot\n'
               '        return Counter(\n'
               '            {\n'
               '                item: max(int(provider_sell[item]), int(expected_available[item]))\n'
               '                for item in self.config["sellable_products"]\n'
               '            }\n'
               '        )\n'
               '\n'
               '    def _coordinate_terminal_market(\n'
               '        self,\n'
               '        action: dict[str, Any],\n'
               '        *,\n'
               '        snapshot: Any,\n'
               '    ) -> dict[str, Any]:\n'
               '        if not self._market_coordination_active(snapshot=snapshot, action=action):\n'
               '            return action\n'
               '\n'
               '        original = deepcopy(action.get("market", []) or [])\n'
               '        sellable_order = list(self.config["sellable_products"])\n'
               '        sellable = set(sellable_order)\n'
               '        provider_sell: Counter[str] = Counter()\n'
               '        for order in original:\n'
               '            if (\n'
               '                isinstance(order, list)\n'
               '                and len(order) >= 3\n'
               '                and order[0] == "SELL"\n'
               '                and order[1] in sellable\n'
               '            ):\n'
               '                provider_sell[str(order[1])] += max(0, int(order[2]))\n'
               '\n'
               '        predicted_drop = self._predicted_drop(action=action, snapshot=snapshot)\n'
               '        shed = Counter(snapshot.private.get("shed", {}) or {})\n'
               '        expected_available = Counter(\n'
               '            {\n'
               '                item: int(shed[item]) + int(predicted_drop[item])\n'
               '                for item in sellable_order\n'
               '            }\n'
               '        )\n'
               '        desired = self._desired_sale_quantities(\n'
               '            snapshot=snapshot,\n'
               '            provider_sell=provider_sell,\n'
               '            expected_available=expected_available,\n'
               '        )\n'
               '\n'
               '        rebuilt: list[Any] = []\n'
               '        emitted_sell: set[str] = set()\n'
               '        for raw_order in original:\n'
               '            if not (\n'
               '                isinstance(raw_order, list)\n'
               '                and len(raw_order) >= 3\n'
               '                and raw_order[0] == "SELL"\n'
               '                and raw_order[1] in sellable\n'
               '            ):\n'
               '                rebuilt.append(deepcopy(raw_order))\n'
               '                continue\n'
               '            item = str(raw_order[1])\n'
               '            if item in emitted_sell or desired[item] <= 0:\n'
               '                continue\n'
               '            rebuilt.append(["SELL", item, int(desired[item]), *raw_order[3:]])\n'
               '            emitted_sell.add(item)\n'
               '\n'
               '        prices = snapshot.market.get("prices", {}) or {}\n'
               '        additions = sorted(\n'
               '            (\n'
               '                (float(prices.get(item, 0.0) or 0.0), item)\n'
               '                for item in sellable_order\n'
               '                if desired[item] > 0 and item not in emitted_sell\n'
               '            ),\n'
               '            reverse=True,\n'
               '        )\n'
               '        max_orders = int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"])\n'
               '        for _price, item in additions:\n'
               '            if len(rebuilt) >= max_orders:\n'
               '                break\n'
               '            rebuilt.append(["SELL", item, int(desired[item])])\n'
               '            emitted_sell.add(item)\n'
               '\n'
               '        non_sell_before = [\n'
               '            order\n'
               '            for order in original\n'
               '            if not (isinstance(order, list) and order and order[0] == "SELL")\n'
               '        ]\n'
               '        non_sell_after = [\n'
               '            order\n'
               '            for order in rebuilt\n'
               '            if not (isinstance(order, list) and order and order[0] == "SELL")\n'
               '        ]\n'
               '        if non_sell_after != non_sell_before:\n'
               '            self.non_sell_preservation_failures += 1\n'
               '\n'
               '        action["market"] = rebuilt\n'
               '        if rebuilt == original:\n'
               '            return action\n'
               '\n'
               '        emitted_quantities: Counter[str] = Counter()\n'
               '        for order in rebuilt:\n'
               '            if (\n'
               '                isinstance(order, list)\n'
               '                and len(order) >= 3\n'
               '                and order[0] == "SELL"\n'
               '                and order[1] in sellable\n'
               '            ):\n'
               '                emitted_quantities[str(order[1])] += max(0, int(order[2]))\n'
               '        incremental = Counter(\n'
               '            {\n'
               '                item: max(0, emitted_quantities[item] - provider_sell[item])\n'
               '                for item in sellable_order\n'
               '                if emitted_quantities[item] > provider_sell[item]\n'
               '            }\n'
               '        )\n'
               '        self.coordinated_market_batches += 1\n'
               '        self.coordinated_sell_orders += sum(1 for value in incremental.values() if value > 0)\n'
               '        self.coordinated_sell_units_requested += sum(incremental.values())\n'
               '        self.market_ledger_records.append(\n'
               '            {\n'
               '                "step": snapshot.clock.step,\n'
               '                "day": snapshot.clock.day,\n'
               '                "hour": snapshot.clock.hour,\n'
               '                "state_id": snapshot.state_id,\n'
               '                "snapshot_fingerprint": snapshot.snapshot_fingerprint,\n'
               '                "provider_market_sha256": stable_payload_hash(original),\n'
               '                "emitted_market_sha256": stable_payload_hash(rebuilt),\n'
               '                "provider_market": original,\n'
               '                "emitted_market": deepcopy(rebuilt),\n'
               '                "shed_before": dict(shed),\n'
               '                "predicted_drop": dict(predicted_drop),\n'
               '                "expected_available_after_drop": dict(expected_available),\n'
               '                "requested_sell_quantities": dict(emitted_quantities),\n'
               '                "incremental_sell_quantities": dict(incremental),\n'
               '                "outcome": "PENDING_NEXT_OBSERVATION",\n'
               '            }\n'
               '        )\n'
               '        self._pending_market_ledger.append(len(self.market_ledger_records) - 1)\n'
               '        return action\n'
               '\n'
               '    def __call__(\n'
               '        self, observation: dict[str, Any], configuration: Any = None\n'
               '    ) -> dict[str, Any]:\n'
               '        snapshot = CodexObservationAdapter.parse(\n'
               '            observation,\n'
               '            configuration,\n'
               '            fallback_turns_per_day=int(self.config["turns_per_day"]),\n'
               '            fallback_episode_steps=int(self.config["episode_steps"]),\n'
               '        )\n'
               '        self._routing_clock = snapshot.clock\n'
               '        self._routing_board_size = int(snapshot.configuration_snapshot["boardSize"])\n'
               '        self._routing_farm = snapshot.farm\n'
               '        self._routing_prices = snapshot.market.get("prices", {}) or {}\n'
               '        self._routing_private = snapshot.private\n'
               '        self._routing_shed_capacity = int(\n'
               '            snapshot.configuration_snapshot["shedCapacity"]\n'
               '        )\n'
               '        self._settle_market_pending(snapshot)\n'
               '        action = super().__call__(observation, configuration)\n'
               '        return self._coordinate_terminal_market(action, snapshot=snapshot)\n'
               '\n'
               '    def telemetry_snapshot(self) -> dict[str, Any]:\n'
               '        for index in self._pending_market_ledger:\n'
               '            self.market_ledger_records[index]["outcome"] = "UNKNOWN"\n'
               '            self.market_execution_outcomes["UNKNOWN"] += 1\n'
               '        self._pending_market_ledger = []\n'
               '        telemetry = super().telemetry_snapshot()\n'
               '        return {\n'
               '            **telemetry,\n'
               '            "agent_version": self.model_spec_version,\n'
               '            "coordinated_market_batches": self.coordinated_market_batches,\n'
               '            "coordinated_sell_orders": self.coordinated_sell_orders,\n'
               '            "coordinated_sell_units_requested": self.coordinated_sell_units_requested,\n'
               '            "non_sell_preservation_failures": self.non_sell_preservation_failures,\n'
               '            "market_execution_outcomes": dict(self.market_execution_outcomes),\n'
               '            "market_ledger_record_count": len(self.market_ledger_records),\n'
               '            "market_ledger_records": deepcopy(self.market_ledger_records),\n'
               '        }\n'
               '\n'
               '\n'
               'def create_codex_e17_reactive_service_routing_v3(\n'
               '    run_context: dict[str, Any] | None = None,\n'
               '    config_path: Path | str | None = None,\n'
               '):\n'
               '    """Create the fail-closed D28 service/routing/liquidation policy."""\n'
               '\n'
               '    instance = CodexE17ReactiveServiceRoutingV3(\n'
               '        run_context=run_context,\n'
               '        config_path=config_path,\n'
               '    )\n'
               '\n'
               '    def policy(\n'
               '        observation: dict[str, Any], configuration: Any = None\n'
               '    ) -> dict[str, Any]:\n'
               '        try:\n'
               '            action = instance(observation, configuration)\n'
               '            policy.codex_e17_service_routing_v3_last_error = None\n'
               '            return action\n'
               '        except (KeyboardInterrupt, SystemExit):\n'
               '            raise\n'
               '        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary\n'
               '            instance.error_count += 1\n'
               '            instance.fallback_count += 1\n'
               '            instance.last_exception = f"{type(exc).__name__}: {exc}"\n'
               '            policy.codex_e17_service_routing_v3_last_error = instance.last_exception\n'
               '            return deepcopy(_SAFE_PASS)\n'
               '\n'
               '    policy.codex_e17_service_routing_v3_instance = instance\n'
               '    policy.codex_e17_service_routing_v3_last_error = None\n'
               '    policy.__name__ = "codex_e17_2_service_routing_core_v3_d28_policy"\n'
               '    return policy\n'
               '\n'
               '\n'
               '__all__ = [\n'
               '    "DEFAULT_V3_CONFIG_PATH",\n'
               '    "V3_MODEL_SPEC_VERSION",\n'
               '    "CodexE17ReactiveServiceRoutingV3",\n'
               '    "create_codex_e17_reactive_service_routing_v3",\n'
               '    "load_v3_config",\n'
               ']\n',
 'routing_v4': '"""E17.2 inventory/deadline batching and optional quadrant affinity.\n'
               '\n'
               'The V4 keeps the complete V3 D28 service and terminal market behavior.  It\n'
               'changes only when a worker returns to the shed and, in the V4B ablation, how\n'
               "otherwise equivalent routes are biased toward the worker's current quadrant.\n"
               '"""\n'
               '\n'
               'from __future__ import annotations\n'
               '\n'
               'import json\n'
               'from collections import Counter\n'
               'from copy import deepcopy\n'
               'from pathlib import Path\n'
               'from typing import Any\n'
               '\n'
               'from _codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_core import (\n'
               '    CoreTask,\n'
               '    _animal_tiles,\n'
               '    _distance,\n'
               '    _inventories,\n'
               '    _shed_access,\n'
               ')\n'
               'from _codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (\n'
               '    _ANIMAL_PRODUCTS,\n'
               '    _SAFE_PASS,\n'
               '    CodexE17ReactiveServiceRoutingV3,\n'
               '    load_v3_config,\n'
               ')\n'
               '\n'
               'REPO_ROOT = Path(__file__).resolve().parents[4]\n'
               'DEFAULT_V4A_CONFIG_PATH = (\n'
               '    REPO_ROOT\n'
               '    / "experiments/e17/configs/codex/"\n'
               '    / "CODEX_E17_2_BATCHED_ROUTING_V4A_D28.json"\n'
               ')\n'
               'DEFAULT_V4B_CONFIG_PATH = (\n'
               '    REPO_ROOT\n'
               '    / "experiments/e17/configs/codex/"\n'
               '    / "CODEX_E17_2_CLUSTERED_ROUTING_V4B_D28.json"\n'
               ')\n'
               'DEFAULT_V4C_CONFIG_PATH = (\n'
               '    REPO_ROOT\n'
               '    / "experiments/e17/configs/codex/"\n'
               '    / "CODEX_E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_D28.json"\n'
               ')\n'
               'DEFAULT_V4D_CONFIG_PATH = (\n'
               '    REPO_ROOT\n'
               '    / "experiments/e17/configs/codex/"\n'
               '    / "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28.json"\n'
               ')\n'
               'V4A_MODEL_SPEC_VERSION = "CODEX-E17.2-BATCHED-ROUTING-V4A-D28"\n'
               'V4B_MODEL_SPEC_VERSION = "CODEX-E17.2-CLUSTERED-ROUTING-V4B-D28"\n'
               'V4C_MODEL_SPEC_VERSION = "CODEX-E17.2-CAPACITY-AWARE-BATCHED-ROUTING-V4C-D28"\n'
               'V4D_MODEL_SPEC_VERSION = "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28"\n'
               '_VARIANTS = {\n'
               '    "CODEX_E17_2_BATCHED_ROUTING_V4A_D28": V4A_MODEL_SPEC_VERSION,\n'
               '    "CODEX_E17_2_CLUSTERED_ROUTING_V4B_D28": V4B_MODEL_SPEC_VERSION,\n'
               '    "CODEX_E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_D28": (\n'
               '        V4C_MODEL_SPEC_VERSION\n'
               '    ),\n'
               '    "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28": (\n'
               '        V4D_MODEL_SPEC_VERSION\n'
               '    ),\n'
               '}\n'
               '\n'
               '\n'
               'def load_v4_config(path: Path | str | None = None) -> dict[str, Any]:\n'
               '    """Merge and validate a causally bounded V4 ablation config."""\n'
               '\n'
               '    config_path = Path(path) if path is not None else DEFAULT_V4A_CONFIG_PATH\n'
               '    overlay = json.loads(config_path.read_text(encoding="utf-8"))\n'
               '    candidate_id = str(overlay.get("candidate_id", ""))\n'
               '    if candidate_id not in _VARIANTS:\n'
               '        raise ValueError(f"unexpected candidate_id: {candidate_id!r}")\n'
               '    expected_version = _VARIANTS[candidate_id]\n'
               '    if overlay.get("model_spec_version") != expected_version:\n'
               '        raise ValueError("model_spec_version does not match candidate_id")\n'
               '    if int(overlay.get("activation_day", -1)) != 28:\n'
               '        raise ValueError("V4 must preserve the D28 handoff")\n'
               '    if int(overlay.get("liquidation_day", -1)) != 29:\n'
               '        raise ValueError("V4 must preserve the D29 liquidation window")\n'
               '    if overlay.get("defer_d28_drop_to_eod") is not True:\n'
               '        raise ValueError("V4 requires the preregistered D28 EOD batching")\n'
               '    if overlay.get("terminal_harvest_before_drop") is not True:\n'
               '        raise ValueError("V4 requires terminal harvest-before-drop routing")\n'
               '    if candidate_id.endswith("V4A_D28") and overlay.get(\n'
               '        "cluster_affinity_enabled"\n'
               '    ):\n'
               '        raise ValueError("V4A is the batching-only ablation")\n'
               '    if candidate_id.endswith("V4B_D28") and not overlay.get(\n'
               '        "cluster_affinity_enabled"\n'
               '    ):\n'
               '        raise ValueError("V4B requires quadrant affinity")\n'
               '    if candidate_id.endswith(("V4C_D28", "V4D_D28")):\n'
               '        if not overlay.get("capacity_aware_flush_enabled"):\n'
               '            raise ValueError("V4C requires capacity-aware flush")\n'
               '        trigger = float(overlay.get("capacity_flush_trigger_ratio", 0.0))\n'
               '        target = float(overlay.get("capacity_flush_target_ratio", 0.0))\n'
               '        if not 0 < target < trigger < 1:\n'
               '            raise ValueError("V4C requires 0 < target < trigger < 1")\n'
               '    if candidate_id.endswith("V4D_D28") and overlay.get(\n'
               '        "release_wheat_carriers_after_feed_complete"\n'
               '    ) is not True:\n'
               '        raise ValueError("V4D requires post-feed Wheat carrier release")\n'
               '    if int(overlay.get("cluster_switch_penalty", -1)) < 0:\n'
               '        raise ValueError("cluster_switch_penalty must be non-negative")\n'
               '\n'
               '    config = load_v3_config()\n'
               '    config.update(overlay)\n'
               '    return config\n'
               '\n'
               '\n'
               'def _cluster(position: tuple[int, int], board_size: int) -> str:\n'
               '    split = board_size // 2\n'
               '    x, y = position\n'
               '    row = "N" if y < split else "S"\n'
               '    col = "W" if x < split else "E"\n'
               '    return f"{row}{col}"\n'
               '\n'
               '\n'
               'class CodexE17BatchedClusterRoutingV4(CodexE17ReactiveServiceRoutingV3):\n'
               '    """Batch carried output until EOD/deadline and optionally stay local."""\n'
               '\n'
               '    def __init__(\n'
               '        self,\n'
               '        *,\n'
               '        run_context: dict[str, Any] | None = None,\n'
               '        config_path: Path | str | None = None,\n'
               '    ) -> None:\n'
               '        super().__init__(run_context=run_context)\n'
               '        self.config = load_v4_config(config_path)\n'
               '        self.candidate_id = str(self.config["candidate_id"])\n'
               '        self.model_spec_version = str(self.config["model_spec_version"])\n'
               '        self.deferred_drop_opportunities = 0\n'
               '        self.batched_harvest_services = 0\n'
               '        self.deadline_drop_assignments = 0\n'
               '        self.cluster_initial_assignments = 0\n'
               '        self.cluster_sticky_assignments = 0\n'
               '        self.cluster_switches = 0\n'
               '        self.max_carried_sellable_units = 0\n'
               '        self.capacity_flush_trigger_events = 0\n'
               '        self.capacity_flush_active_batches = 0\n'
               '        self.post_feed_wheat_carrier_releases = 0\n'
               '        self._worker_cluster: dict[int, str] = {}\n'
               '        self._affinity_day: int | None = None\n'
               '        self._capacity_flush_latched = False\n'
               '\n'
               '    def _sellable_units(self, inventory: dict[str, Any]) -> int:\n'
               '        sellable = set(self.config["sellable_products"])\n'
               '        return sum(\n'
               '            max(0, int(quantity or 0))\n'
               '            for item, quantity in inventory.items()\n'
               '            if item in sellable\n'
               '        )\n'
               '\n'
               '    def _terminal_drop_tasks(\n'
               '        self,\n'
               '        *,\n'
               '        inventories: list[dict[str, Any]],\n'
               '        positions: list[tuple[int, int]],\n'
               '        board_size: int,\n'
               '        day: int,\n'
               '    ) -> list[CoreTask]:\n'
               '        carried = [self._sellable_units(inventory) for inventory in inventories]\n'
               '        self.max_carried_sellable_units = max(\n'
               '            [self.max_carried_sellable_units, *carried]\n'
               '        )\n'
               '        if day < int(self.config["liquidation_day"]):\n'
               '            self.deferred_drop_opportunities += sum(value > 0 for value in carried)\n'
               '            if bool(self.config.get("capacity_aware_flush_enabled", False)):\n'
               '                feed_complete = not any(\n'
               '                    not bool(tile.get("fed_today", False))\n'
               '                    for _position, tile in _animal_tiles(self._routing_farm)\n'
               '                )\n'
               '                release_wheat = bool(\n'
               '                    self.config.get(\n'
               '                        "release_wheat_carriers_after_feed_complete", False\n'
               '                    )\n'
               '                    and feed_complete\n'
               '                )\n'
               '                droppable = [\n'
               '                    value\n'
               '                    if release_wheat\n'
               '                    or int(inventory.get("WHEAT", 0) or 0) == 0\n'
               '                    else 0\n'
               '                    for value, inventory in zip(carried, inventories, strict=True)\n'
               '                ]\n'
               '                pressure = sum(\n'
               '                    int(value or 0)\n'
               '                    for value in (self._routing_private.get("shed", {}) or {}).values()\n'
               '                ) + sum(droppable)\n'
               '                trigger = int(\n'
               '                    self._routing_shed_capacity\n'
               '                    * float(self.config["capacity_flush_trigger_ratio"])\n'
               '                )\n'
               '                if not self._capacity_flush_latched and pressure >= trigger:\n'
               '                    self._capacity_flush_latched = True\n'
               '                    self.capacity_flush_trigger_events += 1\n'
               '                if self._capacity_flush_latched and sum(droppable) > 0:\n'
               '                    accesses = _shed_access(board_size)\n'
               '                    tasks: list[CoreTask] = []\n'
               '                    for worker_id, quantity in enumerate(droppable):\n'
               '                        if quantity <= 0:\n'
               '                            continue\n'
               '                        if release_wheat and int(\n'
               '                            inventories[worker_id].get("WHEAT", 0) or 0\n'
               '                        ) > 0:\n'
               '                            self.post_feed_wheat_carrier_releases += 1\n'
               '                        target = min(\n'
               '                            accesses,\n'
               '                            key=lambda value: (\n'
               '                                _distance(positions[worker_id], value),\n'
               '                                value,\n'
               '                            ),\n'
               '                        )\n'
               '                        tasks.append(\n'
               '                            self._task(\n'
               '                                "DROP_INVENTORY",\n'
               '                                target,\n'
               '                                ("DROP",),\n'
               '                                allowed_workers=(worker_id,),\n'
               '                            )\n'
               '                        )\n'
               '                    return tasks\n'
               '                if sum(droppable) == 0:\n'
               '                    self._capacity_flush_latched = False\n'
               '            return []\n'
               '        return super()._terminal_drop_tasks(\n'
               '            inventories=inventories,\n'
               '            positions=positions,\n'
               '            board_size=board_size,\n'
               '            day=day,\n'
               '        )\n'
               '\n'
               '    def _market_coordination_active(\n'
               '        self,\n'
               '        *,\n'
               '        snapshot: Any,\n'
               '        action: dict[str, Any],\n'
               '    ) -> bool:\n'
               '        if super()._market_coordination_active(snapshot=snapshot, action=action):\n'
               '            return True\n'
               '        active = bool(\n'
               '            self.config.get("capacity_aware_flush_enabled", False)\n'
               '            and snapshot.clock.day == int(self.config["activation_day"])\n'
               '            and self._capacity_flush_latched\n'
               '        )\n'
               '        self.capacity_flush_active_batches += int(active)\n'
               '        return active\n'
               '\n'
               '    def _desired_sale_quantities(\n'
               '        self,\n'
               '        *,\n'
               '        snapshot: Any,\n'
               '        provider_sell: Counter[str],\n'
               '        expected_available: Counter[str],\n'
               '    ) -> Counter[str]:\n'
               '        if snapshot.clock.day >= int(self.config["liquidation_day"]):\n'
               '            return super()._desired_sale_quantities(\n'
               '                snapshot=snapshot,\n'
               '                provider_sell=provider_sell,\n'
               '                expected_available=expected_available,\n'
               '            )\n'
               '        sellable = set(self.config["sellable_products"])\n'
               '        shed = Counter(snapshot.private.get("shed", {}) or {})\n'
               '        fixed_units = sum(\n'
               '            int(quantity or 0)\n'
               '            for item, quantity in shed.items()\n'
               '            if item not in sellable\n'
               '        )\n'
               '        target_total = int(\n'
               '            self._routing_shed_capacity\n'
               '            * float(self.config["capacity_flush_target_ratio"])\n'
               '        )\n'
               '        sellable_target = max(0, target_total - fixed_units)\n'
               '        required = max(0, sum(expected_available.values()) - sellable_target)\n'
               '        desired = Counter({item: int(provider_sell[item]) for item in sellable})\n'
               '        provider_effective = sum(\n'
               '            min(int(provider_sell[item]), int(expected_available[item]))\n'
               '            for item in sellable\n'
               '        )\n'
               '        remaining = max(0, required - provider_effective)\n'
               '        prices = snapshot.market.get("prices", {}) or {}\n'
               '        for item in sorted(\n'
               '            sellable,\n'
               '            key=lambda value: (float(prices.get(value, 0.0) or 0.0), value),\n'
               '            reverse=True,\n'
               '        ):\n'
               '            already = min(int(desired[item]), int(expected_available[item]))\n'
               '            available = max(0, int(expected_available[item]) - already)\n'
               '            amount = min(available, remaining)\n'
               '            if amount > 0:\n'
               '                desired[item] = max(int(desired[item]), already + amount)\n'
               '                remaining -= amount\n'
               '            if remaining <= 0:\n'
               '                break\n'
               '        return desired\n'
               '\n'
               '    def _harvest_value_score(\n'
               '        self,\n'
               '        task: CoreTask,\n'
               '        required_actions: int,\n'
               '    ) -> int:\n'
               '        x, y = task.target\n'
               '        tile = self._routing_farm["tiles"][y][x]\n'
               '        item = str(tile.get("crop", ""))\n'
               '        if tile.get("animal"):\n'
               '            item = _ANIMAL_PRODUCTS[str(tile["animal"])]\n'
               '        gross = float(self._routing_prices.get(item, 0.0) or 0.0) * int(\n'
               '            tile.get("yield_units", 0) or 0\n'
               '        )\n'
               '        return -int(1000 * gross / max(1, required_actions))\n'
               '\n'
               '    def _record_cluster_assignment(\n'
               '        self,\n'
               '        worker_id: int,\n'
               '        task: CoreTask,\n'
               '        previous_identity: tuple[str, tuple[int, int], tuple[Any, ...]] | None,\n'
               '    ) -> None:\n'
               '        if task.kind in {"DROP_INVENTORY", "PICKUP_WHEAT"}:\n'
               '            return\n'
               '        if previous_identity == task.identity:\n'
               '            return\n'
               '        target_cluster = _cluster(task.target, self._routing_board_size)\n'
               '        prior = self._worker_cluster.get(worker_id)\n'
               '        if prior is None:\n'
               '            self.cluster_initial_assignments += 1\n'
               '        elif prior == target_cluster:\n'
               '            self.cluster_sticky_assignments += 1\n'
               '        else:\n'
               '            self.cluster_switches += 1\n'
               '        self._worker_cluster[worker_id] = target_cluster\n'
               '\n'
               '    def _assign(\n'
               '        self,\n'
               '        tasks: list[CoreTask],\n'
               '        positions: list[tuple[int, int]],\n'
               '        private: dict[str, Any],\n'
               '    ) -> dict[int, CoreTask]:\n'
               '        if self._routing_clock is None:\n'
               '            return super()._assign(tasks, positions, private)\n'
               '        day = int(self._routing_clock.day)\n'
               '        if self._affinity_day != day:\n'
               '            self._worker_cluster = {}\n'
               '            self._affinity_day = day\n'
               '\n'
               '        previous = dict(self.last_assignments)\n'
               '        if day < int(self.config["liquidation_day"]):\n'
               '            assignments = super()._assign(tasks, positions, private)\n'
               '            for worker_id, task in assignments.items():\n'
               '                self._record_cluster_assignment(\n'
               '                    worker_id, task, previous.get(worker_id)\n'
               '                )\n'
               '            return assignments\n'
               '\n'
               '        inventories = _inventories(private, len(positions))\n'
               '        accesses = _shed_access(self._routing_board_size)\n'
               '        remaining_actions = max(\n'
               '            0,\n'
               '            int(self.config["episode_steps"]) - 1 - self._routing_clock.step,\n'
               '        )\n'
               '        available_workers = set(range(len(positions)))\n'
               '        remaining_tasks = list(tasks)\n'
               '        reserved_targets: set[tuple[Any, ...]] = set()\n'
               '        assignments: dict[int, CoreTask] = {}\n'
               '        affinity_enabled = bool(self.config["cluster_affinity_enabled"])\n'
               '        switch_penalty = int(self.config["cluster_switch_penalty"])\n'
               '\n'
               '        while available_workers and remaining_tasks:\n'
               '            candidates: list[tuple[int, int, int, int, int]] = []\n'
               '            for task_index, task in enumerate(remaining_tasks):\n'
               '                target_key = (\n'
               '                    (task.kind, task.target, task.allowed_workers)\n'
               '                    if task.kind == "DROP_INVENTORY"\n'
               '                    else (task.kind, task.target)\n'
               '                )\n'
               '                if target_key in reserved_targets:\n'
               '                    continue\n'
               '                eligible = available_workers\n'
               '                if task.allowed_workers is not None:\n'
               '                    eligible = available_workers.intersection(task.allowed_workers)\n'
               '                for worker_id in eligible:\n'
               '                    distance = _distance(positions[worker_id], task.target)\n'
               '                    required = 1\n'
               '                    phase = 1 if task.kind == "DROP_INVENTORY" else 0\n'
               '                    value_score = 0\n'
               '                    if task.kind == "HARVEST":\n'
               '                        required = (\n'
               '                            distance\n'
               '                            + min(\n'
               '                                _distance(task.target, access)\n'
               '                                for access in accesses\n'
               '                            )\n'
               '                            + 2\n'
               '                        )\n'
               '                        if required > remaining_actions:\n'
               '                            continue\n'
               '                        value_score = self._harvest_value_score(task, required)\n'
               '                    target_cluster = _cluster(task.target, self._routing_board_size)\n'
               '                    cluster_cost = 0\n'
               '                    if (\n'
               '                        affinity_enabled\n'
               '                        and task.kind != "DROP_INVENTORY"\n'
               '                        and self._worker_cluster.get(worker_id) not in {\n'
               '                            None,\n'
               '                            target_cluster,\n'
               '                        }\n'
               '                    ):\n'
               '                        cluster_cost = switch_penalty\n'
               '                    continuity = (\n'
               '                        -3 if previous.get(worker_id) == task.identity else 0\n'
               '                    )\n'
               '                    candidates.append(\n'
               '                        (\n'
               '                            phase,\n'
               '                            value_score,\n'
               '                            distance + cluster_cost + continuity,\n'
               '                            worker_id,\n'
               '                            task_index,\n'
               '                        )\n'
               '                    )\n'
               '            if not candidates:\n'
               '                break\n'
               '            _phase, _value, _route, worker_id, task_index = min(candidates)\n'
               '            task = remaining_tasks.pop(task_index)\n'
               '            assignments[worker_id] = task\n'
               '            available_workers.remove(worker_id)\n'
               '            reserved_targets.add(\n'
               '                (task.kind, task.target, task.allowed_workers)\n'
               '                if task.kind == "DROP_INVENTORY"\n'
               '                else (task.kind, task.target)\n'
               '            )\n'
               '\n'
               '        for worker_id, task in assignments.items():\n'
               '            carried = self._sellable_units(inventories[worker_id])\n'
               '            if (\n'
               '                task.kind == "HARVEST"\n'
               '                and positions[worker_id] == task.target\n'
               '                and carried > 0\n'
               '            ):\n'
               '                self.batched_harvest_services += 1\n'
               '            if task.kind == "DROP_INVENTORY":\n'
               '                self.deadline_drop_assignments += 1\n'
               '            self._record_cluster_assignment(worker_id, task, previous.get(worker_id))\n'
               '        return assignments\n'
               '\n'
               '    def telemetry_snapshot(self) -> dict[str, Any]:\n'
               '        telemetry = super().telemetry_snapshot()\n'
               '        cluster_decisions = self.cluster_sticky_assignments + self.cluster_switches\n'
               '        return {\n'
               '            **telemetry,\n'
               '            "agent_version": self.model_spec_version,\n'
               '            "deferred_drop_opportunities": self.deferred_drop_opportunities,\n'
               '            "batched_harvest_services": self.batched_harvest_services,\n'
               '            "deadline_drop_assignments": self.deadline_drop_assignments,\n'
               '            "cluster_initial_assignments": self.cluster_initial_assignments,\n'
               '            "cluster_sticky_assignments": self.cluster_sticky_assignments,\n'
               '            "cluster_switches": self.cluster_switches,\n'
               '            "cluster_switch_rate": (\n'
               '                self.cluster_switches / cluster_decisions\n'
               '                if cluster_decisions\n'
               '                else 0.0\n'
               '            ),\n'
               '            "max_carried_sellable_units": self.max_carried_sellable_units,\n'
               '            "capacity_flush_trigger_events": self.capacity_flush_trigger_events,\n'
               '            "capacity_flush_active_batches": self.capacity_flush_active_batches,\n'
               '            "post_feed_wheat_carrier_releases": (\n'
               '                self.post_feed_wheat_carrier_releases\n'
               '            ),\n'
               '        }\n'
               '\n'
               '\n'
               'def create_codex_e17_batched_cluster_routing_v4(\n'
               '    run_context: dict[str, Any] | None = None,\n'
               '    config_path: Path | str | None = None,\n'
               '):\n'
               '    """Create a fail-closed V4A or V4B routing ablation."""\n'
               '\n'
               '    instance = CodexE17BatchedClusterRoutingV4(\n'
               '        run_context=run_context,\n'
               '        config_path=config_path,\n'
               '    )\n'
               '\n'
               '    def policy(\n'
               '        observation: dict[str, Any], configuration: Any = None\n'
               '    ) -> dict[str, Any]:\n'
               '        try:\n'
               '            action = instance(observation, configuration)\n'
               '            policy.codex_e17_batched_cluster_routing_last_error = None\n'
               '            return action\n'
               '        except (KeyboardInterrupt, SystemExit):\n'
               '            raise\n'
               '        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary\n'
               '            instance.error_count += 1\n'
               '            instance.fallback_count += 1\n'
               '            instance.last_exception = f"{type(exc).__name__}: {exc}"\n'
               '            policy.codex_e17_batched_cluster_routing_last_error = (\n'
               '                instance.last_exception\n'
               '            )\n'
               '            return deepcopy(_SAFE_PASS)\n'
               '\n'
               '    policy.codex_e17_batched_cluster_routing_instance = instance\n'
               '    policy.codex_e17_batched_cluster_routing_last_error = None\n'
               '    policy.__name__ = "codex_e17_2_batched_cluster_routing_v4_policy"\n'
               '    return policy\n'
               '\n'
               '\n'
               '__all__ = [\n'
               '    "DEFAULT_V4A_CONFIG_PATH",\n'
               '    "DEFAULT_V4B_CONFIG_PATH",\n'
               '    "DEFAULT_V4C_CONFIG_PATH",\n'
               '    "DEFAULT_V4D_CONFIG_PATH",\n'
               '    "V4A_MODEL_SPEC_VERSION",\n'
               '    "V4B_MODEL_SPEC_VERSION",\n'
               '    "V4C_MODEL_SPEC_VERSION",\n'
               '    "V4D_MODEL_SPEC_VERSION",\n'
               '    "CodexE17BatchedClusterRoutingV4",\n'
               '    "create_codex_e17_batched_cluster_routing_v4",\n'
               '    "load_v4_config",\n'
               ']\n'}
_CONFIGS = {'v9': {'candidate_id': 'CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY',
        'schema_version': 'model_spec_c2.codex.v9_3q_mixed.v1',
        'model_spec_version': 'CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY',
        'foundation_checkpoint': 'f391ee2',
        'quadrants_owned': 3,
        'workforce_total': 13,
        'q0_workforce_total': 7,
        'dual_workforce_total': 13,
        'crop_working_set_target': 56,
        'crop_counts': {'MELON': 17, 'STRAWBERRY': 27, 'WHEAT': 12},
        'pasture_allocation_target': 17,
        'livestock_targets': {'COW': 6, 'SHEEP': 11},
        'bootstrap_livestock': {'COW': 2, 'SHEEP': 2},
        'q1_livestock_targets': {'COW': 3, 'SHEEP': 3},
        'q2_livestock_targets': {'COW': 0, 'SHEEP': 5},
        'livestock_activation_days': {'COW': 7, 'SHEEP': 8},
        'q1_activation_min_day': 6,
        'q1_activation_max_day': 10,
        'q1_activation_cash': 1800,
        'q1_operating_cash_floor': 250,
        'q2_activation_min_day': 11,
        'q2_activation_max_day': 14,
        'q2_activation_cash_plus_inventory': 6500,
        'q2_operating_cash_floor': 500,
        'q2_land_cost': 2000,
        'q2_min_remaining_days': 15,
        'operating_cash_floor': 50,
        'feed_reserve_rounds': 2,
        'observed_capacity_days': 3,
        'hard_schedule_days': 2,
        'minimum_post_plant_action_phases': 1,
        'payback_cutoff_days': 2,
        'crop_horizon_margin_days': 0,
        'endgame_shutdown_days': 0,
        'max_noop_before_invalidation': 3,
        'turns_per_day': 24,
        'q1_cadence_relief': {'worker_role': 'FERTILIZER_LOGISTICS_Q1',
                              'eligible_tasks': ['ANIMAL_COLLECTION', 'CARE'],
                              'feed_ownership_unchanged': True,
                              'q0_ownership_unchanged': True}},
 'guarded': {'candidate_id': 'CODEX_E17_1_3Q_REACTIVE_GUARDED_V1',
             'schema_version': 'e17.codex.reactive_guarded.v1',
             'model_spec_version': 'CODEX-E17.1-3Q-REACTIVE-GUARDED-V1',
             'base_policy': 'CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY',
             'causal_family': 'WHEAT_FEED_SERVICEABILITY',
             'turns_per_day': 24,
             'episode_steps': 720,
             'feed_reserve_rounds': 1,
             'critical_unfed_threshold': 1,
             'max_extra_wheat_per_step': 6,
             'operating_cash_floor': 100,
             'market_fill_tracking': True,
             'allow_market_buy_append': True,
             'allow_wheat_sale_reduction': True,
             'allow_critical_feed_override': True,
             'allow_animal_purchase_deferral': True},
 'true_reactive': {'candidate_id': 'CODEX_E17_1_TRUE_REACTIVE_V2',
                   'schema_version': 'e17.codex.true_reactive.v2',
                   'model_spec_version': 'CODEX-E17.1-TRUE-REACTIVE-V2',
                   'base_policy': 'CODEX-E17.1-3Q-REACTIVE-GUARDED-V1',
                   'causal_family': 'MARKET_REGIME_ADAPTATION',
                   'turns_per_day': 24,
                   'episode_steps': 720,
                   'reference_prices': {'WHEAT': 25,
                                        'CARROT': 35,
                                        'TOMATO': 60,
                                        'STRAWBERRY': 120,
                                        'MELON': 250,
                                        'EGG': 50,
                                        'MILK': 160,
                                        'WOOL': 200,
                                        'FERTILIZER': 100},
                   'sellable_products': ['CARROT',
                                         'TOMATO',
                                         'STRAWBERRY',
                                         'MELON',
                                         'EGG',
                                         'MILK',
                                         'WOOL',
                                         'FERTILIZER'],
                   'animal_costs': {'GOOSE': 300, 'COW': 400, 'SHEEP': 500},
                   'low_output_price_ratio': 0.9,
                   'high_output_price_ratio': 1.1,
                   'wheat_scarcity_price_ratio': 1.25,
                   'price_recovery_ratio': 1.0,
                   'shed_pressure_ratio': 0.8,
                   'emergency_cash_floor': 500,
                   'feed_reserve_per_animal': 1,
                   'max_deferral_steps': 6,
                   'max_opportunistic_sale_units': 12,
                   'allow_low_price_sale_deferral': True,
                   'allow_high_price_opportunistic_sale': True,
                   'allow_wheat_reserve_protection': False,
                   'allow_scarcity_animal_deferral': False},
 'routing_core': {'candidate_id': 'CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2',
                  'schema_version': 'e17.codex.reactive_service_routing_core.v2',
                  'model_spec_version': 'CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2',
                  'base_policy': 'CODEX-E17.1-TRUE-REACTIVE-V2',
                  'causal_family': 'REACTIVE_SERVICE_AND_ROUTING_CORE',
                  'turns_per_day': 24,
                  'episode_steps': 720,
                  'critical_unfed_threshold': 1,
                  'critical_unwatered_threshold': 1,
                  'activation_day': 29,
                  'wheat_pickup_batch': 6,
                  'wheat_carrier_target': 4,
                  'plant_cutoff_day': 25,
                  'crop_cutoffs': {'MELON': 17, 'STRAWBERRY': 20, 'TOMATO': 22, 'CARROT': 25, 'WHEAT': 25},
                  'pasture_targets': [[3, 2],
                                      [4, 2],
                                      [3, 3],
                                      [4, 3],
                                      [2, 4],
                                      [3, 4],
                                      [4, 4],
                                      [5, 2],
                                      [6, 2],
                                      [5, 3],
                                      [6, 3],
                                      [5, 4],
                                      [6, 4],
                                      [7, 4],
                                      [3, 5],
                                      [4, 5],
                                      [3, 6],
                                      [4, 6],
                                      [4, 7]],
                  'coop_targets': [[4, 1]],
                  'wheat_crop_targets': [[0, 0],
                                         [1, 0],
                                         [2, 0],
                                         [3, 0],
                                         [5, 0],
                                         [6, 0],
                                         [7, 0],
                                         [0, 5],
                                         [1, 5],
                                         [2, 5]],
                  'task_priority': {'CRITICAL_WATER': 1,
                                    'CRITICAL_FEED': 0,
                                    'DROP_INVENTORY': 0,
                                    'PLACE_ANIMAL': 1,
                                    'PICKUP_WHEAT': 0,
                                    'PICKUP_ANIMAL': 2,
                                    'BUILD_STRUCTURE': 2,
                                    'DIG_TARGET': 4,
                                    'HARVEST': 2,
                                    'WATER': 3,
                                    'PLANT': 4,
                                    'CARE': 5}},
 'routing_v3': {'candidate_id': 'CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28',
                'schema_version': 'e17.codex.reactive_service_routing_core.v3.d28',
                'model_spec_version': 'CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28',
                'base_policy': 'CODEX-E17.1-TRUE-REACTIVE-V2',
                'causal_family': 'REACTIVE_SERVICE_ROUTING_AND_TERMINAL_LIQUIDATION',
                'turns_per_day': 24,
                'episode_steps': 720,
                'activation_day': 28,
                'liquidation_day': 29,
                'critical_unfed_threshold': 1,
                'critical_unwatered_threshold': 1,
                'wheat_pickup_batch': 6,
                'wheat_carrier_target': 4,
                'plant_cutoff_day': 27,
                'sellable_products': ['WHEAT',
                                      'CARROT',
                                      'TOMATO',
                                      'STRAWBERRY',
                                      'MELON',
                                      'EGG',
                                      'MILK',
                                      'WOOL',
                                      'FERTILIZER'],
                'crop_cutoffs': {'MELON': 17, 'STRAWBERRY': 20, 'TOMATO': 22, 'CARROT': 25, 'WHEAT': 25},
                'pasture_targets': [],
                'coop_targets': [],
                'wheat_crop_targets': [],
                'task_priority': {'CRITICAL_FEED': 0,
                                  'PICKUP_WHEAT': 0,
                                  'DROP_INVENTORY': 0,
                                  'FEED': 1,
                                  'CRITICAL_WATER': 1,
                                  'HARVEST': 2,
                                  'WATER': 3,
                                  'COLLECT_FERTILIZER': 4,
                                  'PLACE_ANIMAL': 9,
                                  'PICKUP_ANIMAL': 9,
                                  'BUILD_STRUCTURE': 9,
                                  'DIG_TARGET': 9,
                                  'PLANT': 9,
                                  'CARE': 9}},
 'routing_v4': {'candidate_id': 'CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28',
                'schema_version': 'e17.codex.post_feed_capacity_batched_routing.v4d.d28',
                'model_spec_version': 'CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28',
                'base_policy': 'CODEX-E17.2-CAPACITY-AWARE-BATCHED-ROUTING-V4C-D28',
                'causal_family': 'POST_FEED_WHEAT_CARRIER_CAPACITY_RELEASE',
                'turns_per_day': 24,
                'episode_steps': 720,
                'activation_day': 28,
                'liquidation_day': 29,
                'critical_unfed_threshold': 1,
                'critical_unwatered_threshold': 1,
                'wheat_pickup_batch': 6,
                'wheat_carrier_target': 4,
                'plant_cutoff_day': 27,
                'sellable_products': ['WHEAT',
                                      'CARROT',
                                      'TOMATO',
                                      'STRAWBERRY',
                                      'MELON',
                                      'EGG',
                                      'MILK',
                                      'WOOL',
                                      'FERTILIZER'],
                'crop_cutoffs': {'MELON': 17, 'STRAWBERRY': 20, 'TOMATO': 22, 'CARROT': 25, 'WHEAT': 25},
                'pasture_targets': [],
                'coop_targets': [],
                'wheat_crop_targets': [],
                'task_priority': {'CRITICAL_FEED': 0,
                                  'PICKUP_WHEAT': 0,
                                  'DROP_INVENTORY': 0,
                                  'FEED': 1,
                                  'CRITICAL_WATER': 1,
                                  'HARVEST': 2,
                                  'WATER': 3,
                                  'COLLECT_FERTILIZER': 4,
                                  'PLACE_ANIMAL': 9,
                                  'PICKUP_ANIMAL': 9,
                                  'BUILD_STRUCTURE': 9,
                                  'DIG_TARGET': 9,
                                  'PLANT': 9,
                                  'CARE': 9},
                'defer_d28_drop_to_eod': True,
                'terminal_harvest_before_drop': True,
                'cluster_affinity_enabled': False,
                'cluster_switch_penalty': 0,
                'capacity_aware_flush_enabled': True,
                'capacity_flush_trigger_ratio': 0.85,
                'capacity_flush_target_ratio': 0.5,
                'release_wheat_carriers_after_feed_complete': True}}
_ROUTINE_ACTIONS = ({'farmer': ['PASS'], 'hands': [], 'market': []},
 {'farmer': ['NORTH'],
  'hands': [],
  'market': [['BUY_PRODUCT', 'WHEAT', 5],
             ['BUY_SEED', 'WHEAT', 7],
             ['BUY_SEED', 'MELON', 12],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['BUY_ANIMAL', 'COW', 2],
             ['BUY_ANIMAL', 'SHEEP', 2]]},
 {'farmer': ['WEST'],
  'hands': [['PICKUP', 'COW', 1], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'COW', 1]],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['NORTH'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['NORTH'], ['BUILD_PASTURE']],
  'market': []},
 {'farmer': ['PLANT', 'MELON'],
  'hands': [['BUILD_PASTURE'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['PLACE', 'COW', 1]],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['PLACE', 'COW', 1], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['CARE']],
  'market': [['SELL', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['CARE'], ['BUILD_PASTURE'], ['PLANT', 'MELON'], ['WEST'], ['WEST']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['PLANT', 'MELON'],
  'hands': [['WEST'], ['PLACE', 'SHEEP', 1], ['WATER'], ['NORTH'], ['WEST']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['NORTH'], ['CARE'], ['WEST'], ['BUILD_PASTURE'], ['WEST']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['PLANT', 'MELON'], ['FEED'], ['WEST'], ['PLACE', 'SHEEP', 1], ['PLANT', 'MELON']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['WATER'], ['NORTH'], ['WEST'], ['FEED'], ['WATER']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['WEST']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'MELON']],
  'market': []},
 {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'MELON'], ['WATER'], ['NORTH'], ['WATER']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []},
 {'farmer': ['PASS'],
  'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']],
  'market': []},
 {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'MELON'], ['WATER'], ['WATER'], ['WATER']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['WEST'], ['PASS']], 'market': []},
 {'farmer': ['PASS'],
  'hands': [['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PASS']],
  'market': []},
 {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'MELON'], ['WATER'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['NORTH']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['NORTH']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['BUILD_PASTURE']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['PASS'], ['BUILD_PASTURE'], ['PASS'], ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['PASS'], ['WEST']], 'market': []},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 1], ['WEST'], ['PASS'], ['NORTH']],
  'market': [['SELL', 'WHEAT', 2]]},
 {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['WEST']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['PASS'], ['WATER']], 'market': []},
 {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['WEST']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['EAST'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 2],
  'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 6]]},
 {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 4],
  'hands': [],
  'market': [['BUY_SEED', 'WHEAT', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WEST']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PASS'], ['WEST'], ['NORTH'], ['NORTH']],
  'market': [['SELL', 'WHEAT', 1]]},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['PASS'], ['WEST'], ['NORTH'], ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['EAST'], ['NORTH'], ['WEST']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': []},
 {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['WEST']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WEST']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['WATER']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []},
 {'farmer': ['SOUTH'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': []},
 {'farmer': ['EAST'], 'hands': [['PASS'], ['WEST'], ['EAST'], ['HARVEST']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 3],
  'hands': [['PASS'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1]]},
 {'farmer': ['PICKUP', 'COW', 1], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': []},
 {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['EAST']], 'market': []},
 {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []},
 {'farmer': ['PLACE', 'COW', 1], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 3],
  'hands': [],
  'market': [['SELL', 'WHEAT', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 1]]},
 {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []},
 {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []},
 {'farmer': ['CARE'],
  'hands': [['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']],
  'market': []},
 {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PASS'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER']],
  'market': []},
 {'farmer': ['SOUTH'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []},
 {'farmer': ['SOUTH'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['NORTH'], ['WATER']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 3],
  'hands': [['PASS'], ['EAST'], ['PASS'], ['WATER'], ['WEST']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['NORTH'], 'hands': [['PASS'], ['SOUTH'], ['PICKUP', 'COW', 1], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['DROP'], ['WEST'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PLACE', 'COW'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 5], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WEST']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WEST']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WEST']], 'market': []},
 {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PASS'], ['NORTH'], ['EAST'], ['NORTH']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PASS'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['PASS'], ['WATER'], ['CARE'], ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['EAST'], ['SOUTH'], ['WATER']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PASS'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['PLANT', 'WHEAT']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['WEST'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []},
 {'farmer': ['EAST'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'], 'hands': [['PASS'], ['DROP'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 5],
  'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']],
  'market': [['SELL', 'FERTILIZER', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 5], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['WEST'],
  'hands': [['WEST'], ['WEST'], ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE']]},
 {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['WEST'], ['WEST'], ['WEST'], ['PASS']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['PASS']], 'market': [['SELL', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': []},
 {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': []},
 {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['PASS']], 'market': []},
 {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['CARE'], ['NORTH'], ['WEST'], ['EAST'], ['PASS']],
  'market': [['BUY_SEED', 'STRAWBERRY', 2]]},
 {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['PASS']], 'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['FEED'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['PASS']], 'market': []},
 {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['PASS']],
  'market': [['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['PASS']], 'market': []},
 {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': []},
 {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['EAST'], 'hands': [['EAST'], ['PASS'], ['WATER'], ['NORTH'], ['PASS']], 'market': []},
 {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['WATER'],
  'hands': [['PLACE', 'FERTILIZER', 4], ['PASS'], ['PASS'], ['WEST'], ['PASS']],
  'market': [['SELL', 'FERTILIZER', 4]]},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []},
 {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []},
 {'farmer': ['WEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['NORTH'],
  'hands': [['PICKUP', 'WHEAT', 1], ['WEST'], ['PASS'], ['WEST'], ['PICKUP', 'WHEAT', 5], ['PASS'], ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['HIRE']]},
 {'farmer': ['HARVEST'],
  'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['PASS'], ['WEST']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['FEED'], ['WEST'], ['PASS'], ['WEST'], ['FEED'], ['WEST'], ['PASS'], ['WEST']],
  'market': []},
 {'farmer': ['HARVEST'],
  'hands': [['CARE'], ['WEST'], ['PASS'], ['WEST'], ['CARE'], ['NORTH'], ['PASS'], ['WEST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PASS'],
            ['NORTH']],
  'market': []},
 {'farmer': ['PLACE', 'WOOL', 10],
  'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['PASS'], ['WATER'], ['WEST'], ['WATER'], ['PASS'], ['NORTH']],
  'market': [['SELL', 'WOOL', 10],
             ['SELL', 'FERTILIZER', 1],
             ['BUY_PRODUCT', 'WHEAT', 2],
             ['BUY_LAND'],
             ['BUY_ANIMAL', 'COW', 2],
             ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['EAST'], ['EAST'], ['EAST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['PICKUP', 'COW', 1],
  'hands': [['FEED'], ['EAST'], ['NORTH'], ['EAST'], ['CARE'], ['EAST'], ['EAST'], ['EAST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 1],
  'hands': [['CARE'], ['EAST'], ['PICKUP', 'COW', 1], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['EAST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['COLLECT_FERTILIZER'],
            ['EAST'],
            ['PICKUP', 'WHEAT', 1],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 2]]},
 {'farmer': ['BUILD_PASTURE'],
  'hands': [['NORTH'],
            ['BUILD_PASTURE'],
            ['BUILD_PASTURE'],
            ['EAST'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['NORTH']],
  'market': []},
 {'farmer': ['PLACE', 'COW'],
  'hands': [['FEED'],
            ['NORTH'],
            ['PLACE', 'COW'],
            ['BUILD_PASTURE'],
            ['PLACE', 'FERTILIZER', 1],
            ['WATER'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['PLANT', 'STRAWBERRY'],
            ['FEED'],
            ['EAST'],
            ['PLACE', 'FERTILIZER', 1],
            ['WEST'],
            ['BUILD_PASTURE'],
            ['PLANT', 'STRAWBERRY']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['BUILD_PASTURE'], ['WEST'], ['WATER'], ['EAST'], ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'], ['WEST'], ['EAST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['PLANT', 'STRAWBERRY'],
            ['WEST'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['FEED'], ['WEST'], ['BUILD_PASTURE'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['CARE'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WEST'],
            ['PLANT', 'STRAWBERRY'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER'],
            ['WATER'],
            ['PLANT', 'STRAWBERRY'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['EAST'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['SOUTH'], ['WEST'], ['EAST'], ['PASS'], ['WATER'], ['WEST'], ['EAST'], ['EAST']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['PLACE', 'FERTILIZER', 3],
            ['WATER'],
            ['PLANT', 'STRAWBERRY'],
            ['PASS'],
            ['NORTH'],
            ['WATER'],
            ['PLANT', 'STRAWBERRY'],
            ['PLANT', 'WHEAT']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['WATER'],
  'hands': [['PASS'], ['HARVEST'], ['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']],
  'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 1],
  'hands': [],
  'market': [['SELL', 'WOOL', 2],
             ['SELL', 'FERTILIZER', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['WEST'],
  'hands': [['WEST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['WEST'], ['NORTH']],
  'market': [['SELL', 'WHEAT', 9], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1]]},
 {'farmer': ['WEST'],
  'hands': [['PICKUP', 'WHEAT', 1],
            ['PICKUP', 'WHEAT', 1],
            ['PICKUP', 'WHEAT', 1],
            ['WEST'],
            ['PICKUP', 'WHEAT', 1],
            ['PICKUP', 'WHEAT', 1],
            ['WEST'],
            ['WEST']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['NORTH'], ['FEED'], ['WEST'], ['WEST']],
  'market': []},
 {'farmer': ['CARE'],
  'hands': [['FEED'], ['NORTH'], ['CARE'], ['FEED'], ['FEED'], ['CARE'], ['NORTH'], ['WEST']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['CARE'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['CARE'],
            ['PLACE', 'FERTILIZER', 1],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'FERTILIZER', 1],
            ['NORTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'COW', 1],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['PLACE', 'FERTILIZER', 1],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['PLACE', 'FERTILIZER', 1],
            ['EAST'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['SOUTH'],
            ['PLACE', 'COW'],
            ['PLACE', 'FERTILIZER', 1],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']],
  'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'], ['PASS'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'], ['PASS'], ['PICKUP', 'COW', 1], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['NORTH'], ['PASS'], ['NORTH'], ['EAST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WATER'], ['PASS'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']],
  'market': [['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'], ['PASS'], ['PLACE', 'COW'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['PASS'],
            ['CARE'],
            ['NORTH'],
            ['WATER'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['EAST'], ['WATER']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['EAST'], ['PASS'], ['PASS'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['PASS']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['WATER'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['NORTH'], ['PASS'], ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['CARE'], ['WATER'], ['PASS'], ['PASS']],
  'market': []},
 {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['HARVEST'],
  'hands': [['PICKUP', 'WHEAT', 5], ['PICKUP', 'WHEAT', 4], ['EAST'], ['EAST'], ['EAST']],
  'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['SOUTH'],
  'hands': [['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['EAST']],
  'market': []},
 {'farmer': ['PLACE', 'MILK', 6],
  'hands': [['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['PLACE', 'MILK', 6], ['EAST'], ['NORTH']],
  'market': [['SELL', 'MILK', 12],
             ['BUY_PRODUCT', 'WHEAT', 3],
             ['HIRE'],
             ['BUY_ANIMAL', 'COW', 1],
             ['BUY_ANIMAL', 'SHEEP', 2]]},
 {'farmer': ['PICKUP', 'WHEAT', 4],
  'hands': [['WEST'],
            ['PICKUP', 'COW', 1],
            ['SOUTH'],
            ['WEST'],
            ['PASS'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['EAST'],
            ['PICKUP', 'SHEEP', 2],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['CARE'], ['NORTH'], ['EAST'], ['NORTH'], ['PASS'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'],
            ['PLACE', 'COW'],
            ['EAST'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH']],
  'market': [['BUY_SEED', 'STRAWBERRY', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['NORTH'],
            ['CARE'],
            ['PLACE', 'SHEEP'],
            ['WATER'],
            ['PASS'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'], ['EAST'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['EAST'],
            ['WEST'],
            ['PLANT', 'STRAWBERRY'],
            ['SOUTH'],
            ['WATER'],
            ['WATER'],
            ['HARVEST'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['PICKUP', 'WHEAT', 1],
            ['WEST'],
            ['EAST'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER'],
            ['NORTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['WATER'],
            ['PLACE', 'SHEEP'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['PASS']],
  'market': [['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'], ['EAST'], ['CARE'], ['WATER'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['PASS']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['FEED'],
            ['NORTH'],
            ['PASS'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['PLANT', 'STRAWBERRY'],
            ['WEST'],
            ['PASS']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['CARE'],
            ['WATER'],
            ['PASS'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 1],
            ['WATER'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['PASS']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PASS'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['PASS']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['WEST'], ['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PASS']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PLACE', 'FERTILIZER', 3],
            ['NORTH'],
            ['PASS'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['HARVEST'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 3]]},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['WATER'],
            ['PASS'],
            ['WATER'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'WHEAT', 2]]},
 {'farmer': ['PLACE', 'FERTILIZER', 4],
  'hands': [['COLLECT_FERTILIZER'],
            ['WEST'],
            ['PASS'],
            ['SOUTH'],
            ['PASS'],
            ['CARE'],
            ['SOUTH'],
            ['WATER'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 4]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS']],
  'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 3],
  'hands': [],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['WEST'],
  'hands': [['PICKUP', 'WHEAT', 5],
            ['EAST'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 4],
            ['PICKUP', 'WHEAT', 1],
            ['WEST'],
            ['EAST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['HARVEST'],
  'hands': [['FEED'],
            ['EAST'],
            ['NORTH'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 1],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['EAST'],
  'hands': [['CARE'],
            ['EAST'],
            ['NORTH'],
            ['CARE'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['COLLECT_FERTILIZER'],
            ['EAST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['WEST']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['EAST'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['NORTH']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['NORTH'],
            ['WATER'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['NORTH'],
            ['PLACE', 'WOOL', 4],
            ['NORTH'],
            ['WATER'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['CARE'],
            ['NORTH'],
            ['EAST'],
            ['CARE'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['NORTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['WATER'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['WATER'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['NORTH'],
            ['EAST'],
            ['NORTH'],
            ['CARE'],
            ['EAST'],
            ['NORTH'],
            ['PASS'],
            ['WATER'],
            ['WEST'],
            ['WATER']],
  'market': [['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['WATER'],
            ['WATER'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['PASS'],
            ['HARVEST'],
            ['WATER'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['CARE'],
            ['HARVEST'],
            ['EAST'],
            ['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['HARVEST'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['COLLECT_FERTILIZER'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['WATER'],
            ['WATER'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['PASS'],
            ['NORTH'],
            ['EAST'],
            ['WATER']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['FEED'],
            ['WEST'],
            ['WATER'],
            ['FEED'],
            ['WATER'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['WATER'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['WATER'],
            ['EAST'],
            ['CARE'],
            ['WEST'],
            ['WEST'],
            ['PASS'],
            ['PASS'],
            ['HARVEST'],
            ['EAST'],
            ['WATER']],
  'market': []},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'],
            ['PASS'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['NORTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['WEST'],
            ['PASS'],
            ['PASS'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['EAST'],
            ['WATER']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['SOUTH'],
            ['PASS'],
            ['PASS'],
            ['SOUTH'],
            ['SOUTH'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['EAST'],
            ['WATER'],
            ['EAST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['SOUTH'],
            ['PASS'],
            ['PASS'],
            ['PLACE', 'FERTILIZER', 4],
            ['DROP'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['EAST'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 4]]},
 {'farmer': ['PLACE', 'FERTILIZER', 2],
  'hands': [['PLACE', 'FERTILIZER', 4],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['SOUTH'],
            ['WATER'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 6]]},
 {'farmer': ['DROP'],
  'hands': [['DROP'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 2]]},
 {'farmer': ['PASS'],
  'hands': [['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['WEST'],
  'hands': [['WEST'], ['PICKUP', 'WHEAT', 5], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['WEST']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 8], ['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 5],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 5],
            ['NORTH']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['FEED'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['FEED'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['HARVEST'],
  'hands': [['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['HARVEST'],
            ['CARE'],
            ['NORTH']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['HARVEST'],
            ['WATER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['WATER'],
            ['HARVEST'],
            ['WATER'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['HARVEST'],
            ['HARVEST'],
            ['NORTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['EAST'],
            ['HARVEST'],
            ['EAST'],
            ['NORTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['FEED'],
            ['SOUTH'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['FEED'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['CARE'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['PLACE', 'MELON', 6],
            ['CARE'],
            ['EAST']],
  'market': [['SELL', 'MELON', 6]]},
 {'farmer': ['PLACE', 'MELON', 6],
  'hands': [['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['SOUTH'],
            ['PLACE', 'MELON', 6],
            ['SOUTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH']],
  'market': [['SELL', 'MELON', 12], ['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['WEST'],
  'hands': [['PLACE', 'MELON', 6],
            ['PLACE', 'MELON', 6],
            ['SOUTH'],
            ['NORTH'],
            ['PLACE', 'MELON', 6],
            ['SOUTH'],
            ['NORTH'],
            ['PLACE', 'MELON', 6],
            ['CARE'],
            ['EAST'],
            ['SOUTH']],
  'market': [['SELL', 'MELON', 24], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['WEST'],
            ['PLACE', 'MELON', 6],
            ['FEED'],
            ['NORTH'],
            ['PLACE', 'MELON', 6],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['FEED'],
            ['SOUTH']],
  'market': [['SELL', 'MELON', 12], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['FEED'],
            ['PASS'],
            ['CARE'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['CARE'],
            ['SOUTH']],
  'market': [['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['PASS'],
            ['BUILD_COOP'],
            ['PASS'],
            ['BUILD_PASTURE'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'MELON', 6]],
  'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['PLANT', 'STRAWBERRY'],
            ['NORTH'],
            ['PASS'],
            ['EAST'],
            ['SOUTH'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['SOUTH'],
            ['PASS']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['FEED'],
            ['PASS'],
            ['FEED'],
            ['HARVEST'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['FEED'],
            ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['NORTH'],
            ['CARE'],
            ['PASS'],
            ['CARE'],
            ['SOUTH'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['WATER'],
            ['CARE'],
            ['PASS']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['PLANT', 'WHEAT'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['PASS'],
            ['WEST'],
            ['PASS'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['WATER'],
            ['WEST'],
            ['PASS'],
            ['EAST'],
            ['PLACE', 'MILK', 12],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['WATER'],
            ['EAST'],
            ['PASS']],
  'market': [['SELL', 'MILK', 12]]},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['SOUTH'],
            ['PASS'],
            ['FEED'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['HARVEST'],
            ['FEED'],
            ['PASS']],
  'market': []},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['WATER'],
            ['FEED'],
            ['PASS'],
            ['CARE'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['CARE'],
            ['PASS']],
  'market': [['SELL', 'WHEAT', 6]]},
 {'farmer': ['WATER'],
  'hands': [['HARVEST'],
            ['CARE'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['PASS'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': [['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'MELON', 12],
             ['SELL', 'WHEAT', 36],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['BUY_LAND'],
             ['BUY_ANIMAL', 'SHEEP', 4],
             ['BUY_ANIMAL', 'GOOSE', 1],
             ['BUY_PRODUCT', 'FERTILIZER', 2]]},
 {'farmer': ['WEST'],
  'hands': [['PICKUP', 'SHEEP', 1],
            ['BUILD_PASTURE'],
            ['PICKUP', 'WHEAT', 5],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['BUILD_PASTURE'],
            ['PASS'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 2],
             ['BUY_PRODUCT', 'WHEAT', 11],
             ['BUY_SEED', 'MELON', 8],
             ['BUY_SEED', 'WHEAT', 15],
             ['BUY_ANIMAL', 'SHEEP', 3]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['WEST'],
            ['FEED'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 3],
            ['PICKUP', 'SHEEP', 1],
            ['PICKUP', 'SHEEP', 1],
            ['PICKUP', 'SHEEP', 1],
            ['PICKUP', 'GOOSE', 1],
            ['EAST'],
            ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 7]]},
 {'farmer': ['NORTH'],
  'hands': [['PLACE', 'SHEEP'],
            ['PLANT', 'MELON'],
            ['EAST'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH'],
            ['PLACE', 'SHEEP'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 7]],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['WATER'],
            ['FEED'],
            ['FEED'],
            ['CARE'],
            ['FEED'],
            ['SOUTH'],
            ['CARE'],
            ['PLACE', 'SHEEP'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'SHEEP', 1]],
  'market': []},
 {'farmer': ['CARE'],
  'hands': [['WEST'],
            ['WEST'],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['CARE'],
            ['BUILD_PASTURE'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['NORTH'],
            ['PLANT', 'MELON'],
            ['FEED'],
            ['EAST'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['NORTH'],
            ['BUILD_PASTURE'],
            ['PLACE', 'GOOSE'],
            ['CARE'],
            ['SOUTH']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['FEED'],
            ['WATER'],
            ['NORTH'],
            ['PLACE', 'MILK', 6],
            ['CARE'],
            ['NORTH'],
            ['BUILD_PASTURE'],
            ['PLACE', 'SHEEP'],
            ['WEST'],
            ['EAST'],
            ['EAST'],
            ['PLACE', 'SHEEP']],
  'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['CARE'],
            ['WEST'],
            ['WATER'],
            ['PICKUP', 'SHEEP', 1],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['CARE'],
            ['PLANT', 'MELON'],
            ['WATER'],
            ['WATER'],
            ['FEED']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['PLANT', 'MELON'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['PLANT', 'MELON'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['FEED'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['FEED'],
            ['SOUTH'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['NORTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['SOUTH'],
            ['NORTH'],
            ['SOUTH'],
            ['CARE'],
            ['PICKUP', 'SHEEP', 1],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'MELON'],
            ['EAST'],
            ['NORTH'],
            ['FEED']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['PLACE', 'SHEEP'],
            ['NORTH'],
            ['SOUTH'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['CARE']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['FEED'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['CARE'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WATER'],
            ['FEED']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'SHEEP'],
            ['PLANT', 'MELON'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['EAST'],
            ['CARE']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['NORTH'],
            ['WATER'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['FEED'],
            ['WATER'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['PLANT', 'MELON'],
            ['FEED'],
            ['CARE'],
            ['SOUTH'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['SOUTH'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['PLANT', 'WHEAT'],
            ['SOUTH'],
            ['WATER'],
            ['CARE'],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['CARE']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['SOUTH'],
            ['SOUTH'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['SOUTH'],
            ['WEST'],
            ['CARE'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['PASS'],
  'hands': [['FEED'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['WATER'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['WATER'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['PASS'],
  'hands': [['PASS'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'FERTILIZER', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['CARE'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['FEED'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 6],
            ['HARVEST'],
            ['PASS'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['WEST'],
            ['WEST'],
            ['HARVEST'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['FEED'],
            ['FEED'],
            ['CARE'],
            ['SOUTH'],
            ['FEED'],
            ['FEED'],
            ['CARE'],
            ['PLACE', 'WOOL', 4],
            ['CARE'],
            ['PICKUP', 'WHEAT', 2],
            ['COLLECT_FERTILIZER'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WEST'],
            ['SOUTH'],
            ['PLACE', 'MILK', 3],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['NORTH'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 5],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['FEED'],
            ['CARE'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['HARVEST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['EAST'],
            ['FEED'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['NORTH'],
            ['CARE'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['NORTH'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['FEED'],
            ['CARE'],
            ['SOUTH'],
            ['NORTH'],
            ['CARE'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['WEST'],
  'hands': [['FEED'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['NORTH'],
            ['CARE'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['FEED'],
            ['WATER'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['DIG'],
            ['CARE'],
            ['PLACE', 'MILK', 3],
            ['WATER'],
            ['NORTH'],
            ['SOUTH']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WEST'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['PLANT', 'STRAWBERRY'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['PLACE', 'WOOL', 4]],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['FEED'],
            ['EAST'],
            ['WATER'],
            ['CARE'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['NORTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['NORTH'],
            ['CARE'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['EAST'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['EAST'],
            ['PASS'],
            ['EAST'],
            ['CARE'],
            ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['EAST'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['EAST'],
            ['PASS'],
            ['FEED'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['NORTH'],
            ['PASS'],
            ['EAST'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['EAST'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['NORTH'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['WATER'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['HARVEST'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['PASS'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['PASS'],
  'hands': [['PLANT', 'STRAWBERRY'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PASS'],
  'hands': [['WATER'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'FERTILIZER', 6],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['CARE'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8]],
  'market': [['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'WHEAT', 6],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 1],
            ['PASS'],
            ['NORTH'],
            ['CARE'],
            ['PASS'],
            ['CARE'],
            ['EAST'],
            ['PASS'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 2],
            ['FEED'],
            ['WEST'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['WEST'],
            ['CARE'],
            ['CARE']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['SOUTH'],
            ['FEED'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['EAST'],
            ['FEED'],
            ['CARE'],
            ['CARE'],
            ['FEED'],
            ['WATER'],
            ['CARE'],
            ['CARE'],
            ['WATER'],
            ['WATER'],
            ['CARE'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['WATER'],
            ['WATER'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 3]]},
 {'farmer': ['CARE'],
  'hands': [['NORTH'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['WATER'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['WATER'],
            ['WATER'],
            ['WATER'],
            ['CARE'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['NORTH'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['WATER'],
            ['WEST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['WATER'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['WEST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['FEED'],
            ['EAST'],
            ['PLACE', 'MILK', 3],
            ['EAST'],
            ['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['WATER']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['WATER'],
            ['WEST']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['EAST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['NORTH'],
            ['HARVEST'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['WATER']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH']],
  'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['PASS'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['PLANT', 'STRAWBERRY'],
            ['HARVEST'],
            ['SOUTH'],
            ['EAST'],
            ['PASS'],
            ['EAST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['FEED'],
            ['EAST'],
            ['PASS'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 4]]},
 {'farmer': ['WATER'],
  'hands': [['COLLECT_FERTILIZER'],
            ['CARE'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['PASS'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['PASS'],
            ['WEST'],
            ['PASS'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['PASS'],
            ['PASS'],
            ['PASS'],
            ['WATER']],
  'market': []},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'FERTILIZER', 5],
             ['SELL', 'WHEAT', 3],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'],
            ['PICKUP', 'WHEAT', 8],
            ['EAST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['CARE'],
            ['EAST'],
            ['CARE']],
  'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 6],
            ['FEED'],
            ['EAST'],
            ['WEST'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 6]]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 6],
            ['NORTH'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['FEED'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 2],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['CARE'],
            ['WEST'],
            ['FEED'],
            ['FEED'],
            ['FEED'],
            ['HARVEST'],
            ['PLACE', 'MILK', 3],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 2],
            ['CARE'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['CARE'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['CARE'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 1],
            ['FEED'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['CARE']],
  'market': [['BUY_PRODUCT', 'WHEAT', 5]]},
 {'farmer': ['HARVEST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WEST'],
            ['PLACE', 'WOOL', 6],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['NORTH'],
            ['EAST'],
            ['WATER'],
            ['FEED'],
            ['WEST'],
            ['SOUTH'],
            ['CARE'],
            ['FEED'],
            ['WEST'],
            ['CARE'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 3]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['FEED'],
            ['EAST'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['CARE'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['CARE'],
            ['PLACE', 'WOOL', 6],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 4], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['HARVEST'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WEST'],
            ['WEST']],
  'market': []},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['NORTH'],
            ['PLANT', 'STRAWBERRY'],
            ['WEST'],
            ['HARVEST'],
            ['HARVEST'],
            ['FEED'],
            ['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['WATER'],
            ['WEST'],
            ['PLANT', 'STRAWBERRY'],
            ['PLANT', 'STRAWBERRY'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WATER'],
            ['FERTILIZE'],
            ['WEST'],
            ['FERTILIZE']],
  'market': [['SELL', 'WHEAT', 7], ['BUY_SEED', 'STRAWBERRY', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['PLANT', 'STRAWBERRY'],
            ['NORTH'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['HARVEST'],
            ['SOUTH'],
            ['SOUTH'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WATER']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['NORTH'],
            ['PLANT', 'STRAWBERRY'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['SOUTH'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['DIG'],
            ['WATER'],
            ['HARVEST']],
  'market': [['SELL', 'WHEAT', 3]]},
 {'farmer': ['HARVEST'],
  'hands': [['CARE'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['PASS']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['WATER'],
            ['PASS'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['HARVEST'],
            ['WATER'],
            ['HARVEST'],
            ['PASS']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['PASS'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['PASS'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['PASS'],
            ['PASS'],
            ['PASS']],
  'market': [['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['EAST'],
  'hands': [['PASS'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['PASS'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'WHEAT']],
  'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'WHEAT', 16],
             ['SELL', 'FERTILIZER', 2],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['CARE'],
            ['NORTH'],
            ['CARE']],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['NORTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 7],
            ['PASS'],
            ['CARE'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['FEED'],
            ['HARVEST'],
            ['PLACE', 'WOOL', 4],
            ['PLACE', 'MILK', 6],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 2],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['FEED'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 1],
            ['PASS'],
            ['FEED'],
            ['NORTH'],
            ['FEED'],
            ['FEED'],
            ['CARE'],
            ['HARVEST'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['WEST'],
            ['SOUTH'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 1],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['CARE'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['PLACE', 'MILK', 6],
            ['CARE'],
            ['EAST'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['FEED'],
            ['CARE'],
            ['EAST'],
            ['WATER']],
  'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WATER'],
            ['WATER'],
            ['PICKUP', 'FERTILIZER', 5],
            ['NORTH'],
            ['FEED'],
            ['FEED'],
            ['NORTH'],
            ['FEED'],
            ['CARE'],
            ['SOUTH'],
            ['EAST'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['NORTH'],
            ['WEST'],
            ['EAST'],
            ['FEED'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WATER'],
            ['PLACE', 'MILK', 3],
            ['WATER']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['WATER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['EAST'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['WEST'],
            ['EAST'],
            ['NORTH'],
            ['CARE'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['WATER'],
            ['WATER'],
            ['NORTH'],
            ['HARVEST'],
            ['EAST'],
            ['WATER'],
            ['FERTILIZE'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['HARVEST'],
            ['FERTILIZE'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['DIG'],
            ['EAST'],
            ['WATER'],
            ['CARE'],
            ['NORTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['WATER'],
            ['PLANT', 'STRAWBERRY'],
            ['NORTH'],
            ['CARE'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST']],
  'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['WATER'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['PLANT', 'STRAWBERRY'],
            ['SOUTH'],
            ['EAST']],
  'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['EAST'],
            ['FEED'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['WATER'],
            ['SOUTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['CARE'],
  'hands': [['WATER'],
            ['WATER'],
            ['FERTILIZE'],
            ['DIG'],
            ['WATER'],
            ['EAST'],
            ['EAST'],
            ['HARVEST'],
            ['FEED'],
            ['SOUTH'],
            ['WATER'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['SOUTH'],
            ['HARVEST'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['CARE'],
            ['WATER'],
            ['HARVEST'],
            ['PLANT', 'STRAWBERRY']],
  'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['SOUTH'],
            ['HARVEST'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['PASS'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['SOUTH'],
            ['WATER'],
            ['FERTILIZE'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'WHEAT'],
            ['EAST']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['EAST']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['HARVEST'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['EAST']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['PASS'],
            ['SOUTH'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['HARVEST'],
            ['SOUTH']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 8],
             ['SELL', 'WHEAT', 20],
             ['SELL', 'EGG', 3],
             ['SELL', 'FERTILIZER', 2],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 8], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 8], ['PICKUP', 'WHEAT', 8]],
  'market': [['SELL', 'MILK', 3],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['BUY_SEED', 'STRAWBERRY', 4]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 3],
            ['FEED'],
            ['NORTH'],
            ['NORTH'],
            ['FEED'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 6],
            ['PASS'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['SOUTH'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['PICKUP', 'WHEAT', 2],
            ['FEED'],
            ['HARVEST'],
            ['SOUTH'],
            ['FEED'],
            ['SOUTH'],
            ['PASS'],
            ['PASS'],
            ['FEED'],
            ['FEED'],
            ['SOUTH'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['PLACE', 'MILK', 3],
            ['CARE'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 2],
            ['NORTH'],
            ['CARE'],
            ['EAST'],
            ['CARE'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 4], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['NORTH'],
            ['FEED'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['CARE'],
            ['EAST'],
            ['PICKUP', 'WHEAT', 4],
            ['NORTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['CARE'],
            ['PLACE', 'MILK', 6],
            ['PICKUP', 'WHEAT', 1],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['WEST'],
            ['WEST'],
            ['CARE'],
            ['SOUTH'],
            ['CARE']],
  'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['HARVEST'],
  'hands': [['FEED'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 4],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['CARE'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 4], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['CARE'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['CARE'],
            ['WEST'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['PLANT', 'STRAWBERRY'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['EAST'],
            ['PLANT', 'STRAWBERRY'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['NORTH'],
            ['WATER'],
            ['FEED'],
            ['WATER'],
            ['HARVEST'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['HARVEST'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['SOUTH'],
  'hands': [['HARVEST'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['HARVEST'],
            ['WEST'],
            ['FERTILIZE'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['NORTH']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['PLANT', 'STRAWBERRY'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['DIG'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WEST'],
            ['EAST']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['WATER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['FERTILIZE'],
            ['PLANT', 'STRAWBERRY'],
            ['WEST'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['DIG'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['WEST'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['PLANT', 'STRAWBERRY'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['PLACE', 'STRAWBERRY', 2],
  'hands': [['WEST'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['PASS'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['EAST']],
  'market': [['SELL', 'STRAWBERRY', 2]]},
 {'farmer': ['PLACE', 'EGG', 1],
  'hands': [['WEST'],
            ['EAST'],
            ['EAST'],
            ['FERTILIZE'],
            ['WEST'],
            ['PASS'],
            ['WEST'],
            ['EAST'],
            ['EAST'],
            ['WATER'],
            ['PASS'],
            ['NORTH']],
  'market': [['SELL', 'EGG', 1]]},
 {'farmer': ['WEST'],
  'hands': [['SOUTH'],
            ['PASS'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['EAST'],
            ['WEST'],
            ['PASS'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['COLLECT_FERTILIZER'],
            ['PASS'],
            ['WATER'],
            ['PASS'],
            ['WEST'],
            ['PASS'],
            ['SOUTH'],
            ['FEED'],
            ['EAST'],
            ['WEST'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['SOUTH'],
            ['PASS'],
            ['SOUTH'],
            ['PASS'],
            ['SOUTH'],
            ['PASS'],
            ['PLACE', 'STRAWBERRY', 2],
            ['CARE'],
            ['PASS'],
            ['WEST'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PASS'],
  'hands': [['SOUTH'],
            ['PASS'],
            ['CARE'],
            ['PASS'],
            ['SOUTH'],
            ['PASS'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['WEST'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 10],
             ['SELL', 'FERTILIZER', 2],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['HARVEST'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['NORTH'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['WEST'],
            ['CARE']],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['PLACE', 'WOOL', 6],
  'hands': [['FEED'],
            ['HARVEST'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 6]]},
 {'farmer': ['SOUTH'],
  'hands': [['NORTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['HARVEST'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['EAST'],
            ['CARE'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['SOUTH'],
  'hands': [['FEED'],
            ['PLACE', 'WOOL', 6],
            ['HARVEST'],
            ['NORTH'],
            ['EAST'],
            ['PLACE', 'WOOL', 6],
            ['NORTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'WOOL', 12], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['CARE'],
            ['NORTH'],
            ['EAST'],
            ['FEED'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 8],
            ['PLACE', 'WOOL', 6],
            ['HARVEST'],
            ['SOUTH'],
            ['HARVEST'],
            ['WEST'],
            ['PLACE', 'MILK', 3]],
  'market': [['SELL', 'WOOL', 6], ['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['CARE'],
            ['NORTH'],
            ['CARE'],
            ['CARE'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 8],
            ['CARE'],
            ['FEED'],
            ['CARE'],
            ['WATER'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WATER'],
  'hands': [['FEED'],
            ['NORTH'],
            ['PLACE', 'WOOL', 6],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['CARE'],
            ['NORTH'],
            ['WEST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 6], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['CARE'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['FEED'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['COLLECT_FERTILIZER'],
            ['CARE'],
            ['WEST'],
            ['SOUTH'],
            ['CARE'],
            ['CARE'],
            ['SOUTH'],
            ['SOUTH'],
            ['FEED'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['NORTH'],
            ['CARE'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['PLACE', 'WOOL', 6],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['FEED'],
            ['WATER'],
            ['WEST'],
            ['FEED'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['FEED'],
            ['CARE'],
            ['WATER'],
            ['EAST'],
            ['SOUTH'],
            ['WATER'],
            ['WATER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WEST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['WATER'],
            ['WATER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['EAST'],
  'hands': [['WATER'],
            ['EAST'],
            ['SOUTH'],
            ['PLACE', 'MILK', 3],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['FERTILIZE'],
            ['EAST'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WEST'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['WATER'],
            ['NORTH'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['HARVEST'],
            ['EAST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['NORTH'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['PLACE', 'WOOL', 6],
  'hands': [['SOUTH'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 6]]},
 {'farmer': ['NORTH'],
  'hands': [['HARVEST'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WATER'],
            ['NORTH'],
            ['FERTILIZE'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST']],
  'market': []},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['EAST'],
            ['WEST'],
            ['EAST'],
            ['FEED'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['NORTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['WEST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['HARVEST'],
            ['EAST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['CARE'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST']],
  'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 14],
             ['SELL', 'WOOL', 7],
             ['SELL', 'MILK', 3],
             ['SELL', 'EGG', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 8], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 8], ['CARE']],
  'market': [['SELL', 'MILK', 3],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 3],
            ['FEED'],
            ['PICKUP', 'WHEAT', 8],
            ['HARVEST'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['EAST']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 6],
            ['WEST'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['PASS'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['FEED'],
            ['PLACE', 'WOOL', 4],
            ['EAST'],
            ['PICKUP', 'WHEAT', 1],
            ['PASS'],
            ['PASS'],
            ['EAST'],
            ['WEST'],
            ['CARE'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['NORTH'],
            ['FEED'],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 1],
            ['PASS'],
            ['NORTH'],
            ['HARVEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['FEED'],
            ['WEST'],
            ['HARVEST'],
            ['NORTH'],
            ['CARE'],
            ['FEED'],
            ['EAST'],
            ['PICKUP', 'WHEAT', 3],
            ['CARE'],
            ['EAST'],
            ['WATER'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH'],
            ['CARE'],
            ['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['WEST'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['FEED'],
            ['FEED'],
            ['CARE'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['FEED'],
            ['NORTH'],
            ['DROP'],
            ['WATER'],
            ['HARVEST']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['CARE'],
            ['CARE'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['CARE'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['CARE'],
  'hands': [['CARE'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['HARVEST'],
            ['CARE'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['WEST'],
            ['WATER'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['NORTH'],
            ['WATER'],
            ['WEST'],
            ['PLACE', 'MILK', 3],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['WEST'],
  'hands': [['HARVEST'],
            ['WEST'],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 8],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['WEST'],
            ['WATER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['SOUTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['HARVEST'],
            ['WEST'],
            ['PLACE', 'MILK', 3],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['FERTILIZE'],
            ['NORTH'],
            ['FEED'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['FERTILIZE'],
  'hands': [['HARVEST'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['SOUTH'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['WATER'],
  'hands': [['PLANT', 'WHEAT'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['WATER'],
            ['PLACE', 'STRAWBERRY', 5]],
  'market': [['SELL', 'STRAWBERRY', 5],
             ['SELL', 'WHEAT', 3],
             ['BUY_SEED', 'WHEAT', 1],
             ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['EAST'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['WATER'],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['WATER'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['HARVEST'],
            ['WATER'],
            ['PICKUP', 'WHEAT', 1]],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['DIG'],
            ['NORTH'],
            ['FEED'],
            ['HARVEST'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['PLACE', 'STRAWBERRY', 6],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WEST']],
  'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['FERTILIZE'],
  'hands': [['PLANT', 'WHEAT'],
            ['WATER'],
            ['HARVEST'],
            ['PASS'],
            ['SOUTH'],
            ['WATER'],
            ['WEST'],
            ['HARVEST'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['SOUTH']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WATER'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['PLANT', 'WHEAT'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 14],
             ['SELL', 'WHEAT', 4],
             ['SELL', 'EGG', 2],
             ['SELL', 'FERTILIZER', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8]],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 6],
            ['PASS'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['WEST'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['FEED'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 1],
            ['NORTH'],
            ['PASS'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['CARE'],
  'hands': [['HARVEST'],
            ['FEED'],
            ['WEST'],
            ['WEST'],
            ['CARE'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 2],
            ['PASS'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['CARE'],
            ['FEED'],
            ['HARVEST'],
            ['NORTH'],
            ['FEED'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 3],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['CARE'],
            ['HARVEST'],
            ['SOUTH'],
            ['CARE'],
            ['EAST'],
            ['FEED'],
            ['EAST'],
            ['CARE'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['WEST'],
  'hands': [['PLACE', 'MILK', 3],
            ['WEST'],
            ['WATER'],
            ['EAST'],
            ['FEED'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['FERTILIZE']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH'],
            ['FEED'],
            ['FEED'],
            ['WEST'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['NORTH'],
            ['WEST'],
            ['WATER'],
            ['PLACE', 'MILK', 3],
            ['FEED'],
            ['WATER'],
            ['CARE'],
            ['FERTILIZE'],
            ['CARE'],
            ['EAST'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['FEED'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['FERTILIZE'],
            ['WEST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['CARE'],
            ['WEST'],
            ['DIG'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['DIG'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['EAST'],
            ['NORTH'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['HARVEST']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['WATER'],
  'hands': [['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['EAST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['FERTILIZE'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['WATER'],
            ['NORTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['EAST'],
            ['EAST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['WATER'],
            ['EAST'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['HARVEST'],
            ['EAST'],
            ['HARVEST']],
  'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['EAST']],
  'market': []},
 {'farmer': ['CARE'],
  'hands': [['HARVEST'],
            ['FEED'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['SOUTH'],
            ['PLACE', 'WHEAT', 2],
            ['NORTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['WATER'],
            ['PASS'],
            ['EAST']],
  'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['WEST'],
            ['EAST'],
            ['PASS'],
            ['SOUTH'],
            ['CARE'],
            ['PICKUP', 'FERTILIZER', 4],
            ['EAST'],
            ['WATER'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER'],
            ['SOUTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['WEST'],
            ['EAST'],
            ['PASS'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['EAST'],
            ['PASS'],
            ['EAST'],
            ['WEST'],
            ['PASS'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['SOUTH'],
            ['PLACE', 'STRAWBERRY', 2],
            ['PASS'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['EAST'],
            ['PASS'],
            ['FERTILIZE'],
            ['WEST'],
            ['PASS'],
            ['SOUTH']],
  'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 14],
             ['SELL', 'MILK', 3],
             ['SELL', 'EGG', 2],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'],
            ['HARVEST'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 3],
            ['PLACE', 'WOOL', 4],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['CARE'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['WEST']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3]]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 6],
            ['HARVEST'],
            ['FEED'],
            ['HARVEST'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['WEST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['FEED'],
            ['FEED'],
            ['EAST'],
            ['NORTH'],
            ['FEED'],
            ['FEED'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['HARVEST'],
            ['EAST'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['WEST'],
            ['PLACE', 'WOOL', 4],
            ['FEED'],
            ['SOUTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['HARVEST'],
            ['SOUTH'],
            ['CARE'],
            ['WEST']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['FEED'],
            ['WEST'],
            ['NORTH'],
            ['PLACE', 'WOOL', 4],
            ['PLACE', 'WOOL', 4],
            ['SOUTH'],
            ['HARVEST'],
            ['CARE'],
            ['PLACE', 'MILK', 3],
            ['NORTH'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'WOOL', 8], ['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['CARE'],
            ['EAST'],
            ['NORTH'],
            ['HARVEST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['WEST'],
            ['FEED'],
            ['CARE'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['HARVEST'],
  'hands': [['FEED'],
            ['FEED'],
            ['WATER'],
            ['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['PLACE', 'WOOL', 3],
            ['WEST'],
            ['HARVEST'],
            ['SOUTH']],
  'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['FEED'],
            ['NORTH'],
            ['PLACE', 'WOOL', 3],
            ['PICKUP', 'WHEAT', 8],
            ['CARE'],
            ['CARE'],
            ['FERTILIZE']],
  'market': [['SELL', 'WOOL', 3], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['HARVEST'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'WOOL', 3],
            ['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['WATER']],
  'market': [['SELL', 'WOOL', 3], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['CARE'],
  'hands': [['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['CARE'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 8],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 5]]},
 {'farmer': ['SOUTH'],
  'hands': [['HARVEST'],
            ['WATER'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['CARE'],
            ['WEST'],
            ['SOUTH'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['NORTH'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['WEST'],
            ['SOUTH'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH']],
  'market': []},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['PLACE', 'WOOL', 3],
            ['WATER']],
  'market': [['SELL', 'WOOL', 3], ['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['PLACE', 'MILK', 3],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['FERTILIZE'],
            ['WATER'],
            ['WATER'],
            ['PLACE', 'WOOL', 4],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['PICKUP', 'WHEAT', 1],
            ['WATER']],
  'market': [['SELL', 'WOOL', 4]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['PLACE', 'STRAWBERRY', 2],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'STRAWBERRY', 2]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['NORTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['PASS'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['WEST'],
            ['PASS'],
            ['EAST'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['WATER']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['HARVEST'],
            ['PASS'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['FERTILIZE'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['EAST'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WEST'],
            ['PASS'],
            ['NORTH'],
            ['FEED'],
            ['EAST'],
            ['PASS'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 21],
             ['BUY_PRODUCT', 'WHEAT', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['EAST'],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['NORTH'],
            ['CARE']],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['NORTH'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'WHEAT', 8]],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['EAST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 7],
            ['CARE'],
            ['CARE'],
            ['PASS'],
            ['WEST'],
            ['WEST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['FEED'],
            ['FEED'],
            ['WEST'],
            ['PLACE', 'WOOL', 4],
            ['EAST'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 2],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['FEED']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['EAST'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'MILK', 3],
            ['PICKUP', 'WHEAT', 1],
            ['FEED'],
            ['CARE'],
            ['HARVEST'],
            ['HARVEST'],
            ['NORTH'],
            ['SOUTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['NORTH'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['CARE'],
            ['FEED'],
            ['EAST'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['FEED']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['EAST'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['SOUTH'],
  'hands': [['WATER'],
            ['FEED'],
            ['EAST'],
            ['FEED'],
            ['FEED'],
            ['WATER'],
            ['EAST'],
            ['PLACE', 'MILK', 3],
            ['WEST'],
            ['WATER'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['CARE'],
            ['CARE'],
            ['HARVEST'],
            ['WATER'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['HARVEST'],
            ['SOUTH']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['PICKUP', 'FERTILIZER', 2],
  'hands': [['WATER'],
            ['WEST'],
            ['FERTILIZE'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['WATER']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['FEED'],
            ['WATER'],
            ['HARVEST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['NORTH'],
            ['EAST'],
            ['HARVEST'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['CARE'],
            ['WEST'],
            ['EAST'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['WATER'],
            ['DIG'],
            ['WEST'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WATER']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['DIG'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['HARVEST'],
            ['SOUTH']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['PLANT', 'WHEAT'],
            ['NORTH'],
            ['WATER'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['WEST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['WEST'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['FERTILIZE'],
            ['DIG'],
            ['EAST'],
            ['FEED'],
            ['EAST'],
            ['EAST'],
            ['WEST']],
  'market': []},
 {'farmer': ['FERTILIZE'],
  'hands': [['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['FERTILIZE'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['SOUTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['CARE'],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['FEED'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['FERTILIZE'],
  'hands': [['CARE'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['PLACE', 'STRAWBERRY', 6],
            ['NORTH']],
  'market': [['SELL', 'STRAWBERRY', 6], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 8],
             ['SELL', 'MILK', 3],
             ['SELL', 'EGG', 3],
             ['SELL', 'MELON', 4],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 8], ['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 8], ['PICKUP', 'WHEAT', 8]],
  'market': [['SELL', 'MILK', 3],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['BUY_SEED', 'WHEAT', 5]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 3],
            ['FEED'],
            ['PICKUP', 'WHEAT', 8],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['EAST'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 6],
            ['WEST'],
            ['CARE'],
            ['HARVEST'],
            ['FEED'],
            ['FEED'],
            ['PASS'],
            ['PASS'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['FEED'],
            ['FEED'],
            ['SOUTH'],
            ['SOUTH'],
            ['CARE'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 1],
            ['PASS'],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['CARE'],
            ['SOUTH'],
            ['PLACE', 'MILK', 3],
            ['NORTH'],
            ['FEED'],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['CARE'],
  'hands': [['FEED'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 5],
            ['FEED'],
            ['CARE'],
            ['EAST'],
            ['CARE'],
            ['NORTH'],
            ['EAST'],
            ['HARVEST'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['NORTH'],
            ['CARE'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['NORTH'],
            ['HARVEST'],
            ['EAST'],
            ['NORTH'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['FEED'],
            ['SOUTH'],
            ['CARE'],
            ['CARE'],
            ['EAST'],
            ['HARVEST'],
            ['HARVEST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['HARVEST'],
            ['FEED'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['SOUTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['NORTH'],
            ['CARE'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['PLACE', 'MILK', 3]],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['HARVEST'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['NORTH'],
            ['EAST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['CARE'],
            ['NORTH'],
            ['HARVEST'],
            ['FEED'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['HARVEST'],
            ['WEST'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['HARVEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['DIG'],
  'hands': [['WEST'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['PLACE', 'STRAWBERRY', 4],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WATER'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'STRAWBERRY', 4]]},
 {'farmer': ['WATER'],
  'hands': [['COLLECT_FERTILIZER'],
            ['DIG'],
            ['FEED'],
            ['DIG'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WEST'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['WATER'],
            ['EAST'],
            ['HARVEST'],
            ['PLACE', 'STRAWBERRY', 8],
            ['SOUTH'],
            ['SOUTH'],
            ['NORTH']],
  'market': [['SELL', 'STRAWBERRY', 8], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['NORTH'],
            ['FEED'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['DROP'],
            ['SOUTH'],
            ['DIG']],
  'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['WATER'],
            ['CARE'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['SOUTH'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['PLACE', 'STRAWBERRY', 6],
            ['WATER']],
  'market': [['SELL', 'STRAWBERRY', 6]]},
 {'farmer': ['HARVEST'],
  'hands': [['WEST'],
            ['WATER'],
            ['HARVEST'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['EAST']],
  'market': []},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['SOUTH'],
            ['EAST'],
            ['PASS'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['WEST'],
            ['SOUTH'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 4],
             ['SELL', 'WHEAT', 5],
             ['SELL', 'FERTILIZER', 4],
             ['SELL', 'EGG', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8], ['HARVEST'], ['WEST'], ['PICKUP', 'WHEAT', 8], ['NORTH'], ['PICKUP', 'WHEAT', 8]],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 14]]},
 {'farmer': ['WEST'],
  'hands': [['FEED'],
            ['PLACE', 'WOOL', 4],
            ['WEST'],
            ['CARE'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['CARE'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['PICKUP', 'WHEAT', 7],
            ['HARVEST'],
            ['NORTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['HARVEST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['EAST'],
            ['FEED'],
            ['PLACE', 'WOOL', 4],
            ['FEED'],
            ['SOUTH'],
            ['PICKUP', 'WHEAT', 1],
            ['CARE'],
            ['CARE'],
            ['EAST'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'WOOL', 4],
            ['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['HARVEST'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['WEST'],
            ['SOUTH'],
            ['NORTH'],
            ['CARE'],
            ['PLACE', 'WOOL', 4],
            ['HARVEST'],
            ['FEED'],
            ['SOUTH'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['CARE'],
            ['FEED'],
            ['CARE'],
            ['FEED'],
            ['NORTH'],
            ['WEST'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['FEED'],
            ['WEST'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['HARVEST'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['CARE'],
            ['DROP'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['DIG'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['FEED'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['PLANT', 'WHEAT'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['SOUTH'],
            ['PLACE', 'WOOL', 4],
            ['DIG'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['DIG']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['WATER'],
            ['WEST'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['PLACE', 'WOOL', 4],
            ['PLACE', 'MILK', 3],
            ['EAST'],
            ['PLANT', 'WHEAT']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['NORTH'],
            ['DIG'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['PLACE', 'MILK', 3],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WEST'],
            ['PICKUP', 'FERTILIZER', 5],
            ['CARE'],
            ['WATER']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['DIG'],
            ['PLANT', 'WHEAT'],
            ['DIG'],
            ['WATER'],
            ['PICKUP', 'WHEAT', 8],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 4]]},
 {'farmer': ['PICKUP', 'FERTILIZER', 2],
  'hands': [['PLANT', 'WHEAT'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['DIG'],
            ['EAST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['WATER'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['FERTILIZE'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['WATER'],
            ['EAST']],
  'market': []},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['DIG'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['EAST'],
            ['FERTILIZE'],
            ['NORTH'],
            ['NORTH'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['CARE'],
  'hands': [['PLANT', 'WHEAT'],
            ['WEST'],
            ['WEST'],
            ['HARVEST'],
            ['EAST'],
            ['HARVEST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['WATER'],
            ['FERTILIZE'],
            ['DIG'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['WEST'],
            ['FEED'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_PRODUCT', 'FERTILIZER', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['EAST'],
            ['DIG'],
            ['HARVEST'],
            ['DIG'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['WATER'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['FERTILIZE'],
            ['WATER'],
            ['FERTILIZE'],
            ['NORTH'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 3], ['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['SOUTH'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['WATER'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 2]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['DIG'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['NORTH'],
            ['WEST']],
  'market': [['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 6],
             ['SELL', 'WOOL', 4],
             ['SELL', 'WHEAT', 7],
             ['SELL', 'FERTILIZER', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 8], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 8], ['PICKUP', 'WHEAT', 8]],
  'market': [['SELL', 'MILK', 3],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['BUY_SEED', 'WHEAT', 8]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 3],
            ['FEED'],
            ['PICKUP', 'WHEAT', 8],
            ['HARVEST'],
            ['CARE'],
            ['SOUTH'],
            ['NORTH'],
            ['CARE'],
            ['WEST'],
            ['NORTH'],
            ['CARE'],
            ['EAST']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 6],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['EAST'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['PASS'],
            ['PASS'],
            ['HARVEST'],
            ['PASS'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['WEST'],
            ['FEED'],
            ['PLACE', 'WOOL', 4],
            ['EAST'],
            ['FEED'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'WHEAT', 1],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['PICKUP', 'WHEAT', 1],
            ['FEED'],
            ['CARE'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['PLACE', 'MILK', 3],
            ['PASS'],
            ['HARVEST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['NORTH'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 3],
            ['PASS'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['HARVEST'],
  'hands': [['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['CARE'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 3],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['NORTH'],
            ['SOUTH'],
            ['CARE'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['NORTH'],
            ['PLACE', 'MILK', 3]],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['CARE'],
            ['NORTH'],
            ['FEED'],
            ['CARE'],
            ['NORTH'],
            ['FERTILIZE'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['HARVEST'],
  'hands': [['NORTH'],
            ['FEED'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['CARE'],
            ['FERTILIZE'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['PLACE', 'WOOL', 4],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['FEED'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['DIG'],
  'hands': [['HARVEST'],
            ['WEST'],
            ['EAST'],
            ['CARE'],
            ['HARVEST'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['WEST'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['WATER'],
  'hands': [['PLANT', 'WHEAT'],
            ['WEST'],
            ['DIG'],
            ['HARVEST'],
            ['WATER'],
            ['DIG'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['COLLECT_FERTILIZER']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['WATER'],
            ['HARVEST'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['WEST'],
            ['DIG'],
            ['HARVEST'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['NORTH'],
            ['WATER'],
            ['FERTILIZE'],
            ['DIG'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['NORTH'],
            ['WEST']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['PLANT', 'WHEAT'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['FERTILIZE'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['WEST'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['WEST'],
            ['EAST']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['PLACE', 'EGG', 3],
  'hands': [['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER'],
            ['PLACE', 'STRAWBERRY', 4],
            ['EAST'],
            ['SOUTH']],
  'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'EGG', 3], ['BUY_PRODUCT', 'FERTILIZER', 2]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['WATER'],
            ['WATER'],
            ['DIG'],
            ['WEST'],
            ['EAST'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['EAST'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['SOUTH'],
            ['FERTILIZE']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['SOUTH'],
            ['FERTILIZE'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['SOUTH'],
            ['EAST'],
            ['PLACE', 'STRAWBERRY', 4],
            ['EAST'],
            ['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['EAST']],
  'market': [['SELL', 'STRAWBERRY', 4], ['BUY_PRODUCT', 'FERTILIZER', 3]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 13],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['CARE'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 8],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['EAST']],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 5]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 6],
            ['WEST'],
            ['PASS'],
            ['WEST'],
            ['PASS'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 1],
            ['FEED'],
            ['CARE'],
            ['CARE'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['SOUTH'],
            ['FEED'],
            ['HARVEST'],
            ['EAST'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 2],
            ['WEST'],
            ['PLACE', 'MILK', 3],
            ['PASS'],
            ['WEST'],
            ['HARVEST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['FEED'],
            ['CARE'],
            ['CARE'],
            ['FEED'],
            ['WEST'],
            ['SOUTH'],
            ['FEED'],
            ['PICKUP', 'WHEAT', 2],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['CARE']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['CARE'],
  'hands': [['FEED'],
            ['CARE'],
            ['SOUTH'],
            ['WEST'],
            ['CARE'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['EAST'],
  'hands': [['CARE'],
            ['SOUTH'],
            ['FEED'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['SOUTH'],
            ['FEED'],
            ['EAST'],
            ['EAST'],
            ['FERTILIZE'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['CARE'],
            ['NORTH'],
            ['PLACE', 'MILK', 3]],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 2], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['EAST'],
            ['HARVEST'],
            ['SOUTH'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['CARE'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 4], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['WATER'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['CARE']],
  'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['CARE'],
  'hands': [['EAST'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['WATER'],
            ['WATER'],
            ['DIG'],
            ['WATER'],
            ['WEST'],
            ['COLLECT_FERTILIZER']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['NORTH'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['WEST'],
            ['NORTH']],
  'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WATER'],
  'hands': [['NORTH'],
            ['HARVEST'],
            ['WATER'],
            ['EAST'],
            ['EAST'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['WATER'],
            ['DIG'],
            ['WATER'],
            ['NORTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['WATER']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['DIG'],
  'hands': [['FERTILIZE'],
            ['DIG'],
            ['WATER'],
            ['CARE'],
            ['HARVEST'],
            ['EAST'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['NORTH']],
  'market': []},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['EAST'],
            ['PLANT', 'WHEAT'],
            ['FERTILIZE'],
            ['COLLECT_FERTILIZER'],
            ['PLANT', 'WHEAT'],
            ['HARVEST'],
            ['DIG'],
            ['FERTILIZE'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['DIG']],
  'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['WATER'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['WATER'],
            ['DIG'],
            ['NORTH'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['WEST'],
  'hands': [['HARVEST'],
            ['EAST'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['HARVEST'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['WATER']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['PLACE', 'MILK', 3],
            ['WEST'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['WEST'],
            ['WATER'],
            ['FERTILIZE'],
            ['EAST']],
  'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['EAST'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'FERTILIZER', 1]]},
 {'farmer': ['FEED'],
  'hands': [['PLANT', 'WHEAT'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['HARVEST'],
            ['WEST'],
            ['FERTILIZE'],
            ['EAST'],
            ['FERTILIZE']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['WATER'],
            ['NORTH'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'STRAWBERRY', 4],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['WATER'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'STRAWBERRY', 4], ['BUY_PRODUCT', 'FERTILIZER', 2]]},
 {'farmer': ['HARVEST'],
  'hands': [['WEST'],
            ['PLACE', 'STRAWBERRY', 2],
            ['NORTH'],
            ['CARE'],
            ['WEST'],
            ['PICKUP', 'FERTILIZER', 5],
            ['EAST'],
            ['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 6],
             ['SELL', 'FERTILIZER', 14],
             ['SELL', 'WHEAT', 6],
             ['SELL', 'EGG', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['PICKUP', 'WHEAT', 8], ['PICKUP', 'WHEAT', 8], ['PICKUP', 'WHEAT', 8]],
  'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [['PLACE', 'MILK', 3],
            ['PLACE', 'WOOL', 4],
            ['WEST'],
            ['FEED'],
            ['NORTH'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 8],
            ['CARE'],
            ['EAST'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3]]},
 {'farmer': ['WEST'],
  'hands': [['PICKUP', 'WHEAT', 6],
            ['PASS'],
            ['HARVEST'],
            ['WEST'],
            ['HARVEST'],
            ['HARVEST'],
            ['PASS'],
            ['CARE'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['PICKUP', 'WHEAT', 1],
            ['EAST'],
            ['WEST'],
            ['FEED'],
            ['FEED'],
            ['PASS'],
            ['WEST'],
            ['HARVEST'],
            ['CARE'],
            ['NORTH'],
            ['CARE']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['FEED'],
            ['PLACE', 'WOOL', 4],
            ['FEED'],
            ['SOUTH'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['CARE'],
            ['FEED'],
            ['NORTH'],
            ['HARVEST'],
            ['WEST']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 4]]},
 {'farmer': ['FEED'],
  'hands': [['FEED'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PLACE', 'WOOL', 4],
            ['PLACE', 'WOOL', 4],
            ['DROP'],
            ['SOUTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['CARE'],
            ['CARE']],
  'market': [['SELL', 'WOOL', 8], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['CARE'],
            ['DROP'],
            ['HARVEST'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['PLACE', 'MILK', 3],
            ['CARE'],
            ['WEST'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['HARVEST'],
  'hands': [['FEED'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['CARE'],
            ['CARE'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['FEED'],
  'hands': [['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['FEED'],
            ['WEST'],
            ['WEST'],
            ['EAST'],
            ['CARE'],
            ['HARVEST'],
            ['PLACE', 'WOOL', 3],
            ['WEST']],
  'market': [['SELL', 'WOOL', 3], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['EAST'],
  'hands': [['NORTH'],
            ['CARE'],
            ['SOUTH'],
            ['NORTH'],
            ['CARE'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['NORTH'],
            ['CARE'],
            ['PICKUP', 'WHEAT', 8],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['HARVEST'],
  'hands': [['FEED'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH'],
            ['PLACE', 'WOOL', 3],
            ['FEED'],
            ['WEST'],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 3]]},
 {'farmer': ['CARE'],
  'hands': [['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['NORTH'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['SOUTH'],
  'hands': [['NORTH'],
            ['PLACE', 'WOOL', 3],
            ['PLANT', 'WHEAT'],
            ['HARVEST'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['SOUTH'],
            ['CARE'],
            ['SOUTH'],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 3]]},
 {'farmer': ['SOUTH'],
  'hands': [['WATER'],
            ['PICKUP', 'WHEAT', 7],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['WATER'],
            ['HARVEST'],
            ['SOUTH'],
            ['NORTH'],
            ['DROP'],
            ['FEED'],
            ['EAST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 4]]},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['EAST'],
            ['WEST'],
            ['WEST'],
            ['WATER'],
            ['FEED'],
            ['WEST'],
            ['NORTH'],
            ['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'STRAWBERRY', 4]],
  'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['EAST'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['CARE'],
            ['WATER'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['WATER'],
            ['FEED'],
            ['WATER'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['COLLECT_FERTILIZER']],
  'market': []},
 {'farmer': ['PLACE', 'FERTILIZER', 1],
  'hands': [['EAST'],
            ['WEST'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['HARVEST'],
            ['WEST'],
            ['DROP'],
            ['NORTH'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['FERTILIZE'],
            ['SOUTH'],
            ['WATER'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['WATER'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['DROP']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['SOUTH'],
            ['EAST'],
            ['EAST'],
            ['HARVEST'],
            ['EAST'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 3]],
  'market': []},
 {'farmer': ['CARE'],
  'hands': [['NORTH'],
            ['WEST'],
            ['WATER'],
            ['PLACE', 'STRAWBERRY', 6],
            ['WEST'],
            ['WATER'],
            ['EAST'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['WATER'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['WATER'],
            ['WATER'],
            ['WEST'],
            ['WEST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['FERTILIZE'],
            ['WATER'],
            ['FERTILIZE'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['WATER'],
            ['COLLECT_FERTILIZER']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['PICKUP', 'WHEAT', 8],
  'hands': [],
  'market': [['SELL', 'STRAWBERRY', 4],
             ['SELL', 'WHEAT', 8],
             ['SELL', 'FERTILIZER', 5],
             ['SELL', 'EGG', 1],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['FEED'],
  'hands': [['PICKUP', 'WHEAT', 8], ['PICKUP', 'WHEAT', 8], ['EAST'], ['CARE'], ['CARE'], ['PICKUP', 'WHEAT', 8]],
  'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['SOUTH'],
            ['NORTH'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['WEST'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 6],
            ['CARE'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['PICKUP', 'WHEAT', 1],
            ['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['PASS'],
            ['PASS']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['CARE'],
  'hands': [['FEED'],
            ['FEED'],
            ['WEST'],
            ['WEST'],
            ['HARVEST'],
            ['PLACE', 'FERTILIZER', 1],
            ['CARE'],
            ['EAST'],
            ['NORTH'],
            ['PLACE', 'FERTILIZER', 1],
            ['PICKUP', 'WHEAT', 2],
            ['PASS']],
  'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['CARE'],
            ['WEST'],
            ['PLACE', 'MILK', 3],
            ['HARVEST'],
            ['CARE'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['WEST'],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WATER'],
            ['PICKUP', 'WHEAT', 3],
            ['CARE'],
            ['SOUTH'],
            ['FEED'],
            ['WATER'],
            ['FEED'],
            ['CARE'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['CARE'],
            ['EAST'],
            ['PLACE', 'FERTILIZER', 1],
            ['CARE'],
            ['CARE']],
  'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['CARE'],
  'hands': [['FEED'],
            ['HARVEST'],
            ['FEED'],
            ['DIG'],
            ['PLACE', 'MILK', 3],
            ['WEST'],
            ['PLANT', 'WHEAT'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['EAST'],
  'hands': [['CARE'],
            ['WEST'],
            ['CARE'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['FEED'],
            ['SOUTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WEST'],
            ['WEST'],
            ['FEED'],
            ['WATER'],
            ['NORTH'],
            ['CARE'],
            ['CARE'],
            ['FERTILIZE']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['WATER'],
            ['WEST'],
            ['SOUTH'],
            ['WEST']],
  'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['HARVEST'],
            ['WATER'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['FERTILIZE'],
            ['WATER'],
            ['PLANT', 'WHEAT'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['PLANT', 'WHEAT'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['SOUTH'],
            ['WEST']],
  'market': [['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['WEST'],
  'hands': [['WATER'],
            ['WATER'],
            ['WATER'],
            ['DROP'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['HARVEST']],
  'market': [['SELL', 'MILK', 2], ['SELL', 'WOOL', 3]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['EAST'],
            ['EAST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['NORTH'],
            ['DIG'],
            ['WATER'],
            ['EAST'],
            ['FERTILIZE'],
            ['HARVEST'],
            ['NORTH']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WATER'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['NORTH'],
            ['HARVEST'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['WATER']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['NORTH'],
            ['WATER'],
            ['HARVEST'],
            ['WEST'],
            ['WATER'],
            ['NORTH'],
            ['DIG'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['HARVEST'],
            ['FERTILIZE'],
            ['HARVEST']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['PLANT', 'WHEAT'],
            ['WATER'],
            ['WATER'],
            ['EAST'],
            ['WEST'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['DIG'],
  'hands': [['NORTH'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['HARVEST'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['WATER'],
            ['WEST'],
            ['WATER']],
  'market': []},
 {'farmer': ['PLANT', 'WHEAT'],
  'hands': [['WATER'],
            ['NORTH'],
            ['SOUTH'],
            ['FERTILIZE'],
            ['EAST'],
            ['WATER'],
            ['NORTH'],
            ['WATER'],
            ['WATER'],
            ['NORTH'],
            ['NORTH'],
            ['EAST']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['WEST'],
            ['NORTH'],
            ['FEED'],
            ['EAST'],
            ['NORTH'],
            ['NORTH'],
            ['HARVEST'],
            ['FERTILIZE'],
            ['EAST'],
            ['HARVEST'],
            ['WATER'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['HARVEST'],
            ['PLACE', 'STRAWBERRY', 2],
            ['EAST'],
            ['CARE'],
            ['EAST'],
            ['PLANT', 'WHEAT'],
            ['EAST'],
            ['EAST'],
            ['WATER'],
            ['EAST'],
            ['EAST'],
            ['PASS']],
  'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 2]]},
 {'farmer': ['WATER'],
  'hands': [['SOUTH'],
            ['WEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['WATER'],
            ['NORTH'],
            ['PLANT', 'WHEAT']],
  'market': [['BUY_SEED', 'WHEAT', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [],
  'market': [['SELL', 'WHEAT', 25],
             ['SELL', 'STRAWBERRY', 3],
             ['SELL', 'FERTILIZER', 4],
             ['SELL', 'MELON', 22],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['HARVEST'],
            ['PICKUP', 'WHEAT', 8],
            ['EAST'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 8]],
  'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['NORTH'],
  'hands': [['PLACE', 'MILK', 3],
            ['FEED'],
            ['NORTH'],
            ['FEED'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 8],
            ['PICKUP', 'WHEAT', 6],
            ['WEST']],
  'market': [['SELL', 'MILK', 3]]},
 {'farmer': ['HARVEST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['FEED'],
            ['SOUTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['FEED'],
            ['SOUTH'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['SOUTH'],
  'hands': [['PICKUP', 'WHEAT', 2],
            ['FEED'],
            ['HARVEST'],
            ['NORTH'],
            ['EAST'],
            ['FEED'],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH'],
            ['FEED'],
            ['WEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['PLACE', 'MILK', 3],
  'hands': [['NORTH'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['FEED'],
            ['WEST'],
            ['WEST'],
            ['DROP'],
            ['WEST'],
            ['FEED'],
            ['SOUTH'],
            ['SOUTH']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]},
 {'farmer': ['PICKUP', 'WHEAT', 5],
  'hands': [['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['FEED'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['NORTH'],
            ['PASS'],
            ['WEST'],
            ['EAST'],
            ['FEED'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['FEED'],
            ['PLACE', 'MILK', 3],
            ['EAST'],
            ['EAST'],
            ['HARVEST'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['FEED'],
            ['WEST'],
            ['HARVEST']],
  'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 2]]},
 {'farmer': ['FEED'],
  'hands': [['EAST'],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['WEST'],
            ['DROP'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['WEST']],
  'market': [['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['FEED'],
            ['NORTH'],
            ['PICKUP', 'WHEAT', 3],
            ['FEED'],
            ['NORTH'],
            ['SOUTH'],
            ['HARVEST'],
            ['NORTH'],
            ['WATER'],
            ['EAST'],
            ['HARVEST'],
            ['HARVEST']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['FEED'],
  'hands': [['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['WEST'],
            ['HARVEST'],
            ['NORTH'],
            ['HARVEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['FERTILIZE'],
            ['WEST'],
            ['WATER']],
  'market': [['SELL', 'WHEAT', 1]]},
 {'farmer': ['COLLECT_FERTILIZER'],
  'hands': [['EAST'],
            ['EAST'],
            ['FEED'],
            ['NORTH'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['FERTILIZE'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['WATER'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['EAST'],
            ['WEST'],
            ['SOUTH']],
  'market': [['BUY_PRODUCT', 'WHEAT', 1]]},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['FEED'],
            ['EAST'],
            ['HARVEST'],
            ['HARVEST'],
            ['HARVEST'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['SOUTH'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['EAST'],
            ['EAST'],
            ['PLACE', 'FERTILIZER', 1],
            ['WEST'],
            ['EAST'],
            ['WATER'],
            ['PLACE', 'STRAWBERRY', 4],
            ['FERTILIZE'],
            ['EAST'],
            ['HARVEST'],
            ['SOUTH'],
            ['WATER']],
  'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 2], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['FERTILIZE'],
  'hands': [['NORTH'],
            ['SOUTH'],
            ['EAST'],
            ['WATER'],
            ['WATER'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['WATER'],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['HARVEST'],
            ['PLACE', 'STRAWBERRY', 2],
            ['NORTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['WATER'],
            ['SOUTH'],
            ['NORTH'],
            ['EAST'],
            ['NORTH'],
            ['EAST'],
            ['WATER']],
  'market': [['SELL', 'STRAWBERRY', 2]]},
 {'farmer': ['NORTH'],
  'hands': [['WATER'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['FERTILIZE'],
            ['WATER'],
            ['WEST'],
            ['EAST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['WATER'],
  'hands': [['SOUTH'],
            ['SOUTH'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['WATER'],
            ['WATER'],
            ['EAST']],
  'market': []},
 {'farmer': ['HARVEST'],
  'hands': [['WATER'],
            ['COLLECT_FERTILIZER'],
            ['PLACE', 'FERTILIZER', 1],
            ['WATER'],
            ['WATER'],
            ['HARVEST'],
            ['FERTILIZE'],
            ['SOUTH'],
            ['EAST'],
            ['HARVEST'],
            ['EAST'],
            ['EAST']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['EAST'],
  'hands': [['HARVEST'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['HARVEST'],
            ['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['WEST'],
            ['WATER'],
            ['EAST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['SOUTH'],
            ['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['SOUTH'],
            ['HARVEST'],
            ['EAST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['HARVEST'],
            ['WEST'],
            ['EAST'],
            ['HARVEST'],
            ['WEST'],
            ['SOUTH'],
            ['WEST'],
            ['NORTH'],
            ['NORTH']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['HARVEST'],
            ['WEST'],
            ['PLACE', 'FERTILIZER', 1],
            ['WEST'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['PLACE', 'STRAWBERRY', 4],
            ['WEST'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [],
  'market': [['SELL', 'WHEAT', 83],
             ['SELL', 'STRAWBERRY', 8],
             ['SELL', 'MILK', 3],
             ['SELL', 'FERTILIZER', 4],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE'],
             ['HIRE']]},
 {'farmer': ['HARVEST'],
  'hands': [['WEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['WEST']],
  'market': [['SELL', 'EGG', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['WEST'],
            ['HARVEST'],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['HARVEST'],
            ['SOUTH'],
            ['EAST'],
            ['WEST'],
            ['EAST']],
  'market': [['SELL', 'WOOL', 4]]},
 {'farmer': ['SOUTH'],
  'hands': [['HARVEST'],
            ['EAST'],
            ['SOUTH'],
            ['NORTH'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['COLLECT_FERTILIZER']],
  'market': []},
 {'farmer': ['HARVEST'],
  'hands': [['EAST'],
            ['HARVEST'],
            ['HARVEST'],
            ['HARVEST'],
            ['PLACE', 'WOOL', 4],
            ['PLACE', 'WOOL', 4],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 8]]},
 {'farmer': ['NORTH'],
  'hands': [['EAST'],
            ['WEST'],
            ['EAST'],
            ['EAST'],
            ['COLLECT_FERTILIZER'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['EAST'],
            ['HARVEST'],
            ['COLLECT_FERTILIZER']],
  'market': []},
 {'farmer': ['PLACE', 'WOOL', 4],
  'hands': [['PLACE', 'MILK', 3],
            ['WEST'],
            ['NORTH'],
            ['HARVEST'],
            ['DROP'],
            ['DROP'],
            ['NORTH'],
            ['HARVEST'],
            ['WEST'],
            ['EAST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['WEST'],
  'hands': [['COLLECT_FERTILIZER'],
            ['DROP'],
            ['PLACE', 'WOOL', 3],
            ['WEST'],
            ['NORTH'],
            ['NORTH'],
            ['NORTH'],
            ['EAST'],
            ['WEST'],
            ['HARVEST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 7]]},
 {'farmer': ['WEST'],
  'hands': [['DROP'],
            ['WEST'],
            ['WEST'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['NORTH'],
            ['PLACE', 'WOOL', 3],
            ['NORTH'],
            ['HARVEST'],
            ['NORTH']],
  'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['NORTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH'],
            ['EAST'],
            ['HARVEST']],
  'market': []},
 {'farmer': ['WEST'],
  'hands': [['NORTH'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['DROP'],
            ['DROP'],
            ['WEST'],
            ['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['WEST']],
  'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['NORTH'],
            ['EAST'],
            ['DROP'],
            ['NORTH'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['HARVEST'],
            ['NORTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['HARVEST'],
            ['DROP'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['HARVEST'],
            ['EAST'],
            ['WEST'],
            ['WEST'],
            ['HARVEST']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['HARVEST'],
  'hands': [['EAST'],
            ['SOUTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['HARVEST'],
            ['WEST']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['HARVEST'],
            ['SOUTH'],
            ['WEST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['WEST'],
            ['NORTH'],
            ['WEST'],
            ['EAST'],
            ['FERTILIZE']],
  'market': []},
 {'farmer': ['EAST'],
  'hands': [['SOUTH'],
            ['SOUTH'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['EAST'],
            ['HARVEST'],
            ['DROP'],
            ['WEST'],
            ['EAST'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 2]]},
 {'farmer': ['EAST'],
  'hands': [['SOUTH'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['SOUTH'],
            ['EAST'],
            ['NORTH'],
            ['EAST'],
            ['SOUTH'],
            ['EAST'],
            ['SOUTH']],
  'market': []},
 {'farmer': ['NORTH'],
  'hands': [['SOUTH'],
            ['NORTH'],
            ['NORTH'],
            ['SOUTH'],
            ['DROP'],
            ['HARVEST'],
            ['PASS'],
            ['SOUTH'],
            ['SOUTH'],
            ['SOUTH']],
  'market': [['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['NORTH'],
  'hands': [['DROP'], ['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['NORTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['DROP']],
  'market': [['SELL', 'WHEAT', 4], ['SELL', 'FERTILIZER', 4], ['SELL', 'EGG', 1]]},
 {'farmer': ['DROP'],
  'hands': [['EAST'], ['DROP'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['PASS'], ['DROP'], ['SOUTH'], ['PASS']],
  'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 2], ['SELL', 'FERTILIZER', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['EAST'],
            ['PASS'],
            ['EAST'],
            ['WEST'],
            ['COLLECT_FERTILIZER'],
            ['HARVEST'],
            ['PASS'],
            ['EAST'],
            ['DROP'],
            ['PASS']],
  'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WOOL', 3], ['SELL', 'WHEAT', 1]]},
 {'farmer': ['SOUTH'],
  'hands': [['COLLECT_FERTILIZER'],
            ['PASS'],
            ['EAST'],
            ['NORTH'],
            ['EAST'],
            ['EAST'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['PASS']],
  'market': []},
 {'farmer': ['SOUTH'],
  'hands': [['WEST'],
            ['PASS'],
            ['DROP'],
            ['COLLECT_FERTILIZER'],
            ['SOUTH'],
            ['EAST'],
            ['PASS'],
            ['NORTH'],
            ['PASS'],
            ['PASS']],
  'market': [['SELL', 'WHEAT', 1]]})
_CROPS = {'WHEAT': {'seed': 10,
           'first_yield_day': 2,
           'max_yield_day': 4,
           'interval': 0,
           'max_yield': 6,
           'ongoing': False,
           'water_needed': True},
 'CARROT': {'seed': 20,
            'first_yield_day': 2,
            'max_yield_day': 3,
            'interval': 0,
            'max_yield': 4,
            'ongoing': False,
            'water_needed': True},
 'TOMATO': {'seed': 50,
            'first_yield_day': 8,
            'max_yield_day': 8,
            'interval': 1,
            'max_yield': 4,
            'ongoing': True,
            'water_needed': True},
 'STRAWBERRY': {'seed': 100,
                'first_yield_day': 10,
                'max_yield_day': 10,
                'interval': 2,
                'max_yield': 4,
                'ongoing': True,
                'water_needed': True},
 'MELON': {'seed': 80,
           'first_yield_day': 10,
           'max_yield_day': 12,
           'interval': 0,
           'max_yield': 6,
           'ongoing': False,
           'water_needed': True}}


def _package(name):
    module = _types.ModuleType(name)
    module.__package__ = name
    module.__path__ = []
    _sys.modules[name] = module
    return module


def _plain_module(name):
    module = _types.ModuleType(name)
    module.__package__ = name.rpartition(".")[0]
    module.__file__ = "/kaggle/working/codex_bundle/" + name.replace(".", "/") + ".py"
    _sys.modules[name] = module
    return module


def _exec_module(name, source):
    module = _plain_module(name)
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


def _config_loader(config):
    frozen = _deepcopy(config)

    def load(path=None):
        del path
        return _deepcopy(frozen)

    return load


for _name in (
    "_codex_bundle",
    "_codex_bundle.agricola",
    "_codex_bundle.agricola.core",
    "_codex_bundle.agricola.strategy",
    "_codex_bundle.agricola.strategy.codex",
):
    _package(_name)

_state = _plain_module("_codex_bundle.agricola.core.state")
_state.CROPS = _deepcopy(_CROPS)

_routine = _plain_module(
    "_codex_bundle.agricola.strategy.codex.codex_v9_routine_data"
)
_routine.ROUTINE_ACTIONS = _ROUTINE_ACTIONS
_routine.ROUTINE_SHA256 = ROUTINE_SHA256

_observation = _exec_module(
    "_codex_bundle.agricola.core.observation_contract",
    _SOURCES["observation_contract"],
)
_v9 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_3q_mixed_high_density",
    _SOURCES["v9"],
)
_v9.load_v9_config = _config_loader(_CONFIGS["v9"])
_guarded = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_reactive_guarded",
    _SOURCES["guarded"],
)
_guarded.load_reactive_config = _config_loader(_CONFIGS["guarded"])
_true_reactive = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_true_reactive",
    _SOURCES["true_reactive"],
)
_true_reactive.load_true_reactive_config = _config_loader(_CONFIGS["true_reactive"])
_routing_core = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_core",
    _SOURCES["routing_core"],
)
_routing_core.load_core_config = _config_loader(_CONFIGS["routing_core"])
_routing_v3 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_v3",
    _SOURCES["routing_v3"],
)
_routing_v3.load_v3_config = _config_loader(_CONFIGS["routing_v3"])
_routing_v4 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_batched_cluster_routing_v4",
    _SOURCES["routing_v4"],
)
_routing_v4.load_v4_config = _config_loader(_CONFIGS["routing_v4"])


def create_agent(run_context=None):
    return _routing_v4.create_codex_e17_batched_cluster_routing_v4(
        run_context=run_context,
        config_path=_routing_v4.DEFAULT_V4D_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)


# E17.3 productive 6-6-2 topology overlay.  This intentionally replaces the
# default V4D entry point while retaining the hash-verified embedded provider.
_BASE_RELEASE_ID = RELEASE_ID
_BASE_BUILD_METADATA = BUILD_METADATA
RELEASE_ID = 'CODEX-E17.3-TOPOLOGY-FILL-662-KAGGLE-CANDIDATE-V2'
MODEL_SPEC_VERSION = 'CODEX-E17.3-TOPOLOGY-FILL-662-V2'
BUILD_METADATA = {'release_id': 'CODEX-E17.3-TOPOLOGY-FILL-662-KAGGLE-CANDIDATE-V2',
 'model_spec_version': 'CODEX-E17.3-TOPOLOGY-FILL-662-V2',
 'base_release_id': 'CODEX-E17.2-V4D-D28-KAGGLE-CANDIDATE-V1',
 'topology_source_sha256': '3B7A49FB29187D2E03F58F74E48A0D9A114C2C0E7112EB19908C303826D6315C',
 'topology_config_sha256': '0288AB878C7C9224A56B71E84158BDDDFDBE0CECC6D8EAE0F30093F985CEF50C',
 'pasture_targets_by_quadrant': {'Q0': 6, 'Q1': 6, 'Q2': 2},
 'q2_pasture_cap': 2,
 'pasture_fill_target': 14,
 'livestock_resource_cap': 15,
 'livestock_in_transit_buffer': 1,
 'reclaimed_crop_targets': 5,
 'q2_reclaimed_crop_targets': 3,
 'pasture_fill_control': True}
_TOPOLOGY_662_SOURCE = '"""Productive 6-6-2 topology overlay over Codex E17.2 V4D.\n\nThe overlay converts all five cells removed from the V4D 7-7-5 pasture layout\ninto crops, including the three reclaimed Q2 cells.  Reclaimed work is\ntranslated in place so V4D worker trajectories remain synchronized.  The\npasture census targets fourteen occupied structures and permits one in-transit\nlivestock resource while a removed Q0 placement returns to the shed.\n"""\n\nfrom __future__ import annotations\n\nimport json\nfrom collections import Counter\nfrom collections.abc import Callable\nfrom copy import deepcopy\nfrom pathlib import Path\nfrom typing import Any\n\nfrom _codex_bundle.agricola.core.state import CROPS\nfrom _codex_bundle.agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (\n    DEFAULT_V4D_CONFIG_PATH,\n    create_codex_e17_batched_cluster_routing_v4,\n)\n\nREPO_ROOT = Path(__file__).resolve().parents[4]\nDEFAULT_TOPOLOGY_662_CONFIG_PATH = (\n    REPO_ROOT\n    / "experiments/e17/configs/codex/CODEX_E17_3_TOPOLOGY_CAP_662_V1.json"\n)\nTOPOLOGY_662_MODEL_SPEC_VERSION = "CODEX-E17.3-TOPOLOGY-FILL-662-V2"\n_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}\n_PASTURE_LIVESTOCK = frozenset({"COW", "SHEEP"})\n_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})\n_ANIMAL_ONLY_SERVICES = frozenset(\n    {"FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE"}\n)\n\n\ndef _quadrant(position: tuple[int, int]) -> str:\n    x, y = position\n    if x < 5 and y < 5:\n        return "Q0"\n    if x >= 5 and y < 5:\n        return "Q1"\n    if x < 5 and y >= 5:\n        return "Q2"\n    return "Q3"\n\n\ndef load_topology_662_config(path: Path | str | None = None) -> dict[str, Any]:\n    """Load the explicit 6-6-2 topology and validate its hard caps."""\n\n    config_path = (\n        Path(path) if path is not None else DEFAULT_TOPOLOGY_662_CONFIG_PATH\n    )\n    config = json.loads(config_path.read_text(encoding="utf-8"))\n    expected = {\n        "candidate_id": "CODEX_E17_3_TOPOLOGY_FILL_662_V2",\n        "model_spec_version": TOPOLOGY_662_MODEL_SPEC_VERSION,\n        "base_policy": (\n            "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28"\n        ),\n        "causal_family": "RECLAIMED_CROP_AND_PASTURE_FILL_CONTROL",\n        "q2_pasture_cap": 2,\n        "allow_q2_zero_future_variant": True,\n    }\n    for key, value in expected.items():\n        if config.get(key) != value:\n            raise ValueError(f"unexpected {key}: {config.get(key)!r}")\n\n    targets = [tuple(value) for value in config.get("pasture_targets", [])]\n    if len(targets) != len(set(targets)):\n        raise ValueError("pasture targets must be unique")\n    counts = Counter(_quadrant(position) for position in targets)\n    declared = {\n        key: int(value)\n        for key, value in config.get("quadrant_pasture_caps", {}).items()\n    }\n    if declared != {"Q0": 6, "Q1": 6, "Q2": 2}:\n        raise ValueError(f"unexpected declared caps: {declared!r}")\n    if counts["Q0"] != 6 or counts["Q1"] != 6 or counts["Q3"]:\n        raise ValueError(f"topology violates the 6-6-Q2 envelope: {dict(counts)!r}")\n    if counts["Q2"] > int(config["q2_pasture_cap"]):\n        raise ValueError("Q2 pasture targets exceed the hard cap")\n    if int(config["pasture_fill_target"]) != len(targets):\n        raise ValueError("fill target must equal available pasture targets")\n    if int(config["pre_q2_livestock_resource_cap"]) != len(targets):\n        raise ValueError("the pre-Q2 livestock cap must equal the fill target")\n    if int(config["livestock_in_transit_buffer"]) != 1:\n        raise ValueError("the topology requires one in-transit livestock slot")\n    if int(config["livestock_resource_cap"]) != len(targets) + 1:\n        raise ValueError("livestock cap must include the in-transit buffer")\n    reclaimed = [\n        tuple(value) for value in config.get("reclaimed_crop_targets", [])\n    ]\n    blocked = [\n        tuple(value) for value in config.get("blocked_v4d_pasture_targets", [])\n    ]\n    q2_reclaimed = [\n        tuple(value)\n        for value in config.get("q2_reclaimed_crop_targets", [])\n    ]\n    if len(reclaimed) != 5 or len(reclaimed) != len(set(reclaimed)):\n        raise ValueError("exactly five unique V4D pasture cells must be reclaimed")\n    if set(reclaimed) != set(blocked):\n        raise ValueError("every blocked V4D pasture must become a crop target")\n    if set(reclaimed).intersection(targets):\n        raise ValueError("pasture and reclaimed crop targets must be disjoint")\n    if len(q2_reclaimed) != 3 or set(q2_reclaimed) != {\n        value for value in reclaimed if _quadrant(value) == "Q2"\n    }:\n        raise ValueError("the three reclaimed Q2 cells must be explicit")\n    crop_priority = list(config.get("reclaimed_crop_priority", []))\n    crop_cutoffs = config.get("reclaimed_crop_cutoffs", {}) or {}\n    if not crop_priority or any(crop not in CROPS for crop in crop_priority):\n        raise ValueError("reclaimed crop priority contains an unknown crop")\n    if any(int(crop_cutoffs.get(crop, -1)) < 0 for crop in crop_priority):\n        raise ValueError("every reclaimed crop requires a non-negative cutoff")\n    if crop_priority != [str(config.get("reclaimed_seed_backfill_crop"))]:\n        raise ValueError("reclaimed crops must use the dedicated seed backfill")\n    if int(config.get("reclaimed_seed_backfill_units", 0)) != len(reclaimed):\n        raise ValueError("seed backfill must cover every reclaimed crop target")\n    if int(config.get("pasture_fill_mission_worker_limit", 0)) <= 0:\n        raise ValueError("pasture fill mission requires at least one worker")\n    if list(config.get("pasture_fill_quadrant_priority", [])) != [\n        "Q1",\n        "Q2",\n        "Q0",\n    ]:\n        raise ValueError("fill priority must repair Q1 and Q2 before Q0")\n    return deepcopy(config)\n\n\ndef _farm(observation: dict[str, Any]) -> dict[str, Any]:\n    player = int(observation.get("player", 0))\n    farms = observation.get("farms", []) or []\n    return farms[player] if 0 <= player < len(farms) else {}\n\n\ndef _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:\n    return [\n        tuple(farm.get("farmer", [4, 4])),\n        *(tuple(position) for position in farm.get("hands", []) or []),\n    ]\n\n\ndef _inventories(private: dict[str, Any], count: int) -> list[dict[str, Any]]:\n    values = [\n        value if isinstance(value, dict) else {}\n        for value in (private.get("inventories", []) or [])\n    ]\n    values.extend({} for _ in range(max(0, count - len(values))))\n    return values[:count]\n\n\ndef _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:\n    x, y = position\n    rows = farm.get("tiles", []) or []\n    if not 0 <= y < len(rows) or not 0 <= x < len(rows[y]):\n        return "LOCKED"\n    return rows[y][x]\n\n\ndef _distance(source: tuple[int, int], target: tuple[int, int]) -> int:\n    return abs(source[0] - target[0]) + abs(source[1] - target[1])\n\n\ndef _move(source: tuple[int, int], target: tuple[int, int]) -> list[str]:\n    sx, sy = source\n    tx, ty = target\n    if sx < tx:\n        return ["EAST"]\n    if sx > tx:\n        return ["WEST"]\n    if sy < ty:\n        return ["SOUTH"]\n    if sy > ty:\n        return ["NORTH"]\n    return ["PASS"]\n\n\ndef _shed_access(board_size: int) -> tuple[tuple[int, int], ...]:\n    half = board_size // 2\n    return (\n        (half - 1, half - 1),\n        (half, half - 1),\n        (half - 1, half),\n        (half, half),\n    )\n\n\ndef _unit_actions(action: dict[str, Any], count: int) -> list[list[Any]]:\n    actions = [\n        list(action.get("farmer", ["PASS"]) or ["PASS"]),\n        *(list(value or ["PASS"]) for value in action.get("hands", []) or []),\n    ]\n    actions.extend(["PASS"] for _ in range(max(0, count - len(actions))))\n    return actions[:count]\n\n\ndef _store_unit_actions(action: dict[str, Any], actions: list[list[Any]]) -> None:\n    action["farmer"] = actions[0] if actions else ["PASS"]\n    action["hands"] = actions[1:]\n\n\ndef _pasture_livestock_resources(observation: dict[str, Any]) -> int:\n    """Count COW/SHEEP on tiles, in the shed, and in unit inventories."""\n\n    total = 0\n    farm = _farm(observation)\n    for row in farm.get("tiles", []) or []:\n        for tile in row:\n            if isinstance(tile, dict) and tile.get("animal") in _PASTURE_LIVESTOCK:\n                total += 1\n\n    private = observation.get("private", {}) or {}\n    shed = private.get("shed", {}) or {}\n    total += sum(max(0, int(shed.get(item, 0))) for item in _PASTURE_LIVESTOCK)\n    for inventory in private.get("inventories", []) or []:\n        if not isinstance(inventory, dict):\n            continue\n        total += sum(\n            max(0, int(inventory.get(item, 0))) for item in _PASTURE_LIVESTOCK\n        )\n    return total\n\n\nclass CodexE17TopologyCap662Agent:\n    """Reallocate removed pasture work to crops and fill all allowed pastures."""\n\n    def __init__(\n        self,\n        *,\n        run_context: dict[str, Any] | None = None,\n        config_path: Path | str | None = None,\n        base_policy: Callable[..., dict[str, Any]] | None = None,\n    ) -> None:\n        self.config = load_topology_662_config(config_path)\n        self.run_context = deepcopy(run_context or {})\n        self.base_policy = (\n            base_policy\n            if base_policy is not None\n            else create_codex_e17_batched_cluster_routing_v4(\n                run_context=self.run_context,\n                config_path=DEFAULT_V4D_CONFIG_PATH,\n            )\n        )\n        self.candidate_id = str(self.config["candidate_id"])\n        self.model_spec_version = TOPOLOGY_662_MODEL_SPEC_VERSION\n        self.pasture_targets = frozenset(\n            tuple(value) for value in self.config["pasture_targets"]\n        )\n        self.reclaimed_crop_targets = frozenset(\n            tuple(value) for value in self.config["reclaimed_crop_targets"]\n        )\n        target_counts = Counter(\n            _quadrant(position) for position in self.pasture_targets\n        )\n        self.target_pastures_by_quadrant = {\n            quadrant: int(target_counts[quadrant])\n            for quadrant in ("Q0", "Q1", "Q2")\n        }\n        self.q2_pasture_cap = int(self.config["q2_pasture_cap"])\n        self.livestock_resource_cap = int(self.config["livestock_resource_cap"])\n        self.fill_mission_workers: set[int] = set()\n        self.fill_mission_started = False\n        self.error_count = 0\n        self.fallback_count = 0\n        self.last_exception: str | None = None\n        self.observation_count = 0\n        self.override_batches = 0\n        self.blocked_builds: Counter[tuple[int, int]] = Counter()\n        self.blocked_placements: Counter[tuple[int, int]] = Counter()\n        self.clamped_animal_units: Counter[str] = Counter()\n        self.reclaimed_crop_actions: Counter[str] = Counter()\n        self.reassigned_blocked_worker_actions = 0\n        self.pasture_fill_route_actions = 0\n        self.pasture_fill_place_commands = 0\n        self.pasture_fill_pickup_commands = 0\n        self.pasture_fill_purchase_units: Counter[str] = Counter()\n        self.reclaimed_seed_backfill_requested = False\n        self.reclaimed_seed_backfill_units = 0\n        self.max_observed_q2_pastures = 0\n        self.max_active_reclaimed_crops = 0\n        self.latest_target_pastures_built = 0\n        self.latest_target_pastures_filled = 0\n        self.latest_empty_target_pastures = 0\n        self.topology_cap_breaches = 0\n\n    def _observe_topology(self, observation: dict[str, Any]) -> None:\n        farm = _farm(observation)\n        q2_pastures = 0\n        for y, row in enumerate(farm.get("tiles", []) or []):\n            for x, tile in enumerate(row):\n                if (\n                    x < 5\n                    and y >= 5\n                    and isinstance(tile, dict)\n                    and tile.get("kind") == "PASTURE"\n                ):\n                    q2_pastures += 1\n        self.max_observed_q2_pastures = max(\n            self.max_observed_q2_pastures, q2_pastures\n        )\n        if q2_pastures > self.q2_pasture_cap:\n            self.topology_cap_breaches += 1\n        target_tiles = [_tile(farm, target) for target in self.pasture_targets]\n        self.latest_target_pastures_built = sum(\n            isinstance(tile, dict) and tile.get("kind") == "PASTURE"\n            for tile in target_tiles\n        )\n        self.latest_target_pastures_filled = sum(\n            isinstance(tile, dict)\n            and tile.get("kind") == "PASTURE"\n            and tile.get("animal") in _PASTURE_LIVESTOCK\n            for tile in target_tiles\n        )\n        self.latest_empty_target_pastures = (\n            self.latest_target_pastures_built\n            - self.latest_target_pastures_filled\n        )\n        active_reclaimed = sum(\n            isinstance(_tile(farm, target), dict)\n            and _tile(farm, target).get("kind") == "PLANT"\n            for target in self.reclaimed_crop_targets\n        )\n        self.max_active_reclaimed_crops = max(\n            self.max_active_reclaimed_crops,\n            active_reclaimed,\n        )\n\n    def _filter_unit_actions(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n    ) -> set[int]:\n        farm = _farm(observation)\n        positions = _positions(farm)\n        unit_actions = _unit_actions(action, len(positions))\n        crop_tasks = {\n            target: command\n            for _priority, target, command in self._reclaimed_crop_tasks(\n                observation\n            )\n        }\n        claimed_crop_targets: set[tuple[int, int]] = set()\n        released: set[int] = set()\n        for index, command in enumerate(unit_actions):\n            if index >= len(positions) or not command:\n                continue\n            position = positions[index]\n            opcode = str(command[0])\n            blocked = False\n            if opcode == "BUILD_PASTURE" and position not in self.pasture_targets:\n                self.blocked_builds[position] += 1\n                blocked = True\n            elif (\n                opcode == "PLACE"\n                and len(command) >= 2\n                and str(command[1]) in _PASTURE_LIVESTOCK\n                and position not in self.pasture_targets\n            ):\n                self.blocked_placements[position] += 1\n                blocked = True\n            elif (\n                position in self.reclaimed_crop_targets\n                and opcode in _ANIMAL_ONLY_SERVICES\n            ):\n                blocked = True\n\n            desired_crop = crop_tasks.get(position)\n            if (\n                desired_crop is not None\n                and position not in claimed_crop_targets\n                and opcode not in _MOVES\n            ):\n                unit_actions[index] = list(desired_crop)\n                claimed_crop_targets.add(position)\n                self.reclaimed_crop_actions[str(desired_crop[0])] += 1\n                if blocked or opcode == "PASS":\n                    self.reassigned_blocked_worker_actions += 1\n                released.add(index)\n                continue\n\n            if not blocked:\n                continue\n            unit_actions[index] = ["PASS"]\n            released.add(index)\n        _store_unit_actions(action, unit_actions)\n        return released\n\n    def _empty_pastures(self, farm: dict[str, Any]) -> list[tuple[int, int]]:\n        priority = {\n            quadrant: rank\n            for rank, quadrant in enumerate(\n                self.config["pasture_fill_quadrant_priority"]\n            )\n        }\n        return sorted(\n            (\n                target\n                for target in self.pasture_targets\n                if isinstance((tile := _tile(farm, target)), dict)\n                and tile.get("kind") == "PASTURE"\n                and not tile.get("animal")\n            ),\n            key=lambda value: (priority[_quadrant(value)], value[1], value[0]),\n        )\n\n    def _route_pasture_fill(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n        eligible_workers: set[int] | None = None,\n    ) -> set[int]:\n        farm = _farm(observation)\n        private = observation.get("private", {}) or {}\n        positions = _positions(farm)\n        inventories = _inventories(private, len(positions))\n        actions = _unit_actions(action, len(positions))\n        empty = self._empty_pastures(farm)\n        assigned: set[int] = set()\n        reserved: set[tuple[int, int]] = set()\n        species_priority = list(self.config["pasture_fill_species_priority"])\n\n        carriers: list[tuple[int, str]] = []\n        carried_units = 0\n        for worker_id, inventory in enumerate(inventories):\n            for species in species_priority:\n                quantity = max(0, int(inventory.get(species, 0) or 0))\n                carried_units += quantity\n                if (\n                    quantity\n                    and (eligible_workers is None or worker_id in eligible_workers)\n                    and not any(value[0] == worker_id for value in carriers)\n                ):\n                    carriers.append((worker_id, species))\n\n        for worker_id, species in carriers:\n            candidates = [target for target in empty if target not in reserved]\n            if not candidates:\n                break\n            target = min(\n                candidates,\n                key=lambda value: (\n                    self.config["pasture_fill_quadrant_priority"].index(\n                        _quadrant(value)\n                    ),\n                    _distance(positions[worker_id], value),\n                    value,\n                ),\n            )\n            if positions[worker_id] == target:\n                actions[worker_id] = ["PLACE", species, 1]\n                self.pasture_fill_place_commands += 1\n            else:\n                actions[worker_id] = _move(positions[worker_id], target)\n                self.pasture_fill_route_actions += 1\n            assigned.add(worker_id)\n            reserved.add(target)\n\n        pickup_needed = max(0, len(empty) - carried_units)\n        if pickup_needed and int(observation.get("day", 0)) <= int(\n            self.config["fill_purchase_cutoff_day"]\n        ):\n            shed = private.get("shed", {}) or {}\n            free_workers = [\n                worker_id\n                for worker_id, command in enumerate(actions)\n                if worker_id not in assigned\n                and (eligible_workers is None or worker_id in eligible_workers)\n                and command\n                and (\n                    command[0] == "PASS"\n                    or eligible_workers is not None\n                )\n            ]\n            board_size = len(farm.get("tiles", []) or []) or 10\n            accesses = _shed_access(board_size)\n            for species in species_priority:\n                available = min(\n                    max(0, int(shed.get(species, 0) or 0)),\n                    pickup_needed,\n                )\n                for _ in range(available):\n                    if not free_workers:\n                        break\n                    worker_id = min(\n                        free_workers,\n                        key=lambda value: min(\n                            _distance(positions[value], access)\n                            for access in accesses\n                        ),\n                    )\n                    target = min(\n                        accesses,\n                        key=lambda value: (\n                            _distance(positions[worker_id], value),\n                            value,\n                        ),\n                    )\n                    actions[worker_id] = (\n                        ["PICKUP", species, 1]\n                        if positions[worker_id] == target\n                        else _move(positions[worker_id], target)\n                    )\n                    if positions[worker_id] == target:\n                        self.pasture_fill_pickup_commands += 1\n                    else:\n                        self.pasture_fill_route_actions += 1\n                    assigned.add(worker_id)\n                    free_workers.remove(worker_id)\n                    pickup_needed -= 1\n                if pickup_needed <= 0 or not free_workers:\n                    break\n        _store_unit_actions(action, actions)\n        return assigned\n\n    def _crop_choice(\n        self,\n        *,\n        day: int,\n        seeds: Counter[str],\n    ) -> str | None:\n        cutoffs = self.config["reclaimed_crop_cutoffs"]\n        for crop in self.config["reclaimed_crop_priority"]:\n            if day <= int(cutoffs[crop]) and seeds[crop] > 0:\n                seeds[crop] -= 1\n                return str(crop)\n        return None\n\n    def _reclaimed_crop_tasks(\n        self,\n        observation: dict[str, Any],\n    ) -> list[tuple[int, tuple[int, int], list[Any]]]:\n        farm = _farm(observation)\n        private = observation.get("private", {}) or {}\n        day = int(observation.get("day", 0))\n        if (\n            day < int(self.config["reclaimed_crop_activation_day"])\n            or not self.reclaimed_seed_backfill_requested\n        ):\n            return []\n        seeds = Counter(private.get("seeds", {}) or {})\n        tasks: list[tuple[int, tuple[int, int], list[Any]]] = []\n        for target in sorted(self.reclaimed_crop_targets, key=lambda p: (p[1], p[0])):\n            tile = _tile(farm, target)\n            if tile == "LOCKED":\n                continue\n            if tile is None:\n                crop = self._crop_choice(day=day, seeds=seeds)\n                if crop is not None:\n                    tasks.append((3, target, ["PLANT", crop]))\n                continue\n            if not isinstance(tile, dict):\n                continue\n            if tile.get("kind") == "WEED":\n                tasks.append((2, target, ["DIG"]))\n                continue\n            if tile.get("kind") != "PLANT":\n                continue\n            crop = str(tile.get("crop", ""))\n            mature = day - int(tile.get("planted_day", day)) >= int(\n                CROPS.get(crop, {}).get("first_yield_day", 10**6)\n            )\n            if mature and int(tile.get("yield_units", 0) or 0) > 0:\n                tasks.append((0, target, ["HARVEST"]))\n            elif day < 29 and not bool(tile.get("watered_today", False)):\n                tasks.append((1, target, ["WATER"]))\n        return tasks\n\n    def _service_reclaimed_crops(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n        unavailable_workers: set[int],\n        eligible_workers: set[int] | None = None,\n    ) -> None:\n        farm = _farm(observation)\n        positions = _positions(farm)\n        actions = _unit_actions(action, len(positions))\n        tasks = self._reclaimed_crop_tasks(observation)\n\n        remaining: list[tuple[int, tuple[int, int], list[Any]]] = []\n        for task in tasks:\n            _priority, target, command = task\n            fulfilled = any(\n                worker_id not in unavailable_workers\n                and positions[worker_id] == target\n                and actions[worker_id]\n                and actions[worker_id][0] == command[0]\n                for worker_id in range(len(positions))\n            )\n            if not fulfilled:\n                remaining.append(task)\n\n        free_workers = {\n            worker_id\n            for worker_id, command in enumerate(actions)\n            if worker_id not in unavailable_workers\n            and (eligible_workers is None or worker_id in eligible_workers)\n            and command\n            and (command[0] == "PASS" or eligible_workers is not None)\n        }\n        for _priority, target, command in sorted(\n            remaining,\n            key=lambda value: (value[0], value[1][1], value[1][0]),\n        ):\n            if not free_workers:\n                break\n            worker_id = min(\n                free_workers,\n                key=lambda value: (\n                    _distance(positions[value], target),\n                    value,\n                ),\n            )\n            actions[worker_id] = (\n                command if positions[worker_id] == target else _move(positions[worker_id], target)\n            )\n            if positions[worker_id] == target:\n                self.reclaimed_crop_actions[str(command[0])] += 1\n            else:\n                self.reclaimed_crop_actions[str(actions[worker_id][0])] += 1\n            free_workers.remove(worker_id)\n        _store_unit_actions(action, actions)\n\n    def _filter_market(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n    ) -> None:\n        unlocked = len(_farm(observation).get("unlocked_quadrants", []) or [])\n        effective_cap = (\n            self.livestock_resource_cap\n            if unlocked >= 3\n            else int(self.config["pre_q2_livestock_resource_cap"])\n        )\n        remaining = max(\n            0,\n            effective_cap - _pasture_livestock_resources(observation),\n        )\n        rebuilt: list[Any] = []\n        for order in action.get("market", []) or []:\n            if not (\n                isinstance(order, list)\n                and len(order) >= 3\n                and order[0] == "BUY_ANIMAL"\n                and str(order[1]) in _PASTURE_LIVESTOCK\n            ):\n                rebuilt.append(order)\n                continue\n            requested = max(0, int(order[2]))\n            admitted = min(requested, remaining)\n            remaining -= admitted\n            if admitted:\n                rebuilt.append([*order[:2], admitted, *order[3:]])\n            if admitted < requested:\n                self.clamped_animal_units[str(order[1])] += requested - admitted\n        action["market"] = rebuilt\n\n    def _backfill_livestock_market(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n        configuration: Any,\n    ) -> None:\n        day = int(observation.get("day", 0))\n        if day > int(self.config["fill_purchase_cutoff_day"]):\n            return\n        farm = _farm(observation)\n        if len(farm.get("unlocked_quadrants", []) or []) < 3:\n            return\n        built = sum(\n            isinstance(_tile(farm, target), dict)\n            and _tile(farm, target).get("kind") == "PASTURE"\n            for target in self.pasture_targets\n        )\n        resources = _pasture_livestock_resources(observation)\n        planned = sum(\n            max(0, int(order[2]))\n            for order in action.get("market", []) or []\n            if isinstance(order, list)\n            and len(order) >= 3\n            and order[0] == "BUY_ANIMAL"\n            and str(order[1]) in _PASTURE_LIVESTOCK\n        )\n        shortage = max(0, min(built, self.livestock_resource_cap) - resources - planned)\n        if shortage <= 0:\n            return\n        max_orders = (\n            int(configuration.get("maxMarketOrdersPerTurn", 10))\n            if isinstance(configuration, dict)\n            else int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)\n        )\n        if len(action.get("market", []) or []) >= max_orders:\n            return\n        money = float(farm.get("money", 0.0) or 0.0)\n        floor = float(self.config["fill_operating_cash_floor"])\n        for species in self.config["pasture_fill_species_priority"]:\n            cost = max(1.0, float(self.config["animal_costs"][species]))\n            affordable = max(0, int((money - floor) // cost))\n            quantity = min(shortage, affordable)\n            if quantity <= 0:\n                continue\n            action.setdefault("market", []).append(\n                ["BUY_ANIMAL", str(species), quantity]\n            )\n            self.pasture_fill_purchase_units[str(species)] += quantity\n            break\n\n    def _backfill_reclaimed_seed_market(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n        configuration: Any,\n    ) -> None:\n        if self.reclaimed_seed_backfill_requested or int(\n            observation.get("day", 0)\n        ) < int(self.config["reclaimed_crop_activation_day"]):\n            return\n        farm = _farm(observation)\n        max_orders = (\n            int(configuration.get("maxMarketOrdersPerTurn", 10))\n            if isinstance(configuration, dict)\n            else int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)\n        )\n        if len(action.get("market", []) or []) >= max_orders:\n            return\n        units = int(self.config["reclaimed_seed_backfill_units"])\n        cost = float(self.config["reclaimed_seed_unit_cost"])\n        floor = float(self.config["reclaimed_seed_operating_cash_floor"])\n        money = float(farm.get("money", 0.0) or 0.0)\n        if money < floor + units * cost:\n            return\n        action.setdefault("market", []).append(\n            ["BUY_SEED", str(self.config["reclaimed_seed_backfill_crop"]), units]\n        )\n        self.reclaimed_seed_backfill_requested = True\n        self.reclaimed_seed_backfill_units += units\n\n    def _activate_fill_mission(self, observation: dict[str, Any]) -> None:\n        if self.fill_mission_started or int(observation.get("day", 0)) != int(\n            self.config["pasture_fill_mission_day"]\n        ):\n            return\n        farm = _farm(observation)\n        if len(farm.get("unlocked_quadrants", []) or []) < 3:\n            return\n        positions = _positions(farm)\n        accesses = set(_shed_access(len(farm.get("tiles", []) or []) or 10))\n        candidates = [\n            worker_id\n            for worker_id, position in enumerate(positions)\n            if position in accesses\n        ]\n        limit = min(\n            int(self.config["pasture_fill_mission_worker_limit"]),\n            len(self._empty_pastures(farm)),\n        )\n        self.fill_mission_workers = set(candidates[:limit])\n        self.fill_mission_started = bool(self.fill_mission_workers)\n\n    def __call__(\n        self,\n        observation: dict[str, Any],\n        configuration: Any = None,\n    ) -> dict[str, Any]:\n        self._observe_topology(observation)\n        provider = self.base_policy(observation, configuration)\n        action = deepcopy(provider)\n        self._filter_unit_actions(action, observation)\n        self._filter_market(action, observation)\n        self._backfill_livestock_market(action, observation, configuration)\n        self._backfill_reclaimed_seed_market(\n            action,\n            observation,\n            configuration,\n        )\n        self._activate_fill_mission(observation)\n        if (\n            self.fill_mission_workers\n            and int(observation.get("day", 0))\n            == int(self.config["pasture_fill_mission_day"])\n        ):\n            actions = _unit_actions(action, len(_positions(_farm(observation))))\n            for worker_id in self.fill_mission_workers:\n                if worker_id < len(actions):\n                    actions[worker_id] = ["PASS"]\n            _store_unit_actions(action, actions)\n            fill_workers = self._route_pasture_fill(\n                action,\n                observation,\n                eligible_workers=self.fill_mission_workers,\n            )\n            self._service_reclaimed_crops(\n                action,\n                observation,\n                unavailable_workers=fill_workers,\n                eligible_workers=self.fill_mission_workers,\n            )\n        self.observation_count += 1\n        if action != provider:\n            self.override_batches += 1\n        return action\n\n    def telemetry_snapshot(self) -> dict[str, Any]:\n        base_instance = getattr(\n            self.base_policy,\n            "codex_e17_batched_cluster_routing_instance",\n            None,\n        )\n        base = (\n            base_instance.telemetry_snapshot()\n            if base_instance is not None\n            else {}\n        )\n        return {\n            "agent_version": self.model_spec_version,\n            "candidate_id": self.candidate_id,\n            "base_agent_version": base.get("agent_version"),\n            "target_pastures_by_quadrant": self.target_pastures_by_quadrant,\n            "q2_pasture_cap": self.q2_pasture_cap,\n            "livestock_resource_cap": self.livestock_resource_cap,\n            "reclaimed_crop_targets": [\n                list(position) for position in sorted(self.reclaimed_crop_targets)\n            ],\n            "override_batches": self.override_batches,\n            "blocked_builds": {\n                str(position): count for position, count in self.blocked_builds.items()\n            },\n            "blocked_placements": {\n                str(position): count\n                for position, count in self.blocked_placements.items()\n            },\n            "clamped_animal_units": dict(self.clamped_animal_units),\n            "reclaimed_crop_actions": dict(self.reclaimed_crop_actions),\n            "reassigned_blocked_worker_actions": (\n                self.reassigned_blocked_worker_actions\n            ),\n            "fill_mission_workers": sorted(self.fill_mission_workers),\n            "fill_mission_started": self.fill_mission_started,\n            "pasture_fill_route_actions": self.pasture_fill_route_actions,\n            "pasture_fill_place_commands": self.pasture_fill_place_commands,\n            "pasture_fill_pickup_commands": self.pasture_fill_pickup_commands,\n            "pasture_fill_purchase_units": dict(\n                self.pasture_fill_purchase_units\n            ),\n            "reclaimed_seed_backfill_requested": (\n                self.reclaimed_seed_backfill_requested\n            ),\n            "reclaimed_seed_backfill_units": self.reclaimed_seed_backfill_units,\n            "max_active_reclaimed_crops": self.max_active_reclaimed_crops,\n            "latest_target_pastures_built": self.latest_target_pastures_built,\n            "latest_target_pastures_filled": self.latest_target_pastures_filled,\n            "latest_empty_target_pastures": self.latest_empty_target_pastures,\n            "max_observed_q2_pastures": self.max_observed_q2_pastures,\n            "topology_cap_breaches": self.topology_cap_breaches,\n            "provider": base,\n        }\n\n\ndef create_codex_e17_topology_cap_662(\n    run_context: dict[str, Any] | None = None,\n    config_path: Path | str | None = None,\n    base_policy: Callable[..., dict[str, Any]] | None = None,\n):\n    """Create the fail-closed productive 6-6-2 Kaggle candidate."""\n\n    instance = CodexE17TopologyCap662Agent(\n        run_context=run_context,\n        config_path=config_path,\n        base_policy=base_policy,\n    )\n\n    def policy(\n        observation: dict[str, Any],\n        configuration: Any = None,\n    ) -> dict[str, Any]:\n        try:\n            action = instance(observation, configuration)\n            policy.codex_e17_topology_662_last_error = None\n            return action\n        except (KeyboardInterrupt, SystemExit):\n            raise\n        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary\n            instance.error_count += 1\n            instance.fallback_count += 1\n            instance.last_exception = f"{type(exc).__name__}: {exc}"\n            policy.codex_e17_topology_662_last_error = instance.last_exception\n            return deepcopy(_SAFE_PASS)\n\n    policy.codex_e17_topology_662_instance = instance\n    policy.codex_e17_topology_662_last_error = None\n    policy.__name__ = "codex_e17_3_topology_fill_662_policy"\n    return policy\n\n\n__all__ = [\n    "DEFAULT_TOPOLOGY_662_CONFIG_PATH",\n    "TOPOLOGY_662_MODEL_SPEC_VERSION",\n    "CodexE17TopologyCap662Agent",\n    "create_codex_e17_topology_cap_662",\n    "load_topology_662_config",\n]\n'
_TOPOLOGY_662_CONFIG = {'candidate_id': 'CODEX_E17_3_TOPOLOGY_FILL_662_V2',
 'schema_version': 'e17.codex.topology_fill_662.v2',
 'model_spec_version': 'CODEX-E17.3-TOPOLOGY-FILL-662-V2',
 'base_policy': 'CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28',
 'causal_family': 'RECLAIMED_CROP_AND_PASTURE_FILL_CONTROL',
 'quadrant_pasture_caps': {'Q0': 6, 'Q1': 6, 'Q2': 2},
 'q2_pasture_cap': 2,
 'pasture_fill_target': 14,
 'pre_q2_livestock_resource_cap': 14,
 'livestock_in_transit_buffer': 1,
 'livestock_resource_cap': 15,
 'pasture_targets': [[4, 2],
                     [3, 3],
                     [4, 3],
                     [2, 4],
                     [3, 4],
                     [4, 4],
                     [5, 2],
                     [5, 3],
                     [6, 3],
                     [5, 4],
                     [6, 4],
                     [7, 4],
                     [3, 5],
                     [4, 5]],
 'blocked_v4d_pasture_targets': [[3, 2], [6, 2], [3, 6], [4, 6], [4, 7]],
 'reclaimed_crop_targets': [[3, 2], [6, 2], [3, 6], [4, 6], [4, 7]],
 'q2_reclaimed_crop_targets': [[3, 6], [4, 6], [4, 7]],
 'reclaimed_crop_priority': ['STRAWBERRY'],
 'reclaimed_crop_cutoffs': {'STRAWBERRY': 18},
 'reclaimed_crop_activation_day': 11,
 'reclaimed_seed_backfill_crop': 'STRAWBERRY',
 'reclaimed_seed_backfill_units': 5,
 'reclaimed_seed_unit_cost': 100,
 'reclaimed_seed_operating_cash_floor': 500,
 'pasture_fill_mission_day': 12,
 'pasture_fill_mission_worker_limit': 2,
 'pasture_fill_quadrant_priority': ['Q1', 'Q2', 'Q0'],
 'pasture_fill_species_priority': ['SHEEP', 'COW'],
 'fill_purchase_cutoff_day': 26,
 'fill_operating_cash_floor': 500,
 'animal_costs': {'SHEEP': 500, 'COW': 400},
 'allow_q2_zero_future_variant': True,
 'released_worker_limit': 0,
 'released_worker_handoff_day': 28}

_topology_662 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_topology_cap_662",
    _TOPOLOGY_662_SOURCE,
)
_topology_662.load_topology_662_config = _config_loader(_TOPOLOGY_662_CONFIG)


def create_agent(run_context=None):
    return _topology_662.create_codex_e17_topology_cap_662(
        run_context=run_context,
        config_path=_topology_662.DEFAULT_TOPOLOGY_662_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)

# E18.1 public-opponent-reactive topology overlay.  This replaces the E17.3
# entry point while retaining its hash-verified embedded provider.
_E18_BASE_RELEASE_ID = RELEASE_ID
_E18_BASE_BUILD_METADATA = BUILD_METADATA
RELEASE_ID = "CODEX-E18.1-OPPONENT-REACTIVE-662-770-KAGGLE-V1"
MODEL_SPEC_VERSION = "CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1"
BUILD_METADATA = {
    "release_id": RELEASE_ID,
    "model_spec_version": MODEL_SPEC_VERSION,
    "base_release_id": _E18_BASE_RELEASE_ID,
    "source_sha256": "E52C0E41524DDD5DB8CFB28B2A6D1D4230FF06F7F382D8EF2B672627B02C4569",
    "config_sha256": "878858D344C25B255199FE80839253F2386421085525812413C70FB5AC755E36",
    "decision_day": 6,
    "topology_modes": ["6-6-2", "7-7-0"],
    "public_opponent_features_only": True,
    "cross_episode_memory": False,
    "pasture_fill_target": 14,
    "livestock_resource_cap": 14,
    "high_pressure_placement_release_day": 28,
}
_E18_SOURCE = '"""Opponent-aware E18 topology overlay over the productive E17 6-6-2 agent.\n\nThe controller reads only the opponent\'s public farm.  At a preregistered\ncheckpoint it freezes one of two fourteen-pasture layouts: 6-6-2 for a\nconservative opponent and 7-7-0 for visible expansion/crop pressure.  The\ndecision is episode-local and does not use names, ratings, replay IDs, seeds,\nprivate inventories, or cross-episode state.\n"""\n\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nfrom collections import Counter\nfrom copy import deepcopy\nfrom pathlib import Path\nfrom typing import Any\n\nfrom _codex_bundle.agricola.strategy.codex.codex_e17_topology_cap_662 import (\n    _PASTURE_LIVESTOCK,\n    _SAFE_PASS,\n    DEFAULT_TOPOLOGY_662_CONFIG_PATH,\n    CodexE17TopologyCap662Agent,\n    _distance,\n    _farm,\n    _move,\n    _positions,\n    _quadrant,\n    _store_unit_actions,\n    _tile,\n    _unit_actions,\n)\n\nREPO_ROOT = Path(__file__).resolve().parents[4]\nDEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH = (\n    REPO_ROOT\n    / "experiments/e18/configs/codex/"\n    / "CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1.json"\n)\nE18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION = (\n    "CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1"\n)\n_TOPOLOGY_MODES = frozenset({"6-6-2", "7-7-0"})\n\n\ndef _public_opponent_farm(observation: dict[str, Any]) -> dict[str, Any]:\n    """Return the other seat\'s public farm without touching private state."""\n\n    player = int(observation.get("player", 0))\n    farms = observation.get("farms", []) or []\n    opponent = 1 - player\n    if 0 <= opponent < len(farms) and isinstance(farms[opponent], dict):\n        return farms[opponent]\n    return {}\n\n\ndef _positions_from(values: list[list[int]]) -> frozenset[tuple[int, int]]:\n    return frozenset(tuple(value) for value in values)\n\n\ndef load_e18_opponent_reactive_config(\n    path: Path | str | None = None,\n) -> dict[str, Any]:\n    config_path = (\n        Path(path)\n        if path is not None\n        else DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH\n    )\n    config = json.loads(config_path.read_text(encoding="utf-8"))\n    expected = {\n        "candidate_id": "CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1",\n        "model_spec_version": E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION,\n        "base_candidate_id": "CODEX_E17_3_TOPOLOGY_FILL_662_V2",\n        "causal_family": "PUBLIC_OPPONENT_REGIME_AND_DYNAMIC_TOPOLOGY_CONTROL",\n        "mode_below_threshold": "6-6-2",\n        "mode_at_or_above_threshold": "7-7-0",\n        "public_features_only": True,\n        "cross_episode_memory": False,\n        "holdout_consumed": False,\n        "final_confirmation_consumed": False,\n    }\n    for key, value in expected.items():\n        if config.get(key) != value:\n            raise ValueError(f"unexpected {key}: {config.get(key)!r}")\n    if int(config.get("decision_day", -1)) < 1:\n        raise ValueError("decision_day must be positive")\n    if int(config.get("dynamic_build_worker_limit", 0)) < 1:\n        raise ValueError("dynamic build routing requires at least one worker")\n    if int(config.get("livestock_resource_cap", 0)) != 14:\n        raise ValueError("E18 must cap livestock resources at fourteen")\n    if tuple(config.get("delayed_placement_target", [])) != (2, 4):\n        raise ValueError("the service-risk pasture must remain explicit")\n    if int(config.get("high_pressure_placement_release_day", -1)) != 28:\n        raise ValueError("the high-pressure placement release must remain D28")\n    if int(config.get("fill_purchase_cutoff_day", -1)) not in range(12, 30):\n        raise ValueError("fill_purchase_cutoff_day must be in the service window")\n    weights = config.get("pressure_weights", {}) or {}\n    if set(weights) != {\n        "extra_quadrants",\n        "crops",\n        "hands",\n        "animals",\n        "pastures",\n        "weeds",\n    }:\n        raise ValueError("pressure weights do not match the public feature set")\n    topologies = config.get("topologies", {}) or {}\n    if set(topologies) != _TOPOLOGY_MODES:\n        raise ValueError("both 6-6-2 and 7-7-0 must be configured")\n    all_targets: dict[str, frozenset[tuple[int, int]]] = {}\n    all_reclaimed: dict[str, frozenset[tuple[int, int]]] = {}\n    for mode in sorted(_TOPOLOGY_MODES):\n        payload = topologies[mode]\n        targets = _positions_from(payload.get("pasture_targets", []))\n        reclaimed = _positions_from(payload.get("reclaimed_crop_targets", []))\n        counts = Counter(_quadrant(position) for position in targets)\n        declared = {\n            key: int(value)\n            for key, value in payload.get("quadrant_pasture_caps", {}).items()\n        }\n        if len(targets) != 14 or counts["Q3"]:\n            raise ValueError(f"{mode} must define fourteen non-Q3 pastures")\n        if declared != {key: counts[key] for key in ("Q0", "Q1", "Q2")}:\n            raise ValueError(f"{mode} declared caps do not match its targets")\n        if mode != f"{counts[\'Q0\']}-{counts[\'Q1\']}-{counts[\'Q2\']}":\n            raise ValueError(f"{mode} name does not match its topology")\n        if len(reclaimed) != 5 or targets.intersection(reclaimed):\n            raise ValueError(f"{mode} must reclaim five disjoint crop cells")\n        all_targets[mode] = targets\n        all_reclaimed[mode] = reclaimed\n    dynamic = _positions_from(config.get("dynamic_cells", []))\n    if dynamic != all_targets["6-6-2"].symmetric_difference(\n        all_targets["7-7-0"]\n    ):\n        raise ValueError("dynamic_cells must be the topology target difference")\n    if all_targets["6-6-2"].union(all_reclaimed["6-6-2"]) != (\n        all_targets["7-7-0"].union(all_reclaimed["7-7-0"])\n    ):\n        raise ValueError("the two modes must partition the same V4D cells")\n    return deepcopy(config)\n\n\ndef _public_feature_snapshot(farm: dict[str, Any]) -> dict[str, int | float]:\n    counts: Counter[str] = Counter()\n    for row in farm.get("tiles", []) or []:\n        for tile in row:\n            if not isinstance(tile, dict):\n                continue\n            if tile.get("animal"):\n                counts["animals"] += 1\n            kind = str(tile.get("kind", ""))\n            if kind == "PLANT":\n                counts["crops"] += 1\n            elif kind == "PASTURE":\n                counts["pastures"] += 1\n            elif kind == "WEED":\n                counts["weeds"] += 1\n    return {\n        "quadrants": len(farm.get("unlocked_quadrants", []) or []),\n        "hands": len(farm.get("hands", []) or []),\n        "crops": counts["crops"],\n        "animals": counts["animals"],\n        "pastures": counts["pastures"],\n        "weeds": counts["weeds"],\n        "money": float(farm.get("money", 0.0) or 0.0),\n    }\n\n\nclass CodexE18OpponentReactiveTopologyAgent(CodexE17TopologyCap662Agent):\n    """Freeze a 6-6-2 or 7-7-0 layout from live public opponent pressure."""\n\n    def __init__(\n        self,\n        *,\n        run_context: dict[str, Any] | None = None,\n        config_path: Path | str | None = None,\n        base_policy=None,\n    ) -> None:\n        super().__init__(\n            run_context=run_context,\n            config_path=DEFAULT_TOPOLOGY_662_CONFIG_PATH,\n            base_policy=base_policy,\n        )\n        self.e18_config = load_e18_opponent_reactive_config(config_path)\n        self.candidate_id = str(self.e18_config["candidate_id"])\n        self.model_spec_version = E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION\n        self.config["fill_purchase_cutoff_day"] = int(\n            self.e18_config["fill_purchase_cutoff_day"]\n        )\n        self.livestock_resource_cap = int(\n            self.e18_config["livestock_resource_cap"]\n        )\n        self.config["pre_q2_livestock_resource_cap"] = self.livestock_resource_cap\n        self.topology_mode: str | None = None\n        self.mode_decision_day: int | None = None\n        self.mode_decision_pressure: float | None = None\n        self.mode_decision_features: dict[str, int | float] | None = None\n        self.mode_decisions = 0\n        self.dynamic_build_route_actions = 0\n        self.dynamic_build_commands = 0\n        self.persistent_fill_batches = 0\n        self.delayed_livestock_placements = 0\n        self.regime_observations: Counter[str] = Counter()\n        self.regime_transitions: list[dict[str, Any]] = []\n        self.opponent_feature_hashes: set[str] = set()\n        self.last_regime: str | None = None\n        self.last_observed_opponent_day: int | None = None\n        self.latest_opponent_features: dict[str, int | float] = {}\n\n        common = self._targets("6-6-2").intersection(self._targets("7-7-0"))\n        static_reclaimed = self._reclaimed("6-6-2").intersection(\n            self._reclaimed("7-7-0")\n        )\n        self._apply_targets(common, static_reclaimed, q2_cap=0)\n\n    def _targets(self, mode: str) -> frozenset[tuple[int, int]]:\n        return _positions_from(\n            self.e18_config["topologies"][mode]["pasture_targets"]\n        )\n\n    def _reclaimed(self, mode: str) -> frozenset[tuple[int, int]]:\n        return _positions_from(\n            self.e18_config["topologies"][mode]["reclaimed_crop_targets"]\n        )\n\n    def _apply_targets(\n        self,\n        targets: frozenset[tuple[int, int]],\n        reclaimed: frozenset[tuple[int, int]],\n        *,\n        q2_cap: int,\n    ) -> None:\n        self.pasture_targets = targets\n        self.reclaimed_crop_targets = reclaimed\n        counts = Counter(_quadrant(position) for position in targets)\n        self.target_pastures_by_quadrant = {\n            quadrant: counts[quadrant] for quadrant in ("Q0", "Q1", "Q2")\n        }\n        self.q2_pasture_cap = q2_cap\n\n    def _pressure(self, features: dict[str, int | float]) -> float:\n        weights = self.e18_config["pressure_weights"]\n        return (\n            max(0, int(features["quadrants"]) - 1)\n            * float(weights["extra_quadrants"])\n            + int(features["crops"]) * float(weights["crops"])\n            + int(features["hands"]) * float(weights["hands"])\n            + int(features["animals"]) * float(weights["animals"])\n            + int(features["pastures"]) * float(weights["pastures"])\n            + int(features["weeds"]) * float(weights["weeds"])\n        )\n\n    @staticmethod\n    def _regime(features: dict[str, int | float]) -> str:\n        if int(features["quadrants"]) >= 3 or int(features["crops"]) >= 20:\n            return "EXPANSION_CROP_PRESSURE"\n        if (\n            int(features["quadrants"]) >= 2\n            or int(features["crops"]) >= 8\n            or int(features["hands"]) >= 4\n        ):\n            return "DEVELOPING"\n        return "CONSERVATIVE"\n\n    def _observe_public_opponent(self, observation: dict[str, Any]) -> None:\n        day = int(observation.get("day", 0))\n        if day == self.last_observed_opponent_day:\n            return\n        features = _public_feature_snapshot(_public_opponent_farm(observation))\n        regime = self._regime(features)\n        payload = json.dumps(features, sort_keys=True, separators=(",", ":"))\n        feature_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()\n        self.opponent_feature_hashes.add(feature_hash)\n        self.regime_observations[regime] += 1\n        if regime != self.last_regime:\n            self.regime_transitions.append(\n                {"day": day, "from": self.last_regime, "to": regime}\n            )\n            self.last_regime = regime\n        self.latest_opponent_features = features\n        self.last_observed_opponent_day = day\n\n    def _maybe_decide(self, observation: dict[str, Any]) -> None:\n        if self.topology_mode is not None:\n            return\n        day = int(observation.get("day", 0))\n        if day < int(self.e18_config["decision_day"]):\n            return\n        features = deepcopy(self.latest_opponent_features)\n        pressure = self._pressure(features)\n        threshold = float(self.e18_config["expansion_pressure_threshold"])\n        mode = str(\n            self.e18_config[\n                "mode_at_or_above_threshold"\n                if pressure >= threshold\n                else "mode_below_threshold"\n            ]\n        )\n        targets = self._targets(mode)\n        reclaimed = self._reclaimed(mode)\n        q2_cap = int(\n            self.e18_config["topologies"][mode]["quadrant_pasture_caps"]["Q2"]\n        )\n        self._apply_targets(targets, reclaimed, q2_cap=q2_cap)\n        self.topology_mode = mode\n        self.mode_decision_day = day\n        self.mode_decision_pressure = pressure\n        self.mode_decision_features = features\n        self.mode_decisions += 1\n\n    def _route_dynamic_pasture_builds(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n        released: set[int],\n    ) -> None:\n        if self.topology_mode is None:\n            return\n        farm = _farm(observation)\n        positions = _positions(farm)\n        actions = _unit_actions(action, len(positions))\n        dynamic = _positions_from(self.e18_config["dynamic_cells"])\n        missing = [\n            target\n            for target in sorted(self.pasture_targets.intersection(dynamic))\n            if _tile(farm, target) is None\n        ]\n        if not missing:\n            return\n        reserved = {\n            positions[index]\n            for index, command in enumerate(actions)\n            if index < len(positions)\n            and command\n            and command[0] == "BUILD_PASTURE"\n            and positions[index] in missing\n        }\n        free = [\n            index\n            for index, command in enumerate(actions)\n            if index not in released\n            and command\n            and command[0] == "PASS"\n        ]\n        free.extend(sorted(released - set(free)))\n        limit = int(self.e18_config["dynamic_build_worker_limit"])\n        used = 0\n        for target in missing:\n            if target in reserved or not free or used >= limit:\n                continue\n            worker_id = min(\n                free,\n                key=lambda value: (_distance(positions[value], target), value),\n            )\n            actions[worker_id] = (\n                ["BUILD_PASTURE"]\n                if positions[worker_id] == target\n                else _move(positions[worker_id], target)\n            )\n            if positions[worker_id] == target:\n                self.dynamic_build_commands += 1\n            else:\n                self.dynamic_build_route_actions += 1\n            free.remove(worker_id)\n            reserved.add(target)\n            used += 1\n        _store_unit_actions(action, actions)\n\n    def _filter_unit_actions(\n        self,\n        action: dict[str, Any],\n        observation: dict[str, Any],\n    ) -> set[int]:\n        released = super()._filter_unit_actions(action, observation)\n        target = tuple(self.e18_config["delayed_placement_target"])\n        day = int(observation.get("day", 0))\n        should_delay = self.topology_mode is None or (\n            self.topology_mode == "7-7-0"\n            and day\n            < int(self.e18_config["high_pressure_placement_release_day"])\n        )\n        if should_delay:\n            positions = _positions(_farm(observation))\n            actions = _unit_actions(action, len(positions))\n            for worker_id, command in enumerate(actions):\n                if (\n                    positions[worker_id] == target\n                    and command\n                    and command[0] == "PLACE"\n                    and len(command) >= 2\n                    and str(command[1]) in _PASTURE_LIVESTOCK\n                ):\n                    actions[worker_id] = ["PASS"]\n                    released.add(worker_id)\n                    self.delayed_livestock_placements += 1\n            _store_unit_actions(action, actions)\n        self._route_dynamic_pasture_builds(action, observation, released)\n        return released\n\n    def _empty_pastures(\n        self,\n        farm: dict[str, Any],\n    ) -> list[tuple[int, int]]:\n        empty = super()._empty_pastures(farm)\n        target = tuple(self.e18_config["delayed_placement_target"])\n        day = self.last_observed_opponent_day or 0\n        should_delay = self.topology_mode is None or (\n            self.topology_mode == "7-7-0"\n            and day\n            < int(self.e18_config["high_pressure_placement_release_day"])\n        )\n        return [position for position in empty if not (should_delay and position == target)]\n\n    def __call__(\n        self,\n        observation: dict[str, Any],\n        configuration: Any = None,\n    ) -> dict[str, Any]:\n        self._observe_public_opponent(observation)\n        self._maybe_decide(observation)\n        action = super().__call__(observation, configuration)\n        day = int(observation.get("day", 0))\n        if 12 <= day <= int(self.config["fill_purchase_cutoff_day"]):\n            actions = _unit_actions(action, len(_positions(_farm(observation))))\n            eligible = {\n                worker_id\n                for worker_id, command in enumerate(actions)\n                if command and command[0] == "PASS"\n            }\n            if eligible:\n                before = deepcopy(action)\n                self._route_pasture_fill(\n                    action,\n                    observation,\n                    eligible_workers=eligible,\n                )\n                if action != before:\n                    self.persistent_fill_batches += 1\n        return action\n\n    def telemetry_snapshot(self) -> dict[str, Any]:\n        telemetry = super().telemetry_snapshot()\n        telemetry.update(\n            {\n                "agent_version": self.model_spec_version,\n                "candidate_id": self.candidate_id,\n                "topology_mode": self.topology_mode,\n                "mode_decision_day": self.mode_decision_day,\n                "mode_decision_pressure": self.mode_decision_pressure,\n                "mode_decision_features": deepcopy(self.mode_decision_features),\n                "mode_decisions": self.mode_decisions,\n                "regime_observations": dict(self.regime_observations),\n                "regime_transitions": deepcopy(self.regime_transitions),\n                "unique_regimes": len(self.regime_observations),\n                "unique_public_opponent_snapshots": len(\n                    self.opponent_feature_hashes\n                ),\n                "latest_opponent_features": deepcopy(\n                    self.latest_opponent_features\n                ),\n                "dynamic_build_route_actions": (\n                    self.dynamic_build_route_actions\n                ),\n                "dynamic_build_commands": self.dynamic_build_commands,\n                "persistent_fill_batches": self.persistent_fill_batches,\n                "delayed_livestock_placements": (\n                    self.delayed_livestock_placements\n                ),\n                "public_features_only": True,\n                "cross_episode_memory": False,\n            }\n        )\n        return telemetry\n\n\ndef create_codex_e18_opponent_reactive_topology(\n    run_context: dict[str, Any] | None = None,\n    config_path: Path | str | None = None,\n    base_policy=None,\n):\n    """Create the fail-closed E18 public-opponent-reactive candidate."""\n\n    instance = CodexE18OpponentReactiveTopologyAgent(\n        run_context=run_context,\n        config_path=config_path,\n        base_policy=base_policy,\n    )\n\n    def policy(\n        observation: dict[str, Any],\n        configuration: Any = None,\n    ) -> dict[str, Any]:\n        try:\n            action = instance(observation, configuration)\n            policy.codex_e18_opponent_reactive_last_error = None\n            return action\n        except (KeyboardInterrupt, SystemExit):\n            raise\n        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary\n            instance.error_count += 1\n            instance.fallback_count += 1\n            instance.last_exception = f"{type(exc).__name__}: {exc}"\n            policy.codex_e18_opponent_reactive_last_error = instance.last_exception\n            return deepcopy(_SAFE_PASS)\n\n    policy.codex_e18_opponent_reactive_instance = instance\n    policy.codex_e18_opponent_reactive_last_error = None\n    policy.__name__ = "codex_e18_1_opponent_reactive_662_770_policy"\n    return policy\n\n\n__all__ = [\n    "DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH",\n    "E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION",\n    "CodexE18OpponentReactiveTopologyAgent",\n    "create_codex_e18_opponent_reactive_topology",\n    "load_e18_opponent_reactive_config",\n]\n'
_E18_CONFIG = {'candidate_id': 'CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1',
 'schema_version': 'e18.codex.opponent_reactive_topology.v1',
 'model_spec_version': 'CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1',
 'base_candidate_id': 'CODEX_E17_3_TOPOLOGY_FILL_662_V2',
 'causal_family': 'PUBLIC_OPPONENT_REGIME_AND_DYNAMIC_TOPOLOGY_CONTROL',
 'decision_day': 6,
 'expansion_pressure_threshold': 8.0,
 'pressure_weights': {'extra_quadrants': 3.0,
                      'crops': 0.15,
                      'hands': 0.5,
                      'animals': 0.25,
                      'pastures': 0.1,
                      'weeds': -0.2},
 'mode_below_threshold': '6-6-2',
 'mode_at_or_above_threshold': '7-7-0',
 'dynamic_build_worker_limit': 2,
 'livestock_resource_cap': 14,
 'delayed_placement_target': [2, 4],
 'high_pressure_placement_release_day': 28,
 'fill_purchase_cutoff_day': 29,
 'topologies': {'6-6-2': {'quadrant_pasture_caps': {'Q0': 6, 'Q1': 6, 'Q2': 2},
                          'pasture_targets': [[4, 2],
                                              [3, 3],
                                              [4, 3],
                                              [2, 4],
                                              [3, 4],
                                              [4, 4],
                                              [5, 2],
                                              [5, 3],
                                              [6, 3],
                                              [5, 4],
                                              [6, 4],
                                              [7, 4],
                                              [3, 5],
                                              [4, 5]],
                          'reclaimed_crop_targets': [[3, 2], [6, 2], [3, 6], [4, 6], [4, 7]]},
                '7-7-0': {'quadrant_pasture_caps': {'Q0': 7, 'Q1': 7, 'Q2': 0},
                          'pasture_targets': [[3, 2],
                                              [4, 2],
                                              [3, 3],
                                              [4, 3],
                                              [2, 4],
                                              [3, 4],
                                              [4, 4],
                                              [5, 2],
                                              [6, 2],
                                              [5, 3],
                                              [6, 3],
                                              [5, 4],
                                              [6, 4],
                                              [7, 4]],
                          'reclaimed_crop_targets': [[3, 5], [4, 5], [3, 6], [4, 6], [4, 7]]}},
 'dynamic_cells': [[3, 2], [6, 2], [3, 5], [4, 5]],
 'public_features_only': True,
 'cross_episode_memory': False,
 'holdout_consumed': False,
 'final_confirmation_consumed': False}

_e18 = _exec_module(
    "_codex_bundle.agricola.strategy.codex."
    "codex_e18_opponent_reactive_topology",
    _E18_SOURCE,
)
_e18.load_e18_opponent_reactive_config = _config_loader(_E18_CONFIG)


def create_agent(run_context=None):
    return _e18.create_codex_e18_opponent_reactive_topology(
        run_context=run_context,
        config_path=_e18.DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)

