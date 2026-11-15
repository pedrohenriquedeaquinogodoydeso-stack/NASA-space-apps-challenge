##################################
# situations.py
#
# Data catalogue for the survival phase: decision situations and science objectives.
# Edit/extend this file with real NASA-inspired events. game.py only reads it.
#
# Effect keys (all optional):
#   oxygen_kg, water_l, food_kg  -> resource delta
#   integrity                    -> habitat structure delta (0-100)
#   solar                        -> solar-array efficiency multiplier delta (0.4-2.0)
#   science                      -> science points (positive gains use the site multiplier)
#   sample                       -> 0 or 1: +1 sample on the site's first/second objective
#
# Situation keys:
#   periods          -> list of "morning"/"afternoon"/"night" (None = any)
#   sites            -> list of site ids (None = every site)
#   requires         -> dict of conditions, ALL must be true for the event to appear:
#       "modules":         ["greenhouse"]          modules that must be equipped
#       "without_modules": ["moxie_isru"]          modules that must NOT be equipped
#       <stat>: {"min": a, "max": b}               either bound is optional; a bare number means min
#     stats: oxygen_kg, water_l, food_kg, integrity, solar, power (net kWe),
#            crew, sol, science, samples
#     (the old form  "requires": ["greenhouse"]  still works)
#   scheduled_every  -> forced on the morning of every N-th sol
##################################

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


def opt(label, message, effects=None, risk=None, scale_crew=False):
    return {"label": label, "message": message, "effects": effects or {},
            "risk": risk, "scale_crew": scale_crew}


def rk(chance, message, **effects):
    return {"chance": chance, "message": message, "effects": effects}


