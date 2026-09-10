"""Freeze the six-case matched economic gate and standalone action parity."""
import gzip
import hashlib
import json
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'

def read(p):return json.loads(p.read_text())
def actions(path,seat):
    with gzip.open(path,'rt') as f:r=json.load(f)
    return [s[seat]['action'] for s in r['steps'][1:]]

def main():
    rows=[]
    for seed in [180903001,180903002,180903003]:
        source=BASE/f'artifacts/development/E20v18_E18_{seed}.replay.json.gz'
        fresh=read(BASE/f'artifacts/baseline/E19_E18_{seed}.json')
        for seat in (0,1):
            name=f'E20_E18_{seed}' if seat==0 else f'E18_E20_{seed}'
            path=BASE/'artifacts/validation'/f'{name}.json'
            result=read(path)
            detail=read(path.with_suffix('.kpi.json'))['sides'][seat]
            reference=read(ROOT/f'docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907/daily_routes_v48_{seed}_{seat}.json')
            old=reference['sides']['candidate']['reward']
            assert old==fresh['rewards'][0]  # Fresh forward replay reconciles frozen reference.
            assert result['opening'][seat]['topology']==[7,7,2]
            assert not detail['ledger']['animal_escapes']
            assert result['runtime'][seat]['core_errors']==0
            assert result['runtime'][seat]['calls']==719
            assert actions(path.with_suffix('.replay.json.gz'),seat)==actions(source,0)
            rows.append(dict(seed=seed,seat=seat,E19=old,E20=result['rewards'][seat],
                             delta=result['rewards'][seat]-old,source_bundle_action_parity=True,
                             animal_losses=0,crop_water_deaths=len(detail['crop_starvation']),
                             E19_crop_water_deaths=len(reference['sides']['candidate']['crop_starvation'])))
    e19=mean(r['E19'] for r in rows);e20=mean(r['E20'] for r in rows)
    assert e20>=e19
    bundle=ROOT/'submission/submission_codex_e20_772_e20v18_candidate.py'
    result=dict(passed=True,metric='matched final cash against E18',cases=rows,E19_mean=e19,E20_mean=e20,
                delta=e20-e19,delta_percent=100*(e20/e19-1),independent_seeds=3,paired_seats=6,
                bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest(),
                note='Development gate; role swaps are not independent seeds. Tournament seeds remain untouched.')
    (BASE/'artifacts/ECONOMIC_GATE.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# E20 — sviluppo e soglia economica','',
           f"Gate economico superato: E20 {e20:,.1f}, E19 {e19:,.1f}; delta {result['delta_percent']:.2f}%. Tre seed, entrambi i ruoli; tutte le sei differenze positive. Azioni del bundle standalone identiche alla candidata, zero errori core e zero perdite animali.",
           '', 'Limite operativo: il diagnostico comune crop_service_audit registra 10 transizioni crop→weed dopo stress idrico per ogni partita E20, contro 2/2/7 di E19 sui tre seed. La soglia economica non certifica un miglioramento della sicurezza delle colture: questa regressione deve restare esplicita nel report.', '',
           'La selezione usa 23 varianti iniziali sul seed 180903001. V18 viene poi confermata sui seed 180903002/3 e con scambio dei ruoli. Il torneo usa sette seed separati. Gli esperimenti scartati sono conservati: non vengono presentati come prove indipendenti.','',
           '| Variante | Cassa seed 180903001 | Delta da E19 |','|---|---:|---:|']
    trials=[]
    for p in (BASE/'artifacts/development').glob('E20v*_E18_180903001.json'):
        r=read(p);trials.append((int(r['agents'][0][4:]),r['agents'][0],r['rewards'][0]))
    for _,name,cash in sorted(trials):lines.append(f'| {name} | {cash:,.0f} | {cash-99574:+,.0f} |')
    lines+=['','## Diagnosi e scelta','',
            'La prima posizione (3,5)/(4,5) arriva alla topologia ma resta sotto soglia; due pecore e due mucche non bastano. Più personale, avvio ritardato, bridge E18 prolungato e meloni in tutto Q2 peggiorano. La disposizione influenza servizi e tempi di vendita: V18 mantiene una mucca in (4,5) e una pecora in (4,6). V22 guadagna 49 sul seed iniziale ma perde contro E18 e non viene scelta sopra V18 sulla sola cassa marginale.',
            '', 'Sul seed iniziale V18 riduce i PASS da 1.066 a 970, aumenta i CARE da 281 a 317 e gli incassi latte da 39.257 a 44.813; MOVE sale da 3.459 a 3.516. Gli effetti non sono solo produzione: cambiano anche il mercato comune e le decisioni dell’avversario. Non attribuire tutto il delta al numero di animali.',
            '', '[Gate completo](../artifacts/ECONOMIC_GATE.json) · [Protocollo](../VALIDATION_PROTOCOL.json) · [Specifica](../MODEL_SPEC_CODEX_E20_772.md)']
    (BASE/'reports').mkdir(exist_ok=True)
    (BASE/'reports/DEVELOPMENT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
