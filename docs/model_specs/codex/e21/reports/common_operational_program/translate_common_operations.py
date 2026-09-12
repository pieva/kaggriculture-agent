"""Compile the complete observed common operational organization and audit parity."""
from pathlib import Path
import json, hashlib, csv, sys, html, gzip
from collections import Counter, defaultdict
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.operational_program import OperationalProgram
BASE=Path(__file__).resolve().parent
OUT=BASE/'reports/common_operational_program'
OLD=ROOT/'docs/model_specs/codex/e19/reports/restart770_20260912'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(name,value): (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def compile_program(replay,seat,episode):
    frames=[];operations=[];visits=[];market=[];active={}
    for i in range(1,len(replay['steps'])):
        pre=replay['steps'][i-1][seat]['observation'];post=replay['steps'][i][seat]['observation']
        farm=pre['farms'][seat];after=post['farms'][seat]
        positions=[farm['farmer']]+farm['hands'];positions_after=[after['farmer']]+after['hands']
        action=replay['steps'][i][seat].get('action')
        if not isinstance(action,dict):raise ValueError((episode,i,'non-dict action'))
        day,hour=pre['day']+1,pre['hour']+1
        frames.append(dict(day=day,hour=hour,source_step=i,positions_before=positions,action=action))
        commands=[action.get('farmer',['PASS'])]+action.get('hands',[])
        for w,pos in enumerate(positions):
            cmd=commands[w] if w<len(commands) else ['PASS']
            key=(day,w);visit=active.get(key)
            if visit is None or visit['position']!=pos:
                visit=dict(day=day,worker=w,position=pos,start_hour=hour,end_hour=hour,commands=[],source_steps=[])
                visits.append(visit);active[key]=visit
            visit['end_hour']=hour;visit['commands'].append(cmd);visit['source_steps'].append(i)
            inv=pre['private']['inventories'][w]
            same_day=pre['day']==post['day']
            inv_after=post['private']['inventories'][w] if same_day and w<len(post['private']['inventories']) else None
            tile=farm['tiles'][pos[1]][pos[0]]
            operations.append(dict(day=day,hour=hour,worker=w,position_before=pos,command=cmd,
                position_after=positions_after[w] if same_day and w<len(positions_after) else None,
                inventory_before=inv,inventory_after=inv_after,tile_before=tile,
                day_refresh=not same_day,source_step=i))
        for index,order in enumerate(action.get('market',[])):
            market.append(dict(day=day,hour=hour,order=index,command=order,cash_before_batch=farm['money'],
                cash_after_frame=after['money'],source_step=i))
    program=dict(episode=episode,seat=seat,mode='historical operational transcription',
        worker_identity='Farmer=0, hands=1..N. Slot identity is local to a day; refresh resets staffing.',
        frames=frames)
    return program,operations,visits,market

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    ids=read(OLD/'COMMON_ORGANIZATION.json')['common_episodes']
    candidates={x['episode']:x for x in read(OLD/'CANDIDATES.json')}
    cohort=[];groups=defaultdict(list)
    for eid in ids:
        row=candidates[eid];path=Path(row['raw_path']);r=read(path);seat=row['opponent_seat']
        program,ops,visits,market=compile_program(r,seat,eid)
        agent=OperationalProgram(program,seat)
        equal=all(agent(r['steps'][i-1][seat]['observation'],r['configuration'])==r['steps'][i][seat]['action'] for i in range(1,len(r['steps'])))
        assert equal and agent.checked==719
        signature=digest([f['action'] for f in program['frames']]);groups[signature].append(eid)
        cohort.append(dict(episode=eid,seat=seat,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),frames=719,action_parity=equal,
            unit_operations=len(ops),visits=len(visits),market_orders=len(market),action_signature=signature))
        with gzip.open(OUT/f'program_{eid}.json.gz','wt',encoding='utf-8') as f:json.dump(program,f,ensure_ascii=False)
        if eid==107083439:
            save('PROGRAM.json',program);save('OPERATIONS.json',ops);save('VISITS.json',visits);save('MARKET.json',market)
            canonical=(r,seat,program,ops,visits,market)
    save('COHORT.json',cohort);save('ACTION_GROUPS.json',list(groups.values()))
    r,seat,program,ops,visits,market=canonical
    bad=deepcopy(r['steps'][0][seat]['observation']);bad['farms'][seat]['farmer']=[0,0]
    rejected=False
    try:OperationalProgram(program,seat)(bad)
    except RuntimeError:rejected=True
    assert rejected
    # The standalone diagnostic embeds only the operation program, not observations or future prices.
    code=(BASE/'operational_program.py').read_text(encoding='utf-8')
    code+='\nPROGRAM='+repr(program)+"\ndef create_agent(context=None):\n    return OperationalProgram(PROGRAM, (context or {}).get('player_position',0), strict=True)\n"
    (OUT/'compiled_common_agent.py').write_text(code,encoding='utf-8')
    namespace={};exec(compile(code,'<compiled-common>','exec'),namespace)
    agent=namespace['create_agent']({'player_position':seat})
    assert all(agent(r['steps'][i-1][seat]['observation'])==r['steps'][i][seat]['action'] for i in range(1,720))
    for name,rows in [('OPERATIONS.csv',ops),('MARKET.csv',market),('VISITS.csv',visits)]:
        with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader()
            writer.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()} for row in rows)
    # Exact geometric changes needed to adapt this native organization to the frozen 772.
    bp=BASE/'artifacts/calendar772_c1/Base772_E18_180911301.replay.json.gz'
    with gzip.open(bp,'rt',encoding='utf-8') as f:baseline=json.load(f)
    def structures(replay,s):
        tiles=replay['steps'][-1][s]['observation']['farms'][s]['tiles']
        return {(x,y):(t['kind'],t.get('animal')) for y,row in enumerate(tiles) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind') in ('PASTURE','COOP')}
    native=structures(r,seat);target=structures(baseline,0);changes=[]
    for pos in sorted(set(native)|set(target)):
        if native.get(pos)==target.get(pos):continue
        affected=[x for x in ops if tuple(x['position_before'])==pos]
        changes.append(dict(position=list(pos),native=native.get(pos),target772=target.get(pos),
            affected_operations=len(affected),days=sorted({x['day'] for x in affected}),workers_by_day={str(d):sorted({x['worker'] for x in affected if x['day']==d}) for d in sorted({x['day'] for x in affected})}))
    save('ADAPTATION_772.json',changes)
    audit=read(OLD/'external_107083439.json')
    save('OBSERVED_ACCOUNTING.json',audit['ledger'])
    validation=dict(episodes=len(cohort),frames_verified=sum(x['frames'] for x in cohort),all_actions_equal=True,
        standalone_frames_verified=agent.checked,wrong_position_rejected=rejected,
        action_groups=list(groups.values()),native_final=native and [{'position':list(k),'structure':v} for k,v in native.items()],
        public_seed=r['configuration'].get('seed'),scope='Exact action and worker-position parity on historical input observations; not an independent simulation or a validated 772 policy.')
    save('VALIDATION.json',validation)
    # HTML exposes every hour and every worker, without loading the source file in an editor.
    header='<meta charset="utf-8"><title>Organizzazione operativa comune</title><style>body{font:16px/1.5 system-ui;max-width:1500px;margin:25px auto;padding:20px}table{border-collapse:collapse;width:100%}td,th{padding:6px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}code{white-space:pre-wrap}select{font:inherit;padding:6px}section{margin-top:24px}.scroll{max-height:650px;overflow:auto}summary{cursor:pointer;font-weight:bold}</style>'
    text=header+'<h1>Organizzazione operativa comune: traduzione completa D1–D30</h1>'
    text+=f'<p><strong>Tradotti tutti i719 turni del rappresentante107083439 e verificati tutti i {validation["frames_verified"]} turni dei nove esterni.</strong> Il programma esegue direttamente gli ordini compilati, senza riassegnare i lavori mediante priorità.</p>'
    text+='<p>È una riproduzione operativa storica, ancora nella struttura nativa14pascoli+3oche. Non è una772 adattata né una simulazione indipendente: il seed pubblico è null. Le osservazioni storiche sono utilizzate per la verifica; il programma compilato contiene solo azioni, orari e posizioni attese, nessun prezzo futuro.</p>'
    text+='<p>Documentati per ogni lavoratore: posizione, comando, inventario prima/dopo e passaggio di giornata. Le visite raggruppano i servizi consecutivi sulla stessa casella. I lavoratori sono slot della singola giornata, non identità persistenti dopo il rinnovo. L’ordine dei singoli acquisti e vendite è conservato, comprese operazioni opposte nello stesso turno.</p>'
    text+='<p><a href="compiled_common_agent.py">Programma Python eseguibile</a> · <a href="PROGRAM.json">Piano completo</a> · <a href="OPERATIONS.csv">Operazioni CSV</a> · <a href="VISITS.csv">Visite e servizi</a> · <a href="MARKET.csv">Ordini di mercato</a> · <a href="VALIDATION.json">Verifica</a></p>'
    text+='<p>I nove esterni non sono dichiarati identici: le sequenze orarie complete formano '+str(len(groups))+' gruppi. Ogni variante originale è conservata separatamente.</p>'
    text+='<label>Giorno <select id="day">'+''.join(f'<option value="{d}">D{d}</option>' for d in range(1,31))+'</select></label> <label>Lavoratore <select id="worker"><option value="all">Tutti</option>'+''.join(f'<option value="{w}">{"Agricoltore" if w==0 else "Aiutante "+str(w)}</option>' for w in range(13))+'</select></label>'
    text+='<section><h2>Sequenza operativa, percorsi e inventari</h2><div class="scroll"><table><thead><tr><th>Ora</th><th>Lavoratore</th><th>Da → a</th><th>Comando</th><th>Inventario prima → dopo</th></tr></thead><tbody id="operations"></tbody></table></div></section>'
    text+='<section><h2>Ordini di mercato, nell’ordine originale</h2><div class="scroll"><table><thead><tr><th>Ora / ordine</th><th>Operazione</th><th>Cassa prima lotto → dopo turno</th></tr></thead><tbody id="market"></tbody></table></div><p>La variazione di cassa del turno può comprendere più ordini e azioni: non è attribuita al singolo ordine. Contabilità verificata per giornata in OBSERVED_ACCOUNTING.json.</p></section>'
    text+='<section><h2>Visite e servizi consecutivi</h2><div class="scroll"><table><thead><tr><th>Ore</th><th>Lavoratore</th><th>Casella</th><th>Sequenza</th></tr></thead><tbody id="visits"></tbody></table></div></section>'
    text+='<section><h2>Adattamenti necessari alla772</h2><p>Le differenze sono localizzate, non affidate a un dispatcher generico. Devono cambiare insieme posizione, tragitto, acquisti e servizi associati; sostituire soltanto la specie o il numero finale non basta.</p><table><tr><th>Posizione</th><th>Originale →772</th><th>Operazioni da riesaminare</th></tr>'
    for c in changes:text+=f'<tr><td>{c["position"]}</td><td>{html.escape(str(c["native"]))} → {html.escape(str(c["target772"]))}</td><td>{c["affected_operations"]}</td></tr>'
    text+='</table><p>La trasposizione772 non è stata eseguita in questa traduzione. Prima del prossimo confronto economico occorre riscrivere e verificare le visite coinvolte, compresi i due pascoliQ2 e le colture che occupavano quelle caselle.</p></section>'
    payload=json.dumps(dict(operations=ops,market=market,visits=visits),ensure_ascii=False).replace('</','<\/')
    text+='<script id="data" type="application/json">'+payload+'</script>'
    text+="<script>const data=JSON.parse(document.getElementById('data').textContent);const fmt=x=>JSON.stringify(x);function fill(id,rows){const root=document.getElementById(id);root.replaceChildren();for(const cells of rows){const tr=document.createElement('tr');for(const value of cells){const td=document.createElement('td');td.textContent=value;tr.append(td)}root.append(tr)}}function render(){const day=+document.getElementById('day').value,w=document.getElementById('worker').value;const selected=x=>x.day===day&&(w==='all'||x.worker===+w);fill('operations',data.operations.filter(selected).map(x=>[x.hour,x.worker,fmt(x.position_before)+' → '+(x.day_refresh?'rinnovo giornata':fmt(x.position_after)),fmt(x.command),fmt(x.inventory_before)+' → '+(x.day_refresh?'rinnovo giornata':fmt(x.inventory_after))]));fill('market',data.market.filter(x=>x.day===day).map(x=>[x.hour+' / '+(x.order+1),fmt(x.command),x.cash_before_batch+' → '+x.cash_after_frame]));fill('visits',data.visits.filter(selected).map(x=>[x.start_hour+'–'+x.end_hour,x.worker,fmt(x.position),x.commands.map(fmt).join(' → ')]))}document.getElementById('day').onchange=render;document.getElementById('worker').onchange=render;render();</script>"
    (OUT/'REPORT.html').write_text(text,encoding='utf-8')
    save('MANIFEST.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='MANIFEST.json'})
    print(json.dumps(dict(episodes=len(cohort),frames=validation['frames_verified'],operations=len(ops),visits=len(visits),market_orders=len(market),action_groups=len(groups),adaptation_positions=len(changes))))
if __name__=='__main__':main()
