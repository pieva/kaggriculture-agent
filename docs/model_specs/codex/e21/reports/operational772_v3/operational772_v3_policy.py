"""Observed-state execution of compiled daily worker routes, no priority auction."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import json
BASE=Path(__file__).resolve().parent
ANIMALS={'COW':400,'SHEEP':500,'GOOSE':300}
FIRST={'WHEAT':2,'CARROT':2,'MELON':10,'STRAWBERRY':10,'TOMATO':8}
SHEDS=[(4,4),(5,4),(4,5),(5,5)]
class Agent:
    def __init__(self,context=None,adapt=True):
        self.seat=(context or {}).get('player_position',0)
        self.plan=json.loads((BASE/'reports/operational772_v3'/('PLAN_772.json' if adapt else 'PLAN_NATIVE.json')).read_text(encoding='utf-8'))
        self.adapt=adapt;self.day=None;self.queues={};self.indices={};self.carry={};self.log=[];self.metrics=Counter();self.error_count=0;self.core=self
    def move(self,pos,target):
        if pos[0]!=target[0]:return ['EAST' if pos[0]<target[0] else 'WEST']
        if pos[1]!=target[1]:return ['SOUTH' if pos[1]<target[1] else 'NORTH']
        return None
    def start_day(self,day):
        if self.day is not None:
            for w,q in self.queues.items():
                left=q[self.indices.get(w,0):]
                if left:self.log.append(dict(day=self.day,worker=w,unfinished=deepcopy(left)))
                # Carry only unexecuted construction/placement: crop backlog is
                # recorded as a missed biological deadline, never disguised as on-time.
                self.carry[w]=[j for j in left if j['command'][0] in {'BUILD_PASTURE','BUILD_COOP','PLACE'}]
        self.day=day
        self.queues={int(w):deepcopy(q) for w,q in self.plan['days'].get(str(day),{}).items()}
        for w,q in self.carry.items():self.queues.setdefault(w,[])[:0]=q
        self.indices={w:0 for w in self.queues}
    def market(self,obs):
        farm=obs['farms'][self.seat];private=obs['private'];day=obs['day']+1;hour=obs['hour']+1
        original=deepcopy(self.plan['market_frames'].get(f'{day}:{hour}',[]))
        orders=[o for o in original if o and o[0]!='BUY_ANIMAL']
        fertilizer_need=sum(j['command'][0]=='FERTILIZE' for w,q in self.queues.items() for j in q[self.indices.get(w,0):])
        fertilizer_carried=sum(i.get('FERTILIZER',0) for i in private['inventories'])
        fertilizer_reserve=max(0,fertilizer_need-fertilizer_carried)
        revised=[]
        for order in orders:
            if order[:2]==['SELL','FERTILIZER']:
                quantity=min(order[2],max(0,private['shed'].get('FERTILIZER',0)-fertilizer_reserve))
                if quantity:revised.append(['SELL','FERTILIZER',quantity])
            else:revised.append(order)
        orders=revised
        # Keep the historical batch order for products/seeds/hires/land.
        # Replace animal purchases by actual remaining adapted placements.
        missing=Counter();seen=set()
        for d,workers in self.plan['days'].items():
            if int(d)>day:continue
            for queue in workers.values():
                for j in queue:
                    if j['command'][0]!='PLACE':continue
                    p=tuple(j['position']);species=j['command'][1]
                    if species not in ANIMALS or p in seen:continue
                    seen.add(p);tile=farm['tiles'][p[1]][p[0]]
                    if not isinstance(tile,dict) or not tile.get('animal'):missing[species]+=1
        for species,n in missing.items():
            owned=private['shed'].get(species,0)+sum(i.get(species,0) for i in private['inventories'])
            if n>owned and len(orders)<10:orders.append(['BUY_ANIMAL',species,n-owned])
        # Changed animal production is sold from observed stock, not historical
        # quantities. Supplemental orders do not net out original round trips.
        already={o[1] for o in orders if o[0]=='SELL'}
        for item,n in private['shed'].items():
            if item=='FERTILIZER':n=max(0,n-fertilizer_reserve)
            if item not in ANIMALS and (item!='WHEAT' or day==30) and n>0 and item not in already and len(orders)<10:
                orders.append(['SELL',item,n])
        wheat=private['shed'].get('WHEAT',0)+sum(i.get('WHEAT',0) for i in private['inventories'])
        need=sum(bool(t.get('animal')) and not t.get('fed_today') for row in farm['tiles'] for t in row if isinstance(t,dict))
        if need>wheat and len(orders)<10 and not any(o[:2]==['BUY_PRODUCT','WHEAT'] for o in orders):orders.append(['BUY_PRODUCT','WHEAT',need-wheat])
        self.orders=orders
        return orders
    def act_worker(self,w,obs,shared):
        farm=obs['farms'][self.seat];private=obs['private'];positions=[farm['farmer']]+farm['hands'];pos=tuple(positions[w]);inv=private['inventories'][w]
        q=self.queues.get(w,[])
        if obs['day']==29 and any(n>0 for item,n in inv.items() if item not in ANIMALS):
            shed=min(SHEDS,key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))
            distance=abs(pos[0]-shed[0])+abs(pos[1]-shed[1])
            if 23-obs['hour']<=distance+2:
                self.metrics['terminal_return']+=1
                return self.move(pos,shed) or ['DROP']
        for _ in range(len(q)+2):
            index=self.indices.get(w,0)
            if index>=len(q):return ['PASS']
            j=q[index];target=tuple(j['position']);cmd=j['command'];op=cmd[0];tile=farm['tiles'][target[1]][target[0]]
            def done():self.indices[w]=index+1
            # Skip already satisfied or no-longer-applicable services before travel.
            if op in {'FEED','CARE','COLLECT_FERTILIZER'}:
                if not isinstance(tile,dict) or not tile.get('animal'):done();continue
                field={'FEED':'fed_today','CARE':'cared_today','COLLECT_FERTILIZER':'fertilizer_available'}[op]
                if (op!='COLLECT_FERTILIZER' and tile.get(field)) or (op=='COLLECT_FERTILIZER' and not tile.get(field)):done();continue
            if op=='WATER' and (not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('watered_today')):done();continue
            if op=='FERTILIZE' and (not isinstance(tile,dict) or not tile.get('crop') or tile.get('fertilized_until_day',-1)>=obs['day']):done();continue
            if op=='HARVEST' and (not isinstance(tile,dict) or not tile.get('yield_units',0)):done();continue
            if op=='PLACE' and isinstance(tile,dict) and tile.get('animal'):done();continue
            if op.startswith('BUILD_') and isinstance(tile,dict) and tile.get('kind')==op[6:]:done();continue
            if op=='DIG' and tile is None:done();continue
            if op=='PLANT' and isinstance(tile,dict) and tile.get('crop')==cmd[1] and tile.get('planted_day',-1)>=j['source_day']-1:done();continue
            resource=cmd[1] if op=='PLACE' and cmd[1] in ANIMALS else 'WHEAT' if op=='FEED' else 'FERTILIZER' if op=='FERTILIZE' else None
            if resource and inv.get(resource,0)<=0:
                shed=min(SHEDS,key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))
                movement=self.move(pos,shed)
                if movement:return movement
                if shared['shed'].get(resource,0)>0:
                    # One animal, or feed for the remaining assigned visits.
                    n=1 if resource in ANIMALS else max(1,sum(t['command'][0]==('FEED' if resource=='WHEAT' else 'FERTILIZE') for t in q[index:]))
                    n=min(n,shared['shed'][resource]);shared['shed'][resource]-=n
                    return ['PICKUP',resource,n]
                self.metrics['wait_'+resource]+=1;return ['PASS']
            movement=self.move(pos,target)
            if movement:return movement
            if tile=='LOCKED' and op not in {'PICKUP','DROP'}:self.metrics['wait_land']+=1;return ['PASS']
            if op=='PICKUP':
                item=cmd[1];n=min(cmd[2] if len(cmd)>2 else 1,shared['shed'].get(item,0))
                if n<=0:done();continue
                shared['shed'][item]-=n;done();return ['PICKUP',item,n]
            if op=='PLANT':
                if isinstance(tile,dict):
                    if tile.get('kind')=='WEED':return ['DIG']
                    if tile.get('crop'):
                        crop=tile['crop'];age=obs['day']-tile['planted_day']
                        if tile.get('yield_units',0) and age>=FIRST[crop]:
                            self.metrics['dependency_harvest']+=1;return ['HARVEST']
                        if crop in {'STRAWBERRY','TOMATO'} and age>=FIRST[crop]+(6 if crop=='STRAWBERRY' else 3):
                            self.metrics['dependency_dig']+=1;return ['DIG']
                    self.metrics['blocked_crop_slot']+=1;return ['PASS']
                if shared['seeds'].get(cmd[1],0)<=0:
                    if len(self.orders)<10 and not any(x[:2]==['BUY_SEED',cmd[1]] for x in self.orders):self.orders.append(['BUY_SEED',cmd[1],1])
                    self.metrics['wait_seed']+=1;return ['PASS']
                shared['seeds'][cmd[1]]-=1
            if op.startswith('BUILD_') and isinstance(tile,dict):
                if tile.get('kind')=='WEED':return ['DIG']
                if tile.get('crop') and tile.get('yield_units',0) and obs['day']-tile['planted_day']>=FIRST[tile['crop']]:
                    self.metrics['dependency_harvest']+=1;return ['HARVEST']
                self.metrics['blocked_structure_slot']+=1;return ['PASS']
            if op=='HARVEST' and tile.get('crop') and obs['day']-tile['planted_day']<FIRST[tile['crop']]:
                self.metrics['wait_maturity']+=1;return ['PASS']
            if op=='DROP' and not any(inv.values()):done();continue
            done();self.metrics['issued_'+op]+=1
            return deepcopy(cmd)
        raise RuntimeError('Queue failed to advance')
    def __call__(self,obs,cfg=None):
        day=obs['day']+1
        if day!=self.day:self.start_day(day)
        market=self.market(obs)
        shared=deepcopy({k:obs['private'][k] for k in ['shed','seeds']})
        n=len(obs['farms'][self.seat]['hands'])+1
        actions=[self.act_worker(w,obs,shared) for w in range(n)]
        return dict(farmer=actions[0],hands=actions[1:],market=market[:10])
def create_agent(context=None):return Agent(context,True)
