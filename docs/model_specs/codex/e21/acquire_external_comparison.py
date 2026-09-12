"""Acquire an outcome-independent recent public cohort and verify KPI inputs."""
import hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import requests
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3]
OUT=BASE/'reports/external_770_772_774_775'
RAW=ROOT/'data/replays/json/e21_external_comparison'
MODELS={'770':{'submission_id':56101593,'version':'770 V48'},
        '772':{'submission_id':56142698,'version':'772 E20.1 loaderfix (not local E20.2)'},
        '775':{'submission_id':56147218,'version':'775 E18.2 latest unchanged resubmission'}}

def main():
    OUT.mkdir(exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
    receipt=BASE/'artifacts/PUBLICATION_RECEIPT.json'
    if '--include774' in sys.argv and receipt.exists():
        sid=json.loads(receipt.read_text()).get('submission_id')
        if sid:MODELS['774']={'submission_id':sid,'version':'774 E21 Repair2'}
    now=datetime.now(timezone.utc).isoformat()
    protocol={'selected_at_utc':now,'models':MODELS,'selection':'Latest 20 completed public non-self-play episodes per exact submission ID, ordered by createTime then ID; no outcome or topology filtering. Retain failed/truncated replays as technical evidence; exclude them from complete-season aggregates explicitly.',
              'limits':'Different seeds/opponents/market schedules; descriptive comparison, not causal topology estimate. Historical V48 and E20.1 are not latest local candidates.'}
    (OUT/'ACQUISITION_PROTOCOL.json').write_text(json.dumps(protocol,indent=2)+'\n')
    inventory={}
    for model,spec in MODELS.items():
        sid=spec['submission_id']
        response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=30)
        response.raise_for_status();history=response.json()
        (OUT/f'history_{sid}.json').write_text(json.dumps(history,separators=(',',':')))
        allgames=[e for e in history['episodes'] if e.get('state')=='COMPLETED' and e.get('type')=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2]
        selected=sorted(allgames,key=lambda e:(e['createTime'],e['id']),reverse=True)[:20]
        def download(e):
            eid=e['id'];path=RAW/f'{eid}.json';url=f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json'
            try:
                if not path.exists():
                    response=requests.get(url,timeout=45);response.raise_for_status();path.write_bytes(response.content)
                raw=path.read_bytes();r=json.loads(raw)
                a=next(a for a in e['agents'] if a['submissionId']==sid);seat=a.get('index',0)
                complete=len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
                missing=set();daily=[]
                for step in r['steps']:
                    o=step[seat]['observation']
                    for key in ['farms','private','market','town','day','hour']:
                        if key not in o:missing.add(key)
                for day in range(1,31):
                    index=min(24*day-1,len(r['steps'])-1);farm=r['steps'][index][seat]['observation']['farms'][seat];counts=[0]*4
                    for y,row in enumerate(farm['tiles']):
                        for x,t in enumerate(row):
                            if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[int(x>=5)+2*int(y>=5)]+=1
                    daily.append(counts)
                return {'episode':eid,'submission_id':sid,'seat':seat,'opponent_submission_id':next(a['submissionId'] for a in e['agents'] if a['submissionId']!=sid),
                        'url':url,'raw_path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),
                        'steps':len(r['steps']),'complete':complete,'missing_observation_fields':sorted(missing),
                        'daily_topology':daily,'final_topology':daily[-1],'teams':r['info']['TeamNames'],'rewards':r['rewards'],'metadata':e}
            except Exception as exc:return {'episode':eid,'error':str(exc)}
        with ThreadPoolExecutor(max_workers=3) as pool:games=list(pool.map(download,selected))
        inventory[model]={**spec,'available_completed_public':len(allgames),'selected':len(selected),'games':games}
        (OUT/'INVENTORY.json').write_text(json.dumps({'observed_at_utc':now,'models':inventory},indent=2)+'\n')
        print(model,len(allgames),'available;',len(games),'selected;',sum(g.get('complete',False) for g in games),'complete',flush=True)
    print('Saved '+str(OUT/'INVENTORY.json'))
if __name__=='__main__':main()
