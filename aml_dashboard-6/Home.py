"""
Home.py
Portfolio-level overview of the AML Compliance Suite.

Executive KPI row, portfolio risk distribution, transaction volume trend,
case load by analyst, customer lifecycle waterfall, and target gauges.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from db_utils import load_all
from theme import (
    inject_css, page_header, kpi_card, section_title,
    chart_layout_2d, chart_layout_3d, chart_color_sequence,
    RISK_COLOR_MAP,
    TEAL_DARK, TEAL_MID, TEAL_LIGHT, TEAL_PALE, TEAL_SOFT,
    CRITICAL, HIGH, MEDIUM, LOW, INFO,
    TEXT_PRIMARY, TEXT_MUTED, CARD_BORDER, CHART_GRID,
)

st.set_page_config(page_title="AML Compliance Suite", layout="wide")
inject_css()

data = load_all()
customers = data["customers"]
transactions = data["transactions"]
screening = data["screening"]
cases = data["cases"]

page_header(
    "AML Compliance Suite",
    "Customer risk, screening, transaction monitoring, case management and UBO oversight - in one workspace.",
    badge="DEMO DATA",
)

# ==========================================================================
# KPI ROW
# ==========================================================================
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    kpi_card("Total Customers", f"{len(customers):,}",
             f"{(customers['status']=='Active').sum()} active")
with c2:
    high_risk = customers[customers["risk_level"].isin(["High", "Critical"])].shape[0]
    pct = high_risk / len(customers) * 100 if len(customers) else 0
    kpi_card("High / Critical Risk", f"{high_risk:,}", f"{pct:.1f}% of book", HIGH)
with c3:
    open_hits = screening[screening["status"].isin(["Open", "Escalated", "Under Review"])].shape[0]
    kpi_card("Open Screening Alerts", f"{open_hits:,}", f"{screening.shape[0]} total hits", MEDIUM)
with c4:
    open_cases = cases[~cases["status"].str.contains("Closed")].shape[0]
    kpi_card("Active Cases", f"{open_cases:,}", f"{cases.shape[0]} total this period", INFO)
with c5:
    pending_smr = cases[cases["status"] == "Pending SMR Lodgement"].shape[0]
    kpi_card("Pending SMR Lodgement", f"{pending_smr:,}", "within statutory 3-day window", LOW)

# ==========================================================================
# PORTFOLIO RISK DISTRIBUTION  +  INDUSTRY RISK
# ==========================================================================
section_title("Portfolio Risk Distribution")
col1, col2 = st.columns([1.1, 1])

with col1:
    risk_counts = (
        customers["risk_level"]
        .value_counts()
        .reindex(["Low", "Medium", "High", "Critical"])
        .fillna(0)
    )
    fig = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map=RISK_COLOR_MAP,
        labels={"x": "Risk Level", "y": "Customers"},
        text=risk_counts.values,
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(color=TEXT_MUTED, size=11),
        marker=dict(line=dict(width=0.5, color=CARD_BORDER)),
    )
    fig.update_layout(**chart_layout_2d(height=340))
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    industry_risk = (
        customers.groupby("industry")["risk_score"]
        .mean()
        .sort_values(ascending=True)
        .tail(8)
    )
    fig2 = px.bar(
        x=industry_risk.values,
        y=industry_risk.index,
        orientation="h",
        labels={"x": "Avg Risk Score", "y": ""},
        color=industry_risk.values,
        color_continuous_scale=[LOW, MEDIUM, HIGH, CRITICAL],
    )
    fig2.update_traces(marker=dict(line=dict(width=0.5, color=CARD_BORDER)))
    fig2.update_layout(**chart_layout_2d(height=340))
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================================================
# TRANSACTION VOLUME TREND
# ==========================================================================
section_title("Transaction Volume Trend (last 90 days)")
recent = transactions[
    transactions["txn_date"] >= transactions["txn_date"].max() - pd.Timedelta(days=90)
].copy()
daily = (
    recent.groupby([recent["txn_date"].dt.date, "direction"])["amount"]
    .sum()
    .reset_index()
)
fig3 = px.area(
    daily,
    x="txn_date",
    y="amount",
    color="direction",
    color_discrete_map={"Inbound": TEAL_DARK, "Outbound": TEAL_MID},
    labels={"txn_date": "Date", "amount": "Total Amount (AUD)"},
)
fig3.update_traces(
    line=dict(width=1.6),
    fillcolor=None,
)
# Add gradient fill manually
for trace in fig3.data:
    if trace.name == "Inbound":
        trace.update(fillcolor="rgba(61,95,110,0.28)")
    elif trace.name == "Outbound":
        trace.update(fillcolor="rgba(74,110,126,0.22)")
fig3.update_layout(**chart_layout_2d(height=320))
st.plotly_chart(fig3, use_container_width=True)

# ==========================================================================
# CUSTOMER LIFECYCLE WATERFALL
# ==========================================================================
section_title("Customer Lifecycle Waterfall")
st.caption(
    "From onboarding through to case closure / SMR lodgement - how the current book has moved "
    "through each stage of the AML lifecycle."
)

total_customers = len(customers)
active_customers = int((customers["status"] == "Active").sum())
high_crit = int(customers["risk_level"].isin(["High", "Critical"]).sum())
screened = int(screening["customer_id"].nunique())
flagged_case = int(cases["customer_id"].nunique())
escalated = int((cases["status"].isin(
    ["Escalated - Senior Review", "Pending SMR Lodgement", "SMR Lodged", "Post-SMR Monitoring"]
)).sum())
smr_lodged = int((cases["status"].isin(["SMR Lodged", "Post-SMR Monitoring"])).sum())
closed = int(cases["status"].str.contains("Closed").sum())

wf_labels = [
    "Total Customers",
    "Active",
    "High/Critical",
    "Screened",
    "Case Opened",
    "Escalated",
    "SMR Lodged",
    "Closed",
]
wf_values = [
    total_customers,
    active_customers - total_customers,
    high_crit - active_customers,
    screened - high_crit,
    flagged_case - screened,
    escalated - flagged_case,
    smr_lodged - escalated,
    closed - smr_lodged,
]

fig_wf = go.Figure(
    go.Waterfall(
        name="Lifecycle",
        orientation="v",
        measure=["absolute"] + ["relative"] * 7,
        x=wf_labels,
        y=wf_values,
        text=[f"{v:+,}" if i > 0 else f"{v:,}" for i, v in enumerate(wf_values)],
        textposition="outside",
        textfont=dict(color=TEXT_PRIMARY, size=11),
        connector=dict(line=dict(color=CARD_BORDER, width=1)),
        increasing=dict(marker=dict(color=TEAL_DARK, line=dict(width=0.5, color=CARD_BORDER))),
        decreasing=dict(marker=dict(color=HIGH, line=dict(width=0.5, color=CARD_BORDER))),
        totals=dict(marker=dict(color=TEAL_LIGHT, line=dict(width=0.5, color=CARD_BORDER))),
    )
)
fig_wf.update_layout(**chart_layout_2d(height=380))
st.plotly_chart(fig_wf, use_container_width=True)

# ==========================================================================
# TARGET GAUGES
# ==========================================================================
section_title("Compliance Health Gauges")

g1, g2, g3 = st.columns(3)


def _gauge(value, title, target, color, suffix="%"):
    """Small radial gauge with a target threshold line."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": suffix, "font": {"color": TEAL_DARK, "size": 28,
                                               "family": "Source Serif 4, Georgia, serif"}},
            title={"text": title, "font": {"color": TEXT_MUTED, "size": 12}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": TEXT_MUTED,
                    "tickfont": {"color": TEXT_MUTED, "size": 10},
                },
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.4)",
                "borderwidth": 1,
                "bordercolor": CARD_BORDER,
                "steps": [
                    {"range": [0, 40], "color": "rgba(220,232,236,0.35)"},
                    {"range": [40, 70], "color": "rgba(168,196,206,0.35)"},
                    {"range": [70, 100], "color": "rgba(123,168,184,0.35)"},
                ],
                "threshold": {
                    "line": {"color": CRITICAL, "width": 3},
                    "thickness": 0.75,
                    "value": target,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY),
        margin=dict(t=40, b=10, l=20, r=20),
        height=260,
    )
    return fig


