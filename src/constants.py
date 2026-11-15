##################################
# constants.py
# 
# This file contains constants used throughout the application.
# This constants are NASA base data.
#
# 
# Parts of this file were written with AI assistance (Gemini, Claude)
##################################

NASA_CONSTANTS = {
    # NASA-STD-3001 (Daily consumption per crew member)
    "O2_KG_PER_PERSON_DAY": 0.835,
    "WATER_L_PER_PERSON_DAY": 2.5,
    "FOOD_KG_PER_PERSON_DAY": 1.8,
    "CO2_L_PRODUCED_PER_PERSON_DAY": 350.0,

    # NASA-STD-3001 / Habitats (Atmosphere & Pressure)
    "TARGET_PPO2_MMHG": 150.0,
    "HABITAT_PRESSURE_PSI": 8.2,
    "TARGET_TEMP_C": 22.0,
    "TARGET_HUMIDITY_PCT": 45.0,

    # Mars DRA 5.0 & Kilopower
    "MAX_PAYLOAD_MASS_KG": 30000.0,
    "BASE_HABITAT_POWER_KWE": 30.0,
    "KILOPOWER_OUTPUT_KWE": 10.0,
    "WPA_RECOVERY_RATE": 0.93,

    # Curiosity RAD & Martian Environment
    "BASE_MARS_RADIATION_MSV_DAY": 0.64,
    "MIN_SHIELDING_G_CM2": 10.0,
    "EARTH_MARS_DELAY_MIN_RANGE": (4, 24),

    # Launching constants
    "INITIAL_OXIGEN_KG": 500.0,
    "INITIAL_WATER_L": 1500.0,
    "INITIAL_FOOD_KG": 800.0,
    "MAX_MODULES_MASS_KG": 2800.0,
}

MARS_SITES = {
    "jezero": {
        "name": "Jezero Crater (Perseverance Landing Site)",
        "short_name": "Jezero Crater",
        "latitude": 18.38,
        "latitude_label": "18.38° N",
        "avg_temp_c": -55.0,
        "solar_efficiency": 1.0,
        "dust_wear_multiplier": 1.0,
        "isru_water_access": False,
        "natural_radiation_shielding": 0.0,
        "comm_window_efficiency": 1.0,
        "science_multiplier": 1.5,
        "image": "jezero.png",
        "description": "An ancient lake basin with a well-preserved river delta. Chosen for the Perseverance rover mission to search for signs of ancient microbial life and collect samples for potential return to Earth.",
        "map_left": "68%",
        "map_top": "48%",
    },
    "arcadia": {
        "name": "Arcadia Planitia",
        "short_name": "Arcadia Planitia",
        "latitude": 40.0,
        "latitude_label": "40° N",
        "avg_temp_c": -68.0,
        "solar_efficiency": 0.75,
        "dust_wear_multiplier": 0.8,
        "isru_water_access": True,  # Shallow subsurface ice detected by radar
        "natural_radiation_shielding": 0.0,
        "comm_window_efficiency": 1.0,
        "science_multiplier": 1.0,
        "image": "arcadia.png",
        "description": "A smooth volcanic plain containing vast sheets of buried glacier-like water ice close to the surface. Highly prioritized by NASA Design Reference Architecture (DRA 5.0) for in-situ resource utilization (ISRU) water extraction to support human crews.",
        "map_left": "27%",
        "map_top": "30%",
    },
    "gale": {
        "name": "Gale Crater / Mount Sharp (Curiosity Landing Site)",
        "short_name": "Gale Crater",
        "latitude": -5.4,
        "latitude_label": "5.4° S",
        "avg_temp_c": -45.0,
        "solar_efficiency": 1.15,
        "dust_wear_multiplier": 1.35,  # Abrasive dust and slope winds
        "isru_water_access": False,
        "natural_radiation_shielding": 0.0,
        "comm_window_efficiency": 1.0,
        "science_multiplier": 1.3,
        "image": "gale.png",
        "description": "A 154-km-wide crater featuring a massive layered mountain (Aeolis Mons / Mount Sharp). Explored by the Curiosity rover to study Mars' historical transition from a wet, habitable environment to a dry desert.",
        "map_left": "82%",
        "map_top": "72%",
    },
    "valles_marineris": {
        "name": "Valles Marineris Canyon",
        "short_name": "Valles Marineris",
        "latitude": -14.0,
        "latitude_label": "14° S",
        "avg_temp_c": -50.0,
        "solar_efficiency": 0.65,  # Canyon walls block direct sunlight hours
        "dust_wear_multiplier": 1.1,
        "isru_water_access": False,
        "natural_radiation_shielding": 0.25,  # Partial natural protection
        "comm_window_efficiency": 0.60,       # Walls restrict direct line-of-sight
        "science_multiplier": 1.8,
        "image": "valles_marineris.png",
        "description": "A colossal tectonic canyon system stretching over 4,000 kilometers. Offers deep exposure of Martian crustal stratigraphy and provides partial natural radiation shielding inside the canyon floor for future habitats.",
        "map_left": "42%",
        "map_top": "74%",
    },
}

