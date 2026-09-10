import streamlit as st
import pandas as pd

from db_utils import load_all
from onboarding_utils import run_screening, score_onboarding, cdd_record_text, cdd_record_to_docx_bytes
from theme import inject_css, page_header, section_title, risk_pill

st.set_page_config(page_title="New Client Onboarding | AML Suite", page_icon="🧾", layout="wide")
inject_css()
page_header(
    "New Client Onboarding",
    "Guided CDD workflow: capture KYC information, then automatically run screening, risk scoring and EDD checks.",
    "ONBOARDING",
)

data = load_all()
COUNTRIES = sorted(data["customers"]["country"].unique())
INDUSTRIES = sorted(data["customers"]["industry"].unique())

STEPS = ["Customer Type", "Identity", "Ownership & Control", "Relationship & Activity", "Review & Run Checks"]

if "onb_step" not in st.session_state:
    st.session_state.onb_step = 0
if "onb_answers" not in st.session_state:
    st.session_state.onb_answers = {"ubos": []}
if "onb_result" not in st.session_state:
    st.session_state.onb_result = None

answers = st.session_state.onb_answers


def goto(step):
    st.session_state.onb_step = step


# ---------------------------------------------------------------- STEP INDICATOR
cols = st.columns(len(STEPS))
for i, (col, label) in enumerate(zip(cols, STEPS)):
    with col:
        if i < st.session_state.onb_step:
            st.markdown(f"✅ **{label}**")
        elif i == st.session_state.onb_step:
            st.markdown(f"🔵 **{label}**")
        else:
            st.markdown(f"⚪ {label}")
st.progress((st.session_state.onb_step) / (len(STEPS) - 1))
st.divider()

step = st.session_state.onb_step

# ========================================================================
# STEP 0 - CUSTOMER TYPE
# ========================================================================
if step == 0:
    section_title("Who are we onboarding?")
    ctype = st.radio(
        "Customer type", ["Individual", "Business"],
        index=0 if answers.get("customer_type", "Individual") == "Individual" else 1,
        horizontal=True,
    )
    delivery = st.selectbox(
        "How is this customer being onboarded?",
        ["Face-to-face (branch)", "Non face-to-face (digital)", "Referred by existing customer", "Broker/Introducer"],
        index=0,
    )
    st.caption(
        "This determines which identification and verification questions are asked next, and feeds into "
        "the initial risk assessment (non face-to-face onboarding carries elevated impersonation/fraud risk)."
    )
    if st.button("Next →", type="primary"):
        answers["customer_type"] = ctype
        answers["verification_method"] = delivery
        goto(1)
        st.rerun()

# ========================================================================
# STEP 1 - IDENTITY
# ========================================================================
elif step == 1:
    is_biz = answers.get("customer_type") == "Business"
    section_title("Identity Details" if not is_biz else "Entity Details")
    with st.form("identity_form"):
        if is_biz:
            full_name = st.text_input("Legal / registered business name", answers.get("full_name", ""))
            abn = st.text_input("ABN / ACN / company registration number", answers.get("id_number", ""))
            structure_type = st.selectbox(
                "Structure type", ["Pty Ltd", "Trust", "Partnership", "Sole Trader", "Public Company", "Foreign Subsidiary"],
                index=0,
            )
            incorp_date = st.date_input("Incorporation date")
            country = st.selectbox("Country of incorporation", COUNTRIES,
                                    index=COUNTRIES.index(answers["country"]) if answers.get("country") in COUNTRIES else 0)
            industry = st.selectbox("Industry", INDUSTRIES,
                                     index=INDUSTRIES.index(answers["industry"]) if answers.get("industry") in INDUSTRIES else 0)
            website = st.text_input("Website / trading name (optional)")
            id_type = "Certificate of Incorporation"
        else:
            full_name = st.text_input("Full legal name", answers.get("full_name", ""))
            dob = st.date_input("Date of birth")
            nationality = st.selectbox("Nationality", COUNTRIES,
                                        index=COUNTRIES.index(answers["nationality"]) if answers.get("nationality") in COUNTRIES else 0)
            country = st.selectbox("Country of residence", COUNTRIES,
                                    index=COUNTRIES.index(answers["country"]) if answers.get("country") in COUNTRIES else 0)
            occupation = st.text_input("Occupation", answers.get("occupation", ""))
            industry = st.selectbox("Employer industry (if applicable)", INDUSTRIES)
            id_type = st.selectbox("Identification document", ["Passport", "Driver Licence", "National ID Card"])
            id_number = st.text_input("Document number")

        pep_declared = st.checkbox(
            "The customer (or an immediate family member / close associate) is a politically exposed person",
            value=answers.get("self_declared_pep", False),
        )

        c1, c2 = st.columns(2)
        back = c1.form_submit_button("← Back")
        forward = c2.form_submit_button("Next →", type="primary")

    if back:
        goto(0)
        st.rerun()
    if forward:
        answers["full_name"] = full_name
        answers["country"] = country
        answers["self_declared_pep"] = pep_declared
        if is_biz:
            answers["id_number"] = abn
            answers["id_type"] = id_type
            answers["structure_type"] = structure_type
            answers["dob_or_incorp"] = str(incorp_date)
            answers["industry"] = industry
            answers["nationality"] = None
            answers["occupation"] = None
        else:
            answers["id_type"] = id_type
            answers["id_number"] = id_number
            answers["dob_or_incorp"] = str(dob)
            answers["nationality"] = nationality
            answers["occupation"] = occupation
            answers["industry"] = industry
            answers["structure_type"] = None
        goto(2)
        st.rerun()