SITUATIONS = [
    # ---------- Scheduled ----------
    {"id": "resupply", "tag": "LOGISTICS", "periods": ["morning"], "scheduled_every": 45,
     "title": "Cargo lander window",
     "description": "A pre-positioned cargo lander touched down 6 km away. Supplies are waiting, but the trip is long and every hour outside costs oxygen.",
     "yes": opt("Send the rover on the full cargo-recovery EVA", "Most of the cargo is recovered.",
                {"oxygen_kg": 150, "water_l": 100, "food_kg": 320},
                rk(0.30, "The rover slips on a slope; crates and a seal are damaged.", integrity=-6, food_kg=-60),
                scale_crew=True),
     "no": opt("Recover only the nearest crates", "Only the closest crates are brought in.",
               {"oxygen_kg": 40, "food_kg": 80}, scale_crew=True)},

    # ---------- Morning ----------
    {"id": "dust_front", "tag": "WEATHER", "periods": ["morning"],
     "title": "Dust front approaching",
     "description": "Orbital imagery shows a regional dust front reaching the site by midday. Visibility and solar output will drop.",
     "yes": opt("Keep the array deployed and keep working", "The crew keeps sampling under a darkening sky.",
                {"science": 6}, rk(0.45, "Wind-blown grit scours the panels.", solar=-0.3, integrity=-4)),
     "no": opt("Stow the array and shelter in place", "Array stowed; the crew waits out the front.",
               {"oxygen_kg": -1.5, "science": -2})},

    {"id": "eva_primary", "tag": "SCIENCE", "periods": ["morning"],
     "title": "Primary sampling EVA",
     "description": "The science team has a high-value target within walking range. A full EVA is possible, but suits and airlock take wear.",
     "yes": opt("Run the EVA", "Samples collected and sealed.",
                {"oxygen_kg": -6, "sample": 0, "science": 12},
                rk(0.20, "A suit joint tears on the return.", integrity=-5, oxygen_kg=-4)),
     "no": opt("Stay inside and analyse earlier material", "Lab work only; the target waits.",
               {"science": 3, "water_l": -2})},

    {"id": "airlock_seal", "tag": "STRUCTURE", "periods": ["morning"],
     "title": "Airlock seal degraded",
     "description": "The inner airlock door seal is leaking slowly during the pressure check.",
     "yes": opt("Repair it now", "Seal replaced; pressure holds.", {"integrity": 6, "oxygen_kg": -3}),
     "no": opt("Defer the repair", "The leak is logged for later.", {},
               rk(0.50, "The seal gives way during an EVA cycle.", integrity=-10, oxygen_kg=-8))},

    {"id": "greenhouse_blight", "tag": "FOOD", "periods": ["morning"], "requires": ["greenhouse"],
     "title": "Blight in the plant habitat",
     "description": "A fungal bloom is spreading across one growing tray.",
     "yes": opt("Quarantine and replant the tray", "Tray cleaned and replanted.", {"food_kg": -4, "water_l": -10}),
     "no": opt("Harvest early and keep growing", "A quick harvest saves some crop.", {"food_kg": 2},
               rk(0.60, "The blight reaches the other trays.", food_kg=-14))},

    # ---------- Afternoon ----------
    {"id": "solar_cleaning", "tag": "POWER", "periods": ["afternoon"], "requires": ["solar_array"],
     "title": "Dusty solar panels",
     "description": "Output dropped as dust built up on the array.",
     "yes": opt("EVA to clean the panels", "Panels wiped; output recovers.", {"solar": 0.25, "oxygen_kg": -5},
                rk(0.15, "A cleaning brush catches a panel edge.", integrity=-3)),
     "no": opt("Leave them and run science instead", "The crew spends the time in the lab.", {"solar": -0.08, "science": 2})},

    {"id": "wpa_filter", "tag": "WATER", "periods": ["afternoon"], "requires": ["wpa_recycler"],
     "title": "Water recycler filter clogged",
     "description": "The WPA recovery rate is falling. The filter cartridge is saturated.",
     "yes": opt("Swap the cartridge now", "Recovery back to nominal.", {"water_l": -15}),
     "no": opt("Run it a few more sols", "The recycler keeps limping along.", {},
               rk(0.50, "Contaminated water has to be dumped.", water_l=-40))},

    {"id": "moxie_clog", "tag": "OXYGEN", "periods": ["afternoon"], "requires": ["moxie_isru"],
     "title": "MOXIE intake clogged",
     "description": "Abrasive dust is choking the atmospheric intake filter.",
     "yes": opt("Clean the intake on an EVA", "Intake cleared; oxygen output restored.", {"oxygen_kg": 10},
                rk(0.15, "The EVA takes longer than planned.", integrity=-3, oxygen_kg=-4)),
     "no": opt("Skip it and ration the oxygen", "Production stays low.", {},
               rk(0.50, "The pump overheats and shuts down.", oxygen_kg=-12))},

    {"id": "eva_secondary", "tag": "SCIENCE", "periods": ["afternoon"],
     "title": "Secondary target drill",
     "description": "The drill rig can reach a second target, but it needs coolant water and careful handling.",
     "yes": opt("Drill the target", "Core extracted and logged.", {"sample": 1, "science": 10, "water_l": -6},
                rk(0.25, "The drill binds and strains the rig mount.", integrity=-3)),
     "no": opt("Postpone the drilling", "The crew reviews old data instead.", {"science": 2})},

    {"id": "comms_retask", "tag": "COMMS", "periods": ["afternoon"],
     "title": "Priority re-tasking from Earth",
     "description": "Mission control sends an urgent request. Signal delay is 4 to 24 minutes each way, so there is no time for a discussion.",
     "yes": opt("Follow the new plan", "Earth's target is sampled.", {"sample": 0, "science": 8, "food_kg": -2},
                rk(0.20, "The rushed EVA wastes breathing gas.", oxygen_kg=-5)),
     "no": opt("Stick to the local plan", "Earth is not happy with the delay.", {"science": -3})},

    # ---------- Night ----------
    {"id": "thermal_fault", "tag": "STRUCTURE", "periods": ["night"],
     "title": "Thermal loop pump fault",
     "description": "The habitat temperature is dropping overnight after a coolant pump fault.",
     "yes": opt("Reroute power and shut non-essential systems", "Heat holds; some experiments are paused.",
                {"integrity": 3, "science": -4}),
     "no": opt("Wait and see", "The crew hopes the pump recovers.", {},
               rk(0.55, "Pipes freeze and crack.", integrity=-12))},

    {"id": "radiation_alert", "tag": "RADIATION", "periods": ["night"],
     "title": "Solar particle event",
     "description": "A solar flare alert has been issued. Radiation levels on the surface will spike for several hours.",
     "yes": opt("Move everyone to the storm shelter", "Crew shelters; lab work is paused.", {"science": -3, "food_kg": -2}),
     "no": opt("Keep working in the lab", "Night shift continues.", {"science": 6},
               rk(0.35, "Radiation corrupts instruments and control electronics.", integrity=-8))},

    {"id": "micro_leak", "tag": "STRUCTURE", "periods": ["night"],
     "title": "Pressure drop detected",
     "description": "Sensors show a slow pressure loss in the habitat. A micro-leak is likely.",
     "yes": opt("Patch it from the inside now", "Leak sealed.", {"oxygen_kg": -4, "integrity": 4}),
     "no": opt("Wait until morning", "The crew tries to sleep.", {},
               rk(0.60, "The leak grows overnight.", oxygen_kg=-20, integrity=-6))},

    {"id": "night_analysis", "tag": "SCIENCE", "periods": ["night"],
     "title": "Overnight spectrometer run",
     "description": "The spectrometer can process the day's samples through the night, but it needs cooling water.",
     "yes": opt("Run the full analysis", "Data stored and sent to Earth.", {"science": 9, "water_l": -3}),
     "no": opt("Archive the data and rest", "The crew sleeps; analysis waits.", {"science": 2})},

    # ---------- Conditional examples ----------
    {"id": "crew_tension", "tag": "CREW", "periods": ["afternoon"], "requires": {"crew": {"min": 6}},
     "title": "Tension in a large crew",
     "description": "Months in close quarters are wearing on the crew. An argument over chores is spreading.",
     "yes": opt("Hold a crew meeting", "The air is cleared, but work stops for a while.", {"science": -3, "food_kg": -2}),
     "no": opt("Ignore it and keep the schedule", "Everyone keeps working.", {"science": 2},
               rk(0.50, "A shouting match ends with a damaged console.", integrity=-5, science=-6))},

    {"id": "water_rationing", "tag": "WATER", "periods": ["morning"], "requires": {"water_l": {"max": 300}},
     "title": "Water reserves critically low",
     "description": "The tanks are nearly empty. Mission control suggests strict rationing.",
     "yes": opt("Ration strictly", "Showers and lab cooling are cut.", {"water_l": 25, "science": -5}),
     "no": opt("Keep the normal routine", "Life goes on as usual.", {},
               rk(0.50, "A pump runs dry and has to be replaced.", water_l=-30, integrity=-3))},

    {"id": "aging_habitat", "tag": "STRUCTURE", "periods": ["night"],
     "requires": {"sol": {"min": 60}, "integrity": {"max": 70}},
     "title": "The habitat is showing its age",
     "description": "Creaks and small leaks have become common after two months of thermal cycling.",
     "yes": opt("Do a full overnight inspection", "Weak points reinforced.", {"integrity": 8, "oxygen_kg": -4, "water_l": -6}),
     "no": opt("Postpone it", "The crew sleeps; the habitat keeps creaking.", {},
               rk(0.50, "A weld fails during the night.", integrity=-10))},

    # ---------- Site-specific ----------
    {"id": "jezero_delta", "tag": "SITE", "periods": ["afternoon"], "sites": ["jezero"],
     "title": "Delta fan outcrop spotted",
     "description": "Orbital data shows layered delta deposits 2 km away, a good place to look for signs of ancient life.",
     "yes": opt("Make the long traverse", "Layered rock samples collected.", {"sample": 0, "science": 18, "oxygen_kg": -9},
                rk(0.30, "Rough terrain damages equipment.", integrity=-5)),
     "no": opt("Skip the traverse", "The outcrop is logged for later.", {"science": 2})},

    {"id": "arcadia_ice", "tag": "SITE", "periods": ["morning"], "sites": ["arcadia"],
     "title": "Radar shows shallow ice",
     "description": "Ground-penetrating radar finds buried ice a few metres down, a possible water source.",
     "yes": opt("Drill an ice core", "Ice core extracted; some water recovered.", {"sample": 0, "science": 14, "water_l": 40},
                rk(0.25, "The rig seizes in the ice.", integrity=-4, oxygen_kg=-4)),
     "no": opt("Only run a surface radar survey", "Survey completed.", {"sample": 1, "science": 5})},

    {"id": "gale_wind", "tag": "SITE", "periods": ["afternoon"], "sites": ["gale"],
     "title": "Abrasive slope winds",
     "description": "Slope winds are sandblasting seals and joints on the habitat.",
     "yes": opt("EVA to wipe and re-seal the joints", "Seals refreshed.", {"integrity": 5, "oxygen_kg": -4}),
     "no": opt("Ignore it and keep drilling clay", "Drilling continues.", {"science": 4},
               rk(0.50, "Grit gets into the joints.", integrity=-8))},

    {"id": "valles_rockfall", "tag": "SITE", "periods": ["morning"], "sites": ["valles_marineris"],
     "title": "Canyon wall rockfall risk",
     "description": "A fresh rockfall scar shows exposed strata, but the wall above it is unstable.",
     "yes": opt("Sample the strata anyway", "A rare strata sample is secured.", {"sample": 0, "science": 20, "oxygen_kg": -10},
                rk(0.40, "Falling rock hits the rover and the airlock.", integrity=-10)),
     "no": opt("Photograph it from a safe distance", "Remote imaging only.", {"science": 3})},
]