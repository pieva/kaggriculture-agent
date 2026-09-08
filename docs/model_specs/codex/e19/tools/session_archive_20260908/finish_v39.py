import json
from pathlib import Path
from statistics import mean
out=Path('docs/model_specs/codex/e19/reports/spent_renewal_770_20260908')
s=json.loads((out/'summary.json').read_text(encoding='utf-8'))
text='# V39: rinnovo delle fragole esaurite — 2026-09-08\n\n'
text+='Solo 770. V39 deriva da V38: rinnovo di perenni esaurite anche senza prodotto residuo/visita esistente; ciclo breve WHEAT/CARROT scelto sul margine corrente per giorno quando le fragole non arrivano a produzione. Il ciclo breve deve maturare con un giorno residuo. Nessuna eliminazione anticipata di produzioni future o prodotto da raccogliere. Acqua V38 conservata. Chiusura D26+ precedente.\n\n'
for v,r in s.items():
    text+=f"- {v}: cassa {r['cash']:.2f}, V4D {r['opponent_cash']:.2f}, delta {r['relative_pct']:.2f}%, vittorie {r['wins']}/6; morti idriche {r['water_deaths']}, coltivate D25 {r['cultivated']['25']}, infestanti D30 {r['weeds_D30']}.\n"
text+='\nSei casi, tre semi 180903001–003 nelle due posizioni, gia usati nello sviluppo. Dieci test passati (4 nuovi sul rinnovo, 3 calendario V38, 3 certificato V32). Report completi con 22 KPI e confronto Top770-001, V33, V38; hash sorgenti verificati. Nessuna nuova submission; V33 resta riferimento, V29 pubblicata. Il confronto per KPI e fase resta necessario: il recupero del grano non prova di aver risolto servizi e chiusura carote.\n\nReport: `docs/model_specs/codex/e19/reports/spent_renewal_770_20260908/v39_TOP770_D01_D30_COMPLETE_KPI.html`.\n\n---\n\n'
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);p.write_text(text+p.read_text(encoding='utf-8'),encoding='utf-8')
for v in s:
    raw=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
    ps=[json.loads((raw/f'daily_routes_{v}_{seed}_{seat}.json').read_text(encoding='utf-8'))['sides']['candidate'] for seed in range(180903001,180903004) for seat in (0,1)]
    print(v, {k:round(mean(d[k] for p in ps for d in p['operational_daily'][20:25]),2) for k in ['MOVE','PASS','weed_tiles']}, {k:round(mean(d['executed_actions'].get(k,0) for p in ps for d in p['ledger']['daily'][20:25]),2) for k in ['WATER','FEED','CARE','PLANT']})
