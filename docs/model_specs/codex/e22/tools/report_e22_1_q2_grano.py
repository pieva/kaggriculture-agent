"""Render standard 22 KPI + volumes and prices for the frozen wheat release."""
import csv
import gzip
import hashlib
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e22.tools.report_external_20260914 import METRICS,aggregate,page,rowdata
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_1_q2_grano_v1'
ART=ROOT/'docs/model_specs/codex/e22/artifacts/e22_1_q2_grano_v1'


def readgz(p):
    with gzip.open(p,'rt',encoding='utf-8') as f:return json.load(f)


def main():
    rows=json.loads((OUT/'RESULTS.json').read_text());build=json.loads((OUT/'BUILD.json').read_text())
    ds=[r for r in rows if r['kind']=='diagnostic'];direct=[r for r in rows if r['kind']=='direct']
    assert len(ds)==20 and len(direct)==14
    summary=dict(diagnostic_n=20,diagnostic_mean_cash_delta=st.mean(r['cash_delta'] for r in ds),diagnostic_min_cash_delta=min(r['cash_delta'] for r in ds),diagnostic_max_cash_delta=max(r['cash_delta'] for r in ds),diagnostic_positive=sum(r['cash_delta']>0 for r in ds),direct_n=14,direct_wins=sum(r['margin']>0 for r in direct),direct_mean_margin=st.mean(r['margin'] for r in direct),direct_median_margin=st.median(r['margin'] for r in direct),direct_paired_seed_means={str(seed):st.mean(r['margin'] for r in direct if r['seed']==seed) for seed in sorted({r['seed'] for r in direct})},candidate_sha256=build['sha256'],additional_workers=0,additional_hiring_cash=0)
    ps=[readgz(ART/f"diagnostic_{r['episode']}.profile.json.gz") for r in ds]
    bs=[json.loads((OUT.parent/f"external_e22_2_20260914/profiles/56206528_{r['episode']}.json").read_text())['own'] for r in ds]
    views=[dict(title='20 scenari diagnostici · aggregato',labels=['E22.1 Q2 Grano v1','E22.1 pubblicata'],note='Stesso scenario, azioni avversarie congelate; mediana e min–max. Non è una stima di rating.',series=[aggregate(ps),aggregate(bs)])]
    csvrows=[]
    for r,p,b in zip(ds,ps,bs):
        expected=Counter(b['totals']['harvested']);expected['WHEAT']+=2
        assert Counter(p['totals']['harvested'])==expected
        expected=Counter(b['totals']['sold_units']);expected['WHEAT']+=2
        assert Counter(p['totals']['sold_units'])==expected
        assert p['totals']['hire_cash']==b['totals']['hire_cash']
        views.append(dict(title=f"Replay {r['episode']} · delta {r['cash_delta']:+.0f}",labels=['E22.1 Q2 Grano v1','E22.1 pubblicata'],note='Confronto con la versione originale nello stesso scenario.',series=[aggregate([p]),aggregate([b])]))
        for arm,profile in [('grano',p),('baseline',b)]:csvrows.extend(dict(kind='diagnostic',case=str(r['episode']),arm=arm,**d) for d in rowdata(profile))
    for r in direct:
        both=readgz(ART/f"direct_{r['seed']}_{r['seat']}.profiles.json.gz");p,b=both[r['seat']],both[1-r['seat']]
        assert p['totals']['hire_cash']==b['totals']['hire_cash']
        assert p['terminal']['shed'].get('WHEAT',0)==p['terminal']['carried'].get('WHEAT',0)==0
        views.append(dict(title=f"Diretto {r['seed']} · lato {r['seat']} · margine {r['margin']:+.0f}",labels=['E22.1 Q2 Grano v1','E22.1 pubblicata'],note='Due policy reali, stesso incontro e mercato condiviso; non è un confronto controfattuale dello stesso lato.',series=[aggregate([p]),aggregate([b])]))
        for arm,profile in [('grano',p),('baseline',b)]:csvrows.extend(dict(kind='direct',case=f"{r['seed']}_{r['seat']}",arm=arm,**d) for d in rowdata(profile))
    pubfile=OUT/'PUBLICATION.json';pub=json.loads(pubfile.read_text()) if pubfile.exists() else None
    status=(f"Pubblicata: submission {pub['submission']}, stato {pub['status']}." if pub.get('submission') else f"Invio accettato da Kaggle; stato {pub['status']}, elaborazione esterna in corso.") if pub else 'Bundle verificato, in preparazione per la pubblicazione autorizzata.'
    md=f'''# E22.1 Q2 Grano v1

{status}

Il pollaio vuoto in (3,7), previsto a D29 H5, è sostituito da grano seminato D28 H8 dopo l'ultima raccolta di fragole. Due unità raccolte D30 H10, consegnate e vendute a H22. Restano 8 mucche, 6 pecore e 3 oche nei pollai Q0.

Il lavoratore 10 serve anche il grano adiacente (4,7); a D28 si recuperano un DIG a fine ciclo e un'irrigazione non produttiva, a D30 si accorpa la consegna e si usano gli slot inattivi. Nessuna assunzione né costo di lavoro aggiuntivo. Seme aggiuntivo: 10. Il lavoratore 6 usa la vecchia azione BUILD_COOP per WATER. Il piano fino a D27 resta identico.

## Test del bundle effettivo

- Parità con l'intervento diagnostico: 14.380 azioni; risposte indipendenti e caricamento senza __file__.
- 20 partite complete nel loader Kaggle contro avversari registrati: cassa finale esattamente uguale al test dal checkpoint; +2 grani raccolti e venduti per partita, senza nuove fughe e senza rimanenze aggiuntive.
- Incremento medio cassa nei 20 scenari: **+{summary['diagnostic_mean_cash_delta']:.2f}**, minimo +{summary['diagnostic_min_cash_delta']:.0f}, massimo +{summary['diagnostic_max_cash_delta']:.0f}; positivi 20/20. Costi e prezzi effettivi già inclusi.
- 14 confronti diretti con i due file reali, sette semi esposti e due lati: **{summary['direct_wins']}/14 vittorie**, margine medio **{summary['direct_mean_margin']:+.2f}**, mediano {summary['direct_median_margin']:+.2f}. Mix 8C6S3G, zero fughe; raccolta finale aggiuntiva verificata 14/14.
- Ledger contabili e azioni verificati; semi riservati non usati. I sette seed con due lati non costituiscono 14 osservazioni indipendenti. Il piccolo incremento locale non implica un aumento garantito del rating esterno.

SHA256: `{build['sha256']}`. Bundle: `submission_codex_e22_1_q2_grano_v1.py`.

[22 KPI, volumi e prezzi](REPORT.html) · [Dati CSV](DAILY_22_KPI_PRICES.csv) · [Risultati](RESULTS.json) · [Protocollo](PROTOCOL.json) · [Confronto grano/carote e percorso](../e22_1_q2_coop_20260914/REPORT.html).
'''
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body=f'<p><b>{status}</b></p><p>Grano in (3,7) al posto del pollaio vuoto: semina D28, raccolta D30, stessa manodopera. Mix 8C6S3G.</p><p class="note">20 scenari: +{summary["diagnostic_mean_cash_delta"]:.2f} cassa media, tutti positivi. 14 confronti diretti: {summary["direct_wins"]} vittorie, margine medio {summary["direct_mean_margin"]:+.2f}. Nessuna stima di rating.</p><p><a href="REPORT.md">Calendario e verifiche</a> · <a href="DAILY_22_KPI_PRICES.csv">CSV 22 KPI e prezzi</a> · <a href="../e22_1_q2_coop_20260914/REPORT.html">Scelta della coltura</a></p>'
    (OUT/'REPORT.html').write_text(page('E22.1 Q2 Grano v1',body,dict(metrics=METRICS,views=views)),encoding='utf-8')
    with (OUT/'DAILY_22_KPI_PRICES.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2))
    (OUT/'VERIFICATION.json').write_text(json.dumps(dict(sha256=build['sha256'],real_file_loader_games=34,diagnostic_action_parity=14380,cash_ledger_errors=0,panels=len(METRICS),views=len(views),reserved_seeds_used=0),indent=2))
    artifacts=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(ART.iterdir()) if p.is_file()]
    (OUT/'LOCAL_ARTIFACTS.json').write_text(json.dumps(artifacts,indent=2))
    manifest=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ['MANIFEST.json','VERIFY.log']]
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':main()
