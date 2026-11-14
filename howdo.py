import constants
constants = constants.CONSTANTS

def sol():
    new_sol_water = constants.NUMBER_OF_ASTRONEERS * constants.WATER_PER_ASTRONEER
    new_sol_food = constants.NUMBER_OF_ASTRONEERS * constants.FOOD_PER_ASTRONEER
    new_sol_oxygen = constants.NUMBER_OF_ASTRONEERS * constants.OXYGEN_PER_ASTRONEER
    new_sol_energy = constants.EQUIPMENT * constants.ENERGY_PER_DAY
    return new_sol_water, new_sol_food, new_sol_oxygen, new_sol_energy