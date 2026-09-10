"""
pages/1_Customer_Risk.py
Customer risk register with distribution histogram, industry risk heatmap,
3D risk scatter, and risk-level sunburst drill-down.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from db_utils import load_all
from theme import (
    inject_css, page_header, section_title, risk_pill,
    chart_layout_2d, chart_layout_3d, chart_color_sequence,
    RISK_COLOR_MAP,
    TEAL_DARK, TEAL_MID, TEAL_LIGHT, TEAL_PALE, TEAL_SOFT,
    CRITICAL, HIGH, MEDIUM, LOW, INFO,
    TEXT_PRIMARY, TEXT_MUTED, CARD_BORDER, CHART_GRID,
)

st.set_page_config(page_title="Customer Risk", layout="wide")
inject_css()
page_header(
    "Customer Risk Rating",
    "Ongoing risk-based assessment across the customer book.",
    "CUSTOMER RISK",
)

data = load_all()
customers = data["customers"]
transactions = data["transactions"]

# ==========================================================================
# SIDEBAR FILTERS
# ==========================================================================
with st.sidebar:
    st.subheader("Filters")
    industries = st.multiselect("Industry", sorted(customers["industry"].unique()))
    countries = st.multiselect("Country", sorted(customers["country"].unique()))
    levels = st.multiselect("Risk Level", ["Low", "Medium", "High", "Critical"])
    statuses = st.multiselect("Status", sorted(customers["status"].unique()))
    search = st.text_input("Search name / ID")

df = customers.copy()
if industries:
    df = df[df["industry"].isin(industries)]
if countries:
    df = df[df["country"].isin(countries)]
if levels:
    df = df[df["risk_level"].isin(levels)]
if statuses:
    df = df[df["status"].isin(statuses)]
if search:
    mask = df["name"].str.contains(search, case=False, na=False) | \
           df["customer_id"].str.contains(search, case=False, na=False)
    df = df[mask]

# ==========================================================================
# KPI ROW
# ==========================================================================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Filtered Customers", f"{len(df):,}")
c2.metric("Avg Risk Score", f"{df['risk_score'].mean():.1f}" if len(df) else "-")
c3.metric("High/Critical", int(df["risk_level"].isin(["High", "Critical"]).sum()))
c4.metric("Dormant/Closed", int(df["status"].isin(["Dormant", "Closed"]).sum()))

# ==========================================================================
# RISK SCORE HISTOGRAM
# ==========================================================================
section_title("Risk Score Distribution")
fig = px.histogram(
    df, x="risk_score", nbins=25, color="risk_level",
    color_discrete_map=RISK_COLOR_MAP,
)
fig.update_traces(marker=dict(line=dict(width=0.5, color=CARD_BORDER)))
fig.update_layout(**chart_layout_2d(height=300))
fig.update_layout(legend_title_text="", bargap=0.08)
st.plotly_chart(fig, use_container_width=True)

# ==========================================================================
# INDUSTRY × RISK HEATMAP  +  RISK LEVEL SUNBURST
# ==========================================================================
section_title("Portfolio Composition")
col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown("**Industry × Risk Level — Customer Count Heatmap**")
    pivot = (
        df.groupby(["industry", "risk_level"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["Low", "Medium", "High", "Critical"], fill_value=0)
    )
    fig_hm = px.imshow(
        pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        color_continuous_scale=[
            [0.0, "#F6F8FA"],
            [0.25, TEAL_SOFT],
            [0.5, TEAL_PALE],
            [0.75, TEAL_LIGHT],
            [1.0, TEAL_DARK],
        ],
        aspect="auto",
        text_auto=True,
    )
    fig_hm.update_traces(textfont=dict(size=11, color=TEXT_PRIMARY))
    fig_hm.update_layout(**chart_layout_2d(height=420))
    fig_hm.update_layout(coloraxis_showscale=False)
    fig_hm.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_hm, use_container_width=True)

with col2:
    st.markdown("**Risk Level → Industry → Customer — Sunburst**")
    sun_df = df.copy()
    sun_df["risk_level"] = pd.Categorical(
        sun_df["risk_level"], categories=["Low", "Medium", "High", "Critical"], ordered=True
    )
    fig_sb = px.sunburst(
        sun_df,
        path=["risk_level", "industry", "name"],
        color="risk_level",
        color_discrete_map=RISK_COLOR_MAP,
        maxdepth=2,
    )
    fig_sb.update_traces(
        textfont=dict(size=11, color=TEXT_PRIMARY),
        marker=dict(line=dict(width=0.5, color=CARD_BORDER)),
    )
    fig_sb.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=11),
        margin=dict(t=10, b=10, l=10, r=10),
        height=420,
    )
    st.plotly_chart(fig_sb, use_container_width=True)

# ==========================================================================
# 3D RISK SCATTER — risk_score × txn_count × total_amount
# ==========================================================================
section_title("3D Risk Landscape")
st.caption(
    "Each point is a customer. Axes: composite risk score (X), transaction count (Y), "
    "total transaction volume in AUD (Z). Colour encodes risk level."
)

txn_agg = (
    transactions.groupby("customer_id")
    .agg(txn_count=("txn_id", "count"), total_amount=("amount", "sum"))
    .reset_index()
)
scatter_df = df.merge(txn_agg, on="customer_id", how="left").fillna({"txn_count": 0, "total_amount": 0})

# Cap extreme outliers so axes stay readable
cap = scatter_df["total_amount"].quantile(0.98) if len(scatter_df) else 1
scatter_df["total_amount_capped"] = scatter_df["total_amount"].clip(upper=cap)

fig3d = px.scatter_3d(
    scatter_df,
    x="risk_score",
    y="txn_count",
    z="total_amount_capped",
    color="risk_level",
    color_discrete_map=RISK_COLOR_MAP,
    hover_data=["customer_id", "name", "industry", "country"],
    labels={
        "risk_score": "Risk Score",
        "txn_count": "Transaction Count",
        "total_amount_capped": "Total Amount (AUD, capped 98%)",
    },
    opacity=0.82,
)
fig3d.update_traces(marker=dict(size=4.5, line=dict(width=0.4, color="white")))
fig3d.update_layout(**chart_layout_3d(height=560))
st.plotly_chart(fig3d, use_container_width=True)

# ==========================================================================
# CUSTOMER REGISTER TABLE
# ==========================================================================
section_title(f"Customer Register ({len(df):,} results)")
show = df.sort_values("risk_score", ascending=False).copy()
show["Risk"] = show["risk_level"].apply(risk_pill)
show_display = show[[
    "customer_id", "name", "customer_type", "industry", "country",
    "risk_score", "Risk", "status", "onboarding_date",
]].rename(columns={
    "customer_id": "ID",
    "name": "Name",
    "customer_type": "Type",
    "industry": "Industry",
    "country": "Country",
    "risk_score": "Score",
    "status": "Status",
    "onboarding_date": "Onboarded",
})
show_display["Onboarded"] = show_display["Onboarded"].dt.strftime("%d %b %Y")

st.write(show_display.to_html(escape=False, index=False), unsafe_allow_html=True)

st.download_button(
    "Download filtered list (CSV)",
    df.to_csv(index=False).encode(),
    file_name="customer_risk_export.csv",
    mime="text/csv",
)
