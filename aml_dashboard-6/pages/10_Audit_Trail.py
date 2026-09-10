import streamlit as st
import pandas as pd
import plotly.express as px

from db_utils import load_all
from theme import inject_css, page_header, section_title
from workflow_utils import full_audit_log

st.set_page_config(page_title="Audit Trail | AML Suite", page_icon="📜", layout="wide")
inject_css()
page_header(
    "Record Keeping & Audit Trail",
    "Consolidated log of onboarding decisions, alert triage, investigations, escalations, SMR lodgement "
    "and periodic reviews - the evidentiary record of the AML/CTF Program in action.",
    "AUDIT TRAIL",
)

data = load_all()
log = full_audit_log(data["audit_log"])

with st.sidebar:
    st.subheader("Filters")
    entity_types = st.multiselect("Entity type", sorted(log["entity_type"].unique()))
    actors = st.multiselect("Actor", sorted(log["actor"].unique()))
    date_range = st.date_input(
        "Date range",
        value=(log["timestamp"].min().date(), log["timestamp"].max().date()),
    )
    search = st.text_input("Search action / detail")

df = log.copy()
if entity_types:
    df = df[df["entity_type"].isin(entity_types)]
if actors:
    df = df[df["actor"].isin(actors)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    df = df[(df["timestamp"].dt.date >= start) & (df["timestamp"].dt.date <= end)]
if search:
    mask = df["action"].str.contains(search, case=False, na=False) | df["detail"].str.contains(search, case=False, na=False)
    df = df[mask]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Log Entries", f"{len(log):,}")
c2.metric("Filtered Results", f"{len(df):,}")
c3.metric("Distinct Entities Touched", df["entity_id"].nunique())
c4.metric("This Session", len(st.session_state.get("audit_log_live", [])))

section_title("Activity by Entity Type")
counts = log["entity_type"].value_counts()
fig = px.bar(x=counts.index, y=counts.values, labels={"x": "Entity Type", "y": "Log Entries"})
fig.update_traces(marker_color="#1E3A5F")
fig.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   margin=dict(t=10, b=10, l=10, r=10), height=280)
st.plotly_chart(fig, use_container_width=True)

section_title(f"Audit Log ({len(df):,} entries)")
display = df.copy()
display["timestamp"] = display["timestamp"].dt.strftime("%d %b %Y %H:%M")
display = display.rename(columns={
    "timestamp": "Timestamp", "actor": "Actor", "action": "Action",
    "entity_type": "Entity Type", "entity_id": "Entity ID", "detail": "Detail",
})
st.dataframe(display[["Timestamp", "Actor", "Action", "Entity Type", "Entity ID", "Detail"]],
             use_container_width=True, hide_index=True, height=520)

st.download_button(
    "⬇️ Export filtered log (CSV)",
    df.to_csv(index=False).encode(),
    file_name="aml_audit_trail_export.csv",
    mime="text/csv",
)

st.caption(
    "This log satisfies the record-keeping expectation of an AML/CTF Program: every decision, escalation "
    "and report lodgement is timestamped, attributed and retrievable for regulator or internal audit review."
)
