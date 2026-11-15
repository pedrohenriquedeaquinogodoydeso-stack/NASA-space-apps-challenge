#################################################################
# situations.py
#
# Data catalogue for the survival phase: decision situations and science objectives.
# Edit/extend this file with real NASA-inspired events. game.py only reads it.
#
# HOW AN EVENT WORKS
#   Every event has a "yes" and a "no" option, both built with opt(label, message, effects, risk).
#   1. The effects of the chosen option are ALWAYS applied.
#   2. If the option has a risk, the game then rolls once: with probability `chance` the
#      risk's effects are applied ON TOP, as an "incident" (its message is appended and the
#      HUD lists the changes under "Incident"). The roll is independent for every decision.
#   3. rk(chance, message, **effects) builds the risk: rk(0.30, "A suit tears.", integrity=-5).
#      Only one risk per option; its effects are never scaled by crew size.
#   4. A stressed crew makes more mistakes: the real chance is
#      min(0.95, chance * (1 + 0.5 * stress / 100)), so at stress 0 it equals `chance`.
#   Rule of thumb: the expected cost of a risk is chance x effect.
#
# EFFECT KEYS (all optional, usable both in effects and in risks)
#   oxygen_kg, water_l, food_kg  -> resource delta
#   integrity                    -> habitat structure delta (0-100)
#   solar                        -> solar-array efficiency multiplier delta (0.4-2.0)
#   science                      -> science points (gains are multiplied by the site multiplier
#                                   and reduced when crew stress is above 50)
#   sample                       -> index of the site objective that gets +1 sample (0 or 1)
#   power                        -> TEMPORARY change of the net power balance in kWe
#                                   (negative = the event drains power, positive = it saves power)
#   power_sols                   -> how many sols the power change lasts (integer, default 2).
#                                   Only valid together with "power".
#   stress                       -> crew stress delta (0-100). POSITIVE = MORE STRESS (bad).
#                                   Negative values relax the crew (rest, shared meals, good news).
#
# SITUATION KEYS
#   periods          -> list of "morning"/"afternoon"/"night" (None = any)
#   sites            -> list of site ids (None = every site)
#   requires         -> dict of conditions, ALL must be true for the event to appear:
#       "modules":         ["greenhouse"]          modules that must be equipped
#       "without_modules": ["moxie_isru"]          modules that must NOT be equipped
#       <stat>: {"min": a, "max": b}               either bound is optional; a bare number means min
#     stats: oxygen_kg, water_l, food_kg, integrity, solar, power (net kWe), stress,
#            crew, sol, science, samples
#     (the old form  "requires": ["greenhouse"]  still works)
#   scheduled_every  -> forced on the morning of every N-th sol
#   urgent           -> True: as soon as its conditions hold the event jumps the queue
#                       (the 5-decision "recently seen" memory still prevents spam)
#   nasa             -> REAL-WORLD BASIS of the event (see nasa() below). Optional; when present the
#                       HUD shows a "Real NASA event/data" badge with the source link.
#
# nasa() "kind":
#   "event"  -> the situation really happened (or is a close retelling of something that did)
#   "data"   -> real measurements/figures were used to write or scale the situation
#   "analog" -> a plausible extrapolation; only the underlying numbers are real
#################################################################

PERIODS = ["morning", "afternoon", "night"]
PERIOD_LABELS = {"morning": "Morning", "afternoon": "Afternoon", "night": "Night"}

SITE_OBJECTIVES = {
    "jezero": [
        {"id": "biosignatures", "name": "Biosignature rock cores", "target": 8},
        {"id": "delta", "name": "Delta sediment samples", "target": 8},
    ],
    "arcadia": [
        {"id": "ice_cores", "name": "Subsurface ice cores", "target": 8},
        {"id": "ice_survey", "name": "Radar ice-depth surveys", "target": 6},
    ],
    "gale": [
        {"id": "clay", "name": "Clay-mineral drill samples", "target": 8},
        {"id": "strata", "name": "Mount Sharp strata logs", "target": 8},
    ],
    "valles_marineris": [
        {"id": "strata", "name": "Canyon wall strata samples", "target": 8},
        {"id": "hydrated", "name": "Hydrated mineral scans", "target": 6},
    ],
}

NASA_KINDS = ("event", "data", "analog")


def opt(label, message, effects=None, risk=None, scale_crew=False):
    return {
        "label": label,
        "message": message,
        "effects": effects or {},
        "risk": risk,
        "scale_crew": scale_crew
    }


def rk(chance, message, **effects):
    return {
        "chance": chance,
        "message": message,
        "effects": effects
    }


def nasa(kind, fact, source, url=None):
    """Real-world basis of an event. `fact` is written in our own words."""
    return {"kind": kind, "fact": fact, "source": source, "url": url}