# Metric 1: % of book flagged at high/critical risk
pct_high = high_risk / len(customers) * 100 if len(customers) else 0
g1.plotly_chart(_gauge(pct_high, "% High / Critical Risk", target=15, color=TEAL_DARK),
                use_container_width=True)

# Metric 2: % of screening hits that are resolved (cleared or escalated)
total_screening = len(screening)
resolved = int(screening["status"].isin(["Cleared - False Positive", "Escalated"]).sum())
pct_resolved = resolved / total_screening * 100 if total_screening else 0
g2.plotly_chart(_gauge(pct_resolved, "% Screening Hits Resolved", target=80, color=TEAL_MID),
                use_container_width=True)

# Metric 3: % of cases that have reached a terminal state
total_cases = len(cases)
closed_cases = int(cases["status"].str.contains("Closed").sum())
pct_closed = closed_cases / total_cases * 100 if total_cases else 0
g3.plotly_chart(_gauge(pct_closed, "% Cases Closed", target=60, color=TEAL_LIGHT),
                use_container_width=True)

# ==========================================================================
# CASE LOAD BY ANALYST
# ==========================================================================
section_title("Case Load by Analyst")
load_by_analyst = cases.groupby("assigned_analyst").size().sort_values(ascending=False)
fig4 = px.bar(
    x=load_by_analyst.index,
    y=load_by_analyst.values,
    labels={"x": "Analyst", "y": "Cases"},
    text=load_by_analyst.values,
)
fig4.update_traces(
    marker=dict(color=TEAL_DARK, line=dict(width=0.5, color=CARD_BORDER)),
    textposition="outside",
    textfont=dict(color=TEXT_MUTED, size=11),
)
fig4.update_layout(**chart_layout_2d(height=300))
st.plotly_chart(fig4, use_container_width=True)

st.info(
    "Use the sidebar to navigate the full lifecycle: **Customer Risk**, **Screening**, "
    "**Transaction Monitoring**, **Alerts & Triage**, **Case Management & SMR**, **UBO Network**, "
    "**Business KYC**, **New Client Onboarding**, **Periodic Review**, **Audit Trail**, and the "
    "**Process Map** for a full walk-through of every stage."
)
