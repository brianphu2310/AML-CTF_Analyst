import streamlit as st
import pandas as pd
import plotly.express as px

from db_utils import load_all
from theme import inject_css, page_header, kpi_card, section_title

st.set_page_config(page_title="AML Compliance Suite", page_icon="🛡️", layout="wide")
inject_css()

data = load_all()
customers, transactions, screening, cases = (
    data["customers"], data["transactions"], data["screening"], data["cases"]
)

page_header(
    "AML Compliance Suite",
    "Customer risk, screening, transaction monitoring, case management and UBO oversight - in one workspace.",
    badge="DEMO DATA" ,
)

# ---------------------------------------------------------------- KPI ROW
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    kpi_card("Total Customers", f"{len(customers):,}", f"{(customers['status']=='Active').sum()} active")
with c2:
    high_risk = customers[customers["risk_level"].isin(["High", "Critical"])].shape[0]
    kpi_card("High / Critical Risk", f"{high_risk:,}", f"{high_risk/len(customers)*100:.1f}% of book", "#B5541F")
with c3:
    open_hits = screening[screening["status"].isin(["Open", "Escalated", "Under Review"])].shape[0]
    kpi_card("Open Screening Alerts", f"{open_hits:,}", f"{screening.shape[0]} total hits", "#8A6D1D")
with c4:
    open_cases = cases[~cases["status"].str.contains("Closed")].shape[0]
    kpi_card("Active Cases", f"{open_cases:,}", f"{cases.shape[0]} total this period", "#2A4E73")
with c5:
    pending_smr = cases[cases["status"] == "Pending SMR Lodgement"].shape[0]
    kpi_card("Pending SMR Lodgement", f"{pending_smr:,}", "within statutory 3-day window", "#1F6F50")

# ---------------------------------------------------------------- CHARTS
section_title("Portfolio Risk Distribution")
col1, col2 = st.columns([1.1, 1])

with col1:
    risk_counts = customers["risk_level"].value_counts().reindex(["Low", "Medium", "High", "Critical"]).fillna(0)
    fig = px.bar(
        x=risk_counts.index, y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map={"Low": "#1F6F50", "Medium": "#8A6D1D", "High": "#B5541F", "Critical": "#7A1E1E"},
        labels={"x": "Risk Level", "y": "Customers"},
    )
    fig.update_layout(
        showlegend=False, template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=340,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    industry_risk = customers.groupby("industry")["risk_score"].mean().sort_values(ascending=True).tail(8)
    fig2 = px.bar(
        x=industry_risk.values, y=industry_risk.index, orientation="h",
        labels={"x": "Avg Risk Score", "y": ""},
        color=industry_risk.values, color_continuous_scale=["#1F6F50", "#8A6D1D", "#B5541F"],
    )
    fig2.update_layout(
        template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, margin=dict(t=10, b=10, l=10, r=10), height=340,
    )
    st.plotly_chart(fig2, use_container_width=True)

section_title("Transaction Volume Trend (last 90 days)")
recent = transactions[transactions["txn_date"] >= transactions["txn_date"].max() - pd.Timedelta(days=90)]
daily = recent.groupby([recent["txn_date"].dt.date, "direction"])["amount"].sum().reset_index()
fig3 = px.area(
    daily, x="txn_date", y="amount", color="direction",
    color_discrete_map={"Inbound": "#1E3A5F", "Outbound": "#2A4E73"},
    labels={"txn_date": "Date", "amount": "Total Amount (AUD)"},
)
fig3.update_layout(
    template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=10, b=10, l=10, r=10), height=320, legend_title_text="",
)
st.plotly_chart(fig3, use_container_width=True)

section_title("Case Load by Analyst")
load_by_analyst = cases.groupby("assigned_analyst").size().sort_values(ascending=False)
fig4 = px.bar(x=load_by_analyst.index, y=load_by_analyst.values, labels={"x": "Analyst", "y": "Cases"})
fig4.update_traces(marker_color="#1E3A5F")
fig4.update_layout(
    template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=10, b=10, l=10, r=10), height=300,
)
st.plotly_chart(fig4, use_container_width=True)

st.info(
    "Use the sidebar to navigate the full lifecycle: **Customer Risk**, **Screening**, "
    "**Transaction Monitoring**, **Alerts & Triage**, **Case Management & SMR**, **UBO Network**, "
    "**Business KYC**, **New Client Onboarding**, **Periodic Review**, **Audit Trail**, and the "
    "**Process Map** for a full walk-through of every stage.",
    icon="🧭",
)
