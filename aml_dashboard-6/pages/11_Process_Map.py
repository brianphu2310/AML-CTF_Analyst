import streamlit as st

from theme import inject_css, page_header, section_title, NAVY, BRASS, MUTED

st.set_page_config(page_title="Process Map | AML Suite", page_icon="🗺️", layout="wide")
inject_css()
page_header(
    "AML/CTF Process Map",
    "The full customer lifecycle this suite covers, end to end - from onboarding through ongoing "
    "monitoring, investigation, escalation, reporting and review.",
    "PROCESS MAP",
)

PHASES = [
    {
        "title": "1. Client Onboarding & CDD",
        "steps": [
            ("Client Onboarding", "Collect customer information and open the file.", "7_New_Client_Onboarding.py"),
            ("KYC / Identity Verification", "Verify identity, DOB, address and ID/VOI.", "7_New_Client_Onboarding.py"),
            ("KYB (business customers)", "Verify company registration and business activity.", "6_Business_KYC.py"),
            ("Beneficial Ownership / UBO", "Identify who actually owns or controls the business.", "5_UBO_Network.py"),
            ("PEP Screening", "Check for Politically Exposed Persons and related parties.", "2_Screening.py"),
            ("Sanctions Screening", "Check sanctions lists and verify potential matches.", "2_Screening.py"),
            ("Adverse Media Screening", "Search for negative / regulatory / criminal news.", "2_Screening.py"),
            ("Customer Risk Assessment", "Score and risk-rate the customer, geography, ownership, products.", "1_Customer_Risk.py"),
            ("CDD", "Gather and assess the information needed to understand the customer.", "7_New_Client_Onboarding.py"),
            ("EDD (if high risk)", "Request further evidence, source of funds/wealth, ownership detail.", "7_New_Client_Onboarding.py"),
            ("Onboarding Decision", "Approve / reject / conditionally approve / escalate.", "7_New_Client_Onboarding.py"),
        ],
    },
    {
        "title": "2. Ongoing Monitoring & Alert Generation",
        "steps": [
            ("Ongoing Monitoring", "Monitor the customer and their activity after onboarding.", "1_Customer_Risk.py"),
            ("Transaction Monitoring", "Analyse transactions against rules, thresholds and patterns.", "3_Transaction_Monitoring.py"),
            ("Alert Generation", "The system detects red flags and generates an AML alert.", "8_Alerts_Triage.py"),
            ("Alert Triage", "An analyst reviews each alert: false positive, investigate, or escalate.", "8_Alerts_Triage.py"),
        ],
    },
    {
        "title": "3. Investigation & Escalation",
        "steps": [
            ("Investigation", "Review the customer profile, KYC/KYB, UBO, screening and transaction history.", "4_Case_Management_SAR.py"),
            ("Source of Funds / Wealth Review", "Assess where the money came from and how wealth was formed.", "4_Case_Management_SAR.py"),
            ("EDD / Additional Information", "Request further evidence if the activity isn't explained.", "4_Case_Management_SAR.py"),
            ("Escalation", "Escalate to a Senior AML Analyst / Compliance Officer / MLRO.", "4_Case_Management_SAR.py"),
            ("Senior Review / Decision", "Close the case, continue monitoring, or restrict/exit the relationship.", "4_Case_Management_SAR.py"),
        ],
    },
    {
        "title": "4. SMR Reporting",
        "steps": [
            ("SMR Assessment", "Assess whether reasonable grounds for suspicion exist.", "4_Case_Management_SAR.py"),
            ("SMR Preparation", "Prepare suspicious matter details, transactions and grounds-for-suspicion narrative.", "4_Case_Management_SAR.py"),
            ("SMR Submission", "Lodge the SMR with AUSTRAC where required.", "4_Case_Management_SAR.py"),
            ("Post-SMR Ongoing Monitoring", "Continue monitoring the customer and take any further action needed.", "4_Case_Management_SAR.py"),
        ],
    },
    {
        "title": "5. Governance & Record Keeping",
        "steps": [
            ("Periodic Review / Remediation", "Review and remediate customer risk/KYC/CDD/EDD on a risk-based cycle.", "9_Periodic_Review.py"),
            ("Record Keeping / Audit Trail", "Retain files, evidence, alerts, investigation notes, decisions and reports.", "10_Audit_Trail.py"),
        ],
    },
]

total_steps = sum(len(p["steps"]) for p in PHASES)
st.info(f"**{total_steps} stages** across **{len(PHASES)} phases**, each backed by a working page in this suite.", icon="🗺️")

for phase in PHASES:
    section_title(phase["title"])
    for name, desc, page in phase["steps"]:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"**{name}**  \n<span style='color:{MUTED};font-size:0.88rem;'>{desc}</span>",
                        unsafe_allow_html=True)
        with c2:
            st.page_link(f"pages/{page}", label="Open page →")
    st.write("")

st.caption(
    "Every stage above is implemented as a working step in this suite rather than a static diagram - "
    "open any page to see the underlying data, workflow actions and audit trail entries it produces."
)
