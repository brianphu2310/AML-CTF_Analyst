"""
db_utils.py
Central data-access layer for the AML Compliance Suite.

Two modes:
  1. LIVE  -> set USE_DEMO_DATA = False and fill in DB_CONFIG to pull from
             your real Postgres warehouse (customers, transactions,
             screening_hits, cases, businesses, ubo tables).
  2. DEMO  -> USE_DEMO_DATA = True (default) generates a realistic,
             internally-consistent synthetic dataset on the fly so the
             whole suite runs out of the box with no infrastructure.

Every page in /pages imports its data exclusively through the functions
below, so switching modes only requires editing this one file.
"""

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

import report_utils

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
USE_DEMO_DATA = True  # flip to False once DB_CONFIG points at a real database

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "aml_platform",
    "user": "postgres",
    "password": "postgres",
}


@st.cache_resource
def get_engine():
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    return create_engine(url, pool_pre_ping=True)


def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Run raw SQL against the live database. Only used when USE_DEMO_DATA=False."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})


# --------------------------------------------------------------------------
# SYNTHETIC DEMO DATA GENERATOR
# --------------------------------------------------------------------------
_FIRST_NAMES = [
    "James", "Mia", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Lucas",
    "Isabella", "Minh", "Linh", "Wei", "Yuki", "Arjun", "Priya", "Carlos",
    "Fatima", "Dmitri", "Elena", "Kwame", "Amara", "Sione", "Aroha", "Tama",
]
_LAST_NAMES = [
    "Nguyen", "Tran", "Smith", "Johnson", "Chen", "Wang", "Patel", "Kumar",
    "Garcia", "Rossi", "Ivanov", "Petrov", "Silva", "Okafor", "Fale", "Wilson",
    "Brown", "Taylor", "Anderson", "Lee", "Kim", "Sato", "Hoang", "Vu",
]
_BUSINESS_WORDS_1 = [
    "Pacific", "Southern", "Golden", "Meridian", "Horizon", "Summit", "Coastal",
    "Union", "Sterling", "Crown", "Apex", "Global", "Harbour", "Ironbark",
]
_BUSINESS_WORDS_2 = [
    "Trading", "Holdings", "Logistics", "Capital", "Ventures", "Imports",
    "Exchange", "Resources", "Consulting", "Property Group", "Freight", "Metals",
]
_INDUSTRIES = [
    "Import/Export", "Construction", "Real Estate", "Hospitality", "Retail",
    "Remittance/MSB", "Wholesale Trade", "Precious Metals", "Used Vehicle Sales",
    "Digital Currency Exchange", "Professional Services", "Freight & Logistics",
]
_COUNTRIES = [
    "Australia", "China", "Vietnam", "UAE", "Hong Kong", "Singapore", "USA",
    "United Kingdom", "Cambodia", "Papua New Guinea", "Fiji", "Cyprus", "Panama",
    "Nigeria", "Myanmar", "New Zealand",
]
_HIGH_RISK_COUNTRIES = {"Myanmar", "Cambodia", "Panama", "Cyprus", "Nigeria", "Papua New Guinea"}
_CHANNELS = ["International Wire", "Domestic EFT", "Cash Deposit", "Cash Withdrawal", "Crypto Transfer", "Bank Cheque"]
_TYPOLOGIES = [
    "Structuring (Smurfing)", "Rapid Movement of Funds", "Trade-Based ML",
    "Third-Party Layering", "High-Risk Corridor Wires", "Unexplained Wealth",
    "Shell Company Activity", "Round-Tripping",
]
_ADVERSE_MEDIA_TERMS = [
    "fraud investigation", "tax evasion probe", "customs seizure", "bribery allegation",
    "asset freezing order", "organised crime reporting", "sanctions evasion network",
]


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


