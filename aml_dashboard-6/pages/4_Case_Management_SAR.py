import streamlit as st
import pandas as pd

from db_utils import load_all
from report_utils import build_smr, smr_to_docx_bytes
from theme import inject_css, page_header, section_title, risk_pill
from workflow_utils import init_state, log_audit, CASE_STATUSES, SENIOR_DECISIONS, status_pill_html

st.set_page_config(page_title="Case Management & SMR | AML Suite", page_icon="🗂️", layout="wide")
inject_css()
page_header(
    "Case Management, Investigation & SMR",
    "Full investigation lifecycle: profile review -> SOF/SOW -> escalation -> senior decision -> "
    "SMR drafting -> AUSTRAC lodgement -> post-SMR monitoring.",
    "CASE MANAGEMENT",
)

data = load_all()
customers, transactions, screening = data["customers"], data["transactions"], data["screening"]
businesses, ubo, alerts = data["businesses"], data["ubo"], data["alerts"]

cases_live = init_state("cases_live", lambda: data["cases"])


def update_case(case_id: str, **fields):
    idx = st.session_state["cases_live"].index[st.session_state["cases_live"]["case_id"] == case_id]
    for k, v in fields.items():
        st.session_state["cases_live"].loc[idx, k] = v


merged_cases = cases_live.merge(
    customers[["customer_id", "name", "risk_level", "risk_score", "country", "customer_type"]],
    on="customer_id",
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["🗂️ Investigation Queue", "🔍 Investigation Workspace", "⬆️ Escalation & Senior Review",
     "🧾 SMR Assessment, Drafting & Submission"]
)

