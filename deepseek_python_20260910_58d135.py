"""
AML/KYC Transaction Monitoring Intelligence — Single-file Streamlit app.

Chạy với:
    streamlit run app.py

Tất cả chức năng (Home, Customer Risk, Screening, Transaction Monitoring,
Case Management & SAR) được gom vào các TAB trong cùng 1 file.
"""

import os
import io
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

# ==================================================================
# DATABASE CONFIG
# ==================================================================

def _get_db_url() -> str:
    """Đọc DATABASE_URL từ Streamlit Secrets hoặc biến môi trường."""
    try:
        return st.secrets["DATABASE_URL"]
    except (KeyError, FileNotFoundError):
        pass
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:@localhost:5432/aml_platform",
    )


@st.cache_resource
def get_engine():
    url = _get_db_url()
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return create_engine(url)


@st.cache_data(ttl=300)
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})


# ==================================================================
# SQL QUERIES
# ==================================================================

RISK_SCORE_SQL = """
WITH structuring AS (
    SELECT customer_id, COUNT(*) AS structuring_count, SUM(amount) AS structuring_total
    FROM transactions
    WHERE transaction_type = 'Cash Deposit' AND amount BETWEEN 9000 AND 9999
    GROUP BY customer_id
    HAVING COUNT(*) >= 3
),
rapid AS (
    SELECT DISTINCT t1.customer_id
    FROM transactions t1
    JOIN transactions t2
      ON t1.customer_id = t2.customer_id
     AND t2.transaction_type IN ('Wire Transfer','Withdrawal')
     AND t2.transaction_date > t1.transaction_date
     AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days'
    WHERE t1.transaction_type = 'Deposit' AND t1.amount >= 8000
),
highrisk AS (
    SELECT DISTINCT customer_id
    FROM transactions
    WHERE transaction_type = 'Wire Transfer'
      AND counterparty_country IN ('Iran','North Korea','Myanmar','Syria','Yemen')
),
screening_flag AS (
    SELECT DISTINCT customer_id
    FROM screening_results
    WHERE status IN ('Potential Match','Confirmed Match')
)
SELECT
    c.customer_id, c.full_name, c.customer_type, c.country, c.residency_country,
    c.industry, c.occupation, c.annual_income, c.account_open_date, c.customer_status,
    CASE WHEN s.customer_id IS NOT NULL THEN 1 ELSE 0 END AS structuring,
    COALESCE(s.structuring_count, 0) AS structuring_count,
    COALESCE(s.structuring_total, 0) AS structuring_total,
    CASE WHEN r.customer_id IS NOT NULL THEN 1 ELSE 0 END AS rapid_movement,
    CASE WHEN h.customer_id IS NOT NULL THEN 1 ELSE 0 END AS high_risk_country,
    CASE WHEN sc.customer_id IS NOT NULL THEN 1 ELSE 0 END AS screening_hit,
    (CASE WHEN s.customer_id IS NOT NULL THEN 1 ELSE 0 END
     + CASE WHEN r.customer_id IS NOT NULL THEN 1 ELSE 0 END
     + CASE WHEN h.customer_id IS NOT NULL THEN 1 ELSE 0 END
     + CASE WHEN sc.customer_id IS NOT NULL THEN 1 ELSE 0 END) AS risk_score
FROM customers c
LEFT JOIN structuring s ON c.customer_id = s.customer_id
LEFT JOIN rapid r ON c.customer_id = r.customer_id
LEFT JOIN highrisk h ON c.customer_id = h.customer_id
LEFT JOIN screening_flag sc ON c.customer_id = sc.customer_id
ORDER BY risk_score DESC, c.customer_id;
"""

SCREENING_DETAIL_SQL = """
SELECT screening_id, customer_id, screening_type, status, screening_date, match_details
FROM screening_results
ORDER BY customer_id, screening_type;
"""

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


def customer_transactions(customer_id: str) -> pd.DataFrame:
    sql = """
        SELECT transaction_date, transaction_type, amount, currency,
               counterparty_country, channel
        FROM transactions
        WHERE customer_id = :cid
        ORDER BY transaction_date;
    """
    return run_query(sql, {"cid": customer_id})


def customer_screening(customer_id: str) -> pd.DataFrame:
    sql = """
        SELECT screening_type, status, screening_date, match_details
        FROM screening_results
        WHERE customer_id = :cid
        ORDER BY screening_type;
    """
    return run_query(sql, {"cid": customer_id})


