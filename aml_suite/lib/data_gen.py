"""
data_gen.py
Synthetic data generator for the AML/CTF Compliance Suite.

Design intent (see 01_business_design.md):
  - Customers carry the four AUSTRAC risk-factor categories (customer type,
    jurisdiction, service/product, delivery channel) as raw attributes -
    NOT a pre-baked risk label. The risk engine (risk_engine.py) computes
    the rating from these attributes at runtime, the same way a real
    system would, so the rating is always explainable back to source data.
  - Roughly 6-8% of customers are seeded as "latent bad actors" who exhibit
    ONE OR MORE of the typologies from the business design. Their
    transactions are generated to fit the typology pattern but are mixed
    into the same date range, same trust accounts, and same matter types
    as everyone else - there is no separate "flagged" table and no field
    that says "this is suspicious". Detection has to come from the
    typology logic in risk_engine.py, exactly like a real monitoring
    system, not from a hidden label leaking into the UI.
  - Most "elevated" transactions are noise: a big genuine settlement, a
    cash-intensive but legitimate client, a one-off round number. The
    point is that a naive ">$10,000" rule would flag far too many
    innocent transactions and miss the real patterns - which is the
    exact failure mode this project is designed to avoid.

Run this module directly to (re)generate all CSVs into ../data/.
"""

import numpy as np
import pandas as pd
from faker import Faker
import random
import datetime as dt
import os

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_AU")
Faker.seed(SEED)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

TODAY = dt.date(2026, 9, 22)
LOOKBACK_DAYS = 540  # ~18 months of activity

# ---------------------------------------------------------------------------
# REFERENCE DATA
# ---------------------------------------------------------------------------

HIGH_RISK_JURISDICTIONS = [
    "Myanmar", "Democratic People's Republic of Korea", "Iran",
    "Democratic Republic of Congo", "Yemen",
]
MEDIUM_RISK_JURISDICTIONS = [
    "United Arab Emirates", "Cyprus", "Panama", "Cambodia", "Vanuatu",
]
LOW_RISK_JURISDICTIONS = [
    "Australia", "New Zealand", "United Kingdom", "United States",
    "Canada", "Singapore", "Japan", "Germany",
]

MATTER_TYPES = [
    "Residential Conveyancing", "Commercial Conveyancing",
    "Company Formation", "Trust Establishment",
    "Business Sale & Purchase", "Debt Financing Transaction",
    "Estate Administration", "Nominee Director Arrangement",
    "Nominee Shareholder Arrangement",
]

DESIGNATED_SERVICE_ITEMS = {
    "Residential Conveyancing": "Item 3 - Managing client money in a transaction",
    "Commercial Conveyancing": "Item 3 - Managing client money in a transaction",
    "Company Formation": "Item 7 - Acting as director/secretary for a client entity",
    "Trust Establishment": "Item 7 - Acting as trustee for a client entity",
    "Business Sale & Purchase": "Item 3 - Managing client money in a transaction",
    "Debt Financing Transaction": "Item 4 - Assisting with debt financing",
    "Estate Administration": "Item 3 - Managing client money in a transaction",
    "Nominee Director Arrangement": "Item 7 - Acting as director for a client entity",
    "Nominee Shareholder Arrangement": "Item 8 - Acting as nominee shareholder",
}

DELIVERY_CHANNELS = ["Face-to-face", "Remote (video/email only)", "Via intermediary/referrer"]

OCCUPATIONS_BY_BAND = {
    "Low":    ["Teacher", "Nurse", "Retail Manager", "Public Servant", "Tradesperson", "Administrator"],
    "Medium": ["Small Business Owner", "IT Consultant", "Real Estate Agent", "Accountant", "Engineer"],
    "High":   ["Company Director", "Investment Manager", "Import/Export Trader", "Property Developer"],
}
INCOME_BAND_RANGE = {  # annual declared income, AUD
    "Low": (45_000, 95_000),
    "Medium": (95_000, 220_000),
    "High": (220_000, 600_000),
}

PEP_LEVELS = ["Not a PEP", "Domestic PEP (low profile)", "Foreign PEP (high profile)"]