SITUATIONS = [
    # ==========================================
    # SCHEDULED
    # ==========================================
    {
        "id": "resupply",
        "tag": "LOGISTICS",
        "periods": ["morning"],
        "scheduled_every": 45,
        "title": "Cargo lander window",
        "description": "A pre-positioned cargo lander touched down 6 km away. The route crosses sharp, embedded bedrock, the kind of terrain that punched holes in Curiosity's aluminum wheels within its first 18 months.",
        "yes": opt(
            "Send the rover on the full cargo-recovery EVA",
            "All crates secured, but life support reserves took a heavy hit.",
            {"oxygen_kg": 120, "water_l": 80, "food_kg": 250, "stress": 4, "power": -2.0, "power_sols": 2},
            rk(0.45, "Sharp bedrock punctures a wheel skin and tears a suit on the return.", integrity=-8, oxygen_kg=-25, water_l=-15, stress=4),
            scale_crew=True
        ),
        "no": opt(
            "Recover only the nearest crates to conserve life support",
            "A modest haul safely brought in.",
            {"oxygen_kg": 20, "food_kg": 60},
            scale_crew=True
        ),
        "nasa": nasa(
            "event",
            "Curiosity's thin aluminum wheels were punctured by sharp Gale Crater bedrock much faster than predicted. "
            "JPL re-routed it over smoother ground (2014) and uploaded a new wheel-speed control algorithm (2017). "
            "Engineers estimated a wheel has used about 60% of its life once three treads (grousers) break.",
            "NASA/JPL, Curiosity wheel-wear reports 2014-2017; Caltech paper on wheel damage (2017)",
            "https://authors.library.caltech.edu/records/btxrk-e7662",
        ),
    },

    # ==========================================
    # MORNING SITUATIONS
    # ==========================================
    {
        "id": "solar_blackout_comms",
        "tag": "COMMS",
        "periods": ["morning"],
        "title": "Earth communication blackout",
        "description": "A solar coronal mass ejection has temporarily cut the signal with Earth. The colony is on its own for the next few hours.",
        "yes": opt(
            "Make critical decisions autonomously",
            "Autonomous leadership resolves the immediate issue, but takes risks without validation.",
            {"science": 2},
            rk(0.40, "Decisions made without Earth's support lead to structural errors.", integrity=-6)
        ),
        "no": opt(
            "Pause complex operations until signal returns",
            "The base enters standby mode, losing valuable research time.",
            {"science": -5, "oxygen_kg": -2}
        ),
    },
    {
        "id": "dust_front",
        "tag": "WEATHER",
        "periods": ["morning"],
        "title": "Dust front approaching",
        "description": "Orbital imagery shows a regional dust front reaching the site by midday. In 2018 a front like this cut Opportunity's daily solar energy from 468 Wh to 133 Wh in just two sols.",
        "yes": opt(
            "Keep the array deployed and keep working",
            "The crew keeps sampling under a darkening sky.",
            {"science": 6, "stress": 2},
            rk(0.60, "Dust settles on the panels and output sags.", solar=-0.3, stress=2)
        ),
        "no": opt(
            "Stow the array and shelter in place",
            "Array stowed; the crew waits out the front.",
            {"oxygen_kg": -1.5, "science": -2, "stress": 1}
        ),
        "nasa": nasa(
            "event",
            "On sol 5105 (3 Jun 2018) Opportunity's panels made 468 Wh with tau about 1.0. Two sols later, with a regional storm overhead "
            "(tau estimated above 3), output was 133 Wh, and the team switched to a minimum-power plan.",
            "NASA/JPL Opportunity status reports, June 2018",
            "https://www.marsdaily.com/reports/Regional_dust_storm_is_affecting_Opportunity_Mars_rover_999.html",
        ),
    },
    {
        "id": "global_dust_storm",
        "tag": "WEATHER",
        "periods": ["morning"],
        "requires": {"modules": ["solar_array"], "sol": {"min": 20}},
        "title": "Planet-encircling dust storm",
        "description": "Orbiters report a storm growing toward global scale. In June 2018 the atmospheric opacity (tau) over Opportunity reached about 10.8, blotting out the Sun. The rover sent its last message on 10 June and never woke up again.",
        "yes": opt(
            "Enter survival mode and stow everything non-essential",
            "The base rides out the storm on minimum power.",
            {"science": -8, "oxygen_kg": -2, "stress": 3, "power": 1.5, "power_sols": 3}
        ),
        "no": opt(
            "Keep full operations and bet on the batteries",
            "The crew keeps the lab running while the sky goes dark.",
            {"science": 10, "stress": 5, "power": -3.0, "power_sols": 3},
            rk(0.60, "Batteries drain, heaters brown out and the habitat's thermal margin collapses.", integrity=-8, solar=-0.3, stress=6)
        ),
        "nasa": nasa(
            "event",
            "The 2018 global dust storm pushed tau at Opportunity's site to an estimated 10.8 (the 2007 storm was above 5.5). "
            "The rover went into low-power mode, last called home on 10 June 2018, and was never heard from again. "
            "Its heaters were vital but drew down the same battery it could not recharge.",
            "NASA/JPL, 'Opportunity hunkers down during dust storm', June 2018",
            "https://phys.org/news/2018-06-opportunity-hunkers-storm.html",
        ),
    },
    {
        "id": "eva_primary",
        "tag": "SCIENCE",
        "periods": ["morning"],
        "title": "Primary sampling EVA",
        "description": "The science team has a high-value target within walking range. A full EVA is possible, but suits and airlock take wear.",
        "yes": opt(
            "Run the EVA",
            "Samples collected and sealed.",
            {"oxygen_kg": -6, "sample": 0, "science": 12, "stress": 3, "power": -1.0, "power_sols": 1},
            rk(0.20, "A suit joint tears on the return.", integrity=-5, oxygen_kg=-4, stress=4)
        ),
        "no": opt(
            "Stay inside and analyse earlier material",
            "Lab work only; the target waits.",
            {"science": 3, "water_l": -2}
        ),
        "nasa": nasa(
            "data",
            "Sample capacity is a hard limit on real missions: Perseverance carries 43 titanium tubes and the plan is to return roughly 35 rock samples, "
            "so every target is weighed carefully. By September 2025 it had cached 30 samples.",
            "NASA/JPL Perseverance sample-caching updates (2021-2025)",
            "https://www.npr.org/2025/09/10/nx-s1-5536552/nasa-mars-rover-life-biosignature-rock-sample",
        ),
    },
    {
        "id": "suit_anomaly",
        "tag": "EVA",
        "periods": ["morning"],
        "title": "Water in the helmet",
        "description": "After the last EVA, about half a litre of water was found inside a helmet. The crew thinks it was just the drink bag. Another EVA is scheduled for this morning.",
        "yes": opt(
            "Stand the suit down and swap its fan/pump/separator",
            "The suit is rebuilt and tested; the EVA slips a day.",
            {"science": -3, "water_l": -4, "stress": 1}
        ),
        "no": opt(
            "Assume it was the drink bag and go anyway",
            "The EVA goes ahead on schedule.",
            {"science": 6, "stress": 3},
            rk(0.40, "Water floods the helmet mid-EVA. The walk is aborted and the crew rushes back through the airlock.", oxygen_kg=-8, science=-8, integrity=-3, stress=8)
        ),
        "nasa": nasa(
            "event",
            "On 9 Jul 2013 about 0.5-1 L of water was found in Luca Parmitano's helmet and blamed on his drink bag. A week later, on 16 Jul (EVA 23), "
            "1-1.5 L flooded his helmet and the spacewalk was aborted. The mishap board traced it to silica contamination blocking the suit's "
            "water separator and warned against accepting 'commonly accepted causes' for small anomalies.",
            "NASA EVA 23 Mishap Investigation Board / NASA APPEL lessons learned",
            "https://appel.nasa.gov/?p=339139",
        ),
    },
    {
        "id": "airlock_seal",
        "tag": "STRUCTURE",
        "periods": ["morning"],
        "title": "Airlock seal degraded",
        "description": "The inner airlock door seal is leaking slowly during the pressure check. Patching it is easy; making sure it stays fixed is the hard part.",
        "yes": opt(
            "Seal the cracks and re-check the pressure",
            "Seal replaced; base is tight, but crew is exhausted.",
            {"integrity": 4, "oxygen_kg": -8, "water_l": -10, "stress": 2},
            rk(0.25, "The leak returns after the next pressure cycle.", oxygen_kg=-6, integrity=-2, stress=3)
        ),
        "no": opt(
            "Close the hatch and isolate the compartment",
            "The compartment is sealed off and the leak contained, for now.",
            {"oxygen_kg": -2, "science": -3, "stress": 3},
            rk(0.45, "Fatigue cracks keep growing under repeated pressure cycles.", integrity=-5, stress=4)
        ),
        "nasa": nasa(
            "event",
            "Since 2019 the PrK transfer tunnel on the ISS Zvezda module has leaked. The rate rose from about 1.1 kg/day (2.4 lb) in Feb 2024 to a peak of 3.7 lb/day in April 2024. "
            "Cosmonauts sealed cracks and kept the hatch closed, and the leak has come back after repairs. NASA's Inspector General called it a top safety risk.",
            "NASA OIG report IG-24-020 (Sept 2024); NASA statements 2024-2026",
            "https://oig.nasa.gov/topics/space-operations/nasas-management-of-risks-to-sustaining-iss-operations-through-2030/",
        ),
    },
    {
        "id": "greenhouse_blight",
        "tag": "FOOD",
        "periods": ["morning"],
        "requires": ["greenhouse"],
        "title": "Blight in the plant habitat",
        "description": "A fungal bloom is spreading across one growing tray. Wet leaves and weak airflow are the usual culprits.",
        "yes": opt(
            "Cut away dead tissue, sanitize and boost airflow",
            "Tray cleaned and replanted.",
            {"food_kg": -4, "water_l": -10, "stress": -1, "power": -1.0, "power_sols": 2},
            rk(0.25, "The strong airflow dries out the surviving plants, which need extra water.", water_l=-8)
        ),
        "no": opt(
            "Harvest early and keep growing",
            "A quick harvest saves some crop.",
            {"food_kg": 2, "stress": 2},
            rk(0.60, "The blight reaches the other trays.", food_kg=-14, stress=3)
        ),
        "nasa": nasa(
            "event",
            "In Dec 2015 zinnias in the ISS Veggie garden developed mold after excess water and poor airflow. The fix (sanitize with wipes, cut dead tissue, run fans high) "
            "then dried the plants out and they needed more water. NASA let astronaut Scott Kelly decide when to water instead of waiting for Houston.",
            "NASA Veggie team release (Jan 2016)",
            "https://www.sciencedaily.com/releases/2016/01/160119143038.htm",
        ),
    },
    {
        "id": "solar_conjunction",
        "tag": "COMMS",
        "periods": ["morning"],
        "requires": {"sol": {"min": 100}},
        "title": "Solar conjunction blackout",
        "description": "Mars is about to pass behind the Sun. For roughly two weeks mission control will send no commands, and for two days you will not hear from Earth at all.",
        "yes": opt(
            "Follow the conjunction plan: low-risk work and passive monitoring only",
            "A quiet fortnight. Weather and radiation logs fill up and nothing breaks.",
            {"science": 3, "stress": 3}
        ),
        "no": opt(
            "Run the full schedule on your own authority",
            "The crew pushes on without any ground backup.",
            {"science": 9, "stress": 6},
            rk(0.40, "An anomaly hits with no ground support, and the rushed fix burns consumables.", oxygen_kg=-6, integrity=-4, stress=5)
        ),
        "nasa": nasa(
            "event",
            "In 2023 NASA stopped commanding its Mars fleet from 11 to 25 November because charged particles from the Sun's corona can corrupt radio commands. "
            "For two days Mars was fully behind the Sun and nothing was heard. The rovers parked and only did passive weather and radiation monitoring. This happens about every two years.",
            "NASA/JPL, 'NASA's Mars fleet will still conduct science while lying low', Nov 2023",
            "https://phys.org/news/2023-11-nasa-mars-fleet-science.html",
        ),
    },
    {
        "id": "water_rationing",
        "tag": "WATER",
        "periods": ["morning"],
        "requires": {"water_l": {"max": 300}},
        "title": "Water reserves critically low",
        "description": "The tanks are nearly empty. Mission control suggests strict rationing, the way ISS crews live on about a gallon (3.8 L) of water per person per day.",
        "yes": opt(
            "Ration strictly",
            "Showers and lab cooling are cut.",
            {"water_l": 25, "science": -5, "stress": 5, "power": 1.5, "power_sols": 3}
        ),
        "no": opt(
            "Keep the normal routine",
            "Life goes on as usual.",
            {},
            rk(0.50, "A pump runs dry and has to be replaced.", water_l=-30, integrity=-3, stress=3)
        ),
        "nasa": nasa(
            "data",
            "ISS crew members use close to one gallon of water per day. With the Brine Processor the station's total water recovery rose from 93-94% to 98%. "
            "Scott Kelly drank an estimated 730 L of recycled sweat and urine during his year in orbit.",
            "NASA ECLSS water-recovery announcement (2023)",
            "https://www.popsci.com/technology/iss-urine-water-recycling/",
        ),
    },

    # ==========================================
    # AFTERNOON SITUATIONS
    # ==========================================
    {
        "id": "solar_cleaning",
        "tag": "POWER",
        "periods": ["afternoon"],
        "requires": ["solar_array"],
        "title": "Dusty solar panels",
        "description": "Output dropped as dust built up on the array. Mars rovers have sometimes been lucky: wind gusts blew their panels clean, but nobody plans around luck.",
        "yes": opt(
            "EVA to clean the panels",
            "Panels wiped; output recovers.",
            {"solar": 0.25, "oxygen_kg": -5, "stress": 1},
            rk(0.15, "A cleaning brush catches a panel edge.", integrity=-3)
        ),
        "no": opt(
            "Leave them and run science instead",
            "The crew spends the time in the lab. No gust comes to help.",
            {"solar": -0.08, "science": 5}
        ),
        "nasa": nasa(
            "event",
            "In 2004 the Spirit and Opportunity teams discovered 'cleaning events': on several occasions battery levels rose because wind removed dust from the panels. "
            "In 2018 the Opportunity team was still hoping a dust devil would do the same after the global storm.",
            "NASA/JPL Opportunity updates, 2018",
            "https://phys.org/news/2018-08-martian-opportunity-rover.html",
        ),
    },
    {
        "id": "wpa_filter",
        "tag": "WATER",
        "periods": ["afternoon"],
        "requires": ["wpa_recycler"],
        "title": "Water recycler fouling",
        "description": "The recycler's recovery rate is falling as mineral scale builds up in the brine. You can back off, or keep squeezing out every last litre.",
        "yes": opt(
            "Throttle recovery to a safe level and flush the system",
            "Scale flushed; recovery steady at a lower, safer rate.",
            {"water_l": -15, "stress": 1, "power": -1.0, "power_sols": 1}
        ),
        "no": opt(
            "Keep pushing for maximum recovery",
            "The recycler keeps limping along.",
            {},
            rk(0.50, "The distillation unit clogs with scale and contaminated water has to be dumped.", water_l=-40, stress=4)
        ),
        "nasa": nasa(
            "event",
            "The ISS urine processor was designed to recover 85% of the water. In Oct 2010 calcium sulfate (gypsum), boosted by calcium from crew bone loss, clogged its distillation assembly. "
            "Operations dropped to 70% recovery, which raised resupply needs, until a new pretreatment was developed.",
            "NASA Marshall/JSC technical papers on UPA gypsum precipitation (2011, 2017)",
            "https://ntrs.nasa.gov/citations/20110023178",
        ),
    },
    {
        "id": "moxie_clog",
        "tag": "OXYGEN",
        "periods": ["afternoon"],
        "requires": ["moxie_isru"],
        "title": "MOXIE intake clogged",
        "description": "Abrasive dust is choking the atmospheric intake filter. The real MOXIE peaked at only 12 g of oxygen per hour, so every clogged hour is oxygen you never make.",
        "yes": opt(
            "Clean the intake on an EVA",
            "Intake cleared; oxygen output restored.",
            {"oxygen_kg": 10, "stress": 1},
            rk(0.15, "The EVA takes longer than planned.", integrity=-3, oxygen_kg=-4, stress=2)
        ),
        "no": opt(
            "Skip it and ration the oxygen",
            "Production stays low.",
            {"stress": 1},
            rk(0.50, "The pump overheats and shuts down.", oxygen_kg=-12, stress=3)
        ),
        "nasa": nasa(
            "analog",
            "Real MOXIE figures: 16 runs on Perseverance, 122 g of oxygen in total, peak 12 g/h at 98% purity or better (twice the goal), run at different times of day and season. "
            "The dust-intake failure itself is our extrapolation, not a reported MOXIE fault.",
            "NASA/JPL, 'MOXIE completes Mars mission', Sept 2023",
            "https://phys.org/news/2023-09-nasa-oxygen-generating-moxie-mars-mission.html",
        ),
    },
    {
        "id": "eva_secondary",
        "tag": "SCIENCE",
        "periods": ["afternoon"],
        "title": "Secondary target drill",
        "description": "The drill rig can reach a second target, but it needs coolant water and careful handling. The rock looks brittle.",
        "yes": opt(
            "Drill the target",
            "Core extracted and logged.",
            {"sample": 1, "science": 10, "water_l": -6, "stress": 2, "power": -1.5, "power_sols": 1},
            rk(0.25, "The brittle rock crumbles around the bit. Only a fragment is salvaged and the rig mount takes a beating.", integrity=-3, science=-6, stress=3)
        ),
        "no": opt(
            "Postpone the drilling",
            "The crew reviews old data instead.",
            {"science": 2}
        ),
        "nasa": nasa(
            "event",
            "On 6 Aug 2021 Perseverance drilled a hole about 8 cm deep on its first sampling attempt, but the tube came back empty. "
            "The rock was powdery and crumbled before reaching the tube. The team moved to a sturdier rock and succeeded about a month later.",
            "NASA/JPL Perseverance team updates, Aug-Sept 2021",
            "https://www.livescience.com/perseverance-rover-mars-sample-attempt-fails.html",
        ),
    },
    {
        "id": "comms_retask",
        "tag": "COMMS",
        "periods": ["afternoon"],
        "title": "Priority re-tasking from Earth",
        "description": "Mission control sends an urgent request. The signal delay is up to about 22 minutes each way, so there is no time for a discussion.",
        "yes": opt(
            "Follow the new plan",
            "Earth's target is sampled.",
            {"sample": 0, "science": 8, "food_kg": -2, "stress": 3},
            rk(0.20, "The rushed EVA wastes breathing gas.", oxygen_kg=-5, stress=2)
        ),
        "no": opt(
            "Stick to the local plan",
            "Earth is not happy with the delay.",
            {"science": -3, "stress": 2}
        ),
        "nasa": nasa(
            "data",
            "NASA's CHAPEA analog crews live in a 3D-printed Mars habitat for 378 days with communication delays of up to 22 minutes each way and limited resources, "
            "to study how crews cope. CHAPEA-2 finished on 31 Oct 2026.",
            "NASA Johnson, 'CHAPEA Mission 2 crew reflects after 378 days on simulated Mars'",
            "https://www.nasa.gov/centers-and-facilities/johnson/chapea-mission-2-crew-reflects-after-378-days-on-simulated-mars/",
        ),
    },
    {
        "id": "crew_tension",
        "tag": "CREW",
        "periods": ["afternoon"],
        "requires": {"crew": {"min": 6}},
        "title": "Tension in a large crew",
        "description": "Months in close quarters are wearing on the crew. An argument over chores is spreading.",
        "yes": opt(
            "Hold a crew meeting",
            "The air is cleared, but work stops for a while.",
            {"science": -3, "food_kg": -2, "stress": -6}
        ),
        "no": opt(
            "Ignore it and keep the schedule",
            "Everyone keeps working.",
            {"science": 2, "stress": 6},
            rk(0.50, "A shouting match ends with a damaged console.", integrity=-5, science=-6, stress=6)
        ),
        "nasa": nasa(
            "data",
            "Even the small, hand-picked four-person CHAPEA-1 crew (378 days, 2023-2024) reported 'crabby days' and boredom. "
            "NASA's Behavioral Health and Performance team studies these effects, along with exercise, nutrition and medical support.",
            "AFP/NASA, 'One year on Mars: inside NASA's ultra-realistic isolation study', July 2024",
            "https://phys.org/news/2024-07-year-mars-nasa-ultra-realistic.html",
        ),
    },
    {
        "id": "isolation_fatigue",
        "tag": "CREW",
        "periods": ["afternoon"],
        "requires": {"sol": {"min": 250}},
        "title": "Isolation fatigue",
        "description": "Months of identical days are blurring together. The urge to simply walk outside without a suit is getting stronger, not weaker.",
        "yes": opt(
            "Declare a rest sol with a shared meal and exercise",
            "Morale recovers, but the schedule slips.",
            {"science": -3, "food_kg": -3, "stress": -8}
        ),
        "no": opt(
            "Push on to protect the schedule",
            "The crew grinds through it.",
            {"science": 3, "stress": 6},
            rk(0.50, "Tempers fray and a tired mistake damages a console.", integrity=-4, science=-6, stress=4)
        ),
        "nasa": nasa(
            "data",
            "A CHAPEA-1 crew member said the longing to be outdoors did not fade over the 378 days; it grew toward the end. "
            "Researchers use these long analog missions to design countermeasures for real Mars crews.",
            "AFP/NASA, CHAPEA-1 coverage, July 2024",
            "https://phys.org/news/2024-07-year-mars-nasa-ultra-realistic.html",
        ),
    },

    # ==========================================
    # NIGHT SITUATIONS
    # ==========================================
    {
        "id": "thermal_fault",
        "tag": "STRUCTURE",
        "periods": ["night"],
        "title": "Thermal loop pump fault",
        "description": "The habitat temperature is dropping overnight. A stuck valve in the coolant pump is sending too-cold fluid through the loop.",
        "yes": opt(
            "Reroute power and shut non-essential systems",
            "Heat holds; non-essential loads and some experiments are shut down.",
            {"integrity": 3, "science": -4, "stress": 2, "power": 2.0, "power_sols": 2}
        ),
        "no": opt(
            "Wait and see",
            "The crew hopes the pump recovers.",
            {"stress": 3},
            rk(0.55, "Pipes freeze and crack, and the heaters run flat out.", integrity=-12, stress=4, power=-3.0, power_sols=2)
        ),
        "nasa": nasa(
            "event",
            "On 11 Dec 2013 a stuck internal valve shut down one of the ISS's two external ammonia cooling loops. Non-essential equipment was switched off and experiments paused. "
            "Astronauts Rick Mastracchio and Mike Hopkins replaced the 355 kg (780 lb) pump module in spacewalks on 21 and 24 December. The same pump had failed in 2010.",
            "NASA ISS Expedition 38 reports; AFP/AP, Dec 2013",
            "https://phys.org/news/2013-12-astronauts-rare-christmas-eve-spacewalk.html",
        ),
    },
    {
        "id": "radiation_alert",
        "tag": "RADIATION",
        "periods": ["night"],
        "title": "Solar particle event",
        "description": "A solar flare alert has been issued. Surface radiation will spike for several hours. In May 2024 Curiosity measured 8.1 mGy in one event (about 30 chest X-rays), its biggest surge in 12 years.",
        "yes": opt(
            "Move everyone to the storm shelter",
            "Crew shelters; lab work is paused.",
            {"science": -3, "food_kg": -2, "stress": 3}
        ),
        "no": opt(
            "Keep working in the lab",
            "Night shift continues.",
            {"science": 6, "stress": 2},
            rk(0.35, "Energetic particles corrupt instruments and control electronics.", integrity=-8, stress=4)
        ),
        "nasa": nasa(
            "event",
            "On 20 May 2024 an X12 flare and particle burst hit Mars. Curiosity's RAD instrument recorded about 8,100 micrograys, its largest surge since landing, "
            "and the rover's cameras filled with particle 'snow'. NASA noted that cliffsides or lava tubes would add shielding. "
            "A major 2003 flare knocked out Mars Odyssey's radiation detector.",
            "NASA/JPL, 'NASA Watches Mars Light Up During Epic Solar Storm', June 2024",
            "https://www.nasa.gov/solar-system/planets/mars/nasa-watches-mars-light-up-during-epic-solar-storm",
        ),
    },
    {
        "id": "micro_leak",
        "tag": "STRUCTURE",
        "periods": ["night"],
        "title": "Pressure drop detected",
        "description": "Sensors show a slow pressure loss in the habitat. Telemetry says it is not yet dangerous, so the crew could sleep through it.",
        "yes": opt(
            "Wake up and patch it now",
            "A pinhole is found and sealed with tape and epoxy.",
            {"oxygen_kg": -4, "integrity": 4, "stress": 4}
        ),
        "no": opt(
            "Let the crew sleep until morning",
            "The crew tries to sleep.",
            {"stress": 2},
            rk(0.50, "The leak grows overnight.", oxygen_kg=-20, integrity=-6, stress=6)
        ),
        "nasa": nasa(
            "event",
            "On the evening of 29 Aug 2018 ISS controllers saw a slight pressure drop and let the crew sleep. Next morning it was traced to a 2 mm hole in the Soyuz MS-09 orbital module. "
            "Crew members covered it with Kapton tape and then pushed in epoxy-soaked gauze, and pressure stabilised.",
            "NASA/Roscosmos statements, 30 Aug 2018",
            "https://spaceflightnow.com/2018/08/30/cosmonauts-plug-small-air-leak-on-the-international-space-station/",
        ),
    },
    {
        "id": "co2_scrubber",
        "tag": "OXYGEN",
        "periods": ["night"],
        "title": "CO2 climbing in the sleeping module",
        "description": "Carbon dioxide is rising overnight. The spare scrubber cartridges are the wrong shape for the unit that is installed.",
        "yes": opt(
            "Improvise an adapter from a suit hose, tape and cardboard",
            "The ugly adapter works and CO2 starts falling.",
            {"oxygen_kg": -3, "science": -2, "stress": 3, "power": -1.5, "power_sols": 2}
        ),
        "no": opt(
            "Wait for the morning shift",
            "The crew puts up with headaches.",
            {"stress": 4},
            rk(0.60, "CO2 builds up overnight and the crew has to flush the cabin with fresh oxygen.", oxygen_kg=-15, stress=6)
        ),
        "nasa": nasa(
            "event",
            "On Apollo 13 (April 1970) the lunar module's two round lithium hydroxide canisters were sized for two men for two days, not three men for four. "
            "The command module's spares were square. Ground engineers designed an adapter from a suit hose, tape and a flight-plan cover, "
            "and CO2 stayed below 2 mmHg for the rest of the trip home.",
            "NASA, Apollo 13 mission history (SP-350) and NASA image archive",
            "https://www.nasa.gov/wp-content/uploads/static/history/SP-350/ch-13-4.html",
        ),
    },
    {
        "id": "night_analysis",
        "tag": "SCIENCE",
        "periods": ["night"],
        "title": "Overnight spectrometer run",
        "description": "The spectrometer can process the day's samples through the night, but it needs cooling water.",
        "yes": opt(
            "Run the full analysis",
            "Data stored and sent to Earth.",
            {"science": 9, "water_l": -3, "stress": 1, "power": -2.0, "power_sols": 1}
        ),
        "no": opt(
            "Archive the data and rest",
            "The crew sleeps; analysis waits.",
            {"science": 2, "stress": -2}
        ),
        "nasa": nasa(
            "data",
            "Perseverance's PIXL X-ray instrument found iron- and phosphorus-rich minerals in the spots of the 'Cheyava Falls' rock. "
            "That analysis is the basis for the 'potential biosignature' announced in Nature in September 2025.",
            "NASA/JPL, Perseverance 'Sapphire Canyon' results, Sept 2025",
            "https://www.npr.org/2025/09/10/nx-s1-5536552/nasa-mars-rover-life-biosignature-rock-sample",
        ),
    },

    # ==========================================
    # CONDITIONAL SITUATIONS
    # ==========================================
    {
        "id": "aging_habitat",
        "tag": "STRUCTURE",
        "periods": ["night"],
        "requires": {"sol": {"min": 60}, "integrity": {"max": 70}},
        "title": "The habitat is showing its age",
        "description": "Creaks and small leaks have become common after two months of thermal cycling. Nobody agrees on exactly why the metal is cracking.",
        "yes": opt(
            "Do a full overnight inspection",
            "Weak points reinforced.",
            {"integrity": 8, "oxygen_kg": -4, "water_l": -6, "stress": 2, "power": -1.0, "power_sols": 1}
        ),
        "no": opt(
            "Postpone it",
            "The crew sleeps; the habitat keeps creaking.",
            {"stress": 3},
            rk(0.50, "A weld fails during the night.", integrity=-10, stress=5)
        ),
        "nasa": nasa(
            "event",
            "NASA believes the cracks in the ISS Zvezda PrK tunnel have several causes (pressure and mechanical stress, residual stress, material properties, environment). "
            "Russian specialists point to fatigue from micro-vibrations. The root cause was still unresolved years after the first leak.",
            "NASA OIG report IG-24-020 (Sept 2024); NASA Aerospace Safety Advisory Panel",
            "https://spacepolicyonline.com/?p=75872",
        ),
    },
    {
        "id": "crew_fatigue",
        "tag": "CREW",
        "periods": ["night"],
        "requires": {"sol": {"min": 100}},
        "title": "Crew fatigue",
        "description": "The crew has been working long days for months. Sleep is short and restless, and the schedule is slipping.",
        "yes": opt(
            "Declare a rest sol with a shared meal and exercise",
            "Morale recovers, but the schedule slips.",
            {"science": -5, "food_kg": -3, "water_l": -4, "stress": -8},
            scale_crew=True
        ),
        "no": opt(
            "Continue with the current schedule",
            "The crew pushes through the fatigue.",
            {"science": -2, "food_kg": -2, "water_l": -2, "stress": 5}
        )
    },
    {
        # Urgent: appears at the next decision as soon as stress reaches 70.
        # At stress 100 the mission ends ("Crew breakdown"), so this is the player's safety valve.
        "id": "stress_crisis",
        "tag": "CREW",
        "urgent": True,
        "requires": {"stress": {"min": 70}},
        "title": "Crew close to breaking point",
        "description": "Arguments, silence and sleepless nights: the crew is close to breaking point. One more bad decision could end the mission.",
        "yes": opt(
            "Stand down: rest, talk and eat together",
            "The crew gets its first real rest in weeks.",
            {"science": -8, "food_kg": -2, "stress": -15}
        ),
        "no": opt(
            "Push on and ask for one more effort",
            "The crew follows orders, barely.",
            {"science": 4, "stress": 5},
            rk(0.50, "An exhausted crew member makes a serious error at the console.", integrity=-8, science=-6, stress=8)
        ),
        "nasa": nasa(
            "data",
            "Even the small, hand-picked four-person CHAPEA-1 crew (378 days, 2023-2024) reported 'crabby days' and boredom. "
            "NASA's Behavioral Health and Performance team studies these effects, along with exercise, nutrition and medical support.",
            "AFP/NASA, 'One year on Mars: inside NASA's ultra-realistic isolation study', July 2024",
            "https://phys.org/news/2024-07-year-mars-nasa-ultra-realistic.html",
        ),
    },

    # ==========================================
    # SITE-SPECIFIC SITUATIONS
    # ==========================================
    {
        "id": "jezero_delta",
        "tag": "SITE",
        "periods": ["afternoon"],
        "sites": ["jezero"],
        "title": "Delta fan outcrop spotted",
        "description": "Orbital data shows layered delta deposits 2 km away. Jezero was chosen because its ancient river delta is a prime place to preserve traces of microbial life.",
        "yes": opt(
            "Make the long traverse",
            "Layered delta sediments collected.",
            {"sample": 1, "science": 18, "oxygen_kg": -9, "stress": 2, "power": -1.0, "power_sols": 1},
            rk(0.30, "Rough terrain damages equipment.", integrity=-5, stress=3)
        ),
        "no": opt(
            "Skip the traverse",
            "The outcrop is logged for later.",
            {"science": 2}
        ),
        "nasa": nasa(
            "data",
            "Perseverance landed in Jezero Crater in Feb 2021 specifically to sample an ancient river delta that NASA identified as a potentially rich place to find signs of ancient microbial life.",
            "NASA/JPL Mars 2020 mission overview, summarised by NPR, Sept 2025",
            "https://www.npr.org/2025/09/10/nx-s1-5536552/nasa-mars-rover-life-biosignature-rock-sample",
        ),
    },
    {
        "id": "jezero_biosignature",
        "tag": "SITE",
        "periods": ["morning"],
        "sites": ["jezero"],
        "title": "Leopard-spotted rock",
        "description": "A reddish, vein-filled mudstone beside an ancient river valley shows dark 'poppy seed' specks and larger 'leopard spots'. On Earth, features like these often come from microbial chemistry, but non-biological causes cannot be ruled out.",
        "yes": opt(
            "Core it and sample the vein system",
            "A promising core is sealed for the record, and morale lifts.",
            {"sample": 0, "science": 20, "oxygen_kg": -8, "stress": -3},
            rk(0.30, "The slope is steeper than the orbital map suggested.", integrity=-5, stress=4)
        ),
        "no": opt(
            "Image it and move on",
            "Remote imaging only.",
            {"science": 3}
        ),
        "nasa": nasa(
            "event",
            "In July 2024 Perseverance cored the 'Cheyava Falls' rock in Jezero's Bright Angel area (sample 'Sapphire Canyon', its 25th). "
            "It contains iron phosphate and iron sulfide minerals (vivianite and greigite) with spots and halos. "
            "NASA calls it a 'potential biosignature', not proof of life; abiotic explanations are not excluded.",
            "Hurowitz et al., Nature (Sept 2025); NASA news conference",
            "https://www.npr.org/2025/09/10/nx-s1-5536552/nasa-mars-rover-life-biosignature-rock-sample",
        ),
    },
    {
        "id": "arcadia_ice",
        "tag": "SITE",
        "periods": ["morning"],
        "sites": ["arcadia"],
        "title": "Radar shows shallow ice",
        "description": "Ground-penetrating radar confirms buried ice under a thin cover of dust and debris. Orbital radar suggests a sheet tens of metres thick, a possible water source.",
        "yes": opt(
            "Drill an ice core",
            "Ice core extracted; some water recovered.",
            {"sample": 0, "science": 14, "water_l": 40, "stress": 2, "power": -2.0, "power_sols": 1},
            rk(0.25, "The rig seizes in the ice.", integrity=-4, oxygen_kg=-4, stress=3)
        ),
        "no": opt(
            "Only run a surface radar survey",
            "Survey completed.",
            {"sample": 1, "science": 5}
        ),
        "nasa": nasa(
            "data",
            "Mars Reconnaissance Orbiter's SHARAD radar and thermal data show a buried ice sheet in Arcadia Planitia that is decameters thick, "
            "with radar returns reaching about 38 m. The flat, low-boulder terrain makes it a candidate for future human landings.",
            "NASA MRO SHARAD studies; Hibbard et al., Icarus (2021)",
            "https://phys.org/news/2021-05-mid-latitude-glaciers-mars-human-explorers.html",
        ),
    },
    {
        "id": "gale_wind",
        "tag": "SITE",
        "periods": ["afternoon"],
        "sites": ["gale"],
        "title": "Abrasive slope winds",
        "description": "Afternoon slope winds are lifting sand and dust and sandblasting seals and joints on the habitat. Curiosity sees dust lifting peak around solar noon.",
        "yes": opt(
            "Ignore it and keep drilling clay",
            "Drilling continues.",
            {"science": 4, "stress": 2},
            rk(0.50, "Grit gets into the joints.", integrity=-8, stress=3)
        ),
        "no": opt(
            "EVA to wipe and re-seal the joints",
            "Seals refreshed.",
            {"integrity": 5, "oxygen_kg": -4, "stress": 2}
        ),
        "nasa": nasa(
            "data",
            "A NASA study of Curiosity's navcam movies found dust lifting in Gale Crater clusters near solar noon and happens most often over sand-covered ground. "
            "Wind-abraded rocks (ventifacts) along the rover's route record long-term sandblasting.",
            "NASA Ames/JPL, Guzewich et al., dust lifting in Gale Crater (NTRS 2023)",
            "https://ntrs.nasa.gov/api/citations/20230016244/downloads/GuzewichDustSTI.pdf",
        ),
    },
    {
        "id": "valles_rockfall",
        "tag": "SITE",
        "periods": ["morning"],
        "sites": ["valles_marineris"],
        "title": "Canyon wall rockfall risk",
        "description": "A fresh rockfall scar shows exposed strata, but the wall above it is unstable. The canyon floor is already littered with old landslide debris.",
        "yes": opt(
            "Sample the strata anyway",
            "A rare strata sample is secured.",
            {"sample": 0, "science": 20, "oxygen_kg": -10, "stress": 4},
            rk(0.40, "Falling rock hits the rover and the airlock.", integrity=-10, stress=6)
        ),
        "no": opt(
            "Photograph it from a safe distance",
            "Remote imaging only.",
            {"science": 3}
        ),
        "nasa": nasa(
            "data",
            "MRO imaging shows Candor Chasma's floor is a complex mix of mesas, landslides, kilometres-thick layered deposits and dunes. "
            "Parts of Valles Marineris are 6-7 times deeper than the Grand Canyon.",
            "NASA/JPL/Univ. of Arizona (MRO CRISM and HiRISE)",
            "https://photojournal.jpl.nasa.gov/catalog/PIA09934",
        ),
    },
    {
        "id": "valles_sulfates",
        "tag": "SITE",
        "periods": ["afternoon"],
        "sites": ["valles_marineris"],
        "title": "Water-bearing sulfate layers",
        "description": "Orbital spectra flag a bright, layered outcrop rich in hydrated sulfates, minerals with water locked inside their crystals. Scanning it is easy; getting the water out is slow work.",
        "yes": opt(
            "Scan it and bake a sample to test the water yield",
            "The scan confirms hydrated minerals and a little water is recovered.",
            {"sample": 1, "science": 10, "water_l": 10, "stress": 1, "power": -2.5, "power_sols": 1},
            rk(0.20, "Rough ground on the way back damages equipment.", integrity=-3, stress=2)
        ),
        "no": opt(
            "Rely on the orbital spectra",
            "Data logged from orbit.",
            {"science": 3}
        ),
        "nasa": nasa(
            "data",
            "MRO's CRISM spectrometer and Mars Express mapped hydrated sulfates throughout Candor Chasma. HiRISE scientists describe these light-toned layers "
            "as a vast reservoir of water trapped in sulfate minerals, in regions where ice has long since sublimated.",
            "NASA/JPL/Univ. of Arizona, HiRISE ESP_072599_1735 (2022)",
            "https://hirise.lpl.arizona.edu/ESP_072599_1735",
        ),
    },
]