def customer_profile(customer_id: str) -> pd.DataFrame:
    return run_query("SELECT * FROM customers WHERE customer_id = :cid;", {"cid": customer_id})


# ==================================================================
# SAR NARRATIVE GENERATION
# ==================================================================

HIGH_RISK_COUNTRIES = {"Iran", "North Korea", "Myanmar", "Syria", "Yemen"}


def find_structuring_clusters(txns: pd.DataFrame):
    cash = txns[
        (txns["transaction_type"] == "Cash Deposit")
        & (txns["amount"] >= 9000)
        & (txns["amount"] <= 9999)
    ].sort_values("transaction_date")

    clusters, used = [], set()
    dates = cash["transaction_date"].tolist()
    for i in range(len(dates)):
        if i in used:
            continue
        window = cash[
            (cash["transaction_date"] >= dates[i])
            & (cash["transaction_date"] <= dates[i] + pd.Timedelta(days=7))
        ]
        if len(window) >= 3:
            clusters.append(window)
            used.update(range(i, i + len(window)))
    return clusters


def find_rapid_movements(txns: pd.DataFrame):
    deposits = txns[(txns["transaction_type"] == "Deposit") & (txns["amount"] >= 8000)]
    outflows = txns[txns["transaction_type"].isin(["Wire Transfer", "Withdrawal"])]
    pairs = []
    for _, dep in deposits.iterrows():
        matches = outflows[
            (outflows["transaction_date"] > dep["transaction_date"])
            & (outflows["transaction_date"] <= dep["transaction_date"] + pd.Timedelta(days=2))
        ]
        for _, out in matches.iterrows():
            pairs.append((dep, out))
    return pairs


def find_high_risk_wires(txns: pd.DataFrame):
    return txns[
        (txns["transaction_type"] == "Wire Transfer")
        & (txns["counterparty_country"].isin(HIGH_RISK_COUNTRIES))
    ]


