import streamlit as st
import pandas as pd
import plotly.express as px

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill
from workflow_utils import init_state, log_audit, ALERT_DISPOSITIONS, CASE_STATUSES

st.set_page_config(page_title="Alerts & Triage | AML Suite", page_icon="🚨", layout="wide")
inject_css()
page_header(
    "Alert Generation & Triage",
    "Unified queue of watchlist-screening hits and transaction-monitoring detections awaiting analyst disposition.",
    "ALERTS",
)

data = load_all()
customers, transactions, cases = data["customers"], data["transactions"], data["cases"]

alerts = init_state("alerts_live", lambda: data["alerts"])
cases_live = init_state("cases_live", lambda: data["cases"])

# ---------------------------------------------------------------- FILTERS
with st.sidebar:
    st.subheader("Filters")
    sources = st.multiselect("Source", sorted(alerts["source"].unique()))
    severities = st.multiselect("Severity", ["Low", "Medium", "High", "Critical"])
    dispositions = st.multiselect("Disposition", ALERT_DISPOSITIONS)

df = alerts.copy()
if sources:
    df = df[df["source"].isin(sources)]
if severities:
    df = df[df["severity"].isin(severities)]
if dispositions:
    df = df[df["disposition"].isin(dispositions)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Alerts", f"{len(alerts):,}")
c2.metric("New / Untriaged", int((alerts["disposition"] == "New").sum()))
c3.metric("Requires Investigation", int((alerts["disposition"] == "Requires Investigation").sum()))
c4.metric("Escalated to Case", int((alerts["disposition"] == "Escalated to Case").sum()))

section_title("Alerts by Source and Disposition")
col1, col2 = st.columns(2)
with col1:
    src_counts = alerts["source"].value_counts()
    fig = px.pie(names=src_counts.index, values=src_counts.values, hole=0.5,
                 color=src_counts.index,
                 color_discrete_map={"Watchlist Screening": "#2A4E73", "Transaction Monitoring": "#9C7A34"})
    fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=10, b=10, l=10, r=10), height=300)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    disp_counts = alerts["disposition"].value_counts().reindex(ALERT_DISPOSITIONS).fillna(0)
    fig2 = px.bar(x=disp_counts.index, y=disp_counts.values, labels={"x": "Disposition", "y": "Alerts"})
    fig2.update_traces(marker_color="#1E3A5F")
    fig2.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=10, b=10, l=10, r=10), height=300)
    st.plotly_chart(fig2, use_container_width=True)

section_title(f"Alert Queue ({len(df):,} results)")
disp_pill_map = {
    "New": '<span class="pill pill-high">New</span>',
    "False Positive": '<span class="pill pill-low">False Positive</span>',
    "Requires Investigation": '<span class="pill pill-medium">Requires Investigation</span>',
    "Escalated to Case": '<span class="pill pill-critical">Escalated to Case</span>',
}
show = df.sort_values(["disposition", "generated_date"], ascending=[True, False]).copy()
show["Disposition"] = show["disposition"].map(disp_pill_map)
show["Severity"] = show["severity"].apply(risk_pill)
disp_df = show[["alert_id", "customer_id", "name", "source", "alert_type", "detail", "Severity",
                 "Disposition", "generated_date"]]
disp_df = disp_df.rename(columns={
    "alert_id": "Alert ID", "customer_id": "Customer ID", "name": "Name", "source": "Source",
    "alert_type": "Type", "detail": "Detail", "generated_date": "Generated",
})
disp_df["Generated"] = pd.to_datetime(disp_df["Generated"]).dt.strftime("%d %b %Y")
st.write(disp_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()
section_title("Triage an Alert")
st.caption(
    "Every AML alert must be reviewed by an analyst and dispositioned as a false positive, sent for "
    "further investigation, or escalated to open a formal case."
)

if df.empty:
    st.warning("No alerts match the current filters.")
else:
    labels = {f"{r.alert_id} - {r.name} ({r.alert_type})": r.alert_id for r in df.itertuples()}
    chosen = st.selectbox("Select an alert", list(labels.keys()))
    alert_id = labels[chosen]
    alert_row = alerts[alerts["alert_id"] == alert_id].iloc[0]

    colA, colB = st.columns([1.3, 1])
    with colA:
        st.markdown(
            f"**Customer:** {alert_row['name']} ({alert_row['customer_id']})  \n"
            f"**Source:** {alert_row['source']}  \n"
            f"**Type:** {alert_row['alert_type']}  \n"
            f"**Severity:** {alert_row['severity']}  \n"
            f"**Detail:** {alert_row['detail']}"
        )
        note = st.text_area("Analyst note (optional)", placeholder="Rationale for this disposition...")

    with colB:
        new_disposition = st.radio("Set disposition", ALERT_DISPOSITIONS[1:], horizontal=False)
        apply_btn = st.button("Apply Disposition", type="primary", use_container_width=True)

    if apply_btn:
        idx = st.session_state["alerts_live"].index[
            st.session_state["alerts_live"]["alert_id"] == alert_id
        ]
        st.session_state["alerts_live"].loc[idx, "disposition"] = new_disposition
        log_audit(
            action=f"Alert Triaged: {new_disposition}",
            entity_type="Alert", entity_id=alert_id,
            detail=f"{alert_row['source']} alert on {alert_row['customer_id']} set to '{new_disposition}'."
                   + (f" Note: {note}" if note else ""),
        )

        if new_disposition == "Escalated to Case":
            existing = st.session_state["cases_live"]
            if not (existing["customer_id"] == alert_row["customer_id"]).any() or True:
                new_case_id = f"CASE{len(existing) + 1:04d}"
                new_row = {
                    "case_id": new_case_id, "customer_id": alert_row["customer_id"],
                    "opened_date": pd.Timestamp.today().normalize(),
                    "priority": "Critical" if alert_row["severity"] == "Critical" else "High",
                    "status": "Open", "assigned_analyst": "Unassigned", "typology": alert_row["alert_type"],
                    "escalated_to": "", "sof_review_notes": "", "senior_decision": "",
                    "smr_reference": "", "smr_submitted_date": pd.NaT,
                    "next_review_date": pd.Timestamp.today().normalize() + pd.DateOffset(months=6),
                }
                st.session_state["cases_live"] = pd.concat(
                    [existing, pd.DataFrame([new_row])], ignore_index=True
                )
                log_audit(
                    action="Case Opened", entity_type="Case", entity_id=new_case_id,
                    detail=f"Case opened from alert {alert_id} for {alert_row['customer_id']} "
                           f"({alert_row['alert_type']}).",
                )
                st.success(f"Alert escalated - new case **{new_case_id}** opened. "
                           "Continue the investigation on the Case Management & SMR page.")
        else:
            st.success(f"Alert {alert_id} set to '{new_disposition}'.")
        st.rerun()
