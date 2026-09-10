import streamlit as st
from db_utils import run_query, RISK_SCORE_SQL, customer_transactions, customer_screening, customer_profile
from report_utils import generate_sar_narrative, narrative_to_docx_bytes

st.set_page_config(page_title="Case Management & SAR", page_icon="📄", layout="wide")
st.title("📄 Case Management & SAR Generation")
st.caption(
    "Select a flagged customer to auto-generate a SAR-style case narrative from their "
    "profile, screening results, and transaction history."
)

risk_df = run_query(RISK_SCORE_SQL)

# ------------------------------------------------------------------
# CASE QUEUE
# ------------------------------------------------------------------
st.sidebar.header("Case Queue Filter")
min_score = st.sidebar.slider("Minimum risk score to show in queue", 0, 4, 2)

queue = risk_df[risk_df["risk_score"] >= min_score].sort_values("risk_score", ascending=False)
st.subheader(f"Case Queue ({len(queue)} customers with risk score ≥ {min_score})")
st.dataframe(
    queue[["customer_id", "full_name", "country", "industry", "customer_status",
           "structuring", "rapid_movement", "high_risk_country", "screening_hit", "risk_score"]],
    use_container_width=True,
    height=300,
)

st.divider()

# ------------------------------------------------------------------
# SAR GENERATION
# ------------------------------------------------------------------
st.subheader("Generate SAR for a Case")

if queue.empty:
    st.info("No customers meet the selected risk threshold.")
    st.stop()

selected_customer = st.selectbox("Select customer_id", queue["customer_id"].tolist())
analyst_name = st.text_input("Analyst name (appears on the report)", value="Brian Phu")

if st.button("Generate SAR Narrative", type="primary"):
    profile_df = customer_profile(selected_customer)
    screening_df = customer_screening(selected_customer)
    txns_df = customer_transactions(selected_customer)

    if profile_df.empty:
        st.error("Customer not found.")
    else:
        profile = profile_df.iloc[0]
        narrative = generate_sar_narrative(
            selected_customer, profile, screening_df, txns_df, analyst_name
        )
        st.session_state["sar_narrative"] = narrative
        st.session_state["sar_customer"] = selected_customer

if "sar_narrative" in st.session_state and st.session_state.get("sar_customer") == selected_customer:
    st.text_area("SAR Narrative Preview", st.session_state["sar_narrative"], height=500)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download as .txt",
            st.session_state["sar_narrative"].encode("utf-8"),
            file_name=f"SAR_{selected_customer}.txt",
            mime="text/plain",
        )
    with col2:
        try:
            docx_bytes = narrative_to_docx_bytes(st.session_state["sar_narrative"], selected_customer)
            st.download_button(
                "Download as .docx",
                docx_bytes,
                file_name=f"SAR_{selected_customer}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except ImportError:
            st.warning("Install `python-docx` (`pip install python-docx`) to enable .docx export.")
