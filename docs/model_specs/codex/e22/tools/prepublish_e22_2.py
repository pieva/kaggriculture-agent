"""Prepublication review of the exact E22.2 bytes against all recorded trials."""
import ast
import contextlib
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
from time import perf_counter

ROOT=Path(__file__).resolve().parents[5]
BUNDLE=ROOT/'submission/submission_codex_e22_2_pascoli.py'
ART=ROOT/'docs/model_specs/codex/e22/artifacts/q0_8c9s_v1'
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_2_release'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    source=BUNDLE.read_text(encoding='utf-8'); sha=hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
    assert sha=='df6991a5619f09e91bef6b6ac7034ade10f87c59e577d49c19cf197cd5cd2dcd'
    imports=[a.name for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Import) for a in n.names]
    assert set(imports)=={'base64','zlib','json','copy'}
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    records=[]; count=0; slowest=0
    for path in sorted(ART.glob('*.json')):
        row=json.loads(path.read_text(encoding='utf-8')); seat=row['seat']
        assert row['hashes']['candidate']==sha
        game=json.load(gzip.open(path.with_suffix('.replay.json.gz'),'rt',encoding='utf-8'))
        agent=get_last_callable(source)
        assert agent.__name__=='agent'
        assert len(game['steps'])==720 and all(s['status']=='DONE' for s in game['steps'][-1])
        unfed=[]
        for i in range(719):
            obs=game['steps'][i][seat]['observation']; before=copy.deepcopy(obs)
            start=perf_counter(); action=agent(obs,game['configuration']); slowest=max(slowest,perf_counter()-start)
            assert action==game['steps'][i+1][seat]['action'] and obs==before
            assert len(action['market'])<=10
            assert action==agent(obs,game['configuration'])
            count+=1
            # At each real daily refresh, positive consecutive_unfed on an
            # animal is evidence of a missed feeding, irrespective of request.
            if i%24==23:
                f=game['steps'][i+1][seat]['observation']['farms'][seat]
                for x,y in [(4,1),(3,2),(2,3)]:
                    t=f['tiles'][y][x]
                    if isinstance(t,dict) and t.get('animal')=='SHEEP' and t.get('consecutive_unfed',0):
                        unfed.append(dict(day=i//24+1,x=x,y=y,consecutive=t['consecutive_unfed']))
        ledger=row['ledgers'][seat]; terminal=row['terminal'][seat]
        assert row['checks']['mix']=={'COW':8,'SHEEP':9} and not ledger['animal_escapes']
        assert all(l['cash_parity_errors']==0 for l in row['ledgers'])
        for product in ['MILK','WOOL','EGG']:
            assert sum(d['harvested'].get(product,0) for d in ledger['daily'])==sum(d['sold_units'].get(product,0) for d in ledger['daily'])
            assert all(terminal[k].get(product,0)==0 for k in ['shed','carried','tile_yield_units'])
        records.append(dict(seed=row['seed'],seat=seat,unfed_target_days=unfed,terminal=terminal))
        print('VERIFIED',row['seed'],seat,flush=True)
    assert len(records)==14 and count==10066
    result=dict(file=str(BUNDLE.relative_to(ROOT)),sha256=sha,loader='agent',games=14,
                action_parity=count,repeated_call_parity=count,observation_mutations=0,
                max_local_call_seconds=slowest,imports=imports,blocking_errors=[],
                code_changed=False,new_simulations=0,records=records,
                findings=['Occasional single missed feeding days on the three target sheep; no escapes in the 14 tests. Existing scheduling limitation, not repaired in this release.',
                          'Two carried fertilizer units remain at D30; no unsold milk, wool or eggs.',
                          'Fixed routes and purchases do not recover from arbitrary cash/state divergence outside the tested seeds.',
                          'Wool SELL sizes differ from E22.1 before D11 too; external comparison is the whole E22.2 policy.'],
                decision='Publish exact tested E22.2 for user-authorized external diagnostic; no claim of optimality or internal superiority.')
    (OUT/'PREPUBLICATION_REVIEW.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    md='# E22.2 — verifica prima della pubblicazione\n\nNessun errore bloccante rilevato. Bundle invariato: '+sha+'\n\n'
    md+='Caricatore reale: funzione finale agent. Parità su 10.066 azioni in 14 replay, chiamate ripetute deterministiche, osservazioni immutate, solo libreria standard. Mix finale 8 mucche e 9 pecore; zero fughe ed errori contabili; latte/lana/uova raccolti interamente venduti.\n\n'
    md+='Criticità note non corrette per conservare la versione selezionata: singoli giorni senza alimentazione efficace; due unità di fertilizzante trasportate a fine partita; nessun recupero generale da divergenze di cassa o stato. Le vendite lana cambiano anche prima di D11. Non sono prove di ottimalità: il test esterno è diagnostico.\n\n[Dettaglio per partita](PREPUBLICATION_REVIEW.json). Nessuna nuova simulazione e nessun uso dei seed riservati.\n'
    (OUT/'REVIEW.md').write_text(md,encoding='utf-8')
    print('READY',sha,'actions',count,'max_seconds',slowest,flush=True)

if __name__=='__main__':main()
