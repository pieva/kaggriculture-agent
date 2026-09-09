"""Audit only completed V51 screens, preserving all frozen reports."""
import gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.analyze_pass_reduction_v51 import analyze,OUT,OLD

def main():
    variant=sys.argv[1] if len(sys.argv)>1 else 'v51a'
    summary=analyze(variant);parity=[]
    for case in summary['partitions']['development']['cases']:
        seed,seat=case['seed'],case['seat']
        a=json.loads((OLD/f'development_v49f_{seed}_{seat}.json').read_text())
        b=json.loads((OUT/f'development_{variant}_{seed}_{seat}.json').read_text())
        ra=json.load(gzip.open(ROOT/a['details'],'rt'))['replay']
        rb=json.load(gzip.open(ROOT/b['details'],'rt'))['replay']
        mismatch=[i for i in range(1,720) if ra['steps'][i-1][seat]['observation']['day']<28 and ra['steps'][i][seat]['action']!=rb['steps'][i][seat]['action']]
        assert not mismatch,mismatch
        parity.append(dict(seed=seed,seat=seat,d1_d28_identical=True))
    frozen=[]
    for path in [ROOT/'docs/model_specs/codex/e19/artifacts/derived/v48_external_manifest.json',OLD/'candidate_f_manifest.json',OUT.parent/'pass_reduction_v50/candidate_manifest.json']:
        m=json.loads(path.read_text())
        assert hashlib.sha256((ROOT/m['output']).read_bytes()).hexdigest()==m['sha256']
        for name,sha in m['sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
        frozen.append(dict(manifest=str(path.relative_to(ROOT)),sha256=m['sha256']))
    check=dict(parity=parity,frozen=frozen,new_seeds_opened=bool(list(OUT.glob('validation_*.json'))))
    (OUT/f'integrity_{variant}.json').write_text(json.dumps(check,indent=2))
    part=summary['partitions']['development']
    lines=['# V51 — percorsi completi impegnati al giorno 29','',f"Stato: **{summary['status']}**. Confronto con V49F congelata.",'',
        'La modifica inserisce direttamente nel controllore i percorsi verificati per FEED, CARE, WATER e HARVEST. I prelievi sono esatti e condivisi; il lavoro attivo riserva tutte le proprie destinazioni. Il rientro viene incluso quando richiesto dalla policy. Le attività facoltative restano al controllore ereditato dopo queste assegnazioni.','',
        '| Seed | Posto | Δ cash | Δ PASS | Δ MOVE | Δ FEED |','|---|---:|---:|---:|---:|---:|']
    for c in part['cases']:
        d=c['delta'];lines.append(f"| {c['seed']} | {c['seat']} | {d['cash']:+.0f} | {d['pass_count']:+.0f} | {d['move']:+.0f} | {d['FEED']:+.0f} |")
    lines+=['','Medie delle differenze:', '', '| Metrica | Δ medio |','|---|---:|']
    for k,v in part['mean_delta'].items():lines.append(f'| {k} | {v:+.4f} |')
    lines+=['','Criteri:', '']+[f"- {k}: {'PASS' if v else 'FAIL'}" for k,v in part['gates'].items()]
    lines+=['','## Verifiche e limiti','',f"{part['n']} simulazioni complete sui seed di sviluppo già esposti. Azioni D1–D28 identiche alla baseline in tutti i casi. V48, V49F e V50: bundle e sorgenti verificati contro i manifest congelati.",
        '', 'Runtime diagnostico con actTimeout=120: non è una certificazione del runtime standard. Nessuna submission. I seed nuovi non sono stati usati.' if not check['new_seeds_opened'] else 'Consultare gli audit di validazione.',
        '', '[Risultati e gate](summary_v51a.json) · [Integrità](integrity.json) · [Protocollo](PROTOCOL_IT.md)']
    (OUT/f'REPORT_{variant.upper()}_IT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(check))

if __name__=='__main__':main()
