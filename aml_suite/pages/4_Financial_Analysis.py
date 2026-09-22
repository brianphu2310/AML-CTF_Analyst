import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import theme, data_access as da

st.set_page_config(page_title="Financial Analysis", layout="wide")
theme.inject_css()
theme.page_header("Financial Analysis", "Trust ledger reconciliation and portfolio-level financial review")

customers = da.load_customers()
transactions = da.load_transactions()

theme.methodology_note(
    "<b>Two levels of analysis, matching how a financial analyst supports AML casework:</b> "
    "(1) per-matter cash-flow reconstruction to sense-check that trust movements match the "
    "matter's stated purpose, and (2) portfolio-level trends \u2014 funds under management, "
    "concentration, and monthly movement \u2014 for management reporting."
)

tab1, tab2 = st.tabs(["Matter-level reconciliation", "Portfolio-level review"])

with tab1:
    theme.section_title("Select a matter to reconcile")
    matter_ids = sorted(transactions["matter_id"].unique().tolist())
    selected_matter = st.selectbox("Matter", matter_ids)

    mt = transactions[transactions.matter_id == selected_matter].copy()
    mt["txn_date"] = pd.to_datetime(mt["txn_date"])
    mt = mt.sort_values("txn_date")
    cust_id = mt.iloc[0]["customer_id"]
    cust = customers[customers.customer_id == cust_id].iloc[0]

    inflow = mt[mt.txn_type == "Deposit"]["amount_aud"].sum()
    outflow = mt[mt.txn_type == "Withdrawal"]["amount_aud"].sum()
    net = inflow - outflow

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        theme.kpi_card("Client", cust.display_name, cust.customer_id)
    with c2:
        theme.kpi_card("Total inflow", f"${inflow:,.0f}")
    with c3:
        theme.kpi_card("Total outflow", f"${outflow:,.0f}")
    with c4:
        theme.kpi_card("Net trust position", f"${net:,.0f}",
                        risk_class="risk-high" if abs(net) > inflow * 0.15 and inflow > 0 else "risk-low")

    mt["running_balance"] = (mt["amount_aud"] * mt["txn_type"].map({"Deposit": 1, "Withdrawal": -1})).cumsum()
    fig = theme.line_area_chart(
        mt["txn_date"].dt.strftime("%Y-%m-%d"), {"Running trust balance": mt["running_balance"].values},
        y_title="AUD",
    )
    theme.section_title("Running trust ledger balance")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    income = cust.declared_annual_income_aud
    if income > 0:
        ratio = inflow / income
        theme.section_title("Sense checks")
        st.markdown(
            f"- Total inflow is **{ratio:.1f}x** the client's declared annual income "
            f"(${income:,.0f}, occupation: {cust.occupation}). For matter type "
            f"**{cust.primary_matter_type}**, a large multiple is {'expected' if cust.primary_matter_type in ('Residential Conveyancing','Commercial Conveyancing','Business Sale & Purchase','Debt Financing Transaction','Estate Administration') else 'worth reviewing since this matter type is not typically proportional to a large settlement'}."
        )
        third_party = mt["unrelated_third_party"].any()
        st.markdown(f"- Third-party funding source flagged: **{'Yes' if third_party else 'No'}**")
        st.markdown(f"- Running balance never goes negative (no overdraw): "
                     f"**{'Yes' if (mt['running_balance'] >= -0.01).all() else 'No \u2014 review required'}**")

    st.markdown("---")
    theme.section_title("Transaction detail")
    display = mt[["txn_id", "txn_date", "txn_type", "amount_aud", "description"]].copy()
    display["txn_date"] = display["txn_date"].dt.strftime("%Y-%m-%d")
    display["amount_aud"] = display["amount_aud"].apply(lambda v: f"${v:,.0f}")
    display.columns = ["Transaction", "Date", "Type", "Amount", "Description"]
    st.markdown(display.to_html(escape=False, index=False), unsafe_allow_html=True)

with tab2:
    tx = transactions.copy()
    tx["txn_date"] = pd.to_datetime(tx["txn_date"])
    tx["month"] = tx["txn_date"].dt.to_period("M").astype(str)

    total_inflow = tx[tx.txn_type == "Deposit"]["amount_aud"].sum()
    total_outflow = tx[tx.txn_type == "Withdrawal"]["amount_aud"].sum()
    fum = total_inflow - total_outflow

    c1, c2, c3 = st.columns(3)
    with c1:
        theme.kpi_card("Total trust inflow (period)", f"${total_inflow/1e6:.1f}M")
    with c2:
        theme.kpi_card("Total trust outflow (period)", f"${total_outflow/1e6:.1f}M")
    with c3:
        theme.kpi_card("Net funds under management", f"${fum/1e6:.1f}M")

    theme.section_title("Monthly trust movement")
    monthly = tx.groupby(["month", "txn_type"])["amount_aud"].sum().unstack(fill_value=0)
    fig = theme.grouped_bar_chart(
        monthly.index, {c: monthly[c].values for c in monthly.columns},
        colors={"Deposit": theme.SIGNAL_GREEN, "Withdrawal": theme.SIGNAL_RED},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    col1, col2 = st.columns(2)
    with col1:
        theme.section_title("Trust volume by matter type")
        by_matter = tx.groupby("matter_type")["amount_aud"].sum().sort_values(ascending=False)
        fig = theme.bar_chart(by_matter.index, by_matter.values, horizontal=True, axis_title="AUD")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with col2:
        theme.section_title("Concentration \u2014 top 10 clients by volume")
        by_cust = tx.groupby("customer_id")["amount_aud"].sum().sort_values(ascending=False).head(10)
        by_cust_named = by_cust.reset_index().merge(customers[["customer_id", "display_name"]], on="customer_id")
        fig = theme.bar_chart(by_cust_named["display_name"], by_cust_named["amount_aud"], horizontal=True, axis_title="AUD")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