@st.cache_data(ttl=3600)
def load_customers(n: int = 260) -> pd.DataFrame:
    rng = _rng(1)
    rows = []
    for i in range(1, n + 1):
        cid = f"CUST{i:04d}"
        is_business = rng.random() < 0.32
        if is_business:
            name = f"{rng.choice(_BUSINESS_WORDS_1)} {rng.choice(_BUSINESS_WORDS_2)} {'Pty Ltd' if rng.random()<0.7 else 'Ltd'}"
            cust_type = "Business"
            occupation = "N/A"
        else:
            name = f"{rng.choice(_FIRST_NAMES)} {rng.choice(_LAST_NAMES)}"
            cust_type = "Individual"
            occupation = rng.choice(
                ["Company Director", "Trader", "Retail Manager", "Consultant",
                 "Property Developer", "Import/Export Agent", "Unemployed",
                 "Student", "Restaurant Owner", "Financial Advisor"]
            )
        country = rng.choice(_COUNTRIES, p=_weighted(_COUNTRIES))
        industry = rng.choice(_INDUSTRIES)

        base_risk = rng.integers(5, 55)
        if country in _HIGH_RISK_COUNTRIES:
            base_risk += rng.integers(15, 30)
        if industry in ("Remittance/MSB", "Precious Metals", "Digital Currency Exchange", "Used Vehicle Sales"):
            base_risk += rng.integers(10, 25)
        risk_score = int(np.clip(base_risk, 1, 99))

        if risk_score >= 80:
            risk_level = "Critical"
        elif risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 35:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        status = rng.choice(["Active", "Active", "Active", "Dormant", "Closed"])
        onboarding_days_ago = int(rng.integers(30, 2200))
        onboarding_date = pd.Timestamp.today().normalize() - pd.Timedelta(days=onboarding_days_ago)

        rows.append({
            "customer_id": cid,
            "name": name,
            "customer_type": cust_type,
            "occupation": occupation,
            "industry": industry,
            "country": country,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "status": status,
            "onboarding_date": onboarding_date,
        })
    return pd.DataFrame(rows)


def _weighted(countries):
    # Australia dominant, rest tail distribution
    w = np.array([8 if c == "Australia" else 1 for c in countries], dtype=float)
    return w / w.sum()


