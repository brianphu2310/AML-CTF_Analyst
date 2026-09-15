"""
Home.py
Portfolio-level overview of the AML Compliance Suite.

v4: teal / cream / brown theme. Every chart is real 3D geometry from
theme.py's 3D chart engine (Mesh3d extruded bars, a Surface ribbon for
the trend, a connected 3D waterfall, and 3D target bars in place of
flat gauges) - each one draggable to rotate, scroll to zoom, and
hoverable for exact values. Every section leads with its interactive
control in a toolbar row above the chart. No icons anywhere.
"""

import streamlit as st
import pandas as pd

from db_utils import load_all
from theme import (
    inject_css, page_header, kpi_card, section_title, section_toolbar,
    bar3d_chart, ribbon3d_chart, waterfall3d_chart, target_bar3d,
    teal_gradient, RISK_COLOR_MAP,
    TEAL_DARK, TEAL_MID, TEAL_LIGHT, BROWN_MID,
    CRITICAL, HIGH, MEDIUM, LOW, INFO,
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
# PORTFOLIO RISK DISTRIBUTION  +  INDUSTRY RISK  (3D bar charts)
# ==========================================================================
industry_metric = section_toolbar(
    "Portfolio Risk Distribution",
    lambda: st.radio(
        "Industry metric", ["Avg Risk Score", "Customer Count"],
        index=0, horizontal=True, label_visibility="collapsed",
        key="industry_metric_toggle",
    ),
)
st.caption("Drag to rotate, scroll to zoom, hover any bar for its exact value.")

col1, col2 = st.columns([1.1, 1])

with col1:
    risk_counts = (
        customers["risk_level"]
        .value_counts()
        .reindex(["Low", "Medium", "High", "Critical"])
        .fillna(0)
    )
    fig = bar3d_chart(
        categories=list(risk_counts.index),
        values=list(risk_counts.values),
        colors=[RISK_COLOR_MAP[lvl] for lvl in risk_counts.index],
        z_title="Customers",
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if industry_metric == "Customer Count":
        industry_series = customers.groupby("industry").size().sort_values(ascending=False).head(8)
        fmt = lambda v: f"{v:,.0f}"
    else:
        industry_series = customers.groupby("industry")["risk_score"].mean().sort_values(ascending=False).head(8)
        fmt = lambda v: f"{v:.1f}"

    fig2 = bar3d_chart(
        categories=list(industry_series.index),
        values=list(industry_series.values),
        colors=teal_gradient(industry_series.values),
        value_fmt=fmt,
        z_title=industry_metric,
        height=380,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================================================
# TRANSACTION VOLUME TREND  (3D Surface ribbon)
# ==========================================================================
window_label = section_toolbar(
    "Transaction Volume Trend",
    lambda: st.radio(
        "Window", ["30D", "90D", "180D", "1Y"],
        index=1, horizontal=True, label_visibility="collapsed",
        key="txn_window_toggle",
    ),
)
window_days = {"30D": 30, "90D": 90, "180D": 180, "1Y": 365}[window_label]

recent = transactions[
    transactions["txn_date"] >= transactions["txn_date"].max() - pd.Timedelta(days=window_days)
].copy()
daily = (
    recent.groupby([recent["txn_date"].dt.date, "direction"])["amount"]
    .sum()
    .unstack(fill_value=0)
    .sort_index()
)
for col in ("Inbound", "Outbound"):
    if col not in daily.columns:
        daily[col] = 0.0

date_labels = [d.strftime("%d %b") for d in daily.index]
fig3 = ribbon3d_chart(
    x_labels=date_labels,
    series={"Inbound": daily["Inbound"].tolist(), "Outbound": daily["Outbound"].tolist()},
    z_title="Amount (AUD)",
    height=360,
)
st.plotly_chart(fig3, use_container_width=True)
st.caption(f"Showing the trailing {window_label.lower()} of transaction activity. Drag to rotate the surface.")

# ==========================================================================
# CUSTOMER LIFECYCLE WATERFALL  (3D connected waterfall)
# ==========================================================================
section_title("Customer Lifecycle Waterfall")
st.caption(
    "From onboarding through to case closure / SMR lodgement - how the current book has moved "
    "through each stage of the AML lifecycle. Drag to rotate."
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
    "Total Customers", "Active", "High/Critical", "Screened",
    "Case Opened", "Escalated", "SMR Lodged", "Closed",
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

fig_wf = waterfall3d_chart(
    labels=wf_labels,
    values=wf_values,
    height=400,
    colors={"increasing": TEAL_DARK, "decreasing": HIGH, "total": TEAL_LIGHT},
)
st.plotly_chart(fig_wf, use_container_width=True)

# ==========================================================================
# COMPLIANCE HEALTH — 3D TARGET BARS (replaces flat 2D gauges)
# ==========================================================================
section_title("Compliance Health Targets")
st.caption("Each bar's height is the current value; the translucent plate marks the target.")

g1, g2, g3 = st.columns(3)

pct_high = high_risk / len(customers) * 100 if len(customers) else 0
g1.plotly_chart(
    target_bar3d(pct_high, target=15, label="% High / Critical Risk", color=TEAL_DARK, height=280),
    use_container_width=True,
)

total_screening = len(screening)
resolved = int(screening["status"].isin(["Cleared - False Positive", "Escalated"]).sum())
pct_resolved = resolved / total_screening * 100 if total_screening else 0
g2.plotly_chart(
    target_bar3d(pct_resolved, target=80, label="% Screening Hits Resolved", color=BROWN_MID, height=280),
    use_container_width=True,
)

total_cases = len(cases)
closed_cases = int(cases["status"].str.contains("Closed").sum())
pct_closed = closed_cases / total_cases * 100 if total_cases else 0
g3.plotly_chart(
    target_bar3d(pct_closed, target=60, label="% Cases Closed", color=TEAL_LIGHT, height=280),
    use_container_width=True,
)

# ==========================================================================
# CASE LOAD BY ANALYST  (3D bar chart)
# ==========================================================================
sort_mode = section_toolbar(
    "Case Load by Analyst",
    lambda: st.radio(
        "Sort", ["By Case Count", "By Analyst Name"],
        index=0, horizontal=True, label_visibility="collapsed",
        key="case_load_sort_toggle",
    ),
)

load_by_analyst = cases.groupby("assigned_analyst").size()
load_by_analyst = (
    load_by_analyst.sort_index() if sort_mode == "By Analyst Name"
    else load_by_analyst.sort_values(ascending=False)
)

fig4 = bar3d_chart(
    categories=list(load_by_analyst.index),
    values=list(load_by_analyst.values),
    colors=teal_gradient(load_by_analyst.values),
    z_title="Cases",
    height=380,
)
st.plotly_chart(fig4, use_container_width=True)

st.info(
    "Use the sidebar to navigate the full lifecycle: **Customer Risk**, **Screening**, "
    "**Transaction Monitoring**, **Alerts & Triage**, **Case Management & SMR**, **UBO Network**, "
    "**Business KYC**, **New Client Onboarding**, **Periodic Review**, **Audit Trail**, and the "
    "**Process Map** for a full walk-through of every stage."
)

