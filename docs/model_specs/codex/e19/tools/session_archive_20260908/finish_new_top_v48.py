import json,hashlib
from pathlib import Path
b=Path('docs/model_specs/codex/e19');o=b/'reports/new_top_v48_20260908'
cohorts=json.loads((o/'cohorts.json').read_text(encoding='utf-8'))
c=json.loads((o/'census.json').read_text(encoding='utf-8'))
reg=Path('experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md')
note='''

## 2026-09-08 — ciclo V48 e analisi per fasi

V48 congelata e pubblicata prima del confronto. Esclusi tutti gli autori
consumati/esposti elencati sopra, comprese le righe dello screening precedente.
I seguenti autori sono ora ESPOSTI per il ciclo V48; non sono holdout per release future.
La selezione segue l'ordine osservato durante lo screening, con classifica variabile.

| Autore | Submission | Corpus congelato | Stato |
|---|---:|---|---|
'''
for name,sub,eps in cohorts:
 status='Top770-003; 4/5 finali 770, 16/16 checkpoint per ciascuno dei quattro; CONSUMATO nel ciclo diagnostico V48' if name=='Subin An' else 'ESPOSTO; screening o analisi esplorativa'
 note+=f'| {name} | {sub} | '+', '.join(map(str,eps))+f' | {status} |\n'
note+='''
Il quinto replay di Top770-003 (106835267, 10-7-0) è conservato ed è incluso nel
report del corpus completo. Matthew: 3/5 finali 770, non qualificato dal criterio storico.
Suliman: 10-7-0 in 3/3, alternativa esplorativa, non prova di superiorità.

Su richiesta successiva del proprietario aggiunta analisi D15, moda D15-D25,
sblocco/utilizzo Q2 e D30. Questo criterio aggiunto non è retroattivamente
preregistrato e non sostituisce silenziosamente il criterio finale originario.
Un solo nuovo autore Top770 qualificato, non dodici nuovi Top770.
Gli avversari incidentali nei replay sono stati visibili nello screening:
la loro presenza non qualifica nuovi alias né va trattata come cecità completa.

Report: docs/model_specs/codex/e19/reports/new_top_v48_20260908/REPORT_NUOVI_TOP_V48_IT.html
Quattro report da 22 KPI: Top770-003 filtrato n4, corpus completo n5, Matthew n5,
Suliman n3. Confronto V48 locale n6, non appaiato a questi replay esterni.
Nessuna nuova policy, nessuna 662, nessuna ulteriore submission.
'''
reg.write_text(reg.read_text(encoding='utf-8')+note,encoding='utf-8')
checkpoint='''# Nuovi Top / V48: analisi completata — 2026-09-08

Report principale: docs/model_specs/codex/e19/reports/new_top_v48_20260908/REPORT_NUOVI_TOP_V48_IT.html
12 autori sottoposti a screening, un nuovo Top770 qualificato: Top770-003 (Subin An), 4/5; conservato anche il quinto 10-7-0. Registro comune aggiornato: tutti esposti/consumati per questo ciclo, non riutilizzabili come holdout. Quattro report completi 22 KPI e verifica DOM superata (grafici, tabelle, legenda, selezione giorno), UTF8 e hash.

Conclusione: conservare pianificazione biologica e ottimizzare prima percorsi/personale su 770. Prima alternativa proposta per un test futuro: 10-7-0, Q2 agricolo; non implementata e non provata causalmente superiore. D15-D25 Subin corpus completo n5: MOVE 111 vs V48 150,24; PASS 6,91 vs 28,79; WATER 44,27 vs35,12; CARE16,8 vs12; persone11,53 vs13; infestanti0 vs2,15. Corpus diversi: non inferire rating dalla cassa.

Suliman 10-7-0 daD11 in3/3 ma con perdite animali. Matthew biforca prima della chiusura: 3x770, 2x11-7-0 aD15 ->10-7-0 aD16 ->10-7-1 aD29. Subin4x770 e1x10-7-0 stabiliD15-D30. Tutti13 replay approfonditi sbloccano e usanoQ2 entroD12. Censimento contiene layout, date semine/collocamento e cronologia. Causa economica della scelta tra template ancora non dimostrata; non copiare quote/date senza test. Nessuna modifica V48/pubblicazione aggiuntiva.

---

'''
for f in [Path('docs/NEW_SESSION.md'),Path('docs/PROJECT_STATE.md')]:f.write_text(checkpoint+f.read_text(encoding='utf-8'),encoding='utf-8')
m=json.loads((o/'manifest.json').read_text(encoding='utf-8'))
for p in [reg,Path('scratch/summarize_new_top.py'),Path('scratch/verify_new_top_reports.py'),Path('docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py'),Path('docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d30_closure.py'),Path('experiments/e18/tools/common/replay_daily_operational_kpi.py')]:m['sources'][str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
m['verification']='4 reports: 22 panels, 30 days, valid median/min/max, DOM legend/day controls passed; UTF-8 checked'
(o/'manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
print(m['unique_episodes'],'unique replay files; registry and checkpoints updated')
