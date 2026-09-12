# Repair1's failed diagnostics are retained. Repair2 fixes the observed
# unplaced Q2 sheep and refuses target sowing without a next-turn water slot.
_REPAIR2_PARENT = Repaired774Policy
MODEL_VERSION = 'CODEX-E21-774-REPAIR2'
RELEASE_ID = MODEL_VERSION
BUILD_METADATA = dict(BUILD_METADATA,release_id=MODEL_VERSION)

class Repaired774Policy(_REPAIR2_PARENT):
    def __init__(self,context=None):
        super().__init__(context)
        original_empty = self.core._empty_pastures
        self.core._empty_pastures = lambda farm: [p for p in original_empty(farm) if p != (6,3)]
        original_tasks = self.core._reclaimed_crop_tasks
        def admitted_tasks(observation):
            tasks = original_tasks(observation)
            if not any(command[0]=='PLANT' for _,_,command in tasks):
                return tasks
            farm=observation['farms'][observation['player']]
            positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
            index=observation['day']*24+observation['hour']
            covered=False
            if observation['hour']<23 and index+1<len(_v9.ROUTINE_ACTIONS):
                upcoming=self.commands(_v9.ROUTINE_ACTIONS[index+1],len(positions))
                covered=any(position==self.target and upcoming[i][0] in {'PASS','FEED','CARE','COLLECT_FERTILIZER','FERTILIZE','HARVEST'}
                            for i,position in enumerate(positions))
            if not covered:
                self.metrics['uncovered_sowings_declined']+=1
                tasks=[task for task in tasks if task[2][0]!='PLANT']
            return tasks
        self.core._reclaimed_crop_tasks=admitted_tasks

    def bypass(self,observation,configuration=None):
        # The mission places the remaining purchased sheep into Q2 (3,6).
        # Excluding Q1 (6,3) preserves the intended 17 occupied pastures.
        self.core.config['pasture_fill_mission_worker_limit']=1
        return super().bypass(observation,configuration)

    def __call__(self,observation,configuration=None):
        observation=dict(observation)
        observation.setdefault('step',observation['day']*24+observation['hour'])
        return super().__call__(observation,configuration)

# create_agent and agent resolve the repaired class at call time.
