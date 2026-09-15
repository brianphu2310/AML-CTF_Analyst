import streamlit as st
import pandas as pd

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill, grouped_bar3d_chart, RISK_COLOR_MAP

st.set_page_config(page_title="Customer Risk | AML Suite", layout="wide")
inject_css()
page_header("Customer Risk Rating", "Ongoing risk-based assessment across the customer book.", "CUSTOMER RISK")

data = load_all()
customers = data["customers"]

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
    mask = df["name"].str.contains(search, case=False) | df["customer_id"].str.contains(search, case=False)
    df = df[mask]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Filtered Customers", f"{len(df):,}")
c2.metric("Avg Risk Score", f"{df['risk_score'].mean():.1f}" if len(df) else "-")
c3.metric("High/Critical", int(df["risk_level"].isin(["High", "Critical"]).sum()))
c4.metric("Dormant/Closed", int(df["status"].isin(["Dormant", "Closed"]).sum()))

section_title("Risk Score Distribution")
st.caption("Drag to rotate, scroll to zoom. Each bin is broken down by risk level.")
if df.empty:
    st.info("No customers match the current filters.")
else:
    bin_edges = list(range(0, 101, 10))
    bin_labels = [f"{a}-{b}" for a, b in zip(bin_edges[:-1], bin_edges[1:])]
    binned = df.copy()
    binned["score_bin"] = pd.cut(binned["risk_score"], bins=bin_edges, labels=bin_labels, include_lowest=True)
    pivot = binned.groupby(["score_bin", "risk_level"]).size().unstack(fill_value=0)
    for lvl in ["Low", "Medium", "High", "Critical"]:
        if lvl not in pivot.columns:
            pivot[lvl] = 0
    pivot = pivot.reindex(bin_labels).fillna(0)

    fig = grouped_bar3d_chart(
        categories=bin_labels,
        series={lvl: pivot[lvl].tolist() for lvl in ["Low", "Medium", "High", "Critical"]},
        colors=RISK_COLOR_MAP,
        z_title="Customers",
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

section_title(f"Customer Register ({len(df):,} results)")
show = df.sort_values("risk_score", ascending=False).copy()
show["Risk"] = show["risk_level"].apply(risk_pill)
show_display = show[["customer_id", "name", "customer_type", "industry", "country", "risk_score", "Risk", "status", "onboarding_date"]]
show_display = show_display.rename(columns={
    "customer_id": "ID", "name": "Name", "customer_type": "Type", "industry": "Industry",
    "country": "Country", "risk_score": "Score", "status": "Status", "onboarding_date": "Onboarded",
})
show_display["Onboarded"] = show_display["Onboarded"].dt.strftime("%d %b %Y")

st.write(
    show_display.to_html(escape=False, index=False),
    unsafe_allow_html=True,
)

st.download_button(
    "Download filtered list (CSV)",
    df.to_csv(index=False).encode(),
    file_name="customer_risk_export.csv",
    mime="text/csv",
)
