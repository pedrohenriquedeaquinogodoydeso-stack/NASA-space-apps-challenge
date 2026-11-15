/*
  Humanity’s Future Is Red - Shared frontend code
  Styles, header and footer used by both the home page (index.html)
  and the planning page (planning.html).

  Parts of this file were written with AI assistance (Gemini, Claude)
*/

const h = React.createElement;

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

function SiteHeader() {
    return h("header", {
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
            }, "Humanity’s Future Is Red"))
        );
}

function SiteFooter() {
    return h("footer", {
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
            h("span", null, "NASA SPACE APPS CHALLENGE · HUMANITY’S FUTURE IS RED"),
            h("span", null, "ONE SMALL STEP TOWARD YOUR NEXT GREAT MISSION")
        );
}