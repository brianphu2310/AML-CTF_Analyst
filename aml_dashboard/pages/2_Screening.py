import streamlit as st
import plotly.express as px
from db_utils import run_query, SCREENING_DETAIL_SQL

st.set_page_config(page_title="Screening", page_icon="🔎", layout="wide")
st.title("🔎 PEP / Sanctions / Adverse Media Screening")

screening_df = run_query(SCREENING_DETAIL_SQL)

# ------------------------------------------------------------------
# FILTERS
# ------------------------------------------------------------------
st.sidebar.header("Filters")
type_filter = st.sidebar.multiselect(
    "Screening type", sorted(screening_df["screening_type"].unique().tolist())
)
status_filter = st.sidebar.multiselect(
    "Status", sorted(screening_df["status"].unique().tolist())
)

filtered = screening_df.copy()
if type_filter:
    filtered = filtered[filtered["screening_type"].isin(type_filter)]
if status_filter:
    filtered = filtered[filtered["status"].isin(status_filter)]

# ------------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Total Screening Records", len(screening_df))
c2.metric("Potential Matches", int((screening_df["status"] == "Potential Match").sum()))
c3.metric("Confirmed Matches", int((screening_df["status"] == "Confirmed Match").sum()))

st.divider()

c4, c5 = st.columns(2)
with c4:
    st.subheader("Outcomes by Screening Type")
    grouped = screening_df.groupby(["screening_type", "status"]).size().reset_index(name="count")
    fig = px.bar(
        grouped, x="screening_type", y="count", color="status", barmode="stack",
        color_discrete_map={
            "Clear": "#2ecc71",
            "Potential Match": "#f39c12",
            "Confirmed Match": "#c0392b",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

with c5:
    st.subheader("Overall Outcome Split")
    fig2 = px.pie(
        screening_df, names="status", hole=0.5,
        color="status",
        color_discrete_map={
            "Clear": "#2ecc71",
            "Potential Match": "#f39c12",
            "Confirmed Match": "#c0392b",
        },
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# DETAIL TABLE (non-Clear results highlighted first)
# ------------------------------------------------------------------
st.subheader("Screening Records")
st.caption("Potential/Confirmed matches are the ones requiring analyst review — sorted to the top.")

filtered = filtered.copy()
status_order = {"Confirmed Match": 0, "Potential Match": 1, "Clear": 2}
filtered["_sort"] = filtered["status"].map(status_order)
filtered = filtered.sort_values(["_sort", "customer_id"]).drop(columns="_sort")

st.dataframe(filtered, use_container_width=True, height=500)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered results as CSV", csv, "screening_filtered.csv", "text/csv")
