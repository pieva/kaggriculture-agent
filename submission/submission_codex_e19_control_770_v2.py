import math
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from math import ceil
CROPS = {'WHEAT': {'seed': 10, 'first_yield_day': 2, 'max_yield_day': 4, 'interval': 0, 'max_yield': 6, 'ongoing': False, 'water_needed': True}, 'CARROT': {'seed': 20, 'first_yield_day': 2, 'max_yield_day': 3, 'interval': 0, 'max_yield': 4, 'ongoing': False, 'water_needed': True}, 'TOMATO': {'seed': 50, 'first_yield_day': 8, 'max_yield_day': 8, 'interval': 1, 'max_yield': 4, 'ongoing': True, 'water_needed': True}, 'STRAWBERRY': {'seed': 100, 'first_yield_day': 10, 'max_yield_day': 10, 'interval': 2, 'max_yield': 4, 'ongoing': True, 'water_needed': True}, 'MELON': {'seed': 80, 'first_yield_day': 10, 'max_yield_day': 12, 'interval': 0, 'max_yield': 6, 'ongoing': False, 'water_needed': True}}
MARKET_PARAMS = {'WHEAT': {'base': 25, 'I0': 10000, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'I0': 10000, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'I0': 10000, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'I0': 10000, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'I0': 10000, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'I0': 10000, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'I0': 10000, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'I0': 10000, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'I0': 10000, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}
PRICE_FLOOR = 1
HINGE_GAIN = 8.0

def _shape(func, x, T=None):
    x = max(0.0, x)
    if func == 'linear':
        return x
    if func == 'sq':
        return x * x
    if func == 'sqrt':
        return math.sqrt(x)
    if func == 'log':
        return math.log(1.0 + x)
    if func == 'log10':
        return math.log10(1.0 + x)
    if func == 'hinge':
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x

def market_price(item, inventory, params=None):
    """Floor at PRICE_FLOOR."""
    p = (params or MARKET_PARAMS)[item]
    base = p['base']
    I0 = p['I0']
    T = p['T']
    if inventory < I0:
        f = p['below_func']
        amp = p['below_target'] * base / _shape(f, T, T)
        price = base + amp * _shape(f, I0 - inventory, T)
    else:
        f = p['above_func']
        amp = p['above_target'] * base / _shape(f, T, T)
        price = base - amp * _shape(f, inventory - I0, T)
    return max(PRICE_FLOOR, int(round(price)))
'Parametric, quadrant-invariant kernel. No trajectory/controller dependencies.\n\nThis first implementation is a diagnostic kernel, not a released full agent.\nPrices are passed as observed/conditional quotes; it never sees opponent or seed.\n'
ANIMALS = {'COW': dict(cost=400, first_yield_day=8, interval=2, max_held=6, product='MILK'), 'SHEEP': dict(cost=500, first_yield_day=6, interval=3, max_held=6, product='WOOL')}

@dataclass(frozen=True)
class Profile:
    target: int
    local_capacity: int
    maximum_quadrants: int
    maximum_hands: int
    mix_weights: tuple
    crops: tuple
    bootstrap_animals: tuple = ()
    bootstrap_crops: tuple = ()
    bootstrap_retire: str = 'first_confirmed_crop_harvest'
    bootstrap_crop_weights: tuple = ()

    @classmethod
    def from_config(cls, config):
        keys = {'schema_version', 'pastures', 'maximum_unlocked_quadrants', 'maximum_hands', 'livestock_mix_weights', 'allowed_crops'}
        version = config.get('schema_version')
        bootstrap = config.get('bootstrap', {})
        if version in {'e18.codex.common_resource_policy.v2', 'e18.codex.common_resource_policy.v3'}:
            keys.add('bootstrap')
            b_keys = {'livestock_ceiling', 'allowed_crops', 'retire_on'}
            if version.endswith('.v2') and bootstrap.get('retire_on') == 'initial_portfolio_established':
                raise ValueError('Initial portfolio requires version 3 weights')
            if version.endswith('.v3'):
                b_keys.add('crop_mix_weights')
                weights = bootstrap.get('crop_mix_weights', {})
                if set(weights) != set(bootstrap.get('allowed_crops', [])) or any((type(w) is not int or w <= 0 for w in weights.values())):
                    raise ValueError('Invalid initial crop weights')
                if bootstrap.get('retire_on') != 'initial_portfolio_established':
                    raise ValueError('Initial portfolio must retire when established')
            if set(bootstrap) != b_keys or bootstrap['retire_on'] not in {'first_confirmed_crop_harvest', 'self_funded_initial_cycle_renewal', 'initial_portfolio_established'}:
                raise ValueError('Only a one-time observation-retired bootstrap is allowed')
            if set(bootstrap['livestock_ceiling']) != set(ANIMALS) or any((type(n) is not int or n < 0 for n in bootstrap['livestock_ceiling'].values())):
                raise ValueError('Invalid initial livestock ceiling')
            b_crops = bootstrap['allowed_crops']
            if not isinstance(b_crops, list) or not b_crops or len(b_crops) != len(set(b_crops)) or (not set(b_crops) <= set(config['allowed_crops'])):
                raise ValueError('Invalid initial crop set')
        if set(config) != keys or version not in {'e18.codex.common_resource_policy.v1', 'e18.codex.common_resource_policy.v2', 'e18.codex.common_resource_policy.v3'}:
            raise ValueError('Unknown or missing policy fields; no legacy config merge')
        if set(config['pastures']) != {'target', 'uniform_capacity_per_quadrant'}:
            raise ValueError('Pastures contain only global target and uniform capacity')
        if set(config['livestock_mix_weights']) != set(ANIMALS):
            raise ValueError('Unsupported species profile')
        numbers = [config['pastures']['target'], config['pastures']['uniform_capacity_per_quadrant'], config['maximum_unlocked_quadrants'], config['maximum_hands'], *config['livestock_mix_weights'].values()]
        if any((type(n) is not int or n < 0 for n in numbers)) or any((n <= 0 for n in [numbers[1], numbers[2], *numbers[4:]])):
            raise ValueError('Invalid numerical policy limit')
        crops = config['allowed_crops']
        if not isinstance(crops, list) or not crops or len(set(crops)) != len(crops) or (not set(crops) <= set(CROPS)):
            raise ValueError('Invalid shared crop set')
        return cls(numbers[0], numbers[1], numbers[2], numbers[3], tuple(sorted(config['livestock_mix_weights'].items())), tuple(crops), tuple(sorted(bootstrap.get('livestock_ceiling', {}).items())), tuple(bootstrap.get('allowed_crops', ())), bootstrap.get('retire_on', 'first_confirmed_crop_harvest'), tuple(sorted(bootstrap.get('crop_mix_weights', {}).items())))

    def validate_board(self, size):
        if size <= 0 or size % 2 or self.maximum_quadrants > 4:
            raise ValueError('Unsupported environment geometry')
        if self.local_capacity > (size // 2) ** 2 or self.target > self.local_capacity * self.maximum_quadrants:
            raise ValueError('Profile cannot fit on permitted land')

    def pasture_budgets(self, activation_order):
        if len(set(activation_order)) != len(activation_order):
            raise ValueError('Duplicate quadrant identity')
        return {q: min(self.local_capacity, max(0, self.target - self.local_capacity * rank)) if rank < self.maximum_quadrants else 0 for rank, q in enumerate(activation_order)}

    def species_targets(self):
        total = sum((w for _, w in self.mix_weights))
        targets = {s: self.target * w // total for s, w in self.mix_weights}
        order = sorted(self.mix_weights, key=lambda sw: (-(self.target * sw[1] % total), sw[0]))
        for species, _ in order[:self.target - sum(targets.values())]:
            targets[species] += 1
        assert sum(targets.values()) == self.target
        return targets

def quadrant(coord, size):
    x, y = coord
    return ('N' if y < size // 2 else 'S') + ('W' if x < size // 2 else 'E')

def shed_access(size):
    h = size // 2
    return ((h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h))

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def walk(start, target):
    x, y = start
    tx, ty = target
    return [['EAST' if tx > x else 'WEST']] * abs(tx - x) + [['SOUTH' if ty > y else 'NORTH']] * abs(ty - y)

def biological_deadline(tile, day, turns_per_day, episode_steps):
    """Last executable zero-based step before starvation/escape/episode end."""
    if tile.get('kind') == 'PLANT':
        counter, done = (tile.get('consecutive_unwatered', 0), tile.get('watered_today', False))
    elif tile.get('animal'):
        counter, done = (tile.get('consecutive_unfed', 0), tile.get('fed_today', False))
    else:
        raise ValueError('No biological obligation on this tile')
    next_failure_day = day + (2 if done else max(0, 1 - counter))
    return min(episode_steps - 2, (next_failure_day + 1) * turns_per_day - 1)

def needs_water(tile, day):
    if tile.get('watered_today'):
        return False
    rule = CROPS[tile['crop']]
    age = day - tile['planted_day']
    return tile.get('consecutive_unwatered', 0) >= 1 or (not rule['ongoing'] and ceil(rule['max_yield_day'] / 2) <= age <= rule['max_yield_day']) or (rule['ongoing'] and tile.get('fertilized_until_day', -1) >= day and (age + 1 >= rule['first_yield_day']) and ((age + 1 - rule['first_yield_day']) % rule['interval'] == 0))

def pasture_candidates(farm, profile, reserved=()):
    """All legal opportunities, not a table of predetermined pasture coordinates."""
    size = len(farm['tiles'])
    profile.validate_board(size)
    quotas = profile.pasture_budgets(farm['unlocked_quadrants'])
    occupied = Counter()
    for y, row in enumerate(farm['tiles']):
        for x, tile in enumerate(row):
            if isinstance(tile, dict) and tile.get('kind') == 'PASTURE':
                occupied[quadrant((x, y), size)] += 1
    reserved = set(reserved)
    for p in reserved:
        tile = farm['tiles'][p[1]][p[0]]
        if not (isinstance(tile, dict) and tile.get('kind') == 'PASTURE'):
            occupied[quadrant(p, size)] += 1
    candidates = []
    for y, row in enumerate(farm['tiles']):
        for x, tile in enumerate(row):
            pos = (x, y)
            q = quadrant(pos, size)
            if pos in reserved or tile == 'LOCKED' or (isinstance(tile, dict) and tile.get('animal')):
                continue
            empty_pasture = isinstance(tile, dict) and tile.get('kind') == 'PASTURE'
            if q not in quotas or quotas[q] == 0 or (not empty_pasture and occupied[q] >= quotas[q]):
                continue
            candidates.append(pos)
    return sorted(candidates, key=lambda p: (min((distance(p, s) for s in shed_access(size))), p))

def crop_candidates(farm, reserved=()):
    reserved = set(reserved)
    return [(x, y) for y, row in enumerate(farm['tiles']) for x, tile in enumerate(row) if (x, y) not in reserved and (tile is None or (isinstance(tile, dict) and tile.get('kind') == 'WEED'))]

def crop_cashflows(crop, planted_day, final_day, *, fertilized=False):
    """Exact biological potential of one maintained cycle, no future prices.

    Annual harvest at max yield, or earlier at the last useful day; ongoing
    harvest on each production day. Acquisition/execution funding is separate.
    Values become harvestable at the beginning of the indicated day.
    """
    rule = CROPS[crop]
    events = []
    if rule['ongoing']:
        for k in range(rule['max_yield']):
            day = planted_day + rule['first_yield_day'] + k * rule['interval']
            if day <= final_day:
                events.append((day, 2 if fertilized else 1))
    else:
        harvest = min(final_day, planted_day + rule['max_yield_day'])
        age = harvest - planted_day
        if age >= rule['first_yield_day']:
            waters = max(0, age - ceil(rule['max_yield_day'] / 2) + 1)
            events.append((harvest, min(rule['max_yield'], 1 + waters * (2 if fertilized else 1))))
    return events

def animal_cashflows(species, placed_day, final_day, *, care=True):
    rule = ANIMALS[species]
    events = []
    bonus = 0
    for day in range(placed_day, final_day):
        next_day = day + 1
        age = next_day - placed_day
        if age >= rule['first_yield_day'] and (age - rule['first_yield_day']) % rule['interval'] == 0:
            events.append((next_day, min(rule['max_held'], 1 + bonus)))
            bonus = 0
        if care:
            bonus += 1
    return events

def new_crop_value(crop, day, final_day, quotes, maintenance_action_cost=0):
    flows = crop_cashflows(crop, day, final_day)
    if not flows:
        return dict(gain=-CROPS[crop]['seed'], revenue=0, cost=CROPS[crop]['seed'], first_income=None, daily_load=0)
    last = flows[-1][0]
    life = last - day + 1
    actions = 1 + life + len(flows) + 1
    revenue = sum((quotes(crop, 'SELL', n) for _, n in flows))
    cost = CROPS[crop]['seed'] + actions * maintenance_action_cost
    return dict(gain=revenue - cost, revenue=revenue, cost=cost, first_income=flows[0][0], daily_load=actions / life)

def new_animal_value(species, day, final_day, quotes, maintenance_action_cost=0):
    rule = ANIMALS[species]
    flows = animal_cashflows(species, day, final_day)
    life = final_day - day + 1
    if not flows:
        return dict(gain=-rule['cost'], revenue=0, cost=rule['cost'], first_income=None, daily_load=0)
    revenue = sum((quotes(rule['product'], 'SELL', n) for _, n in flows))
    revenue += quotes('FERTILIZER', 'SELL', max(0, life - 1))
    cost = rule['cost'] + quotes('WHEAT', 'BUY', life) + (3 * life + len(flows) + 3) * maintenance_action_cost
    return dict(gain=revenue - cost, revenue=revenue, cost=cost, first_income=min(day + 1, flows[0][0]), daily_load=3 + len(flows) / life)

class PriceEnvelope:
    """Two preregistered conditional scenarios; history belongs to this episode."""

    def __init__(self):
        self.low = {}
        self.high = {}

    def observe(self, prices):
        for item, price in prices.items():
            self.low[item] = min(price, self.low.get(item, price))
            self.high[item] = max(price, self.high.get(item, price))

    def conservative(self, item, operation, unit_quotes):
        if operation == 'SELL':
            return sum((min(p, self.low[item]) for p in unit_quotes))
        return sum((max(p, self.high[item]) for p in unit_quotes))
'Native observation-driven diagnostic adapter, without any historical plan.\n\nV1 is intentionally a first integration probe. Opportunity values and capacity\nare conservative local approximations, NOT the full portfolio certificate in\nthe specification; this adapter must not be promoted on a smoke result.\n'
MOVES = {'EAST': (1, 0), 'WEST': (-1, 0), 'SOUTH': (0, 1), 'NORTH': (0, -1)}

class CommonController:

    def __init__(self, config, market_price, market_params, seat=0):
        self.profile = Profile.from_config(config)
        self.seat = seat
        self.market_price, self.market_params = (market_price, deepcopy(market_params))
        self.envelope = PriceEnvelope()
        self.active = {}
        self.previous = {}
        self.clock_day = None
        self.events = []
        self.metrics = Counter()
        self.daily_metrics = defaultdict(Counter)
        self.error_count = 0
        self.last_error = None
        self.incomplete_missions = 0
        self.serial = 0
        self.bootstrap_done = not bool(self.profile.bootstrap_crops)
        self.bootstrap_first_cycle = set()
        self.bootstrap_harvested = set()
        self.bootstrap_renewed = set()
        self.day_opening_cash = None
        self.previous_day_cash_delta = None
        self.quote_cache = {}
        self.value_quote_cache = {}
        self.bootstrap_crop_targets = None

    def _quote(self, item, operation, units):
        key = (item, operation, units)
        if key in self.quote_cache:
            return self.quote_cache[key]
        inv = self.market['inventory'][item]
        params = self.market.get('params', self.market_params)
        prices = []
        for _ in range(units):
            p = self.market_price(item, inv - int(operation == 'BUY'), params)
            prices.append(p)
            inv += (1 if p > 1 else 0) if operation == 'SELL' else -1
        result = self.envelope.conservative(item, operation, prices)
        self.quote_cache[key] = result
        return result

    def _tile(self, pos):
        return self.farm['tiles'][pos[1]][pos[0]]

    def _value_quote(self, item, operation, units):
        """V4 marginal supply probe; purchases use current conservative quotes.

        Committed crop output is not free future money. Its projected market
        impact is used only to avoid admitting the same monoculture repeatedly.
        This approximation still lacks full chronological portfolio valuation.
        """
        if operation != 'SELL' or item not in CROPS:
            return self._quote(item, operation, units)
        key = (item, operation, units)
        if key in self.value_quote_cache:
            return self.value_quote_cache[key]
        supply = 0
        for row in self.farm['tiles']:
            for tile in row:
                if not isinstance(tile, dict) or tile.get('crop') != item:
                    continue
                rule = CROPS[item]
                age = self.day - tile['planted_day']
                if rule['ongoing']:
                    produced = max(0, (age - rule['first_yield_day']) // rule['interval'] + 1)
                    supply += tile.get('yield_units', 0) + max(0, rule['max_yield'] - produced)
                else:
                    supply += tile.get('yield_units', 0) if age >= rule['max_yield_day'] else rule['max_yield']
        for job in self.active.values():
            supply += sum((CROPS[item]['max_yield'] for cmd, _ in job['steps'] if cmd == ['PLANT', item]))
        inventory = self.market['inventory'][item] + supply
        params = self.market.get('params', self.market_params)
        quotes = [self.market_price(item, inventory + n, params) for n in range(units)]
        result = self.envelope.conservative(item, 'SELL', quotes)
        self.value_quote_cache[key] = result
        return result

    def _owned(self):
        owned = Counter(self.private['shed'])
        for inv in self.private['inventories']:
            owned.update(inv)
        owned.update((t['animal'] for row in self.farm['tiles'] for t in row if isinstance(t, dict) and t.get('animal')))
        return owned

    def _acknowledge(self):
        for worker, (cmd, target, before) in list(self.previous.items()):
            job = self.active.get(worker)
            if job is None:
                continue
            op = cmd[0]
            tile = self._tile(target)
            inv = self.private['inventories'][worker] if worker < len(self.private['inventories']) else {}
            if op in MOVES:
                ok = worker < len(self.positions) and self.positions[worker] == target
            elif op == 'PICKUP':
                ok = inv.get(cmd[1], 0) >= before.get(cmd[1], 0) + cmd[2]
            elif op == 'DROP':
                ok = not inv
            elif op == 'DIG':
                ok = tile is None
            elif op == 'BUILD_PASTURE':
                ok = isinstance(tile, dict) and tile.get('kind') == 'PASTURE'
            elif op == 'PLACE':
                ok = isinstance(tile, dict) and tile.get('animal') == cmd[1]
            elif op == 'PLANT':
                ok = isinstance(tile, dict) and tile.get('crop') == cmd[1] and (tile.get('planted_day') == self.day)
            elif op in {'FEED', 'CARE', 'WATER'}:
                ok = isinstance(tile, dict) and tile.get({'FEED': 'fed_today', 'CARE': 'cared_today', 'WATER': 'watered_today'}[op], False)
            elif op == 'FERTILIZE':
                ok = isinstance(tile, dict) and tile.get('fertilized_until_day', -1) >= self.day
            elif op in {'HARVEST', 'COLLECT_FERTILIZER'}:
                ok = sum(inv.values()) > sum(before.values())
            else:
                ok = False
            if ok:
                if not self.bootstrap_done:
                    if op == 'PLANT':
                        if tuple(target) in self.bootstrap_harvested:
                            self.bootstrap_renewed.add(tuple(target))
                        elif not self.bootstrap_harvested:
                            self.bootstrap_first_cycle.add(tuple(target))
                    if op == 'HARVEST' and any((inv.get(c, 0) > before.get(c, 0) for c in CROPS)):
                        self.bootstrap_harvested.add(tuple(target))
                        if self.profile.bootstrap_retire == 'first_confirmed_crop_harvest':
                            self.bootstrap_done = True
                            self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='bootstrap_retired', reason='confirmed_crop_harvest'))
                job['steps'].pop(0)
                self.metrics['ack_' + op] += 1
            else:
                self.metrics['unack_' + op] += 1
                invalid = op in {'WATER', 'FERTILIZE'} and (not (isinstance(tile, dict) and tile.get('kind') == 'PLANT')) or (op in {'FEED', 'CARE', 'COLLECT_FERTILIZER'} and (not (isinstance(tile, dict) and tile.get('animal'))))
                if invalid:
                    self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='invalidated', kind=job['kind'], target=job['target']))
                    del self.active[worker]
                    continue
            if not job['steps']:
                self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='complete', kind=job['kind'], target=job['target']))
                del self.active[worker]
        self.previous.clear()

    def _requirements(self):
        items, seeds = (Counter(), Counter())
        for w, job in self.active.items():
            inv = Counter(self.private['inventories'][w])
            need = Counter()
            pickups = Counter()
            for cmd, _ in job['steps']:
                if cmd[0] == 'PICKUP':
                    pickups[cmd[1]] += cmd[2]
                if cmd[0] == 'PLACE':
                    need[cmd[1]] += 1
                elif cmd[0] == 'FEED':
                    need['WHEAT'] += 1
                elif cmd[0] == 'FERTILIZE':
                    need['FERTILIZER'] += 1
                elif cmd[0] == 'PLANT':
                    seeds[cmd[1]] += 1
            items.update(need - inv | pickups)
        return (items, seeds)

    def _prepare_steps(self, worker, target, commands, *, buy=False, requirements=None):
        pos = self.positions[worker]
        inv = Counter(self.private['inventories'][worker])
        need = Counter()
        for cmd in commands:
            if cmd[0] == 'FEED':
                need['WHEAT'] += 1
            elif cmd[0] == 'FERTILIZE':
                need['FERTILIZER'] += 1
            elif cmd[0] == 'PLACE':
                need[cmd[1]] += 1
        need -= inv
        steps = []

        def travel(destination):
            nonlocal pos
            for cmd in walk(pos, destination):
                dx, dy = MOVES[cmd[0]]
                pos = (pos[0] + dx, pos[1] + dy)
                steps.append((cmd, pos))
        if need:
            shed = min(self.sheds, key=lambda s: (distance(pos, s) + distance(s, target), s))
            travel(shed)
            existing = self._requirements()[0] if requirements is None else requirements
            for item, n in need.items():
                free = self.private['shed'].get(item, 0) - existing[item]
                if not buy and free < n:
                    return None
                if item == 'WHEAT' and free >= n:
                    tiles = [t for row in self.farm['tiles'] for t in row if isinstance(t, dict)]
                    a = sum((bool(t.get('animal')) for t in tiles))
                    c = sum((t.get('kind') == 'PLANT' for t in tiles))
                    service_units = min(self.profile.maximum_hands + 1, max(1, ceil((6 * a + 3 * c) / max(1, self.turns - 3))))
                    fair_share = ceil(max(1, self.unfed) / max(len(self.positions), service_units))
                    n = min(free, max(n, fair_share))
                steps.append((['PICKUP', item, n], pos))
        travel(target)
        steps.extend(((cmd, target) for cmd in commands))
        output = any((c[0] in {'HARVEST', 'COLLECT_FERTILIZER'} for c in commands))
        return_cost = min((distance(target, s) for s in self.sheds)) + 1 if output else 0
        if len(steps) + return_cost + int(buy) > self.remaining:
            return None
        return steps

    def _services(self):
        result = []
        claims = {tuple(j['target']) for j in self.active.values() if j['kind'] != 'DELIVER'}
        for y, row in enumerate(self.farm['tiles']):
            for x, tile in enumerate(row):
                target = (x, y)
                if target in claims or not isinstance(tile, dict):
                    continue
                commands, priority, value = ([], 0, 0)
                if tile.get('animal'):
                    a = ANIMALS[tile['animal']]
                    if not tile.get('fed_today'):
                        commands.append(['FEED'])
                        priority = 3 if tile.get('consecutive_unfed', 0) else 2
                    if not tile.get('cared_today') and self.final_day - self.day >= a['interval']:
                        commands.append(['CARE'])
                    if tile.get('yield_units', 0):
                        commands.append(['HARVEST'])
                        value += self._quote(a['product'], 'SELL', tile['yield_units'])
                    if tile.get('fertilizer_available'):
                        commands.append(['COLLECT_FERTILIZER'])
                        value += self._quote('FERTILIZER', 'SELL', 1)
                elif tile.get('kind') == 'PLANT':
                    crop = CROPS[tile['crop']]
                    age = self.day - tile['planted_day']
                    fertilize = False
                    if crop['ongoing'] and tile.get('fertilized_until_day', -1) < self.day:
                        next_productions = sum((0 <= self.day + offset + 1 - tile['planted_day'] - crop['first_yield_day'] <= (crop['max_yield'] - 1) * crop['interval'] and (self.day + offset + 1 - tile['planted_day'] - crop['first_yield_day']) % crop['interval'] == 0 and (self.day + offset + 1 <= self.final_day) for offset in range(3)))
                        req, _ = self._requirements()
                        benefit = self._quote(tile['crop'], 'SELL', next_productions) - self._quote('FERTILIZER', 'SELL', 1)
                        if next_productions and benefit > 0 and (self.private['shed'].get('FERTILIZER', 0) > req['FERTILIZER']):
                            commands.append(['FERTILIZE'])
                            fertilize = True
                            value += benefit
                    if needs_water(tile, self.day) or (fertilize and (not tile.get('watered_today'))):
                        commands.append(['WATER'])
                        priority = 3 if tile.get('consecutive_unwatered', 0) else 1
                    harvestable = tile.get('yield_units', 0) > 0 and age >= crop['first_yield_day']
                    cash_short = self.farm['money'] < self.feed_reserve
                    if harvestable and (crop['ongoing'] or age >= crop['max_yield_day'] or cash_short or (self.day == self.final_day)):
                        commands.append(['HARVEST'])
                        value += self._quote(tile['crop'], 'SELL', tile['yield_units'])
                if commands:
                    result.append((target, commands, priority, max(1, value), 'SERVICE'))
        return result

    def _essential_steps(self, worker, target, commands, priority, cash_free, requirements):
        essential = [c for c in commands if c[0] in {'FEED', 'WATER'}]
        if not essential:
            return None
        inv = self.private['inventories'][worker]
        accessible = inv.get('WHEAT', 0) + max(0, self.private['shed'].get('WHEAT', 0) - requirements['WHEAT'])
        procure = priority == 3 and essential[0][0] == 'FEED' and (accessible < 1) and (cash_free >= self._quote('WHEAT', 'BUY', 1))
        return self._prepare_steps(worker, target, essential, buy=procure, requirements=requirements)

    def _growth(self, cash_free):
        """Same crop/pasture proposals everywhere; final economic rollout pending."""
        offers = []
        claims = {tuple(j['target']) for j in self.active.values() if j['kind'] != 'DELIVER'}
        pastures_reserved = {tuple(j['target']) for j in self.active.values() if j['kind'] == 'NEW_ANIMAL'}
        owned = self._owned()
        req, seeds_req = self._requirements()
        owned.update({s: max(0, req[s] - self.private['shed'].get(s, 0)) for s in ANIMALS})
        targets = self.profile.species_targets()
        animal_incremental = self._maintenance_floor(extra_animals=1) - self.maintenance_floor
        crop_incremental = self._maintenance_floor(extra_crops=1) - self.maintenance_floor
        if not self.bootstrap_done:
            initial = dict(self.profile.bootstrap_animals)
            targets = {s: min(n, initial.get(s, 0)) for s, n in targets.items()}
        for species in ANIMALS:
            if owned[species] >= targets[species]:
                continue
            price = ANIMALS[species]['cost']
            if cash_free < price + self._quote('WHEAT', 'BUY', 2):
                continue
            value = self.animal_values[species]
            if value['gain'] <= 0:
                continue
            for target in pasture_candidates(self.farm, self.profile, pastures_reserved):
                if target in claims:
                    continue
                tile = self._tile(target)
                opportunity_cost = 0
                commands = []
                if isinstance(tile, dict) and tile.get('kind') == 'PLANT':
                    crop = tile['crop']
                    opportunity_cost = new_crop_value(crop, tile['planted_day'], self.final_day, self._value_quote)['revenue']
                    if value['gain'] <= opportunity_cost:
                        continue
                    if tile.get('yield_units', 0) and self.day - tile['planted_day'] >= CROPS[crop]['first_yield_day']:
                        commands.append(['HARVEST'])
                        if CROPS[crop]['ongoing']:
                            commands.append(['DIG'])
                    else:
                        commands.append(['DIG'])
                elif isinstance(tile, dict) and tile.get('kind') == 'WEED':
                    commands.append(['DIG'])
                if not (isinstance(tile, dict) and tile.get('kind') == 'PASTURE'):
                    commands.append(['BUILD_PASTURE'])
                commands += [['PLACE', species], ['FEED'], ['CARE']]
                incremental = animal_incremental
                if cash_free < price + self._quote('WHEAT', 'BUY', 2) + incremental:
                    continue
                offers.append((target, commands, 0, value['gain'] - opportunity_cost, 'NEW_ANIMAL'))
        for target in crop_candidates(self.farm, claims):
            for crop in self.profile.crops if self.bootstrap_done else self.profile.bootstrap_crops:
                if not self.bootstrap_done and self.bootstrap_crop_targets is not None:
                    present = sum((t.get('crop') == crop for row in self.farm['tiles'] for t in row if isinstance(t, dict)))
                    if present + seeds_req[crop] >= self.bootstrap_crop_targets[crop]:
                        continue
                value = self.crop_values[crop]
                seed_cost = CROPS[crop]['seed']
                incremental = crop_incremental
                if value['gain'] <= 0 or cash_free < seed_cost + incremental:
                    continue
                commands = [['DIG']] if self._tile(target) is not None else []
                commands += [['PLANT', crop], ['WATER']]
                offers.append((target, commands, 0, value['gain'], 'NEW_CROP'))
        return offers

    def _maintenance_floor(self, extra_animals=0, extra_crops=0):
        """V2 next-day funding guard; still a load estimate, not route proof."""
        animals = sum((bool(t.get('animal')) for row in self.farm['tiles'] for t in row if isinstance(t, dict)))
        crops = sum((t.get('kind') == 'PLANT' for row in self.farm['tiles'] for t in row if isinstance(t, dict)))
        for job in self.active.values():
            for cmd, _ in job['steps']:
                animals += cmd[0] == 'PLACE'
                crops += cmd[0] == 'PLANT'
        animals += extra_animals
        crops += extra_crops
        hands = min(self.profile.maximum_hands, max(0, ceil((6 * animals + 3 * crops) / max(1, self.turns - 3)) - 1))
        payroll, a, b = (0, 1, 1)
        for _ in range(hands):
            payroll += a * self.hire_mult
            a, b = (b, a + b)
        observed_wheat = self.private['shed'].get('WHEAT', 0) + sum((inv.get('WHEAT', 0) for inv in self.private['inventories']))
        return payroll + self._quote('WHEAT', 'BUY', max(0, 2 * animals - observed_wheat))

    def _day_route_certificate(self, proposed_worker, proposed_job, services=None):
        """V6: pack observed obligations AFTER the proposed investment.

        No synthetic hires, fixed quadrant routes, or day-specific windows.
        This is a conservative current-day certificate, not a claim that the
        full future portfolio is certified. Inventory is simulated per worker.
        """
        jobs = dict(self.active)
        jobs[proposed_worker] = proposed_job
        resources = []
        for worker, pos in enumerate(self.positions):
            inv = Counter(self.private['inventories'][worker])
            elapsed = 0
            if worker in jobs:
                job = jobs[worker]
                elapsed = len(job['steps'])
                for cmd, destination in job['steps']:
                    if cmd[0] in MOVES:
                        pos = destination
                    elif cmd[0] == 'PICKUP':
                        inv[cmd[1]] += cmd[2]
                        if self.private['shed'].get(cmd[1], 0) < cmd[2]:
                            elapsed += 1
                    elif cmd[0] in {'FEED', 'FERTILIZE', 'PLACE'}:
                        item = {'FEED': 'WHEAT', 'FERTILIZE': 'FERTILIZER'}.get(cmd[0], cmd[1] if len(cmd) > 1 else None)
                        inv[item] -= 1
                    elif cmd[0] == 'DROP':
                        inv.clear()
            resources.append([tuple(pos), elapsed, inv])
        services = [s for s in (self._services() if services is None else services) if s[0] != tuple(proposed_job['target'])]
        services.sort(key=lambda s: (-s[2], -len(s[1]), -min((distance(s[0], p) for p in self.sheds)), s[0]))
        for target, commands, priority, value, kind in services:
            choices = []
            for worker, (pos, elapsed, inv) in enumerate(resources):
                need = Counter()
                for cmd in commands:
                    if cmd[0] in {'FEED', 'FERTILIZE'}:
                        need['WHEAT' if cmd[0] == 'FEED' else 'FERTILIZER'] += 1
                missing = need - inv
                travel = distance(pos, target)
                if missing:
                    travel = min((distance(pos, s) + distance(s, target) for s in self.sheds)) + len(missing)
                finish = elapsed + travel + len(commands)
                delivery = min((distance(target, s) for s in self.sheds)) + 1 if any((c[0] in {'HARVEST', 'COLLECT_FERTILIZER'} for c in commands)) else 0
                if finish + delivery <= self.remaining:
                    choices.append((finish, worker, missing))
            if not choices:
                return False
            finish, worker, missing = min(choices, key=lambda c: (c[0], c[1]))
            inv = resources[worker][2] + missing
            for cmd in commands:
                if cmd[0] in {'FEED', 'FERTILIZE'}:
                    inv['WHEAT' if cmd[0] == 'FEED' else 'FERTILIZER'] -= 1
            resources[worker] = [target, finish, inv]
        return True

    def _bootstrap_transition(self):
        """Diagnostic release of initial support, never a date-based program."""
        if not self.bootstrap_done and self.profile.bootstrap_retire == 'initial_portfolio_established':
            if self.bootstrap_crop_targets is None:
                area = sum((t != 'LOCKED' for row in self.farm['tiles'] for t in row))
                size = max(0, area - sum((min(n, self.profile.species_targets()[s]) for s, n in self.profile.bootstrap_animals)))
                weights = dict(self.profile.bootstrap_crop_weights)
                total = sum(weights.values())
                targets = {c: size * w // total for c, w in weights.items()}
                for c in sorted(weights, key=lambda c: (-(size * weights[c] % total), c))[:size - sum(targets.values())]:
                    targets[c] += 1
                self.bootstrap_crop_targets = targets
                self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='bootstrap_portfolio_targets', crops=targets))
            crops = Counter((t.get('crop') for row in self.farm['tiles'] for t in row if isinstance(t, dict)))
            animals = Counter((t.get('animal') for row in self.farm['tiles'] for t in row if isinstance(t, dict)))
            if all((crops[c] >= n for c, n in self.bootstrap_crop_targets.items())) and all((animals[s] >= min(n, self.profile.species_targets()[s]) for s, n in self.profile.bootstrap_animals)):
                self.bootstrap_done = True
                self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='bootstrap_retired', reason=self.profile.bootstrap_retire))
            return
        if self.bootstrap_done or self.profile.bootstrap_retire != 'self_funded_initial_cycle_renewal':
            return
        initial_complete = bool(self.bootstrap_first_cycle) and self.bootstrap_first_cycle <= self.bootstrap_renewed
        owned = self._owned()
        livestock_complete = all((owned[s] >= min(n, self.profile.species_targets()[s]) for s, n in self.profile.bootstrap_animals))
        funded = self.farm['money'] >= self.maintenance_floor
        last_day_nonnegative = self.previous_day_cash_delta is not None and self.previous_day_cash_delta >= 0
        conditions = dict(initial_tiles=len(self.bootstrap_first_cycle), renewed_tiles=len(self.bootstrap_renewed), initial_cycle_renewed=initial_complete, livestock_complete=livestock_complete, next_maintenance_funded=funded, last_complete_day_nonnegative=last_day_nonnegative, maintenance_floor=self.maintenance_floor, money=self.farm['money'])
        if self.hour == 0:
            self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='bootstrap_readiness', **conditions))
        if initial_complete and livestock_complete and funded and last_day_nonnegative:
            self.bootstrap_done = True
            self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='bootstrap_retired', reason=self.profile.bootstrap_retire, **conditions))

    def _market_orders(self):
        orders = []
        items, seeds = self._requirements()
        grain_carried = sum((inv.get('WHEAT', 0) for inv in self.private['inventories']))
        items['WHEAT'] = max(items['WHEAT'], self.unfed - grain_carried)
        budget = float(self.farm['money'])
        for item, n in sorted(self.private['shed'].items()):
            if item in ANIMALS:
                continue
            sell = max(0, n - items[item])
            if sell and len(orders) < 4:
                orders.append(['SELL', item, sell])
                budget += self._quote(item, 'SELL', sell)
        for item, n in sorted(items.items(), key=lambda kv: (kv[0] != 'WHEAT', kv[0])):
            deficit = max(0, n - self.private['shed'].get(item, 0))
            quantity = 0
            for candidate in range(1, deficit + 1):
                cost = ANIMALS[item]['cost'] * candidate if item in ANIMALS else self._quote(item, 'BUY', candidate)
                if cost > budget:
                    break
                quantity = candidate
            if quantity and len(orders) < 10:
                cost = ANIMALS[item]['cost'] * quantity if item in ANIMALS else self._quote(item, 'BUY', quantity)
                orders.append(['BUY_ANIMAL' if item in ANIMALS else 'BUY_PRODUCT', item, quantity])
                budget -= cost
        for crop, n in seeds.items():
            deficit = max(0, n - self.private['seeds'].get(crop, 0))
            if deficit and len(orders) < 10:
                quantity = min(deficit, int(budget // CROPS[crop]['seed']))
                if quantity:
                    orders.append(['BUY_SEED', crop, quantity])
                    budget -= quantity * CROPS[crop]['seed']
        services = self._services()
        free_tiles = len(crop_candidates(self.farm))
        work = sum((len(c) + 2 for _, c, _, _, _ in services))
        work += sum((len(j['steps']) for j in self.active.values()))
        if self.day < self.final_day and budget > self.maintenance_floor and (self.remaining > 6):
            work += min(free_tiles, int((budget - self.maintenance_floor) // min((CROPS[c]['seed'] for c in self.profile.crops)))) * 4
        target = min(self.profile.maximum_hands, max(0, ceil(work / max(1, self.remaining - 2)) - 1))
        for i in range(len(self.farm['hands']), target):
            a, b = (1, 1)
            for _ in range(i):
                a, b = (b, a + b)
            cost = a * self.hire_mult
            if len(orders) >= 10 or budget < cost or self.remaining <= 3:
                break
            orders.append(['HIRE'])
            budget -= cost
        count = len(self.farm['unlocked_quadrants'])
        if count < self.profile.maximum_quadrants and len(orders) < 10 and (free_tiles <= len(self.positions)):
            cost = 1000 * 2 ** (count - 1)
            if budget >= cost + self.feed_reserve and max((v['gain'] for v in self.crop_values.values())) > 0:
                orders.append(['BUY_LAND'])
        return orders

    def __call__(self, observation, configuration):
        self.quote_cache.clear()
        self.value_quote_cache.clear()
        self.farm = observation['farms'][self.seat]
        self.private, self.market = (observation['private'], observation['market'])
        self.day, self.hour = (observation['day'], observation['hour'])
        self.turns = configuration.get('turnsPerDay', 24)
        self.episode_steps = configuration.get('episodeSteps', 720)
        self.final_day = (self.episode_steps - 2) // self.turns
        step = self.day * self.turns + self.hour
        self.remaining = min(self.turns - self.hour, self.episode_steps - 1 - step)
        self.hire_mult = configuration.get('farmHandCostMult', 1)
        self.positions = [tuple(p) for p in [self.farm['farmer'], *self.farm['hands']]]
        self.sheds = shed_access(len(self.farm['tiles']))
        self.envelope.observe(self.market['prices'])
        if self.clock_day != self.day:
            if self.clock_day is not None:
                self.metrics['jobs_at_refresh'] += len(self.active)
                self.previous_day_cash_delta = self.farm['money'] - self.day_opening_cash
            self.day_opening_cash = self.farm['money']
            self.active.clear()
            self.previous.clear()
            self.clock_day = self.day
        self._acknowledge()
        tiles = [t for row in self.farm['tiles'] for t in row if isinstance(t, dict)]
        animals = [t for t in tiles if t.get('animal')]
        self.unfed = sum((not t.get('fed_today') for t in animals))
        all_wheat = self.private['shed'].get('WHEAT', 0) + sum((inv.get('WHEAT', 0) for inv in self.private['inventories']))
        self.feed_reserve = self._quote('WHEAT', 'BUY', max(0, self.unfed + len(animals) - all_wheat))
        self.maintenance_floor = self._maintenance_floor()
        self._bootstrap_transition()
        self.crop_values = {c: new_crop_value(c, self.day, self.final_day, self._value_quote) for c in self.profile.crops}
        self.animal_values = {a: new_animal_value(a, self.day, self.final_day, self._quote) for a in ANIMALS}
        free = set(range(len(self.positions))) - self.active.keys()
        while free:
            self.value_quote_cache.clear()
            self.crop_values = {c: new_crop_value(c, self.day, self.final_day, self._value_quote) for c in self.profile.crops}
            req, seeds = self._requirements()
            cost = sum((max(0, n - self.private['shed'].get(s, 0)) * ANIMALS[s]['cost'] for s, n in req.items() if s in ANIMALS))
            cost += sum((max(0, n - self.private['seeds'].get(c, 0)) * CROPS[c]['seed'] for c, n in seeds.items()))
            self.maintenance_floor = self._maintenance_floor()
            cash_free = self.farm['money'] - max(self.feed_reserve, self.maintenance_floor) - cost
            services = self._services()
            alternatives = services + self._growth(cash_free)
            options = []
            for worker in free:
                inv = self.private['inventories'][worker]
                for target, commands, priority, value, kind in alternatives:
                    steps = self._prepare_steps(worker, target, commands, buy=kind.startswith('NEW_'), requirements=req)
                    if steps is None and kind == 'SERVICE':
                        steps = self._essential_steps(worker, target, commands, priority, cash_free, req)
                        if steps:
                            value = 1
                    if steps:
                        score = (int(priority == 3), value / max(1, len(steps)), -len(steps), -worker, tuple((-n for n in target)))
                        options.append((score, worker, dict(target=target, steps=steps, kind=kind)))
                products = {k: n for k, n in inv.items() if k not in ANIMALS and k != 'WHEAT'}
                if products:
                    target = min(self.sheds, key=lambda s: (distance(self.positions[worker], s), s))
                    steps = self._prepare_steps(worker, target, [['DROP']])
                    if steps:
                        urgent = int(self.remaining <= len(steps) + 1) * 4
                        value = sum((self._quote(k, 'SELL', n) for k, n in products.items()))
                        options.append(((urgent, value / len(steps), -len(steps), -worker, (0, 0)), worker, dict(target=target, steps=steps, kind='DELIVER')))
            if not options:
                break
            selected = None
            certificates = {}
            for option in sorted(options, key=lambda o: o[0], reverse=True):
                _, worker, job = option
                if job['kind'].startswith('NEW_'):
                    key = (worker, tuple(job['target']), tuple(((tuple(cmd[:1] if cmd[0] == 'PLANT' else cmd), tuple(pos)) for cmd, pos in job['steps'])))
                    if key not in certificates:
                        certificates[key] = self._day_route_certificate(worker, job, services)
                    if not certificates[key]:
                        self.metrics['growth_rejected_day_route'] += 1
                        continue
                selected = option
                break
            if selected is None:
                break
            _, worker, job = selected
            self.active[worker] = job
            self.events.append(dict(day=self.day + 1, hour=self.hour + 1, event='admitted', kind=job['kind'], target=job['target']))
            free.remove(worker)
        commands = [['PASS'] for _ in self.positions]
        available = Counter(self.private['shed'])
        seed_available = Counter(self.private['seeds'])
        for worker, job in self.active.items():
            cmd, target = job['steps'][0]
            inv = self.private['inventories'][worker]
            if cmd[0] == 'PICKUP':
                if available[cmd[1]] < cmd[2]:
                    self.metrics['wait_input'] += 1
                    continue
                available[cmd[1]] -= cmd[2]
            elif cmd[0] == 'PLANT':
                if not seed_available[cmd[1]]:
                    self.metrics['wait_seed'] += 1
                    continue
                seed_available[cmd[1]] -= 1
            elif cmd[0] in {'FEED', 'FERTILIZE', 'PLACE'}:
                item = {'FEED': 'WHEAT', 'FERTILIZE': 'FERTILIZER'}.get(cmd[0], cmd[1] if len(cmd) > 1 else None)
                if not inv.get(item, 0):
                    self.metrics['wait_carried_input'] += 1
                    continue
            commands[worker] = cmd
            self.previous[worker] = (cmd, target, dict(inv))
        result = dict(farmer=commands[0], hands=commands[1:], market=self._market_orders())
        self.daily_metrics[self.day + 1].update((c[0] for c in commands))
        return result

    def acknowledge_terminal(self, observation):
        self.farm = observation['farms'][self.seat]
        self.private = observation['private']
        self.positions = [tuple(p) for p in [self.farm['farmer'], *self.farm['hands']]]
        self._acknowledge()
        self.incomplete_missions = len(self.active)

    def finalize_metrics(self):
        pass
MODEL_VERSION = 'E19-CONTROL-770-V2'
SOURCE_HASHES = {'C:\\Users\\pietr\\Projects\\kaggriculture-agent\\docs\\model_specs\\codex\\e18\\configs\\CODEX_E18_33_COMMON_RESOURCE_POLICY_V2_BOOTSTRAP.json': 'e2d312dadca690222bcb95ea6bc8457fae0b8d8cbaa977e40922eac660d8a86f', 'C:\\Users\\pietr\\Projects\\kaggriculture-agent\\.venv\\Lib\\site-packages\\kaggle_environments\\envs\\kaggriculture\\kaggriculture.py': 'bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e', 'C:\\Users\\pietr\\Projects\\kaggriculture-agent\\docs\\model_specs\\codex\\e18\\tools\\e18_33_common_policy.py': '49e8ad67f48622515f0c50a0b0f7ecee4d9f90cf05a1314fc5e33b1a043a51c2', 'C:\\Users\\pietr\\Projects\\kaggriculture-agent\\docs\\model_specs\\codex\\e18\\tools\\e18_33_common_controller.py': 'ace9cbc6c67d87a3ed6640787e7e03311883e9826651c26d99ff24d55e50673f', 'C:\\Users\\pietr\\Projects\\kaggriculture-agent\\docs\\model_specs\\codex\\e18\\tools\\build_e18_33_parametric_submission.py': '19d77b0ff4dd36ef3cb032781b3e857cf53fe073d6b1ccaf3a5bb8ec7df4442c'}
PROFILE = {'schema_version': 'e18.codex.common_resource_policy.v2', 'pastures': {'target': 14, 'uniform_capacity_per_quadrant': 7}, 'livestock_mix_weights': {'COW': 9, 'SHEEP': 5}, 'maximum_unlocked_quadrants': 3, 'maximum_hands': 12, 'allowed_crops': ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON'], 'bootstrap': {'livestock_ceiling': {'COW': 2, 'SHEEP': 2}, 'allowed_crops': ['WHEAT', 'CARROT'], 'retire_on': 'first_confirmed_crop_harvest'}}

def create_agent(run_context=None):
    return CommonController(deepcopy(PROFILE), market_price, MARKET_PARAMS, int((run_context or {}).get('player_position', 0)))
_ACTIVE = {}

def agent(observation, configuration=None):
    seat = int(observation.get('player', 0))
    step = int(observation.get('step', observation['day'] * 24 + observation['hour']))
    previous = _ACTIVE.get(seat)
    policy = create_agent({'player_position': seat}) if previous is None or step <= previous[0] else previous[1]
    _ACTIVE[seat] = (step, policy)
    return policy(observation, configuration or {})
