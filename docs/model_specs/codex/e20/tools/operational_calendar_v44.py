"""E20.9: remove opening wheat round trip; two late tomato missions."""
from copy import deepcopy
from docs.model_specs.codex.e20.tools.operational_calendar_goose2 import Agent as Parent

TOMATO_SITES=((3,7),(4,8))

class Agent(Parent):
    def __init__(self,context=None,tomatoes=True):
        super().__init__(context)
        self.tomatoes=tomatoes
        self.tomato_committed=False

    def start_day(self,day):
        super().start_day(day)
        if self.tomatoes and day in (20,21,29,30):
            specialist=self.base_people[day]
            # Reuse original WATER/HARVEST visits; never consume the animal
            # backup worker's daily budget during D22-D28.
            q=self.queues[specialist]
            for pos in TOMATO_SITES:
                for cmd in [['TOMATO_MISSION']]:
                    q.append(dict(position=list(pos),command=cmd,source_day=day,source_hour=1,changed=True))
            q.append(dict(position=[4,5],command=['DROP'],source_day=day,source_hour=1,changed=True))

    def act_worker(self,w,obs,shared):
        if obs['day']==29:
            farm=obs['farms'][self.seat]
            pos=tuple(([farm['farmer']]+farm['hands'])[w])
            inv=obs['private']['inventories'][w]
            if any(n>0 for item,n in inv.items() if item not in {'COW','SHEEP','GOOSE'}):
                shed=min(((4,4),(5,4),(4,5),(5,5)),key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))
                if 23-obs['hour']<=abs(pos[0]-shed[0])+abs(pos[1]-shed[1])+3:
                    return self.move(pos,shed) or ['DROP']
        q=self.queues.get(w,[])
        index=self.indices.get(w,0)
        if index<len(q) and q[index]['command'][0]=='TOMATO_MISSION':
            target=tuple(q[index]['position']);farm=obs['farms'][self.seat]
            pos=tuple(([farm['farmer']]+farm['hands'])[w]);tile=farm['tiles'][target[1]][target[0]]
            day=obs['day']+1
            def skip():
                self.indices[w]=index+1
                return self.act_worker(w,obs,shared)
            if not self.tomato_committed:return skip()
            if day==30:
                # A final harvest needs travel, harvest, return, drop and sale.
                delivery=min(abs(target[0]-x)+abs(target[1]-y) for x,y in ((4,4),(5,4),(4,5),(5,5)))
                if abs(pos[0]-target[0])+abs(pos[1]-target[1])+delivery+3>23-obs['hour']:return skip()
            if not isinstance(tile,dict) or tile.get('crop')!='TOMATO':
                if day>21:return skip()
                # Reserve enough time for travel, DIG, PLANT and first WATER.
                if abs(pos[0]-target[0])+abs(pos[1]-target[1])+3>23-obs['hour']:return skip()
                move=self.move(pos,target)
                if move:return move
                if isinstance(tile,dict):
                    if tile.get('animal') or tile.get('kind') not in {'PLANT','WEED'}:return skip()
                    if tile.get('yield_units',0) and obs['day']-tile.get('planted_day',0)>=10:return ['HARVEST']
                    return ['DIG']
                if shared['seeds'].get('TOMATO',0)<=0:return skip()
                shared['seeds']['TOMATO']-=1
                return ['PLANT','TOMATO']
            if day in (20,21) and tile.get('watered_today'):return skip()
            age=obs['day']-tile['planted_day']
            command=['HARVEST'] if age>=8 and tile.get('yield_units',0)>0 else ['WATER'] if day<30 and not tile.get('watered_today') else None
            if command is None:return skip()
            return self.move(pos,target) or command
        marker=next((i for i in range(index,len(q)) if q[i]['command'][0]=='TOMATO_MISSION'),None)
        if marker is None:return super().act_worker(w,obs,shared)
        # Parent may skip several satisfied jobs in one call. Keep the custom
        # sentinel out of its command interpreter, then dispatch it ourselves.
        self.queues[w]=q[:marker]
        try:action=super().act_worker(w,obs,shared)
        finally:self.queues[w]=q
        if action==['PASS'] and self.indices.get(w,0)>=marker:
            return self.act_worker(w,obs,shared)
        return action

    def __call__(self,obs,cfg=None):
        day,hour=obs['day']+1,obs['hour']+1
        if self.tomatoes and day==19 and hour==1:
            # Small fixed exploratory allocation, current cash only. Never
            # assume that the untraded late tomato price survives our supply.
            self.tomato_committed=obs['farms'][self.seat]['money']>=1000
        action=super().__call__(obs,cfg)
        if day==1 and hour==1:
            assert action['market']==[['BUY_PRODUCT','WHEAT',13],['SELL','WHEAT',13],['BUY_PRODUCT','WHEAT',13]]
            action['market']=[['BUY_PRODUCT','WHEAT',13]]
            self.metrics['opening_round_trip_removed']+=1
        if self.tomato_committed and day==19:
            need=max(0,2-obs['private']['seeds'].get('TOMATO',0))
            if need and len(action['market'])<10:
                action['market'].append(['BUY_SEED','TOMATO',need])
        if self.tomatoes and day>=20:
            farm=obs['farms'][self.seat];positions=[farm['farmer']]+farm['hands']
            commands=[action['farmer']]+action['hands']
            for w,(pos,cmd) in enumerate(zip(positions,commands)):
                if w!=self.base_people[day] and tuple(pos) in TOMATO_SITES and cmd[0] in {'PLANT','DIG'} and isinstance(farm['tiles'][pos[1]][pos[0]],dict) and farm['tiles'][pos[1]][pos[0]].get('crop')=='TOMATO':
                    cmd[:]=['PASS']
        return action

def create_agent(context=None):return Agent(context)
