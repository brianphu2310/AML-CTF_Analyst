import streamlit as st
import pandas as pd

from db_utils import load_all
from report_utils import detect_structuring, detect_rapid_movement, detect_high_risk_wires, HIGH_RISK_COUNTRIES_DEFAULT
from theme import inject_css, page_header, section_title, bar3d_chart, scatter3d_chart, brown_gradient

st.set_page_config(page_title="Transaction Monitoring | AML Suite", layout="wide")
inject_css()
page_header("Transaction Monitoring", "Automated typology detection across the full transaction ledger.", "MONITORING")

data = load_all()
customers, transactions = data["customers"], data["transactions"]

tab1, tab2, tab3, tab4 = st.tabs(
    ["Structuring", "Rapid Movement", "High-Risk Wires", "Customer Drill-down"]
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
        fig = bar3d_chart(
            categories=list(vol.index),
            values=list(vol.values),
            colors=brown_gradient(vol.values),
            value_fmt=lambda v: f"${v:,.0f}",
            z_title="Total AUD",
            height=340,
        )
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

    st.caption("Drag to rotate, scroll to zoom. Depth (z) separates transactions by channel.")
    channels = sorted(cust_txns["channel"].unique())
    channel_index = {c: i for i, c in enumerate(channels)}
    max_amount = cust_txns["amount"].max() if len(cust_txns) else 1
    fig = scatter3d_chart(
        x=cust_txns["txn_date"].tolist(),
        y=cust_txns["amount"].tolist(),
        z=[channel_index[c] for c in cust_txns["channel"]],
        color_labels=cust_txns["direction"].tolist(),
        color_map={"Inbound": "#1F5E5B", "Outbound": "#B5651D"},
        size=[8 + 14 * (a / max_amount) for a in cust_txns["amount"]],
        hover_text=[f"{d} - {ch} - {cty} - ${amt:,.0f}" for d, ch, cty, amt in
                    zip(cust_txns["txn_date"].dt.strftime("%d %b %Y"), cust_txns["channel"],
                        cust_txns["counterparty_country"], cust_txns["amount"])],
        x_title="Date", y_title="Amount (AUD)", z_title="Channel",
        height=380,
    )
    fig.update_layout(scene=dict(zaxis=dict(tickvals=list(range(len(channels))), ticktext=channels)))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        cust_txns[["txn_id", "txn_date", "amount", "direction", "channel", "counterparty_country", "description"]],
        use_container_width=True, hide_index=True,
    )

    st.caption("Tip: flagged customers can have an AUSTRAC-format SMR auto-drafted on the "
               "**Case Management & SMR** page.")