CUSTOMER_STRUCTURES = [
    "Individual", "Individual", "Individual", "Individual",  # weighted common
    "Pty Ltd Company - simple", "Pty Ltd Company - multi-layer ownership",
    "Family Trust", "Discretionary Trust", "Unit Trust",
    "Foreign-incorporated entity",
]

# ---------------------------------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------------------------------

def _pick_jurisdiction():
    r = random.random()
    if r < 0.03:
        return random.choice(HIGH_RISK_JURISDICTIONS), 2
    elif r < 0.14:
        return random.choice(MEDIUM_RISK_JURISDICTIONS), 1
    else:
        return random.choice(LOW_RISK_JURISDICTIONS), 0


def _customer_type_score(structure, pep_level, cash_intensive):
    # Structure alone is a MEDIUM factor at most - "unusually complex,
    # unclear purpose" is what makes a structure high-risk per AUSTRAC
    # guidance, not the structure type in isolation. A multi-layer company
    # or foreign entity is flagged medium; it only reaches high when
    # combined with a high-profile PEP, which is scored independently below.
    score = 0
    if structure in ("Pty Ltd Company - multi-layer ownership", "Foreign-incorporated entity"):
        score = max(score, 1)
    elif structure in ("Family Trust", "Discretionary Trust", "Unit Trust"):
        score = max(score, 1) if random.random() < 0.3 else score  # most trusts are routine estate/tax planning
    if pep_level == "Foreign PEP (high profile)":
        score = 2
    elif pep_level == "Domestic PEP (low profile)":
        score = max(score, 1)
    if cash_intensive:
        score = 2  # cash-intensive is a well-established high-impact ML factor on its own
    return score


def _service_score(matter_type):
    if matter_type in ("Nominee Director Arrangement", "Nominee Shareholder Arrangement"):
        return 2
    if matter_type in ("Trust Establishment", "Debt Financing Transaction", "Company Formation"):
        return 1
    return 0


def _channel_score(channel):
    return {"Face-to-face": 0, "Remote (video/email only)": 1, "Via intermediary/referrer": 1}[channel]


def generate_customers(n=420, bad_actor_rate=0.07):
    rows = []
    n_bad = max(6, int(n * bad_actor_rate))
    bad_actor_idx = set(random.sample(range(n), n_bad))

    for i in range(n):
        cust_id = f"CUST-{10000 + i}"
        structure = random.choice(CUSTOMER_STRUCTURES)
        is_company = structure != "Individual"
        jurisdiction, jur_score = _pick_jurisdiction()

        pep_roll = random.random()
        pep_level = "Foreign PEP (high profile)" if pep_roll < 0.012 else (
            "Domestic PEP (low profile)" if pep_roll < 0.04 else "Not a PEP")

        cash_intensive = random.random() < 0.035
        matter_type = random.choice(MATTER_TYPES)
        channel = random.choices(DELIVERY_CHANNELS, weights=[0.62, 0.28, 0.10])[0]

        income_band = random.choices(["Low", "Medium", "High"], weights=[0.45, 0.4, 0.15])[0]
        occupation = random.choice(OCCUPATIONS_BY_BAND[income_band])
        income_lo, income_hi = INCOME_BAND_RANGE[income_band]
        declared_income = round(random.uniform(income_lo, income_hi), -3)

        is_bad_actor = i in bad_actor_idx
        # Bad actors are deliberately NOT pushed to obviously-high on every
        # factor - some hide behind a low-risk-looking profile (e.g. an
        # Individual, low PEP, low-risk jurisdiction) and only reveal
        # themselves through transaction behaviour (see generate_transactions).
        if is_bad_actor and random.random() < 0.5:
            # half of bad actors get ONE elevated structural factor
            structure = random.choice([
                "Pty Ltd Company - multi-layer ownership", "Foreign-incorporated entity",
                "Nominee Director Arrangement" if False else structure,  # keep structure field clean
            ])
            if random.random() < 0.4:
                jurisdiction, jur_score = random.choice(HIGH_RISK_JURISDICTIONS), 2

        cust_type_score = _customer_type_score(structure, pep_level, cash_intensive)
        service_score = _service_score(matter_type)
        channel_score = _channel_score(channel)

        onboarded = TODAY - dt.timedelta(days=random.randint(30, LOOKBACK_DAYS + 200))

        rows.append(dict(
            customer_id=cust_id,
            display_name=fake.company() if is_company else fake.name(),
            structure=structure,
            is_company=is_company,
            jurisdiction=jurisdiction,
            pep_level=pep_level,
            cash_intensive_business=cash_intensive,
            primary_matter_type=matter_type,
            designated_service=DESIGNATED_SERVICE_ITEMS[matter_type],
            delivery_channel=channel,
            occupation=occupation,
            declared_annual_income_aud=declared_income,
            onboarded_date=onboarded,
            customer_type_score=cust_type_score,
            jurisdiction_score=jur_score,
            service_score=service_score,
            channel_score=channel_score,
            _is_seeded_bad_actor=is_bad_actor,  # kept for generator QA only;
                                                 # dropped before app sees it
        ))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# TRUST ACCOUNT TRANSACTIONS
