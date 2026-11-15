/*
  Mars Mission Planner - Frontend Application Logic
  Handles user interface interactions, telemetry updates, and API communications.
*/

const h = React.createElement;
const BOOTSTRAP = JSON.parse(document.getElementById("mission-bootstrap").textContent);

const NASA_CONSTANTS = BOOTSTRAP.nasaConstants;
const MARS_SITES = BOOTSTRAP.marsSites;
const MODULES = BOOTSTRAP.modules;
const ROCKET_ARCHITECTURES = BOOTSTRAP.rocketArchitectures;

const colors = {
    background: "#311e00",
    panel: "rgba(58, 0, 0, 0.78)",
    text: "#f4f7ff",
    muted: "#a7b3c9",
    orange: "#ff764a",
    cyan: "#70e1e8",
    green: "#56e39f",
    red: "#ff6b6b",
    border: "rgba(173, 194, 225, 0.17)"
};

const page = {
    minHeight: "100vh",
    color: colors.text,
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    background:
        "radial-gradient(ellipse at 82% 35%, rgba(32, 71, 116, 0.28), transparent 38%), " +
        "radial-gradient(ellipse at 12% 4%, rgba(255, 118, 74, 0.11), transparent 32%), " +
        colors.background
};

const container = {
    width: "min(1120px, calc(100% - 48px))",
    margin: "0 auto"
};

