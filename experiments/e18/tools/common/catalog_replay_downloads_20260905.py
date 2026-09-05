"""Freeze recoverable Kaggle cache inventory and Top770 operational evidence."""

import hashlib
import json
from pathlib import Path

from experiments.e18.tools.common.replay_daily_operational_kpi import (
    daily_operational_kpi,
)

ROOT = Path(__file__).resolve().parents[4]
CACHE = ROOT / "data/replays/json"
COMMON = ROOT / "experiments/e18"
CODEX = ROOT / "docs/model_specs/codex/e18"


def main():
    profiles = json.loads(
        (CODEX / "artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json").read_text()
    )["jesse"]
    top = {p["episode_id"]: p for p in profiles}
    records, operational = [], []
    for path in sorted(CACHE.rglob("*.json")):
        assert path.resolve().is_relative_to(CACHE.resolve()) and not path.is_symlink()
        assert path.stem.isdigit(), f"Not a recoverable numeric replay: {path}"
        raw = path.read_bytes()
        replay = json.loads(raw)
        episode = int(path.stem)
        assert replay["info"]["EpisodeId"] == episode
        assert len(replay["steps"]) == 720
        assert all(r["status"] == "DONE" for r in replay["steps"][-1])
        digest = hashlib.sha256(raw).hexdigest()
        record = {
            "episode_id": episode,
            "relative_path": path.relative_to(ROOT).as_posix(),
            "sha256": digest,
            "bytes": len(raw),
            "states": 720,
            "statuses": [r["status"] for r in replay["steps"][-1]],
            "seed": replay["info"].get("seed"),
            "rewards": replay["rewards"],
            "recovery_url": f"https://www.kaggle.com/competitions/episodes/{episode}/replay.json",
            "role": "TOP770_FROZEN_STRATEGY_NOT_HOLDOUT"
            if episode in top
            else "E18_16_EXTERNAL_LOSS_DIAGNOSTIC_NOT_HOLDOUT",
            "group": "Top770" if episode in top else "E18.16 losses",
        }
        records.append(record)
        if episode in top:
            profile = top[episode]
            assert digest == profile["sha256"]
            operational.append(
                {
                    "episode_id": episode,
                    "seat": profile["seat"],
                    "sha256": digest,
                    "daily": daily_operational_kpi(
                        replay, profile["seat"], profile["ledger"]
                    ),
                }
            )
    assert len(records) == 22 and len({r["episode_id"] for r in records}) == 22
    assert len(operational) == 5
    payload = {
        "catalog_id": "E18_REPLAY_DOWNLOAD_CATALOG_20260905",
        "created_date": "2026-09-05",
        "removal_status": "PENDING_AFTER_ANALYSIS",
        "cache_root": CACHE.relative_to(ROOT).as_posix(),
        "files": records,
        "file_count": len(records),
        "total_bytes": sum(r["bytes"] for r in records),
        "recovery": "Download recovery_url through authenticated Kaggle; verify episode ID, 720 DONE/DONE states and SHA-256. If bytes change, quarantine and compare canonical contents before reuse.",
        "not_deleted": "Derived artifacts, local simulation data, plans, configs, source, reports and Git history.",
    }
    destination = (
        COMMON / "artifacts/derived/common/E18_REPLAY_DOWNLOAD_CATALOG_20260905.json"
    )
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (CODEX / "artifacts/derived/TOP770_D01_D30_OPERATIONAL_KPI.json").write_text(
        json.dumps(
            {
                "analysis_id": "TOP770_D01_D30_OPERATIONAL_KPI",
                "profiles": operational,
                "checkpoint": "H24 pre-last batch, D30 terminal; unwatered is not a verified missed deadline",
                "flows": "MOVE/PASS per executed calendar day; verified animal losses attributed to the day preceding refresh",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    lines = [
        "# E18 — catalogo di recupero download replay, 2026-09-05",
        "",
        f"Inventario verificato: {len(records)} replay, {payload['total_bytes'] / 1024**2:.2f} MiB. Rimozione: **in attesa della conclusione delle analisi**.",
        "",
        "I file sono cache grezze Kaggle riscaricabili, non esperimenti locali. Nessun file è cancellato da questo generatore.",
        "",
        "| Episode / recupero | Gruppo | Seed | Reward P0 / P1 | MiB | SHA-256 |",
        "|---|---|---:|---|---:|---|",
    ]
    for r in records:
        lines.append(
            f"| [{r['episode_id']}]({r['recovery_url']}) | {r['group']} | {r['seed']} | {r['rewards'][0]} / {r['rewards'][1]} | {r['bytes'] / 1024**2:.2f} | `{r['sha256']}` |"
        )
    lines += [
        "",
        "## Recupero e limiti",
        "",
        "Aprire il link canonico dell'episodio in Kaggle autenticato e scaricare il replay. Salvare come `<EPISODE_ID>.json` nella cache canonica; verificare hash, ID, 720 stati e DONE/DONE prima del riuso. Un endpoint è un riferimento di recupero, non una garanzia di disponibilità eterna: se il file cambia, non sostituire silenziosamente la fonte congelata.",
        "",
        "Manifest con percorsi esatti, byte e hash: `../../artifacts/derived/common/E18_REPLAY_DOWNLOAD_CATALOG_20260905.json`.",
        "",
        "## Evidenze conservate",
        "",
        "- Top770: profili e ledger D1-D30, traiettorie/quantità, diagnosi D25-D30, KPI completi e audit COOP nei derivati Codex E18.",
        "- Nuovo `docs/model_specs/codex/e18/artifacts/derived/TOP770_D01_D30_OPERATIONAL_KPI.json`: MOVE/PASS giornalieri, unwatered/stressed H24, WEED H24 e perdite animali verificate, per i cinque replay.",
        "- Sconfitte E18.16: `docs/model_specs/codex/e18/artifacts/derived/E18_16_KAGGLE_LOSS_DIAGNOSTIC_2026_09_04.json` e report corrispondente.",
        "- Catalogo storico: `data/replays/json/json.md`. Tutto questo corpus è diagnostica/training, non holdout.",
        "",
        "La rimozione autorizzata riguarda solo i 22 percorsi nel manifest, dopo verifica dell'hash corrente. Restano metriche, report, config, piani, simulazioni locali e cronologia Git. Per rigenerare analisi frame-by-frame sarà necessario riscaricare i grezzi.",
        "",
    ]
    report = COMMON / "reports/common/E18_REPLAY_DOWNLOAD_REFERENCE_20260905_IT.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "files": len(records),
                "MiB": payload["total_bytes"] / 1024**2,
                "report": str(report),
            }
        )
    )


if __name__ == "__main__":
    main()
