#############################
#   File for storage the Pre-Mars mission loadout
#
# In here is gona be calculated the loadout for the mission, based on the constants and the landing site selected.
# The player choice number of crew members, landing site, modules ......
#

from constants import NASA_CONSTANTS, MARS_SITES, MODULES
from dataclasses import dataclass

@dataclass
class MissionLoadout:
    crew_size: int
    landing_site: str
    mission_duration_days: int
    
    total_mass_kg: float = 0.0
    total_power_kwe: float = 0.0
    total_water_l: float = 0.0
    total_food_kg: float = 0.0
    total_o2_kg: float = 0.0
    total_co2_l: float = 0.0

    # Modules
    has_solar_array: bool = True      # Lightweight solar panels (~800 kg)
    has_wpa_recycler: bool = True     # Water Processor Assembly (~1,200 kg)
    has_greenhouse: bool = False      # Veggie / Plant Habitat module (~2,500 kg)
    has_moxie_isru: bool = False      # Atmospheric O2 generator (~1,000 kg)
    extra_radiation_shielding_g_cm2: float = 10.0  # Extra water/polyethylene mass

    # Initial embedded supplies (kg or liters)
    initial_oxygen_kg: float = NASA_CONSTANTS["INITIAL_OXIGEN_KG"]
    initial_water_l: float = NASA_CONSTANTS["INITIAL_WATER_L"]
    initial_food_kg: float = NASA_CONSTANTS["INITIAL_FOOD_KG"]

    def calculate_kg_loadout(self):
        # Calculate the loadout based on crew size, mission duration, and constants.
        self.total_o2_kg = NASA_CONSTANTS["O2_KG_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        self.total_water_l = NASA_CONSTANTS["WATER_L_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        self.total_food_kg = NASA_CONSTANTS["FOOD_KG_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        self.total_co2_l = NASA_CONSTANTS["CO2_L_PRODUCED_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        
        # Calculate total mass and power based on modules and other factors.
        self.total_mass_kg = (
            (MODULES["solar_array"]["mass_kg"] if self.has_solar_array else 0) +
            (MODULES["wpa_recycler"]["mass_kg"] if self.has_wpa_recycler else 0) +
            (MODULES["greenhouse"]["mass_kg"] if self.has_greenhouse else 0) +
            (MODULES["moxie_isru"]["mass_kg"] if self.has_moxie_isru else 0) +
            self.initial_oxygen_kg +
            self.initial_water_l +  # Assuming water density ~1 kg/L
            self.initial_food_kg +
            (self.extra_radiation_shielding_g_cm2 * 10)  # Convert g/cm² to kg for a given area
        )

        self.total_power_kwe = (
            (MODULES["solar_array"]["power_kwe"] if self.has_solar_array else 0) +
            (MODULES["wpa_recycler"]["power_kwe"] if self.has_wpa_recycler else 0) +
            (MODULES["greenhouse"]["power_kwe"] if self.has_greenhouse else 0) +
            (MODULES["moxie_isru"]["power_kwe"] if self.has_moxie_isru else 0)
        )

        # Additional calculations can be added here based on landing site characteristics.