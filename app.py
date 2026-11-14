from flask import Flask, abort, render_template, request

from src.constants import MARS_SITES, MODULES, NASA_CONSTANTS, ROCKET_ARCHITECTURES
from src.mission_loadout import MissionLoadout

app = Flask(__name__)


@app.route('/')
def index():
    default_modules = ['solar_array', 'wpa_recycler']
    initial_loadout = build_loadout_from_params(
        crew_size=4,
        site_id='jezero',
        rocket_id='ares_v_ntr',
        active_modules=default_modules,
    )

    return render_template(
        'index.html',
        nasa_constants=NASA_CONSTANTS,
        mars_sites=MARS_SITES,
        modules=MODULES,
        rocket_architectures=ROCKET_ARCHITECTURES,
        default_modules=default_modules,
        initial_loadout=initial_loadout.to_dict(),
    )


@app.route('/api/preview_loadout', methods=['POST'])
def preview_loadout():
    data = request.get_json(silent=True) or {}
    crew_size = int(data.get('crew_size', 4))
    site_id = data.get('site', 'jezero')
    rocket_id = data.get('rocket', 'ares_v_ntr')
    active_modules = data.get('modules', [])

    if not 1 <= crew_size <= 12 or site_id not in MARS_SITES or rocket_id not in ROCKET_ARCHITECTURES:
        return jsonify({'error': 'Invalid mission parameters'}), 400

    loadout = build_loadout_from_params(
        crew_size=crew_size,
        site_id=site_id,
        rocket_id=rocket_id,
        active_modules=active_modules,
    )
    return jsonify(loadout.to_dict())

@app.route('/c')
def game1():
    return render_template('choosedificulty.html')

@app.route('/d')
def game2():
    return render_template('dict.html')


@app.route('/game')
def game():
    crew_size_value = request.args.get('crew_size', '4')
    try:
        crew_size = int(crew_size_value)
    except ValueError:
        abort(400)

    site_id = request.args.get('site', 'jezero')
    rocket_id = request.args.get('rocket', 'ares_v_ntr')
    raw_modules = request.args.get('modules', '')
    active_modules = [m for m in raw_modules.split(',') if m in MODULES]

    site_id = {'valles': 'valles_marineris'}.get(site_id, site_id)
    if (
        not 1 <= crew_size <= 12
        or site_id not in MARS_SITES
        or rocket_id not in ROCKET_ARCHITECTURES
    ):
        abort(400)

    site = MARS_SITES[site_id]
    rocket = ROCKET_ARCHITECTURES[rocket_id]
    loadout = build_loadout_from_params(
        crew_size=crew_size,
        site_id=site_id,
        rocket_id=rocket_id,
        active_modules=active_modules,
    )

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
        * (1.0 - site['natural_radiation_shielding'])
    )

    return render_template(
        'game.html',
        crew_size=crew_size,
        site=site,
        site_name=site['name'],
        temperature=site['avg_temp_c'],
        rocket=rocket,
        loadout=loadout,
        daily_requirements=daily_requirements,
        habitat_targets=habitat_targets,
        radiation_msv_day=radiation_msv_day,
    )


@app.route('/game/situation', methods=['POST'])
def game_situation():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400)

    action = payload.get('action')
    if action == 'next':
        return jsonify(situation=maybe_create_situation())
    if action not in ('yes', 'no'):
        abort(400)

    choice_index = payload.get('choice_index')
    if (
        isinstance(choice_index, bool)
        or not isinstance(choice_index, int)
        or choice_index != SITUATION['id']
    ):
        abort(400)

    solar = number_from_payload(payload, 'solar', 0.5, 1.5)
    integrity = number_from_payload(payload, 'integrity', 0, 100)

    if action == 'yes':
        solar = max(0.5, solar - 0.1)
        message = SITUATION['yes_consequence']
    else:
        integrity = max(0, integrity - 10)
        message = SITUATION['no_consequence']

    return jsonify(
        solar=solar,
        power=max(30, min(100, solar * 100)),
        integrity=integrity,
        message=message,
        situation=maybe_create_situation(),
    )


if __name__ == '__main__':
    app.run(debug=True)