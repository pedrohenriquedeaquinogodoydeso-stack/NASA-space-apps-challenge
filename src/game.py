##################################
# game.py
#
# Survival phase: 3 decisions per sol (morning, afternoon, night).
# After the night decision the sol ends and daily consumption is deducted.
# The score is science points. The manager is authoritative: it owns all state.
##################################

import random

from src.constants import MARS_SITES, MODULES, NASA_CONSTANTS
from src.situations import PERIOD_LABELS, PERIODS, SITE_OBJECTIVES, SITUATIONS

SOLAR_MIN, SOLAR_MAX = 0.4, 2.0
GREENHOUSE_FOOD_KG_DAY = 2.4
GREENHOUSE_O2_KG_DAY = 0.9
MOXIE_O2_KG_DAY = 2.0
ISRU_WATER_L_DAY = 6.0
DAILY_DUST_ON_SOLAR = 0.02
DAILY_STRUCTURE_WEAR = 0.25
RECENT_MEMORY = 5

RESOURCES = [("oxygen", "Oxygen", "kg"), ("water", "Water", "L"), ("food", "Food", "kg")]
RESOURCE_KEYS = {"oxygen_kg": "oxygen", "water_l": "water", "food_kg": "food"}
RANKS = [(0, "Rookie Outpost"), (80, "Field Station"), (250, "Research Base"),
         (500, "Scientific Hub"), (900, "Mars Observatory")]


def _clamp(value, low, high):
    return max(low, min(high, value))


EFFECT_KEYS = {"oxygen_kg", "water_l", "food_kg", "integrity", "solar", "science", "sample"}
STAT_KEYS = {"oxygen_kg", "water_l", "food_kg", "integrity", "solar", "power", "crew", "sol", "science", "samples"}
REQUIRE_KEYS = STAT_KEYS | {"modules", "without_modules"}


def validate_situations(situations):
    """Fail fast with a clear message when an event in situations.py has a typo."""
    ids = set()
    for s in situations:
        sid = s.get("id", "<no id>")
        if sid in ids:
            raise ValueError(f"Event '{sid}': duplicate id")
        ids.add(sid)
        for key in ("id", "tag", "title", "description", "yes", "no"):
            if key not in s:
                raise ValueError(f"Event '{sid}': missing '{key}'")
        for p in s.get("periods") or []:
            if p not in PERIODS:
                raise ValueError(f"Event '{sid}': unknown period '{p}'")
        for site in s.get("sites") or []:
            if site not in MARS_SITES:
                raise ValueError(f"Event '{sid}': unknown site '{site}'")
        req = s.get("requires") or {}
        if isinstance(req, (list, tuple)):
            req = {"modules": list(req)}
        for key, rule in req.items():
            if key not in REQUIRE_KEYS:
                raise ValueError(f"Event '{sid}': unknown requirement '{key}' (valid: {sorted(REQUIRE_KEYS)})")
            if key in ("modules", "without_modules"):
                for m in rule:
                    if m not in MODULES:
                        raise ValueError(f"Event '{sid}': unknown module '{m}'")
            elif isinstance(rule, dict) and not set(rule) <= {"min", "max"}:
                raise ValueError(f"Event '{sid}': requirement '{key}' only accepts 'min' and 'max'")
        for answer in ("yes", "no"):
            opt = s[answer]
            for fx in (opt["effects"], (opt.get("risk") or {}).get("effects", {})):
                bad = set(fx) - EFFECT_KEYS
                if bad:
                    raise ValueError(f"Event '{sid}' ({answer}): unknown effect {sorted(bad)} (valid: {sorted(EFFECT_KEYS)})")


