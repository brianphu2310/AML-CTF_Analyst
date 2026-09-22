"""Simulator — Case decision mode.

The officer loads an alert (or types a new case), ticks the red flags found and the verification obtained,
and gets: a 0-100 suspicion score, the recommended next step, the regulatory clocks that start, what would
change the decision, how similar past alerts ended — and can escalate to the MLRO and download an SMR draft
(Word) in one click. Every change re-scores instantly, which is the "simulator" part: tick "source of funds
verified" and watch the recommendation move.
"""
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import case as C
from core import escalation as E
from core import metrics as X
from core import ui
from core.ref import (AS_OF, CUSTOMER_TYPES, CHANNELS, FOREIGN_TIERS, PRODUCTS, TYPOLOGY_NAMES, AU_STATE_NAMES,
                      USER_NAME, MLRO_NAME)
from core.smr_doc import build_smr_docx
from core.theme import LIME, TEAL, SLATE, AMBER, RED, INK, MUTED, FAINT, CARD_2, TIER_COLORS

TONE = {"ok": "#4f9fb0", "watch": AMBER, "alert": "#f07a45", "critical": RED}
BAND_COLORS = ["#4f9fb0", AMBER, "#f07a45", RED]
FLAG_BY_SHORT = {v: k for k, v in C.FLAG_SHORT.items()}
MIT_BY_SHORT = {v: k for k, v in C.MITIGANT_SHORT.items()}
HARD_BY_SHORT = {v: k for k, v in C.HARD_SHORT.items()}
CASE_KEYS = ["case_pick", "case_client", "case_type", "case_channel", "case_foreign", "case_product", "case_state", "case_typology",
             "case_amount", "case_ntx", "case_cash", "case_flags", "case_mits", "case_hard", "case_rationale"]


# ------------------------------------------------------------------ state ----
def _widget_values(c):
    return dict(case_client=c["client"], case_type=c["client_type"], case_channel=c["channel"], case_foreign=c["foreign_tier"],
                case_product=c["product"], case_state=c.get("state", "NSW"), case_typology=c["typology"],
                case_amount=float(round(c["amount"])), case_ntx=int(c["n_txns"]), case_cash=float(round(c["largest_cash"])),
                case_flags=[C.FLAG_SHORT[f] for f in c["flags"] if f in C.FLAG_SHORT],
                case_mits=[C.MITIGANT_SHORT[m] for m in c["mitigants"] if m in C.MITIGANT_SHORT],
                case_hard=[C.HARD_SHORT[h] for h in c["hard"] if h in C.HARD_SHORT], case_rationale="")


def _load(M, alert_id=None):
    def cb():
        ss = st.session_state
        c = C.case_from_alert(M, alert_id or ss.get("case_pick")) if (alert_id or ss.get("case_pick")) != "__new__" else C.blank_case()
        for k, v in _widget_values(c).items():
            ss[k] = v
        ss["case_meta"] = dict(ref=c["ref"], alert_id=c["alert_id"], client_id=c.get("client_id"), opened=c.get("opened"),
                               analyst=c.get("analyst"), branch=c.get("branch"), transactions=c.get("transactions", []),
                               disposition=c.get("disposition"))
        ss.pop("case_last_esc", None)
    return cb


def _current_case():
    ss = st.session_state
    meta = ss.get("case_meta", {})
    return dict(ref=meta.get("ref", "New case"), alert_id=meta.get("alert_id"), client_id=meta.get("client_id"),
                opened=meta.get("opened"), analyst=meta.get("analyst"), branch=meta.get("branch", "Richmond"),
                transactions=meta.get("transactions", []),
                client=ss["case_client"], client_type=ss["case_type"], channel=ss["case_channel"], foreign_tier=ss["case_foreign"],
                product=ss["case_product"], state=ss["case_state"], typology=ss["case_typology"], amount=float(ss["case_amount"] or 0),
                n_txns=int(ss["case_ntx"] or 1), largest_cash=float(ss["case_cash"] or 0),
                flags=[FLAG_BY_SHORT[x] for x in (ss["case_flags"] or [])],
                mitigants=[MIT_BY_SHORT[x] for x in (ss["case_mits"] or [])],
                hard=[HARD_BY_SHORT[x] for x in (ss["case_hard"] or [])])


