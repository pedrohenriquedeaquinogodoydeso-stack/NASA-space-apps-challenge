/*
  Mars Mission - Mission sidebar
  Fixed side panel with the mission configuration. Used by planning.html (live
  preview while the player configures the mission) and game.html (read-only
  reminder of the launch setup while the player is playing).

  Requires React and common.js (for `h` and `colors`).

  Usage:
      h(MissionSidebar, { data: {...}, title: "MISSION TELEMETRY", subtitle: "...", live: true })

  data = {
      crewSize, siteName, siteTempC, rocketName,
      durationDays, scienceGoal, sampleTargetMult,
      loadout,            // dict returned by MissionLoadout.to_dict()
      activeModules,      // [{ id, name }]
      baselines,          // { o2, water, food } per person per day
      radiationMsvDay
  }
*/

const SIDEBAR_WIDTH = 320;
const SIDEBAR_WIDE_BREAKPOINT = 1100;   // below this the sidebar overlays the page instead of pushing it
const SIDEBAR_STORAGE_KEY = "marsMissionSidebarOpen";

function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function initialSidebarOpen() {
    if (window.innerWidth < SIDEBAR_WIDE_BREAKPOINT) {
        return false;
    }
    try {
        return window.localStorage.getItem(SIDEBAR_STORAGE_KEY) !== "0";
    } catch (error) {
        return true;
    }
}

function formatNumber(value) {
    return Number(value || 0).toLocaleString();
}

function SidebarRow(props) {
    return h("div", {
        style: {
            display: "flex",
            justifyContent: "space-between",
            alignItems: "baseline",
            gap: "12px",
            padding: "4px 0",
            fontSize: "12px",
            lineHeight: 1.5
        }
    },
        h("span", { style: { color: colors.muted } }, props.label),
        h("strong", { style: { color: props.color || colors.text, textAlign: "right" } }, props.value)
    );
}

function SidebarSection(props) {
    return h("section", {
        style: {
            padding: "14px 0",
            borderTop: "1px solid rgba(255, 255, 255, 0.08)"
        }
    },
        h("div", {
            style: {
                marginBottom: "6px",
                color: colors.cyan,
                fontSize: "10px",
                fontWeight: 800,
                letterSpacing: "1.4px"
            }
        }, props.title),
        props.children
    );
}

