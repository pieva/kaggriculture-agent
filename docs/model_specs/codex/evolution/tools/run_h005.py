"""Freeze H005 predictions before retrospective labels and one-step payoffs."""
import gzip,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.evolution.tools.infer_market_order_mixed import witness,forecast
BASE=ROOT/'docs/model_specs/codex/evolution';SOURCE=ROOT/'docs/model_specs/codex/e20/artifacts/e20_1_confirmation';OUT=BASE/'reports/H005'
def load(path):
    with gzip.open(path,'rb') as f:raw=f.read()
    return json.loads(raw),hashlib.sha256(raw).hexdigest()
def main():
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    predictions=[]
    for p in sorted(SOURCE.glob('*.json')):
        if '.kpi.' in p.name:continue
        meta=json.loads(p.read_text());r,sha=load(p.with_suffix('.replay.json.gz'));assert sha==meta['replay_sha256']
        for seat,model in enumerate(meta['agents']):
            evidence=[]
            for day in range(15,20):
                i=(day-1)*24
                e=witness(r['steps'][i][seat]['observation'],r['steps'][i+1][seat]['observation'],r['steps'][i+1][seat]['action'],r['configuration'],engine)
                evidence.append(dict(day=day,**e))
            predictions.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha,model=model,opponent=meta['agents'][1-seat],seed=meta['seed'],seat=seat,evidence=evidence,forecast=forecast(evidence)))
    assert len(predictions)==84
    prediction_path=OUT/'PREDICTIONS.json';prediction_path.write_text(json.dumps(predictions,indent=2)+'\n')
    prediction_hash=hashlib.sha256(prediction_path.read_bytes()).hexdigest()
    # Evaluation boundary: no contemporaneous opponent order or H003 payoff was read above.
    scan=json.loads((BASE/'reports/H003/ONE_STEP.json').read_text())['rows'];evaluation=[];historical=[]
    cache={}
    for p in predictions:
        if p['source'] not in cache:cache[p['source']]=load((ROOT/p['source']).with_suffix('.replay.json.gz'))[0]
        r=cache[p['source']];seat=p['seat']
        def label(index):
            orders=r['steps'][index][1-seat]['action'].get('market',[])
            pos=next((i for i,o in enumerate(orders) if len(o)>1 and o[:2]==['SELL','STRAWBERRY']),None)
            return 'absent' if pos is None else 'first' if pos==0 else 'not_first'
        for e in p['evidence']:
            historical.append(dict(model=p['model'],seed=p['seed'],seat=seat,day=e['day'],status=e['status'],inferred=e.get('label'),truth=label((e['day']-1)*24+1)))
        truth=label(457)
        payoff=next(x for x in scan if (x['model'],x['opponent'],x['seed'],x['seat'])==(p['model'],p['opponent'],p['seed'],p['seat']))
        assert payoff['source_sha256']==p['source_sha256']
        apply=p['forecast']=='first' and payoff['reason']=='reordered'
        evaluation.append(dict(model=p['model'],opponent=p['opponent'],seed=p['seed'],seat=seat,forecast=p['forecast'],truth=truth,apply=apply,delta_cash=payoff['delta_cash'] if apply else 0,delta_margin=payoff['delta_margin'] if apply else 0,unconditional_delta_cash=payoff['delta_cash']))
    statuses=Counter(e['status'] for e in historical);identified=[e for e in historical if e['status']=='identified'];covered=[e for e in evaluation if e['forecast']!='abstain'];applied=[e for e in evaluation if e['apply']]
    result=dict(predictions_sha256=prediction_hash,statuses=dict(statuses),historical_identified=len(identified),historical_errors=sum(e['inferred']!=e['truth'] for e in identified),forecast_covered=len(covered),forecast_errors=sum(e['forecast']!=e['truth'] for e in covered),applied=len(applied),applied_losses=sum(e['delta_cash']<0 for e in applied),total_delta_cash=sum(e['delta_cash'] for e in evaluation),evaluation=evaluation,historical=historical,adopted=False)
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# H005: stimare la priorita concorrente dalla storia osservabile','', '84situazioni,42partite,7seed diagnostici gia esposti. Ogni previsione usa solo cinque transizioni H1 precedenti (D15-D19), osservazioni proprie/pubbliche e ordini propri. Le predizioni vengono scritte e hashate prima di leggere etichette D20 e payoff H003. Nessuna nuova policy o submission.', '', f'Testimonianze identificate: {len(identified)}/420; errori retrospettivi: {result["historical_errors"]}. Forecast non astenuti: {len(covered)}/84; errori: {result["forecast_errors"]}. Riordini H003 selezionati: {len(applied)}; negativi: {result["applied_losses"]}.', '', '## Copertura del modello inverso','','| Esito | Testimonianze |','|---|---:|']
    for status,n in sorted(statuses.items()):lines.append(f'| {status} | {n} |')
    lines+=['','## Decisione H005 sulla transizione D20 H1','','| Modello | Forecast non astenuti | Errori forecast | Riordini | Negativi | Delta cassa totale |','|---|---:|---:|---:|---:|---:|']
    for model in ['E18','E19','E20.1']:
        rr=[r for r in evaluation if r['model']==model];cc=[r for r in rr if r['forecast']!='abstain']
        lines.append(f'| {model} | {len(cc)}/28 | {sum(r["forecast"]!=r["truth"] for r in cc)} | {sum(r["apply"] for r in rr)} | {sum(r["delta_cash"]<0 for r in rr)} | {sum(r["delta_cash"] for r in rr):+.0f} |')
    lines+=['', 'Nessuna promozione. Una testimonianza storica esatta non garantisce che l avversario mantenga lo stesso ordine il giorno successivo. I payoff riusano soltanto le transizioni H003 coincidenti per hash; non sono nuove partite o risultati terminali. Le astensioni valgono nessun cambiamento, non successi. Il modello inverso supporta acquisti di prodotti/semi e ipotizza una richiesta per prodotto; non identifica in generale acquisti/rivendite compensati o vendite spezzate; i casi incompatibili vengono esclusi.', '', '[Protocollo](../../H005_PROTOCOL.md) - [Predizioni congelate](PREDICTIONS.json) - [Errori ed esiti completi](RESULT.json).']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['evaluation','historical']},indent=2))
if __name__=='__main__':main()
