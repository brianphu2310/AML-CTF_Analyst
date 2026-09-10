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
    for i, cid in enumerate(candidates[:n_cases], start=1):
        priority = rng.choice(["Critical", "High", "Medium"], p=[0.2, 0.45, 0.35])
        status = rng.choice(["Open", "Under Investigation", "Pending SMR Lodgement", "Closed - No Action", "SMR Lodged"],
                             p=[0.28, 0.27, 0.15, 0.15, 0.15])
        rows.append({
            "case_id": f"CASE{i:04d}",
            "customer_id": cid,
            "opened_date": pd.Timestamp.today().normalize() - pd.Timedelta(days=int(rng.integers(1, 90))),
            "priority": priority,
            "status": status,
            "assigned_analyst": rng.choice(analysts),
            "typology": rng.choice(_TYPOLOGIES),
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
    else:
        customers = run_query("SELECT * FROM customers")
        transactions = run_query("SELECT * FROM transactions")
        screening = run_query("SELECT * FROM screening_hits")
        cases = run_query("SELECT * FROM cases")
        businesses = run_query("SELECT * FROM businesses")
        ubo = run_query("SELECT * FROM ubo")

    return {
        "customers": customers,
        "transactions": transactions,
        "screening": screening,
        "cases": cases,
        "businesses": businesses,
        "ubo": ubo,
    }
