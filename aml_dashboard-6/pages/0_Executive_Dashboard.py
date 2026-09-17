"""
0_Executive_Dashboard.py
A single-page executive report built the way a senior data analyst would
lay out a real Power BI report: a persistent slicer/filter panel at the
top, a row of KPI cards with trend indicators, and a set of report pages
(tabs) each holding a small, purposeful set of flat 2D visuals - a line/
area trend, a donut, ranked bar charts, bullet-style KPI indicators and a
matrix table with inline conditional-formatting bars. Every chart comes
from theme.py's flat 2D chart engine (not the rotated 3D scenes used
elsewhere in the suite) because that is what a real BI report is built
from, and every chart's card is sized to the chart itself rather than a
tall panel with empty space around it.
"""

import pandas as pd
import streamlit as st

from db_utils import load_all
from theme import (
    inject_css, page_header, section_title, kpi_card, kpi_card_trend,
    bar2d_chart, grouped_bar2d_chart, line_area_chart, donut_chart,
    bullet_kpi_chart, matrix_table_html, teal_gradient,
    RISK_COLOR_MAP, TEAL_DARK, TEAL_MID, TEAL_LIGHT, BROWN_MID,
    CRITICAL, HIGH, MEDIUM, LOW,
)
from workflow_utils import CASE_STATUSES

st.set_page_config(page_title="Executive Dashboard | AML Suite", layout="wide")
inject_css()
page_header(
    "Executive Dashboard",
    "Portfolio-wide AML/CTF performance across risk, screening, transaction monitoring and case "
    "management - the one-page view a Board Risk Committee would expect to see.",
    "REPORT",
)

data = load_all()
customers, transactions, screening = data["customers"], data["transactions"], data["screening"]
cases, businesses, ubo, alerts = data["cases"], data["businesses"], data["ubo"], data["alerts"]

