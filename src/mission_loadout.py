#############################
#   File for storage the Pre-Mars mission loadout
#
# In here is gona be calculated the loadout for the mission, based on the constants and the landing site selected.
# The player choice number of crew members, landing site, modules ......
#

from constants import NASA_CONSTANTS, MARS_SITES
from dataclasses import dataclass

@dataclass
class MissionLoadout:
    crew_size: int
    landing_site: str
    mission_duration_days: int
    modules: list
    total_mass_kg: float = 0.0
    total_power_kwe: float = 0.0
    total_water_l: float = 0.0
    total_food_kg: float = 0.0
    total_o2_kg: float = 0.0
    total_co2_l: float = 0.0

    def calculate_loadout(self):
        # Calculate the loadout based on crew size, mission duration, and constants.
        self.total_o2_kg = NASA_CONSTANTS["O2_KG_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        self.total_water_l = NASA_CONSTANTS["WATER_L_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        self.total_food_kg = NASA_CONSTANTS["FOOD_KG_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        self.total_co2_l = NASA_CONSTANTS["CO2_L_PRODUCED_PER_PERSON_DAY"] * self.crew_size * self.mission_duration_days
        
        # Calculate total mass and power based on modules and other factors.
        for module in self.modules:
            self.total_mass_kg += module.mass_kg
            self.total_power_kwe += module.power_kwe

        # Additional calculations can be added here based on landing site characteristics.