@st.cache_data(ttl=3600)
def load_transactions(customers: pd.DataFrame, seed: int = 2) -> pd.DataFrame:
    rng = _rng(seed)
    rows = []
    txn_counter = 1
    today = pd.Timestamp.today().normalize()

    for _, cust in customers.iterrows():
        risk_score = cust["risk_score"]
        n_txn = int(rng.integers(15, 45) + risk_score // 3)

        # inject specific typologies for higher-risk customers
        inject_structuring = risk_score >= 60 and rng.random() < 0.5
        inject_rapid = risk_score >= 55 and rng.random() < 0.4
        inject_wire = risk_score >= 65 and rng.random() < 0.45

        for _ in range(n_txn):
            days_ago = int(rng.integers(0, 180))
            txn_date = today - pd.Timedelta(days=days_ago)
            channel = rng.choice(_CHANNELS, p=[0.18, 0.32, 0.2, 0.12, 0.1, 0.08])
            direction = rng.choice(["Inbound", "Outbound"])
            amount = float(round(rng.lognormal(mean=8.0, sigma=1.1), 2))
            amount = min(amount, 250000)
            counterparty_country = rng.choice(_COUNTRIES)
            rows.append({
                "txn_id": f"TXN{txn_counter:06d}",
                "customer_id": cust["customer_id"],
                "txn_date": txn_date,
                "amount": round(amount, 2),
                "direction": direction,
                "channel": channel,
                "counterparty_country": counterparty_country,
                "description": f"{direction} {channel.lower()}",
            })
            txn_counter += 1

        if inject_structuring:
            cluster_date = today - pd.Timedelta(days=int(rng.integers(3, 40)))
            for k in range(rng.integers(4, 7)):
                rows.append({
                    "txn_id": f"TXN{txn_counter:06d}",
                    "customer_id": cust["customer_id"],
                    "txn_date": cluster_date + pd.Timedelta(hours=int(rng.integers(0, 72))),
                    "amount": round(float(rng.uniform(8800, 9950)), 2),
                    "direction": "Inbound",
                    "channel": "Cash Deposit",
                    "counterparty_country": cust["country"],
                    "description": "Cash deposit just under reporting threshold",
                })
                txn_counter += 1

        if inject_rapid:
            in_date = today - pd.Timedelta(days=int(rng.integers(3, 60)))
            big_amt = round(float(rng.uniform(30000, 120000)), 2)
            rows.append({
                "txn_id": f"TXN{txn_counter:06d}", "customer_id": cust["customer_id"],
                "txn_date": in_date, "amount": big_amt, "direction": "Inbound",
                "channel": "International Wire", "counterparty_country": rng.choice(_COUNTRIES),
                "description": "Large inbound wire",
            })
            txn_counter += 1
            for k in range(rng.integers(2, 4)):
                rows.append({
                    "txn_id": f"TXN{txn_counter:06d}", "customer_id": cust["customer_id"],
                    "txn_date": in_date + pd.Timedelta(hours=int(rng.integers(1, 48))),
                    "amount": round(big_amt / rng.integers(2, 4), 2), "direction": "Outbound",
                    "channel": rng.choice(["International Wire", "Crypto Transfer"]),
                    "counterparty_country": rng.choice(list(_HIGH_RISK_COUNTRIES)),
                    "description": "Rapid outbound transfer following large inbound credit",
                })
                txn_counter += 1

        if inject_wire:
            for k in range(rng.integers(2, 5)):
                rows.append({
                    "txn_id": f"TXN{txn_counter:06d}", "customer_id": cust["customer_id"],
                    "txn_date": today - pd.Timedelta(days=int(rng.integers(1, 90))),
                    "amount": round(float(rng.uniform(15000, 95000)), 2),
                    "direction": rng.choice(["Inbound", "Outbound"]),
                    "channel": "International Wire",
                    "counterparty_country": rng.choice(list(_HIGH_RISK_COUNTRIES)),
                    "description": "Wire to/from high-risk jurisdiction",
                })
                txn_counter += 1

    df = pd.DataFrame(rows)
    df["txn_date"] = pd.to_datetime(df["txn_date"])
    return df.sort_values("txn_date").reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_screening(customers: pd.DataFrame, seed: int = 3) -> pd.DataFrame:
    rng = _rng(seed)
    rows = []
    sid = 1
    for _, cust in customers.iterrows():
        n_hits = 0
        if cust["risk_score"] >= 70:
            n_hits = rng.integers(1, 3)
        elif rng.random() < 0.08:
            n_hits = 1
        for _ in range(n_hits):
            match_type = rng.choice(["PEP", "Sanctions", "Adverse Media"], p=[0.4, 0.15, 0.45])
            if match_type == "PEP":
                detail = rng.choice(["Foreign PEP - Government Official", "Domestic PEP - Local Council",
                                      "PEP Family Member", "PEP Close Associate"])
                source = "World-Check / Dow Jones PEP List"
            elif match_type == "Sanctions":
                detail = rng.choice(["DFAT Consolidated List", "OFAC SDN List", "UN Security Council List"])
                source = "Sanctions Watchlist"
            else:
                detail = rng.choice(_ADVERSE_MEDIA_TERMS).capitalize()
                source = rng.choice(["Reuters", "Factiva", "LexisNexis News Archive"])
            status = rng.choice(["Open", "Under Review", "Escalated", "Cleared - False Positive"],
                                 p=[0.35, 0.25, 0.2, 0.2])
            rows.append({
                "screening_id": f"SCR{sid:05d}",
                "customer_id": cust["customer_id"],
                "match_type": match_type,
                "match_detail": detail,
                "list_source": source,
                "match_score": int(rng.integers(65, 99)),
                "status": status,
                "screened_date": pd.Timestamp.today().normalize() - pd.Timedelta(days=int(rng.integers(0, 120))),
            })
            sid += 1
    return pd.DataFrame(rows)


@st.cache_data(ttl=3600)
def load_cases(customers: pd.DataFrame, screening: pd.DataFrame, seed: int = 4) -> pd.DataFrame:
    rng = _rng(seed)
    high_risk = customers[customers["risk_score"] >= 60]
    flagged_ids = set(screening[screening["status"].isin(["Escalated", "Open"])]["customer_id"])
    candidates = pd.unique(pd.concat([high_risk["customer_id"], pd.Series(list(flagged_ids))]))
    candidates = list(candidates)
    rng.shuffle(candidates)
    n_cases = min(len(candidates), 42)
    rows = []
    analysts = ["A. Nguyen", "R. Patel", "S. Thompson", "J. Kim", "M. Silva", "L. Chen"]
    seniors = ["Compliance Manager - D. Osei", "MLRO - K. Whitfield"]
    # Full lifecycle status set - see workflow_utils.CASE_STATUSES
    statuses = ["Open", "Under Investigation", "Escalated - Senior Review", "Pending SMR Lodgement",
                "SMR Lodged", "Post-SMR Monitoring", "Closed - No Action", "Closed - Restricted / Exited"]
    status_p = [0.18, 0.20, 0.12, 0.10, 0.10, 0.08, 0.14, 0.08]
    for i, cid in enumerate(candidates[:n_cases], start=1):
        priority = rng.choice(["Critical", "High", "Medium"], p=[0.2, 0.45, 0.35])
        status = rng.choice(statuses, p=status_p)
        opened_date = pd.Timestamp.today().normalize() - pd.Timedelta(days=int(rng.integers(1, 120)))

        escalated_to = ""
        senior_decision = ""
        sof_notes = ""
        smr_reference = ""
        smr_submitted_date = pd.NaT
        if status in ("Escalated - Senior Review", "Pending SMR Lodgement", "SMR Lodged",
                      "Post-SMR Monitoring", "Closed - No Action", "Closed - Restricted / Exited"):
            escalated_to = rng.choice(seniors)
            sof_notes = "Source of funds reviewed against declared occupation/industry; " + rng.choice([
                "explanation consistent with profile.",
                "explanation only partially substantiated - further evidence requested from customer.",
                "no satisfactory explanation obtained from customer.",
            ])
        if status in ("Pending SMR Lodgement", "SMR Lodged", "Post-SMR Monitoring"):
            senior_decision = "Continue Monitoring" if status == "Post-SMR Monitoring" else "Close Case"
        if status == "Closed - No Action":
            senior_decision = "Close Case"
        if status == "Closed - Restricted / Exited":
            senior_decision = "Restrict / Exit Relationship"
        if status in ("SMR Lodged", "Post-SMR Monitoring"):
            smr_submitted_date = opened_date + pd.Timedelta(days=int(rng.integers(3, 20)))
            smr_reference = f"AUSTRAC-SMR-{smr_submitted_date.strftime('%Y%m%d')}-{i:04d}"

        rows.append({
            "case_id": f"CASE{i:04d}",
            "customer_id": cid,
            "opened_date": opened_date,
            "priority": priority,
            "status": status,
            "assigned_analyst": rng.choice(analysts),
            "typology": rng.choice(_TYPOLOGIES),
            "escalated_to": escalated_to,
            "sof_review_notes": sof_notes,
            "senior_decision": senior_decision,
            "smr_reference": smr_reference,
            "smr_submitted_date": smr_submitted_date,
            "next_review_date": opened_date + pd.DateOffset(months=int(rng.choice([3, 6, 12]))),
        })
    return pd.DataFrame(rows)


@st.cache_data(ttl=3600)
def load_businesses(n: int = 55, seed: int = 5) -> pd.DataFrame:
    rng = _rng(seed)
    rows = []
    structures = ["Pty Ltd", "Trust", "Partnership", "Sole Trader", "Public Company", "Foreign Subsidiary"]
    for i in range(1, n + 1):
        name = f"{rng.choice(_BUSINESS_WORDS_1)} {rng.choice(_BUSINESS_WORDS_2)} {rng.choice(['Pty Ltd','Group','Ltd'])}"
        country = rng.choice(_COUNTRIES, p=_weighted(_COUNTRIES))
        industry = rng.choice(_INDUSTRIES)
        risk = int(rng.integers(5, 95))
        if country in _HIGH_RISK_COUNTRIES:
            risk = int(np.clip(risk + rng.integers(10, 25), 1, 99))
        rows.append({
            "business_id": f"BUS{i:04d}",
            "legal_name": name,
            "abn": f"{rng.integers(10,99)} {rng.integers(100,999)} {rng.integers(100,999)} {rng.integers(100,999)}",
            "industry": industry,
            "incorporation_country": country,
            "incorporation_date": pd.Timestamp.today().normalize() - pd.Timedelta(days=int(rng.integers(60, 4000))),
            "structure_type": rng.choice(structures),
            "risk_rating": ("Critical" if risk >= 80 else "High" if risk >= 60 else "Medium" if risk >= 35 else "Low"),
            "risk_score": risk,
        })
    return pd.DataFrame(rows)


@st.cache_data(ttl=3600)
def load_ubo(businesses: pd.DataFrame, seed: int = 6) -> pd.DataFrame:
    """Simplified beneficial ownership register - up to 2 layers deep."""
    rng = _rng(seed)
    rows = []
    uid = 1
    for _, biz in businesses.iterrows():
        n_owners = rng.integers(1, 4)
        remaining = 100.0
        for k in range(n_owners):
            is_corporate = rng.random() < 0.35 and k < n_owners - 1
            pct = round(float(remaining if k == n_owners - 1 else rng.uniform(10, remaining * 0.6)), 1)
            remaining = max(remaining - pct, 0)
            if is_corporate:
                owner_name = f"{rng.choice(_BUSINESS_WORDS_1)} {rng.choice(_BUSINESS_WORDS_2)} Holdings"
                owner_type = "Corporate"
            else:
                owner_name = f"{rng.choice(_FIRST_NAMES)} {rng.choice(_LAST_NAMES)}"
                owner_type = "Individual"
            rows.append({
                "ubo_id": f"UBO{uid:05d}",
                "business_id": biz["business_id"],
                "owner_name": owner_name,
                "owner_type": owner_type,
                "ownership_pct": pct,
                "is_pep": bool(rng.random() < 0.06),
                "nationality": rng.choice(_COUNTRIES),
            })
            uid += 1
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# ALERT GENERATION (transaction-monitoring findings -> triage-able alerts)
# --------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_txn_alerts(customers: pd.DataFrame, transactions: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    """Runs the typology detectors per customer and turns each hit into a
    triage-able alert row, the same way a rules engine would generate an
    AML alert from a transaction-monitoring scenario."""
    rng = _rng(seed)
    rows = []
    aid = 1
    dispositions = ["New", "New", "False Positive", "Requires Investigation", "Escalated to Case"]
    for cid, grp in transactions.groupby("customer_id"):
        for f in report_utils.run_all_detections(grp):
            name = customers.loc[customers["customer_id"] == cid, "name"]
            if name.empty:
                continue
            rows.append({
                "alert_id": f"ALT{aid:05d}",
                "customer_id": cid,
                "name": name.values[0],
                "source": "Transaction Monitoring",
                "alert_type": f.typology,
                "detail": f.summary,
                "severity": f.severity,
                "generated_date": pd.Timestamp(f.evidence["txn_date"].max()).normalize(),
                "disposition": rng.choice(dispositions, p=[0.3, 0.15, 0.2, 0.2, 0.15]),
            })
            aid += 1
    return pd.DataFrame(rows)


@st.cache_data(ttl=3600)
def load_alerts(customers: pd.DataFrame, transactions: pd.DataFrame, screening: pd.DataFrame) -> pd.DataFrame:
    """Unified Alert Triage queue: watchlist screening hits + transaction-
    monitoring detections, normalised to one schema."""
    txn_alerts = load_txn_alerts(customers, transactions)

    scr = screening.merge(customers[["customer_id", "name"]], on="customer_id", how="left")
    status_to_disposition = {
        "Open": "New",
        "Under Review": "Requires Investigation",
        "Escalated": "Escalated to Case",
        "Cleared - False Positive": "False Positive",
    }
    scr_alerts = pd.DataFrame({
        "alert_id": scr["screening_id"],
        "customer_id": scr["customer_id"],
        "name": scr["name"],
        "source": "Watchlist Screening",
        "alert_type": scr["match_type"],
        "detail": scr["match_detail"] + " (" + scr["list_source"] + ")",
        "severity": scr["match_score"].apply(lambda s: "Critical" if s >= 90 else "High" if s >= 75 else "Medium"),
        "generated_date": scr["screened_date"],
        "disposition": scr["status"].map(status_to_disposition).fillna("New"),
    })

    alerts = pd.concat([scr_alerts, txn_alerts], ignore_index=True)
    return alerts.sort_values("generated_date", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------
# RECORD KEEPING / AUDIT TRAIL (seeded historical log)
# --------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_audit_log(customers: pd.DataFrame, cases: pd.DataFrame, alerts: pd.DataFrame, seed: int = 8) -> pd.DataFrame:
    """Synthetic historical record-keeping log spanning onboarding, screening
    disposition, alert triage, case escalation, SMR lodgement and periodic
    review actions - so the Audit Trail page has a realistic, consistent
    history to display even before this session's own actions are added."""
    rng = _rng(seed)
    rows = []
    eid = 1
    actors = ["A. Nguyen", "R. Patel", "S. Thompson", "J. Kim", "M. Silva", "L. Chen",
              "Compliance Manager - D. Osei", "MLRO - K. Whitfield", "System"]

    def add(ts, actor, action, entity_type, entity_id, detail):
        nonlocal eid
        rows.append({"timestamp": ts, "actor": actor, "action": action,
                      "entity_type": entity_type, "entity_id": entity_id, "detail": detail})
        eid += 1

    for _, c in customers.sample(min(120, len(customers)), random_state=seed).iterrows():
        onboard_ts = pd.Timestamp(c["onboarding_date"])
        add(onboard_ts, "System", "Onboarding Decision Recorded", "Customer", c["customer_id"],
            f"CDD tier assigned based on {c['risk_level']} risk rating; customer onboarded.")
        if c["risk_score"] >= 60:
            add(onboard_ts + pd.Timedelta(days=int(rng.integers(180, 400))), rng.choice(actors[:6]),
                "Periodic Review Completed", "Customer", c["customer_id"],
                "Scheduled risk-based periodic review completed; KYC and risk rating reconfirmed.")

    for _, a in alerts.sample(min(150, len(alerts)), random_state=seed + 1).iterrows():
        ts = pd.Timestamp(a["generated_date"]) + pd.Timedelta(hours=int(rng.integers(1, 48)))
        add(ts, rng.choice(actors[:6]), f"Alert Triaged: {a['disposition']}", "Alert", a["alert_id"],
            f"{a['source']} alert on {a['customer_id']} triaged as '{a['disposition']}'.")

    for _, cs in cases.iterrows():
        add(pd.Timestamp(cs["opened_date"]), rng.choice(actors[:6]), "Case Opened", "Case", cs["case_id"],
            f"Investigation opened for {cs['customer_id']} - typology: {cs['typology']}.")
        if cs["escalated_to"]:
            add(pd.Timestamp(cs["opened_date"]) + pd.Timedelta(days=int(rng.integers(1, 10))),
                rng.choice(actors[:6]), "Case Escalated", "Case", cs["case_id"],
                f"Escalated to {cs['escalated_to']} for senior review. {cs['sof_review_notes']}")
        if cs["senior_decision"]:
            add(pd.Timestamp(cs["opened_date"]) + pd.Timedelta(days=int(rng.integers(10, 20))),
                cs["escalated_to"] or "Compliance Manager - D. Osei", "Senior Review Decision", "Case", cs["case_id"],
                f"Decision: {cs['senior_decision']}.")
        if cs["smr_reference"]:
            add(pd.Timestamp(cs["smr_submitted_date"]), "MLRO - K. Whitfield", "SMR Lodged with AUSTRAC", "Case",
                cs["case_id"], f"Reference {cs['smr_reference']} lodged via AUSTRAC Online.")
        if cs["status"] in ("Closed - No Action", "Closed - Restricted / Exited"):
            add(pd.Timestamp(cs["opened_date"]) + pd.Timedelta(days=int(rng.integers(20, 40))),
                rng.choice(actors[:6]), "Case Closed", "Case", cs["case_id"], f"Final status: {cs['status']}.")

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# UNIFIED LOADER
# --------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_all():
    """Single entry point used by every page. Returns a dict of dataframes."""
    if USE_DEMO_DATA:
        customers = load_customers()
        transactions = load_transactions(customers)
        screening = load_screening(customers)
        cases = load_cases(customers, screening)
        businesses = load_businesses()
        ubo = load_ubo(businesses)
        alerts = load_alerts(customers, transactions, screening)
        audit_log = load_audit_log(customers, cases, alerts)
    else:
        customers = run_query("SELECT * FROM customers")
        transactions = run_query("SELECT * FROM transactions")
        screening = run_query("SELECT * FROM screening_hits")
        cases = run_query("SELECT * FROM cases")
        businesses = run_query("SELECT * FROM businesses")
        ubo = run_query("SELECT * FROM ubo")
        alerts = load_alerts(customers, transactions, screening)
        audit_log = run_query("SELECT * FROM audit_log") if False else load_audit_log(customers, cases, alerts)

    return {
        "customers": customers,
        "transactions": transactions,
        "screening": screening,
        "cases": cases,
        "businesses": businesses,
        "ubo": ubo,
        "alerts": alerts,
        "audit_log": audit_log,
    }
