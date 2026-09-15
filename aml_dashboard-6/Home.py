"""
Home.py
Portfolio-level overview of the AML Compliance Suite.

Executive KPI row, portfolio risk distribution, transaction volume trend,
case load by analyst, customer lifecycle waterfall, and target gauges.

v4 (TEAL / CREAM / BROWN / WHITE): warm light theme from theme.py. Every
bar chart now gets a genuine "3D box" look via apply_3d_bar_caps() (a
lighter lid strip on top of / at the tip of each bar simulating a
top-down light source) instead of a single flat fill color, and the
transaction area chart uses a real vertical gradient fill
(apply_gradient_fill) rather than one translucent color. All charts keep
unified hover + spike lines, a visible zoom/pan/reset modebar, legend
click-to-isolate, and smooth transitions on re-render.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from db_utils import load_all
from theme import (
    inject_css, page_header, kpi_card, section_title, section_toolbar,
    chart_layout_2d, chart_layout_3d, chart_color_sequence,
    teal_gradient, brown_gradient, enable_rich_interaction,
    apply_3d_bar_caps, apply_gradient_fill, PLOTLY_CONFIG,
    RISK_COLOR_MAP,
    TEAL_DARK, TEAL_MID, TEAL_LIGHT, TEAL_PALE, TEAL_SOFT,
    BROWN_DARK, BROWN_MID, BROWN_LIGHT, BROWN_PALE,
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
industry_metric = section_toolbar(
    "Portfolio Risk Distribution",
    lambda: st.radio(
        "Industry metric", ["Avg Risk Score", "Customer Count"],
        index=0, horizontal=True, label_visibility="collapsed",
        key="industry_metric_toggle",
    ),
)

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
        marker=dict(line=dict(width=0.6, color="rgba(255,255,255,0.6)")),
        hovertemplate="<b>%{x}</b><br>%{y:,} customers<extra></extra>",
    )
    fig.update_layout(**chart_layout_2d(height=340))
    fig.update_layout(showlegend=False, hovermode="x")
    # Genuine 3D "beveled box" look: a lighter lid on top of each bar.
    fig = apply_3d_bar_caps(fig, risk_counts.index, risk_counts.values, orientation="v")
    fig = enable_rich_interaction(fig)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

with col2:
    if industry_metric == "Customer Count":
        industry_series = (
            customers.groupby("industry").size()
            .sort_values(ascending=True)
            .tail(8)
        )
        x_label = "Customers"
    else:
        industry_series = (
            customers.groupby("industry")["risk_score"]
            .mean()
            .sort_values(ascending=True)
            .tail(8)
        )
        x_label = "Avg Risk Score"

    # Harmonized teal ramp (pale -> deep accent with magnitude) so this
    # non-semantic chart still reads as part of the same color family.
    bar_colors = teal_gradient(industry_series.values)

    fig2 = px.bar(
        x=industry_series.values,
        y=industry_series.index,
        orientation="h",
        labels={"x": x_label, "y": ""},
    )
    fig2.update_traces(
        marker=dict(color=bar_colors, line=dict(width=0.6, color="rgba(255,255,255,0.6)")),
        text=[f"{v:,.0f}" if industry_metric == "Customer Count" else f"{v:.1f}"
              for v in industry_series.values],
        textposition="outside",
        textfont=dict(color=TEXT_MUTED, size=11),
        hovertemplate="<b>%{y}</b><br>" + x_label + ": %{x:,.1f}<extra></extra>",
    )
    fig2.update_layout(**chart_layout_2d(height=340))
    fig2.update_layout(hovermode="y")
    # 3D cap at the tip of each horizontal bar.
    fig2 = apply_3d_bar_caps(fig2, industry_series.values, industry_series.index, orientation="h")
    fig2 = enable_rich_interaction(fig2)
    st.plotly_chart(fig2, use_container_width=True, config=PLOTLY_CONFIG)

# ==========================================================================
# TRANSACTION VOLUME TREND
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
    .reset_index()
)
fig3 = px.area(
    daily,
    x="txn_date",
    y="amount",
    color="direction",
    color_discrete_map={"Inbound": TEAL_DARK, "Outbound": BROWN_MID},
    labels={"txn_date": "Date", "amount": "Total Amount (AUD)"},
)
fig3.update_traces(
    line=dict(width=2.2),
    hovertemplate="%{x|%d %b %Y}<br>$%{y:,.0f}<extra></extra>",
)
fig3.update_layout(**chart_layout_2d(height=320))
# Genuine vertical gradient fills — deep teal fading to pale near the
# baseline for Inbound, deep brown fading to cream for Outbound — instead
# of one flat translucent color.
fig3 = apply_gradient_fill(fig3, top_color="rgba(31,111,111,0.55)",
                            bottom_color="rgba(31,111,111,0.03)", trace_name="Inbound")
fig3 = apply_gradient_fill(fig3, top_color="rgba(107,74,50,0.45)",
                            bottom_color="rgba(107,74,50,0.03)", trace_name="Outbound")
fig3.update_layout(
    xaxis=dict(rangeslider=dict(visible=True, thickness=0.06,
                                 bgcolor="rgba(107,74,50,0.05)",
                                 bordercolor=CARD_BORDER, borderwidth=1)),
)
fig3 = enable_rich_interaction(fig3)
st.plotly_chart(fig3, use_container_width=True, config=PLOTLY_CONFIG)
st.caption(f"Showing the trailing {window_label.lower()} of transaction activity. Drag the range slider or scroll to zoom.")

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
        increasing=dict(marker=dict(color=TEAL_DARK, line=dict(width=0.6, color="rgba(255,255,255,0.6)"))),
        decreasing=dict(marker=dict(color=CRITICAL, line=dict(width=0.6, color="rgba(255,255,255,0.6)"))),
        totals=dict(marker=dict(color=BROWN_MID, line=dict(width=0.6, color="rgba(255,255,255,0.6)"))),
        hovertemplate="<b>%{x}</b><br>%{y:+,}<extra></extra>",
    )
)
fig_wf.update_layout(**chart_layout_2d(height=380))
fig_wf.update_layout(hovermode="x")
fig_wf = enable_rich_interaction(fig_wf, hover_glow=False)
st.plotly_chart(fig_wf, use_container_width=True, config=PLOTLY_CONFIG)

# ==========================================================================
# TARGET GAUGES
# ==========================================================================
section_title("Compliance Health Gauges")

g1, g2, g3 = st.columns(3)


def _gauge(value, title, target, color, suffix="%"):
    """Small radial gauge with a glow-edged bar and a target threshold line."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": suffix, "font": {"color": BROWN_DARK, "size": 30,
                                               "family": "Source Serif 4, Georgia, serif"}},
            title={"text": title, "font": {"color": TEXT_MUTED, "size": 12}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": TEXT_MUTED,
                    "tickfont": {"color": TEXT_MUTED, "size": 10},
                },
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.6)",
                "borderwidth": 1,
                "bordercolor": CARD_BORDER,
                "steps": [
                    {"range": [0, 40], "color": "rgba(139,94,60,0.08)"},
                    {"range": [40, 70], "color": "rgba(139,94,60,0.14)"},
                    {"range": [70, 100], "color": "rgba(139,94,60,0.20)"},
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
        transition=dict(duration=450, easing="cubic-in-out"),
    )
    return fig


