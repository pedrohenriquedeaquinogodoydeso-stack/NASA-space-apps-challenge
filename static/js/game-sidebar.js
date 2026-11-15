/*
  Humanity’s Future Is Red - Mission sidebar on the game page (game.html)
  Mounts the shared MissionSidebar (mission-sidebar.js) with the setup chosen
  on the planning screen, so the player can check it while playing.
  Loaded after game.js: if it fails, the game itself keeps working.

  Parts of this file were written with AI assistance (Gemini, Claude)
*/
(function () {
    "use strict";

    const BOOT = JSON.parse(document.getElementById("game-bootstrap").textContent);
    const lo = BOOT.loadout;
    const nasa = BOOT.nasaConstants;

    const data = {
        crewSize: lo.crew_size,
        siteName: BOOT.site.name,
        siteTempC: BOOT.site.avg_temp_c,
        rocketName: lo.rocket_name,
        durationDays: lo.mission_duration_days,
        scienceGoal: lo.science_goal,
        sampleTargetMult: lo.sample_target_mult,
        loadout: lo,
        activeModules: BOOT.activeModules.map(function (id) {
            return { id: id, name: (BOOT.modules[id] || {}).name || id };
        }),
        baselines: {
            o2: nasa.O2_KG_PER_PERSON_DAY,
            water: nasa.WATER_L_PER_PERSON_DAY,
            food: nasa.FOOD_KG_PER_PERSON_DAY
        },
        radiationMsvDay: BOOT.radiationMsvDay
    };

    ReactDOM.createRoot(document.getElementById("mission-sidebar-root")).render(
        h(MissionSidebar, {
            data: data,
            title: "MISSION CONFIG",
            subtitle: "Your launch setup. Check it any time while you play.",
            live: false
        })
    );
})();