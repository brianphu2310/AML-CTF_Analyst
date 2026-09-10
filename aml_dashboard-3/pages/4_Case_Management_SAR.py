import streamlit as st
import pandas as pd

from db_utils import load_all
from report_utils import build_smr, smr_to_docx_bytes
from theme import inject_css, page_header, section_title, risk_pill

st.set_page_config(page_title="Case Management & SMR | AML Suite", page_icon="🗂️", layout="wide")
inject_css()
page_header(
    "Case Management & SMR Drafting",
    "Investigation queue with one-click AUSTRAC-aligned Suspicious Matter Report generation.",
    "CASE MANAGEMENT",
)

data = load_all()
customers, transactions, screening, cases = (
    data["customers"], data["transactions"], data["screening"], data["cases"]
)

merged_cases = cases.merge(customers[["customer_id", "name", "risk_level", "risk_score", "country"]], on="customer_id")

with st.sidebar:
    st.subheader("Filters")
    priorities = st.multiselect("Priority", ["Critical", "High", "Medium"])
    statuses = st.multiselect("Status", sorted(merged_cases["status"].unique()))
    analysts = st.multiselect("Analyst", sorted(merged_cases["assigned_analyst"].unique()))
    min_risk = st.slider("Minimum customer risk score", 0, 100, 0)

df = merged_cases.copy()
if priorities:
    df = df[df["priority"].isin(priorities)]
if statuses:
    df = df[df["status"].isin(statuses)]
if analysts:
    df = df[df["assigned_analyst"].isin(analysts)]
df = df[df["risk_score"] >= min_risk]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Open Cases", int((~df["status"].str.contains("Closed")).sum()))
c2.metric("Critical Priority", int((df["priority"] == "Critical").sum()))
c3.metric("Pending SMR Lodgement", int((df["status"] == "Pending SMR Lodgement").sum()))
c4.metric("SMR Lodged (period)", int((df["status"] == "SMR Lodged").sum()))

section_title(f"Investigation Queue ({len(df):,} results)")
priority_pill = {
    "Critical": '<span class="pill pill-critical">Critical</span>',
    "High": '<span class="pill pill-high">High</span>',
    "Medium": '<span class="pill pill-medium">Medium</span>',
}
show = df.sort_values(["priority", "risk_score"], ascending=[True, False]).copy()
show["Priority"] = show["priority"].map(priority_pill)
show["Risk"] = show["risk_level"].apply(risk_pill)
display = show[["case_id", "customer_id", "name", "typology", "Priority", "Risk", "status", "assigned_analyst", "opened_date"]]
display = display.rename(columns={
    "case_id": "Case ID", "customer_id": "Customer ID", "name": "Name", "typology": "Typology",
    "status": "Status", "assigned_analyst": "Analyst", "opened_date": "Opened",
})
display["Opened"] = display["Opened"].dt.strftime("%d %b %Y")
st.write(display.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()
section_title("Generate AUSTRAC-Format Suspicious Matter Report")
st.caption(
    "Select a case to auto-analyse the customer's transaction history for structuring, rapid movement "
    "and high-risk corridor typologies, and draft a Grounds-for-Suspicion narrative in AUSTRAC's "
    "WHO / WHAT / WHEN / WHERE / HOW / WHY format."
)

if df.empty:
    st.warning("No cases match the current filters.")
else:
    case_labels = {
        f"{r.case_id} - {r.name} ({r.priority} priority, {r.typology})": r.case_id
        for r in df.itertuples()
    }
    chosen_label = st.selectbox("Select a case", list(case_labels.keys()))
    chosen_case_id = case_labels[chosen_label]
    case_row = df[df["case_id"] == chosen_case_id].iloc[0]
    customer_row = customers[customers["customer_id"] == case_row["customer_id"]].iloc[0]

    colA, colB = st.columns([1, 2])
    with colA:
        st.markdown(f"**Customer:** {customer_row['name']}  \n"
                    f"**ID:** {customer_row['customer_id']}  \n"
                    f"**Risk:** {customer_row['risk_level']} ({customer_row['risk_score']}/100)  \n"
                    f"**Country:** {customer_row['country']}  \n"
                    f"**Typology (case):** {case_row['typology']}")
        generate = st.button("🧾 Generate SMR Narrative", type="primary", use_container_width=True)

    if generate:
        with st.spinner("Analysing transaction history and drafting narrative..."):
            report = build_smr(customer_row, transactions, screening)
        st.session_state["current_smr"] = report

    if "current_smr" in st.session_state and st.session_state["current_smr"].customer["customer_id"] == customer_row["customer_id"]:
        report = st.session_state["current_smr"]
        with colB:
            if report.findings:
                st.success(f"{len(report.findings)} typology finding(s) detected and incorporated into the draft.")
                for f in report.findings:
                    st.markdown(f"- **{f.typology}** ({f.severity}): {f.summary}")
            else:
                st.info("No automated typology triggers found - narrative will contain placeholder fields "
                        "for manual completion.")

        st.text_area("SMR Draft (editable preview)", report.full_text(), height=480)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "⬇️ Download as .txt",
                report.full_text().encode(),
                file_name=f"{report.reference}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with dl2:
            docx_bytes = smr_to_docx_bytes(report)
            st.download_button(
                "⬇️ Download as .docx",
                docx_bytes,
                file_name=f"{report.reference}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

        st.warning(
            "This is a system-generated draft to accelerate case review. A qualified compliance officer / "
            "MLRO must verify all details, complete bracketed fields, and approve the report before it is "
            "lodged with AUSTRAC via AUSTRAC Online. Do not submit unedited system output.",
            icon="⚠️",
        )