# ---------------------------------------------------------------------------

def _normal_transaction_amount(matter_type):
    ranges = {
        "Residential Conveyancing": (15_000, 850_000),
        "Commercial Conveyancing": (80_000, 3_200_000),
        "Company Formation": (500, 15_000),
        "Trust Establishment": (1_000, 40_000),
        "Business Sale & Purchase": (25_000, 1_500_000),
        "Debt Financing Transaction": (50_000, 2_000_000),
        "Estate Administration": (5_000, 900_000),
        "Nominee Director Arrangement": (500, 8_000),
        "Nominee Shareholder Arrangement": (500, 8_000),
    }
    lo, hi = ranges.get(matter_type, (1_000, 100_000))
    # log-uniform so it isn't a flat, obviously-synthetic distribution
    return round(float(np.exp(np.random.uniform(np.log(lo), np.log(hi)))), 2)


def generate_transactions(customers_df, avg_txns_per_customer=6):
    rows = []
    txn_counter = 0

    for _, cust in customers_df.iterrows():
        n_txns = max(1, int(np.random.poisson(avg_txns_per_customer)))
        is_bad = cust["_is_seeded_bad_actor"]
        onboarded = cust["onboarded_date"]
        window_start = max(onboarded, TODAY - dt.timedelta(days=LOOKBACK_DAYS))

        # decide which typology (if any) this bad actor expresses -
        # not all seeded bad actors get every typology; mix it up
        typology_roll = None
        if is_bad:
            typology_roll = random.choice([
                "structuring", "pass_through", "third_party_mismatch",
                "income_mismatch", "jurisdiction_nexus",
            ])

        matter_type = cust["primary_matter_type"]
        matter_id = f"MTR-{cust['customer_id'][-5:]}-{random.randint(1,9)}"

        if typology_roll == "structuring" and random.random() < 0.8:
            # several deposits just under an internal threshold ($10k), close together
            threshold = 10_000
            n_struct = random.randint(3, 6)
            base_date = window_start + dt.timedelta(
                days=random.randint(0, max(1, (TODAY - window_start).days - 14)))
            for k in range(n_struct):
                amt = round(random.uniform(threshold * 0.82, threshold * 0.985), 2)
                txn_counter += 1
                rows.append(_txn_row(txn_counter, cust, matter_id, matter_type,
                                      base_date + dt.timedelta(days=k * random.randint(1, 3)),
                                      "Deposit", amt, "Trust receipt - client funds"))
            n_txns = max(0, n_txns - n_struct)

        elif typology_roll == "pass_through" and random.random() < 0.8:
            base_date = window_start + dt.timedelta(
                days=random.randint(0, max(1, (TODAY - window_start).days - 10)))
            amt = _normal_transaction_amount(matter_type)
            txn_counter += 1
            rows.append(_txn_row(txn_counter, cust, matter_id, matter_type, base_date,
                                  "Deposit", amt, "Trust receipt - client funds"))
            out_date = base_date + dt.timedelta(days=random.randint(1, 3))
            txn_counter += 1
            rows.append(_txn_row(txn_counter, cust, matter_id, matter_type, out_date,
                                  "Withdrawal", round(amt * random.uniform(0.94, 0.99), 2),
                                  "Trust disbursement - third party"))
            n_txns = max(0, n_txns - 2)

        elif typology_roll == "third_party_mismatch" and random.random() < 0.8:
            base_date = window_start + dt.timedelta(
                days=random.randint(0, max(1, (TODAY - window_start).days - 5)))
            amt = _normal_transaction_amount(matter_type)
            txn_counter += 1
            rows.append(_txn_row(txn_counter, cust, matter_id, matter_type, base_date,
                                  "Deposit", amt, "Trust receipt - third party (unrelated to matter)",
                                  unrelated_third_party=True))
            n_txns = max(0, n_txns - 1)

        elif typology_roll == "income_mismatch" and random.random() < 0.8:
            # Only meaningful for matter types where the deposit SHOULD
            # roughly track the client's own means (company formation,
            # trust establishment, nominee arrangements) - not a
            # conveyancing settlement, where a big number is normal.
            base_date = window_start + dt.timedelta(
                days=random.randint(0, max(1, (TODAY - window_start).days - 5)))
            inflated = cust["declared_annual_income_aud"] * random.uniform(7, 14)
            txn_counter += 1
            im_matter_type = matter_type if matter_type in (
                "Company Formation", "Trust Establishment",
                "Nominee Director Arrangement", "Nominee Shareholder Arrangement",
            ) else "Trust Establishment"
            rows.append(_txn_row(txn_counter, cust, matter_id, im_matter_type, base_date,
                                  "Deposit", round(inflated, 2), "Trust receipt - client funds"))
            n_txns = max(0, n_txns - 1)

        elif typology_roll == "jurisdiction_nexus" and random.random() < 0.8:
            base_date = window_start + dt.timedelta(
                days=random.randint(0, max(1, (TODAY - window_start).days - 5)))
            amt = _normal_transaction_amount(matter_type)
            txn_counter += 1
            rows.append(_txn_row(txn_counter, cust, matter_id, matter_type, base_date,
                                  "Deposit", amt, "Trust receipt - international wire",
                                  counterparty_country=random.choice(HIGH_RISK_JURISDICTIONS)))
            n_txns = max(0, n_txns - 1)

        # remaining/normal transactions for this customer (noise, incl. for
        # bad actors who need cover activity, and ALL normal customers)
        for _ in range(n_txns):
            t_date = window_start + dt.timedelta(
                days=random.randint(0, max(1, (TODAY - window_start).days)))
            amt = _normal_transaction_amount(matter_type)
            kind = random.choices(["Deposit", "Withdrawal"], weights=[0.55, 0.45])[0]
            desc = "Trust receipt - client funds" if kind == "Deposit" else "Trust disbursement - settlement"
            txn_counter += 1
            rows.append(_txn_row(txn_counter, cust, matter_id, matter_type, t_date, kind, amt, desc))

    df = pd.DataFrame(rows)
    df = df.sort_values("txn_date").reset_index(drop=True)
    return df


