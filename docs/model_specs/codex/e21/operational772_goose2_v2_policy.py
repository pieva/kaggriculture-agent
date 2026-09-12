"""V8 ablation: replace cows at (6,3) and (4,5) with geese in-place."""
from docs.model_specs.codex.e21.operational772_v8_policy import Agent as BaseAgent

GOOSE_SITES={(6,3),(4,5)}

def convert(queue):
    for job in queue:
        if tuple(job['position']) not in GOOSE_SITES:
            continue
        if job['command']==['BUILD_PASTURE']:
            job['command']=['BUILD_COOP']
        elif job['command']==['PLACE','COW']:
            job['command']=['PLACE','GOOSE']

class Agent(BaseAgent):
    def __init__(self,context=None):
        super().__init__(context,True)
        for workers in self.plan['days'].values():
            for queue in workers.values():
                convert(queue)

    def start_day(self,day):
        super().start_day(day)
        # Base's Q2 specialist builds its routine dynamically, outside PLAN.
        for queue in self.queues.values():
            convert(queue)
        # BUILD_COOP in the plan must also be assigned exclusively to specialist.
        if day>=12:
            for worker,queue in self.queues.items():
                if worker!=self.base_people[day]:
                    self.queues[worker]=[j for j in queue if not (tuple(j['position'])==(4,5) and j['command']==['BUILD_COOP'])]

    def __call__(self,obs,cfg=None):
        action=super().__call__(obs,cfg)
        farm=obs['farms'][self.seat]
        positions=[farm['farmer']]+farm['hands']
        commands=[action['farmer']]+action['hands']
        for pos,cmd in zip(positions,commands):
            if tuple(pos) in GOOSE_SITES and cmd==['BUILD_PASTURE']:
                cmd[:]=['BUILD_COOP']
        return action

def create_agent(context=None):return Agent(context)
