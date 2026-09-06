"""Summarize matched official-engine evidence, keeping CRN diagnostics separate."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]
DERIVED=ROOT/'artifacts/derived'


def key(m):
    return m['opponent'],m['seed'],m['seat']


def phase(m, first, last):
    counts=sum((Counter(d) for d in m['action_daily'][first-1:last]),Counter())
    return dict(passes=counts['PASS'],moves=counts['MOVE'],slots=sum(counts.values()),
                cow_days=sum(d['animals']['COW'] for d in m['daily'][first-1:last]))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--candidate',default='E18_31_ASSIGNMENT_GATE_DEVELOPMENT_V7_20260906.json')
    parser.add_argument('--baseline',nargs='*',default=[])
    parser.add_argument('--label',default='V7_20260906')
    args=parser.parse_args()
    source=json.loads((DERIVED/args.candidate).read_text())
    assert source['complete'] and not source.get('engine_regime')
    baseline={}
    files=['E18_30_MISSION_GATE_CROP_STRESS_V2_20260906.json',
           'E18_30_MISSION_GATE_CROP_DEVELOPMENT_V2_20260906.json',
           'E18_30_MISSION_GATE_CROP_CONTROL_V2_20260906.json',*args.baseline]
    for name in files:
        data=json.loads((DERIVED/name).read_text())
        assert data['complete'] and not data.get('engine_regime')
        for m in data['matches']:
            if m['variant'] not in {'CROP_POOL','BASELINE'}:
                continue
            if key(m) in baseline:
                assert baseline[key(m)]['actions_sha256']==m['actions_sha256']
            baseline[key(m)]=m
    candidate=source['matches']
    safety=[]
    for m in candidate:
        checks=dict(errors=m['errors']==0, crop_deaths=not m['crop_starvation'],
            animal_losses=not m['ledger']['animal_escapes'], missions=m['incomplete_missions']==0,
            money=not m['ledger']['cash_parity_errors'], cap=m['max_resources']<=14 and m['max_hands']<=12,
            filled=m['daily'][-1]['animals']=={'COW':9,'SHEEP':5,'GOOSE':0},
            topology=m['daily'][-1]['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0})
        safety.append(dict(case=key(m),checks=checks,passed=all(checks.values())))
    summaries=[]
    for opponent in sorted({m['opponent'] for m in candidate}):
        rows=[m for m in candidate if m['opponent']==opponent and key(m) in baseline]
        if not rows:
            continue
        controls=[baseline[key(m)] for m in rows]
        out=dict(opponent=opponent,n_paired=len(rows),n_candidate=sum(m['opponent']==opponent for m in candidate),
                 baseline_cash=mean(m['reward'] for m in controls),candidate_cash=mean(m['reward'] for m in rows),
                 paired_positive=sum(m['reward']>b['reward'] for m,b in zip(rows,controls)),
                 candidate_wins=sum(m['reward']>m['opponent_reward'] for m in rows),
                 baseline_wins=sum(m['reward']>m['opponent_reward'] for m in controls))
        out['cash_delta']=out['candidate_cash']-out['baseline_cash']
        out['cash_delta_pct']=100*out['cash_delta']/out['baseline_cash']
        out['phases']={}
        for first,last in [(1,15),(5,10),(16,30)]:
            bp=[phase(m,first,last) for m in controls]
            cp=[phase(m,first,last) for m in rows]
            out['phases'][f'D{first}_D{last}']={
                'baseline':{k:mean(d[k] for d in bp) for k in bp[0]},
                'candidate':{k:mean(d[k] for d in cp) for k in cp[0]}}
        out['days']=[dict(day=d,baseline_pass=mean(m['action_daily'][d-1].get('PASS',0) for m in controls),
            candidate_pass=mean(m['action_daily'][d-1].get('PASS',0) for m in rows),
            baseline_cows=mean(m['daily'][d-1]['animals']['COW'] for m in controls),
            candidate_cows=mean(m['daily'][d-1]['animals']['COW'] for m in rows),
            baseline_hands=mean(m['daily'][d-1]['hands'] for m in controls),
            candidate_hands=mean(m['daily'][d-1]['hands'] for m in rows)) for d in range(5,11)]
        summaries.append(out)
    result=dict(candidate_source=args.candidate,baseline_sources=files,holdout_consumed=False,
        supplementary_crn_included=False,safety=safety,summaries=summaries,
        caveats=['Two seats of a seed are not independent seeds.',
                 'The stock engine couples empty-tile RNG draws to town-shop selection.',
                 'Cow-days use the standard daily stock snapshot, not exact animal-hours.',
                 'Report available matched coverage explicitly; do not impute missing controls.'])
    output=DERIVED/f'E18_31_ASSIGNMENT_SUMMARY_{args.label}.json'
    assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines=['# E18.31 — verifica integrata PASS / mucche','',
           'Sviluppo interno, non submission e non promozione. Baseline E18.30 CROP_POOL V2.',
           f"Safety completa: {sum(s['passed'] for s in safety)}/{len(safety)} casi. Holdout non consumato.",'',
           'Le condizioni di investimento e missione valgono lungo il mese. Il programma colturale e il budget HIRE ereditati restano controlli della sperimentazione; non dichiarare riscritta tutta la strategia.', '']
    for s in summaries:
        lines += [f"## Controllo {s['opponent']}",'',
            f"Confronti appaiati: {s['n_paired']} di {s['n_candidate']} casi candidati. Cassa media {s['candidate_cash']:.2f} vs {s['baseline_cash']:.2f} ({s['cash_delta_pct']:+.2f}%).",
            f"Casi con miglioramento: {s['paired_positive']}/{s['n_paired']}; vittorie candidato {s['candidate_wins']}, baseline {s['baseline_wins']}.",'',
            '| Giorno | PASS E18.30 | PASS E18.31 | Mucche E18.30 | Mucche E18.31 | Manovali E18.30 | Manovali E18.31 |',
            '|---|---:|---:|---:|---:|---:|---:|']
        lines += [f"| D{d['day']} | {d['baseline_pass']:.2f} | {d['candidate_pass']:.2f} | {d['baseline_cows']:.2f} | {d['candidate_cows']:.2f} | {d['baseline_hands']:.2f} | {d['candidate_hands']:.2f} |" for d in s['days']]
        lines += ['']
    lines += ['## Limiti del giudizio','',
              'I PASS vanno letti insieme agli slot lavorativi realmente disponibili: meno assunzioni può ridurli senza migliorare la produttività.',
              'Il sorteggio dei negozi usa lo stesso RNG delle erbacce dopo un numero di estrazioni dipendente dalle tile vuote. Cambiare occupazione può quindi cambiare domanda e prezzi a seed uguale. Una singola partita non separa questi effetti.',
              'Gli eventuali esperimenti a numeri casuali comuni sono diagnostici supplementari, chiaramente separati dal motore ufficiale e non utilizzabili come verifica Kaggle.',
              'Nessun dato Top770 alimenta le nuove regole. Non dichiarare entrambi i problemi risolti con il solo miglioramento operativo o una media economica negativa.','']
    report=ROOT/'reports'/f'E18_31_ASSIGNMENT_SUMMARY_{args.label}_IT.md'
    report.write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(summaries,indent=2))


if __name__=='__main__':
    main()
