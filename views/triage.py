"""Alert Triage & Case Management — analyst queue, workflow states, disposition and SLA tracking."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import escalation as E
from core import metrics as X
from core import ui
from core.ref import AS_OF, SLA_DAYS, MLRO_NAME
from core.smr_doc import build_smr_docx
from views.case_sim import open_case
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
            o1, o2, _ = st.columns([2.2, 1.3, 2.5], vertical_alignment="bottom")
            ids = list(q.sort_values("opened")["alert_id"])
            with o1:
                pick = st.selectbox("Work a case", ids, key="tri_pick",
                                    format_func=lambda i: f"{i} · {q.set_index('alert_id').loc[i, 'customer']}")
            with o2:
                st.button("Open in Case Simulator →", key="act_tri_open", on_click=open_case(M, pick), width="stretch")
            ui.csv_button(show, "alert_queue", "tri_queue")
        else:
            ui.note("Queue is empty for this period.", "good")

    ui.spacer(6)
    _escalation_queue(M)

    ui.sim_cta("If the queue keeps growing, model how many analyst hours a threshold change or a new hire would actually save.", target_kind="Match the current alert-volume run-rate", key="tri")


# ------------------------------------------------------------------ escalations ----
def _decide(idx, decision):
    def cb():
        recs = st.session_state["escalations"]
        recs[idx] = E.decide(recs[idx], decision, AS_OF)
    return cb


STATUS_COLOR = {E.STATUS_AWAITING: AMBER, E.STATUS_SUSPICION: RED, E.STATUS_RETURNED: SKY, E.STATUS_CLOSED: FAINT,
                "SMR lodged": LIME, "SMR lodged · acknowledged": LIME}


def _escalation_queue(M):
    recs = st.session_state.get("escalations", [])
    hist = E.history(M)
    awaiting = sum(r["status"] == E.STATUS_AWAITING for r in recs)
    with ui.card("tri_esc"):
        ui.card_title("MLRO Escalation Queue", right=f"MLRO: {MLRO_NAME} · {awaiting} awaiting a decision")
        if recs:
            st.markdown('<div class="esc-row" style="color:#6f7780;font-size:10.5px;font-weight:700;">'
                        '<span>ESCALATION</span><span>CLIENT · TYPOLOGY</span><span>STATUS</span><span>SCORE</span><span>MLRO DECISION</span></div>',
                        unsafe_allow_html=True)
            for i in range(len(recs) - 1, -1, -1):
                r = recs[i]
                col = STATUS_COLOR.get(r["status"], MUTED)
                due = f'<div class="esc-sub">SMR due {r["smr_due"]:%a %d %b %Y}</div>' if r.get("smr_due") is not None else ""
                c1, c2 = st.columns([3.9, 2.1], vertical_alignment="center")
                with c1:
                    st.markdown(f'<div class="esc-row" style="grid-template-columns:1.1fr 1.6fr 1.4fr 0.7fr;border-bottom:none;">'
                                f'<span><span class="esc-id">{r["esc_id"]}</span><div class="esc-sub">{r["alert_id"]} · {r["escalated"]:%d %b %Y} · {r["analyst"]}</div></span>'
                                f'<span>{r["client"]}<div class="esc-sub">{r["typology"]}</div></span>'
                                f'<span class="esc-status" style="color:{col}">{r["status"]}{due}</span>'
                                f'<span><b>{r["score"]}</b>/100</span></div>', unsafe_allow_html=True)
                with c2:
                    b1, b2, b3, b4 = st.columns(4)
                    waiting = r["status"] == E.STATUS_AWAITING
                    b1.button("Suspicion", key=f"act_esc_s_{i}", on_click=_decide(i, "suspicion"), disabled=not waiting, width="stretch",
                              help="MLRO forms a suspicion: the SMR must be lodged within 3 business days (24 hours for terrorism financing).")
                    b2.button("Return", key=f"act_esc_r_{i}", on_click=_decide(i, "return"), disabled=not waiting, width="stretch",
                              help="Send back to the analyst for more information.")
                    b3.button("Close", key=f"act_esc_c_{i}", on_click=_decide(i, "close"), disabled=not waiting, width="stretch",
                              help="No suspicion formed — close with the MLRO's rationale on file.")
                    b4.download_button("SMR ⬇", build_smr_docx(r["case"], AS_OF, smr_ref=f"SMR-{r['esc_id']}", rationale=r["rationale"] or None,
                                                               escalated_on=r["escalated"], analyst=r["analyst"]),
                                       file_name=f"SMR_draft_{r['esc_id']}.docx", key=f"act_esc_d_{i}", width="stretch",
                                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        else:
            ui.note("No escalations from this session yet. Open a case in the Case Simulator and press <b>Escalate to MLRO</b>; "
                    "it lands here for the MLRO's decision.")
        ui.spacer(4)
        st.markdown(f'<div class="case-sec">Past escalations · {len(hist)} accepted by the MLRO</div>', unsafe_allow_html=True)
        show = hist.head(40)[["esc_id", "alert_id", "client", "typology", "analyst", "escalated", "status", "smr_id"]].copy()
        show["escalated"] = show["escalated"].dt.strftime("%d %b %Y")
        st.dataframe(show.rename(columns={"esc_id": "Escalation", "alert_id": "Alert", "client": "Client", "typology": "Typology",
                                          "analyst": "Analyst", "escalated": "Escalated", "status": "Outcome", "smr_id": "SMR"}),
                     width="stretch", hide_index=True, height=220)
