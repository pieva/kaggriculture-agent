"""Native observation-driven diagnostic adapter, without any historical plan.

V1 is intentionally a first integration probe. Opportunity values and capacity
are conservative local approximations, NOT the full portfolio certificate in
the specification; this adapter must not be promoted on a smoke result.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from math import ceil

from docs.model_specs.codex.e18.tools.e18_33_common_policy import (
    ANIMALS, CROPS, Profile, PriceEnvelope, crop_candidates, pasture_candidates,
    distance, walk, shed_access, needs_water, new_crop_value, new_animal_value,
)

MOVES = {"EAST": (1, 0), "WEST": (-1, 0), "SOUTH": (0, 1), "NORTH": (0, -1)}


class CommonController:
    def __init__(self, config, market_price, market_params, seat=0):
        self.profile = Profile.from_config(config)
        self.seat = seat
        # Explicit pure environment pricing adapter; no environment state/RNG.
        self.market_price, self.market_params = market_price, deepcopy(market_params)
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

    def _quote(self, item, operation, units):
        inv = self.market["inventory"][item]
        params = self.market.get("params", self.market_params)
        prices = []
        for _ in range(units):
            p = self.market_price(item, inv-int(operation == "BUY"), params)
            prices.append(p)
            # At the floor a sale does not add supply (official engine).
            inv += (1 if p > 1 else 0) if operation == "SELL" else -1
        return self.envelope.conservative(item, operation, prices)

    def _tile(self, pos):
        return self.farm["tiles"][pos[1]][pos[0]]

    def _owned(self):
        owned = Counter(self.private["shed"])
        for inv in self.private["inventories"]:
            owned.update(inv)
        owned.update(t["animal"] for row in self.farm["tiles"] for t in row
                     if isinstance(t, dict) and t.get("animal"))
        return owned

    def _acknowledge(self):
        for worker, (cmd, target, before) in list(self.previous.items()):
            job = self.active.get(worker)
            if job is None:
                continue
            op = cmd[0]
            tile = self._tile(target)
            inv = self.private["inventories"][worker] if worker < len(self.private["inventories"]) else {}
            if op in MOVES:
                ok = worker < len(self.positions) and self.positions[worker] == target
            elif op == "PICKUP":
                ok = inv.get(cmd[1], 0) >= before.get(cmd[1], 0) + cmd[2]
            elif op == "DROP":
                ok = not inv
            elif op == "DIG":
                ok = tile is None
            elif op == "BUILD_PASTURE":
                ok = isinstance(tile, dict) and tile.get("kind") == "PASTURE"
            elif op == "PLACE":
                ok = isinstance(tile, dict) and tile.get("animal") == cmd[1]
            elif op == "PLANT":
                ok = isinstance(tile, dict) and tile.get("crop") == cmd[1] and tile.get("planted_day") == self.day
            elif op in {"FEED", "CARE", "WATER"}:
                ok = isinstance(tile, dict) and tile.get({"FEED": "fed_today", "CARE": "cared_today", "WATER": "watered_today"}[op], False)
                # On refresh these flags reset; compare the last action's effect
                # on survival separately through replay audit, never invent ack.
            elif op == "FERTILIZE":
                ok = isinstance(tile, dict) and tile.get("fertilized_until_day", -1) >= self.day
            elif op in {"HARVEST", "COLLECT_FERTILIZER"}:
                ok = sum(inv.values()) > sum(before.values())
            else:
                ok = False
            if ok:
                job["steps"].pop(0)
                self.metrics["ack_" + op] += 1
            else:
                self.metrics["unack_" + op] += 1
                invalid = (op in {"WATER", "FERTILIZE"} and not (isinstance(tile, dict) and tile.get("kind") == "PLANT")
                           or op in {"FEED", "CARE", "COLLECT_FERTILIZER"} and not (isinstance(tile, dict) and tile.get("animal")))
                if invalid:
                    self.events.append(dict(day=self.day+1,hour=self.hour+1,event="invalidated",kind=job["kind"],target=job["target"]))
                    del self.active[worker]
                    continue
            if not job["steps"]:
                self.events.append(dict(day=self.day+1, hour=self.hour+1, event="complete", kind=job["kind"], target=job["target"]))
                del self.active[worker]
        self.previous.clear()

    def _requirements(self):
        items, seeds = Counter(), Counter()
        for w, job in self.active.items():
            inv = Counter(self.private["inventories"][w])
            need = Counter()
            for cmd, _ in job["steps"]:
                if cmd[0] == "PLACE":
                    need[cmd[1]] += 1
                elif cmd[0] == "FEED":
                    need["WHEAT"] += 1
                elif cmd[0] == "FERTILIZE":
                    need["FERTILIZER"] += 1
                elif cmd[0] == "PLANT":
                    seeds[cmd[1]] += 1
            items.update(need - inv)
        return items, seeds

    def _prepare_steps(self, worker, target, commands, *, buy=False):
        pos = self.positions[worker]
        inv = Counter(self.private["inventories"][worker])
        need = Counter()
        for cmd in commands:
            if cmd[0] == "FEED":
                need["WHEAT"] += 1
            elif cmd[0] == "FERTILIZE":
                need["FERTILIZER"] += 1
            elif cmd[0] == "PLACE":
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
            existing, _ = self._requirements()
            for item, n in need.items():
                free = self.private["shed"].get(item, 0) - existing[item]
                if not buy and free < n:
                    return None
                if item == "WHEAT" and free >= n:
                    fair_share = ceil(max(1, self.unfed) / max(1, len(self.positions)))
                    n = min(free, max(n, fair_share))
                steps.append((["PICKUP", item, n], pos))
        travel(target)
        steps.extend((cmd, target) for cmd in commands)
        # Delivery may be a separate dynamically chosen mission, but must still
        # be physically possible before the last executable batch.
        output = any(c[0] in {"HARVEST", "COLLECT_FERTILIZER"} for c in commands)
        return_cost = min(distance(target, s) for s in self.sheds)+1 if output else 0
        if len(steps) + return_cost + int(buy) > self.remaining:
            return None
        return steps

    def _services(self):
        result = []
        claims = {tuple(j["target"]) for j in self.active.values() if j["kind"] != "DELIVER"}
        for y, row in enumerate(self.farm["tiles"]):
            for x, tile in enumerate(row):
                target = (x, y)
                if target in claims or not isinstance(tile, dict):
                    continue
                commands, priority, value = [], 0, 0
                if tile.get("animal"):
                    a = ANIMALS[tile["animal"]]
                    if not tile.get("fed_today"):
                        commands.append(["FEED"])
                        priority = 3 if tile.get("consecutive_unfed", 0) else 2
                    if not tile.get("cared_today") and self.final_day-self.day >= a["interval"]:
                        commands.append(["CARE"])
                    if tile.get("yield_units", 0):
                        commands.append(["HARVEST"])
                        value += self._quote(a["product"], "SELL", tile["yield_units"])
                    if tile.get("fertilizer_available"):
                        commands.append(["COLLECT_FERTILIZER"])
                        value += self._quote("FERTILIZER", "SELL", 1)
                elif tile.get("kind") == "PLANT":
                    crop = CROPS[tile["crop"]]
                    age = self.day - tile["planted_day"]
                    if needs_water(tile, self.day):
                        commands.append(["WATER"])
                        priority = 3 if tile.get("consecutive_unwatered", 0) else 1
                    harvestable = tile.get("yield_units", 0) > 0 and age >= crop["first_yield_day"]
                    cash_short = self.farm["money"] < self.feed_reserve
                    if harvestable and (crop["ongoing"] or age >= crop["max_yield_day"] or cash_short or self.day == self.final_day):
                        commands.append(["HARVEST"])
                        value += self._quote(tile["crop"], "SELL", tile["yield_units"])
                if commands:
                    result.append((target, commands, priority, max(1, value), "SERVICE"))
        return result

    def _growth(self, cash_free):
        """Same crop/pasture proposals everywhere; final economic rollout pending."""
        offers = []
        claims = {tuple(j["target"]) for j in self.active.values() if j["kind"] != "DELIVER"}
        pastures_reserved = {tuple(j["target"]) for j in self.active.values() if j["kind"] == "NEW_ANIMAL"}
        owned = self._owned()
        req, seeds_req = self._requirements()
        owned.update({s: max(0, req[s] - self.private["shed"].get(s, 0)) for s in ANIMALS})
        targets = self.profile.species_targets()
        for species in ANIMALS:
            if owned[species] >= targets[species]:
                continue
            price = ANIMALS[species]["cost"]
            if cash_free < price + self._quote("WHEAT", "BUY", 2):
                continue
            value = self.animal_values[species]
            if value["gain"] <= 0:
                continue
            for target in pasture_candidates(self.farm, self.profile, pastures_reserved):
                if target in claims:
                    continue
                tile = self._tile(target)
                opportunity_cost = 0
                commands = []
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    # V2 explicit conversion alternative, conservative value of
                    # the crop's whole original cycle (overstates remaining loss).
                    crop = tile["crop"]
                    opportunity_cost = new_crop_value(crop, tile["planted_day"], self.final_day, self._quote)["revenue"]
                    if value["gain"] <= opportunity_cost:
                        continue
                    if tile.get("yield_units",0) and self.day-tile["planted_day"] >= CROPS[crop]["first_yield_day"]:
                        commands.append(["HARVEST"])
                        if CROPS[crop]["ongoing"]:
                            commands.append(["DIG"])
                    else:
                        commands.append(["DIG"])
                elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                    commands.append(["DIG"])
                if not (isinstance(tile, dict) and tile.get("kind") == "PASTURE"):
                    commands.append(["BUILD_PASTURE"])
                commands += [["PLACE", species], ["FEED"], ["CARE"]]
                incremental = self._maintenance_floor(extra_animals=1) - self.maintenance_floor
                if cash_free < price + self._quote("WHEAT","BUY",2) + incremental:
                    continue
                offers.append((target, commands, 0, value["gain"]-opportunity_cost, "NEW_ANIMAL"))
        for target in crop_candidates(self.farm, claims):
            for crop in self.profile.crops:
                value = self.crop_values[crop]
                seed_cost = CROPS[crop]["seed"]
                incremental = self._maintenance_floor(extra_crops=1) - self.maintenance_floor
                if value["gain"] <= 0 or cash_free < seed_cost + incremental:
                    continue
                commands = [["DIG"]] if self._tile(target) is not None else []
                commands += [["PLANT", crop], ["WATER"]]
                offers.append((target, commands, 0, value["gain"], "NEW_CROP"))
        return offers

    def _maintenance_floor(self, extra_animals=0, extra_crops=0):
        """V2 next-day funding guard; still a load estimate, not route proof."""
        animals = sum(bool(t.get("animal")) for row in self.farm["tiles"] for t in row if isinstance(t,dict))
        crops = sum(t.get("kind")=="PLANT" for row in self.farm["tiles"] for t in row if isinstance(t,dict))
        for job in self.active.values():
            for cmd,_ in job["steps"]:
                animals += cmd[0] == "PLACE"
                crops += cmd[0] == "PLANT"
        animals += extra_animals
        crops += extra_crops
        # Shared service + local travel allowance, uniform over the whole map.
        hands = min(self.profile.maximum_hands, max(0, ceil((6*animals+3*crops)/max(1,self.turns-3))-1))
        payroll, a, b = 0, 1, 1
        for _ in range(hands):
            payroll += a*self.hire_mult
            a,b = b,a+b
        return payroll + self._quote("WHEAT","BUY",2*animals)

    def _market_orders(self):
        orders = []
        items, seeds = self._requirements()
        # Count remaining daily feed regardless of currently assigned jobs.
        grain_carried = sum(inv.get("WHEAT", 0) for inv in self.private["inventories"])
        items["WHEAT"] = max(items["WHEAT"], self.unfed - grain_carried)
        budget = float(self.farm["money"])
        # Only observed shed contents finance immediate purchases. Conservative
        # floor for income when the opponent changes quotes in this batch.
        for item, n in sorted(self.private["shed"].items()):
            if item in ANIMALS:
                continue
            sell = max(0, n - items[item])
            if sell and len(orders) < 4:
                orders.append(["SELL", item, sell])
                budget += self._quote(item, "SELL", sell)
        for item, n in sorted(items.items(), key=lambda kv:(kv[0]!="WHEAT",kv[0])):
            deficit = max(0, n - self.private["shed"].get(item, 0))
            for _ in range(deficit):
                cost = ANIMALS[item]["cost"] if item in ANIMALS else self._quote(item, "BUY", 1)
                if budget < cost or len(orders) >= 10:
                    break
                orders.append(["BUY_ANIMAL" if item in ANIMALS else "BUY_PRODUCT", item, 1])
                budget -= cost
        for crop, n in seeds.items():
            deficit = max(0, n - self.private["seeds"].get(crop, 0))
            if deficit and len(orders) < 10:
                quantity = min(deficit, int(budget // CROPS[crop]["seed"]))
                if quantity:
                    orders.append(["BUY_SEED", crop, quantity])
                    budget -= quantity * CROPS[crop]["seed"]
        # Organic capacity from observed obligations and admissible vacant work.
        services = self._services()
        free_tiles = len(crop_candidates(self.farm))
        work = sum(len(c) + 2 for _, c, _, _, _ in services)
        work += sum(len(j["steps"]) for j in self.active.values())
        if self.day < self.final_day and budget > self.feed_reserve:
            work += min(free_tiles, int((budget-self.feed_reserve)//min(CROPS[c]["seed"] for c in self.profile.crops))) * 4
        target = min(self.profile.maximum_hands, max(0, ceil(work / max(1, self.remaining-2))-1))
        for i in range(len(self.farm["hands"]), target):
            a, b = 1, 1
            for _ in range(i):
                a, b = b, a+b
            cost = a*self.hire_mult
            if len(orders) >= 10 or budget - self.feed_reserve < cost or self.remaining <= 3:
                break
            orders.append(["HIRE"])
            budget -= cost
        # Land is state-triggered. V1 only expands when current available crop
        # space is nearly consumed; no date or future trajectory is consulted.
        count = len(self.farm["unlocked_quadrants"])
        if count < self.profile.maximum_quadrants and len(orders) < 10 and free_tiles <= len(self.positions):
            cost = 1000 * 2**(count-1)
            if budget >= cost + self.feed_reserve and max(v["gain"] for v in self.crop_values.values()) > 0:
                orders.append(["BUY_LAND"])
        return orders

    def __call__(self, observation, configuration):
        self.farm = observation["farms"][self.seat]
        self.private, self.market = observation["private"], observation["market"]
        self.day, self.hour = observation["day"], observation["hour"]
        self.turns = configuration.get("turnsPerDay", 24)
        self.episode_steps = configuration.get("episodeSteps", 720)
        self.final_day = (self.episode_steps-2)//self.turns
        step = self.day*self.turns + self.hour
        self.remaining = min(self.turns-self.hour, self.episode_steps-1-step)
        self.hire_mult = configuration.get("farmHandCostMult", 1)
        self.positions = [tuple(p) for p in [self.farm["farmer"], *self.farm["hands"]]]
        self.sheds = shed_access(len(self.farm["tiles"]))
        self.envelope.observe(self.market["prices"])
        if self.clock_day != self.day:
            if self.clock_day is not None:
                self.metrics["jobs_at_refresh"] += len(self.active)
            self.active.clear()
            self.previous.clear()
            self.clock_day = self.day
        self._acknowledge()
        tiles = [t for row in self.farm["tiles"] for t in row if isinstance(t, dict)]
        animals = [t for t in tiles if t.get("animal")]
        self.unfed = sum(not t.get("fed_today") for t in animals)
        self.feed_reserve = self._quote("WHEAT", "BUY", self.unfed+len(animals))
        self.maintenance_floor = self._maintenance_floor()
        self.crop_values = {c: new_crop_value(c, self.day, self.final_day, self._quote) for c in self.profile.crops}
        self.animal_values = {a: new_animal_value(a, self.day, self.final_day, self._quote) for a in ANIMALS}
        free = set(range(len(self.positions))) - self.active.keys()
        while free:
            req, seeds = self._requirements()
            cost = sum(max(0, n-self.private["shed"].get(s, 0))*ANIMALS[s]["cost"] for s,n in req.items() if s in ANIMALS)
            cost += sum(max(0, n-self.private["seeds"].get(c, 0))*CROPS[c]["seed"] for c,n in seeds.items())
            self.maintenance_floor = self._maintenance_floor()
            cash_free = self.farm["money"]-max(self.feed_reserve,self.maintenance_floor)-cost
            alternatives = self._services()+self._growth(cash_free)
            options = []
            for worker in free:
                inv = self.private["inventories"][worker]
                for target, commands, priority, value, kind in alternatives:
                    steps = self._prepare_steps(worker, target, commands, buy=kind.startswith("NEW_"))
                    if steps:
                        score = (priority, value/max(1,len(steps)), -len(steps), -worker, tuple(-n for n in target))
                        options.append((score, worker, dict(target=target, steps=steps, kind=kind)))
                products = {k:n for k,n in inv.items() if k not in ANIMALS and k != "WHEAT"}
                if products:
                    target = min(self.sheds, key=lambda s:(distance(self.positions[worker],s),s))
                    steps = self._prepare_steps(worker, target, [["DROP"]])
                    if steps:
                        urgent = int(self.remaining <= len(steps)+1)*4
                        value = sum(self._quote(k,"SELL",n) for k,n in products.items())
                        options.append(((urgent,value/len(steps),-len(steps),-worker,(0,0)),worker,dict(target=target,steps=steps,kind="DELIVER")))
            if not options:
                break
            _, worker, job = max(options, key=lambda o:o[0])
            self.active[worker] = job
            self.events.append(dict(day=self.day+1,hour=self.hour+1,event="admitted",kind=job["kind"],target=job["target"]))
            free.remove(worker)
        commands = [["PASS"] for _ in self.positions]
        available = Counter(self.private["shed"])
        seed_available = Counter(self.private["seeds"])
        for worker, job in self.active.items():
            cmd, target = job["steps"][0]
            inv = self.private["inventories"][worker]
            if cmd[0] == "PICKUP":
                if available[cmd[1]] < cmd[2]:
                    self.metrics["wait_input"] += 1
                    continue
                available[cmd[1]] -= cmd[2]
            elif cmd[0] == "PLANT":
                if not seed_available[cmd[1]]:
                    self.metrics["wait_seed"] += 1
                    continue
                seed_available[cmd[1]] -= 1
            elif cmd[0] in {"FEED", "FERTILIZE", "PLACE"}:
                item = {"FEED":"WHEAT", "FERTILIZE":"FERTILIZER"}.get(cmd[0], cmd[1] if len(cmd)>1 else None)
                if not inv.get(item,0):
                    self.metrics["wait_carried_input"] += 1
                    continue
            commands[worker] = cmd
            self.previous[worker] = (cmd, target, dict(inv))
        result = dict(farmer=commands[0],hands=commands[1:],market=self._market_orders())
        self.daily_metrics[self.day+1].update(c[0] for c in commands)
        return result

    def acknowledge_terminal(self, observation):
        # The external replay audits biological and cash effects; incomplete
        # jobs remain visible instead of being erased at termination.
        self.farm = observation["farms"][self.seat]
        self.private = observation["private"]
        self.positions = [tuple(p) for p in [self.farm["farmer"], *self.farm["hands"]]]
        self._acknowledge()
        self.incomplete_missions = len(self.active)

    def finalize_metrics(self):
        pass
