"""
AML/KYC Transaction Monitoring Intelligence — Home / Overview page.

Run with:
    streamlit run Home.py

This is a MULTIPAGE app. Additional pages live in the pages/ folder and
will appear automatically in the sidebar:
    1_Customer_Risk.py
    2_Screening.py
    3_Transaction_Monitoring.py
    4_Case_Management_SAR.py
"""

import streamlit as st
import plotly.express as px
from db_utils import run_query, RISK_SCORE_SQL, SCREENING_DETAIL_SQL

st.set_page_config(
    page_title="AML/KYC Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AML / KYC Transaction Monitoring Intelligence")
st.caption(
    "Synthetic data portfolio project — end-to-end AML pipeline: "
    "customer onboarding, UBO/beneficial ownership, PEP/Sanctions/Adverse "
    "Media screening, transaction monitoring, and case management."
)

try:
    risk_df = run_query(RISK_SCORE_SQL)
    screening_df = run_query(SCREENING_DETAIL_SQL)
except Exception as e:
    st.error(
        "Could not connect to the database. Check DB_CONFIG in db_utils.py "
        f"(host/port/dbname/user/password).\n\nDetails: {e}"
    )
    st.stop()

# ------------------------------------------------------------------
# KPI ROW
# ------------------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", len(risk_df))
col2.metric("Critical Risk (score = 4)", int((risk_df["risk_score"] == 4).sum()))
col3.metric("Elevated Risk (score ≥ 2)", int((risk_df["risk_score"] >= 2).sum()))
col4.metric("Any Screening Hit", int((risk_df["screening_hit"] == 1).sum()))
col5.metric(
    "Confirmed Matches",
    int((screening_df["status"] == "Confirmed Match").sum()),
)

st.divider()

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Risk Score Distribution Across Customer Base")
    dist = risk_df["risk_score"].value_counts().sort_index().reset_index()
    dist.columns = ["risk_score", "count"]
    fig = px.bar(
        dist, x="risk_score", y="count", text="count",
        labels={"risk_score": "Composite Risk Score (0–4)", "count": "Customers"},
        color="risk_score",
        color_continuous_scale=["#2ecc71", "#f1c40f", "#e67e22", "#c0392b", "#7b241c"],
    )
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Screening Outcomes")
    outcome_counts = screening_df["status"].value_counts().reset_index()
    outcome_counts.columns = ["status", "count"]
    fig2 = px.pie(
        outcome_counts, names="status", values="count", hole=0.5,
        color="status",
        color_discrete_map={
            "Clear": "#2ecc71",
            "Potential Match": "#f39c12",
            "Confirmed Match": "#c0392b",
        },
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.markdown(
    """
    ### How to use this dashboard
    Use the sidebar to navigate:
    - **Customer Risk** — full risk-scored customer list with filters
    - **Screening** — PEP / Sanctions / Adverse Media results by customer
    - **Transaction Monitoring** — structuring, rapid movement, high-risk wires, per-customer timelines
    - **Case Management & SAR** — select a flagged customer and generate a SAR-style case narrative,
      downloadable as `.txt` or `.docx`
    """
)

st.caption("All data in this dashboard is synthetic and generated for portfolio demonstration purposes only.")