def _escalate(case):
    def cb():
        ss = st.session_state
        recs = ss.setdefault("escalations", [])
        rec = E.new_escalation(recs, case, AS_OF, USER_NAME, ss.get("case_rationale", ""))
        recs.append(rec)
        ss["case_last_esc"] = rec["esc_id"]
    return cb


def open_case(M, alert_id):
    """Callback for other pages: load `alert_id` into the case form and open the Simulator on it."""
    def cb():
        ss = st.session_state
        ss["case_pick"] = ss["_keep_case_pick"] = alert_id
        _load(M, alert_id)()
        for k in CASE_KEYS:                   # the form is not on screen yet: prime the restore buffer too
            if k in ss:
                ss["_keep_" + k] = ss[k]
        ss["view_name"] = "Simulator"
        ss["sim_mode"] = ss["_keep_sim_mode"] = "Case decision"
    return cb


def _go_triage():
    st.session_state["view_name"] = "Triage"


def _pick_options(M):
    a = M["alerts"]
    recent = a[a["opened"] >= AS_OF - pd.Timedelta(days=120)].sort_values("opened", ascending=False)
    q = X.alert_queue(M, AS_OF)
    ids = list(q.sort_values("opened", ascending=False)["alert_id"]) + [x for x in recent["alert_id"] if x not in set(q["alert_id"])]
    lab = a.set_index("alert_id")
    fmt = {i: f"{i} · {lab.loc[i, 'customer']} · {lab.loc[i, 'typology']} · {lab.loc[i, 'disposition']}" for i in ids}
    fmt["__new__"] = "➕ New blank case (manual entry)"
    return ids + ["__new__"], fmt, list(q["alert_id"])


# ------------------------------------------------------------------ gauge ----
def _gauge_svg(score, tone_color):
    """Half-ring gauge 0-100 with the four decision bands and a needle."""
    W, H, cx, cy, r = 260, 150, 130, 132, 104
    def pt(v, rad):
        a = math.pi * (1 - v / 100)
        return cx + rad * math.cos(a), cy - rad * math.sin(a)
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="case-gauge">']
    bounds = [b[0] for b in C.BANDS] + [100]
    for (lo, hi), col in zip(zip(bounds, bounds[1:]), BAND_COLORS):
        (x0, y0), (x1, y1) = pt(lo + 0.6, r), pt(hi - 0.6, r)
        out.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{col}" stroke-width="16" stroke-opacity="0.9"/>')
    for v in bounds[1:-1]:
        (x, y) = pt(v, r + 16)
        out.append(f'<text x="{x:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-size="9" fill="{FAINT}" font-family="Inter,sans-serif">{v}</text>')
    mx, my = pt(min(max(score, 0.8), 99.2), r)
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="10" fill="#15171a" stroke="{INK}" stroke-width="3"/>'
               f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="4" fill="{tone_color}"/>'
               f'<text x="{cx}" y="{cy - 22}" text-anchor="middle" font-size="40" font-weight="700" fill="{tone_color}" font-family="Inter,sans-serif">{score:.0f}</text>'
               f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="10" fill="{FAINT}" font-family="Inter,sans-serif">suspicion score / 100</text></svg>')
    return "".join(out)


