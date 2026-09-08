import json
from pathlib import Path
from statistics import mean
out=Path('docs/model_specs/codex/e19/reports/animal_service_770_20260908')
s=json.loads((out/'summary.json').read_text(encoding='utf-8'))
text='# V41: protezione mirata FEED durante i rinnovi — 2026-09-08\n\n'
text+='Solo 770, richiesta prosegui. V40 protegge tutte le visite FEED/CARE nel packing (prima delle altre visite) e dispatcher (priorita 8): screen seed001 seat0, cassa 71,796 vs 92,029 V4D, zero perdite animali ma 7 idriche. Scartata, non estesa a sei casi. V41 limita questa protezione agli animali con consecutive_unfed>=1 e non ancora nutriti. Recupero della visita completa fuori area sin dal mattino per questi animali. Mantiene rinnovi V39, calendario acqua V38 e chiusura precedente D26+.\n\n'
for v,r in s.items():
    text+=f"- {v}: cassa {r['cash']:.2f}, V4D {r['opponent_cash']:.2f}, delta {r['relative_pct']:.2f}%, vittorie {r['wins']}/6; perdite animali {r['animal_losses']}, idriche {r['water_deaths']}, coltivate D25 {r['cultivated']['25']}, infestanti D30 {r['weeds_D30']}.\n"
raw=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
phases={}
for v in ['v39','v41']:
    ps=[json.loads((raw/f'daily_routes_{v}_{seed}_{seat}.json').read_text(encoding='utf-8'))['sides']['candidate'] for seed in range(180903001,180903004) for seat in (0,1)]
    vals={k:round(mean(d[k] for p in ps for d in p['operational_daily'][20:25]),2) for k in ['MOVE','PASS','weed_tiles']}
    vals.update({k:round(mean(d['executed_actions'].get(k,0) for p in ps for d in p['ledger']['daily'][20:25]),2) for k in ['WATER','FEED','CARE','PLANT']})
    phases[v]=vals
    text+=f'\n{v} medie D21–D25: {vals}\n'
text+='\nSei casi di sviluppo: tre semi, entrambe le posizioni. Sei test packing/ordine/budget passati (V40 e V41). Report completo con 22 KPI contro Top770-001, V33, V38, V39; hash sorgenti verificati. Nessuna promozione automatica o submission. V33 resta riferimento e V29 pubblicata. Verificare regressioni acqua, superficie, PASS e competitivita prima di promuovere; il recupero di FEED non equivale a soluzione globale.\n\nReport: `docs/model_specs/codex/e19/reports/animal_service_770_20260908/v41_TOP770_D01_D30_COMPLETE_KPI.html`.\n\n---\n\n'
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);p.write_text(text+p.read_text(encoding='utf-8'),encoding='utf-8')
print(json.dumps(phases,indent=2))