# ========================================================================
# STEP 2 - OWNERSHIP & CONTROL
# ========================================================================
elif step == 2:
    section_title("Ownership & Control")
    if answers.get("customer_type") != "Business":
        st.info("Not applicable for individual customers - beneficial ownership only applies to business entities.")
        c1, c2 = st.columns(2)
        if c1.button("← Back"):
            goto(1)
            st.rerun()
        if c2.button("Next →", type="primary"):
            answers["ubos"] = []
            goto(3)
            st.rerun()
    else:
        st.caption("List every individual or entity that owns 25% or more, or otherwise exercises control "
                   "(e.g. director, trustee, appointor).")
        default_rows = pd.DataFrame(answers.get("ubos") or [
            {"name": "", "role": "Director", "ownership_pct": 0, "nationality": "Australia", "is_pep": False}
        ])
        edited = st.data_editor(
            default_rows,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "role": st.column_config.SelectboxColumn(options=["Director", "Shareholder", "Trustee", "Appointor", "Beneficiary"]),
                "nationality": st.column_config.SelectboxColumn(options=COUNTRIES),
                "ownership_pct": st.column_config.NumberColumn(min_value=0, max_value=100, format="%d%%"),
                "is_pep": st.column_config.CheckboxColumn("PEP?"),
            },
            key="ubo_editor",
        )
        total_pct = edited["ownership_pct"].fillna(0).sum() if not edited.empty else 0
        if total_pct > 100:
            st.warning(f"Total ownership currently sums to {total_pct:.0f}% - please check the entries.")

        c1, c2 = st.columns(2)
        if c1.button("← Back"):
            goto(1)
            st.rerun()
        if c2.button("Next →", type="primary"):
            answers["ubos"] = edited.fillna({"name": "", "nationality": "Australia"}).to_dict("records")
            goto(3)
            st.rerun()

# ========================================================================
# STEP 3 - RELATIONSHIP & ACTIVITY PROFILE
# ========================================================================
elif step == 3:
    section_title("Relationship & Expected Activity")
    with st.form("activity_form"):
        purpose = st.selectbox(
            "Purpose of the relationship",
            ["Everyday banking", "Trade Finance", "Investment - Domestic", "Investment - Offshore",
             "Property Purchase", "Remittance", "Business operating account", "Other"],
        )
        source_of_funds = st.selectbox(
            "Primary source of funds",
            ["Employment income", "Business revenue", "Sale of asset", "Inheritance",
             "Investment returns", "Loan (bank/institutional)", "Loan (private/informal)",
             "Gift", "Gambling winnings", "Other / Unspecified"],
        )
        source_of_wealth = st.text_area(
            "Source of wealth (for higher-value relationships, describe how overall wealth was accumulated)",
            answers.get("source_of_wealth", ""),
        )
        expected_volume = st.selectbox(
            "Expected transaction volume",
            ["Under $10,000 / month", "$10,000 - $50,000 / month", "$50,000 - $250,000 / month", "Over $250,000 / month"],
        )
        expected_channels = st.multiselect(
            "Expected transaction channels",
            ["Cash", "Domestic EFT", "International Wire", "Digital Currency", "Cheque"],
        )
        expected_countries = st.multiselect("Countries the customer expects to transact with", COUNTRIES)
        cash_intensive = st.checkbox("This is (or the business operates as) a cash-intensive business")

        c1, c2 = st.columns(2)
        back = c1.form_submit_button("← Back")
        forward = c2.form_submit_button("Next →", type="primary")

    if back:
        goto(2)
        st.rerun()
    if forward:
        answers.update({
            "purpose": purpose, "source_of_funds": source_of_funds, "source_of_wealth": source_of_wealth,
            "expected_volume": expected_volume, "expected_channels": expected_channels,
            "expected_countries": expected_countries, "cash_intensive": cash_intensive,
        })
        goto(4)
        st.rerun()

