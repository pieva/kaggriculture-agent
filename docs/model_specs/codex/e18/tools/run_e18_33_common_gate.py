"""Development probe of the native adapter; no E19 match or public upload."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path

from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as gate
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

BASE = Path(__file__).resolve().parents[1]
PROFILE = BASE / "configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--label", required=True)
    p.add_argument('--profile',type=Path,default=PROFILE)
    p.add_argument("--seeds", type=int, nargs="+", default=[180903001])
    p.add_argument("--seats", type=int, nargs="+", default=[0])
    p.add_argument("--opponents", choices=["E18.16", "E18.2/V4D"], nargs="+", default=["E18.16"])
    args = p.parse_args()
    profile = args.profile.resolve()
    assert profile.parent == PROFILE.resolve().parent and profile.is_file()
    assert args.label.replace("_", "").isalnum()
    assert set(args.seeds) <= set(range(180903001, 180903008)) and set(args.seats) <= {0, 1}
    out = BASE / f"artifacts/derived/E18_33_COMMON_GATE_{args.label}.json"
    assert not out.exists()
    engine = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")
    source = [profile, Path(__file__), Path(__file__).with_name("e18_33_common_policy.py"),
              Path(__file__).with_name("e18_33_common_controller.py"), Path(engine.__file__)]
    payload = dict(role="NATIVE_ADAPTER_DIAGNOSTIC_NOT_RELEASE", complete=False, matches=[], failures=[],
                   source_sha256={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in source},
                   holdout_consumed=False, e19_started=False)
    instances = []
    def construct(ignored_plan, seat, ignored_variant):
        instance = CommonController(json.loads(profile.read_text()), engine.market_price, engine.MARKET_PARAMS, seat)
        instances.append(instance)
        return instance
    gate.MissionRuntimeController = construct
    for opponent in args.opponents:
        for seed in args.seeds:
            for seat in args.seats:
                try:
                    result = gate.run_one("CROP_POOL", opponent, seed, seat)
                    instance = instances[-1]
                    result.update(version="E18.33 NATIVE PROBE", variant=args.label,
                                  common_metrics=dict(instance.metrics), common_events=instance.events)
                    payload["matches"].append(result)
                except Exception as exc:
                    payload["failures"].append(dict(seed=seed,seat=seat,opponent=opponent,error=repr(exc)))
                    print(repr(exc), flush=True)
                out.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    payload["complete"] = not payload["failures"] and len(payload["matches"]) == len(args.opponents)*len(args.seeds)*len(args.seats)
    out.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(out, flush=True)
    if not payload["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