def generate_sar_narrative(customer_id, profile, screening, txns, analyst_name="[Your name]"):
    today = date.today().strftime("%d %B %Y")
    structuring_clusters = find_structuring_clusters(txns)
    rapid_pairs = find_rapid_movements(txns)
    high_risk_wires = find_high_risk_wires(txns)

    screening_hits = screening[screening["status"] != "Clear"]
    has_pep = "PEP" in screening_hits["screening_type"].values
    has_sanctions = "Sanctions" in screening_hits["screening_type"].values
    has_adverse = "Adverse Media" in screening_hits["screening_type"].values

    risk_score = sum([
        len(structuring_clusters) > 0,
        len(rapid_pairs) > 0,
        len(high_risk_wires) > 0,
        len(screening_hits) > 0,
    ])

    L = []
    L.append("SUSPICIOUS ACTIVITY REPORT (SAR) — CASE FILE")
    L.append("=" * 60)
    L.append(f"Case Reference: AML-{date.today().year}-{customer_id[-4:]}")
    L.append(f"Prepared by: {analyst_name}")
    L.append(f"Date prepared: {today}")
    L.append(f"Composite Risk Score: {risk_score} / 4")
    L.append("")

    L.append("1. SUBJECT INFORMATION")
    L.append("-" * 60)
    L.append(f"Customer ID:        {customer_id}")
    L.append(f"Name:               {profile.get('full_name', 'N/A')}")
    L.append(f"Customer Type:      {profile.get('customer_type', 'N/A')}")
    L.append(f"Date of Birth:      {profile.get('date_of_birth', 'N/A')}")
    L.append(f"Country:            {profile.get('country', 'N/A')}")
    L.append(f"Residency:          {profile.get('residency_country', 'N/A')}")
    L.append(f"Industry:           {profile.get('industry', 'N/A')}")
    L.append(f"Occupation:         {profile.get('occupation', 'N/A')}")
    L.append(f"Declared Income:    {profile.get('annual_income', 'N/A')}")
    L.append(f"Account Opened:     {profile.get('account_open_date', 'N/A')}")
    L.append(f"Account Status:     {profile.get('customer_status', 'N/A')}")
    L.append("")

    L.append("2. SCREENING FINDINGS")
    L.append("-" * 60)
    if screening.empty:
        L.append("No screening records found for this customer.")
    else:
        for _, row in screening.iterrows():
            detail = f" — {row['match_details']}" if pd.notna(row.get("match_details")) and row.get("match_details") else ""
            L.append(f"{row['screening_type']:<15} {row['status']:<18}{detail}")
    L.append("")

    L.append("3. TRANSACTION PATTERN ANALYSIS")
    L.append("-" * 60)
    if structuring_clusters:
        for idx, cluster in enumerate(structuring_clusters, 1):
            total = cluster["amount"].sum()
            start, end = cluster["transaction_date"].min(), cluster["transaction_date"].max()
            L.append(f"a{idx}) Structuring cluster: {len(cluster)} cash deposits between "
                     f"{start} and {end}, totaling ${total:,.2f} AUD, all just under the "
                     f"$10,000 reporting threshold.")
            for _, r in cluster.iterrows():
                L.append(f"     - {r['transaction_date']}: ${r['amount']:,.2f} ({r['channel']})")
    else:
        L.append("No structuring pattern detected.")
    L.append("")

    if rapid_pairs:
        for idx, (dep, out) in enumerate(rapid_pairs, 1):
            pct = (out["amount"] / dep["amount"]) * 100 if dep["amount"] else 0
            L.append(f"b{idx}) Rapid movement: deposit of ${dep['amount']:,.2f} on "
                     f"{dep['transaction_date']} followed by {out['transaction_type']} of "
                     f"${out['amount']:,.2f} to {out['counterparty_country']} on "
                     f"{out['transaction_date']} ({pct:.0f}% of deposit passed through "
                     f"within {(out['transaction_date'] - dep['transaction_date']).days} day(s)).")
    else:
        L.append("No rapid movement pattern detected.")
    L.append("")

    if not high_risk_wires.empty:
        L.append("c) Wire transfers to high-risk jurisdictions:")
        for _, r in high_risk_wires.iterrows():
            L.append(f"     - {r['transaction_date']}: ${r['amount']:,.2f} to {r['counterparty_country']}")
    else:
        L.append("No wire transfers to high-risk jurisdictions detected.")
    L.append("")

    L.append("4. RED FLAGS SUMMARY")
    L.append("-" * 60)
    n = 1
    if has_pep:
        L.append(f"{n}. PEP screening hit not yet resolved via Enhanced Due Diligence (EDD)."); n += 1
    if has_sanctions:
        L.append(f"{n}. Sanctions screening hit — requires immediate escalation."); n += 1
    if has_adverse:
        L.append(f"{n}. Adverse media hit — requires manual review of source article(s)."); n += 1
    if structuring_clusters:
        L.append(f"{n}. Structuring — multiple deposits just under the reporting threshold."); n += 1
    if rapid_pairs:
        L.append(f"{n}. Rapid pass-through of funds shortly after deposit."); n += 1
    if not high_risk_wires.empty:
        L.append(f"{n}. Funds transferred to a high-risk/sanctioned-adjacent jurisdiction."); n += 1
    if n == 1:
        L.append("No red flags identified based on current monitoring rules.")
    L.append("")

    L.append("5. RECOMMENDATION")
    L.append("-" * 60)
    if risk_score >= 3:
        L.append("Escalate to Senior Compliance Officer. Recommend filing a Suspicious")
        L.append("Matter Report (SMR) with AUSTRAC pending Enhanced Due Diligence outcome.")
        L.append("Flag account for enhanced ongoing monitoring.")
    elif risk_score == 2:
        L.append("Recommend Enhanced Due Diligence (EDD) and a follow-up review within")
        L.append("30 days. Escalate to team lead if further red flags emerge.")
    else:
        L.append("Continue standard monitoring. No immediate escalation required.")

    return "\n".join(L)


def narrative_to_docx_bytes(narrative: str) -> bytes:
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    for line in narrative.split("\n"):
        if line.startswith("=") or line.startswith("-"):
            continue
        if line.isupper() and line.strip() and not line.startswith(" "):
            doc.add_heading(line, level=2)
        else:
            doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()


# ==================================================================
# PAGE CONFIG
# ==================================================================

st.set_page_config(
    page_title="AML/KYC Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AML / KYC Transaction Monitoring Intelligence")
st.caption(
    "Synthetic data portfolio project — end-to-end AML pipeline: "
    "customer onboarding, UBO/beneficial ownership, PEP/Sanctions/Adverse "
    "Media screening, transaction monitoring, and case management."
)