# Metric 1: % of book flagged at high/critical risk
pct_high = high_risk / len(customers) * 100 if len(customers) else 0
g1.plotly_chart(_gauge(pct_high, "% High / Critical Risk", target=15, color=TEAL_DARK),
                use_container_width=True, config=PLOTLY_CONFIG)

# Metric 2: % of screening hits that are resolved (cleared or escalated)
total_screening = len(screening)
resolved = int(screening["status"].isin(["Cleared - False Positive", "Escalated"]).sum())
pct_resolved = resolved / total_screening * 100 if total_screening else 0
g2.plotly_chart(_gauge(pct_resolved, "% Screening Hits Resolved", target=80, color=BROWN_MID),
                use_container_width=True, config=PLOTLY_CONFIG)

# Metric 3: % of cases that have reached a terminal state
total_cases = len(cases)
closed_cases = int(cases["status"].str.contains("Closed").sum())
pct_closed = closed_cases / total_cases * 100 if total_cases else 0
g3.plotly_chart(_gauge(pct_closed, "% Cases Closed", target=60, color=LOW),
                use_container_width=True, config=PLOTLY_CONFIG)

# ==========================================================================
# CASE LOAD BY ANALYST
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
if sort_mode == "By Analyst Name":
    load_by_analyst = load_by_analyst.sort_index()
else:
    load_by_analyst = load_by_analyst.sort_values(ascending=False)

fig4 = px.bar(
    x=load_by_analyst.index,
    y=load_by_analyst.values,
    labels={"x": "Analyst", "y": "Cases"},
    text=load_by_analyst.values,
)
fig4.update_traces(
    marker=dict(color=brown_gradient(load_by_analyst.values), line=dict(width=0.6, color="rgba(255,255,255,0.6)")),
    textposition="outside",
    textfont=dict(color=TEXT_MUTED, size=11),
    hovertemplate="<b>%{x}</b><br>%{y:,} cases<extra></extra>",
)
fig4.update_layout(**chart_layout_2d(height=300))
fig4.update_layout(hovermode="x")
fig4 = apply_3d_bar_caps(fig4, load_by_analyst.index, load_by_analyst.values, orientation="v")
fig4 = enable_rich_interaction(fig4)
st.plotly_chart(fig4, use_container_width=True, config=PLOTLY_CONFIG)

st.info(
    "Use the sidebar to navigate the full lifecycle: **Customer Risk**, **Screening**, "
    "**Transaction Monitoring**, **Alerts & Triage**, **Case Management & SMR**, **UBO Network**, "
    "**Business KYC**, **New Client Onboarding**, **Periodic Review**, **Audit Trail**, and the "
    "**Process Map** for a full walk-through of every stage."
)