# ------------------------------------------------------------------ render ----
def render(M):
    ids, fmt, queue_ids = _pick_options(M)
    ss = st.session_state
    if "case_meta" not in ss:                        # first visit: open the newest alert in the queue
        first = queue_ids[0] if queue_ids else ids[0]
        ss.setdefault("case_pick", first)
        _load(M, first)()
    ui.restore_state({"case_pick": queue_ids[0] if queue_ids else ids[0], **_widget_values(C.blank_case())})

    left, right = st.columns([1.08, 1])

    # ---------------- case input ----------------
    with left:
        with ui.card("case_input"):
            ui.card_title("Case input", right="load an alert or enter a case · every change re-scores")
            p1, p2 = st.columns([3.2, 1], vertical_alignment="bottom")
            with p1:
                st.selectbox("Load from alerts (open queue first)", ids, key="case_pick", format_func=lambda i: fmt.get(i, i))
            with p2:
                st.button("Load case", key="act_case_load", on_click=_load(M), width="stretch", type="primary")
            meta = ss.get("case_meta", {})
            prior = M["smrs"][M["smrs"]["alert_id"] == meta.get("alert_id")] if meta.get("alert_id") else M["smrs"].iloc[0:0]
            if len(prior):
                pr = prior.iloc[0]
                ui.note(f"This alert already has <b>{pr['smr_id']}</b> on record ({pr['status'].lower()}, escalated "
                        f"{pr['escalated']:%d %b %Y}). Replaying it here is a review of that decision.", "warn")
            if meta.get("alert_id"):
                st.markdown(f'<div class="case-meta">Case <b>{meta["alert_id"]}</b> · opened {meta["opened"]:%d %b %Y} · '
                            f'analyst {meta.get("analyst") or "—"} · {meta.get("branch") or "—"} office · '
                            f'{len(meta.get("transactions") or [])} transactions on file</div>', unsafe_allow_html=True)

            st.markdown('<div class="case-sec">Client</div>', unsafe_allow_html=True)
            a1, a2 = st.columns([1.4, 1])
            a1.text_input("Client name", key="case_client")
            a2.selectbox("Client type", list(CUSTOMER_TYPES), key="case_type")
            b1, b2, b3 = st.columns([1.2, 1.5, 0.7])
            b1.selectbox("Delivery channel", list(CHANNELS), key="case_channel")
            b2.selectbox("Foreign dimension", list(FOREIGN_TIERS), key="case_foreign")
            b3.selectbox("State", AU_STATE_NAMES, key="case_state")
            c1, c2 = st.columns(2)
            c1.selectbox("Designated service", list(PRODUCTS), key="case_product")
            c2.selectbox("Monitoring rule / typology", TYPOLOGY_NAMES, key="case_typology")

            st.markdown('<div class="case-sec">Money moved</div>', unsafe_allow_html=True)
            d1, d2, d3 = st.columns(3)
            d1.number_input("Total value (AUD)", min_value=0.0, step=1000.0, key="case_amount", format="%.0f")
            d2.number_input("Transactions", min_value=1, step=1, key="case_ntx")
            d3.number_input("Largest physical cash (AUD)", min_value=0.0, step=500.0, key="case_cash", format="%.0f")

            st.markdown('<div class="case-sec">Red flags found</div>', unsafe_allow_html=True)
            st.pills("Red flags", list(C.FLAG_SHORT.values()), selection_mode="multi", key="case_flags", label_visibility="collapsed")
            st.markdown('<div class="case-sec">Verification obtained</div>', unsafe_allow_html=True)
            st.pills("Verification", list(C.MITIGANT_SHORT.values()), selection_mode="multi", key="case_mits", label_visibility="collapsed")
            st.markdown('<div class="case-sec hard">Hard stops</div>', unsafe_allow_html=True)
            st.pills("Hard stops", list(C.HARD_SHORT.values()), selection_mode="multi", key="case_hard", label_visibility="collapsed")

    case = _current_case()
    res = C.assess(case, AS_OF)
    tone = TONE[res["tone"]]

    # ---------------- decision ----------------
    with right:
        with ui.card("case_decision"):
            ui.card_title("Recommended decision", right=f"client risk {res['client_tier']} · {res['client_score']:.0f}/100")
            g, t = st.columns([1, 1.25], vertical_alignment="center")
            with g:
                st.markdown(f'<div class="gauge-wrap">{_gauge_svg(res["score"], tone)}</div>', unsafe_allow_html=True)
            with t:
                steps = "".join(f"<li>{s}</li>" for s in res["steps"])
                st.markdown(f'<div class="decision" style="--tone:{tone}"><div class="decision-title">{res["title"]}</div>'
                            f'<ol class="decision-steps">{steps}</ol></div>', unsafe_allow_html=True)
            if res["clocks"]:
                rows = "".join(f'<div class="clock"><span class="clock-l">⏱ {lab}</span><span class="clock-d">{d:%a %d %b %Y}'
                               f'<span class="clock-n"> · {n}</span></span></div>' for lab, d, n in res["clocks"])
                st.markdown(f'<div class="clocks">{rows}</div>', unsafe_allow_html=True)

        with ui.card("case_drivers"):
            ui.card_title("What drives the score", right="points added (+) or removed (−)")
            contrib = C.contributions(case)
            labels = [c[0] if len(c[0]) < 46 else c[0][:44] + "…" for c in contrib][::-1]
            vals = [c[1] for c in contrib][::-1]
            kinds = [c[2] for c in contrib][::-1]
            colors = [{"flag": RED, "mitigant": TEAL, "client": SLATE, "amount": "#8a9098"}[k] for k in kinds]
            fig = go.Figure(go.Bar(y=labels, x=vals, orientation="h", marker_color=colors, text=[f"{v:+.0f}" for v in vals],
                                   textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:+.1f}<extra></extra>"))
            fig.update_layout(**ui.base_layout(max(150, 26 * len(vals) + 30), margin=dict(l=4, r=30, t=4, b=4)), bargap=0.35)
            fig.update_xaxes(showgrid=True, gridcolor="#24282d", zeroline=True, zerolinecolor="#6f7780", tickfont=dict(size=9, color=FAINT))
            fig.update_yaxes(tickfont=dict(size=10.5, color="#c9ced4"))
            ui.show(fig, key="case_contrib_fig")

        with ui.card("case_whatif"):
            ui.card_title("What would change the decision")
            wi = C.what_if(case, AS_OF)[:5]
            if wi:
                rows = ""
                for kind, label, s2, title2, changes in wi:
                    verb = "If verified:" if kind == "verify" else "If cleared:"
                    rows += (f'<div class="wi-row{" wi-hit" if changes else ""}"><span class="wi-l"><span class="wi-verb">{verb}</span> {label}</span>'
                             f'<span class="wi-r">{res["score"]:.0f} → <b>{s2:.0f}</b> · {title2}</span></div>')
                st.markdown(rows, unsafe_allow_html=True)
            else:
                ui.note("Nothing on the form would move the score.")
            hb = C.history_base_rate(M, case["typology"], res["client_tier"])
            if hb["n"]:
                st.markdown(f'<div class="precedent">Precedent: of <b>{hb["n"]}</b> past <b>{case["typology"]}</b> alerts on '
                            f'<b>{res["client_tier"]}</b>-risk clients, <b>{hb["smr"]}</b> ({hb["rate"]:.0%}) ended in an SMR.</div>',
                            unsafe_allow_html=True)

        with ui.card("case_actions"):
            ui.card_title("Act on it", right=f"MLRO: {MLRO_NAME}")
            st.text_area("Analyst's note for the MLRO (goes into the escalation and the SMR draft)", key="case_rationale", height=68,
                         placeholder="e.g. Client could not explain why deposits were split across three branches.")
            e1, e2, e3 = st.columns([1, 1.1, 0.9])
            with e1:
                st.button("⇪ Escalate to MLRO", key="act_case_escalate", on_click=_escalate(case), width="stretch",
                          type="primary" if res["escalate"] else "secondary")
            with e2:
                esc_on = AS_OF if ss.get("case_last_esc") else None
                data = build_smr_docx(case, AS_OF, rationale=ss.get("case_rationale") or None, analyst=USER_NAME, escalated_on=esc_on)
                fname = f"SMR_draft_{(case.get('alert_id') or 'manual').replace('-', '_')}.docx"
                st.download_button("⬇ SMR draft (Word)", data, file_name=fname, key="act_case_smr",
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", width="stretch")
            with e3:
                st.button("Escalation queue →", key="act_case_queue", on_click=_go_triage, width="stretch")
            if ss.get("case_last_esc"):
                ui.note(f"Escalated as <b>{ss['case_last_esc']}</b> — awaiting {MLRO_NAME}'s decision on the Triage page.", "good")
            elif not res["escalate"]:
                ui.note("The score does not call for escalation. You can still escalate if your judgement differs — "
                        "the engine recommends, the MLRO decides.")

    ui.keep_state(CASE_KEYS)
