##################################
# constants.py
# 
# This file contains constants used throughout the application.
# This constants are NASA base data.
#
##################################

#===> THIS DATAS IS NOT ACTUAL YET!! NEED VERIFICATION <===
#
# Use NASA standards and references for accurate values.
#
NASA_CONSTANTS = {
    # NASA-STD-3001 (Daily consumption per crew member)
    "O2_KG_PER_PERSON_DAY": 0.835,
    "WATER_L_PER_PERSON_DAY": 2.5,
    "FOOD_KG_PER_PERSON_DAY": 1.8,
    "CO2_L_PRODUCED_PER_PERSON_DAY": 350.0,

    # NASA-STD-3001 / Habitats (Atmosphere & Pressure)
    "TARGET_PPO2_MMHG": 150.0,         # Normoxia target: 145-155 mmHg
    "HABITAT_PRESSURE_PSI": 8.2,       # 56.5 kPa (exploration atmosphere)
    "TARGET_TEMP_C": 22.0,             # Thermal comfort: 20-25°C
    "TARGET_HUMIDITY_PCT": 45.0,       # 30-60%

    # Mars DRA 5.0 & Kilopower
    "MAX_PAYLOAD_MASS_KG": 30000.0,    # 30 metric tons payload limit
    "BASE_HABITAT_POWER_KWE": 30.0,    # Base continuous demand (30-40 kWe)
    "KILOPOWER_OUTPUT_KWE": 10.0,      # 10 kWe per Kilopower reactor unit
    "WPA_RECOVERY_RATE": 0.93,         # 93% water recovery (ISS standard)

    # Curiosity RAD & Martian Environment
    "BASE_MARS_RADIATION_MSV_DAY": 0.64,  # Real average measured by RAD (~0.64 mSv/day)
    "MIN_SHIELDING_G_CM2": 10.0,          # Minimum reference shielding
    "EARTH_MARS_DELAY_MIN_RANGE": (4, 24), # Real comm delay range (4 to 24 minutes)

    # Lauching constants
    "INITIAL_OXIGEN_KG": 500.0,  # Initial mass at launch (50 metric tons)
    "INITIAL_WATER_L": 1500.0,  # Initial mass at launch (1.5 metric tons)
    "INITIAL_FOOD_KG": 800.0,   # Initial mass at launch (800 kg)
}

MARS_SITES = {
    "jezero": {
        "name": "Jezero Crater (Perseverance Landing Site)",
        "latitude": 18.38,
        "avg_temp_c": -55.0,
        "solar_efficiency": 1.0,
        "dust_wear_multiplier": 1.0,
        "isru_water_access": False,
        "natural_radiation_shielding": 0.0,
        "comm_window_efficiency": 1.0,
        "science_multiplier": 1.5,
    },
    "arcadia": {
        "name": "Arcadia Planitia",
        "latitude": 40.0,
        "avg_temp_c": -68.0,
        "solar_efficiency": 0.75,
        "dust_wear_multiplier": 0.8,
        "isru_water_access": True,  # Shallow subsurface ice detected by SHARAD/MRO radar
        "natural_radiation_shielding": 0.0,
        "comm_window_efficiency": 1.0,
        "science_multiplier": 1.0,
    },
    "gale": {
        "name": "Gale Crater / Mount Sharp (Curiosity Landing Site)",
        "latitude": -5.4,
        "avg_temp_c": -45.0,
        "solar_efficiency": 1.15,
        "dust_wear_multiplier": 1.35,  # Abrasive dust and slope winds
        "isru_water_access": False,
        "natural_radiation_shielding": 0.0,
        "comm_window_efficiency": 1.0,
        "science_multiplier": 1.3,
    },
    "valles_marineris": {
        "name": "Valles Marineris Canyon",
        "latitude": -14.0,
        "avg_temp_c": -50.0,
        "solar_efficiency": 0.65,  # Canyon walls block direct sunlight hours
        "dust_wear_multiplier": 1.1,
        "isru_water_access": False,
        "natural_radiation_shielding": 0.25,  # Partial natural protection from canyon walls
        "comm_window_efficiency": 0.60,       # Walls restrict direct Earth line-of-sight
        "science_multiplier": 1.8,
    },
}

MODULES = {
    "solar_array": {
        "mass_kg": 800.0,
        "power_kwe": 10.0
    },
    "wpa_recycler": {
        "mass_kg": 1200.0,
        "power_kwe": 5.0
    },
    "greenhouse": {
        "mass_kg": 2500.0,
        "power_kwe": 15.0
    },
    "moxie_isru": {
        "mass_kg": 1000.0,
        "power_kwe": 20.0
    }
}

ROCKET_ARCHITECTURES = {
    "ares_v_ntr": {
        "name": "Ares V + Nuclear Thermal Rocket (NTR)",
        "surface_payload_limit_kg": 40000.0, # Full 40t surface delivery capacity
        "imleo_mass_kg": 848700.0,           # 848.7 metric tons in Low Earth Orbit
        "ares_v_launches_required": 9,       # 5 cargo + 4 crew launches
        "isp_seconds": 900.0,                # High efficiency (875-950s)
        "budget_cost_multiplier": 1.2,       # Higher R&D/tech cost, fewer launches
    },
    "ares_v_chemical": {
        "name": "Ares V + Chemical / Aerocapture",
        "surface_payload_limit_kg": 32000.0, # Reduced net cargo due to heavy propellant/aeroshell mass
        "imleo_mass_kg": 1251800.0,          # 1,251.8 metric tons in Low Earth Orbit
        "ares_v_launches_required": 12,      # 12 Ares V launches required
        "isp_seconds": 450.0,                # Standard LOX/LH2 chemical efficiency
        "budget_cost_multiplier": 1.0,       # Lower tech cost per engine, higher launch count
    }
}