# ============================================================== FILTER / SLICER PANEL
with st.container(border=True):
    st.markdown('<div class="slicer-label">Filters</div>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([1.3, 1, 1, 1])
    with f1:
        period_label = st.radio(
            "Period", ["Last 90 Days", "Last 180 Days", "Last 12 Months", "All Time"],
            index=0, horizontal=True, label_visibility="collapsed",
        )
    with f2:
        risk_sel = st.multiselect("Risk Level", ["Low", "Medium", "High", "Critical"],
                                   placeholder="Risk Level")
    with f3:
        industry_sel = st.multiselect("Industry", sorted(customers["industry"].unique()),
                                       placeholder="Industry")
    with f4:
        country_sel = st.multiselect("Country", sorted(customers["country"].unique()),
                                      placeholder="Country")

window_map = {"Last 90 Days": 90, "Last 180 Days": 180, "Last 12 Months": 365, "All Time": None}
window_days = window_map[period_label]

fc = customers.copy()
if risk_sel:
    fc = fc[fc["risk_level"].isin(risk_sel)]
if industry_sel:
    fc = fc[fc["industry"].isin(industry_sel)]
if country_sel:
    fc = fc[fc["country"].isin(country_sel)]
scope_ids = set(fc["customer_id"])

ftxn_all = transactions[transactions["customer_id"].isin(scope_ids)]
fcases = cases[cases["customer_id"].isin(scope_ids)]
falerts = alerts[alerts["customer_id"].isin(scope_ids)]
fscreening = screening[screening["customer_id"].isin(scope_ids)]

end_date = transactions["txn_date"].max()
has_comparison = window_days is not None
if has_comparison:
    start_cur = end_date - pd.Timedelta(days=window_days)
    start_prior = start_cur - pd.Timedelta(days=window_days)
    ftxn = ftxn_all[ftxn_all["txn_date"] > start_cur]
    prior_txn = ftxn_all[(ftxn_all["txn_date"] <= start_cur) & (ftxn_all["txn_date"] > start_prior)]
    cur_alerts = falerts[falerts["generated_date"] > start_cur]
    prior_alerts = falerts[(falerts["generated_date"] <= start_cur) & (falerts["generated_date"] > start_prior)]
else:
    ftxn = ftxn_all
    prior_txn = ftxn_all.iloc[0:0]
    cur_alerts = falerts
    prior_alerts = falerts.iloc[0:0]


def pct_delta(cur, prior) -> str:
    if not has_comparison or not prior:
        return ""
    d = (cur - prior) / prior * 100
    return f"{'+' if d >= 0 else ''}{d:.1f}%"


# ============================================================== KPI ROW
cur_vol = ftxn["amount"].sum()
prior_vol = prior_txn["amount"].sum()
pct_hc = (fc["risk_level"].isin(["High", "Critical"]).sum() / len(fc) * 100) if len(fc) else 0.0
open_cases = fcases[~fcases["status"].str.contains("Closed")]
pending_smr = fcases[fcases["status"] == "Pending SMR Lodgement"]

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi_card_trend("Customers in Scope", f"{len(fc):,}",
                    sub=f"{(len(fc) / len(customers) * 100) if len(customers) else 0:.0f}% of book")
with k2:
    hc_delta = f"{'+' if pct_hc >= 15 else '-'}{abs(pct_hc - 15):.1f} pts"
    kpi_card_trend("High / Critical Risk", f"{fc['risk_level'].isin(['High', 'Critical']).sum():,}",
                    delta=hc_delta, higher_is_better=False, sub="vs 15% target")
with k3:
    kpi_card_trend("Alerts (Period)", f"{len(cur_alerts):,}",
                    delta=pct_delta(len(cur_alerts), len(prior_alerts)), higher_is_better=False,
                    sub=(f"{len(prior_alerts)} in prior period" if has_comparison else "no prior-period baseline"))
with k4:
    kpi_card_trend("Active Cases", f"{len(open_cases):,}", sub=f"{len(fcases)} total in scope")
with k5:
    kpi_card_trend("Pending SMR Lodgement", f"{len(pending_smr):,}", sub="within statutory 3-day window")
with k6:
    kpi_card_trend("Transaction Volume", f"${cur_vol / 1_000_000:.1f}M",
                    delta=pct_delta(cur_vol, prior_vol),
                    sub=(f"${prior_vol / 1_000_000:.1f}M prior period" if has_comparison else "no prior-period baseline"))

st.markdown('<div class="bi-tabbar">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Overview", "Risk & Compliance", "Operations & SMR"])
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================== TAB 1 - OVERVIEW
with tab1:
    c1, c2 = st.columns([1.7, 1])
    with c1:
        section_title("Transaction Volume Trend")
        trend_txns = ftxn_all[ftxn_all["txn_date"] > start_cur] if has_comparison else ftxn_all
        daily = (
            trend_txns.groupby([pd.Grouper(key="txn_date", freq="D"), "direction"])["amount"]
            .sum().unstack(fill_value=0)
        )
        for col in ("Inbound", "Outbound"):
            if col not in daily.columns:
                daily[col] = 0.0
        daily = daily.sort_index()
        date_labels = [d.strftime("%d %b") for d in daily.index]
        fig = line_area_chart(
            date_labels, {"Inbound": daily["Inbound"].tolist(), "Outbound": daily["Outbound"].tolist()},
            colors={"Inbound": TEAL_DARK, "Outbound": BROWN_MID}, y_title="AUD", height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        section_title("Alerts by Disposition")
        disp_counts = falerts["disposition"].value_counts()
        if disp_counts.empty:
            st.info("No alerts in the current filter scope.")
        else:
            disp_color = {"New": HIGH, "False Positive": LOW, "Requires Investigation": MEDIUM,
                          "Escalated to Case": CRITICAL}
            fig = donut_chart(
                disp_counts.index.tolist(), disp_counts.values.tolist(),
                colors=[disp_color.get(d, TEAL_MID) for d in disp_counts.index],
                center_label="Total Alerts", center_value=f"{disp_counts.sum():,}", height=300,
            )
            st.plotly_chart(fig, use_container_width=True)

    section_title("Compliance Health Targets")
    total_screening = len(fscreening)
    resolved = int(fscreening["status"].isin(["Cleared - False Positive", "Escalated"]).sum())
    pct_resolved = resolved / total_screening * 100 if total_screening else 0.0
    pct_closed = (fcases["status"].str.contains("Closed").sum() / len(fcases) * 100) if len(fcases) else 0.0

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown('<div class="bi-visual-label">% High / Critical Risk</div>'
                    f'<div class="bi-visual-value">{pct_hc:.1f}%</div>', unsafe_allow_html=True)
        st.plotly_chart(bullet_kpi_chart(pct_hc, 15, TEAL_DARK, label="High/Critical Risk"),
                        use_container_width=True)
    with g2:
        st.markdown('<div class="bi-visual-label">% Screening Hits Resolved</div>'
                    f'<div class="bi-visual-value">{pct_resolved:.1f}%</div>', unsafe_allow_html=True)
        st.plotly_chart(bullet_kpi_chart(pct_resolved, 80, BROWN_MID, label="Screening Resolved"),
                        use_container_width=True)
    with g3:
        st.markdown('<div class="bi-visual-label">% Cases Closed</div>'
                    f'<div class="bi-visual-value">{pct_closed:.1f}%</div>', unsafe_allow_html=True)
        st.plotly_chart(bullet_kpi_chart(pct_closed, 60, TEAL_LIGHT, label="Cases Closed"),
                        use_container_width=True)

# ============================================================== TAB 2 - RISK & COMPLIANCE
with tab2:
    c1, c2 = st.columns([1.5, 1])
    with c1:
        section_title("Customer Risk Mix by Industry (Top 8)")
        if fc.empty:
            st.info("No customers match the current filters.")
        else:
            top_ind = fc["industry"].value_counts().head(8).index.tolist()
            piv = fc[fc["industry"].isin(top_ind)].groupby(["industry", "risk_level"]).size().unstack(fill_value=0)
            for lvl in ["Low", "Medium", "High", "Critical"]:
                if lvl not in piv.columns:
                    piv[lvl] = 0
            piv = piv.reindex(top_ind).fillna(0)
            fig = grouped_bar2d_chart(
                top_ind, {lvl: piv[lvl].tolist() for lvl in ["Low", "Medium", "High", "Critical"]},
                colors=RISK_COLOR_MAP, height=340,
            )
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        section_title("Top Countries by Avg Risk Score")
        grp = fc.groupby("country").agg(avg_risk=("risk_score", "mean"), n=("customer_id", "count"))
        grp = grp[grp["n"] >= 3].sort_values("avg_risk", ascending=False).head(10)
        if grp.empty:
            st.info("Not enough customers per country in scope to rank.")
        else:
            fig = bar2d_chart(
                grp.index.tolist(), grp["avg_risk"].round(1).tolist(), horizontal=True,
                colors=teal_gradient(grp["avg_risk"].tolist()), axis_title="Avg Risk Score", height=340,
            )
            st.plotly_chart(fig, use_container_width=True)

    section_title("Risk Register Matrix - Industry x Risk Level")
    if fc.empty:
        st.info("No customers match the current filters.")
    else:
        all_ind = fc["industry"].value_counts().head(10).index.tolist()
        mpiv = fc[fc["industry"].isin(all_ind)].groupby(["industry", "risk_level"]).size().unstack(fill_value=0)
        for lvl in ["Low", "Medium", "High", "Critical"]:
            if lvl not in mpiv.columns:
                mpiv[lvl] = 0
        mpiv = mpiv.reindex(all_ind).fillna(0)[["Low", "Medium", "High", "Critical"]]
        html = matrix_table_html(mpiv.index.tolist(), ["Low", "Medium", "High", "Critical"],
                                  mpiv.values.tolist(), row_header="Industry", color=TEAL_MID)
        st.markdown(html, unsafe_allow_html=True)

    st.divider()
    section_title("Beneficial Ownership Exposure")
    st.caption("Business register is portfolio-wide and not affected by the customer filters above.")
    pep_biz = set(ubo[ubo["is_pep"]]["business_id"])
    p1, p2, p3 = st.columns(3)
    with p1:
        kpi_card("Entities with PEP Owner", f"{len(pep_biz):,}",
                 f"of {businesses['business_id'].nunique():,} entities on file")
    with p2:
        kpi_card("Corporate Owners", f"{(ubo['owner_type'] == 'Corporate').sum():,}",
                 f"of {len(ubo):,} beneficial owners")
    with p3:
        n_biz = businesses["business_id"].nunique()
        kpi_card("Avg Ownership Layers", f"{(len(ubo) / n_biz):.1f}" if n_biz else "-", "owners per entity")

# ============================================================== TAB 3 - OPERATIONS & SMR
with tab3:
    c1, c2 = st.columns([1.4, 1])
    with c1:
        section_title("Case Pipeline by Status")
        status_counts = fcases["status"].value_counts().reindex(CASE_STATUSES).fillna(0)
        pipeline_colors = [
            CRITICAL if "Restrict" in s else LOW if "Closed" in s else HIGH if ("Pending" in s or "Escalat" in s)
            else TEAL_DARK
            for s in CASE_STATUSES
        ]
        fig = bar2d_chart(CASE_STATUSES, status_counts.values.tolist(), colors=pipeline_colors,
                          horizontal=True, category_order=CASE_STATUSES, height=340)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        section_title("Case Load by Analyst")
        load_by_analyst = fcases["assigned_analyst"].value_counts()
        if load_by_analyst.empty:
            st.info("No cases in the current filter scope.")
        else:
            fig = bar2d_chart(load_by_analyst.index.tolist(), load_by_analyst.values.tolist(),
                              colors=teal_gradient(load_by_analyst.values.tolist()), horizontal=True, height=340)
            st.plotly_chart(fig, use_container_width=True)

    section_title("SMR Lodgement Timeliness")
    lodged = fcases[fcases["smr_submitted_date"].notna()].copy()
    if lodged.empty:
        st.info("No SMRs lodged within the current filter scope.")
    else:
        lodged["days_to_lodge"] = (lodged["smr_submitted_date"] - lodged["opened_date"]).dt.days
        avg_days = float(lodged["days_to_lodge"].mean())
        m1, m2 = st.columns([1, 2])
        with m1:
            kpi_card("Avg Days: Case Open -> SMR Lodged", f"{avg_days:.1f} days",
                     f"{len(lodged)} SMRs lodged in scope")
        with m2:
            st.markdown('<div class="bi-visual-label">Avg Days to Lodge vs 3-Day Statutory Target</div>',
                        unsafe_allow_html=True)
            color = LOW if avg_days <= 3 else CRITICAL
            st.plotly_chart(
                bullet_kpi_chart(avg_days, 3, color, max_value=max(avg_days, 3) * 1.3,
                                 suffix=" days", label="Days to Lodge"),
                use_container_width=True,
            )

    st.divider()
    section_title("Case Aging by Priority")
    fcases_open = fcases[~fcases["status"].str.contains("Closed")].copy()
    if fcases_open.empty:
        st.info("No open cases in the current filter scope.")
    else:
        today = pd.Timestamp.today().normalize()
        fcases_open["age_days"] = (today - fcases_open["opened_date"]).dt.days
        bins = [0, 7, 30, 60, 10_000]
        bin_labels = ["0-7 days", "8-30 days", "31-60 days", "60+ days"]
        fcases_open["age_bucket"] = pd.cut(fcases_open["age_days"], bins=bins, labels=bin_labels,
                                            include_lowest=True)
        age_piv = fcases_open.groupby(["age_bucket", "priority"], observed=False).size().unstack(fill_value=0)
        for p in ["Critical", "High", "Medium"]:
            if p not in age_piv.columns:
                age_piv[p] = 0
        age_piv = age_piv.reindex(bin_labels).fillna(0)[["Critical", "High", "Medium"]]
        html = matrix_table_html(age_piv.index.tolist(), ["Critical", "High", "Medium"],
                                  age_piv.values.tolist(), row_header="Case Age", color=BROWN_MID)
        st.markdown(html, unsafe_allow_html=True)

st.markdown(
    f'<div class="bi-footer">Data as of {end_date.strftime("%d %b %Y")} '
    "- synthetic demo dataset, refreshed each session.</div>",
    unsafe_allow_html=True,
)
