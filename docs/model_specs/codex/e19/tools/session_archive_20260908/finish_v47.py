import json
from pathlib import Path
from statistics import mean
out=Path('docs/model_specs/codex/e19/reports/final_water_770_20260908')
s=json.loads((out/'summary.json').read_text(encoding='utf-8'))
raw=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
text='# V47: servizi finali e protezione idrica D28–D29 — 2026-09-08\n\n'
text+='Solo 770. V47 deriva da V46 e aggiunge protezione WATER per piante gia stressate a D28–D29 (priorita 8 e recupero fuori area), escludendo PLANT/DIG. V46 aveva aggiunto 12 perdite idriche finali (10 carote, 2 fragole) rispetto a V45. V46 deriva da V45: prolunga piano/percorsi/certificato/dispatch fino a D29. CARE da D28 solo se care_value prevede una produzione utile entro fine partita; FEED conservato. Nessuna nuova annuale pianificata da D27. D30 riprende gestione terminale precedente. Consistenze, ledger giornalieri e KPI operativi D1–D27 verificati identici a V45.\n\n'
for v in ['v41','v45','v46','v47']:
    r=s[v]
    text+=f"- {v}: cassa {r['cash']:.2f}, V4D {r['opponent_cash']:.2f}, scarto {r['relative_pct']:.2f}%, vittorie {r['wins']}/6; perdite animali {r['animal_losses']}, idriche {r['water_deaths']}, infestanti mediane D30 {r['weeds_D30']}.\n"
    ps=[json.loads((raw/f'daily_routes_{v}_{seed}_{seat}.json').read_text(encoding='utf-8'))['sides']['candidate'] for seed in range(180903001,180903004) for seat in (0,1)]
    vals={k:round(mean(d['executed_actions'].get(k,0) for p in ps for d in p['ledger']['daily'][27:]),2) for k in ['FEED','CARE','WATER','HARVEST']}
    vals.update({k:round(mean(d[k] for p in ps for d in p['operational_daily'][27:]),2) for k in ['MOVE','PASS']})
    text+=f'  Medie D28–D30: {vals}\n';print(v,vals)
text+='\nSette test mirati passati: quattro V46 su CARE/FEED/terminale, tre V47 su finestre temporali, esclusione nuove semine e ordine protetto dei percorsi. Sei casi di sviluppo, tre semi nelle due posizioni. Report completo 22 KPI e tabella raccolte/vendite/prezzi D28–D30. Nessuna promozione automatica o pubblicazione; V29 resta submission pubblicata.\n\nReport: `docs/model_specs/codex/e19/reports/final_water_770_20260908/v47_TOP770_D01_D30_COMPLETE_KPI.html`.\n\n---\n\n'
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);p.write_text(text+p.read_text(encoding='utf-8'),encoding='utf-8')
