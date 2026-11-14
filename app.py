from flask import Flask, abort, render_template, request

from src.constants import MARS_SITES, NASA_CONSTANTS

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():
    crew_size_value = request.args.get('crew_size', '4')
    try:
        crew_size = int(crew_size_value)
    except ValueError:
        abort(400)

    difficulties = {
        'easy': 'Easy',
        'standard': 'Standard',
        'hard': 'Hard',
    }
    difficulty = request.args.get('difficulty', 'standard')
    site_id = request.args.get('site', 'jezero')

    site_id = {'valles': 'valles_marineris'}.get(site_id, site_id)
    if not 1 <= crew_size <= 12 or difficulty not in difficulties or site_id not in MARS_SITES:
        abort(400)

    site = MARS_SITES[site_id]
    daily_requirements = {
        'oxygen_kg': NASA_CONSTANTS['O2_KG_PER_PERSON_DAY'] * crew_size,
        'water_l': NASA_CONSTANTS['WATER_L_PER_PERSON_DAY'] * crew_size,
        'food_kg': NASA_CONSTANTS['FOOD_KG_PER_PERSON_DAY'] * crew_size,
        'co2_l': NASA_CONSTANTS['CO2_L_PRODUCED_PER_PERSON_DAY'] * crew_size,
    }
    habitat_targets = {
        'oxygen_partial_pressure_mmhg': NASA_CONSTANTS['TARGET_PPO2_MMHG'],
        'pressure_psi': NASA_CONSTANTS['HABITAT_PRESSURE_PSI'],
        'temperature_c': NASA_CONSTANTS['TARGET_TEMP_C'],
        'humidity_pct': NASA_CONSTANTS['TARGET_HUMIDITY_PCT'],
    }
    radiation_msv_day = (
        NASA_CONSTANTS['BASE_MARS_RADIATION_MSV_DAY']
        * (1 - site['natural_radiation_shielding'])
    )

    return render_template(
        'game.html',
        crew_size=crew_size,
        difficulty=difficulties[difficulty],
        site=site,
        site_name=site['name'],
        temperature=site['avg_temp_c'],
        daily_requirements=daily_requirements,
        habitat_targets=habitat_targets,
        radiation_msv_day=radiation_msv_day,
    )


if __name__ == '__main__':
    app.run(debug=True)
