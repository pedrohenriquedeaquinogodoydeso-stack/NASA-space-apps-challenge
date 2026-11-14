#############################
#   File for storage the Pre-Mars mission loadout
#
# In here is gona be calculated the loadout for the mission, based on the constants and the landing site selected.
# The player choice number of crew members, landing site, modules ......
#

from src.constants import NASA_CONSTANTS, MODULES, ROCKET_ARCHITECTURES, MARS_SITES
from dataclasses import dataclass

@dataclass
class MissionLoadout:
    # Modules
    # Modules
    has_solar_array: bool
    has_wpa_recycler: bool
    has_greenhouse: bool
    has_moxie_isru: bool

    crew_size: int
    landing_site: str
    mission_duration_days: int
    rocket_architecture: str = "ares_v_ntr"

    total_mass_kg: float = 0.0
    modules_mass_kg: float = 0.0
    total_power_kwe: float = 0.0
    net_module_power_kwe: float = 0.0
    total_water_l: float = 0.0
    total_food_kg: float = 0.0
    total_o2_kg: float = 0.0
    total_co2_l: float = 0.0

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
            self.initial_food_kg
        )

        self.total_power_kwe = (
            (MODULES["solar_array"]["power_kwe"] if self.has_solar_array else 0) +
            (MODULES["wpa_recycler"]["power_kwe"] if self.has_wpa_recycler else 0) +
            (MODULES["greenhouse"]["power_kwe"] if self.has_greenhouse else 0) +
            (MODULES["moxie_isru"]["power_kwe"] if self.has_moxie_isru else 0)
        )

        # Net power balance from modules (generation minus consumption)
        solar_gen = (MODULES["solar_array"]["power_kwe"] * site_data["solar_efficiency"]) if self.has_solar_array else 0.0
        modules_draw = (
            (MODULES["wpa_recycler"]["power_kwe"] if self.has_wpa_recycler else 0.0) +
            (MODULES["greenhouse"]["power_kwe"] if self.has_greenhouse else 0.0) +
            (MODULES["moxie_isru"]["power_kwe"] if self.has_moxie_isru else 0.0)
        )
        self.net_module_power_kwe = round(solar_gen - modules_draw, 2)

    def to_dict(self):
        rocket_data = ROCKET_ARCHITECTURES.get(self.rocket_architecture, ROCKET_ARCHITECTURES["ares_v_ntr"])
        return {
            "crew_size": self.crew_size,
            "landing_site": self.landing_site,
            "mission_duration_days": self.mission_duration_days,
            "rocket_architecture": self.rocket_architecture,
            "rocket_name": rocket_data["name"],
            "modules_mass_kg": self.modules_mass_kg,
            "total_mass_kg": self.total_mass_kg,
            "max_payload_mass_kg": NASA_CONSTANTS["MAX_PAYLOAD_MASS_KG"],
            "base_habitat_power_kwe": NASA_CONSTANTS["BASE_HABITAT_POWER_KWE"],
            "total_power_kwe": self.total_power_kwe,
            "net_module_power_kwe": self.net_module_power_kwe,
            "total_o2_kg": round(self.total_o2_kg, 2),
            "total_water_l": round(self.total_water_l, 2),
            "total_food_kg": round(self.total_food_kg, 2),
        }

    