import streamlit as st
import pandas as pd
import datetime as dt
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from lib import theme, data_access as da

st.set_page_config(page_title="AML/CTF Compliance Suite", layout="wide", page_icon=None)
theme.inject_css()

theme.page_header(
    "AML/CTF Compliance Suite",
    "Meridian Legal Partners \u2014 designated services under the AML/CTF Act 2006 (Cth), Tranche 2",
    badge="AUSTRAC REPORTING ENTITY",
)

customers = da.load_customers()
transactions = da.load_transactions()
alerts = da.load_alerts()

TODAY = dt.date(2026, 9, 22)

# ---------------------------------------------------------------- KPI ROW
total_customers = len(customers)
high_risk = int((customers.risk_rating == "High").sum())
high_risk_pct = high_risk / total_customers * 100
open_alerts = int((alerts.status == "Open").sum())
escalated = int((alerts.status == "Escalated to Case").sum())
this_month_txn = transactions[
    pd.to_datetime(transactions.txn_date) >= pd.Timestamp(TODAY) - pd.Timedelta(days=30)
]
trust_volume_30d = this_month_txn.amount_aud.sum()

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    theme.kpi_card("Customers in scope", f"{total_customers:,}", "Active client relationships under AML/CTF Program")
with c2:
    theme.kpi_card("High risk rating", f"{high_risk}", f"{high_risk_pct:.0f}% of client book", risk_class="risk-high")
with c3:
    theme.kpi_card("Open alerts", f"{open_alerts}", "Awaiting analyst triage", risk_class="risk-high" if open_alerts else "risk-low")
with c4:
    theme.kpi_card("Escalated to case", f"{escalated}", "Under active investigation", risk_class="risk-medium")
with c5:
    theme.kpi_card("Trust volume (30d)", f"${trust_volume_30d/1e6:.2f}M", "Total trust account movement")

theme.methodology_note(
    "<b>How these numbers are derived:</b> customer risk ratings apply AUSTRAC's four-factor "
    "model (customer type, jurisdiction, service/product, delivery channel) with the rule that "
    "any single high-risk factor drives an overall High rating, regardless of the other three. "
    "Alerts are generated only where a transaction matches a named typology and the composite "
    "score clears the alert threshold \u2014 see the Risk Methodology page for the full logic."
)

# ---------------------------------------------------------------- CHARTS
col1, col2 = st.columns([1.4, 1])

with col1:
    theme.section_title("Alert volume by typology")
    typ_counts = alerts["typology"].value_counts()
    fig = theme.bar_chart(
        typ_counts.index, typ_counts.values, horizontal=True,
        colors=[theme.CHART_SEQ[i % len(theme.CHART_SEQ)] for i in range(len(typ_counts))],
        axis_title="Alerts",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col2:
    theme.section_title("Client book by risk rating")
    rating_counts = customers["risk_rating"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
    fig = theme.donut_chart(
        rating_counts.index, rating_counts.values,
        colors=[theme.RISK_COLOR_MAP[r] for r in rating_counts.index],
        center_label="Total clients", center_value=f"{total_customers}",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

col3, col4 = st.columns(2)

with col3:
    theme.section_title("Trust account volume \u2014 last 12 months")
    tx = transactions.copy()
    tx["txn_date"] = pd.to_datetime(tx["txn_date"])
    tx["month"] = tx["txn_date"].dt.to_period("M").astype(str)
    monthly = tx[tx["txn_date"] >= pd.Timestamp(TODAY) - pd.Timedelta(days=365)].groupby("month")["amount_aud"].sum()
    fig = theme.line_area_chart(monthly.index, {"Trust volume": monthly.values}, y_title="AUD")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col4:
    theme.section_title("Alert status distribution")
    status_counts = alerts["status"].value_counts()
    fig = theme.bar_chart(
        status_counts.index, status_counts.values,
        colors=[theme.STATUS_COLOR_MAP.get(s, theme.SLATE) for s in status_counts.index],
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")
theme.section_title("Highest-priority open items")
priority = alerts[alerts.status.isin(["Open", "Escalated to Case"])].sort_values(
    "composite_score", ascending=False
).head(8)
if len(priority):
    display = priority.merge(customers[["customer_id", "display_name"]], on="customer_id", how="left")
    rows = "".join(
        f"<tr><td>{r.alert_id}</td><td>{r.display_name}</td><td>{r.typology}</td>"
        f"<td>{theme.risk_pill(r.risk_rating)}</td><td>{r.composite_score:.0f}</td>"
        f"<td>{theme.status_pill(r.status)}</td></tr>"
        for r in display.itertuples()
    )
    st.markdown(
        "<table><thead><tr><th>Alert</th><th>Customer</th><th>Typology</th>"
        "<th>Customer risk</th><th>Score</th><th>Status</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>",
        unsafe_allow_html=True,
    )
else:
    st.info("No open or escalated alerts at this time.")
