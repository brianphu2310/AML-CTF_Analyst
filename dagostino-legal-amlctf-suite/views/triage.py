"""Alert Triage & Case Management — analyst queue, workflow states, disposition and SLA tracking."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import metrics as X
from core import ui
from core.ref import AS_OF, SLA_DAYS
from core.theme import LIME, SKY, SLATE, TEAL, CARD, CARD_2, MUTED, FAINT, GREEN, RED, AMBER


def render(M, cur, cmp):
    ui.page_header("Alert Triage & Case Management", f"Analyst queue and investigation workflow · SLA target {SLA_DAYS} days.", ui.period_tag(cur, cmp))

    q = X.alert_queue(M, cur.end)
    sla = X.sla_table(M, cur)
    disp = X.disposition_table(M, cur)

    kpis = [
        dict(label="Open queue", value=f"{len(q)}", label_cmp=None),
        dict(label="Closed · period", value=f"{sla['closed']}", label_cmp=None),
        dict(label="SLA breach rate", value=ui.fmt_pct(sla["breach_rate"]) if pd.notna(sla["breach_rate"]) else "—", up_good=False, label_cmp=None),
        dict(label="Avg turnaround", value=f"{sla['avg_days']:.1f}d" if pd.notna(sla["avg_days"]) else "—", label_cmp=None),
        dict(label="Escalated to SMR · period", value=f"{int(disp['Escalated to SMR'])}", label_cmp=None),
    ]
    ui.kpi_row(kpis)

    c1, c2 = st.columns([1.15, 1.0])
    with c1:
        with ui.card("tri_flow"):
            ui.card_title("Investigation Workflow — alerts this period")
            stages = ["Opened", "Under investigation", "Escalated to SMR", "Closed — false positive", "Closed — no further action"]
            vals = [int(disp.get("Open", 0)) + int(disp.get("Under investigation", 0)) + int(disp.get("Escalated to SMR", 0)) + int(disp.get("Closed — false positive", 0)) + int(disp.get("Closed — no further action", 0)),
                    int(disp.get("Under investigation", 0)) + int(disp.get("Escalated to SMR", 0)) + int(disp.get("Closed — false positive", 0)) + int(disp.get("Closed — no further action", 0)),
                    int(disp.get("Escalated to SMR", 0)), int(disp.get("Closed — false positive", 0)), int(disp.get("Closed — no further action", 0))]
            f = go.Figure(go.Funnel(y=stages, x=[max(v, 0) for v in vals], textinfo="value", marker=dict(color=[TEAL, SKY, LIME, "#4a5058", SLATE], line=dict(color=CARD, width=1.5)),
                                    textfont=dict(color=["#0b0c0e", "#0b0c0e", "#0b0c0e", "#eef0f2", "#0b0c0e"], size=11),
                                    connector=dict(fillcolor=CARD_2, line=dict(color=CARD_2, width=1)), hovertemplate="%{y}: %{x}<extra></extra>"))
            f.update_layout(margin=dict(l=8, r=8, t=2, b=2), height=230, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=11))
            ui.show(f, key="tri_funnel")
            ui.note("Workflow states: Open → Under investigation → disposition (Escalated to SMR, Closed — false positive, or Closed — no further action).")
    with c2:
        with ui.card("tri_disp"):
            ui.card_title("Disposition Mix · period")
            colors = {"Open": AMBER, "Under investigation": SKY, "Escalated to SMR": LIME, "Closed — false positive": "#4a5058", "Closed — no further action": SLATE}
            labels = [k for k in disp.index if disp[k] > 0]
            if labels:
                ui.donut(labels, [disp[k] for k in labels], [colors[k] for k in labels], h=180,
                         center=f"<b style='font-size:16px;'>{int(disp.sum())}</b><br><span style='font-size:9px;color:{FAINT}'>alerts</span>", key="tri_donut")
            else:
                ui.note("No alerts in this period.")

    ui.spacer(6)
    with ui.card("tri_queue"):
        ui.card_title(f"Open Queue · as of {cur.end:%d %b %Y}", right=f"{len(q)} items")
        if len(q):
            show = q.sort_values("opened")[["alert_id", "opened", "typology", "customer", "risk_tier", "analyst", "disposition", "hours"]].copy()
            show["days_open"] = (min(AS_OF, cur.end) - show["opened"]).dt.days
            show["sla_status"] = np.where(show["days_open"] > SLA_DAYS, "Breach", "On track")
            show["opened"] = show["opened"].dt.strftime("%d %b %Y")
            st.dataframe(show.rename(columns={"alert_id": "Alert", "opened": "Opened", "typology": "Typology", "customer": "Client", "risk_tier": "Risk tier",
                        "analyst": "Analyst", "disposition": "Status", "hours": "Est. hours", "days_open": "Days open", "sla_status": "SLA"}),
                        width="stretch", hide_index=True, height=300)
            ui.csv_button(show, "alert_queue", "tri_queue")
        else:
            ui.note("Queue is empty for this period.", "good")

    ui.sim_cta("If the queue keeps growing, model how many analyst hours a threshold change or a new hire would actually save.", target_kind="Match the current alert-volume run-rate", key="tri")
