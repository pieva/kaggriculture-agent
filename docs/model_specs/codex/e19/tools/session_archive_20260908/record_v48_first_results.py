import json
from pathlib import Path
from statistics import mean,median
b=Path('docs/model_specs/codex/e19');p=b/'artifacts/derived/v48_external_20260908/first_cohort.json'
d=json.loads(p.read_text(encoding='utf-8'));rs=d['games']
assert all(r['steps']==720 and r['statuses']==['DONE','DONE'] for r in rs)
d['summary']=dict(wins=sum(r['cash']>r['opponent_cash'] for r in rs),losses=sum(r['cash']<r['opponent_cash'] for r in rs),mean_cash=mean(r['cash'] for r in rs),median_cash=median(r['cash'] for r in rs),mean_opponent_cash=mean(r['opponent_cash'] for r in rs))
p.write_text(json.dumps(d,indent=2),encoding='utf-8')
receipt=b/'artifacts/derived/v48_external_publication_receipt.json'
v=json.loads(receipt.read_text(encoding='utf-8'));v.update(submission_id=56101593,status='Complete',rating=822.1,observed_utc=d['observed_utc'],url='https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56101593',first_cohort=str(p));receipt.write_text(json.dumps(v,indent=2),encoding='utf-8')
note='''# V48: primi otto incontri esterni — 2026-09-08

Submission 56101593 Complete; rating osservato 822,1. Otto incontri non self-play: 5 vittorie, 3 sconfitte, tutti 720 stati DONE/DONE. Replay congelati integralmente in docs/model_specs/codex/e19/artifacts/derived/v48_external_20260908; first_cohort.json include hash e risultati. Non è ancora dimostrata superiorità su V29/V4D. Diagnosi KPI dei replay ancora da eseguire.

Lavoro Top in corso: registro storico verificato, autori esposti esclusi. Screening acquisito in new_top_screen_20260908; scratch/new_top_cohorts.json elenca 12 autori. Subin An 4/5 finali 770, Matthew 3/5 escluso dal criterio finale storico. Nuova indicazione utente: confrontare anche D15 e stabilizzazione Q2, separare assetto produttivo e chiusura. Non cambiare retroattivamente criterio senza documentarlo. Dettagli quantitativi variability.json e variability_diagnosis.json. Suliman 10-7-0 da D11 in 3/3; SpaTaro ha anche perdite animali a D20-D21, non tutta variabilità è ottimizzazione. Nuovi report comparativi ancora da completare; nessuna policy modificata.

---

'''
for f in [Path('docs/NEW_SESSION.md'),Path('docs/PROJECT_STATE.md')]:f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
print(d['summary'])
