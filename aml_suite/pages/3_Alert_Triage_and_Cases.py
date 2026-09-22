import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import theme, data_access as da

st.set_page_config(page_title="Alert Triage & Cases", layout="wide")
theme.inject_css()
theme.page_header("Alert Triage & Case Management", "From system-generated alert to SMR decision")

customers = da.load_customers()
alerts = da.load_alerts()

theme.methodology_note(
    "<b>Workflow:</b> Transaction Monitoring generates an <b>Alert</b> (typology + composite "
    "score). An analyst triages it to <i>Escalate to Case</i>, <i>Close \u2014 False Positive</i>, "
    "or <i>Close \u2014 No Issue</i> (with documented rationale). An escalated case can end in a "
    "<b>Suspicious Matter Report (SMR)</b> filed with AUSTRAC. Filing an SMR is a reporting "
    "obligation, not an instruction to end the client relationship \u2014 and nothing in this "
    "workflow discloses a pending SMR to the customer (the AML/CTF Act's tipping-off prohibition)."
)

tab1, tab2 = st.tabs(["Alert queue", "Case pipeline"])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        status_filter = st.multiselect(
            "Status", alerts["status"].unique().tolist(), default=alerts["status"].unique().tolist()
        )
    with c2:
        typology_filter = st.multiselect(
            "Typology", alerts["typology"].unique().tolist(), default=[]
        )
    with c3:
        min_score = st.slider("Minimum composite score", 0, int(alerts.composite_score.max()) if len(alerts) else 0, 0)

    filtered = alerts[alerts.status.isin(status_filter)]
    if typology_filter:
        filtered = filtered[filtered.typology.isin(typology_filter)]
    filtered = filtered[filtered.composite_score >= min_score]
    filtered = filtered.sort_values("composite_score", ascending=False)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        theme.kpi_card("Alerts shown", f"{len(filtered)}")
    with c2:
        theme.kpi_card("Open", f"{(filtered.status=='Open').sum()}", risk_class="risk-high")
    with c3:
        theme.kpi_card("Escalated", f"{(filtered.status=='Escalated to Case').sum()}", risk_class="risk-medium")
    with c4:
        closed = filtered.status.isin(["Closed - False Positive", "Closed - No Issue"]).sum()
        conv_rate = (filtered.status == "Escalated to Case").sum() / len(filtered) * 100 if len(filtered) else 0
        theme.kpi_card("Alert \u2192 case conversion", f"{conv_rate:.0f}%")

    view = filtered.merge(customers[["customer_id", "display_name"]], on="customer_id", how="left")
    display = view[["alert_id", "alert_date", "display_name", "typology", "risk_rating",
                     "composite_score", "amount_aud", "status", "reason"]].copy()
    display["amount_aud"] = display["amount_aud"].apply(lambda v: f"${v:,.0f}")
    display["risk_rating"] = display["risk_rating"].apply(theme.risk_pill)
    display["status"] = display["status"].apply(theme.status_pill)
    display.columns = ["Alert", "Date", "Customer", "Typology", "Customer risk",
                        "Score", "Amount", "Status", "Reason"]
    st.markdown(display.to_html(escape=False, index=False), unsafe_allow_html=True)

with tab2:
    theme.section_title("Case pipeline \u2014 escalated alerts")
    cases = alerts[alerts.status.isin(["Escalated to Case", "Closed - No Issue", "Closed - False Positive"])]
    funnel_data = alerts["status"].value_counts().reindex(
        ["Open", "Escalated to Case", "Closed - No Issue", "Closed - False Positive"]
    ).fillna(0)

    col1, col2 = st.columns([1, 1])
    with col1:
        theme.section_title("Pipeline funnel")
        fig = theme.bar_chart(funnel_data.index, funnel_data.values,
                               colors=[theme.STATUS_COLOR_MAP.get(s, theme.SLATE) for s in funnel_data.index])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with col2:
        theme.section_title("Escalated cases by typology")
        esc = alerts[alerts.status == "Escalated to Case"]
        if len(esc):
            counts = esc["typology"].value_counts()
            fig = theme.donut_chart(counts.index, counts.values, center_label="Escalated", center_value=str(len(esc)))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No escalated cases currently.")

    st.markdown("---")
    theme.section_title("Case investigation view")
    esc_ids = alerts[alerts.status == "Escalated to Case"]["alert_id"].tolist()
    if esc_ids:
        selected = st.selectbox("Select a case", esc_ids)
        case = alerts[alerts.alert_id == selected].iloc[0]
        cust = customers[customers.customer_id == case.customer_id].iloc[0]

        cc1, cc2 = st.columns([1, 1])
        with cc1:
            st.markdown(f"**Customer:** {cust.display_name} ({cust.customer_id})")
            st.markdown(f"**Risk rating:** {theme.risk_pill(cust.risk_rating)}", unsafe_allow_html=True)
            st.markdown(f"**Structure:** {cust.structure}")
            st.markdown(f"**Jurisdiction:** {cust.jurisdiction}")
            st.markdown(f"**Matter:** {case.matter_id} \u2014 {cust.primary_matter_type}")
        with cc2:
            st.markdown(f"**Typology:** {case.typology}")
            st.markdown(f"**Composite score:** {case.composite_score:.1f}")
            st.markdown(f"**Amount involved:** ${case.amount_aud:,.0f}")
            st.markdown(f"**Transactions:** {len(case.txn_ids)}")

        st.markdown("**Investigation note (internal only \u2014 not disclosed to customer):**")
        st.markdown(f"> {case.reason}")

        st.markdown("**Decision:**")
        decision = st.radio(
            "Recommended next step",
            ["File Suspicious Matter Report (SMR) with AUSTRAC", "Close case \u2014 no SMR (document rationale)",
             "Request EDD refresh before deciding"],
            index=None,
            key=f"decision_{selected}",
        )
        if decision:
            st.success(f"Recorded decision for {selected}: {decision}")
    else:
        st.info("No escalated cases to review right now.")
