"""Transaction Monitoring — rule-based typology detection with configurable thresholds."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import metrics as X
from core import ui
from core.ref import TYPOLOGIES, TYPOLOGY_NAMES
from core.theme import LIME, SKY, GRID, MUTED, FAINT, TYP_COLORS


def render(M, cur, cmp):
    ui.page_header("Transaction Monitoring", "Rule-based alert generation across five AML/CTF typologies.", ui.period_tag(cur, cmp))

    tt = X.typology_table(M, cur)
    total_alerts = int(tt["alerts"].sum())
    total_fp = int(tt["false_positives"].sum())
    total_esc = int(tt["escalated"].sum())
    fp_rate = total_fp / max(total_alerts, 1)

    kpis = [
        dict(label="Alerts generated", value=f"{total_alerts}", label_cmp=None),
        dict(label="False-positive rate", value=ui.fmt_pct(fp_rate), label_cmp=None, up_good=False),
        dict(label="Escalated to SMR", value=f"{total_esc}", label_cmp=None),
        dict(label="Avg analyst hours/alert", value=f"{tt['avg_hours'].mean():.1f}h", label_cmp=None),
    ]
    ui.kpi_row(kpis)

    c1, c2 = st.columns([1.2, 1.0])
    with c1:
        with ui.card("mon_bar"):
            ui.card_title("Alerts by Typology · period")
            f = go.Figure(go.Bar(x=tt["typology"], y=tt["alerts"], marker_color=TYP_COLORS, text=tt["alerts"], textposition="outside",
                                 hovertemplate="%{x}: %{y} alerts<extra></extra>"))
            f.update_layout(**ui.base_layout(230))
            f.update_xaxes(showgrid=False, tickfont=dict(size=9)); f.update_yaxes(showgrid=True, gridcolor="#24282d")
            ui.show(f, key="mon_bar_fig")
    with c2:
        with ui.card("mon_fp"):
            ui.card_title("False-Positive Rate by Typology")
            f2 = go.Figure(go.Bar(x=tt["typology"], y=(tt["fp_rate"] * 100).round(1), marker_color=SKY,
                                  hovertemplate="%{x}: %{y}%<extra></extra>"))
            f2.update_layout(**ui.base_layout(230))
            f2.update_xaxes(showgrid=False, tickfont=dict(size=9)); f2.update_yaxes(showgrid=True, gridcolor="#24282d", ticksuffix="%")
            ui.show(f2, key="mon_fp_fig")

    ui.spacer(4)
    st.markdown('<div class="card-title" style="margin-bottom:6px;">Typology Detection Logic</div>', unsafe_allow_html=True)
    for i, t in enumerate(TYPOLOGY_NAMES):
        spec = TYPOLOGIES[t]
        with ui.card(f"mon_typ_{i}"):
            c1, c2, c3 = st.columns([2.2, 1, 1])
            with c1:
                st.markdown(f'<div class="card-title" style="display:flex;align-items:center;gap:8px;">'
                            f'<span style="width:9px;height:9px;border-radius:50%;background:{TYP_COLORS[i]};display:inline-block;"></span>{t}</div>', unsafe_allow_html=True)
                st.caption(spec["desc"])
            with c2:
                row = tt[tt["typology"] == t].iloc[0]
                st.markdown(ui.kpi_html("Alerts · period", f"{int(row['alerts'])}", label_cmp=None), unsafe_allow_html=True)
            with c3:
                st.markdown(ui.kpi_html("FP rate", ui.fmt_pct(row["fp_rate"]) if pd.notna(row["fp_rate"]) else "—", label_cmp=None), unsafe_allow_html=True)
    ui.sim_cta("Every threshold below is a lever in the Simulator — tighten or loosen them and see the projected effect on volume, false positives and analyst hours.", key="mon")

    ui.spacer(6)
    with ui.card("mon_queue"):
        ui.card_title("Alerts Raised This Period")
        a = X.alerts_in(M, cur).sort_values("opened", ascending=False)
        show = a[["alert_id", "opened", "typology", "customer", "risk_tier", "analyst", "disposition", "hours"]].copy()
        show["opened"] = show["opened"].dt.strftime("%d %b %Y")
        st.dataframe(show.rename(columns={"alert_id": "Alert", "opened": "Opened", "typology": "Typology", "customer": "Client",
                    "risk_tier": "Risk tier", "analyst": "Analyst", "disposition": "Disposition", "hours": "Hours"}),
                    width="stretch", hide_index=True, height=300)
        ui.csv_button(show, "alerts_period", "mon_alerts")