class MarsGameManager:
    def __init__(self, loadout=None, rng=None):
        self.rng = rng or random.Random()
        self.catalog = [dict(s, index=i) for i, s in enumerate(SITUATIONS)]

        site_id = getattr(loadout, "landing_site", "jezero")
        self.site_id = site_id if site_id in MARS_SITES else "jezero"
        self.site = MARS_SITES[self.site_id]
        self.crew = getattr(loadout, "crew_size", 4)
        self.duration = getattr(loadout, "mission_duration_days", 500)
        self.modules = {
            "solar_array": getattr(loadout, "has_solar_array", True),
            "wpa_recycler": getattr(loadout, "has_wpa_recycler", True),
            "greenhouse": getattr(loadout, "has_greenhouse", False),
            "moxie_isru": getattr(loadout, "has_moxie_isru", False),
        }
        self.objectives = SITE_OBJECTIVES[self.site_id]

        self.start = {
            "oxygen": getattr(loadout, "initial_oxygen_kg", NASA_CONSTANTS["INITIAL_OXIGEN_KG"]),
            "water": getattr(loadout, "initial_water_l", NASA_CONSTANTS["INITIAL_WATER_L"]),
            "food": getattr(loadout, "initial_food_kg", NASA_CONSTANTS["INITIAL_FOOD_KG"]),
        }
        self.oxygen = self.start["oxygen"]
        self.water = self.start["water"]
        self.food = self.start["food"]
        self.integrity = 100.0
        self.solar = 1.0

        self.sol = 1
        self.period_idx = 0
        self.science = 0.0
        self.samples = [0] * len(self.objectives)

        self.current = None
        self.recent = []
        self.last_scheduled_sol = 0
        self.sol_report = None
        self.last_changes = None
        self.game_over = False
        self.victory = False
        self.ending = None

    # ------------------------------------------------------------------ power
    def _power(self):
        base = NASA_CONSTANTS["BASE_HABITAT_POWER_KWE"]  # 3 Kilopower units cover the base habitat
        solar_gen = 0.0
        if self.modules["solar_array"]:
            solar_gen = MODULES["solar_array"]["power_kwe"] * self.site["solar_efficiency"] * self.solar
        demand = base + sum(
            MODULES[m]["power_kwe"] for m, on in self.modules.items()
            if on and not MODULES[m]["is_generator"]
        )
        supply = base + solar_gen
        return supply, demand, supply - demand, min(1.0, supply / demand)

    # ------------------------------------------------------------- daily flow
    def _flows(self):
        """Net change per sol for each resource (negative = loss)."""
        _, _, _, ratio = self._power()
        c = self.crew
        dust = self.site["dust_wear_multiplier"]
        water_use = NASA_CONSTANTS["WATER_L_PER_PERSON_DAY"] * c
        if self.modules["wpa_recycler"]:
            water_use *= 1 - NASA_CONSTANTS["WPA_RECOVERY_RATE"] * ratio
        flows = {
            "oxygen": -NASA_CONSTANTS["O2_KG_PER_PERSON_DAY"] * c,
            "water": -water_use,
            "food": -NASA_CONSTANTS["FOOD_KG_PER_PERSON_DAY"] * c,
        }
        if self.modules["greenhouse"]:
            flows["food"] += GREENHOUSE_FOOD_KG_DAY * ratio
            flows["oxygen"] += GREENHOUSE_O2_KG_DAY * ratio
        if self.modules["moxie_isru"]:
            flows["oxygen"] += MOXIE_O2_KG_DAY * ratio / dust
            if self.site["isru_water_access"]:
                flows["water"] += ISRU_WATER_L_DAY * ratio
        return flows

    # ---------------------------------------------------------------- effects
    @staticmethod
    def _change(label, delta, unit="", decimals=0):
        return {"label": label, "delta": round(delta, decimals), "unit": unit, "decimals": decimals}

    def _apply_effects(self, fx, scale=1.0):
        """Apply effects and return the ACTUAL changes (after clamping) for the UI."""
        changes = []

        def add(label, old, new, unit, decimals=0):
            if round(new - old, decimals) != 0:
                changes.append(self._change(label, new - old, unit, decimals))

        for key, attr in RESOURCE_KEYS.items():
            v = fx.get(key)
            if v:
                v = v * scale if v > 0 else v
                old = getattr(self, attr)
                setattr(self, attr, max(0.0, old + v))
                label, unit = next((l, u) for a, l, u in RESOURCES if a == attr)
                add(label, old, getattr(self, attr), unit, 1)
        if fx.get("integrity"):
            old = self.integrity
            self.integrity = _clamp(old + fx["integrity"], 0, 100)
            add("Structure", old, self.integrity, "%", 1)
        if fx.get("solar"):
            old = self.solar
            self.solar = _clamp(old + fx["solar"], SOLAR_MIN, SOLAR_MAX)
            add("Solar efficiency", old, self.solar, "x", 2)
        if fx.get("science"):
            pts = fx["science"]
            if pts > 0:
                pts *= self.site["science_multiplier"]
            old = self.science
            self.science = max(0.0, old + pts)
            add("Science points", old, self.science, "pts")
        if "sample" in fx and fx["sample"] < len(self.samples):
            self.samples[fx["sample"]] += 1
            changes.append(self._change(self.objectives[fx["sample"]]["name"], 1, "sample"))
        return changes

    # ------------------------------------------------------------ situations
    def _stats(self):
        """Current values that an event's 'requires' can test."""
        _, _, net, _ = self._power()
        return {
            "oxygen_kg": self.oxygen, "water_l": self.water, "food_kg": self.food,
            "integrity": self.integrity, "solar": self.solar, "power": net,
            "crew": self.crew, "sol": self.sol, "science": self.science, "samples": sum(self.samples),
        }

    def _meets(self, requires):
        if not requires:
            return True
        if isinstance(requires, (list, tuple)):  # legacy form: list of modules
            requires = {"modules": list(requires)}
        stats = self._stats()
        for key, rule in requires.items():
            if key == "modules":
                ok = all(self.modules.get(m) for m in rule)
            elif key == "without_modules":
                ok = not any(self.modules.get(m) for m in rule)
            else:
                if not isinstance(rule, dict):  # shorthand: a number means "at least"
                    rule = {"min": rule}
                ok = rule.get("min", float("-inf")) <= stats[key] <= rule.get("max", float("inf"))
            if not ok:
                return False
        return True

    def _pick(self):
        period = PERIODS[self.period_idx]
        for s in self.catalog:
            every = s.get("scheduled_every")
            if (every and period == "morning" and self.sol % every == 0
                    and self.last_scheduled_sol != self.sol and self._meets(s.get("requires"))):
                self.last_scheduled_sol = self.sol
                return s

        def base(s, check_period=True):
            return (not s.get("scheduled_every")
                    and (not check_period or s.get("periods") is None or period in s["periods"])
                    and (s.get("sites") is None or self.site_id in s["sites"]))

        pool = [s for s in self.catalog if base(s) and self._meets(s.get("requires"))]
        if not pool:  # safety net: unconditional events for this period, then any period
            pool = [s for s in self.catalog if base(s) and not s.get("requires")] \
                or [s for s in self.catalog if base(s, False) and not s.get("requires")]
        fresh = [s for s in pool if s["id"] not in self.recent]
        choice = self.rng.choice(fresh or pool)
        self.recent = (self.recent + [choice["id"]])[-RECENT_MEMORY:]
        return choice

    def _public(self, s):
        period = PERIODS[self.period_idx]
        return {
            "index": s["index"], "id": s["id"], "tag": s["tag"], "title": s["title"],
            "description": s["description"], "period": period, "period_label": PERIOD_LABELS[period],
            "options": {"yes": s["yes"]["label"], "no": s["no"]["label"]},
        }

    def get_next_situation(self):
        if self.game_over:
            return self._ending_payload()
        if self.current is None:
            self.current = self._pick()
        return self._public(self.current)

    # ----------------------------------------------------------------- flow
    def process_action(self, choice_index, action, solar=None, integrity=None):
        # solar/integrity sent by the client are ignored: the server state is authoritative.
        self.sol_report = None
        self.last_changes = None
        if self.game_over:
            return self._result("The mission has ended.")
        if self.current is None:
            self.current = self._pick()
        if choice_index != self.current["index"]:
            return self._result("Telemetry out of sync. Situation refreshed.")

        option = self.current[action]
        scale = self.crew / 4 if option.get("scale_crew") else 1.0
        changes = self._apply_effects(option["effects"], scale)
        message = option["message"]
        incident = None
        risk = option.get("risk")
        if risk and self.rng.random() < risk["chance"]:
            incident = {"text": risk["message"], "changes": self._apply_effects(risk["effects"])}
            message += " Incident: " + risk["message"]
        self.last_changes = {"choice": changes, "incident": incident}

        self._check_end()
        if not self.game_over:
            self.period_idx += 1
            if self.period_idx >= len(PERIODS):
                self._end_of_sol()
                self._check_end()
        self.current = None if self.game_over else self._pick()
        return self._result(message)

    def state_payload(self):
        """Used by the 'next' action so the client gets the dashboards on load."""
        if self.current is None and not self.game_over:
            self.current = self._pick()
        return self._result("")

    def _end_of_sol(self):
        flows = self._flows()
        _, _, net, _ = self._power()
        dust = self.site["dust_wear_multiplier"]
        changes = []
        for attr, label, unit in RESOURCES:
            old = getattr(self, attr)
            setattr(self, attr, max(0.0, old + flows[attr]))
            changes.append(self._change(label, getattr(self, attr) - old, unit, 1))
        old = self.integrity
        wear = DAILY_STRUCTURE_WEAR * dust + (1.0 if net < 0 else 0.0)
        self.integrity = max(0.0, old - wear)
        changes.append(self._change("Structure", self.integrity - old, "%", 2))
        old = self.solar
        self.solar = _clamp(old - DAILY_DUST_ON_SOLAR * dust, SOLAR_MIN, SOLAR_MAX)
        if round(self.solar - old, 2) != 0:
            changes.append(self._change("Solar efficiency", self.solar - old, "x", 2))
        self.sol_report = {"sol": self.sol, "power_deficit": net < 0, "changes": changes}
        self.sol += 1
        self.period_idx = 0

    def _check_end(self):
        causes = [
            (self.oxygen <= 0, "Asphyxiation", "The oxygen ran out. The crew did not survive."),
            (self.water <= 0, "Dehydration", "The water ran out. The crew did not survive."),
            (self.food <= 0, "Starvation", "The food ran out. The crew did not survive."),
            (self.integrity <= 0, "Habitat breach", "The habitat structure failed. The crew did not survive."),
        ]
        for hit, title, text in causes:
            if hit:
                return self._finish(False, title, text)
        if self.sol > self.duration:
            self._finish(True, "Mission complete", f"The crew survived all {self.duration} sols on Mars.")

    def _finish(self, victory, title, text):
        self.game_over, self.victory = True, victory
        self.ending = {"title": title, "description": text}

    def _ending_payload(self):
        return {
            "game_over": True, "victory": self.victory, **self.ending,
            "stats": {"sol": min(self.sol, self.duration), "science": round(self.science), "samples": sum(self.samples)},
        }

    # ------------------------------------------------------------ dashboards
    @staticmethod
    def _status(days_left):
        if days_left is None:
            return "ok"
        return "crit" if days_left < 10 else "warn" if days_left < 30 else "ok"

    def build_survival_dashboard(self):
        supply, demand, net, ratio = self._power()
        flows = self._flows()
        resources = []
        for attr, label, unit in RESOURCES:
            value, flow = getattr(self, attr), flows[attr]
            days = value / -flow if flow < 0 else None
            resources.append({
                "id": attr, "label": label, "unit": unit, "value": round(value, 1),
                "max": round(max(self.start[attr], value), 1), "net": round(flow, 2),
                "days_left": None if days is None else round(days, 1), "status": self._status(days),
            })
        t = NASA_CONSTANTS
        shell = 0.8 + 0.2 * self.integrity / 100  # pressure and ppO2 sag as the structure degrades
        return {
            "clock": {
                "sol": min(self.sol, self.duration), "duration": self.duration,
                "period": PERIODS[self.period_idx], "period_label": PERIOD_LABELS[PERIODS[self.period_idx]],
                "period_index": self.period_idx,
            },
            "resources": resources,
            "power": {
                "net": round(net, 1), "supply": round(supply, 1), "demand": round(demand, 1),
                "status": "ok" if ratio >= 1 else "warn" if ratio >= 0.8 else "crit",
                "solar_output": round(MODULES["solar_array"]["power_kwe"] * self.site["solar_efficiency"] * self.solar, 1)
                if self.modules["solar_array"] else 0.0,
            },
            "structure": {
                "integrity": round(self.integrity, 1),
                "status": "crit" if self.integrity < 30 else "warn" if self.integrity < 60 else "ok",
            },
            "habitat": {
                "temperature_c": round(t["TARGET_TEMP_C"] - max(0.0, -net) * 0.3, 1),
                "pressure_psi": round(t["HABITAT_PRESSURE_PSI"] * shell, 2),
                "ppo2_mmhg": round(t["TARGET_PPO2_MMHG"] * shell, 1),
                "humidity_pct": t["TARGET_HUMIDITY_PCT"],
                "radiation_msv_day": round(t["BASE_MARS_RADIATION_MSV_DAY"] * (1 - self.site["natural_radiation_shielding"]), 2),
            },
            "modules": [
                {"id": m, "name": MODULES[m]["name"], "active": on, "online": on and ratio >= 0.5}
                for m, on in self.modules.items()
            ],
            "sol_report": self.sol_report,
        }

    def build_research_dashboard(self):
        rank_idx = max(i for i, (need, _) in enumerate(RANKS) if self.science >= need)
        nxt = RANKS[rank_idx + 1][0] if rank_idx + 1 < len(RANKS) else None
        return {
            "site": self.site["short_name"], "multiplier": self.site["science_multiplier"],
            "score": round(self.science), "rank": RANKS[rank_idx][1], "next_rank_at": nxt,
            "objectives": [
                {"name": o["name"], "count": self.samples[i], "target": o["target"],
                 "pct": min(100, round(100 * self.samples[i] / o["target"]))}
                for i, o in enumerate(self.objectives)
            ],
            "samples_total": sum(self.samples),
            "avg_per_sol": round(self.science / max(1, self.sol - 1), 1),
        }

    def _result(self, message):
        _, _, net, _ = self._power()
        return {
            "solar": round(self.solar, 2), "power": round(net, 1), "integrity": round(self.integrity, 1),
            "message": message, "changes": self.last_changes, "situation": self.get_next_situation(),
            "survival_dashboard": self.build_survival_dashboard(),
            "research_dashboard": self.build_research_dashboard(),
        }


validate_situations(SITUATIONS)