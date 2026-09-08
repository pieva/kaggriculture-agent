"""Shared experimental D1-D11 teacher governor, followed by the frozen V2 core.

This is explicit historical assistance, not a newly autonomous crop allocator.
Only observed positions/structures and the target profile constrain the teacher.
"""
from collections import Counter
from copy import deepcopy


class AssistedStart:
    def __init__(self, teacher, core, assisted_days=11):
        self.teacher, self.core = teacher, core
        self.profile = core.profile
        self.assisted_days = assisted_days
        self.events = []
        self.handed_over = False

    def __call__(self, observation, configuration):
        if observation['day'] >= self.assisted_days:
            if not self.handed_over:
                # The old wheat/carrot bootstrap must never restart on an
                # established farm. New missions use actual carried inventory.
                self.core.bootstrap_done = True
                self.handed_over = True
                self.events.append(dict(event='HANDOVER', day=observation['day']+1))
            return self.core(observation, configuration)
        action = deepcopy(self.teacher(observation, configuration))
        farm = observation['farms'][self.core.seat]
        size = len(farm['tiles'])
        def quadrant(pos):
            x, y = pos
            return ('N' if y < size//2 else 'S') + ('W' if x < size//2 else 'E')
        budgets = self.profile.pasture_budgets(farm['unlocked_quadrants'])
        counts = Counter(quadrant((x,y)) for y,row in enumerate(farm['tiles'])
                         for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind')=='PASTURE')
        positions = [farm['farmer'], *farm['hands']]
        commands = [action.get('farmer',['PASS']), *action.get('hands',[])]
        reserved = set()
        for worker, command in enumerate(commands):
            if worker >= len(positions):
                continue
            pos = tuple(positions[worker]); q = quadrant(pos)
            tile = farm['tiles'][pos[1]][pos[0]]
            reason = None
            if command[0] == 'BUILD_COOP':
                reason = 'profile_has_no_geese'
            elif command[0] == 'BUILD_PASTURE' and not (isinstance(tile,dict) and tile.get('kind')=='PASTURE'):
                if counts[q] >= budgets.get(q,0):
                    reason = 'quadrant_capacity'
                elif pos not in reserved:
                    counts[q] += 1
                    reserved.add(pos)
            if reason:
                commands[worker] = ['PASS']
                self.events.append(dict(event='FILTER', day=observation['day']+1,
                                        hour=observation['hour'], worker=worker,
                                        position=pos, command=command, reason=reason))
        action['farmer'], action['hands'] = commands[0], commands[1:]
        return action
