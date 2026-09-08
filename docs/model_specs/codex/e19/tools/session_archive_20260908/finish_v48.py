import json
from pathlib import Path
from statistics import mean
out=Path('docs/model_specs/codex/e19/reports/productive_water_770_20260908')
s=json.loads((out/'summary.json').read_text(encoding='utf-8'))
raw=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
text='# V48: WATER produttivo prima di HARVEST — 2026-09-08\n\n'
text+='Solo 770. V48 deriva da V47. A D28–D30 conserva WATER prima del raccolto in scadenza sulle annuali non ancora irrigate, in finestra di resa e sotto massimo. Incremento stimato +1/+2 limitato al massimo osservato; valore della visita aggiornato al prezzo corrente. Offre HARVEST breve a priorita inferiore e impedisce che il lavoro WATER+HARVEST non fattibile degeneri in solo WATER. Prime consistenze, ledger e KPI D1–D27 verificati uguali a V47.\n\n'
for v in ['v41','v45','v47','v48']:
    r=s[v]
    text+=f"- {v}: cassa {r['cash']:.2f}, V4D {r['opponent_cash']:.2f}, margine relativo {r['relative_pct']:.2f}%, vittorie {r['wins']}/6; perdite idriche {r['water_deaths']}, animali {r['animal_losses']}, infestanti mediane D30 {r['weeds_D30']}.\n"
    ps=[json.loads((raw/f'daily_routes_{v}_{seed}_{seat}.json').read_text(encoding='utf-8'))['sides']['candidate'] for seed in range(180903001,180903004) for seat in (0,1)]
    vals={crop:{k:round(mean(sum(d[k].get(crop,0) for d in p['ledger']['daily'][27:]) for p in ps),2) for k in ['harvested','sold_units','sales_cash']} for crop in ['WHEAT','CARROT']}
    print(v,vals);text+=f'  Raccolte/vendite D28–D30: {vals}\n'
text+='\nQuattro test mirati passati: resa acqua limitata, visita completa/ripiego, invarianza prima di D28, divieto ripiego solo WATER. Sei casi di sviluppo (tre semi nelle due posizioni), non validazione indipendente. Report 22 KPI e tabella quantita/prezzi; nessuna pubblicazione automatica.\n\nReport: `docs/model_specs/codex/e19/reports/productive_water_770_20260908/v48_TOP770_D01_D30_COMPLETE_KPI.html`.\n\n---\n\n'
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);p.write_text(text+p.read_text(encoding='utf-8'),encoding='utf-8')