function MissionSidebar(props) {
    const d = props.data;
    const lo = d.loadout;

    const [open, setOpen] = React.useState(initialSidebarOpen);
    const [wide, setWide] = React.useState(window.innerWidth >= SIDEBAR_WIDE_BREAKPOINT);

    React.useEffect(function () {
        function onResize() { setWide(window.innerWidth >= SIDEBAR_WIDE_BREAKPOINT); }
        window.addEventListener("resize", onResize);
        return function () { window.removeEventListener("resize", onResize); };
    }, []);

    // On wide screens the page makes room for the sidebar; on narrow screens it overlays the page.
    React.useEffect(function () {
        document.body.style.transition = prefersReducedMotion() ? "none" : "padding-right .25s ease";
        document.body.style.paddingRight = open && wide ? SIDEBAR_WIDTH + "px" : "0px";
    }, [open, wide]);

    React.useEffect(function () {
        return function () { document.body.style.paddingRight = "0px"; };
    }, []);

    function toggle() {
        const next = !open;
        setOpen(next);
        if (wide) {
            try { window.localStorage.setItem(SIDEBAR_STORAGE_KEY, next ? "1" : "0"); } catch (error) {}
        }
    }

    const totalMass = Number(lo.total_mass_kg || 0);
    const maxPayload = Number(lo.max_payload_mass_kg || 0);
    const overLimit = maxPayload > 0 && totalMass > maxPayload;
    const massPercent = maxPayload > 0 ? Math.min(100, (totalMass / maxPayload) * 100) : 0;
    const netPower = Number(lo.net_module_power_kwe || 0);
    const animate = !prefersReducedMotion();

    return h("aside", {
        id: "mission-sidebar",
        "aria-label": "Mission telemetry",
        style: {
            position: "fixed",
            top: 0,
            right: 0,
            bottom: 0,
            zIndex: 9,
            width: "min(" + SIDEBAR_WIDTH + "px, 88vw)",
            boxSizing: "border-box",
            borderLeft: "1px solid " + colors.border,
            background: "rgba(30, 17, 3, 0.98)",
            boxShadow: open ? "-12px 0 35px rgba(0, 0, 0, 0.45)" : "none",
            color: colors.text,
            fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            transform: open ? "translateX(0)" : "translateX(100%)",
            visibility: open ? "visible" : "hidden",
            transition: !animate ? "none" : (open ? "transform .25s ease" : "transform .25s ease, visibility 0s linear .25s")
        }
    },
        // Tab attached to the sidebar edge: always reachable, even when the panel is collapsed
        h("button", {
            type: "button",
            onClick: toggle,
            "aria-expanded": open,
            "aria-controls": "mission-sidebar-content",
            "aria-label": open ? "Hide mission telemetry" : "Show mission telemetry",
            style: {
                position: "absolute",
                top: "96px",
                right: "100%",
                visibility: "visible",
                width: "30px",
                padding: "14px 0",
                border: "1px solid " + colors.border,
                borderRight: "none",
                borderRadius: "8px 0 0 8px",
                background: "rgba(30, 17, 3, 0.98)",
                color: colors.cyan,
                cursor: "pointer",
                fontSize: "10px",
                fontWeight: 800,
                letterSpacing: "1.6px",
                writingMode: "vertical-rl"
            }
        }, open ? "HIDE PANEL" : "MISSION TELEMETRY"),

        h("div", {
            id: "mission-sidebar-content",
            "aria-live": props.live ? "polite" : "off",
            style: {
                height: "100%",
                boxSizing: "border-box",
                overflowY: "auto",
                padding: "22px 20px 32px"
            }
        },
            h("div", { style: { display: "flex", alignItems: "center", gap: "8px" } },
                h("span", { "aria-hidden": "true", style: { color: colors.orange, fontSize: "10px" } }, "●"),
                h("strong", { style: { fontSize: "12px", letterSpacing: "1.4px" } }, props.title || "MISSION TELEMETRY")
            ),
            props.subtitle
                ? h("p", { style: { margin: "6px 0 14px", color: colors.muted, fontSize: "11px", lineHeight: 1.6 } }, props.subtitle)
                : null,

            h(SidebarSection, { title: "MISSION" },
                h(SidebarRow, { label: "Crew", value: d.crewSize + (d.crewSize === 1 ? " member" : " members") }),
                h(SidebarRow, { label: "Landing site", value: d.siteName }),
                h(SidebarRow, { label: "Avg. temperature", value: d.siteTempC + "°C" }),
                h(SidebarRow, { label: "Rocket", value: d.rocketName }),
                h(SidebarRow, { label: "Duration", value: d.durationDays + " Sols", color: colors.cyan }),
                h(SidebarRow, { label: "Science goal", value: d.scienceGoal + " pts", color: colors.cyan }),
                h(SidebarRow, { label: "Sample target scale", value: d.sampleTargetMult + "x", color: colors.cyan })
            ),

            h(SidebarSection, { title: "PAYLOAD" },
                h(SidebarRow, {
                    label: "Total mass",
                    value: formatNumber(totalMass) + " / " + formatNumber(maxPayload) + " kg",
                    color: overLimit ? colors.red : colors.cyan
                }),
                h("div", {
                    role: "progressbar",
                    "aria-label": "Payload mass used",
                    "aria-valuemin": 0,
                    "aria-valuemax": 100,
                    "aria-valuenow": Math.round(massPercent),
                    style: { height: "6px", margin: "4px 0 6px", borderRadius: "4px", background: "rgba(255, 255, 255, 0.08)", overflow: "hidden" }
                },
                    h("div", {
                        style: {
                            width: massPercent + "%",
                            height: "100%",
                            borderRadius: "4px",
                            background: overLimit ? colors.red : colors.green,
                            transition: animate ? "width .3s ease" : "none"
                        }
                    })
                ),
                overLimit
                    ? h("div", { style: { margin: "2px 0 4px", color: colors.red, fontSize: "11px", fontWeight: 700 } },
                        "Over the payload limit by " + formatNumber(totalMass - maxPayload) + " kg")
                    : null,
                h(SidebarRow, { label: "Modules mass", value: formatNumber(lo.modules_mass_kg) + " kg" })
            ),

            h(SidebarSection, { title: "POWER" },
                h(SidebarRow, { label: "Total generation", value: Number(lo.total_power_kwe || 0).toFixed(1) + " kWe", color: colors.green }),
                h(SidebarRow, {
                    label: "Module net",
                    value: (netPower >= 0 ? "+" : "") + netPower.toFixed(1) + " kWe",
                    color: netPower >= 0 ? colors.green : colors.orange
                }),
                h(SidebarRow, { label: "Base habitat", value: lo.base_habitat_power_kwe + " kWe" })
            ),

            h(SidebarSection, { title: "ACTIVE MODULES" },
                d.activeModules.length === 0
                    ? h("div", { style: { color: colors.muted, fontSize: "12px" } }, "No optional modules")
                    : h("div", { style: { display: "flex", flexWrap: "wrap", gap: "6px" } },
                        d.activeModules.map(function (mod) {
                            return h("span", {
                                key: mod.id,
                                style: {
                                    padding: "4px 9px",
                                    border: "1px solid rgba(86, 227, 159, 0.4)",
                                    borderRadius: "4px",
                                    color: colors.green,
                                    fontSize: "11px",
                                    fontWeight: 700
                                }
                            }, mod.name);
                        })
                    )
            ),

            h(SidebarSection, { title: "MISSION TOTAL CONSUMABLES" },
                h(SidebarRow, { label: "Oxygen (O₂)", value: formatNumber(lo.total_o2_kg) + " kg" }),
                h(SidebarRow, { label: "Water", value: formatNumber(lo.total_water_l) + " L" }),
                h(SidebarRow, { label: "Food", value: formatNumber(lo.total_food_kg) + " kg" }),
                h(SidebarRow, { label: "CO₂ produced", value: formatNumber(lo.total_co2_l) + " L" })
            ),

            h(SidebarSection, { title: "NASA-STD-3001 BASELINES" },
                h(SidebarRow, { label: "O₂ / person / day", value: d.baselines.o2 + " kg" }),
                h(SidebarRow, { label: "Water / person / day", value: d.baselines.water + " L" }),
                h(SidebarRow, { label: "Food / person / day", value: d.baselines.food + " kg" }),
                h(SidebarRow, { label: "Surface radiation", value: Number(d.radiationMsvDay).toFixed(2) + " mSv/day" })
            )
        )
    );
}