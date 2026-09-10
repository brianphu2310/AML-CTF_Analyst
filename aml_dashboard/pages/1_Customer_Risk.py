import streamlit as st
import plotly.express as px
from db_utils import run_query, RISK_SCORE_SQL

st.set_page_config(page_title="Customer Risk", page_icon="📊", layout="wide")
st.title("📊 Customer Risk Scoring")

risk_df = run_query(RISK_SCORE_SQL)

# ------------------------------------------------------------------
# FILTERS
# ------------------------------------------------------------------
st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum risk score", 0, 4, 0)
industries = st.sidebar.multiselect(
    "Industry", sorted(risk_df["industry"].dropna().unique().tolist())
)
countries = st.sidebar.multiselect(
    "Country", sorted(risk_df["country"].dropna().unique().tolist())
)
status_filter = st.sidebar.multiselect(
    "Customer status", sorted(risk_df["customer_status"].dropna().unique().tolist())
)

filtered = risk_df[risk_df["risk_score"] >= min_score]
if industries:
    filtered = filtered[filtered["industry"].isin(industries)]
if countries:
    filtered = filtered[filtered["country"].isin(countries)]
if status_filter:
    filtered = filtered[filtered["customer_status"].isin(status_filter)]

st.caption(f"Showing {len(filtered)} of {len(risk_df)} customers")

# ------------------------------------------------------------------
# SUMMARY CHARTS
# ------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Risk Score by Industry")
    by_industry = filtered.groupby("industry")["risk_score"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(by_industry, x="industry", y="risk_score", labels={"risk_score": "Avg. Risk Score"})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Flag Breakdown (Filtered Set)")
    flag_counts = {
        "Structuring": int(filtered["structuring"].sum()),
        "Rapid Movement": int(filtered["rapid_movement"].sum()),
        "High-Risk Country": int(filtered["high_risk_country"].sum()),
        "Screening Hit": int(filtered["screening_hit"].sum()),
    }
    fig2 = px.bar(
        x=list(flag_counts.keys()), y=list(flag_counts.values()),
        labels={"x": "Flag Type", "y": "Customers Flagged"},
        color=list(flag_counts.keys()),
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# FULL TABLE
# ------------------------------------------------------------------
st.subheader("Customer Risk Table")
display_cols = [
    "customer_id", "full_name", "customer_type", "country", "industry",
    "customer_status", "structuring", "rapid_movement", "high_risk_country",
    "screening_hit", "risk_score",
]
st.dataframe(
    filtered[display_cols].sort_values("risk_score", ascending=False),
    use_container_width=True,
    height=500,
)

csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
st.download_button("Download filtered results as CSV", csv, "customer_risk_filtered.csv", "text/csv")
