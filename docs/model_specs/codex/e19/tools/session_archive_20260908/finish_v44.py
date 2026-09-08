import json
from pathlib import Path
from statistics import mean
out=Path('docs/model_specs/codex/e19/reports/water_route_770_20260908')
s=json.loads((out/'summary.json').read_text(encoding='utf-8'))
raw=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
text='# V44: servizi oltre rinnovi provvisori — 2026-09-08\n\n'
text+='Solo 770. V42 estende protezione V41 a WATER delle colture gia stressate: un caso, cassa 97,290 vs V4D 112,257, zero perdite idriche e animali ma D25 coltivate 39. V43 recupera fuori area solo se il percorso previsto arriva tardi: un caso, cassa 70,555 vs 72,615, zero perdite ma D25 coltivate 38. Nessuna delle due estesa a sei casi.\n\nV44 torna a V41: quando prepara un servizio esistente, filtra dalla coda precedente le proposte NEW_ non ancora ammesse. Permette quindi WATER/FEED ecc. anche oltre un rinnovo provvisorio, conservando ordine fra servizi e priorita originali. Nessuna modifica calendario, recupero fuori area o chiusura D26+. Le proposte non vengono cancellate dal piano.\n\n'
for v in ['v41','v44']:
    r=s[v]
    text+=f"- {v}: cassa {r['cash']:.2f}, V4D {r['opponent_cash']:.2f}, scarto {r['relative_pct']:.2f}%, vittorie {r['wins']}/6; perdite animali {r['animal_losses']}, idriche {r['water_deaths']}, coltivate mediane D25 {r['cultivated']['25']}, infestanti D30 {r['weeds_D30']}.\n"
    ps=[json.loads((raw/f'daily_routes_{v}_{seed}_{seat}.json').read_text(encoding='utf-8'))['sides']['candidate'] for seed in range(180903001,180903004) for seat in (0,1)]
    vals={k:round(mean(d[k] for p in ps for d in p['operational_daily'][20:25]),2) for k in ['MOVE','PASS','weed_tiles']}
    vals.update({k:round(mean(d['executed_actions'].get(k,0) for p in ps for d in p['ledger']['daily'][20:25]),2) for k in ['WATER','FEED','CARE','PLANT']})
    text+=f'  Medie D21–D25: {vals}\n'
    print(v,vals)
text+='\nUndici test mirati passati (4 V42, 3 V43, 4 V44). Sei casi di sviluppo, tre semi nelle due posizioni, non indipendenti. Report completo 22 KPI e manifest SHA256. Nessuna submission o promozione automatica: V33 resta riferimento e V29 pubblicata. Valutare tutti i KPI e la cassa relativa prima della scelta.\n\nReport: `docs/model_specs/codex/e19/reports/water_route_770_20260908/v44_TOP770_D01_D30_COMPLETE_KPI.html`.\n\n---\n\n'
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);p.write_text(text+p.read_text(encoding='utf-8'),encoding='utf-8')
