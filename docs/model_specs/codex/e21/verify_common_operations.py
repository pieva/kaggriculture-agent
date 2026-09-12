"""Cross-replay verification of the translated worker organization."""
from pathlib import Path
from collections import defaultdict
import json,gzip,hashlib
from html import escape
BASE=Path(__file__).resolve().parent
OUT=BASE/'reports/common_operational_program'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def unit(frame):return {k:frame['action'].get(k) for k in ('farmer','hands')}
def main():
    programs={};groups=defaultdict(list)
    for p in sorted(OUT.glob('program_*.json.gz')):
        with gzip.open(p,'rt',encoding='utf-8') as f:program=json.load(f)
        programs[program['episode']]=program
        key=json.dumps([unit(x) for x in program['frames']],sort_keys=True)
        groups[key].append(program['episode'])
    ref=programs[107083439];comparisons=[]
    for eid,program in programs.items():
        row=dict(episode=eid)
        for label,extract in [('workers',unit),('positions',lambda f:f['positions_before']),('market',lambda f:f['action'].get('market'))]:
            matches=[extract(a)==extract(b) for a,b in zip(ref['frames'],program['frames'])]
            index=next((i for i,m in enumerate(matches) if not m),None)
            row[label]=dict(equal_frames=sum(matches),first_difference=None if index is None else dict(day=ref['frames'][index]['day'],hour=ref['frames'][index]['hour'],canonical=extract(ref['frames'][index]),observed=extract(program['frames'][index])))
        comparisons.append(row)
    same=[x['episode'] for x in comparisons if x['workers']['equal_frames']==719 and x['positions']['equal_frames']==719]
    assert len(same)==5
    ops=read(OUT/'OPERATIONS.json');moves=[];directions={'NORTH':(0,-1),'SOUTH':(0,1),'EAST':(1,0),'WEST':(-1,0)}
    for op in ops:
        if op['command'][0] not in directions or op['day_refresh']:continue
        dx,dy=directions[op['command'][0]];x,y=op['position_before'];expected=[x+dx,y+dy]
        if expected!=op['position_after']:moves.append(dict(day=op['day'],hour=op['hour'],worker=op['worker'],command=op['command'],expected=expected,observed=op['position_after']))
    result=dict(same_complete_worker_program=same,unit_groups=list(groups.values()),comparisons=comparisons,
        cardinal_movement_mismatches=moves,scope='Unit commands AND positions identical across five independent historical games. Market quantities are not one universal inferred rule.')
    (OUT/'CROSS_REPLAY_VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    report=OUT/'REPORT.html';text=report.read_text(encoding='utf-8')
    section='<section><h2>Verifica incrociata: stessa organizzazione in cinque partite</h2><p><strong>Lo stesso programma dei lavoratori coincide per719turni su719, incluse tutte le posizioni, in cinque replay diversi.</strong> Non è soltanto ricopiare ogni replay su sé stesso. Gli ordini di mercato possono invece differire: il programma economico compilato resta quello del rappresentante, non una regola adattativa privata ricostruita.</p><table><tr><th>Episodio</th><th>Turni comandi uguali</th><th>Turni posizioni uguali</th><th>Turni mercato uguali</th><th>Prima differenza nei comandi</th></tr>'
    for row in comparisons:
        first=row['workers']['first_difference'];when='nessuna' if first is None else f"D{first['day']} H{first['hour']}"
        section+=f"<tr><td>{row['episode']}</td><td>{row['workers']['equal_frames']}/719</td><td>{row['positions']['equal_frames']}/719</td><td>{row['market']['equal_frames']}/719</td><td>{when}</td></tr>"
    section+='</table><p>Le sequenze dei lavoratori formano cinque gruppi,5+1+1+1+1; le sequenze complete con il mercato ne formano nove. Le differenze sono conservate con il primo comando divergente in CROSS_REPLAY_VERIFICATION.json. Controllo indipendente dei movimenti cardinali sulle osservazioni consecutive: '+str(len(moves))+' differenze, escluse le transizioni di giornata.</p></section>'
    marker='<label>Giorno '
    text=text.replace(marker,section+marker)
    report.write_text(text,encoding='utf-8')
    print(json.dumps(dict(shared_full_program=same,movement_mismatches=len(moves))))
if __name__=='__main__':main()
