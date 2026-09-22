import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import theme, data_access as da

st.set_page_config(page_title="Transaction Monitoring", layout="wide")
theme.inject_css()
theme.page_header("Transaction Monitoring", "Typology detection across trust account activity")

customers = da.load_customers()
transactions = da.load_transactions()
hits = da.load_typology_hits()

theme.methodology_note(
    "<b>Methodology:</b> five named typologies are detected directly from transaction "
    "patterns \u2014 structuring, rapid movement of funds, third-party funding mismatch, "
    "unexplained source-of-funds jump, and high-risk jurisdiction nexus. Each hit carries a "
    "plain-language reason. A generic \u201cflag anything over $10,000\u201d rule is deliberately "
    "not used \u2014 it would flag routine property settlements and miss the actual patterns."
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    theme.kpi_card("Transactions reviewed", f"{len(transactions):,}")
with c2:
    theme.kpi_card("Typology hits", f"{len(hits):,}", risk_class="risk-medium" if len(hits) else "")
with c3:
    hit_rate = len(hits) / len(transactions) * 100 if len(transactions) else 0
    theme.kpi_card("Hit rate", f"{hit_rate:.1f}%", "Of all transactions reviewed")
with c4:
    theme.kpi_card("Typologies monitored", "5", "Structuring, pass-through, 3rd-party, income, jurisdiction")

col1, col2 = st.columns([1.3, 1])
with col1:
    theme.section_title("Hits by typology")
    if len(hits):
        counts = hits["typology"].value_counts()
        fig = theme.bar_chart(counts.index, counts.values, horizontal=True, axis_title="Hits")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No typology hits in the current dataset.")

with col2:
    theme.section_title("Hits over time")
    if len(hits):
        h = hits.copy()
        h["txn_date"] = pd.to_datetime(h["txn_date"])
        h["month"] = h["txn_date"].dt.to_period("M").astype(str)
        monthly = h.groupby("month").size()
        fig = theme.line_area_chart(monthly.index, {"Typology hits": monthly.values})
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")
theme.section_title("Typology reference")
ref = {
    "Structuring": "Multiple deposits just under the $10,000 threshold within a short window \u2014 classic evasion of threshold reporting.",
    "Rapid movement of funds (pass-through)": "Money received into trust and paid out again within days, with no matching matter activity \u2014 trust used as a layering conduit.",
    "Third-party funding mismatch": "Funds received from a party with no documented connection to the client or matter.",
    "Unexplained source-of-funds jump": "Deposit materially inconsistent with the client's declared income \u2014 checked only for matter types where this comparison is meaningful.",
    "High-risk jurisdiction nexus": "Counterparty linked to an AUSTRAC-relevant high-risk jurisdiction.",
}
for name, desc in ref.items():
    st.markdown(f"**{name}** \u2014 {desc}")

st.markdown("---")
theme.section_title("Flagged transactions")
if len(hits):
    view = hits.merge(customers[["customer_id", "display_name", "risk_rating"]], on="customer_id", how="left")
    view = view.sort_values("txn_date", ascending=False)
    display = view[["txn_id", "txn_date", "display_name", "matter_type", "typology",
                     "amount_aud", "typology_reason", "risk_rating"]].copy()
    display["amount_aud"] = display["amount_aud"].apply(lambda v: f"${v:,.0f}")
    display["risk_rating"] = display["risk_rating"].apply(theme.risk_pill)
    display.columns = ["Transaction", "Date", "Customer", "Matter type", "Typology",
                        "Amount", "Reason", "Customer risk"]
    st.markdown(display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No flagged transactions to display.")
