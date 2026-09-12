"""Execute an explicitly compiled historical operation program, without a dispatcher.

Local diagnostic, not a general or published 772 agent. No future observations
or prices are used. Strict mode stops at a changed worker layout rather than
silently sending commands to the wrong worker or tile.
"""
from copy import deepcopy


class OperationalProgram:
    def __init__(self, program, seat=0, strict=True):
        self.program = program
        self.seat = seat
        self.strict = strict
        self.frames = {(f['day'], f['hour']): f for f in program['frames']}
        self.checked = 0

    def __call__(self, observation, configuration=None):
        key = (observation['day'] + 1, observation['hour'] + 1)
        if key not in self.frames:
            raise RuntimeError(f'No compiled operation at {key}')
        frame = self.frames[key]
        farm = observation['farms'][self.seat]
        positions = [farm['farmer']] + farm['hands']
        if self.strict and positions != frame['positions_before']:
            raise RuntimeError(f'Operational layout divergence at D{key[0]} H{key[1]}: '
                               f'expected {frame["positions_before"]}, observed {positions}')
        self.checked += 1
        return deepcopy(frame['action'])
