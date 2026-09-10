"""
Generates a SAR-style (Suspicious Activity Report) narrative for a given
customer, based on their profile, screening results, and transaction
monitoring rule hits. Used by the Case Management & SAR page.
"""

from datetime import date
import pandas as pd
import io

HIGH_RISK_COUNTRIES = {"Iran", "North Korea", "Myanmar", "Syria", "Yemen"}


def find_structuring_clusters(txns: pd.DataFrame):
    """Return list of (dates, amounts, total) for cash-deposit clusters
    of >=3 deposits between $9,000-$9,999 within a 7-day window."""
    cash = txns[
        (txns["transaction_type"] == "Cash Deposit")
        & (txns["amount"] >= 9000)
        & (txns["amount"] <= 9999)
    ].sort_values("transaction_date")

    clusters = []
    used = set()
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
    """Return list of (deposit_row, outflow_row) pairs where a deposit
    >= $8,000 is followed within 2 days by a Wire Transfer/Withdrawal."""
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


def generate_sar_narrative(customer_id: str, profile: pd.Series,
                             screening: pd.DataFrame, txns: pd.DataFrame,
                             analyst_name: str = "[Your name]") -> str:
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

    lines = []
    lines.append("SUSPICIOUS ACTIVITY REPORT (SAR) — CASE FILE")
    lines.append("=" * 60)
    lines.append(f"Case Reference: AML-{date.today().year}-{customer_id[-4:]}")
    lines.append(f"Prepared by: {analyst_name}")
    lines.append(f"Date prepared: {today}")
    lines.append(f"Composite Risk Score: {risk_score} / 4")
    lines.append("")

    # Section 1
    lines.append("1. SUBJECT INFORMATION")
    lines.append("-" * 60)
    lines.append(f"Customer ID:        {customer_id}")
    lines.append(f"Name:               {profile.get('full_name', 'N/A')}")
    lines.append(f"Customer Type:      {profile.get('customer_type', 'N/A')}")
    lines.append(f"Date of Birth:      {profile.get('date_of_birth', 'N/A')}")
    lines.append(f"Country:            {profile.get('country', 'N/A')}")
    lines.append(f"Residency:          {profile.get('residency_country', 'N/A')}")
    lines.append(f"Industry:           {profile.get('industry', 'N/A')}")
    lines.append(f"Occupation:         {profile.get('occupation', 'N/A')}")
    lines.append(f"Declared Income:    {profile.get('annual_income', 'N/A')}")
    lines.append(f"Account Opened:     {profile.get('account_open_date', 'N/A')}")
    lines.append(f"Account Status:     {profile.get('customer_status', 'N/A')}")
    lines.append("")

    # Section 2
    lines.append("2. SCREENING FINDINGS")
    lines.append("-" * 60)
    if screening.empty:
        lines.append("No screening records found for this customer.")
    else:
        for _, row in screening.iterrows():
            detail = f" — {row['match_details']}" if pd.notna(row.get("match_details")) and row.get("match_details") else ""
            lines.append(f"{row['screening_type']:<15} {row['status']:<18}{detail}")
    lines.append("")

    # Section 3
    lines.append("3. TRANSACTION PATTERN ANALYSIS")
    lines.append("-" * 60)

    if structuring_clusters:
        for idx, cluster in enumerate(structuring_clusters, start=1):
            total = cluster["amount"].sum()
            start = cluster["transaction_date"].min()
            end = cluster["transaction_date"].max()
            lines.append(f"a{idx}) Structuring cluster: {len(cluster)} cash deposits between "
                         f"{start} and {end}, totaling ${total:,.2f} AUD, all just under the "
                         f"$10,000 reporting threshold.")
            for _, r in cluster.iterrows():
                lines.append(f"     - {r['transaction_date']}: ${r['amount']:,.2f} ({r['channel']})")
    else:
        lines.append("No structuring pattern detected.")
    lines.append("")

    if rapid_pairs:
        for idx, (dep, out) in enumerate(rapid_pairs, start=1):
            pct = (out["amount"] / dep["amount"]) * 100 if dep["amount"] else 0
            lines.append(f"b{idx}) Rapid movement: deposit of ${dep['amount']:,.2f} on "
                         f"{dep['transaction_date']} followed by {out['transaction_type']} of "
                         f"${out['amount']:,.2f} to {out['counterparty_country']} on "
                         f"{out['transaction_date']} ({pct:.0f}% of deposit passed through "
                         f"within {(out['transaction_date'] - dep['transaction_date']).days} day(s)).")
    else:
        lines.append("No rapid movement pattern detected.")
    lines.append("")

    if not high_risk_wires.empty:
        lines.append("c) Wire transfers to high-risk jurisdictions:")
        for _, r in high_risk_wires.iterrows():
            lines.append(f"     - {r['transaction_date']}: ${r['amount']:,.2f} to {r['counterparty_country']}")
    else:
        lines.append("No wire transfers to high-risk jurisdictions detected.")
    lines.append("")

    # Section 4 - Red flags
    lines.append("4. RED FLAGS SUMMARY")
    lines.append("-" * 60)
    flag_num = 1
    if has_pep:
        lines.append(f"{flag_num}. PEP screening hit not yet resolved via Enhanced Due Diligence (EDD).")
        flag_num += 1
    if has_sanctions:
        lines.append(f"{flag_num}. Sanctions screening hit — requires immediate escalation.")
        flag_num += 1
    if has_adverse:
        lines.append(f"{flag_num}. Adverse media hit — requires manual review of source article(s).")
        flag_num += 1
    if structuring_clusters:
        lines.append(f"{flag_num}. Structuring — multiple deposits just under the reporting threshold.")
        flag_num += 1
    if rapid_pairs:
        lines.append(f"{flag_num}. Rapid pass-through of funds shortly after deposit.")
        flag_num += 1
    if not high_risk_wires.empty:
        lines.append(f"{flag_num}. Funds transferred to a high-risk/sanctioned-adjacent jurisdiction.")
        flag_num += 1
    if flag_num == 1:
        lines.append("No red flags identified based on current monitoring rules.")
    lines.append("")

    # Section 5 - Recommendation
    lines.append("5. RECOMMENDATION")
    lines.append("-" * 60)
    if risk_score >= 3:
        lines.append("Escalate to Senior Compliance Officer. Recommend filing a Suspicious")
        lines.append("Matter Report (SMR) with AUSTRAC pending Enhanced Due Diligence outcome.")
        lines.append("Flag account for enhanced ongoing monitoring.")
    elif risk_score == 2:
        lines.append("Recommend Enhanced Due Diligence (EDD) and a follow-up review within")
        lines.append("30 days. Escalate to team lead if further red flags emerge.")
    else:
        lines.append("Continue standard monitoring. No immediate escalation required.")

    return "\n".join(lines)


def narrative_to_docx_bytes(narrative: str, customer_id: str) -> bytes:
    """Convert the plain-text SAR narrative into a downloadable .docx file."""
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
