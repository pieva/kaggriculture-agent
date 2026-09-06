"""Summarize every native probe; failed gates remain visible."""
import json
from pathlib import Path
from statistics import mean

BASE=Path(__file__).resolve().parents[1]
DERIVED=BASE/"artifacts/derived"


def main():
    baseline=json.loads((DERIVED/"E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json").read_text())
    controls={(r["seed"],r["seat"],r["opponent"]):r for r in baseline["matches"]}
    probes=[]
    for path in sorted(DERIVED.glob("E18_33_COMMON_GATE_NATIVE_V*.json")):
        payload=json.loads(path.read_text())
        rows=[]
        for r in payload["matches"]:
            c=controls[(r["seed"],r["seat"],r["opponent"])]
            topology=r["daily"][-1]["pasture_topology"]
            row=dict(seed=r["seed"],seat=r["seat"],opponent=r["opponent"],cash=r["reward"],
                control_cash=c["reward"],cash_delta=r["reward"]-c["reward"],
                PASS=r["totals"].get("PASS",0),MOVE=r["totals"].get("MOVE",0),
                control_PASS=c["totals"].get("PASS",0),control_MOVE=c["totals"].get("MOVE",0),
                crop_deaths=len(r["crop_starvation"]),animal_losses=len(r["ledger"]["animal_escapes"]),
                incomplete_missions=r["incomplete_missions"],final_topology=topology,
                exact770=topology=={"Q0":7,"Q1":7,"Q2":0,"Q3":0},
                cash_parity_errors=r["ledger"]["cash_parity_errors"],max_resources=r["max_resources"],max_hands=r["max_hands"])
            row["gate_pass"]=bool(row["exact770"] and not row["crop_deaths"] and not row["animal_losses"]
                and not row["incomplete_missions"] and not row["cash_parity_errors"] and row["cash_delta"]>0
                and row["max_resources"]<=14 and row["max_hands"]<=12)
            rows.append(row)
        probes.append(dict(file=path.name,complete=payload["complete"],failures=payload["failures"],matches=rows,
            means={k:mean(r[k] for r in rows) for k in ("cash","control_cash","cash_delta","PASS","MOVE","control_PASS","control_MOVE")},
            gate_pass_count=sum(r["gate_pass"] for r in rows)))
    output=DERIVED/"E18_33_NATIVE_PROBES_CHECKPOINT_20260906.json"
    assert not output.exists()
    output.write_text(json.dumps(dict(probes=probes,selection="NONE_ELIGIBLE",e19_started=False,holdout_consumed=False),indent=2)+"\n",encoding="utf-8")
    for p in probes:
        print(p["file"],p["means"],"gates",p["gate_pass_count"],flush=True)


if __name__=="__main__":
    main()