# ========================================================================
# STEP 4 - REVIEW & RUN CHECKS
# ========================================================================
elif step == 4:
    section_title("Review Captured Information")
    is_biz = answers.get("customer_type") == "Business"

    colA, colB = st.columns(2)
    with colA:
        st.markdown(f"""
**Customer type:** {answers.get('customer_type')}
**Name:** {answers.get('full_name')}
**{'Incorporation date' if is_biz else 'Date of birth'}:** {answers.get('dob_or_incorp')}
**Country:** {answers.get('country')}
**{'Structure' if is_biz else 'Occupation'}:** {answers.get('structure_type') if is_biz else answers.get('occupation')}
**ID:** {answers.get('id_type')} {answers.get('id_number')}
**Verification method:** {answers.get('verification_method')}
**Self-declared PEP:** {"Yes" if answers.get('self_declared_pep') else "No"}
        """)
    with colB:
        st.markdown(f"""
**Purpose:** {answers.get('purpose')}
**Source of funds:** {answers.get('source_of_funds')}
**Expected volume:** {answers.get('expected_volume')}
**Expected channels:** {', '.join(answers.get('expected_channels', [])) or '-'}
**Expected countries:** {', '.join(answers.get('expected_countries', [])) or '-'}
**Cash-intensive:** {"Yes" if answers.get('cash_intensive') else "No"}
        """)

    if is_biz and answers.get("ubos"):
        section_title("Beneficial Owners")
        st.dataframe(pd.DataFrame(answers["ubos"]), use_container_width=True, hide_index=True)

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("← Back to edit"):
        goto(3)
        st.rerun()
    run = c2.button("🚦 Run Onboarding Compliance Checks", type="primary", use_container_width=True)

    if run:
        with st.spinner("Screening against PEP / Sanctions / Adverse Media lists and calculating risk score..."):
            hits = run_screening(answers.get("full_name", ""), is_biz, answers.get("self_declared_pep", False))
            result = score_onboarding(answers, hits)
        st.session_state.onb_result = result

    result = st.session_state.onb_result
    if result:
        st.divider()
        section_title("Compliance Check Results")

        m1, m2, m3 = st.columns(3)
        m1.markdown(f"**Risk score:** {result.score}/100  \n**Risk rating:** {risk_pill(result.risk_level)}",
                    unsafe_allow_html=True)
        m2.markdown(f"**CDD tier required:**  \n{result.cdd_tier}")
        decision_color = "🟥" if "DO NOT" in result.decision else ("🟧" if result.risk_level in ("High", "Critical") else "🟩")
        m3.markdown(f"**Decision:**  \n{decision_color} {result.decision}")

        section_title("Screening Results")
        if result.screening_hits:
            st.dataframe(pd.DataFrame(result.screening_hits), use_container_width=True, hide_index=True)
        else:
            st.success("No PEP, sanctions or adverse media matches identified.")

        section_title("Risk Factor Breakdown")
        st.dataframe(result.factor_table(), use_container_width=True, hide_index=True)

        if result.risk_level in ("High", "Critical"):
            st.warning(
                "This customer requires **Enhanced Due Diligence** before the account is activated: verify "
                "source of wealth documentation, obtain senior management / MLRO approval, and set an initial "
                "review date of no more than 6 months.",
                icon="⚠️",
            )
        if any(h["type"] == "Sanctions" for h in result.screening_hits):
            st.error(
                "Potential sanctions match identified. Do not provide any service to this customer until the "
                "match has been manually reviewed and cleared by the MLRO, in line with the AML/CTF Act's "
                "sanctions obligations.",
                icon="🚨",
            )

        section_title("Customer Due Diligence Record")
        st.text_area("CDD Record (editable preview)", cdd_record_text(answers, result), height=380)

        dl1, dl2, dl3 = st.columns(3)
        with dl1:
            st.download_button(
                "⬇️ Download as .txt", cdd_record_text(answers, result).encode(),
                file_name=f"CDD_{answers.get('full_name','client').replace(' ','_')}.txt",
                mime="text/plain", use_container_width=True,
            )
        with dl2:
            st.download_button(
                "⬇️ Download as .docx", cdd_record_to_docx_bytes(answers, result),
                file_name=f"CDD_{answers.get('full_name','client').replace(' ','_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with dl3:
            if st.button("🔄 Start New Onboarding", use_container_width=True):
                st.session_state.onb_step = 0
                st.session_state.onb_answers = {"ubos": []}
                st.session_state.onb_result = None
                st.rerun()

        st.caption(
            "In live-DB mode, confirming this record would insert a new row into the `customers` table "
            "(and `ubo` table for business owners) via `db_utils.py`, and open a case automatically if "
            "Enhanced Due Diligence is required."
        )
