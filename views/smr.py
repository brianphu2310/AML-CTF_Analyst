"""SMR Register & Reporting — Suspicious Matter Report register with AUSTRAC-style submission tracking."""
import numpy as np
import pandas as pd
import streamlit as st

from core import case as C
from core import metrics as X
from core import ui
from core.smr_doc import build_smr_docx
from core.ref import AS_OF
from core.theme import LIME, SKY, GRID, GREEN, AMBER, RED, FAINT


def render(M, cur, cmp):
    ui.page_header("SMR Register & Reporting", "Suspicious Matter Reports (Australia's SAR equivalent) and their AUSTRAC lodgement status.", ui.period_tag(cur, cmp))

    reg = X.smr_register(M, cur)
    status = X.austrac_status_table(M, cur.end)
    lag = (reg["submitted"] - reg["escalated"]).dt.days.dropna()

    kpis = [
        dict(label="SMRs filed · period", value=f"{len(reg)}", label_cmp=None),
        dict(label="Draft — pending submission", value=f"{int(status['Draft'])}", label_cmp=None, up_good=False),
        dict(label="Submitted to AUSTRAC", value=f"{int(status['Submitted'])}", label_cmp=None),
        dict(label="Acknowledged", value=f"{int(status['Acknowledged'])}", label_cmp=None),
        dict(label="Avg lodgement lag", value=f"{lag.mean():.1f}d" if len(lag) else "—", label_cmp=None, sub="Escalation to AUSTRAC submission"),
    ]
    ui.kpi_row(kpis)

    c1, c2 = st.columns([1.2, 1.0])
    with c1:
        with ui.card("smr_bytyp"):
            ui.card_title("SMRs by Typology · period")
            tt = reg["typology"].value_counts()
            if len(tt):
                import plotly.graph_objects as go
                from core.theme import TYP_COLORS
                order = list(M["alerts"]["typology"].unique())
                tt = tt.reindex([t for t in order if t in tt.index]).fillna(0)
                f = go.Figure(go.Bar(x=tt.index, y=tt.values, marker_color=LIME, hovertemplate="%{x}: %{y}<extra></extra>"))
                f.update_layout(**ui.base_layout(210)); f.update_xaxes(showgrid=False, tickfont=dict(size=9)); f.update_yaxes(showgrid=True, gridcolor="#24282d")
                ui.show(f, key="smr_typ_fig")
            else:
                ui.note("No SMRs filed in this period.")
    with c2:
        with ui.card("smr_status"):
            ui.card_title("AUSTRAC Status · all live SMRs")
            colors = {"Draft": AMBER, "Submitted": SKY, "Acknowledged": LIME}
            labels = [k for k in status.index if status[k] > 0]
            if labels:
                ui.donut(labels, [status[k] for k in labels], [colors[k] for k in labels], h=170,
                         center=f"<b style='font-size:16px;'>{int(status.sum())}</b><br><span style='font-size:9px;color:{FAINT}'>SMRs</span>", key="smr_status_donut")

    ui.spacer(6)
    with ui.card("smr_register"):
        ui.card_title("SMR Register", right=f"{len(reg)} reports this period")
        if len(reg):
            show = reg.sort_values("escalated", ascending=False)[["smr_id", "escalated", "customer", "typology", "analyst", "branch", "status", "submitted"]].copy()
            show["escalated"] = show["escalated"].dt.strftime("%d %b %Y")
            show["submitted"] = show["submitted"].dt.strftime("%d %b %Y").fillna("—")
            st.dataframe(show.rename(columns={"smr_id": "SMR", "escalated": "Escalated", "customer": "Client", "typology": "Typology", "analyst": "Analyst",
                        "branch": "Branch", "status": "AUSTRAC status", "submitted": "Submitted"}), width="stretch", hide_index=True, height=320)
            d1, d2, d3 = st.columns([2.4, 1.2, 1.4], vertical_alignment="bottom")
            ordered = reg.sort_values("escalated", ascending=False)
            with d1:
                sid = st.selectbox("Generate the SMR document for", list(ordered["smr_id"]), key="smr_pick",
                                   format_func=lambda i: f"{i} · {ordered.set_index('smr_id').loc[i, 'customer']} · {ordered.set_index('smr_id').loc[i, 'typology']}")
            row = ordered.set_index("smr_id").loc[sid]
            with d2:
                st.download_button("⬇ SMR (Word)", build_smr_docx(C.case_from_alert(M, row["alert_id"]), row["escalated"], smr_ref=sid,
                                                                  escalated_on=row["escalated"], analyst=row["analyst"]),
                                   file_name=f"{sid}.docx", key="act_smr_doc", width="stretch",
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            with d3:
                ui.csv_button(show, "smr_register", "smr_reg")
            ui.note("Every SMR here originates from an alert escalated on the Alert Triage page — the two registers always reconcile.")
        else:
            ui.note("No SMRs were filed for this reporting period.", "good")
