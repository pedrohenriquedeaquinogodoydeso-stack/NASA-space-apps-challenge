/*
  Mars survival phase - front-end logic.
  Talks to POST /game/situation and renders the two dashboards.
*/
function playButtonSound3() {
    const sound = new Audio("/static/music/page.mp3");
    sound.volume = 0.3;
    sound.play().catch(function (error) {
        console.warn("Não foi possível tocar o som do botão.", error);
    });
}
(function () {
    "use strict";

    const BOOT = JSON.parse(document.getElementById("game-bootstrap").textContent);
    const PERIODS = ["Morning", "Afternoon", "Night"];
    const DICTIONARY_ENTRIES = [
        {
            id: "solar-storm",
            term: "Solar storm",
            definition: "A solar storm occurs when intense radiation and charged particles from the Sun hit a planet or its surface, potentially causing damage."
        },
        {
            id: "solar-panel",
            term: "Solar panel",
            definition: "A solar panel is a large panel made from glass and other materials. It captures sunlight and converts it into electricity for homes and other places."
        },
        {
            id: "life-support",
            term: "Water and oxygen",
            definition: "Water and oxygen are essential resources for survival on another planet, such as Mars. Resources, including energy, are limited there."
        }
    ];
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

    const rootStyle = document.documentElement.style;
    rootStyle.setProperty("--bg", colors.background);
    rootStyle.setProperty("--panel", colors.panel);
    rootStyle.setProperty("--text", colors.text);
    rootStyle.setProperty("--cream", colors.text);
    rootStyle.setProperty("--muted", colors.muted);
    rootStyle.setProperty("--orange", colors.orange);
    rootStyle.setProperty("--cyan", colors.cyan);
    rootStyle.setProperty("--green", colors.green);
    rootStyle.setProperty("--red", colors.red);
    rootStyle.setProperty("--border", colors.border);
    rootStyle.setProperty("--amber", colors.orange);

    const state = { situation: null, solar: 1.0, integrity: 100, busy: false, lastReportSol: 0 };
    const $ = (id) => document.getElementById(id);

    function h(tag, cls, text) {
        const el = document.createElement(tag);
        if (cls) el.className = cls;
        if (text !== undefined) el.textContent = text;
        return el;
    }

    async function post(body) {
        const res = await fetch("/game/situation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error("Server returned " + res.status);
        return res.json();
    }

    // ---------------------------------------------------------------- render
    function renderClock(clock) {
        $("sol").textContent = clock.sol;
        $("duration").textContent = clock.duration;
        const pips = $("pips");
        pips.replaceChildren();
        PERIODS.forEach(function (name, i) {
            const cls = i < clock.period_index ? "pip done" : i === clock.period_index ? "pip now" : "pip";
            pips.appendChild(h("div", cls, name));
        });
    }

    // ------------------------------------------------- real-event badge + panel
    const NASA_KINDS = {
        event:  { badge: "Real NASA event",       heading: "What really happened" },
        data:   { badge: "Real NASA data",        heading: "The real data behind it" },
        analog: { badge: "Inspired by NASA data", heading: "The real numbers behind it" }
    };
    const NASA_CSS = [
        ".nasa-badge{display:inline-flex;align-items:center;gap:.45em;margin:.35rem 0 .15rem;padding:.3em .8em;",
        "border:1px solid var(--cyan);border-radius:999px;background:rgba(112,225,232,.12);color:var(--cyan);",
        "font:inherit;font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;cursor:pointer;}",
        ".nasa-badge:hover,.nasa-badge:focus-visible{background:rgba(112,225,232,.26);outline:none;}",
        ".nasa-badge .nasa-i{display:inline-grid;place-items:center;width:1.25em;height:1.25em;border-radius:50%;",
        "background:var(--cyan);color:#0b1b1d;font-size:.85em;line-height:1;}",
        ".nasa-badge[hidden],.nasa-modal[hidden]{display:none;}",
        ".nasa-modal{position:fixed;inset:0;z-index:1000;display:grid;place-items:center;padding:1rem;",
        "background:rgba(0,0,0,.62);}",
        ".nasa-card{position:relative;width:min(34rem,100%);max-height:85vh;overflow:auto;padding:1.4rem 1.5rem;",
        "border:1px solid var(--cyan);border-radius:14px;background:var(--bg);color:var(--text);",
        "box-shadow:0 12px 40px rgba(0,0,0,.55);}",
        ".nasa-card h3{margin:.2rem 0 .8rem;font-size:1.2rem;}",
        ".nasa-kicker{color:var(--cyan);font-size:.75rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;}",
        ".nasa-heading{margin:.2rem 0;color:var(--muted);font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;}",
        ".nasa-fact{margin:.2rem 0 .9rem;line-height:1.55;}",
        ".nasa-note{margin:0 0 .9rem;padding:.55rem .75rem;border-left:3px solid var(--orange);",
        "background:rgba(255,118,74,.1);color:var(--muted);font-size:.85rem;line-height:1.45;}",
        ".nasa-source{margin:0 0 1rem;color:var(--muted);font-size:.85rem;line-height:1.4;}",
        ".nasa-source b{color:var(--text);}",
        ".nasa-link{display:inline-block;padding:.55em 1.1em;border-radius:8px;background:var(--cyan);color:#0b1b1d;",
        "font-weight:700;text-decoration:none;}",
        ".nasa-link:hover,.nasa-link:focus-visible{filter:brightness(1.12);outline:2px solid var(--text);outline-offset:2px;}",
        ".nasa-host{display:block;margin-top:.35rem;color:var(--muted);font-size:.75rem;}",
        ".nasa-close{position:absolute;top:.5rem;right:.7rem;width:2rem;height:2rem;border:0;border-radius:50%;",
        "background:transparent;color:var(--text);font-size:1.5rem;line-height:1;cursor:pointer;}",
        ".nasa-close:hover,.nasa-close:focus-visible{background:rgba(255,255,255,.14);outline:none;}"
    ].join("");
    const CREW_CSS = ".astro-name{display:block;max-width:7rem;margin-top:.3rem;color:var(--muted);font-size:.68rem;"
        + "line-height:1.15;text-align:center;overflow-wrap:anywhere;}";
    const nasaUI = { badge: null, modal: null, lastFocus: null };

    // Only plain http(s) links coming from the server are ever opened.
    function safeUrl(raw) {
        try {
            const u = new URL(raw);
            return (u.protocol === "https:" || u.protocol === "http:") ? u : null;
        } catch (e) { return null; }
    }

    function isNasaHost(host) {
        return host === "nasa.gov" || host.endsWith(".nasa.gov");
    }

    function initNasaPanel() {
        const style = h("style");
        style.textContent = NASA_CSS + CREW_CSS;
        document.head.appendChild(style);

        const badge = h("button", "nasa-badge");
        badge.type = "button";
        badge.hidden = true;
        badge.setAttribute("aria-haspopup", "dialog");
        badge.addEventListener("click", openNasaPanel);
        $("title").insertAdjacentElement("afterend", badge);
        nasaUI.badge = badge;

        const modal = h("div", "nasa-modal");
        modal.hidden = true;
        modal.setAttribute("role", "dialog");
        modal.setAttribute("aria-modal", "true");
        modal.setAttribute("aria-labelledby", "nasa-modal-title");
        const card = h("div", "nasa-card");
        const close = h("button", "nasa-close", "\u00d7");
        close.type = "button";
        close.setAttribute("aria-label", "Close");
        close.addEventListener("click", closeNasaPanel);
        const title = h("h3");
        title.id = "nasa-modal-title";
        const link = h("a", "nasa-link");
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        card.append(close, h("div", "nasa-kicker"), title, h("div", "nasa-heading"), h("p", "nasa-fact"),
            h("p", "nasa-note"), h("p", "nasa-source"), link, h("span", "nasa-host"));
        modal.appendChild(card);
        modal.addEventListener("click", function (e) { if (e.target === modal) closeNasaPanel(); });
        document.body.appendChild(modal);
        nasaUI.modal = modal;

        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && !modal.hidden) closeNasaPanel();
        });
    }

    function renderNasa(info) {
        closeNasaPanel(true);
        const badge = nasaUI.badge;
        if (!badge) return;
        if (!info || !info.fact) {
            badge.hidden = true;
            return;
        }
        const kind = NASA_KINDS[info.kind] || NASA_KINDS.data;
        badge.replaceChildren(h("span", "nasa-i", "i"), document.createTextNode(kind.badge));
        badge.setAttribute("aria-label", kind.badge + ". Open details and source.");
        badge.hidden = false;
    }

    function openNasaPanel() {
        const info = state.situation && state.situation.nasa;
        if (!info || !nasaUI.modal) return;
        playButtonSound3();
        const kind = NASA_KINDS[info.kind] || NASA_KINDS.data;
        const q = function (cls) { return nasaUI.modal.querySelector("." + cls); };
        q("nasa-kicker").textContent = kind.badge;
        $("nasa-modal-title").textContent = state.situation.title;
        q("nasa-heading").textContent = kind.heading;
        q("nasa-fact").textContent = info.fact;

        const note = q("nasa-note");
        note.hidden = info.kind !== "analog";
        note.textContent = info.kind === "analog"
            ? "Only the numbers above are real. The exact failure in this scenario is our own extrapolation."
            : "";

        const src = q("nasa-source");
        src.replaceChildren(h("b", "", "Source: "), document.createTextNode(info.source || "NASA"));

        const link = q("nasa-link");
        const host = q("nasa-host");
        const url = info.url ? safeUrl(info.url) : null;
        link.hidden = host.hidden = !url;
        if (url) {
            link.href = url.href;
            link.textContent = "Read the source \u2197";
            const name = url.hostname.replace(/^www\./, "");
            host.textContent = (isNasaHost(url.hostname) ? "Official NASA page \u00b7 " : "External page \u00b7 ") + name;
        }

        nasaUI.lastFocus = document.activeElement;
        nasaUI.modal.hidden = false;
        q("nasa-close").focus();
    }

    function closeNasaPanel(silent) {
        const modal = nasaUI.modal;
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        if (silent !== true && nasaUI.lastFocus && nasaUI.lastFocus.focus) nasaUI.lastFocus.focus();
    }

    function renderSituation(s) {
        if (!s) return;
        if (s.game_over) { showEnding(s); return; }
        state.situation = s;
        $("tag").textContent = s.tag;
        $("title").textContent = s.title;
        $("description").textContent = s.description;
        renderNasa(s.nasa);
        $("label-yes").textContent = s.options.yes;
        $("label-no").textContent = s.options.no;
        $("btn-yes").disabled = false;
        $("btn-no").disabled = false;
    }

    function barRow(status, label, right, pct, note) {
        const row = h("div", "row " + status);
        const top = h("div", "top");
        top.append(h("b", "", label), h("span", "", right));
        const bar = h("div", "bar");
        const fill = h("div", "fill");
        fill.style.width = Math.max(0, Math.min(100, pct)) + "%";
        bar.appendChild(fill);
        row.append(top, bar);
        if (note) row.appendChild(h("div", "note", note));
        return row;
    }

    function section(title) {
        const s = h("div", "section");
        s.appendChild(h("div", "label", title));
        return s;
    }

    function cell(label, value, target) {
        const c = h("div", "cell");
        c.append(h("small", "", label), h("b", "", value));
        if (target) c.appendChild(h("small", "", target));
        return c;
    }

    // ------------------------------------------------------------ crew + changes
    function div(cls, parent) {
        const e = h("div", cls);
        if (parent) parent.appendChild(e);
        return e;
    }

    function makeAstronaut(status, n, member) {
        const wrap = h("div", "astro " + status);
        wrap.title = member ? member.name + " \u00b7 " + member.agency + " (" + member.country + ")" : "Crew member " + n;
        const fig = div("astronaut-figure", wrap);
        div("astronaut-backpack", fig);
        div("astronaut-ear left", fig);
        div("astronaut-ear right", fig);
        div("astronaut-helmet", fig).appendChild(h("span", "astronaut-visor"));
        div("astronaut-neck", fig);
        ["left", "right"].forEach(function (side) {
            div("astronaut-arm " + side, fig).appendChild(h("span", "astronaut-glove"));
        });
        const torso = div("astronaut-torso", fig);
        const con = div("astronaut-console", torso);
        for (let i = 0; i < 3; i++) con.appendChild(h("span"));
        torso.appendChild(h("span", "astronaut-belt"));
        ["left", "right"].forEach(function (side) {
            div("astronaut-leg " + side, fig).appendChild(h("span", "astronaut-boot"));
        });
        return wrap;
    }

    function worstStatus(d) {
        const all = d.resources.map(function (r) { return r.status; }).concat([d.power.status, d.structure.status, d.crew ? d.crew.status : "ok"]);
        return all.indexOf("crit") >= 0 ? "crit" : all.indexOf("warn") >= 0 ? "warn" : "ok";
    }

    function stressNote(c) {
        const text = c.stress < 40 ? "The crew is calm" : c.stress < 70 ? "Tension is building" : "The crew is close to breaking";
        const extra = [];
        if (c.science_factor < 1) extra.push("science \u00d7" + c.science_factor.toFixed(2));
        if (c.risk_factor > 1.15) extra.push("incident risk \u00d7" + c.risk_factor.toFixed(2));
        return extra.length ? text + " \u00b7 " + extra.join(", ") : text;
    }

    function renderCrew(d) {
        const crew = d.crew || null;
        const members = crew && crew.members && crew.members.length ? crew.members : null;
        const n = members ? members.length : BOOT.crewSize;
        const s = section("Crew · " + n + (n === 1 ? " member" : " members"));
        const dock = h("div", "crew");
        const st = worstStatus(d);
        for (let i = 0; i < n; i++) dock.appendChild(makeAstronaut(st, i + 1, members ? members[i] : null));
        s.appendChild(dock);
        if (crew) {
            s.appendChild(barRow(crew.status, "Crew stress", Math.round(crew.stress) + " / 100", crew.stress, stressNote(crew)));
        }
        return s;
    }

    function fmtDelta(c) {
        const v = Number(Math.abs(c.delta).toFixed(c.decimals));
        return (c.delta > 0 ? "+" : "−") + v + (c.unit ? " " + c.unit : "");
    }

    function nonZero(list) {
        return (list || []).filter(function (c) { return c.delta !== 0; });
    }

    function changesText(list) {
        return nonZero(list).map(function (c) { return c.label + " " + fmtDelta(c); }).join(", ");
    }

    function renderChanges(ch, rep) {
        const root = $("changes");
        root.replaceChildren();
        function group(title, list, cls) {
            list = nonZero(list);
            if (!list.length) return;
            const g = h("div", "chg-group " + (cls || ""));
            g.appendChild(h("div", "label", title));
            const box = h("div", "chg");
            list.forEach(function (c) {
                const good = c.invert ? c.delta < 0 : c.delta > 0;  // stress: a rise is bad
                const chip = h("span", "chg-item " + (good ? "up" : "down"));
                chip.append(h("span", "arrow", c.delta > 0 ? "▲" : "▼"), h("span", "", c.label), h("b", "", fmtDelta(c)));
                box.appendChild(chip);
            });
            g.appendChild(box);
            root.appendChild(g);
        }
        if (ch) {
            group("Your decision", ch.choice);
            if (ch.incident) group("Incident: " + ch.incident.text, ch.incident.changes, "incident");
        }
        if (rep) group("Sol " + rep.sol + " closed (daily consumption and wear)", rep.changes, "sol");
    }

    function renderSurvival(d) {
        renderClock(d.clock);
        const root = $("view-survival");
        root.replaceChildren();

        root.appendChild(renderCrew(d));

        const res = section("Life support reserves");
        d.resources.forEach(function (r) {
            let note;
            if (r.days_left === null) note = "Stable: production covers consumption";
            else note = "About " + Math.floor(r.days_left) + " sols left at " + r.net.toFixed(1) + " " + r.unit + "/sol";
            res.appendChild(barRow(r.status, r.label, r.value.toLocaleString() + " / " + r.max.toLocaleString() + " " + r.unit,
                100 * r.value / r.max, note));
        });
        root.appendChild(res);

        const sys = section("Power and structure");
        const p = d.power;
        const loads = (p.loads || []).map(function (l) {
            return l.source + " " + (l.kwe > 0 ? "+" : "\u2212") + Math.abs(l.kwe) + " kWe (" + l.sols_left + (l.sols_left === 1 ? " sol" : " sols") + ")";
        });
        sys.appendChild(barRow(p.status, "Power balance", (p.net >= 0 ? "+" : "") + p.net + " kWe",
            100 * Math.min(1, p.supply / p.demand),
            p.supply + " kWe supply / " + p.demand + " kWe demand · solar " + p.solar_output + " kWe"
                + (loads.length ? " · event loads: " + loads.join(", ") : "")));
        sys.appendChild(barRow(d.structure.status, "Habitat structure", d.structure.integrity + "%", d.structure.integrity,
            d.structure.status === "ok" ? "" : "Repair the habitat before the next incident"));
        root.appendChild(sys);

        const hab = section("Habitat conditions");
        const grid = h("div", "grid");
        const t = BOOT.habitatTargets;
        grid.append(
            cell("Temperature", d.habitat.temperature_c + " °C", "target " + t.temperature_c + " °C"),
            cell("Pressure", d.habitat.pressure_psi + " psi", "target " + t.pressure_psi + " psi"),
            cell("O₂ partial pressure", d.habitat.ppo2_mmhg + " mmHg", "target " + t.oxygen_partial_pressure_mmhg + " mmHg"),
            cell("Humidity", d.habitat.humidity_pct + " %", "target " + t.humidity_pct + " %"),
            cell("Radiation", d.habitat.radiation_msv_day + " mSv/day")
        );
        hab.appendChild(grid);
        root.appendChild(hab);

        const mods = section("Modules");
        const chips = h("div", "chips");
        d.modules.forEach(function (m) {
            if (!m.active) return;
            chips.appendChild(h("span", "chip " + (m.online ? "on" : "off"), m.name + (m.online ? "" : " (low power)")));
        });
        if (!chips.children.length) chips.appendChild(h("span", "chip", "No optional modules equipped"));
        mods.appendChild(chips);
        root.appendChild(mods);

        const req = section("Daily crew requirements");
        const rg = h("div", "grid");
        const q = BOOT.dailyRequirements;
        rg.append(
            cell("Oxygen", q.oxygen_kg.toFixed(1) + " kg"),
            cell("Water", q.water_l.toFixed(1) + " L"),
            cell("Food", q.food_kg.toFixed(1) + " kg")
        );
        req.appendChild(rg);
        root.appendChild(req);
    }

    function renderResearch(d) {
        const root = $("view-research");
        root.replaceChildren();

        const top = section("Science score · " + d.site + " (x" + d.multiplier + ")");
        top.appendChild(h("div", "score", String(d.score)));
        top.appendChild(h("div", "rank", d.rank));
        if (d.next_rank_at !== null) {
            top.appendChild(barRow("ok", "Next rank", d.score + " / " + d.next_rank_at, 100 * d.score / d.next_rank_at));
        }
        root.appendChild(top);

        const obj = section("Site objectives");
        d.objectives.forEach(function (o) {
            obj.appendChild(barRow("ok", o.name, o.count + " / " + o.target, o.pct));
        });
        root.appendChild(obj);

        const stats = section("Statistics");
        const g = h("div", "grid");
        g.append(cell("Samples collected", String(d.samples_total)), cell("Points per sol", String(d.avg_per_sol)));
        stats.appendChild(g);
        root.appendChild(stats);
    }

    function renderDashboards(data) {
        if (data.survival_dashboard) renderSurvival(data.survival_dashboard);
        if (data.research_dashboard) renderResearch(data.research_dashboard);
    }

    function addLog(text, cls, prefix) {
        const li = h("li", cls || "");
        if (prefix) li.appendChild(h("b", "", prefix + " "));
        li.appendChild(document.createTextNode(text));
        const log = $("log");
        log.prepend(li);
        while (log.children.length > 30) log.lastChild.remove();
    }

    function showEnding(s) {
        $("btn-yes").disabled = true;
        $("btn-no").disabled = true;
        $("ending-card").className = "panel ending " + (s.victory ? "win" : "lose");
        $("ending-title").textContent = s.title;
        $("ending-text").textContent = s.description;
        $("ending-stats").textContent = "Sols survived: " + s.stats.sol + " · Science points: " + s.stats.science + " · Samples: " + s.stats.samples;
        $("ending").hidden = false;
    }

    // ---------------------------------------------------------------- actions
    function applyResponse(data, periodLabel) {
        if (typeof data.solar === "number") state.solar = data.solar;
        if (typeof data.integrity === "number") state.integrity = data.integrity;
        if (!data.survival_dashboard || !data.research_dashboard) {
            console.warn("Dashboards missing: app.py must return the full payload (see state_payload).");
        }
        const ch = data.changes || null;
        const rep = data.survival_dashboard && data.survival_dashboard.sol_report;
        $("feedback").textContent = data.message || "";
        if (data.message) {
            const all = ch ? ch.choice.concat(ch.incident ? ch.incident.changes : []) : [];
            const txt = changesText(all);
            addLog(data.message + (txt ? " (" + txt + ")" : ""), "", periodLabel);
        }
        renderChanges(ch, rep);
        if (rep && rep.sol !== state.lastReportSol) {
            state.lastReportSol = rep.sol;
            addLog(changesText(rep.changes), "report", "Sol " + rep.sol + " closed:");
        }
        renderDashboards(data);
        renderSituation(data.situation);
    }

    async function choose(action) {
        if (state.busy || !state.situation) return;
        state.busy = true;
        $("btn-yes").disabled = true;
        $("btn-no").disabled = true;
        const periodLabel = state.situation.period_label;
        try {
            const data = await post({
                action: action,
                choice_index: state.situation.index,
                solar: Math.max(0.4, Math.min(2.0, state.solar)),
                integrity: Math.max(0, Math.min(100, state.integrity))
            });
            applyResponse(data, periodLabel);
        } catch (err) {
            $("feedback").textContent = "Connection lost. Try again.";
            $("btn-yes").disabled = false;
            $("btn-no").disabled = false;
        } finally {
            state.busy = false;
        }
    }

    function selectTab(name) {
        ["survival", "research"].forEach(function (n) {
            $("tab-" + n).setAttribute("aria-selected", String(n === name));
            $("view-" + n).hidden = n !== name;
        });
    }

    function initDictionary() {
        const book = $("dictionary-book");
        const buttons = book.querySelectorAll(".dictionary-bookmark");

        buttons.forEach(function (button) {
            button.addEventListener("click", function () {
                playButtonSound3();
                const isOpen = button.getAttribute("aria-expanded") === "true";
                buttons.forEach(function (item) { item.setAttribute("aria-expanded", "false"); });
                if (isOpen) {
                    book.classList.remove("is-open");
                    $("dictionary-term").textContent = "Choose a bookmark";
                    $("dictionary-definition").textContent = "Select one of the colored tabs to read a space dictionary entry.";
                    return;
                }

                const entry = DICTIONARY_ENTRIES.find(function (item) { return item.id === button.dataset.entry; });
                if (!entry) return;
                $("dictionary-term").textContent = entry.term;
                $("dictionary-definition").textContent = entry.definition;
                button.setAttribute("aria-expanded", "true");
                book.classList.add("is-open");
            });
        });
    }

    async function init() {
        initDictionary();
        initNasaPanel();
        $("btn-yes").addEventListener("click", function () { choose("yes"); });
        $("btn-no").addEventListener("click", function () { choose("no"); });
        $("tab-survival").addEventListener("click", function () { selectTab("survival"); });
        $("tab-research").addEventListener("click", function () { selectTab("research"); });
        try {
            applyResponse(await post({ action: "next" }), "");
        } catch (err) {
            $("title").textContent = "No signal from the habitat";
            $("description").textContent = "Reload the page to try again.";
        }
    }

    init();
})();