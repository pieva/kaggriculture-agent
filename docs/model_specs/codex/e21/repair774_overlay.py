# Appended to the frozen diagnostic bundle; no filesystem dependency at runtime.
_REPAIR774_PARENT_CREATE = create_agent
from collections import Counter as _RepairCounter
from copy import deepcopy as _repair_copy

MODEL_VERSION = 'CODEX-E21-774-REPAIR1'
RELEASE_ID = MODEL_VERSION
BUILD_METADATA = {'release_id': MODEL_VERSION, 'base': 'fixed774 modern reconstruction',
                  'topology': '7-7-4', 'livestock': '8 COW + 9 SHEEP + 1 GOOSE',
                  'status': 'LOCAL_DIAGNOSTIC', 'uploaded': False}

class Repaired774Policy:
    moves = {'NORTH': (0,-1), 'SOUTH': (0,1), 'EAST': (1,0), 'WEST': (-1,0)}
    target = (4,7)
    def __init__(self, context=None):
        self.parent = _REPAIR774_PARENT_CREATE(context)
        self.core = self.parent.core
        self.configured = False
        self.detours = {}
        self.events = []
        self.metrics = _RepairCounter()

    @staticmethod
    def commands(action, count):
        return [action.get('farmer', ['PASS']), *action.get('hands', [])][:count] + [['PASS'] for _ in range(max(0,count-1-len(action.get('hands',[]))))]

    def bypass(self, observation, configuration=None):
        action = self.original_provider(observation, configuration)
        if not 11 <= observation['day'] < 28:
            return action
        action = _repair_copy(action)
        farm = observation['farms'][observation['player']]
        positions = [tuple(farm['farmer']), *map(tuple,farm['hands'])]
        commands = self.commands(action,len(positions))
        step = observation['step']
        hour = observation['hour']
        target_needs_work = bool(self.core._reclaimed_crop_tasks(observation))
        # Remove only excursions whose next substantive routine stop is the
        # reclaimed tile and for which there is no current crop obligation.
        # The unchanged next stop and its original hour are the rejoin contract.
        for worker, position in enumerate(positions):
            plan = self.detours.get(worker)
            if plan and step >= plan['end']:
                if position != plan['target']:
                    raise RuntimeError('774 route failed to rejoin')
                self.metrics['rejoins'] += 1
                del self.detours[worker]
                plan = None
            if not plan and not target_needs_work:
                virtual = position
                removed = False
                for offset in range(min(16,24-hour)):
                    index = step+offset
                    if index >= len(_v9.ROUTINE_ACTIONS): break
                    future = self.commands(_v9.ROUTINE_ACTIONS[index],len(positions))[worker]
                    op = future[0]
                    if op in self.moves:
                        dx,dy = self.moves[op]
                        virtual = (max(0,min(9,virtual[0]+dx)),max(0,min(9,virtual[1]+dy)))
                    elif op == 'PASS':
                        continue
                    elif virtual == self.target and op in {'FEED','CARE','COLLECT_FERTILIZER','FERTILIZE','HARVEST','PLACE','BUILD_PASTURE'}:
                        removed = True
                    else:
                        distance = abs(position[0]-virtual[0])+abs(position[1]-virtual[1])
                        if removed and offset > 0 and distance <= offset and virtual != self.target:
                            plan = {'end':step+offset,'target':virtual}
                            self.detours[worker] = plan
                            self.events.append({'step':step,'worker':worker,'rejoin_step':step+offset,'target':virtual})
                            self.metrics['excursions_removed'] += 1
                        break
            if plan:
                goal = plan['target']
                if position[0] != goal[0]: command = ['EAST' if position[0]<goal[0] else 'WEST']
                elif position[1] != goal[1]: command = ['SOUTH' if position[1]<goal[1] else 'NORTH']
                else: command = ['PASS']
                commands[worker] = command
                self.metrics['rerouted_commands'] += 1
        action['farmer'], action['hands'] = commands[0],commands[1:]
        # Productive use of slack is restricted to the current tile: no new
        # route can break the next scheduled stop or reserve another worker.
        idle = self.core._pass_workers(action,len(positions)) & self.detours.keys()
        used = self.core._route_idle_service(action,observation,tasks=self.core._recovery_tasks(observation),eligible=idle,limit=len(idle))
        self.metrics['slack_services'] += len(used)
        return action

    def __call__(self, observation, configuration=None):
        if observation['day'] < 11:
            return self.parent(observation,configuration)
        if not self.configured:
            t = self.core
            t.committed_reclaims = {self.target}
            t._apply_reclaim_envelope()
            assert t.target_pastures_by_quadrant == {'Q0':7,'Q1':7,'Q2':4}
            t.livestock_resource_cap = 17
            t.config['pre_q2_livestock_resource_cap'] = 17
            t.config['reclaimed_seed_backfill_units'] = 1
            t.config['pasture_fill_mission_worker_limit'] = 0
            t.candidate_id = MODEL_VERSION
            t.model_spec_version = MODEL_VERSION
            t._transition(observation['day'],'RECLAIM_CROP','repair1_fixed774_17_pasture_animals')
            self.parent.configured = True
            self.original_provider = t.base_policy
            t.base_policy = self.bypass
            self.configured = True
        # Keep E18's terminal routing authoritative. Topology/market guards
        # remain, but crop replacement cannot preempt terminal deliveries.
        if observation['day'] >= 28:
            action = _repair_copy(self.original_provider(observation,configuration))
            farm = observation['farms'][observation['player']]
            positions = [tuple(farm['farmer']),*map(tuple,farm['hands'])]
            commands = self.commands(action,len(positions))
            for i,c in enumerate(commands):
                if positions[i] == self.target and c[0] in {'BUILD_PASTURE','PLACE','FEED','CARE','COLLECT_FERTILIZER'}:
                    commands[i] = ['PASS']
            action['farmer'],action['hands'] = commands[0],commands[1:]
            self.core._filter_market(action,observation)
            self.metrics['terminal_passthrough'] += 1
            return action
        return self.parent(observation,configuration)

def create_agent(run_context=None):
    return Repaired774Policy(run_context)

_REPAIR774_ACTIVE = {}
def agent(observation, configuration=None):
    configuration = configuration or {}
    seat = int(observation.get('player',0))
    step = observation['day']*configuration.get('turnsPerDay',24)+observation['hour']
    previous = _REPAIR774_ACTIVE.get(seat)
    policy = create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _REPAIR774_ACTIVE[seat] = (step,policy)
    return policy(observation,configuration)
