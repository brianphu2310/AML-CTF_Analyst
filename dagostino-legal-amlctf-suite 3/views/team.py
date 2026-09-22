"""Team & Workload — analyst caseload and SLA compliance."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import metrics as X
from core import ui
from core.ref import ANALYSTS
from core.theme import LIME, TEAL, MUTED, FAINT, GREEN, RED


def render(M, cur, cmp):
    ui.page_header("Team & Workload", "Analyst caseload and SLA compliance across the compliance team.", ui.period_tag(cur, cmp))

    at = X.analyst_table(M, cur)
    kpis = [
        dict(label="Team headcount", value=f"{len(ANALYSTS)}", label_cmp=None),
        dict(label="Alerts worked · period", value=f"{int(at['alerts'].sum())}", label_cmp=None),
        dict(label="Total analyst hours", value=f"{at['hours'].sum():.0f}h", label_cmp=None),
        dict(label="Team SLA breach rate", value=ui.fmt_pct(at['sla_breach_rate'].mean()) if at['sla_breach_rate'].notna().any() else "—", up_good=False, label_cmp=None),
    ]
    ui.kpi_row(kpis)

    c1, c2 = st.columns([1.2, 1.0])
    with c1:
        with ui.card("team_case"):
            ui.card_title("Caseload by Analyst · period")
            d = at.sort_values("alerts", ascending=True)
            f = go.Figure(go.Bar(y=d["short"], x=d["alerts"], orientation="h", marker_color=LIME, hovertemplate="%{y}: %{x} alerts<extra></extra>"))
            f.update_layout(**ui.base_layout(230)); f.update_yaxes(tickfont=dict(size=10)); f.update_xaxes(showgrid=True, gridcolor="#24282d")
            ui.show(f, key="team_case_fig")
    with c2:
        with ui.card("team_sla"):
            ui.card_title("SLA Breach Rate by Analyst")
            d = at.dropna(subset=["sla_breach_rate"]).sort_values("sla_breach_rate", ascending=True)
            if len(d):
                colors = [RED if v > 0.25 else (TEAL if v > 0.1 else GREEN) for v in d["sla_breach_rate"]]
                f2 = go.Figure(go.Bar(y=d["short"], x=(d["sla_breach_rate"] * 100).round(1), orientation="h", marker_color=colors, hovertemplate="%{y}: %{x}%<extra></extra>"))
                f2.update_layout(**ui.base_layout(230)); f2.update_yaxes(tickfont=dict(size=10)); f2.update_xaxes(showgrid=True, gridcolor="#24282d", ticksuffix="%")
                ui.show(f2, key="team_sla_fig")
            else:
                ui.note("No closed alerts in this period to compute SLA rates from.")

    ui.spacer(6)
    cols = st.columns(len(ANALYSTS))
    for col, a in zip(cols, ANALYSTS):
        row = at[at["short"] == a["short"]].iloc[0]
        with col:
            initials = "".join(p[0] for p in a["name"].split()[:2]).upper()
            months = max(cur.days / 30.4, 0.1)
            util = row["alerts"] / (a["capacity"] * months) if a["capacity"] else 0
            st.markdown(f'<div class="analyst-card"><div class="analyst-avatar">{initials}</div>'
                        f'<div style="font-weight:700;font-size:12.5px;">{a["name"]}</div>'
                        f'<div style="font-size:10.5px;color:{MUTED};margin-bottom:6px;">{a["role"]} · {a["branch"]}</div>'
                        f'<div style="font-size:11px;color:{MUTED};">{int(row["alerts"])} alerts · {row["hours"]:.0f}h</div>'
                        f'<div style="font-size:11px;color:{MUTED};">{util*100:.0f}% of caseload capacity</div></div>', unsafe_allow_html=True)

    ui.spacer(6)
    with ui.card("team_table"):
        ui.card_title("Analyst Detail")
        show = at[["analyst", "role", "branch", "alerts", "hours", "closed", "sla_breach_rate", "escalated"]].copy()
        show["sla_breach_rate"] = (show["sla_breach_rate"] * 100).round(1)
        st.dataframe(show.rename(columns={"analyst": "Analyst", "role": "Role", "branch": "Branch", "alerts": "Alerts", "hours": "Hours",
                    "closed": "Closed", "sla_breach_rate": "SLA breach %", "escalated": "Escalated to SMR"}), width="stretch", hide_index=True)
    ui.sim_cta("Model whether hiring another analyst — or tightening thresholds instead — is the better fix for the queue.", preset="Hire an AML analyst", key="team")