def _txn_row(counter, cust, matter_id, matter_type, t_date, kind, amount, description,
             unrelated_third_party=False, counterparty_country=None):
    return dict(
        txn_id=f"TXN-{100000 + counter}",
        customer_id=cust["customer_id"],
        matter_id=matter_id,
        matter_type=matter_type,
        txn_date=t_date,
        txn_type=kind,
        amount_aud=amount,
        description=description,
        unrelated_third_party=unrelated_third_party,
        counterparty_country=counterparty_country or cust["jurisdiction"],
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def build_and_save():
    customers = generate_customers()
    transactions = generate_transactions(customers)

    customers_public = customers.drop(columns=["_is_seeded_bad_actor"])
    customers_public.to_csv(os.path.join(OUT_DIR, "customers.csv"), index=False)
    transactions.to_csv(os.path.join(OUT_DIR, "transactions.csv"), index=False)

    # QA copy retained only for generator development - not read by the app
    customers.to_csv(os.path.join(OUT_DIR, "_customers_with_labels_QA_ONLY.csv"), index=False)

    print(f"customers: {len(customers)} rows ({customers['_is_seeded_bad_actor'].sum()} seeded bad actors)")
    print(f"transactions: {len(transactions)} rows")
    return customers_public, transactions


if __name__ == "__main__":
    build_and_save()
