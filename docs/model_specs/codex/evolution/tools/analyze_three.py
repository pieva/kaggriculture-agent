"""Three-model diagnostic cohort: provenance, economic windows and paired contrasts."""
import csv,gzip,hashlib,json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/diagnostic_20260910'
SOURCE=ROOT/'docs/model_specs/codex/e20/artifacts/e20_1_confirmation'
MODELS=['E18','E19','E20.1'];WINDOWS=[('D15-D19',14,19),('D20-D24',19,24),('D25-D30',24,30)]
def main():
    rows=[];manifest=[];daily=[]
    for path in sorted(SOURCE.glob('*.kpi.json')):
        c=json.loads(path.read_text());meta_path=path.with_name(path.name.replace('.kpi.json','.json'));meta=json.loads(meta_path.read_text())
        assert all(x['calls']==719 and x['core_errors'] in [0,None] for x in meta['runtime'])
        replay_path=meta_path.with_suffix('.replay.json.gz')
        with gzip.open(replay_path,'rb') as f:raw=f.read()
        assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256']==c['replay_sha256']
        r=json.loads(raw);assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
        manifest.append(dict(path=str(meta_path.relative_to(ROOT)),seed=c['seed'],agents=meta['agents'],replay_sha256=meta['replay_sha256'],metadata_sha256=hashlib.sha256(meta_path.read_bytes()).hexdigest(),kpi_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        for seat,s in enumerate(c['sides']):
            assert not s['ledger']['cash_parity_errors']
            opponent=c['sides'][1-seat]['name'];win={}
            for label,start,end in WINDOWS:
                ds=s['ledger']['daily'][start:end]
                sales=sum(sum(d['sales_cash'].values()) for d in ds);purchases=sum(sum(d['purchase_cash'].values()) for d in ds)
                wages=sum(d['hire_cash'] for d in ds);land=sum(d['land_cash'] for d in ds);unit=sum(d['unit_cash_delta'] for d in ds)
                cash_start=r['steps'][start*24][seat]['observation']['farms'][seat]['money']
                cash_end=r['steps'][min(end*24,719)][seat]['observation']['farms'][seat]['money']
                net=sales-purchases-wages-land+unit
                assert abs(cash_end-cash_start-net)<1e-6,(path,label,cash_end-cash_start,net)
                win[label]=dict(cash_start=cash_start,cash_end=cash_end,net=net,sales=sales,purchases=purchases,wages=wages,land=land,unit_cash=unit,
                    sales_by_product={k:sum(d['sales_cash'].get(k,0) for d in ds) for k in sorted({k for d in ds for k in d['sales_cash']})},
                    MOVE=sum(s['kpi'][d]['MOVE'] for d in range(start,end)),PASS=sum(s['kpi'][d]['PASS'] for d in range(start,end)),crop_tiles_mean=mean(s['kpi'][d]['crop_tiles'] for d in range(start,end)))
            rows.append(dict(seed=c['seed'],model=s['name'],opponent=opponent,seat=seat,reward=s['reward'],windows=win))
            daily.extend(dict(seed=c['seed'],model=s['name'],opponent=opponent,seat=seat,day=d+1,**{k:v[k] for k,_,_ in FIELDS}) for d,v in enumerate(s['kpi']))
    seeds=sorted({r['seed'] for r in rows});assert len(manifest)==42 and len(seeds)==7
    assert {(r['seed'],r['model'],r['opponent'],r['seat']) for r in rows}=={(s,m,o,w) for s in seeds for m in MODELS for o in MODELS if m!=o for w in (0,1)}
    summary={m:dict(cash=mean(r['reward'] for r in rows if r['model']==m),windows={label:{k:mean(r['windows'][label][k] for r in rows if r['model']==m) for k in ['net','sales','purchases','wages','MOVE','PASS','crop_tiles_mean']} for label,_,_ in WINDOWS}) for m in MODELS}
    paired=[]
    for a,b,opponent in [('E19','E20.1','E18'),('E18','E19','E20.1'),('E18','E20.1','E19')]:
        contrasts=[]
        for seed in seeds:
            aa=[r for r in rows if r['seed']==seed and r['model']==a and r['opponent']==opponent];bb=[r for r in rows if r['seed']==seed and r['model']==b and r['opponent']==opponent]
            contrasts.append(dict(seed=seed,delta_cash_b_minus_a=mean(r['reward'] for r in bb)-mean(r['reward'] for r in aa),windows={label:{k:mean(r['windows'][label][k] for r in bb)-mean(r['windows'][label][k] for r in aa) for k in ['net','sales','purchases','wages']} for label,_,_ in WINDOWS}))
        paired.append(dict(a=a,b=b,opponent=opponent,mean_delta=mean(x['delta_cash_b_minus_a'] for x in contrasts),seeds_positive=sum(x['delta_cash_b_minus_a']>0 for x in contrasts),contrasts=contrasts))
    OUT.mkdir(parents=True,exist_ok=True)
    result=dict(reference='E18',cohort_role='diagnostic_previously_exposed',games=42,seeds=seeds,summary=summary,paired_common_opponent=paired,rows=rows)
    (OUT/'data.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'COHORT.json').write_text(json.dumps(dict(role='diagnostic_not_holdout',games=manifest),indent=2)+'\n')
    with (OUT/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(daily[0]));writer.writeheader();writer.writerows(daily)
    lines=['# E18, E19, E20.1: banco diagnostico a tre','', 'E18 e il riferimento principale. 42 partite esistenti, sette seed gia esposti, tutti gli accoppiamenti e ruoli. Nessun nuovo candidato. Le differenze descrivono comportamenti completi; non isolano la causa e non sono una validazione indipendente.', '', 'Finestre senza doppio conteggio: D15-D19, D20-D24, D25-D30. Cassa ai confini esatti del giorno, ultimo confine terminale. Ogni variazione di cassa e riconciliata con vendite - acquisti - manodopera - terreno + effetti monetari delle azioni. I 22 KPI conservano i checkpoint storici, che precedono l ultima azione giornaliera.', '', '| Modello | Cassa finale media |','|---|---:|']
    for m in MODELS:lines.append(f'| {m} | {summary[m]["cash"]:.1f} |')
    for label,_,_ in WINDOWS:
        lines+=['',f'## {label}','','| Modello | Cassa generata | Vendite | Acquisti | Manodopera | MOVE | PASS | Coltivate medie |','|---|---:|---:|---:|---:|---:|---:|---:|']
        for m in MODELS:
            w=summary[m]['windows'][label];lines.append('| '+m+' | '+' | '.join(f'{w[k]:.1f}' for k in ['net','sales','purchases','wages','MOVE','PASS','crop_tiles_mean'])+' |')
    lines+=['','## Confronti con lo stesso avversario','','Delta secondo modello meno primo; ruoli mediati dentro ogni seed. Sette unita diagnostiche, non quattordici repliche indipendenti. L avversario reagisce alla partita: anche questo confronto non e un intervento causale isolato.','','| Primo | Secondo | Avversario comune | Delta cassa | Seed positivi |','|---|---|---|---:|---:|']
    for p in paired:lines.append(f'| {p["a"]} | {p["b"]} | {p["opponent"]} | {p["mean_delta"]:+.1f} | {p["seeds_positive"]}/7 |')
    lines+=['','## Scomposizione del divario E20.1 rispetto a E19, avversario E18','',
            '| Finestra | Delta cassa generata | Delta vendite | Delta acquisti | Delta manodopera |','|---|---:|---:|---:|---:|']
    for label,_,_ in WINDOWS:
        contrasts=paired[0]['contrasts']
        lines.append('| '+label+' | '+' | '.join(f'{mean(x["windows"][label][k] for x in contrasts):+.1f}' for k in ['net','sales','purchases','wages'])+' |')
    lines+=['', 'Qui il costo dei manovali non spiega il divario D15-D24: e uguale. La differenza contabile e soprattutto nelle vendite. D25-D30 contribuiscono anche maggiori acquisti. Questo localizza la domanda, ma non distingue ancora volumi prodotti, prezzi di vendita e tempi di consegna.',
            '', 'E18 resta il riferimento esterno di progetto. Il torneo interno non dimostra una sua superiorita universale: i modelli scambiano maggiore produzione/vendite con minori acquisti. La selezione futura deve conservare il dettaglio per avversario, finestra e seed.',
            '', '[Primo esperimento da stato salvato](H001_REPORT.md) - [Protocollo del metodo](../../PROTOCOL.md).']
    incidents=[]
    for pair in paired:
        ordered=sorted(pair['contrasts'],key=lambda x:x['delta_cash_b_minus_a'])
        for label,item in [('minimum_delta',ordered[0]),('median_delta',ordered[len(ordered)//2]),('maximum_delta',ordered[-1])]:
            incidents.append(dict(selection=label,model_a=pair['a'],model_b=pair['b'],opponent=pair['opponent'],**item))
    (OUT/'INCIDENTS.json').write_text(json.dumps(dict(selection_rule='minimum, median and maximum signed delta for each common-opponent contrast; descriptive selection, not independent tests',incidents=incidents),indent=2)+'\n')
    lines+=['','[22 KPI per partita, con identita dell avversario](daily_22_kpi.csv) - [Dati e contrasti per seed](data.json) - [Traiettorie dei 22 KPI, torneo originale](../../../e20/reports/e20_1_confirmation/REPORT.html).']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
