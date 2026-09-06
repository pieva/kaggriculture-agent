"""E18.32 development: readiness and marginal production, no opponent inputs."""
from collections import Counter
from copy import deepcopy

from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController
from docs.model_specs.codex.e18.tools.e18_31_assignment_controller import CROP_DATA, FIB, MOVES, SHED_ACCESS, distance


class ReadyWorkController(UnifiedInvestmentController):
    def __init__(self, plan, seat=0, variant='COMBINED', reference_plan=None):
        super().__init__(deepcopy(plan), seat, reference_plan=reference_plan)
        self.ready_variant = variant
        self.ready_metrics = Counter()
        self.fertility_reserve = 0
        self.ready_observation = None
        if variant in {'CLOCK', 'COMBINED'}:
            # Keep task order and dates as a controlled ablation, not their
            # nominal within-day clock. Dependencies are checked on observation.
            for rows in self.routes.values():
                for row in rows:
                    row['turn'] = 1

    def _planned_or_recovery(self, row, farm, private, worker, key):
        target = tuple(row['position'])
        if row['opcode'] not in {*MOVES, 'PASS', 'DROP', 'PICKUP'} and self._tile(farm, target) == 'LOCKED':
            self.ready_metrics['land_dependency_wait'] += 1
            return ['PASS'], None
        return super()._planned_or_recovery(row, farm, private, worker, key)

    def fertilizer_gain(self, day, tile, target, prices):
        """Conservative added yield, net of selling the same fertilizer.

        The existing crop contract is an experimental control. In particular,
        do not count bonus units that hit the storage cap before its harvest.
        Calendar here means the crop's existing service commitments, not a
        benchmark target or a special treatment day.
        """
        if not isinstance(tile, dict) or tile.get('kind') != 'PLANT':
            return 0
        today = day - 1
        if tile.get('fertilized_until_day', -1) >= today:
            return 0
        crop = tile['crop']
        first, maximum, cap, interval = CROP_DATA[crop]
        age = today - tile['planted_day']
        baseline = treated = tile.get('yield_units', 0)
        if interval:
            for offset in range(min(3, 30 - day)):
                age_next = age + offset + 1
                if age_next >= first and (age_next - first) % interval == 0 and (age_next-first)//interval < cap:
                    baseline = min(cap, baseline + 1)
                    treated = min(cap, treated + 2)
        else:
            harvest = min((r['day'] for r in self.plan['trajectory']
                           if r['opcode']=='HARVEST' and tuple(r['position'])==target and r['day']>=day), default=30)
            for d in range(day, min(harvest, 30)+1):
                a = d - 1 - tile['planted_day']
                watered = d == day and tile.get('watered_today')
                water_planned = any(r['day']==d and r['opcode']=='WATER' and tuple(r['position'])==target
                                    for r in self.plan['trajectory'])
                if watered or not water_planned or not (maximum+1)//2 <= a <= maximum:
                    continue
                baseline = min(cap, baseline + 1)
                treated = min(cap, treated + (2 if d-day<3 else 1))
        extra = treated - baseline
        net = .9 * (extra * prices.get(crop, 0) - prices.get('FERTILIZER', 0))
        return max(0, net) if extra else 0

    def _fertility_offers(self, day, turn, worker, farm, private, prices):
        if self.ready_variant not in {'FERTILITY', 'COMBINED'}:
            return []
        pending = self._remaining_rows(day, worker)
        if pending and pending[0]['turn'] <= turn:
            return []
        fence = min(23, pending[0]['turn']-1) if pending else 23
        pos = self._position(farm, worker)
        inv = self._inventory(private, worker)
        if inv and set(+inv) != {'FERTILIZER'}:
            return []
        reserved = super()._pending_requirements(day, 'pickup')['FERTILIZER']
        for job in self.active.values():
            reserved += sum(c[2] for c,_ in job['steps'][job['index']:] if c[:2]==['PICKUP','FERTILIZER'])
        reserved += sum(c[2] for c,_ in self.selected if c[:2]==['PICKUP','FERTILIZER'])
        if not inv['FERTILIZER'] and private['shed'].get('FERTILIZER',0) <= reserved:
            return []
        claims = {j['target'] for j in self.active.values()}
        claims.update(self._position(farm,w) for w,(c,_) in enumerate(self.selected)
                      if c[0] not in {*MOVES,'PASS','PICKUP','DROP'})
        offers = []
        for y,row in enumerate(farm['tiles']):
            for x,tile in enumerate(row):
                target=(x,y)
                if target in claims or self._row_pending(day,'FERTILIZE',target) or self._row_pending(day,'DIG',target):
                    continue
                value=self.fertilizer_gain(day,tile,target,prices)
                if value <= 0:
                    continue
                steps=[]
                p=pos
                if not inv['FERTILIZER']:
                    shed=min(SHED_ACCESS,key=lambda s:distance(p,s)+distance(s,target))
                    self._walk(steps,p,shed)
                    steps.append((['PICKUP','FERTILIZER',1],shed))
                    p=shed
                self._walk(steps,p,target)
                steps.append((['FERTILIZE'],target))
                # Bonus for ongoing crops requires water at refresh. For annuals,
                # WATER can also realize today's bonus immediately.
                if not tile.get('watered_today'):
                    steps.append((['WATER'],target))
                if pending:
                    self._walk(steps,target,pos)
                if turn+len(steps)-1 > fence:
                    continue
                offers.append(dict(key=f'{day}:FERTILITY:{target}:{worker}:{turn}',
                    day=day,op='FERTILITY',target=target,worker=worker,steps=steps,index=0,
                    phase='OUT',origin=pos if pending else None,fence=fence,start_turn=turn,
                    claimed_ops=['FERTILIZE','WATER'],score=(0,value/len(steps),-len(steps)),
                    purchase=False,emitted=False,procure_required={},procurement={}))
        return offers

    def _offers_for_worker(self, day, turn, worker, farm, private, prices):
        offers=super()._offers_for_worker(day,turn,worker,farm,private,prices)
        offers.extend(self._fertility_offers(day,turn,worker,farm,private,prices))
        return offers

    def _pending_requirements(self, day, requirement_kind):
        result=super()._pending_requirements(day,requirement_kind)
        if requirement_kind=='pickup':
            result['FERTILIZER']+=self.fertility_reserve
        return result

    def _prepare(self, observation, configuration):
        self.ready_observation=observation
        self.fertility_reserve=0
        super()._prepare(observation,configuration)
        if self.ready_variant not in {'FERTILITY','COMBINED'}:
            return
        day=observation['day']+1
        farm, private=observation['farms'][self.seat],observation['private']
        prices=observation['market']['prices']
        # No speculative fertilizer purchase and no diversion of cattle/feed
        # liquidity. Preserve supply for a profitable service only with slack.
        floor=sum(FIB[:self.daily_hands.get(day+1,0)])+400+2*prices['WHEAT']*1.1
        if farm['money']>=floor:
            count=sum(self.fertilizer_gain(day,t,(x,y),prices)>0 for y,row in enumerate(farm['tiles']) for x,t in enumerate(row))
            self.fertility_reserve=min(private['shed'].get('FERTILIZER',0),count)