MODULES = {
    "solar_array": {
        "name": "Lightweight Solar Array",
        "mass_kg": 800.0,
        "power_kwe": 10.0,
        "is_generator": True,   
        "image": "solar_array.png",
        "pros": "Generates renewable surface power scaled by site solar efficiency with low launch mass.",
        "cons": "Power drops during dust storms or high-latitude winters; requires regular dust cleaning."
    },
    "wpa_recycler": {
        "name": "WPA Water Recycler",
        "mass_kg": 1200.0,
        "power_kwe": 5.0,
        "is_generator": False,
        "image": "wpa_recycler.png",
        "pros": "Recovers up to 93% of wastewater and humidity (ISS standard), drastically extending water reserves.",
        "cons": "Consumes continuous electrical power and requires spare filtration cartridges."
    },
    "greenhouse": {
        "name": "Veggie / Plant Habitat",
        "mass_kg": 2500.0,
        "power_kwe": 15.0,
        "is_generator": False,
        "image": "greenhouse.png",
        "pros": "Produces fresh food, recycles CO2 into O2, and boosts long-term crew morale.",
        "cons": "Heaviest surface module (2,500 kg) and demands 15 kWe for grow lights and thermal control."
    },
    "moxie_isru": {
        "name": "MOXIE Atmospheric ISRU",
        "mass_kg": 1000.0,
        "power_kwe": 20.0,
        "is_generator": False,
        "image": "moxie_isru.png",
        "pros": "Splits Martian CO2 atmosphere into breathable O2 and propellant oxidizer on-site.",
        "cons": "Highest power draw (20 kWe) and vulnerable to abrasive Martian dust clogging intake filters."
    }
}

ROCKET_ARCHITECTURES = {
    "ares_v_ntr": {
        "name": "Ares V + Nuclear Thermal Rocket (NTR)",
        "fuel_type": "Liquid Hydrogen (LH2) + Nuclear Reactor Core",
        "surface_payload_limit_kg": 103000.0,
        "imleo_mass_kg": 848700.0,
        "isp_seconds": 900.0,
        "budget_cost_multiplier": 1.2,
        "pros": "2x propellant efficiency (900s Isp), 32% less mass required in Earth orbit, faster transit windows.",
        "cons": "20% higher R&D cost, strict nuclear safety protocols, complex thermal reactor shielding."
    },
    "ares_v_chemical": {
        "name": "Ares V + Chemical / Aerocapture",
        "fuel_type": "Cryogenic LOX / LH2 + Martian Aerocapture",
        "surface_payload_limit_kg": 103000.0,
        "imleo_mass_kg": 1251800.0,
        "isp_seconds": 450.0,
        "budget_cost_multiplier": 1.0,
        "pros": "Flight-proven cryogenic propulsion, lower unit engine cost, uses Mars atmosphere to brake.",
        "cons": "Requires 403 t extra propellant in orbit, higher heavy-lift launch count, risky aerocapture entry."
    }
}