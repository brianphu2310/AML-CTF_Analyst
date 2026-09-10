import streamlit as st
import pandas as pd
import plotly.express as px

from db_utils import load_all
from report_utils import detect_structuring, detect_rapid_movement, detect_high_risk_wires, HIGH_RISK_COUNTRIES_DEFAULT
from theme import inject_css, page_header, section_title

st.set_page_config(page_title="Transaction Monitoring | AML Suite", page_icon="📈", layout="wide")
inject_css()
page_header("Transaction Monitoring", "Automated typology detection across the full transaction ledger.", "MONITORING")

data = load_all()
customers, transactions = data["customers"], data["transactions"]

tab1, tab2, tab3, tab4 = st.tabs(
    ["🧩 Structuring", "⚡ Rapid Movement", "🌐 High-Risk Wires", "🔎 Customer Drill-down"]
)

# ---------------------------------------------------------------- STRUCTURING
with tab1:
    section_title("Structuring / Smurfing Alerts")
    results = []
    for cid, grp in transactions.groupby("customer_id"):
        f = detect_structuring(grp)
        if f:
            results.append((cid, f))
    st.metric("Customers flagged", len(results))
    if results:
        rows = []
        for cid, f in results:
            name = customers.loc[customers["customer_id"] == cid, "name"].values[0]
            rows.append({"Customer ID": cid, "Name": name, "Finding": f.summary, "Severity": f.severity})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.success("No structuring patterns detected in the current dataset.")

# ---------------------------------------------------------------- RAPID MOVEMENT
with tab2:
    section_title("Rapid Movement of Funds Alerts")
    results = []
    for cid, grp in transactions.groupby("customer_id"):
        f = detect_rapid_movement(grp)
        if f:
            results.append((cid, f))
    st.metric("Customers flagged", len(results))
    if results:
        rows = []
        for cid, f in results:
            name = customers.loc[customers["customer_id"] == cid, "name"].values[0]
            rows.append({"Customer ID": cid, "Name": name, "Finding": f.summary, "Severity": f.severity})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.success("No rapid movement patterns detected in the current dataset.")

# ---------------------------------------------------------------- HIGH-RISK WIRES
with tab3:
    section_title("High-Risk Corridor Wire Alerts")
    results = []
    for cid, grp in transactions.groupby("customer_id"):
        f = detect_high_risk_wires(grp, HIGH_RISK_COUNTRIES_DEFAULT)
        if f:
            results.append((cid, f))
    st.metric("Customers flagged", len(results))
    if results:
        rows = []
        for cid, f in results:
            name = customers.loc[customers["customer_id"] == cid, "name"].values[0]
            rows.append({"Customer ID": cid, "Name": name, "Finding": f.summary, "Severity": f.severity})
        wire_df = pd.DataFrame(rows)
        st.dataframe(wire_df, use_container_width=True, hide_index=True)

        section_title("Wire Volume by Counterparty Country")
        wires = transactions[
            (transactions["channel"] == "International Wire")
            & (transactions["counterparty_country"].isin(HIGH_RISK_COUNTRIES_DEFAULT))
        ]
        vol = wires.groupby("counterparty_country")["amount"].sum().sort_values(ascending=False)
        fig = px.bar(x=vol.index, y=vol.values, labels={"x": "Country", "y": "Total AUD"})
        fig.update_traces(marker_color="#B5541F")
        fig.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No high-risk corridor wire activity detected in the current dataset.")

# ---------------------------------------------------------------- DRILLDOWN
with tab4:
    section_title("Customer Transaction Drill-down")
    options = customers.sort_values("risk_score", ascending=False)
    label_map = {f"{r.customer_id} - {r.name} (risk {r.risk_score})": r.customer_id for r in options.itertuples()}
    choice = st.selectbox("Select a customer", list(label_map.keys()))
    cid = label_map[choice]
    cust_txns = transactions[transactions["customer_id"] == cid].sort_values("txn_date", ascending=False)
    cust = customers[customers["customer_id"] == cid].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transactions", len(cust_txns))
    c2.metric("Total Inbound", f"${cust_txns[cust_txns.direction=='Inbound']['amount'].sum():,.0f}")
    c3.metric("Total Outbound", f"${cust_txns[cust_txns.direction=='Outbound']['amount'].sum():,.0f}")
    c4.metric("Risk Score", f"{cust['risk_score']}/100")

    fig = px.scatter(
        cust_txns, x="txn_date", y="amount", color="direction", size="amount",
        color_discrete_map={"Inbound": "#1E3A5F", "Outbound": "#2A4E73"},
        hover_data=["channel", "counterparty_country"],
    )
    fig.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=10, b=10, l=10, r=10), height=340, legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        cust_txns[["txn_id", "txn_date", "amount", "direction", "channel", "counterparty_country", "description"]],
        use_container_width=True, hide_index=True,
    )

    st.caption("Tip: flagged customers can have an AUSTRAC-format SMR auto-drafted on the "
               "**Case Management & SMR** page.")
