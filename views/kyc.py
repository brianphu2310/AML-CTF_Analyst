"""Client Risk Rating (KYC) — the AUSTRAC 4-factor risk model, onboarding pipeline and periodic reviews."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import metrics as X
from core import ui
from core.ref import AS_OF, RISK_WEIGHTS_DEFAULT, RISK_TIER_BOUNDS
from core.theme import LIME, TEAL, SKY, SLATE, CARD, CARD_2, MUTED, FAINT, TIER_COLORS


def render(M, cur, cmp):
    ui.page_header("Client Risk Rating (KYC)", "AUSTRAC's 4-factor risk model — client type, delivery channel, foreign dimension, products & services.", ui.period_tag(cur, cmp))

    cust = M["cust"]
    live = cust[cust["onboarded"] <= cur.end]
    tiers = X.risk_tier_breakdown(M, cur.end)
    overdue = X.overdue_customers(M, cur.end)

    kpis = [
        dict(label="Active clients", value=ui.fmt_num(len(live)), label_cmp=None),
        dict(label="Low risk", value=f"{int(tiers['Low'])}", color=TIER_COLORS["Low"], label_cmp=None, sub=f"{tiers['Low']/max(len(live),1)*100:.0f}% of book"),
        dict(label="Medium risk", value=f"{int(tiers['Medium'])}", color=TIER_COLORS["Medium"], label_cmp=None, sub=f"{tiers['Medium']/max(len(live),1)*100:.0f}% of book"),
        dict(label="High risk", value=f"{int(tiers['High'])}", color=TIER_COLORS["High"], label_cmp=None, sub=f"{tiers['High']/max(len(live),1)*100:.0f}% of book"),
        dict(label="Overdue periodic reviews", value=f"{len(overdue)}", color=TIER_COLORS["High"] if len(overdue) else LIME, label_cmp=None,
             sub=f"{len(overdue)/max(len(live),1)*100:.1f}% of active clients"),
        dict(label="New onboardings · period", value=ui.fmt_num(len(X.customers_onboarded_in(M, cur))), label_cmp=None),
    ]
    ui.kpi_row(kpis)

    c1, c2 = st.columns([1.15, 1.0])
    with c1:
        with ui.card("kyc_funnel"):
            ui.card_title("Onboarding Pipeline")
            stages = ["Applications received", "Identity verified", "Risk assessed", "Approved & active"]
            vals = X.onboarding_funnel(M, cur)
            for i in range(1, len(vals)):
                vals[i] = min(vals[i], vals[i - 1])
            f = go.Figure(go.Funnel(y=stages, x=vals, textinfo="value+percent initial", textfont=dict(size=11, color="#0b0c0e", family="Inter, sans-serif"),
                                    marker=dict(color=[LIME, TEAL, SKY, SLATE], line=dict(color=CARD, width=1.5)),
                                    connector=dict(fillcolor=CARD_2, line=dict(color=CARD_2, width=1)), hovertemplate="%{y}: %{x}<extra></extra>"))
            f.update_layout(margin=dict(l=8, r=8, t=2, b=2), height=210, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=11))
            ui.show(f, key="kyc_funnel_fig")
            ui.note("Conversion assumptions: 62% of applications clear identity verification on the first pass, 90% of risk-assessed clients are approved.")
    with c2:
        with ui.card("kyc_weights"):
            ui.card_title("4-Factor Risk Model — Current Weights")
            rows = ""
            for k, label in [("type", "Client type"), ("channel", "Delivery/service channel"), ("foreign", "Foreign dimension"), ("product", "Products & services")]:
                w = RISK_WEIGHTS_DEFAULT[k] * 100
                rows += (f'<div class="bar-row"><div class="bar-head"><span class="lbl">{label}</span><span class="val">{w:.0f}%</span></div>'
                         f'<div class="bar-track"><div class="bar-fill" style="width:{w:.0f}%;background:{LIME};"></div></div></div>')
            st.markdown(rows, unsafe_allow_html=True)
            ui.note(f"Risk tier bounds: score &lt; {RISK_TIER_BOUNDS[0]:.0f} = Low, {RISK_TIER_BOUNDS[0]:.0f}–{RISK_TIER_BOUNDS[1]:.0f} = Medium, "
                    f"&gt; {RISK_TIER_BOUNDS[1]:.0f} = High (see docs/METHODOLOGY.md). Tune these weights in the Simulator.")
            ui.sim_cta("See how shifting the foreign-dimension weight changes the risk book and alert volume.", preset="Raise foreign-dimension weight", key="kyc")

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    tabs = st.tabs(["Overdue reviews", "By client type", "By foreign dimension", "Full client list"])
    with tabs[0]:
        if len(overdue):
            odf = overdue.sort_values("next_review_due")[["customer_id", "name", "type", "risk_tier", "branch", "last_review", "next_review_due"]].copy()
            odf["days_overdue"] = (AS_OF - odf["next_review_due"]).dt.days
            odf["last_review"] = odf["last_review"].dt.strftime("%d %b %Y"); odf["next_review_due"] = odf["next_review_due"].dt.strftime("%d %b %Y")
            st.dataframe(odf.rename(columns={"customer_id": "ID", "name": "Client", "type": "Type", "risk_tier": "Risk tier", "branch": "Branch",
                        "last_review": "Last review", "next_review_due": "Was due", "days_overdue": "Days overdue"}), width="stretch", hide_index=True, height=280)
            ui.csv_button(odf, "overdue_reviews", "kyc_overdue")
        else:
            ui.note("No overdue periodic reviews for this period.", "good")
    with tabs[1]:
        tt = live.groupby("type").agg(customers=("customer_id", "count"), avg_score=("risk_score", "mean")).reset_index().sort_values("customers", ascending=False)
        st.dataframe(tt.rename(columns={"type": "Client type", "customers": "Clients", "avg_score": "Avg risk score"}), width="stretch", hide_index=True)
    with tabs[2]:
        ft = live.groupby("foreign_tier").agg(customers=("customer_id", "count"), avg_score=("risk_score", "mean")).reset_index()
        st.dataframe(ft.rename(columns={"foreign_tier": "Foreign dimension", "customers": "Clients", "avg_score": "Avg risk score"}), width="stretch", hide_index=True)
    with tabs[3]:
        show = live.sort_values("risk_score", ascending=False)[["customer_id", "name", "type", "channel", "foreign_tier", "product", "risk_score", "risk_tier", "branch", "onboarded"]].copy()
        show["onboarded"] = show["onboarded"].dt.strftime("%d %b %Y"); show["risk_score"] = show["risk_score"].round(1)
        st.dataframe(show.rename(columns={"customer_id": "ID", "name": "Client", "type": "Type", "channel": "Channel", "foreign_tier": "Foreign dimension",
                    "product": "Product/service", "risk_score": "Risk score", "risk_tier": "Tier", "branch": "Branch", "onboarded": "Onboarded"}),
                    width="stretch", hide_index=True, height=320)
        ui.csv_button(show, "client_register", "kyc_all")