# ================================================================== TAB 1
with tab1:
    with st.sidebar:
        st.subheader("Queue Filters")
        priorities = st.multiselect("Priority", ["Critical", "High", "Medium"])
        statuses = st.multiselect("Status", CASE_STATUSES)
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

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Open Cases", int((~df["status"].str.contains("Closed")).sum()))
    c2.metric("Under Investigation", int((df["status"] == "Under Investigation").sum()))
    c3.metric("Escalated", int((df["status"] == "Escalated - Senior Review").sum()))
    c4.metric("Pending SMR Lodgement", int((df["status"] == "Pending SMR Lodgement").sum()))
    c5.metric("SMR Lodged / Monitoring", int(df["status"].isin(["SMR Lodged", "Post-SMR Monitoring"]).sum()))

    section_title(f"Investigation Queue ({len(df):,} results)")
    priority_pill = {
        "Critical": '<span class="pill pill-critical">Critical</span>',
        "High": '<span class="pill pill-high">High</span>',
        "Medium": '<span class="pill pill-medium">Medium</span>',
    }
    show = df.sort_values(["priority", "risk_score"], ascending=[True, False]).copy()
    show["Priority"] = show["priority"].map(priority_pill)
    show["Risk"] = show["risk_level"].apply(risk_pill)
    show["Status"] = show["status"].apply(status_pill_html)
    display = show[["case_id", "customer_id", "name", "typology", "Priority", "Risk", "Status",
                     "assigned_analyst", "opened_date"]]
    display = display.rename(columns={
        "case_id": "Case ID", "customer_id": "Customer ID", "name": "Name", "typology": "Typology",
        "assigned_analyst": "Analyst", "opened_date": "Opened",
    })
    display["Opened"] = pd.to_datetime(display["Opened"]).dt.strftime("%d %b %Y")
    st.write(display.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.caption("Use the **Investigation Workspace** tab to review a case, and **Escalation & Senior Review** "
               "or **SMR Assessment** to progress it through the lifecycle.")

# ================================================================== TAB 2
with tab2:
    section_title("Investigation Workspace")
    if cases_live.empty:
        st.info("No cases in the queue.")
    else:
        case_labels = {
            f"{r.case_id} - {r.customer_id} ({r.status})": r.case_id
            for r in merged_cases.itertuples()
        }
        chosen = st.selectbox("Select a case to investigate", list(case_labels.keys()), key="ws_case")
        case_id = case_labels[chosen]
        case_row = cases_live[cases_live["case_id"] == case_id].iloc[0]
        cust = customers[customers["customer_id"] == case_row["customer_id"]].iloc[0]

        colA, colB = st.columns([1, 1.4])
        with colA:
            st.markdown("**Customer Profile**")
            st.markdown(
                f"- Name: {cust['name']}\n"
                f"- Type: {cust['customer_type']} | Industry: {cust['industry']}\n"
                f"- Country: {cust['country']} | Status: {cust['status']}\n"
                f"- Onboarded: {pd.Timestamp(cust['onboarding_date']).strftime('%d %b %Y')}\n"
                f"- Current risk rating: {cust['risk_level']} ({cust['risk_score']}/100)\n"
            )
            if cust["customer_type"] == "Business":
                st.caption("Full UBO structure available on the **UBO Network** and **Business KYC** pages.")

            st.markdown("**Prior Alerts on this Customer**")
            cust_alerts = alerts[alerts["customer_id"] == cust["customer_id"]]
            if cust_alerts.empty:
                st.caption("No prior alerts recorded.")
            else:
                st.dataframe(
                    cust_alerts[["alert_id", "source", "alert_type", "severity", "disposition", "generated_date"]],
                    use_container_width=True, hide_index=True,
                )

            st.markdown("**Screening Hits**")
            cust_screen = screening[screening["customer_id"] == cust["customer_id"]]
            if cust_screen.empty:
                st.caption("No PEP, sanctions or adverse media matches.")
            else:
                st.dataframe(
                    cust_screen[["match_type", "match_detail", "match_score", "status"]],
                    use_container_width=True, hide_index=True,
                )

        with colB:
            st.markdown("**Transaction History**")
            cust_txns = transactions[transactions["customer_id"] == cust["customer_id"]].sort_values(
                "txn_date", ascending=False
            )
            st.dataframe(
                cust_txns[["txn_date", "amount", "direction", "channel", "counterparty_country", "description"]].head(25),
                use_container_width=True, hide_index=True,
            )

            st.markdown("**Source of Funds / Source of Wealth Review**")
            sof_input = st.text_area(
                "Investigation notes - SOF/SOW review, EDD findings, additional evidence requested",
                value=case_row.get("sof_review_notes", "") or "",
                height=110, key=f"sof_{case_id}",
            )

            act1, act2, act3 = st.columns(3)
            with act1:
                if st.button("💾 Save Notes", use_container_width=True):
                    update_case(case_id, sof_review_notes=sof_input)
                    log_audit("Investigation Notes Updated", "Case", case_id, "SOF/SOW review notes saved.")
                    st.success("Notes saved.")
            with act2:
                if st.button("✅ Close - False Positive", use_container_width=True):
                    update_case(case_id, status="Closed - No Action", senior_decision="Close Case",
                                sof_review_notes=sof_input)
                    log_audit("Case Closed", "Case", case_id, "Closed at investigation stage - false positive, no reasonable grounds for suspicion.")
                    st.success("Case closed as false positive.")
                    st.rerun()
            with act3:
                if st.button("⬆️ Escalate to Senior Review", type="primary", use_container_width=True):
                    update_case(case_id, status="Escalated - Senior Review", sof_review_notes=sof_input,
                                escalated_to="MLRO - K. Whitfield")
                    log_audit("Case Escalated", "Case", case_id,
                              "Escalated to senior review following investigation of transaction history, "
                              "screening results and SOF/SOW.")
                    st.success("Case escalated to Senior Review.")
                    st.rerun()

# ================================================================== TAB 3
with tab3:
    section_title("Escalation & Senior Review")
    st.caption(
        "Cases escalated by an analyst are reviewed by a Senior AML Analyst / Compliance Officer / MLRO, "
        "who decides whether to close the case, continue monitoring, or restrict/exit the relationship."
    )
    escalated = cases_live[cases_live["status"] == "Escalated - Senior Review"]
    if escalated.empty:
        st.success("No cases currently awaiting senior review.")
    else:
        merged_esc = escalated.merge(customers[["customer_id", "name", "risk_level"]], on="customer_id")
        labels = {f"{r.case_id} - {r.name} (escalated to {r.escalated_to})": r.case_id for r in merged_esc.itertuples()}
        chosen = st.selectbox("Select an escalated case", list(labels.keys()))
        case_id = labels[chosen]
        case_row = cases_live[cases_live["case_id"] == case_id].iloc[0]

        st.markdown(
            f"**Case:** {case_id}  \n"
            f"**Customer:** {case_row['customer_id']}  \n"
            f"**Escalated to:** {case_row['escalated_to']}  \n"
            f"**Investigation notes:** {case_row['sof_review_notes'] or '-'}"
        )
        decision = st.radio("Senior decision", SENIOR_DECISIONS, horizontal=True)
        sign_off = st.text_input("Reviewing officer", value=case_row["escalated_to"] or "MLRO - K. Whitfield")
        confirm = st.button("Record Senior Decision", type="primary")

        if confirm:
            if decision == "Close Case":
                update_case(case_id, senior_decision=decision, status="Closed - No Action")
                detail = "Senior review concluded no reasonable grounds for suspicion - case closed."
            elif decision == "Continue Monitoring":
                update_case(case_id, senior_decision=decision, status="Pending SMR Lodgement")
                detail = ("Senior review found reasonable grounds for suspicion may exist - referred for "
                          "SMR assessment and continued monitoring.")
            else:
                update_case(case_id, senior_decision=decision, status="Closed - Restricted / Exited")
                detail = "Senior review determined the customer relationship should be restricted/exited."
            log_audit("Senior Review Decision", "Case", case_id, f"{detail} Reviewed by {sign_off}.")
            st.success(f"Decision recorded: {decision}")
            st.rerun()

    st.divider()
    section_title("Recently Decided Cases")
    decided = cases_live[cases_live["senior_decision"] != ""].merge(
        customers[["customer_id", "name"]], on="customer_id"
    )
    if decided.empty:
        st.caption("No senior decisions recorded yet.")
    else:
        st.dataframe(
            decided[["case_id", "name", "escalated_to", "senior_decision", "status"]].rename(columns={
                "case_id": "Case ID", "name": "Customer", "escalated_to": "Reviewed By",
                "senior_decision": "Decision", "status": "Current Status",
            }),
            use_container_width=True, hide_index=True,
        )

# ================================================================== TAB 4
with tab4:
    section_title("SMR Assessment & Grounds for Suspicion")
    st.caption(
        "For cases referred for SMR assessment: auto-analyse transaction history for structuring, rapid "
        "movement and high-risk corridor typologies, draft the AUSTRAC WHO/WHAT/WHEN/WHERE/HOW/WHY "
        "narrative, and track lodgement."
    )

    smr_eligible = cases_live[cases_live["status"].isin(
        ["Pending SMR Lodgement", "SMR Lodged", "Post-SMR Monitoring", "Under Investigation",
         "Escalated - Senior Review"]
    )]
    if smr_eligible.empty:
        st.info("No cases currently eligible for SMR drafting.")
    else:
        merged_smr = smr_eligible.merge(
            customers[["customer_id", "name", "risk_level", "risk_score", "country"]], on="customer_id"
        )
        case_labels = {
            f"{r.case_id} - {r.name} ({r.status})": r.case_id for r in merged_smr.itertuples()
        }
        chosen_label = st.selectbox("Select a case", list(case_labels.keys()), key="smr_case")
        chosen_case_id = case_labels[chosen_label]
        case_row = cases_live[cases_live["case_id"] == chosen_case_id].iloc[0]
        customer_row = customers[customers["customer_id"] == case_row["customer_id"]].iloc[0]

        colA, colB = st.columns([1, 2])
        with colA:
            st.markdown(f"**Customer:** {customer_row['name']}  \n"
                        f"**ID:** {customer_row['customer_id']}  \n"
                        f"**Risk:** {customer_row['risk_level']} ({customer_row['risk_score']}/100)  \n"
                        f"**Case status:** {case_row['status']}")
            reasonable_grounds = st.checkbox(
                "I have reasonable grounds to suspect this matter is relevant to money laundering / "
                "terrorism financing (AML/CTF Act s.41)"
            )
            generate = st.button("🧾 Generate SMR Narrative", type="primary", use_container_width=True,
                                  disabled=not reasonable_grounds)
            if not reasonable_grounds:
                st.caption("Confirm reasonable grounds for suspicion to enable drafting.")

        if generate:
            with st.spinner("Analysing transaction history and drafting narrative..."):
                report = build_smr(customer_row, transactions, screening)
            st.session_state["current_smr"] = report
            log_audit("SMR Assessment", "Case", chosen_case_id,
                      "Reasonable grounds for suspicion confirmed; SMR narrative drafted for review.")

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

            st.text_area("SMR Draft (editable preview)", report.full_text(), height=420)

            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button(
                    "⬇️ Download as .txt", report.full_text().encode(),
                    file_name=f"{report.reference}.txt", mime="text/plain", use_container_width=True,
                )
            with dl2:
                docx_bytes = smr_to_docx_bytes(report)
                st.download_button(
                    "⬇️ Download as .docx", docx_bytes, file_name=f"{report.reference}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

            st.warning(
                "This is a system-generated draft to accelerate case review. A qualified compliance officer / "
                "MLRO must verify all details, complete bracketed fields, and approve the report before it is "
                "lodged with AUSTRAC via AUSTRAC Online. Do not submit unedited system output.",
                icon="⚠️",
            )

            st.divider()
            section_title("SMR Submission")
            if case_row["status"] in ("SMR Lodged", "Post-SMR Monitoring"):
                st.success(f"Already lodged - reference **{case_row['smr_reference']}** on "
                           f"{pd.Timestamp(case_row['smr_submitted_date']).strftime('%d %b %Y')}.")
                if case_row["status"] == "SMR Lodged":
                    if st.button("Move to Post-SMR Ongoing Monitoring"):
                        update_case(chosen_case_id, status="Post-SMR Monitoring")
                        log_audit("Post-SMR Monitoring Started", "Case", chosen_case_id,
                                  "Case moved to ongoing monitoring following SMR lodgement.")
                        st.rerun()
            else:
                ref_input = st.text_input("AUSTRAC lodgement reference", value=report.reference)
                lodged = st.button("📤 Mark as Lodged with AUSTRAC", type="primary")
                if lodged:
                    update_case(
                        chosen_case_id, status="SMR Lodged", smr_reference=ref_input,
                        smr_submitted_date=pd.Timestamp.today().normalize(),
                    )
                    log_audit("SMR Lodged with AUSTRAC", "Case", chosen_case_id,
                              f"Reference {ref_input} lodged via AUSTRAC Online.")
                    st.success(f"SMR marked as lodged - reference {ref_input}.")
                    st.rerun()
