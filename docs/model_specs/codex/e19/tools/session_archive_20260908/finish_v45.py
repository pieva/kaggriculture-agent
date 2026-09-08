import json
from pathlib import Path
from statistics import mean
out=Path('docs/model_specs/codex/e19/reports/closure_bridge_770_20260908')
s=json.loads((out/'summary.json').read_text(encoding='utf-8'))
raw=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
text='# V45: ponte pianificato D26–D27 — 2026-09-08\n\n'
text+='Solo 770. V45 deriva da V44: prolunga pianificazione biologica, percorsi, dispatch e certificato fino a D27 incluso. A D26 nuove colture annuali solo se maturano entro D29 con D30 disponibile per raccolta/vendita: carote. A D27 nessuna nuova annuale soddisfa il margine. D28–D30 vecchia chiusura. Consistenze, ledger e KPI operativi D1–D25 verificati identici a V44 sui sei casi.\n\nAnalisi iniziale: il divario finale V44/V41 non e solo operativo; D26–D30 latte raccolto 49,33 vs 56,33, venduto 66,33 vs 69,33, prezzo realizzato circa 122 vs 159. La tabella report distingue volume e prezzo nel mercato condiviso.\n\n'
for v in ['v41','v44','v45']:
    r=s[v]
    text+=f"- {v}: cassa {r['cash']:.2f}, V4D {r['opponent_cash']:.2f}, scarto {r['relative_pct']:.2f}%, vittorie {r['wins']}/6; animali persi {r['animal_losses']}, perdite idriche {r['water_deaths']}, infestanti mediane D30 {r['weeds_D30']}.\n"
    ps=[json.loads((raw/f'daily_routes_{v}_{seed}_{seat}.json').read_text(encoding='utf-8'))['sides']['candidate'] for seed in range(180903001,180903004) for seat in (0,1)]
    vals={k:round(mean(d['executed_actions'].get(k,0) for p in ps for d in p['ledger']['daily'][25:27]),2) for k in ['FEED','CARE','WATER','PLANT']}
    vals.update({k:round(mean(d[k] for p in ps for d in p['operational_daily'][25:27]),2) for k in ['MOVE','PASS']})
    text+=f'  Medie D26–D27: {vals}\n'
    print(v,vals)
text+='\nTre test mirati passati: ciclo carote a D26, rifiuto semine tarde D27, delega chiusura D28. Sei casi di sviluppo (tre semi, due posizioni), non validazione indipendente. Report completi 22 KPI, tabelle quantità/prezzi e hash sorgenti. Nessuna pubblicazione o promozione automatica; V29 resta pubblicata, V33 riferimento storico.\n\nReport: `docs/model_specs/codex/e19/reports/closure_bridge_770_20260908/v45_TOP770_D01_D30_COMPLETE_KPI.html`.\n\n---\n\n'
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);p.write_text(text+p.read_text(encoding='utf-8'),encoding='utf-8')
