import streamlit as st
import plotly.express as px
from db_utils import run_query, RISK_SCORE_SQL, customer_transactions

st.set_page_config(page_title="Transaction Monitoring", page_icon="💰", layout="wide")
st.title("💰 Transaction Monitoring Rules")

STRUCTURING_SQL = """
SELECT customer_id, COUNT(*) AS cash_deposit_count, SUM(amount) AS total_amount,
       MIN(transaction_date) AS window_start, MAX(transaction_date) AS window_end
FROM transactions
WHERE transaction_type = 'Cash Deposit' AND amount BETWEEN 9000 AND 9999
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY total_amount DESC;
"""

RAPID_SQL = """
SELECT t1.customer_id, t1.transaction_date AS deposit_date, t1.amount AS deposit_amount,
       t2.transaction_date AS outflow_date, t2.amount AS outflow_amount,
       t2.transaction_type AS outflow_type, t2.counterparty_country
FROM transactions t1
JOIN transactions t2
  ON t1.customer_id = t2.customer_id
 AND t2.transaction_type IN ('Wire Transfer','Withdrawal')
 AND t2.transaction_date > t1.transaction_date
 AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days'
WHERE t1.transaction_type = 'Deposit' AND t1.amount >= 8000
ORDER BY t1.customer_id, t1.transaction_date;
"""

HIGH_RISK_SQL = """
SELECT customer_id, transaction_date, amount, counterparty_country, channel
FROM transactions
WHERE transaction_type = 'Wire Transfer'
  AND counterparty_country IN ('Iran','North Korea','Myanmar','Syria','Yemen')
ORDER BY amount DESC;
"""

TXN_TYPE_SQL = """
SELECT transaction_type, COUNT(*) AS count, SUM(amount) AS total_amount
FROM transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;
"""

structuring_df = run_query(STRUCTURING_SQL)
rapid_df = run_query(RAPID_SQL)
highrisk_df = run_query(HIGH_RISK_SQL)
txn_type_df = run_query(TXN_TYPE_SQL)
risk_df = run_query(RISK_SCORE_SQL)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧱 Structuring", "⚡ Rapid Movement", "🌍 High-Risk Country Wires", "🔍 Customer Drill-Down"
])

with tab1:
    st.subheader("Structuring — Cash Deposits Just Under $10,000 Threshold")
    st.caption("3+ Cash Deposits between $9,000–$9,999 for the same customer within a 7-day window.")
    c1, c2 = st.columns(2)
    c1.metric("Customers Flagged", len(structuring_df))
    c2.metric("Total Structured Amount", f"${structuring_df['total_amount'].sum():,.2f}")
    st.dataframe(structuring_df, use_container_width=True, height=400)

with tab2:
    st.subheader("Rapid Movement — Large Deposit Followed by Near-Immediate Outflow")
    st.caption("Deposit ≥ $8,000 followed within 2 days by a Wire Transfer or Withdrawal.")
    c1, c2 = st.columns(2)
    c1.metric("Pattern Instances", len(rapid_df))
    c2.metric(
        "To High-Risk Country",
        int(rapid_df["counterparty_country"].isin(
            ["Iran", "North Korea", "Myanmar", "Syria", "Yemen"]
        ).sum()),
    )
    st.dataframe(rapid_df, use_container_width=True, height=400)

with tab3:
    st.subheader("Wire Transfers to High-Risk Jurisdictions")
    c1, c2 = st.columns(2)
    c1.metric("Wires Flagged", len(highrisk_df))
    c2.metric("Total Amount", f"${highrisk_df['amount'].sum():,.2f}")
    fig = px.bar(
        highrisk_df.groupby("counterparty_country")["amount"].sum().reset_index(),
        x="counterparty_country", y="amount",
        labels={"amount": "Total AUD", "counterparty_country": "Country"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(highrisk_df, use_container_width=True, height=350)

with tab4:
    st.subheader("Per-Customer Transaction Timeline")
    all_customers = risk_df.sort_values("risk_score", ascending=False)["customer_id"].tolist()
    selected = st.selectbox("Select customer", all_customers)

    txns = customer_transactions(selected)
    st.write(f"**{len(txns)} transactions** for `{selected}`")

    fig2 = px.scatter(
        txns, x="transaction_date", y="amount", color="transaction_type", size="amount",
        hover_data=["counterparty_country", "channel"],
        title=f"Transaction Timeline — {selected}",
    )
    fig2.add_hline(y=10000, line_dash="dash", line_color="red",
                    annotation_text="$10,000 reporting threshold")
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(txns, use_container_width=True)

st.divider()
st.subheader("Overall Transaction Volume by Type")
fig3 = px.pie(txn_type_df, names="transaction_type", values="total_amount", hole=0.4)
st.plotly_chart(fig3, use_container_width=True)
