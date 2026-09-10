import streamlit as st
import plotly.express as px

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill

st.set_page_config(page_title="Screening | AML Suite", page_icon="🔍", layout="wide")
inject_css()
page_header("PEP, Sanctions & Adverse Media Screening", "Watchlist match review and disposition queue.", "SCREENING")

data = load_all()
customers, screening = data["customers"], data["screening"]

merged = screening.merge(customers[["customer_id", "name", "risk_level", "country"]], on="customer_id", how="left")

with st.sidebar:
    st.subheader("Filters")
    match_types = st.multiselect("Match Type", sorted(merged["match_type"].unique()))
    statuses = st.multiselect("Status", sorted(merged["status"].unique()))
    min_score = st.slider("Minimum match score", 0, 100, 0)

df = merged.copy()
if match_types:
    df = df[df["match_type"].isin(match_types)]
if statuses:
    df = df[df["status"].isin(statuses)]
df = df[df["match_score"] >= min_score]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Hits", f"{len(merged):,}")
c2.metric("Open / Under Review", int(merged["status"].isin(["Open", "Under Review"]).sum()))
c3.metric("Escalated", int((merged["status"] == "Escalated").sum()))
c4.metric("Cleared (False Positive)", int(merged["status"].str.contains("Cleared").sum()))

section_title("Hits by Type and Status")
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(df, names="match_type", hole=0.5,
                 color="match_type",
                 color_discrete_map={"PEP": "#60A5FA", "Sanctions": "#F87171", "Adverse Media": "#FBBF24"})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    status_counts = df["status"].value_counts()
    fig2 = px.bar(x=status_counts.index, y=status_counts.values, labels={"x": "Status", "y": "Count"})
    fig2.update_traces(marker_color="#2DD4BF")
    fig2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig2, use_container_width=True)

section_title(f"Alert Queue ({len(df):,} results)")
show = df.sort_values("match_score", ascending=False).copy()
show["Risk"] = show["risk_level"].apply(risk_pill)
status_pill_map = {
    "Open": '<span class="pill pill-high">Open</span>',
    "Under Review": '<span class="pill pill-medium">Under Review</span>',
    "Escalated": '<span class="pill pill-critical">Escalated</span>',
    "Cleared - False Positive": '<span class="pill pill-low">Cleared</span>',
}
show["Status"] = show["status"].map(status_pill_map).fillna(show["status"])
display = show[["screening_id", "customer_id", "name", "match_type", "match_detail", "list_source",
                 "match_score", "Risk", "Status", "screened_date"]]
display = display.rename(columns={
    "screening_id": "Alert ID", "customer_id": "Customer ID", "name": "Name", "match_type": "Type",
    "match_detail": "Detail", "list_source": "Source", "match_score": "Score", "screened_date": "Screened",
})
display["Screened"] = display["Screened"].dt.strftime("%d %b %Y")
st.write(display.to_html(escape=False, index=False), unsafe_allow_html=True)
