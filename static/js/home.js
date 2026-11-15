/*
  Humanity’s Future Is Red - Home page (index.html)
  Presents the project and links to the planning page.

  Parts of this file were written with AI assistance (Gemini, Claude)
*/

const highlights = [
    { number: "01", label: "CHOOSE A LANDING SITE", detail: "Jezero, Arcadia, and more" },
    { number: "02", label: "BUILD YOUR MISSION", detail: "Propulsion, modules, and crew" },
    { number: "03", label: "SURVIVE ON MARS", detail: "Every choice shapes the outcome" }
];

const aboutCards = [
    {
        title: "REAL NASA NUMBERS",
        text: "Oxygen, water and food needs per astronaut are based on NASA reference values, so your crew consumes what a real crew would."
    },
    {
        title: "PICK YOUR HARDWARE",
        text: "Choose a rocket architecture and decide which modules fit in the payload: solar array, water recycler, greenhouse or MOXIE oxygen production."
    },
    {
        title: "EVERY SITE IS DIFFERENT",
        text: "Each landing site has its own temperature, solar efficiency and natural radiation shielding. The best science is not always the safest place."
    },
    {
        title: "DECISIONS UNDER PRESSURE",
        text: "Once on Mars, you face situations that demand a yes or no. Your habitat integrity and solar power decide how well you survive them."
    }
];

function Home() {
    return h("main", { style: page },
        h(SiteHeader),

        h(React.Fragment, null,
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
                            href: "/planning",
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
        ),

        // About the project
        h("section", { style: Object.assign({}, container, { paddingBottom: "70px" }) },
            h("div", { style: { color: colors.cyan, fontSize: "10px", letterSpacing: "1.7px", fontWeight: 800 } }, "ABOUT THE PROJECT"),
            h("h2", {
                style: { margin: "14px 0 14px", fontSize: "clamp(28px, 4vw, 40px)", lineHeight: 1.1, letterSpacing: "-1.5px", fontWeight: 850 }
            }, "Plan it. Launch it. Survive it."),
            h("p", {
                style: { maxWidth: "680px", margin: "0 0 32px", color: colors.muted, fontSize: "15px", lineHeight: 1.8 }
            }, "Humanity’s Future Is Red is an interactive simulation created for the NASA Space Apps Challenge. First you design a crewed mission to Mars on the planning screen. Then you take command of it, managing resources and facing the unexpected."),
            h("div", { style: { display: "flex", flexWrap: "wrap", gap: "16px" } },
                aboutCards.map(function (card) {
                    return h("div", {
                        key: card.title,
                        style: {
                            flex: "1 1 240px",
                            padding: "22px",
                            boxSizing: "border-box",
                            border: "1px solid " + colors.border,
                            borderRadius: "6px",
                            background: colors.panel
                        }
                    },
                        h("div", { style: { color: colors.orange, fontSize: "10px", letterSpacing: "1.4px", fontWeight: 800 } }, card.title),
                        h("p", { style: { margin: "10px 0 0", color: colors.muted, fontSize: "13px", lineHeight: 1.7 } }, card.text)
                    );
                })
            ),
            h("div", { style: { fontSize: "20px",marginTop: "50px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", } }, 
                h("h1", { style: { fontWeight: 800, letterSpacing: "1.5px", color: colors.orange, fontSize: "20px"} }, "Everyone knows that planning missions is decisive, but it can involve many difficult choices in order to reduce damage and needs. Analyze the important variables."),
            ), 
            h("div", { style: { marginTop: "36px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "20px" } },
                h("img", { src: "/static/imgs/oxygen.png", alt: "Oxygen", style: { width: "100px", height: "100px", objectFit: "contain", flex: "0 0 100px" } }),
                h("h1", { style: { flex: "1 1 280px", margin: 0, fontWeight: 800, letterSpacing: "1.5px", fontSize: "15px"} }, "Oxygen: It is essential for the Cellular respiration and the maintenance of life, being used in aerobic respiration of animals, plants, and most living organisms. On a space mission, it becomes one of the first points that must be observed. Average per crew member:"),
            ),
            h("div", { style: { marginTop: "36px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "20px" } },
                h("img", { src: "/static/imgs/waternfood.png", alt: "Water and Food", style: { width: "100px", height: "100px", objectFit: "contain", flex: "0 0 100px" } }),
                h("h1", { style: { flex: "1 1 280px", margin: 0, fontWeight: 800, letterSpacing: "1.5px", fontSize: "15px"} }, "Water and Food: Is crucial for the survival of the crew, and it is necessary to plan the amount of water and food that will be needed for the entire mission. Average per crew member: "),
            ),
            h("div", { style: { marginTop: "36px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "20px" } },
                h("img", { src: "/static/imgs/temperature.png", alt: "Temperature", style: { width: "100px", height: "100px", objectFit: "contain", flex: "0 0 100px" } }),
                h("h1", { style: { flex: "1 1 280px", margin: 0, fontWeight: 800, letterSpacing: "1.5px", fontSize: "15px"} }, "The temperatures can vary greatly on Mars, with the average temperature being -81,4ºF(-63ºC). In the martian summer, it can reach up to +20ºC(68ºF), and, in the winter, up to -99,4ºF(-73ºC). "),
            ),
            h("div", { style: { marginTop: "36px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "20px" } },
                h("img", { src: "/static/imgs/pressure.png", alt: "Pressure", style: { width: "200px", height: "200px", objectFit: "contain", flex: "0 0 100px" } }),
                h("h1", { style: { flex: "1 1 280px", margin: 0, fontWeight: 800, letterSpacing: "1.5px", fontSize: "15px"} }, "Pressure: The average atmospheric pressure in Mars is 6,1 millibars (less than 1% of Earth's), but it can go from 0,7 millibar up to 12 or 14 millibars."),
            ),
            h("div", { style: { marginTop: "36px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "20px" } },
                h("img", { src: "/static/imgs/humidity.png", alt: "Humidity", style: { width: "200px", height: "200px", objectFit: "contain", flex: "0 0 100px" } }),
                h("h1", { style: { flex: "1 1 280px", margin: 0, fontWeight: 800, letterSpacing: "1.5px", fontSize: "15px"} }, "Humidity: The humidity levels on Mars can be extremely low, due to its weak atmospheric pression (100 times lower than Earth's) and its freezing temperatures."),
            ),
            h("div", { style: { marginTop: "36px", background: colors.panel, flex: "1 1 240px", padding: "22px", boxSizing: "border-box", border: "1px solid " + colors.border, borderRadius: "6px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "20px" } },
                h("img", { src: "/static/imgs/radiation.png", alt: "Solar Radiation", style: { width: "100px", height: "100px", objectFit: "contain", flex: "0 0 100px" } }),
                h("h1", { style: { flex: "1 1 280px", margin: 0, fontWeight: 800, letterSpacing: "1.5px", fontSize: "15px"} }, "Solar Radiation: Mars experiences lower solar irradiance levels (around 586 W/m²), but extremely high UV radiation levels on its surface. The solar radiation levels on Mars are about 43% of Earth's. "),
            ),
            h("div", { style: { marginTop: "36px" } },
                h("a", {
                    href: "/planning",
                    style: {
                        display: "inline-flex",
                        alignItems: "center",
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
                }, "Start planning", h("span", { "aria-hidden": "true", style: { fontSize: "18px" } }, "→"))
            )
        ),

        h(SiteFooter)
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(h(Home));