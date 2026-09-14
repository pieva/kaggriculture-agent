"""Trace the late empty Q2 coop and proposed (4,5) site in 20 frozen E22.1 games."""
import hashlib
import html
import json
import statistics as st
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT/'docs/model_specs/codex/e22/reports/external_e22_2_20260914'
OUT = ROOT/'docs/model_specs/codex/e22/reports/e22_1_q2_coop_20260914'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cohort=[g for g in json.loads((SOURCE/'COHORT.json').read_text()) if g['submission']==56206528]
    rows=[]
    for g in cohort:
        raw=(ROOT/g['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==g['sha256']
        game=json.loads(raw);seat=g['seat']
        profile=json.loads((SOURCE/'profiles'/f"56206528_{g['episode']}.json").read_text())['own']
        sites={}
        for x,y in [(3,7),(4,5)]:
            transitions=[e for e in profile['transitions'] if (e['x'],e['y'])==(x,y)]
            harvests=[e for e in profile['harvest_events'] if (e['x'],e['y'])==(x,y)]
            occupied=[];builds=[];idle=[]
            for i,step in enumerate(game['steps']):
                obs=step[seat]['observation'];farm=obs['farms'][seat];tile=farm['tiles'][y][x]
                if isinstance(tile,dict) and tile.get('animal'):
                    occupied.append(dict(step=i,animal=tile['animal']))
                if i==719:continue
                a=game['steps'][i+1][seat]['action']
                for w,(pos,cmd) in enumerate(zip([farm['farmer']]+farm['hands'],[a['farmer']]+a['hands'])):
                    if tuple(pos)!=(x,y):continue
                    if cmd[0]=='BUILD_COOP':builds.append(dict(day=i//24+1,hour=i%24+1,worker=w,tile_before=tile))
                    if i>=672 and tile is None and cmd==['PASS']:
                        idle.append(dict(day=i//24+1,hour=i%24+1,worker=w))
            sites[f'{x},{y}']=dict(transitions=transitions,harvests=harvests,
                harvested=dict(sum((Counter(e['gain']) for e in harvests),Counter())),
                animal_states=occupied,build_requests=builds,empty_idle_slots_d29_d30=idle)
        rows.append(dict(episode=g['episode'],seat=seat,replay_sha256=g['sha256'],sites=sites))
    old=[r['sites']['3,7'] for r in rows];near=[r['sites']['4,5'] for r in rows]
    summary=dict(games=len(rows),coop_ever_occupied=sum(bool(s['animal_states']) for s in old),
        coop_egg_units=sum(s['harvested'].get('EGG',0) for s in old),
        build_requests=dict(Counter(f"D{b['day']} H{b['hour']} worker {b['worker']}" for s in old for b in s['build_requests'])),
        builds_executed=sum(e['command'][0]=='BUILD_COOP' for s in old for e in s['transitions']),
        old_site_strawberries=[s['harvested'].get('STRAWBERRY',0) for s in old],
        near_site_strawberries=[s['harvested'].get('STRAWBERRY',0) for s in near],
        near_site_digs=dict(Counter(f"D{e['day']} H{e['hour']}" for s in near for e in s['transitions'] if e['command'][0]=='DIG')),
        near_site_idle_slots=sum(len(s['empty_idle_slots_d29_d30']) for s in near),
        direct_coop_sales_cash=0,build_cash_cost=0,goose_purchase_cost=300,goose_first_production_delay_days=4,
        new_policy_created=False,simulated_roi_of_new_goose=False)
    assert summary['coop_ever_occupied']==0 and summary['coop_egg_units']==0
    (OUT/'EVIDENCE.json').write_text(json.dumps(rows,indent=2))
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2))
    n=summary['near_site_strawberries'];o=summary['old_site_strawberries']
    md=f'''# E22.1 — pollaio Q2 e alternativa (4,5)

Coordinate `(x,y)` a base zero; Q2 è il quadrante sud-ovest. Controllati tutti i 720 stati di 20 replay E22.1 (submission 56206528), con transizioni e raccolte già riconciliate nel motore.

**Il pollaio in (3,7) non produce reddito nel calendario E22.1.** Non ospita animali in nessuno dei 20 replay: zero uova, zero fertilizzante animale e zero vendite attribuibili al pollaio. La costruzione è richiesta a D29 H5 dal lavoratore 6; eseguita {summary['builds_executed']}/20 volte. BUILD_COOP non costa denaro, ma occupa un comando. La struttura vuota non aggiunge valore al premio finale, che coincide con la cassa.

Non va confuso il pollaio con la casella: prima della costruzione, (3,7) ospita fragole, con {st.mean(o):.1f} unità raccolte medie (min–max {min(o)}–{max(o)}). Il pollaio compare dopo la rimozione della coltura a fine ciclo.

## Spostamento in (4,5)

- È una casella adiacente al magazzino, quindi geometricamente più comoda per prelevare mangime e consegnare prodotti. PICKUP e DROP non richiedono un pollaio: l'accesso al magazzino funziona anche su coltura, struttura o terreno libero.
- Nel calendario esistente ospita fragole: {st.mean(n):.1f} unità raccolte medie (min–max {min(n)}–{max(n)}), prima della rimozione a D29 H3. Le raccolte riuscite e le eccezioni sono elencate per replay in EVIDENCE.json.
- Uno spostamento a fine ciclo è tecnicamente possibile dopo aver liberato la casella, ma richiede assegnare il comando a un lavoratore presente. Spostare la sola struttura vuota non genera ricavi.
- Collocare un'oca a D29 sarebbe troppo tardi: la prima produzione arriva quattro giorni dopo il collocamento, oltre D30. Per un quarto pollaio produttivo occorre anticipare l'investimento, comprare un'oca (300), fornire grano e cure, riprogrammare raccolta/vendita e confrontare il risultato con le fragole sostituite.

## Indicazione operativa

**Non spostare automaticamente il pollaio vuoto.** Il primo intervento candidato è eliminare il BUILD_COOP tardivo, preservando il calendario delle colture. Un quarto pollaio anticipato in (4,5) è un esperimento strategico distinto, con un costo opportunità misurabile; questo audit non ne dimostra la redditività.

Il lavoratore 6 non compie una missione isolata per il pollaio: dopo (3,7) prosegue verso (2,7) e le colture sud-occidentali. Eliminare il BUILD non consente quindi di cancellare automaticamente tutti gli spostamenti di quel percorso. Non sono state modificate E22.1 né le sue rotte.

[Dati per replay](EVIDENCE.json) · [Riepilogo](SUMMARY.json). Regole controllate nel motore installato: `_apply_unit_action` (costruzione), `_daily_refresh_animals` (maturazione), assegnazione finale `reward = money`.
'''
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body=''.join('<p>'+html.escape(p).replace('\n','<br>')+'</p>' for p in md.split('\n\n'))
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E22.1 · pollaio Q2</title><style>body{font:16px/1.6 system-ui;max-width:950px;margin:40px auto;padding:0 20px;color:#24344b;background:#f6f8fa}p{padding:12px;background:white;border-radius:8px}</style>'+body,encoding='utf-8')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
