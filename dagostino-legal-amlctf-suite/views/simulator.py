"""Alert Threshold & Model Tuning Simulator — the flagship page.

An AML analyst adjusts risk-model factor weights and monitoring-rule thresholds and sees the projected
effect on alert volume, false-positive rate, analyst hours, SLA-breach risk and detection coverage —
the model-governance trade-off a Compliance Committee expects to be quantified, not asserted.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import simulate as S
from core import ui
from core.ref import SLA_DAYS
from core.theme import LIME, TEAL, MUTED, FAINT, GREEN, RED, AMBER

LEVER_KEYS = list(S.DEFAULTS)


def _apply(lever, value):
    def cb():
        st.session_state[lever] = value
    return cb


def _apply_preset(name):
    def cb():
        for k, v in S.preset_state(name).items():
            st.session_state[k] = v
    return cb


def _reset():
    for k, v in S.DEFAULTS.items():
        st.session_state[k] = v


def render(M, cur, cmp):
    st.markdown('<div class="sim-hero"><div><div class="sim-hero-kicker">FLAGSHIP · MODEL GOVERNANCE</div>'
                '<div class="sim-hero-title">Alert Threshold &amp; Model Tuning Simulator</div>'
                '<div class="sim-hero-sub">Tune the 4-factor risk-model weights and the five monitoring-rule thresholds, then see the '
                'projected effect on alert volume, false positives, analyst hours, SLA-breach risk and detection coverage before anything ships.</div></div>'
                '<span class="sim-hero-tag">Last 12 months baseline</span></div>', unsafe_allow_html=True)

    ui.restore_state(dict(S.DEFAULTS))
    p, f = S.base_actuals(M)
    s = {k: st.session_state[k] for k in LEVER_KEYS}
    r = S.project(f, s)
    r0 = S.project(f, S.DEFAULTS)

    # ---------------- presets ----------------
    with ui.card("sim_presets"):
        ui.card_title("Presets", right="one click loads a full scenario")
        cols = st.columns(len(S.PRESETS))
        for i, (name, col) in enumerate(zip(S.PRESETS, cols)):
            with col:
                st.button(name, key=f"act_preset_{i}", on_click=_apply_preset(name), width="stretch", help=S.PRESET_HELP[name])
        st.button("↺ Reset all levers", key="act_reset", on_click=_reset)

    # ---------------- levers ----------------
    with ui.card("sim_levers"):
        ui.card_title("Monitoring-Rule Thresholds", right="negative = more sensitive (lower threshold)")
        cols = st.columns(len(S.THRESH_LEVERS))
        for lever, col in zip(S.THRESH_LEVERS, cols):
            lo, hi, step = S.BOUNDS[lever]
            with col:
                st.slider(S.LEVER_LABEL[lever], lo, hi, key=lever, step=step)
        ui.spacer(4)
        c1, c2, c3 = st.columns(3)
        with c1:
            lo, hi, step = S.BOUNDS["sim_weight_foreign"]
            st.slider(S.LEVER_LABEL["sim_weight_foreign"], lo, hi, key="sim_weight_foreign", step=step)
        with c2:
            lo, hi, step = S.BOUNDS["sim_hires"]
            st.slider(S.LEVER_LABEL["sim_hires"], int(lo), int(hi), key="sim_hires", step=int(step))
        with c3:
            lo, hi, step = S.BOUNDS["sim_handle_time"]
            st.slider(S.LEVER_LABEL["sim_handle_time"], lo, hi, key="sim_handle_time", step=step)
    ui.keep_state(LEVER_KEYS)

    # ---------------- projected KPIs ----------------
    d = lambda a, b: (a - b) / b if b else None
    kpis = [
        dict(label="Projected alerts/month", value=f"{r['alerts1']:.1f}", d=d(r["alerts1"], r0["alerts1"]), up_good=False, label_cmp="vs neutral"),
        dict(label="False-positive rate", value=ui.fmt_pct(r["fp_rate1"]), d=d(r["fp_rate1"], r0["fp_rate1"]), up_good=False, label_cmp="vs neutral"),
        dict(label="Analyst hours/month", value=f"{r['hours1']:.0f}h", d=d(r["hours1"], r0["hours1"]), up_good=False, label_cmp="vs neutral"),
        dict(label="SLA-breach risk", value=ui.fmt_pct(r["sla_breach_risk1"]), d=d(r["sla_breach_risk1"], r0["sla_breach_risk1"]) if r0["sla_breach_risk1"] else None, up_good=False, label_cmp="vs neutral"),
        dict(label="Detection coverage", value=ui.fmt_pct(r["coverage1"]), d=d(r["coverage1"], r0["coverage1"]), up_good=True, label_cmp="vs neutral"),
    ]
    ui.kpi_row(kpis)

    # ---------------- bridge + tornado ----------------
    c1, c2 = st.columns([1.2, 1.0])
    with c1:
        with ui.card("sim_bridge"):
            ui.card_title("Alert-Volume Bridge — neutral to tuned run-rate")
            steps = S.bridge_data(f, s)
            labels = [x[0] for x in steps]; vals = [x[1] for x in steps]
            measure = ["absolute"] + ["relative"] * (len(steps) - 2) + ["total"]
            fig = go.Figure(go.Waterfall(x=labels, y=vals, measure=measure, connector=dict(line=dict(color="#3a3f46")),
                                         increasing=dict(marker=dict(color=RED)), decreasing=dict(marker=dict(color=GREEN)),
                                         totals=dict(marker=dict(color=LIME)), textposition="outside", texttemplate="%{y:+.1f}"))
            fig.update_layout(**ui.base_layout(260))
            fig.update_xaxes(tickfont=dict(size=8.5)); fig.update_yaxes(showgrid=True, gridcolor="#24282d")
            ui.show(fig, key="sim_bridge_fig")
    with c2:
        with ui.card("sim_tornado"):
            ui.card_title("What Moves Alert Volume Most", right="+1 unit of each lever")
            rank = S.lever_ranking(f)
            names = [x[0] for x in rank]; vals = [x[1] for x in rank]
            colors = [RED if v > 0 else GREEN for v in vals]
            fig2 = go.Figure(go.Bar(y=names, x=vals, orientation="h", marker_color=colors, hovertemplate="%{y}: %{x:+.2f} alerts/mo<extra></extra>"))
            fig2.update_layout(**ui.base_layout(260)); fig2.update_yaxes(tickfont=dict(size=9.5)); fig2.update_xaxes(showgrid=True, gridcolor="#24282d", zeroline=True, zerolinecolor="#6f7780")
            ui.show(fig2, key="sim_tornado_fig")

    # ---------------- goal seek ----------------
    with ui.card("sim_goal"):
        ui.card_title("Goal Seek — what threshold hits a target?")
        gc1, gc2, gc3 = st.columns([1.3, 1.3, 2])
        with gc1:
            metric = st.radio("Target metric", ["Alert volume (per month)", "Analyst hours (per month)"], key="sim_goal_metric", horizontal=False)
        default_target = round(r0["alerts1"] * 0.93, 1) if metric.startswith("Alert") else round(r0["hours1"] * 0.93, 1)
        with gc2:
            target = st.number_input("Target value", value=st.session_state.get("sim_goal_target", default_target), key="sim_goal_target", step=1.0)
        with gc3:
            st.markdown(f'<div class="goal-txt">Current projection: <b>{r["alerts1"]:.1f}</b> alerts/month, <b>{r["hours1"]:.0f}</b> analyst hours/month. '
                        f'Each row below shows how far <i>that lever alone</i> would need to move (holding everything else fixed) to reach the target.</div>', unsafe_allow_html=True)
        gs = S.goal_seek(f, s, target_alerts=target if metric.startswith("Alert") else None, target_hours=None if metric.startswith("Alert") else target)
        diff_color = {"Already met": GREEN, "Comfortable": GREEN, "Stretch": AMBER, "Not reachable on its own": RED, "Beyond a realistic range": RED}
        for _, row in gs.iterrows():
            required_ok = pd.notna(row["required"])
            apply_ok = pd.notna(row["apply_value"])
            need = ("Already met" if row["difficulty"] == "Already met" else
                    (f"Move to <b>{row['required']:.1f}</b> ({row['change']:+.1f})" if required_ok else "Not reachable with this lever alone"))
            c1, c2, c3 = st.columns([2.2, 3, 1.2])
            c1.markdown(f'<div class="goal-row" style="border-bottom:none;"><span class="lv">{row["label"]}</span></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="goal-row" style="border-bottom:none;"><span class="need">{need} · <span style="color:{diff_color[row["difficulty"]]};font-weight:700;">{row["difficulty"]}</span></span></div>', unsafe_allow_html=True)
            c3.button("Apply", key=f"act_apply_{row['lever']}", disabled=not apply_ok,
                      on_click=_apply(row["lever"], row["apply_value"]) if apply_ok else None, width="stretch")

    # ---------------- delivery risk ----------------
    with ui.card("sim_delivery"):
        ui.card_title("Delivery-Risk View", right="what if the tuning only partially lands by go-live?")
        dr = S.delivery_range(f, s)
        cols = st.columns(len(dr))
        for col, (_, row) in zip(cols, dr.iterrows()):
            with col:
                st.markdown(ui.kpi_html(f"{row['delivery']*100:.0f}% delivered", f"{row['alerts']:.1f}/mo",
                            sub=f"{row['hours']:.0f}h · {row['sla_risk']*100:.0f}% SLA risk", label_cmp=None), unsafe_allow_html=True)
        ui.note("A hire's headcount and pay are committed on day one and are never softened by delivery risk; threshold and weight changes "
                "are, because validating a new rule threshold against real data before go-live is the part that can slip.")