# ==================================================================
# LOAD DATA (một lần, dùng chung cho mọi tab)
# ==================================================================

try:
    risk_df = run_query(RISK_SCORE_SQL)
    screening_df = run_query(SCREENING_DETAIL_SQL)
    structuring_df = run_query(STRUCTURING_SQL)
    rapid_df = run_query(RAPID_SQL)
    highrisk_df = run_query(HIGH_RISK_SQL)
    txn_type_df = run_query(TXN_TYPE_SQL)
except Exception as e:
    st.error(
        "❌ Could not connect to the database.\n\n"
        "**Local:** kiểm tra `DATABASE_URL` trong `.streamlit/secrets.toml` hoặc biến môi trường.\n\n"
        "**Streamlit Cloud:** vào *Settings → Secrets* và thêm `DATABASE_URL`.\n\n"
        f"**Chi tiết lỗi:** `{e}`"
    )
    st.stop()

# ==================================================================
# TABS
# ==================================================================

tab_home, tab_risk, tab_screen, tab_txn, tab_sar = st.tabs([
    "🏠 Overview",
    "📊 Customer Risk",
    "🔎 Screening",
    "💰 Transaction Monitoring",
    "📄 Case Management & SAR",
])

# ------------------------------------------------------------------
# TAB 1 — OVERVIEW
# ------------------------------------------------------------------
with tab_home:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Customers", len(risk_df))
    c2.metric("Critical Risk (score = 4)", int((risk_df["risk_score"] == 4).sum()))
    c3.metric("Elevated Risk (score ≥ 2)", int((risk_df["risk_score"] >= 2).sum()))
    c4.metric("Any Screening Hit", int((risk_df["screening_hit"] == 1).sum()))
    c5.metric("Confirmed Matches", int((screening_df["status"] == "Confirmed Match").sum()))

    st.divider()
    cc1, cc2 = st.columns([2, 1])

    with cc1:
        st.subheader("Risk Score Distribution Across Customer Base")
        dist = risk_df["risk_score"].value_counts().sort_index().reset_index()
        dist.columns = ["risk_score", "count"]
        fig = px.bar(
            dist, x="risk_score", y="count", text="count",
            labels={"risk_score": "Composite Risk Score (0–4)", "count": "Customers"},
            color="risk_score",
            color_continuous_scale=["#2ecc71", "#f1c40f", "#e67e22", "#c0392b", "#7b241c"],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with cc2:
        st.subheader("Screening Outcomes")
        outcome_counts = screening_df["status"].value_counts().reset_index()
        outcome_counts.columns = ["status", "count"]
        fig2 = px.pie(
            outcome_counts, names="status", values="count", hole=0.5,
            color="status",
            color_discrete_map={
                "Clear": "#2ecc71",
                "Potential Match": "#f39c12",
                "Confirmed Match": "#c0392b",
            },
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.markdown(
        """
        ### How to use this dashboard
        Dùng các tab phía trên để điều hướng:
        - **📊 Customer Risk** — danh sách khách hàng đã chấm điểm rủi ro
        - **🔎 Screening** — kết quả PEP / Sanctions / Adverse Media
        - **💰 Transaction Monitoring** — structuring, rapid movement, wires đến quốc gia rủi ro
        - **📄 Case Management & SAR** — chọn khách hàng và sinh báo cáo SAR (.txt / .docx)
        """
    )
    st.caption("All data is synthetic — for portfolio demonstration only.")

# ------------------------------------------------------------------
# TAB 2 — CUSTOMER RISK
# ------------------------------------------------------------------
with tab_risk:
    st.subheader("📊 Customer Risk Scoring")

    st.sidebar.header("Filters — Customer Risk")
    min_score = st.sidebar.slider("Minimum risk score", 0, 4, 0)
    industries = st.sidebar.multiselect(
        "Industry", sorted(risk_df["industry"].dropna().unique().tolist())
    )
    countries = st.sidebar.multiselect(
        "Country", sorted(risk_df["country"].dropna().unique().tolist())
    )
    status_filter = st.sidebar.multiselect(
        "Customer status", sorted(risk_df["customer_status"].dropna().unique().tolist())
    )

    filtered = risk_df[risk_df["risk_score"] >= min_score]
    if industries:
        filtered = filtered[filtered["industry"].isin(industries)]
    if countries:
        filtered = filtered[filtered["country"].isin(countries)]
    if status_filter:
        filtered = filtered[filtered["customer_status"].isin(status_filter)]

    st.caption(f"Showing {len(filtered)} of {len(risk_df)} customers")

    cc1, cc2 = st.columns(2)
    with cc1:
        st.subheader("Risk Score by Industry")
        by_industry = filtered.groupby("industry")["risk_score"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(by_industry, x="industry", y="risk_score", labels={"risk_score": "Avg. Risk Score"})
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with cc2:
        st.subheader("Flag Breakdown (Filtered Set)")
        flag_counts = {
            "Structuring": int(filtered["structuring"].sum()),
            "Rapid Movement": int(filtered["rapid_movement"].sum()),
            "High-Risk Country": int(filtered["high_risk_country"].sum()),
            "Screening Hit": int(filtered["screening_hit"].sum()),
        }
        fig2 = px.bar(
            x=list(flag_counts.keys()), y=list(flag_counts.values()),
            labels={"x": "Flag Type", "y": "Customers Flagged"},
            color=list(flag_counts.keys()),
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Customer Risk Table")
    display_cols = [
        "customer_id", "full_name", "customer_type", "country", "industry",
        "customer_status", "structuring", "rapid_movement", "high_risk_country",
        "screening_hit", "risk_score",
    ]
    st.dataframe(
        filtered[display_cols].sort_values("risk_score", ascending=False),
        use_container_width=True, height=500,
    )
    csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered results as CSV", csv, "customer_risk_filtered.csv", "text/csv")

# ------------------------------------------------------------------
# TAB 3 — SCREENING
# ------------------------------------------------------------------
with tab_screen:
    st.subheader("🔎 PEP / Sanctions / Adverse Media Screening")

    st.sidebar.header("Filters — Screening")
    type_filter = st.sidebar.multiselect(
        "Screening type", sorted(screening_df["screening_type"].unique().tolist())
    )
    status_filter_s = st.sidebar.multiselect(
        "Status", sorted(screening_df["status"].unique().tolist())
    )

    sf = screening_df.copy()
    if type_filter:
        sf = sf[sf["screening_type"].isin(type_filter)]
    if status_filter_s:
        sf = sf[sf["status"].isin(status_filter_s)]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Screening Records", len(screening_df))
    c2.metric("Potential Matches", int((screening_df["status"] == "Potential Match").sum()))
    c3.metric("Confirmed Matches", int((screening_df["status"] == "Confirmed Match").sum()))

    st.divider()
    cc1, cc2 = st.columns(2)
    with cc1:
        st.subheader("Outcomes by Screening Type")
        grouped = screening_df.groupby(["screening_type", "status"]).size().reset_index(name="count")
        fig = px.bar(
            grouped, x="screening_type", y="count", color="status", barmode="stack",
            color_discrete_map={
                "Clear": "#2ecc71",
                "Potential Match": "#f39c12",
                "Confirmed Match": "#c0392b",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with cc2:
        st.subheader("Overall Outcome Split")
        fig2 = px.pie(
            screening_df, names="status", hole=0.5, color="status",
            color_discrete_map={
                "Clear": "#2ecc71",
                "Potential Match": "#f39c12",
                "Confirmed Match": "#c0392b",
            },
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Screening Records")
    sf = sf.copy()
    status_order = {"Confirmed Match": 0, "Potential Match": 1, "Clear": 2}
    sf["_sort"] = sf["status"].map(status_order)
    sf = sf.sort_values(["_sort", "customer_id"]).drop(columns="_sort")
    st.dataframe(sf, use_container_width=True, height=500)

    csv = sf.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered results as CSV", csv, "screening_filtered.csv", "text/csv")

# ------------------------------------------------------------------
# TAB 4 — TRANSACTION MONITORING
# ------------------------------------------------------------------
with tab_txn:
    st.subheader("💰 Transaction Monitoring Rules")

    t1, t2, t3, t4 = st.tabs([
        "🧱 Structuring", "⚡ Rapid Movement", "🌍 High-Risk Country Wires", "🔍 Customer Drill-Down"
    ])

    with t1:
        st.markdown("**Structuring** — Cash Deposits Just Under $10,000 Threshold")
        st.caption("3+ Cash Deposits between $9,000–$9,999 for the same customer within a 7-day window.")
        c1, c2 = st.columns(2)
        c1.metric("Customers Flagged", len(structuring_df))
        c2.metric("Total Structured Amount", f"${structuring_df['total_amount'].sum():,.2f}")
        st.dataframe(structuring_df, use_container_width=True, height=400)

    with t2:
        st.markdown("**Rapid Movement** — Large Deposit Followed by Near-Immediate Outflow")
        st.caption("Deposit ≥ $8,000 followed within 2 days by a Wire Transfer or Withdrawal.")
        c1, c2 = st.columns(2)
        c1.metric("Pattern Instances", len(rapid_df))
        c2.metric(
            "To High-Risk Country",
            int(rapid_df["counterparty_country"].isin(list(HIGH_RISK_COUNTRIES)).sum()),
        )
        st.dataframe(rapid_df, use_container_width=True, height=400)

    with t3:
        st.markdown("**Wire Transfers to High-Risk Jurisdictions**")
        c1, c2 = st.columns(2)
        c1.metric("Wires Flagged", len(highrisk_df))
        c2.metric("Total Amount", f"${highrisk_df['amount'].sum():,.2f}")
        if not highrisk_df.empty:
            fig = px.bar(
                highrisk_df.groupby("counterparty_country")["amount"].sum().reset_index(),
                x="counterparty_country", y="amount",
                labels={"amount": "Total AUD", "counterparty_country": "Country"},
            )
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(highrisk_df, use_container_width=True, height=350)

    with t4:
        st.markdown("**Per-Customer Transaction Timeline**")
        all_customers = risk_df.sort_values("risk_score", ascending=False)["customer_id"].tolist()
        selected = st.selectbox("Select customer", all_customers)

        txns = customer_transactions(selected)
        st.write(f"**{len(txns)} transactions** for `{selected}`")

        if not txns.empty:
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
    if not txn_type_df.empty:
        fig3 = px.pie(txn_type_df, names="transaction_type", values="total_amount", hole=0.4)
        st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------------------------
# TAB 5 — CASE MANAGEMENT & SAR
# ------------------------------------------------------------------
with tab_sar:
    st.subheader("📄 Case Management & SAR Generation")
    st.caption(
        "Chọn khách hàng bị flag để sinh tự động báo cáo SAR từ profile, "
        "kết quả screening và lịch sử giao dịch."
    )

    st.sidebar.header("Filters — Case Queue")
    min_score_sar = st.sidebar.slider("Minimum risk score in queue", 0, 4, 2)

    queue = risk_df[risk_df["risk_score"] >= min_score_sar].sort_values("risk_score", ascending=False)
    st.markdown(f"**Case Queue** — {len(queue)} customers with risk score ≥ {min_score_sar}")

    if not queue.empty:
        st.dataframe(
            queue[["customer_id", "full_name", "country", "industry", "customer_status",
                   "structuring", "rapid_movement", "high_risk_country", "screening_hit", "risk_score"]],
            use_container_width=True, height=250,
        )

    st.divider()
    st.subheader("Generate SAR for a Case")

    if queue.empty:
        st.info("Không có khách hàng nào đạt ngưỡng risk score đã chọn.")
    else:
        selected_customer = st.selectbox("Select customer_id", queue["customer_id"].tolist())
        analyst_name = st.text_input("Analyst name (appears on the report)", value="Brian Phu")

        if st.button("Generate SAR Narrative", type="primary"):
            profile_df = customer_profile(selected_customer)
            screening_c = customer_screening(selected_customer)
            txns_c = customer_transactions(selected_customer)

            if profile_df.empty:
                st.error("Customer not found.")
            else:
                narrative = generate_sar_narrative(
                    selected_customer, profile_df.iloc[0], screening_c, txns_c, analyst_name
                )
                st.session_state["sar_narrative"] = narrative
                st.session_state["sar_customer"] = selected_customer

        if ("sar_narrative" in st.session_state
                and st.session_state.get("sar_customer") == selected_customer):
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
                    docx_bytes = narrative_to_docx_bytes(st.session_state["sar_narrative"])
                    st.download_button(
                        "Download as .docx",
                        docx_bytes,
                        file_name=f"SAR_{selected_customer}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                except ImportError:
                    st.warning("Cài `python-docx` để bật export .docx.")