function App() {
    const [screen, setScreen] = React.useState("landing");
    const [crewSize, setCrewSize] = React.useState(BOOTSTRAP.initialLoadout.crew_size);
    const [siteId, setSiteId] = React.useState(BOOTSTRAP.initialLoadout.landing_site);
    const [rocketId, setRocketId] = React.useState(BOOTSTRAP.initialLoadout.rocket_architecture);
    const [activeModules, setActiveModules] = React.useState(BOOTSTRAP.defaultModules);
    const [durationDays, setDurationDays] = React.useState(BOOTSTRAP.initialLoadout.mission_duration_days || 500);
    const [scienceGoal, setScienceGoal] = React.useState(BOOTSTRAP.initialLoadout.science_goal || 500);
    const [sampleTargetMult, setSampleTargetMult] = React.useState(BOOTSTRAP.initialLoadout.sample_target_mult || 1.0);
    const [loadoutPreview, setLoadoutPreview] = React.useState(BOOTSTRAP.initialLoadout);

    const selectedSite = MARS_SITES[siteId];
    const selectedRocket = ROCKET_ARCHITECTURES[rocketId];

    const baseSuppliesMassKg =
        NASA_CONSTANTS.INITIAL_OXIGEN_KG +
        NASA_CONSTANTS.INITIAL_WATER_L +
        NASA_CONSTANTS.INITIAL_FOOD_KG;

    // Fetch dynamic loadout calculations from backend when parameters change
    React.useEffect(function () {
        let cancelled = false;
        fetch("/api/preview_loadout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                crew_size: crewSize,
                site: siteId,
                rocket: rocketId,
                modules: activeModules,
                duration_days: durationDays,
                science_goal: scienceGoal,
                sample_target_mult: sampleTargetMult
            })
        })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (!cancelled && !data.error) {
                    setLoadoutPreview(data);
                }
            })
            .catch(function () {});

        return function () { cancelled = true; };
    }, [crewSize, siteId, rocketId, activeModules.join(","), durationDays, scienceGoal, sampleTargetMult]);

    function toggleModule(modId) {
        setActiveModules(function (prev) {
            if (prev.includes(modId)) {
                return prev.filter(function (id) { return id !== modId; });
            }
            return prev.concat([modId]);
        });
    }

    const highlights = [
        { number: "01", label: "CHOOSE A LANDING SITE", detail: "Jezero, Arcadia, and more" },
        { number: "02", label: "BUILD YOUR MISSION", detail: "Propulsion, modules, and crew" },
        { number: "03", label: "SURVIVE ON MARS", detail: "Every choice shapes the outcome" }
    ];

    function plannerContent() {
        const gameUrl = "/game?crew_size=" + crewSize +
            "&site=" + encodeURIComponent(siteId) +
            "&rocket=" + encodeURIComponent(rocketId) +
            "&modules=" + encodeURIComponent(activeModules.join(",")) +
            "&duration=" + durationDays +
            "&science_goal=" + scienceGoal +
            "&sample_target_mult=" + sampleTargetMult;

        return h("section", {
            style: Object.assign({}, container, { paddingTop: "44px", paddingBottom: "60px" })
        },
            h("button", {
                type: "button",
                onClick: function () { setScreen("landing"); },
                style: {
                    padding: "8px 0",
                    border: "none",
                    background: "transparent",
                    color: colors.cyan,
                    cursor: "pointer",
                    fontSize: "11px",
                    fontWeight: 800,
                    letterSpacing: "1.2px"
                }
            }, "← BACK TO OVERVIEW"),

            // Ares V rocket banner displayed at the top of the planning screen
            h("div", {
                style: {
                    display: "flex",
                    alignItems: "center",
                    gap: "20px",
                    marginTop: "20px",
                    marginBottom: "28px",
                    padding: "20px",
                    border: "1px solid " + colors.border,
                    borderRadius: "8px",
                    background: colors.panel,
                    flexWrap: "wrap"
                }
            },
                h("img", {
                    src: "/static/imgs/ares_v.png",
                    alt: "Ares V Heavy-Lift Rocket Pixel Art",
                    style: {
                        width: "110px",
                        height: "auto",
                        objectFit: "contain",
                        filter: "drop-shadow(0 10px 20px rgba(0,0,0,0.4))"
                    }
                }),
                h("div", { style: { flex: 1, minWidth: "220px" } },
                    h("div", { style: { color: colors.cyan, fontSize: "10px", fontWeight: 800, letterSpacing: "1.5px" } }, "HEAVY-LIFT PROPULSION // ARES V"),
                    h("h3", { style: { margin: "4px 0 6px", fontSize: "18px", fontWeight: 800 } }, "Mission Architecture & Launch Manifest"),
                    h("p", { style: { margin: 0, color: colors.muted, fontSize: "12px", lineHeight: 1.6 } }, "Configure your surface modules, payload mass limits, and crew life support provisions before initiating terminal countdown.")
                )
            ),

            h("div", { style: { margin: "22px 0 28px" } },
                h("div", {
                    style: {
                        color: colors.orange,
                        fontSize: "10px",
                        fontWeight: 800,
                        letterSpacing: "2px"
                    }
                }, "MISSION PLANNER // STEP 01"),
                h("h1", {
                    style: {
                        margin: "10px 0 8px",
                        fontSize: "clamp(34px, 5vw, 52px)",
                        letterSpacing: "-2px"
                    }
                }, "Build your mission plan"),
                h("p", {
                    style: { margin: 0, color: colors.muted, fontSize: "14px", lineHeight: 1.7 }
                }, "Configure your landing site, rocket propulsion architecture, surface payload modules, and crew before launch.")
            ),

            // Top section: Map & Sticky Telemetry Preview Sidebar
            h("div", {
                style: {
                    display: "flex",
                    alignItems: "flex-start",
                    flexWrap: "wrap",
                    gap: "20px"
                }
            },
                h("section", {
                    style: {
                        flex: "1 1 540px",
                        minWidth: "0",
                        padding: "20px",
                        border: "1px solid " + colors.border,
                        borderRadius: "8px",
                        background: colors.panel,
                        boxSizing: "border-box"
                    },
                    "aria-label": "Mars thermal map"
                },
                    h("div", {
                        style: {
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            flexWrap: "wrap",
                            gap: "10px",
                            marginBottom: "16px"
                        }
                    },
                        h("div", { style: { fontSize: "11px", fontWeight: 800, letterSpacing: "1.3px" } }, "MARS THERMAL MAP"),
                        h("span", { style: { color: colors.muted, fontSize: "10px" } }, "SCHEMATIC · PROJECT ESTIMATES")
                    ),
                    h("div", {
                        style: {
                            position: "relative",
                            minHeight: "350px",
                            overflow: "hidden",
                            border: "1px solid rgba(255,255,255,.1)",
                            borderRadius: "6px",
                            background:
                                "radial-gradient(ellipse at 73% 72%, rgba(255, 104, 57, .86), transparent 18%), " +
                                "radial-gradient(ellipse at 42% 74%, rgba(255, 139, 66, .72), transparent 20%), " +
                                "radial-gradient(ellipse at 68% 48%, rgba(255, 125, 68, .64), transparent 21%), " +
                                "radial-gradient(ellipse at 27% 30%, rgba(81, 163, 232, .85), transparent 22%), " +
                                "radial-gradient(ellipse at 45% 45%, rgba(187, 80, 57, .9), transparent 56%), " +
                                "linear-gradient(140deg, #552c38, #ad533a 48%, #482b3d)",
                            backgroundSize: "cover",
                            boxShadow: "inset 0 0 70px rgba(6, 9, 20, .55)"
                        }
                    },
                        h("div", {
                            style: {
                                position: "absolute",
                                inset: 0,
                                opacity: .14,
                                backgroundImage: "linear-gradient(rgba(255,255,255,.3) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 1px)",
                                backgroundSize: "40px 40px",
                                pointerEvents: "none"
                            }
                        }),
                        Object.entries(MARS_SITES).map(function (entry) {
                            const key = entry[0];
                            const site = entry[1];
                            const isSelected = key === siteId;
                            return h("button", {
                                key: key,
                                type: "button",
                                onClick: function () { setSiteId(key); },
                                "aria-pressed": isSelected,
                                "aria-label": site.short_name + ", average temperature " + site.avg_temp_c + " degrees Celsius",
                                title: site.name + " · " + site.avg_temp_c + "°C",
                                style: {
                                    position: "absolute",
                                    left: site.map_left,
                                    top: site.map_top,
                                    transform: "translate(-50%, -50%)",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "7px",
                                    padding: "7px 9px",
                                    border: "1px solid " + (isSelected ? colors.cyan : "rgba(255,255,255,.42)"),
                                    borderRadius: "20px",
                                    background: isSelected ? "#0b1724" : "rgba(8, 13, 24, .78)",
                                    color: colors.text,
                                    cursor: "pointer",
                                    whiteSpace: "nowrap",
                                    boxShadow: isSelected ? "0 0 0 3px rgba(112,225,232,.2)" : "none",
                                    fontSize: "10px",
                                    fontWeight: 700
                                }
                            },
                                h("span", {
                                    style: {
                                        width: "8px",
                                        height: "8px",
                                        borderRadius: "50%",
                                        background: site.avg_temp_c <= -60 ? "#70d6ff" : site.avg_temp_c <= -50 ? "#ffb05e" : "#ff654a",
                                        boxShadow: "0 0 10px currentColor"
                                    }
                                }),
                                site.short_name
                            );
                        }),
                        h("div", {
                            style: {
                                position: "absolute",
                                left: "12px",
                                bottom: "12px",
                                color: "rgba(255,255,255,.72)",
                                fontSize: "9px",
                                letterSpacing: "1.1px",
                                pointerEvents: "none"
                            }
                        }, "N  ↑")
                    ),
                    h("div", {
                        style: {
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            marginTop: "15px",
                            color: colors.muted,
                            fontSize: "10px"
                        }
                    },
                        h("span", null, "COLDER"),
                        h("span", {
                            style: {
                                flex: 1,
                                height: "7px",
                                borderRadius: "8px",
                                background: "linear-gradient(90deg, #54b9ed, #e1b45d, #ff654a)"
                            }
                        }),
                        h("span", null, "WARMER")
                    ),
                    // Landing site details card
                    h("div", {
                        style: {
                            marginTop: "18px",
                            padding: "16px",
                            border: "1px solid " + colors.border,
                            borderRadius: "6px",
                            background: "rgba(7, 11, 22, .65)",
                            display: "flex",
                            flexDirection: "column",
                            gap: "14px"
                        }
                    },
                        h("img", {
                            src: "/static/imgs/" + selectedSite.image,
                            alt: selectedSite.name,
                            style: {
                                width: "100%",
                                height: "400px",
                                objectFit: "cover",
                                borderRadius: "4px",
                                border: "1px solid " + colors.border,
                                background: "#070b16"
                            }
                        }),
                        h("div", {
                            style: {
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "flex-start",
                                flexWrap: "wrap",
                                gap: "10px"
                            }
                        },
                            h("div", { style: { flex: 1, minWidth: "200px" } },
                                h("div", { style: { color: colors.cyan, fontSize: "9px", letterSpacing: "1.3px", fontWeight: 800 } }, "SELECTED LANDING SITE"),
                                h("div", { style: { marginTop: "4px", fontSize: "16px", fontWeight: 800 } }, selectedSite.name),
                                h("div", { style: { marginTop: "3px", color: colors.muted, fontSize: "11px" } },
                                    "Latitude " + selectedSite.latitude_label +
                                    " · Solar Efficiency " + Math.round(selectedSite.solar_efficiency * 100) + "%" +
                                    " · Science Multiplier " + selectedSite.science_multiplier + "x"
                                )
                            ),
                            h("div", { style: { textAlign: "right" } },
                                h("div", { style: { color: colors.muted, fontSize: "9px", letterSpacing: "1px" } }, "AVG. SURFACE TEMP."),
                                h("div", { style: { marginTop: "2px", color: colors.orange, fontSize: "22px", fontWeight: 800 } }, selectedSite.avg_temp_c + "°C")
                            )
                        ),
                        h("p", {
                            style: {
                                margin: 0,
                                color: colors.muted,
                                fontSize: "12px",
                                lineHeight: 1.65,
                                borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                                paddingTop: "10px"
                            }
                        }, selectedSite.description)
                    )
                ),

                // Sidebar with Crew Size and Sticky Telemetry Preview
                h("aside", {
                    style: {
                        flex: "1 1 300px",
                        minWidth: "0",
                        position: "sticky",
                        top: "20px",
                        zIndex: 20,
                        display: "flex",
                        flexDirection: "column",
                        gap: "16px"
                    }
                },
                    h("section", {
                        style: {
                            padding: "20px",
                            border: "1px solid " + colors.border,
                            borderRadius: "8px",
                            background: colors.panel
                        }
                    },
                        h("div", { style: { fontSize: "11px", fontWeight: 800, letterSpacing: "1.3px" } }, "CREW SIZE"),
                        h("div", {
                            style: {
                                display: "flex",
                                alignItems: "baseline",
                                justifyContent: "space-between",
                                marginTop: "12px"
                            }
                        },
                            h("label", { htmlFor: "crew-size", style: { color: colors.muted, fontSize: "12px" } }, "Crew members"),
                            h("output", {
                                htmlFor: "crew-size",
                                style: { color: colors.cyan, fontSize: "26px", fontWeight: 800 }
                            }, String(crewSize))
                        ),
                        h("input", {
                            id: "crew-size",
                            type: "range",
                            min: 1,
                            max: 12,
                            step: 1,
                            value: crewSize,
                            onChange: function (event) { setCrewSize(Number(event.target.value)); },
                            "aria-label": "Number of crew members",
                            style: { width: "100%", margin: "12px 0", accentColor: colors.orange, cursor: "pointer" }
                        }),
                        h("div", {
                            style: { display: "flex", justifyContent: "space-between", color: colors.muted, fontSize: "10px" }
                        }, h("span", null, "1 PERSON"), h("span", null, "12 PEOPLE"))
                    ),

                    // Sticky Telemetry Preview Card
                    h("div", {
                        "aria-live": "polite",
                        style: {
                            padding: "18px",
                            borderLeft: "3px solid " + colors.orange,
                            borderTop: "1px solid " + colors.border,
                            borderRight: "1px solid " + colors.border,
                            borderBottom: "1px solid " + colors.border,
                            borderRadius: "8px",
                            background: "rgba(38, 22, 4, 0.94)",
                            backdropFilter: "blur(12px)",
                            boxShadow: "0 12px 35px rgba(0,0,0,0.6)",
                            color: colors.muted,
                            fontSize: "11px",
                            lineHeight: 1.75
                        }
                    },
                        h("strong", { style: { color: colors.text, letterSpacing: "0.8px" } }, "MISSION TELEMETRY PREVIEW"),
                        h("br"),
                        crewSize + (crewSize === 1 ? " crew member" : " crew members"),
                        h("br"),
                        selectedSite.short_name + " (" + selectedSite.avg_temp_c + "°C)",
                        h("br"),
                        "Rocket: " + selectedRocket.name,
                        h("br"),
                        "Mission Duration: ",
                        h("strong", { style: { color: colors.cyan } }, durationDays + " Sols"),
                        h("br"),
                        "Science Goal: ",
                        h("strong", { style: { color: colors.cyan } }, scienceGoal + " pts"),
                        h("br"),
                        "Sample Target Scale: ",
                        h("strong", { style: { color: colors.cyan } }, sampleTargetMult + "x"),
                        h("br"),
                        "Payload Mass: ",
                        h("strong", { style: { color: loadoutPreview.total_mass_kg > loadoutPreview.max_payload_mass_kg ? colors.red : colors.cyan } }, Number(loadoutPreview.total_mass_kg).toLocaleString() + " kg"),
                        " / " + Number(loadoutPreview.max_payload_mass_kg).toLocaleString() + " kg limit",
                        h("br"),
                        "Modules Mass: ",
                        h("strong", { style: { color: colors.text } }, Number(loadoutPreview.modules_mass_kg || 0).toLocaleString() + " kg"),
                        h("br"),
                        "Total Power Generation: ",
                        h("strong", { style: { color: colors.green } }, (loadoutPreview.total_power_kwe || 0).toFixed(1) + " kWe"),
                        h("br"),
                        "Module Power Net: ",
                        h("strong", { style: { color: loadoutPreview.net_module_power_kwe >= 0 ? colors.green : colors.orange } },
                            (loadoutPreview.net_module_power_kwe >= 0 ? "+" : "") + loadoutPreview.net_module_power_kwe.toFixed(1) + " kWe"
                        ),
                        " (Base: " + loadoutPreview.base_habitat_power_kwe + " kWe)",
                        h("div", {
                            style: {
                                marginTop: "10px",
                                borderTop: "1px solid rgba(255,255,255,0.1)",
                                paddingTop: "8px",
                                fontSize: "10px"
                            }
                        },
                            h("strong", { style: { color: colors.cyan } }, "Mission Total Consumables:"),
                            h("br"),
                            "• Total O₂: " + Number(loadoutPreview.total_o2_kg || 0).toLocaleString() + " kg",
                            h("br"),
                            "• Total Water: " + Number(loadoutPreview.total_water_l || 0).toLocaleString() + " L",
                            h("br"),
                            "• Total Food: " + Number(loadoutPreview.total_food_kg || 0).toLocaleString() + " kg",
                            h("br"),
                            "• Total CO₂ Produced: " + Number(loadoutPreview.total_co2_l || 0).toLocaleString() + " L"
                        ),
                        h("div", {
                            style: {
                                marginTop: "8px",
                                borderTop: "1px solid rgba(255,255,255,0.1)",
                                paddingTop: "6px",
                                fontSize: "10px"
                            }
                        },
                            h("strong", { style: { color: colors.cyan } }, "NASA-STD-3001 Baselines:"),
                            h("br"),
                            "• O₂/person/day: " + NASA_CONSTANTS.O2_KG_PER_PERSON_DAY + " kg",
                            h("br"),
                            "• Water/person/day: " + NASA_CONSTANTS.WATER_L_PER_PERSON_DAY + " L",
                            h("br"),
                            "• Food/person/day: " + NASA_CONSTANTS.FOOD_KG_PER_PERSON_DAY + " kg",
                            h("br"),
                            "• Surface Radiation: " + (NASA_CONSTANTS.BASE_MARS_RADIATION_MSV_DAY * (1.0 - selectedSite.natural_radiation_shielding)).toFixed(2) + " mSv/day"
                        )
                    )
                )
            ),

            // Mission Parameters & Goals Section
            h("section", {
                style: {
                    marginTop: "24px",
                    padding: "22px",
                    border: "1px solid " + colors.border,
                    borderRadius: "8px",
                    background: colors.panel
                }
            },
                h("div", { style: { color: colors.orange, fontSize: "10px", fontWeight: 800, letterSpacing: "1.5px" } }, "MISSION PARAMETERS & OBJECTIVES"),
                h("h2", { style: { margin: "4px 0 16px", fontSize: "18px", fontWeight: 800 } }, "Configure Mission Goals & Duration"),
                h("div", {
                    style: {
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
                        gap: "20px"
                    }
                },
                    // Duration Slider
                    h("div", { style: { padding: "14px", border: "1px solid " + colors.border, borderRadius: "6px", background: "rgba(7, 11, 22, 0.5)" } },
                        h("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center" } },
                            h("span", { style: { fontSize: "12px", fontWeight: 700 } }, "Mission Duration (Sols)"),
                            h("span", { style: { color: colors.cyan, fontSize: "16px", fontWeight: 800 } }, durationDays)
                        ),
                        h("input", {
                            type: "range",
                            min: 100,
                            max: 1000,
                            step: 25,
                            value: durationDays,
                            onChange: function (e) { setDurationDays(Number(e.target.value)); },
                            style: { width: "100%", margin: "10px 0", accentColor: colors.orange, cursor: "pointer" }
                        }),
                        h("div", { style: { display: "flex", justifyContent: "space-between", color: colors.muted, fontSize: "10px" } }, h("span", null, "100 Sols"), h("span", null, "1000 Sols"))
                    ),
                    // Science Goal Slider
                    h("div", { style: { padding: "14px", border: "1px solid " + colors.border, borderRadius: "6px", background: "rgba(7, 11, 22, 0.5)" } },
                        h("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center" } },
                            h("span", { style: { fontSize: "12px", fontWeight: 700 } }, "Science Points Goal"),
                            h("span", { style: { color: colors.cyan, fontSize: "16px", fontWeight: 800 } }, scienceGoal + " pts")
                        ),
                        h("input", {
                            type: "range",
                            min: 100,
                            max: 2000,
                            step: 50,
                            value: scienceGoal,
                            onChange: function (e) { setScienceGoal(Number(e.target.value)); },
                            style: { width: "100%", margin: "10px 0", accentColor: colors.orange, cursor: "pointer" }
                        }),
                        h("div", { style: { display: "flex", justifyContent: "space-between", color: colors.muted, fontSize: "10px" } }, h("span", null, "100 pts"), h("span", null, "2000 pts"))
                    ),
                    // Rock Sample Target Multiplier
                    h("div", { style: { padding: "14px", border: "1px solid " + colors.border, borderRadius: "6px", background: "rgba(7, 11, 22, 0.5)" } },
                        h("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center" } },
                            h("span", { style: { fontSize: "12px", fontWeight: 700 } }, "Rock Sample Target Scale"),
                            h("span", { style: { color: colors.cyan, fontSize: "16px", fontWeight: 800 } }, sampleTargetMult + "x")
                        ),
                        h("input", {
                            type: "range",
                            min: 0.5,
                            max: 2.0,
                            step: 0.25,
                            value: sampleTargetMult,
                            onChange: function (e) { setSampleTargetMult(Number(e.target.value)); },
                            style: { width: "100%", margin: "10px 0", accentColor: colors.orange, cursor: "pointer" }
                        }),
                        h("div", { style: { display: "flex", justifyContent: "space-between", color: colors.muted, fontSize: "10px" } }, h("span", null, "0.5x (Easier)"), h("span", null, "2.0x (Hardcore)"))
                    )
                )
            ),

            // Rocket Architecture Selection Section
            h("section", {
                style: {
                    marginTop: "24px",
                    padding: "22px",
                    border: "1px solid " + colors.border,
                    borderRadius: "8px",
                    background: colors.panel
                }
            },
                h("div", {
                    style: {
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        flexWrap: "wrap",
                        gap: "8px",
                        marginBottom: "16px"
                    }
                },
                    h("div", null,
                        h("div", { style: { color: colors.cyan, fontSize: "10px", fontWeight: 800, letterSpacing: "1.5px" } }, "LAUNCH VEHICLE // MARS DRA 5.0"),
                        h("h2", { style: { margin: "4px 0 0", fontSize: "18px", fontWeight: 800 } }, "Rocket Architecture & Propellant Type")
                    ),
                    h("span", { style: { color: colors.muted, fontSize: "11px" } },
                        "Surface Payload Limit: " + Number(selectedRocket.surface_payload_limit_kg).toLocaleString() + " kg"
                    )
                ),
                h("div", {
                    style: {
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
                        gap: "16px"
                    }
                },
                    Object.entries(ROCKET_ARCHITECTURES).map(function (entry) {
                        const key = entry[0];
                        const rocket = entry[1];
                        const isSelected = key === rocketId;
                        const imleoTons = (rocket.imleo_mass_kg / 1000).toFixed(1);

                        return h("button", {
                            key: key,
                            type: "button",
                            onClick: function () { setRocketId(key); },
                            "aria-pressed": isSelected,
                            style: {
                                padding: "18px",
                                textAlign: "left",
                                border: "1px solid " + (isSelected ? colors.cyan : colors.border),
                                borderRadius: "6px",
                                background: isSelected ? "rgba(112, 225, 232, 0.08)" : "rgba(7, 11, 22, 0.5)",
                                color: colors.text,
                                cursor: "pointer",
                                display: "flex",
                                flexDirection: "column",
                                gap: "10px",
                                boxShadow: isSelected ? "0 0 0 2px rgba(112,225,232,0.15)" : "none"
                            }
                        },
                            h("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: "8px" } },
                                h("span", { style: { fontSize: "14px", fontWeight: 800, color: isSelected ? colors.cyan : colors.text } }, rocket.name),
                                h("span", { style: { fontSize: "15px", color: isSelected ? colors.cyan : colors.muted } }, isSelected ? "●" : "○")
                            ),
                            h("div", { style: { fontSize: "11px", color: colors.orange, fontWeight: 700 } }, "Propellant: " + rocket.fuel_type),
                            h("div", {
                                style: {
                                    display: "flex",
                                    flexWrap: "wrap",
                                    gap: "8px",
                                    fontSize: "10px",
                                    fontWeight: 700
                                }
                            },
                                h("span", { style: { padding: "3px 8px", borderRadius: "4px", background: "rgba(255,255,255,0.06)", color: colors.text } }, rocket.isp_seconds + "s Isp"),
                                h("span", { style: { padding: "3px 8px", borderRadius: "4px", background: "rgba(255,255,255,0.06)", color: colors.text } }, imleoTons + " t IMLEO"),
                                h("span", { style: { padding: "3px 8px", borderRadius: "4px", background: "rgba(255,255,255,0.06)", color: colors.muted } }, rocket.budget_cost_multiplier + "x Budget")
                            ),
                            h("div", { style: { fontSize: "11px", lineHeight: 1.55, color: colors.muted } },
                                h("strong", { style: { color: colors.green } }, "+ Benefits: "),
                                rocket.pros
                            ),
                            h("div", { style: { fontSize: "11px", lineHeight: 1.55, color: colors.muted } },
                                h("strong", { style: { color: colors.red } }, "− Drawbacks: "),
                                rocket.cons
                            )
                        );
                    })
                )
            ),

            // Surface Modules Selection Section
            h("section", {
                style: {
                    marginTop: "24px",
                    padding: "22px",
                    border: "1px solid " + colors.border,
                    borderRadius: "8px",
                    background: colors.panel
                }
            },
                h("div", {
                    style: {
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        flexWrap: "wrap",
                        gap: "8px",
                        marginBottom: "16px"
                    }
                },
                    h("div", null,
                        h("div", { style: { color: colors.orange, fontSize: "10px", fontWeight: 800, letterSpacing: "1.5px" } }, "CARGO MANIFEST // OPTIONAL MODULES"),
                        h("h2", { style: { margin: "4px 0 0", fontSize: "18px", fontWeight: 800 } }, "Colony Modules & Trade-offs")
                    ),
                    h("span", { style: { color: colors.muted, fontSize: "11px" } },
                        "Selected Modules Mass: " + Number(loadoutPreview.modules_mass_kg).toLocaleString() +
                        " kg (+ " + Number(baseSuppliesMassKg).toLocaleString() + " kg base supplies)"
                    )
                ),
                h("div", {
                    style: {
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
                        gap: "16px"
                    }
                },
                    Object.entries(MODULES).map(function (entry) {
                        const key = entry[0];
                        const mod = entry[1];
                        const isActive = activeModules.includes(key);
                        const powerLabel = (mod.is_generator ? "+" : "-") + mod.power_kwe.toFixed(1) + " kWe " + (mod.is_generator ? "Output" : "Demand");

                        return h("button", {
                            key: key,
                            type: "button",
                            onClick: function () { toggleModule(key); },
                            "aria-pressed": isActive,
                            style: {
                                padding: "16px",
                                textAlign: "left",
                                border: "1px solid " + (isActive ? colors.cyan : colors.border),
                                borderRadius: "6px",
                                background: isActive ? "rgba(112, 225, 232, 0.08)" : "rgba(7, 11, 22, 0.5)",
                                color: colors.text,
                                cursor: "pointer",
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-between",
                                gap: "10px"
                            }
                        },
                            h("div", { style: { display: "flex", gap: "12px", alignItems: "center" } },
                                h("img", {
                                    src: "static/imgs/" + mod.image,
                                    alt: mod.name,
                                    style: {
                                        width: "52px",
                                        height: "52px",
                                        objectFit: "cover",
                                        borderRadius: "6px",
                                        border: "1px solid " + colors.border,
                                        background: "#070b16"
                                    }
                                }),
                                h("div", { style: { flex: 1, minWidth: 0 } },
                                    h("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "8px" } },
                                        h("span", { style: { fontSize: "13px", fontWeight: 800, color: isActive ? colors.cyan : colors.text } }, mod.name),
                                        h("span", {
                                            style: {
                                                padding: "2px 7px",
                                                borderRadius: "4px",
                                                fontSize: "9px",
                                                fontWeight: 800,
                                                background: isActive ? colors.cyan : "rgba(255,255,255,0.08)",
                                                color: isActive ? "#070b16" : colors.muted
                                            }
                                        }, isActive ? "EQUIPPED" : "ADD")
                                    ),
                                    h("div", {
                                        style: {
                                            display: "flex",
                                            gap: "8px",
                                            marginTop: "4px",
                                            fontSize: "10px",
                                            fontWeight: 700
                                        }
                                    },
                                        h("span", { style: { color: colors.muted } }, Number(mod.mass_kg).toLocaleString() + " kg"),
                                        h("span", { style: { color: colors.muted } }, "·"),
                                        h("span", { style: { color: mod.is_generator ? colors.green : colors.orange } }, powerLabel)
                                    )
                                )
                            ),
                            h("div", { style: { fontSize: "11px", lineHeight: 1.5, color: colors.muted, borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: "8px" } },
                                h("p", { style: { margin: "0 0 4px 0" } },
                                    h("strong", { style: { color: colors.green } }, "+ Benefit: "),
                                    mod.pros
                                ),
                                h("p", { style: { margin: 0 } },
                                    h("strong", { style: { color: colors.red } }, "− Drawback: "),
                                    mod.cons
                                ),
                                mod.notes ? h("p", { style: { marginTop: "10px" } },
                                    h("strong", { style: { color: colors.gray } }, "− Notes: "),
                                    mod.notes
                                ) : null
                            )
                        );
                    })
                )
            ),

            // Bottom section featuring the launch rocket image and "3... 2... 1... LAUNCH!" button
            h("div", {
                style: {
                    marginTop: "32px",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: "14px",
                    padding: "24px",
                    border: "1px solid " + colors.cyan,
                    borderRadius: "8px",
                    background: "rgba(112, 225, 232, 0.04)"
                }
            },
                h("img", {
                    src: "/static/imgs/ares_v_lancamento.png",
                    alt: "Ares V Rocket Launch Pixel Art",
                    style: {
                        width: "110px",
                        height: "auto",
                        objectFit: "contain",
                        filter: "drop-shadow(0 10px 20px rgba(255, 118, 74, 0.35))"
                    }
                }),
                h("div", { style: { fontSize: "12px", color: colors.cyan, fontWeight: 700, letterSpacing: "1px", textAlign: "center" } },
                    "READY FOR LIFTOFF? REVIEW YOUR TELEMETRY AND INITIATE LAUNCH"
                ),
                h("a", {
                    href: gameUrl,
                    "aria-label": "Initiate Mars rocket launch",
                    style: {
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: "12px",
                        minHeight: "56px",
                        width: "min(400px, 100%)",
                        borderRadius: "6px",
                        background: colors.orange,
                        color: "#160c0a",
                        fontSize: "13px",
                        fontWeight: 900,
                        letterSpacing: "1.3px",
                        textDecoration: "none",
                        boxShadow: "0 10px 30px rgba(255, 118, 74, .25)"
                    }
                }, "3... 2... 1... LAUNCH!", h("span", { "aria-hidden": "true", style: { fontSize: "18px" } }, "→"))
            )
        );
    }

    return h("main", { style: page },
        h("header", {
            style: Object.assign({}, container, {
                minHeight: "88px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "24px",
                borderBottom: "1px solid " + colors.border
            })
        },
            h("a", {
                href: "/",
                style: {
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    color: colors.text,
                    textDecoration: "none"
                }
            },
                h("span", {
                    style: {
                        width: "38px",
                        height: "38px",
                        display: "grid",
                        placeItems: "center",
                        border: "1px solid rgba(112, 225, 232, .6)",
                        borderRadius: "50%",
                        color: colors.cyan,
                        fontSize: "19px"
                    }
                }, "✦"),
                h("span", { style: { fontSize: "12px", lineHeight: 1.35, letterSpacing: "1.5px", fontWeight: 800 } },
                    "NASA SPACE APPS",
                    h("br"),
                    h("span", { style: { color: colors.muted, fontSize: "10px", fontWeight: 500 } }, "MARS CHALLENGE")
                )
            ),
            h("div", {
                style: {
                    color: colors.cyan,
                    fontSize: "11px",
                    fontWeight: 700,
                    letterSpacing: "1.8px",
                    textAlign: "right"
                }
            }, "MISSION CONTROL", h("br"), h("span", {
                style: { color: colors.muted, fontWeight: 500, letterSpacing: "1px" }
            }, "MISSION MARS // 2045"))
        ),

        screen === "landing" ? h(React.Fragment, null,
            h("section", {
                style: Object.assign({}, container, {
                    minHeight: "590px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "32px",
                    paddingTop: "54px",
                    paddingBottom: "54px",
                    boxSizing: "border-box",
                    flexWrap: "wrap"
                })
            },
                h("div", { style: { flex: "1 1 440px", maxWidth: "570px", zIndex: 1 } },
                    h("div", {
                        style: {
                            display: "inline-flex",
                            alignItems: "center",
                            gap: "9px",
                            padding: "8px 12px",
                            border: "1px solid rgba(112, 225, 232, .28)",
                            borderRadius: "4px",
                            background: "rgba(112, 225, 232, .06)",
                            color: colors.cyan,
                            fontSize: "10px",
                            letterSpacing: "1.7px",
                            fontWeight: 800
                        }
                    }, h("span", { style: { color: colors.orange } }, "●"), " MISSION SIMULATION // MARS"),
                    h("h1", {
                        style: {
                            margin: "25px 0 18px",
                            fontSize: "clamp(42px, 7vw, 76px)",
                            lineHeight: 0.99,
                            letterSpacing: "-3.5px",
                            fontWeight: 850
                        }
                    }, "Humanity's", h("br"), h("span", { style: { color: colors.orange } }, "future"), h("br"), "is red."),
                    h("p", {
                        style: {
                            maxWidth: "490px",
                            margin: "0 0 30px",
                            color: colors.muted,
                            fontSize: "16px",
                            lineHeight: 1.8
                        }
                    }, "A mission to Mars depends on making the right choices. Plan your colony, manage resources, and find out if your crew can survive on the Red Planet."),
                    h("div", {
                        style: {
                            display: "flex",
                            alignItems: "center",
                            flexWrap: "wrap",
                            gap: "16px"
                        }
                    },
                        h("a", {
                            href: "#planner",
                            onClick: function (event) {
                                event.preventDefault();
                                setScreen("planner");
                                window.scrollTo({ top: 0, behavior: "smooth" });
                            },
                            style: {
                                display: "inline-flex",
                                alignItems: "center",
                                justifyContent: "center",
                                gap: "13px",
                                minHeight: "54px",
                                padding: "0 23px",
                                borderRadius: "4px",
                                background: colors.orange,
                                color: "#160c0a",
                                fontSize: "12px",
                                fontWeight: 900,
                                letterSpacing: "1.2px",
                                textDecoration: "none",
                                boxShadow: "0 10px 35px rgba(255, 118, 74, .2)"
                            }
                        }, "Start planning", h("span", { "aria-hidden": "true", style: { fontSize: "18px" } }, "→")),
                        h("span", { style: { color: colors.muted, fontSize: "11px", letterSpacing: ".5px" } }, "GET READY FOR LIFTOFF")
                    )
                ),
                h("div", {
                    style: {
                        flex: "1 1 340px",
                        minWidth: "0",
                        display: "flex",
                        justifyContent: "center",
                        position: "relative"
                    }
                },
                    h("div", {
                        style: {
                            position: "absolute",
                            width: "min(420px, 90vw)",
                            aspectRatio: "1",
                            border: "1px solid rgba(112, 225, 232, .14)",
                            borderRadius: "50%",
                            boxShadow: "0 0 0 35px rgba(112, 225, 232, .025), 0 0 0 75px rgba(112, 225, 232, .02)"
                        }
                    }),
                    h("img", {
                        src: "/static/imgs/astronaut_front.png",
                        alt: "An astronaut in a spacesuit, standing on the surface of Mars, with the planet's red landscape and a distant horizon in the background.",
                        style: {
                            position: "relative",
                            display: "block",
                            width: "min(100%, 430px)",
                            height: "auto",
                            objectFit: "contain",
                            filter: "drop-shadow(0 22px 50px rgba(0, 0, 0, .45))"
                        }
                    }),
                    h("div", {
                        style: {
                            position: "absolute",
                            right: "0",
                            bottom: "8%",
                            padding: "13px 17px",
                            border: "1px solid " + colors.border,
                            borderRadius: "4px",
                            background: colors.panel,
                            backdropFilter: "blur(10px)"
                        }
                    },
                        h("div", { style: { color: colors.cyan, fontSize: "9px", letterSpacing: "1.6px", fontWeight: 800 } }, "DESTINATION"),
                        h("div", { style: { marginTop: "5px", fontSize: "14px", fontWeight: 700 } }, "MARS · 225 MILLION KM")
                    )
                )
            ),

            h("section", { style: Object.assign({}, container, { paddingBottom: "58px" }) },
                h("div", {
                    style: {
                        display: "flex",
                        flexWrap: "wrap",
                        border: "1px solid " + colors.border,
                        borderRadius: "6px",
                        background: "rgba(15, 23, 40, .72)"
                    }
                }, highlights.map(function (item, index) {
                    return h("div", {
                        key: item.number,
                        style: {
                            flex: "1 1 210px",
                            display: "flex",
                            gap: "15px",
                            alignItems: "flex-start",
                            padding: "22px",
                            boxSizing: "border-box",
                            borderRight: index < highlights.length - 1 ? "1px solid " + colors.border : "none"
                        }
                    },
                        h("span", { style: { color: colors.orange, fontSize: "12px", fontWeight: 800 } }, item.number),
                        h("div", null,
                            h("div", { style: { fontSize: "10px", letterSpacing: "1.3px", fontWeight: 800 } }, item.label),
                            h("div", { style: { marginTop: "7px", color: colors.muted, fontSize: "12px" } }, item.detail)
                        )
                    );
                }))
            )
        ) : plannerContent(),

        h("footer", {
            style: Object.assign({}, container, {
                padding: "18px 0 25px",
                borderTop: "1px solid " + colors.border,
                color: colors.muted,
                fontSize: "10px",
                letterSpacing: ".7px",
                display: "flex",
                justifyContent: "space-between",
                flexWrap: "wrap",
                gap: "10px"
            })
        },
            h("span", null, "NASA SPACE APPS CHALLENGE · MARS MISSION"),
            h("span", null, "ONE SMALL STEP TOWARD YOUR NEXT GREAT MISSION")
        )
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(h(App));