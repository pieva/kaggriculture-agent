"""Coupled growth: budget actual outstanding feed, not already served animals.

V7 treats every early cow as an extra current-day feed liability even after FEED
was acknowledged. Rebuying that completed obligation can consume tomorrow's
payroll. The same obligation rule below applies throughout the season.
"""
from docs.model_specs.codex.e18.tools.e18_31_assignment_controller import AssignmentController


class ObligationController(AssignmentController):
    def __init__(self, plan, seat=0, variant='OBLIGATION', reference_plan=None):
        super().__init__(plan, seat, 'COMBINED', reference_plan)
        self.procurement_observation = None

    def _prepare(self, observation, configuration):
        self.procurement_observation = observation
        super()._prepare(observation, configuration)

    def _extra_feed(self, day):
        obs = self.procurement_observation
        if obs is None or day != obs['day']+1:
            return super()._extra_feed(day)
        farm,private = obs['farms'][self.seat],obs['private']
        due = 0
        for target in self.advanced:
            if self.pasture_plan[target][0] <= day:
                continue
            tile = self._tile(farm,target)
            if not isinstance(tile,dict) or not tile.get('animal') or tile.get('fed_today'):
                continue
            assigned = next((j for j in self.active.values() if j['target']==target
                and any(c[0]=='FEED' for c,_ in j['steps'][j['index']:])),None)
            if assigned is not None:
                worker = assigned['worker']
                # Already carried feed is no longer a shed purchase obligation.
                # An emitted PICKUP is counted separately by the batch ledger.
                selected = self.selected[worker][0]
                if self._inventory(private,worker)['WHEAT'] or selected[:2]==['PICKUP','WHEAT']:
                    continue
            due += 1
        return due

    def _offers_for_worker(self, day, turn, worker, farm, private, prices):
        offers = super()._offers_for_worker(day,turn,worker,farm,private,prices)
        accepted = []
        for job in offers:
            if job['op']=='ANIMAL_SERVICE' and 'CARE' in job['claimed_ops']:
                tile=self._tile(farm,job['target'])
                species=tile['animal']
                product,interval={'COW':('MILK',2),'SHEEP':('WOOL',3)}[species]
                # Additional care creates output, not necessarily additional
                # profit. A conservative maintenance-margin guard avoids adding
                # a bonus in a depressed market. No calendar blackout is used.
                if prices.get(product,0) <= interval*prices.get('WHEAT',0):
                    job['steps']=[s for s in job['steps'] if s[0][0]!='CARE']
                    job['claimed_ops']=[op for op in job['claimed_ops'] if op!='CARE']
                    if not job['claimed_ops']:
                        continue
                    value=tile.get('yield_units',0)*prices.get(product,0) if 'HARVEST' in job['claimed_ops'] else 0
                    if 'COLLECT_FERTILIZER' in job['claimed_ops']:
                        value+=prices.get('FERTILIZER',0)
                    job['score']=(int('FEED' in job['claimed_ops']),value/len(job['steps']),-len(job['steps']))
            accepted.append(job)
        return accepted
