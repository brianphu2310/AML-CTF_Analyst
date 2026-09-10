import streamlit as st
import pandas as pd
import plotly.express as px

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill
from workflow_utils import init_state, log_audit, review_due_date

st.set_page_config(page_title="Periodic Review | AML Suite", page_icon="🔄", layout="wide")
inject_css()
page_header(
    "Periodic Review & Remediation",
    "Risk-based scheduled re-verification of KYC, risk rating and screening - Low 24mo / Medium 12mo / "
    "High 6mo / Critical 3mo.",
    "PERIODIC REVIEW",
)

data = load_all()
customers = data["customers"]
reviews_live = init_state("reviews_live", lambda: pd.DataFrame(columns=["customer_id", "last_review_date", "outcome"]))

df = customers[customers["status"] == "Active"].copy()
df["review_due"] = df.apply(lambda r: review_due_date(r["onboarding_date"], r["risk_level"]), axis=1)
today = pd.Timestamp.today().normalize()
df["days_until_due"] = (df["review_due"] - today).dt.days
df["review_state"] = df["days_until_due"].apply(
    lambda d: "Overdue" if d < 0 else "Due within 30 days" if d <= 30 else "Scheduled"
)

completed_ids = set(reviews_live["customer_id"]) if not reviews_live.empty else set()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Active Customers", f"{len(df):,}")
c2.metric("Overdue for Review", int((df["review_state"] == "Overdue").sum()))
c3.metric("Due within 30 Days", int((df["review_state"] == "Due within 30 days").sum()))
c4.metric("Completed This Session", len(completed_ids))

section_title("Review Schedule by Risk Level")
sched = df.groupby(["risk_level", "review_state"]).size().reset_index(name="count")
fig = px.bar(
    sched, x="risk_level", y="count", color="review_state",
    category_orders={"risk_level": ["Low", "Medium", "High", "Critical"]},
    color_discrete_map={"Overdue": "#7A1E1E", "Due within 30 days": "#B5541F", "Scheduled": "#1F6F50"},
    labels={"risk_level": "Risk Level", "count": "Customers"},
)
fig.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   margin=dict(t=10, b=10, l=10, r=10), height=320, legend_title_text="")
st.plotly_chart(fig, use_container_width=True)

with st.sidebar:
    st.subheader("Filters")
    state_filter = st.multiselect("Review state", ["Overdue", "Due within 30 days", "Scheduled"])
    level_filter = st.multiselect("Risk level", ["Low", "Medium", "High", "Critical"])

show = df.copy()
if state_filter:
    show = show[show["review_state"].isin(state_filter)]
if level_filter:
    show = show[show["risk_level"].isin(level_filter)]

section_title(f"Review Register ({len(show):,} results)")
show = show.sort_values("days_until_due").copy()
state_pill = {
    "Overdue": '<span class="pill pill-critical">Overdue</span>',
    "Due within 30 days": '<span class="pill pill-high">Due within 30 days</span>',
    "Scheduled": '<span class="pill pill-low">Scheduled</span>',
}
show["State"] = show["review_state"].map(state_pill)
show["Risk"] = show["risk_level"].apply(risk_pill)
disp = show[["customer_id", "name", "Risk", "review_due", "State"]].rename(columns={
    "customer_id": "ID", "name": "Name", "review_due": "Review Due",
})
disp["Review Due"] = pd.to_datetime(disp["Review Due"]).dt.strftime("%d %b %Y")
st.write(disp.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()
section_title("Complete a Periodic Review")
st.caption(
    "Remediate the customer file: reconfirm identity documents are current, re-run PEP/sanctions/adverse "
    "media screening, and reassess the risk rating against current activity."
)

if show.empty:
    st.info("No customers match the current filters.")
else:
    options = {f"{r.customer_id} - {r.name} ({r.review_state})": r.customer_id for r in show.itertuples()}
    choice = st.selectbox("Select a customer", list(options.keys()))
    cid = options[choice]
    cust = customers[customers["customer_id"] == cid].iloc[0]

    st.markdown(
        f"**Current risk rating:** {cust['risk_level']} ({cust['risk_score']}/100)  \n"
        f"**Industry / country:** {cust['industry']} / {cust['country']}"
    )
    remediation = st.multiselect(
        "Remediation checklist completed",
        ["Identity documents reconfirmed / re-verified", "Re-screened for PEP / Sanctions / Adverse Media",
         "Source of funds/wealth reconfirmed", "Beneficial ownership reconfirmed (business customers)",
         "Risk rating reassessed against current activity"],
    )
    outcome = st.radio("Review outcome", ["No change to risk rating", "Risk rating increased",
                                           "Risk rating decreased", "Refer for EDD / escalation"], horizontal=True)
    notes = st.text_area("Review notes")
    complete = st.button("✅ Mark Review Complete", type="primary")

    if complete:
        new_row = pd.DataFrame([{
            "customer_id": cid, "last_review_date": pd.Timestamp.today().normalize(), "outcome": outcome,
        }])
        st.session_state["reviews_live"] = pd.concat([reviews_live, new_row], ignore_index=True)
        log_audit(
            "Periodic Review Completed", "Customer", cid,
            f"Outcome: {outcome}. Checklist: {', '.join(remediation) if remediation else 'none recorded'}. "
            + (f"Notes: {notes}" if notes else ""),
        )
        st.success(f"Periodic review recorded for {cust['name']}.")
        st.rerun()
