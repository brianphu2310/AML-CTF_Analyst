"""
risk_engine.py
Implements the two core compliance methodologies from 01_business_design.md:

  1. Customer risk rating (AUSTRAC 4-factor model, "any high factor -> High"
     rule - see business design doc S2.2)
  2. Transaction typology detection for alert generation (S3)

Nothing here reads a hidden "is this suspicious" label from the data - every
rating and every alert is derived only from fields a real analyst would also
see (customer attributes, transaction attributes, timing).
"""

import pandas as pd
import numpy as np
import datetime as dt


# ---------------------------------------------------------------------------
# 1. CUSTOMER RISK RATING
# ---------------------------------------------------------------------------

MEDIUM_THRESHOLD = 2  # sum of factor scores (excluding any-high override)

def rate_customer(row) -> tuple[str, int, list[str]]:
    """
    Returns (rating, total_score, reasons[]).
    Implements: any single factor scoring 2 (high) overrides to HIGH,
    regardless of the other three factors - per AUSTRAC's worked example
    for risk-based customer rating (business design S2.2).
    """
    factors = {
        "Customer type": row["customer_type_score"],
        "Jurisdiction": row["jurisdiction_score"],
        "Service/product": row["service_score"],
        "Delivery channel": row["channel_score"],
    }
    total = sum(factors.values())
    reasons = []

    any_high = any(v == 2 for v in factors.values())
    for name, v in factors.items():
        if v == 2:
            reasons.append(f"{name}: HIGH-risk factor present")
        elif v == 1:
            reasons.append(f"{name}: medium-risk factor present")

    if any_high:
        rating = "High"
    elif total >= MEDIUM_THRESHOLD:
        rating = "Medium"
    else:
        rating = "Low"

    if not reasons:
        reasons = ["No elevated risk factors identified across the four AUSTRAC categories."]

    return rating, total, reasons


def apply_customer_ratings(customers_df: pd.DataFrame) -> pd.DataFrame:
    df = customers_df.copy()
    ratings, scores, reasons = [], [], []
    for _, row in df.iterrows():
        r, s, why = rate_customer(row)
        ratings.append(r)
        scores.append(s)
        reasons.append(" | ".join(why))
    df["risk_rating"] = ratings
    df["risk_score"] = scores
    df["risk_rationale"] = reasons

    # EDD trigger + review cadence, both DRIVEN by the rating (business
    # design S2.3) - not independent fields.
    df["edd_required"] = df["risk_rating"] == "High"
    df["review_cadence"] = df["risk_rating"].map({
        "Low": "36 months", "Medium": "12 months", "High": "6 months",
    })
    return df


# ---------------------------------------------------------------------------
# 2. TRANSACTION TYPOLOGY DETECTION
# ---------------------------------------------------------------------------

STRUCTURING_THRESHOLD = 10_000
STRUCTURING_WINDOW_DAYS = 10
STRUCTURING_MIN_COUNT = 3
STRUCTURING_BAND = (0.80, 1.00)  # fraction of threshold

PASS_THROUGH_WINDOW_DAYS = 4
PASS_THROUGH_MIN_RATIO = 0.90  # outflow must be >= 90% of inflow to count

INCOME_MISMATCH_MULTIPLE = 6.0  # txn amount vs declared annual income
# Matter types where a large trust receipt is EXPECTED regardless of the
# client's personal income (the money is the sale/settlement proceeds,
# not their income) - comparing income to transaction size here would be
# a naive rule that floods alerts with routine property/business deals.
INCOME_MISMATCH_EXEMPT_MATTERS = {
    "Residential Conveyancing", "Commercial Conveyancing",
    "Business Sale & Purchase", "Debt Financing Transaction",
    "Estate Administration",
}


def _detect_structuring(txns: pd.DataFrame) -> pd.DataFrame:
    """Flags clusters of deposits just under STRUCTURING_THRESHOLD within a
    short window for the same customer."""
    hits = []
    deposits = txns[
        (txns.txn_type == "Deposit")
        & (txns.amount_aud >= STRUCTURING_THRESHOLD * STRUCTURING_BAND[0])
        & (txns.amount_aud < STRUCTURING_THRESHOLD * STRUCTURING_BAND[1])
    ].sort_values(["customer_id", "txn_date"])

    for cust_id, grp in deposits.groupby("customer_id"):
        grp = grp.reset_index(drop=True)
        for i in range(len(grp)):
            window = grp[
                (grp.txn_date >= grp.loc[i, "txn_date"])
                & (grp.txn_date <= grp.loc[i, "txn_date"] + dt.timedelta(days=STRUCTURING_WINDOW_DAYS))
            ]
            if len(window) >= STRUCTURING_MIN_COUNT:
                for _, t in window.iterrows():
                    hits.append(t["txn_id"])
    return txns[txns.txn_id.isin(set(hits))].assign(
        typology="Structuring",
        typology_reason=f"Deposit just under the ${STRUCTURING_THRESHOLD:,.0f} threshold, "
                         f"part of {STRUCTURING_MIN_COUNT}+ similar deposits within "
                         f"{STRUCTURING_WINDOW_DAYS} days for this customer.",
    )


def _detect_pass_through(txns: pd.DataFrame) -> pd.DataFrame:
    """Flags a large deposit followed quickly by a near-equal withdrawal,
    for the same customer/matter, with no time for normal matter progress."""
    hits = []
    reasons = {}
    for (cust_id, matter_id), grp in txns.groupby(["customer_id", "matter_id"]):
        grp = grp.sort_values("txn_date").reset_index(drop=True)
        deposits = grp[grp.txn_type == "Deposit"]
        withdrawals = grp[grp.txn_type == "Withdrawal"]
        for _, dep in deposits.iterrows():
            later_out = withdrawals[
                (withdrawals.txn_date > dep.txn_date)
                & (withdrawals.txn_date <= dep.txn_date + dt.timedelta(days=PASS_THROUGH_WINDOW_DAYS))
                & (withdrawals.amount_aud >= dep.amount_aud * PASS_THROUGH_MIN_RATIO)
            ]
            if len(later_out) > 0 and dep.amount_aud >= 5_000:
                out = later_out.iloc[0]
                hits.extend([dep["txn_id"], out["txn_id"]])
                r = (f"Funds received then paid out again within "
                     f"{(out.txn_date - dep.txn_date).days} day(s) - inconsistent with "
                     f"normal matter progress.")
                reasons[dep["txn_id"]] = r
                reasons[out["txn_id"]] = r
    flagged = txns[txns.txn_id.isin(set(hits))].copy()
    flagged["typology"] = "Rapid movement of funds (pass-through)"
    flagged["typology_reason"] = flagged["txn_id"].map(reasons)
    return flagged


def _detect_third_party_mismatch(txns: pd.DataFrame) -> pd.DataFrame:
    flagged = txns[txns.get("unrelated_third_party", False) == True].copy()
    flagged["typology"] = "Third-party funding mismatch"
    flagged["typology_reason"] = (
        "Funds received from a party with no documented connection to the named client or matter."
    )
    return flagged


def _detect_income_mismatch(txns: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    merged = txns.merge(
        customers[["customer_id", "declared_annual_income_aud"]], on="customer_id", how="left"
    )
    mask = (
        (merged.txn_type == "Deposit")
        & (~merged.matter_type.isin(INCOME_MISMATCH_EXEMPT_MATTERS))
        & (merged.declared_annual_income_aud > 0)
        & (merged.amount_aud >= merged.declared_annual_income_aud * INCOME_MISMATCH_MULTIPLE)
    )
    flagged = merged[mask].copy()
    flagged["typology"] = "Unexplained source-of-funds jump"
    flagged["typology_reason"] = flagged.apply(
        lambda r: (f"Deposit of ${r.amount_aud:,.0f} is "
                   f"{r.amount_aud / r.declared_annual_income_aud:.1f}x this customer's "
                   f"declared annual income (${r.declared_annual_income_aud:,.0f})."),
        axis=1,
    )
    return flagged.drop(columns=["declared_annual_income_aud"])


def _detect_jurisdiction_nexus(txns: pd.DataFrame, high_risk_countries: list[str]) -> pd.DataFrame:
    flagged = txns[txns.counterparty_country.isin(high_risk_countries)].copy()
    flagged["typology"] = "High-risk jurisdiction nexus"
    flagged["typology_reason"] = flagged["counterparty_country"].apply(
        lambda c: f"Counterparty linked to {c}, an AUSTRAC-relevant high-risk jurisdiction."
    )
    return flagged


def _detect_round_dollar(txns: pd.DataFrame) -> pd.DataFrame:
    """Weak supporting signal only - round amounts on matter types where
    settlements are rarely round. Used as a contributing score factor,
    not surfaced as its own alert typology (per business design S3)."""
    round_prone = txns.amount_aud % 1000 == 0
    non_round_matters = ~txns.matter_type.isin(["Company Formation", "Nominee Director Arrangement",
                                                  "Nominee Shareholder Arrangement", "Trust Establishment"])
    return txns[round_prone & non_round_matters & (txns.amount_aud >= 20_000)]


HIGH_RISK_JURISDICTIONS = [
    "Myanmar", "Democratic People's Republic of Korea", "Iran",
    "Democratic Republic of Congo", "Yemen",
]

TYPOLOGY_WEIGHT = {
    "Structuring": 35,
    "Rapid movement of funds (pass-through)": 30,
    "Third-party funding mismatch": 25,
    "Unexplained source-of-funds jump": 25,
    "High-risk jurisdiction nexus": 20,
}
ALERT_SCORE_THRESHOLD = 20  # min composite score to generate an alert
ROUND_DOLLAR_BONUS = 8


def detect_typologies(transactions: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Runs all typology detectors and returns one row per (txn, typology)
    hit, each carrying its own reason. A single transaction can appear
    more than once if it matches multiple typologies."""
    txns = transactions.copy()
    txns["txn_date"] = pd.to_datetime(txns["txn_date"]).dt.date

    results = [
        _detect_structuring(txns),
        _detect_pass_through(txns),
        _detect_third_party_mismatch(txns),
        _detect_income_mismatch(txns, customers),
        _detect_jurisdiction_nexus(txns, HIGH_RISK_JURISDICTIONS),
    ]
    results = [r for r in results if len(r) > 0]
    if not results:
        return pd.DataFrame(columns=list(txns.columns) + ["typology", "typology_reason"])

    hits = pd.concat(results, ignore_index=True, sort=False)
    round_dollar_ids = set(_detect_round_dollar(txns)["txn_id"])
    hits["round_dollar_supporting"] = hits["txn_id"].isin(round_dollar_ids)
    return hits


def build_alerts(transactions: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates typology hits into alerts: one alert per (customer, date
    cluster, primary typology), composite-scored, thresholded so alert
    volume stays realistic rather than flagging every hit individually
    (business design S3, "alert-to-case conversion" point).
    """
    hits = detect_typologies(transactions, customers)
    if hits.empty:
        return pd.DataFrame(columns=[
            "alert_id", "customer_id", "matter_id", "alert_date", "typology",
            "composite_score", "amount_aud", "reason", "txn_ids", "status",
        ])

    ratings = apply_customer_ratings(customers)[["customer_id", "risk_rating"]]
    hits = hits.merge(ratings, on="customer_id", how="left")

    grouped = (
        hits.groupby(["customer_id", "matter_id", "typology"])
        .agg(
            alert_date=("txn_date", "max"),
            amount_aud=("amount_aud", "sum"),
            reason=("typology_reason", "first"),
            txn_ids=("txn_id", lambda s: list(s)),
            risk_rating=("risk_rating", "first"),
            round_dollar_supporting=("round_dollar_supporting", "any"),
        )
        .reset_index()
    )

    grouped["base_weight"] = grouped["typology"].map(TYPOLOGY_WEIGHT).fillna(15)
    risk_multiplier = {"Low": 1.0, "Medium": 1.15, "High": 1.35}
    grouped["composite_score"] = (
        grouped["base_weight"] * grouped["risk_rating"].map(risk_multiplier).fillna(1.0)
        + grouped["round_dollar_supporting"].astype(int) * ROUND_DOLLAR_BONUS
    ).round(1)

    alerts = grouped[grouped["composite_score"] >= ALERT_SCORE_THRESHOLD].copy()
    alerts = alerts.sort_values("composite_score", ascending=False).reset_index(drop=True)
    alerts["alert_id"] = [f"ALRT-{20000 + i}" for i in range(len(alerts))]

    # deterministic-but-varied triage status for demo purposes, weighted
    # toward "Open" for the most recent / highest scoring alerts
    rng = np.random.default_rng(7)
    statuses = []
    for _, r in alerts.iterrows():
        days_old = (pd.Timestamp("2026-09-22").date() - r["alert_date"]).days
        if days_old <= 3:
            statuses.append("Open")
        else:
            statuses.append(rng.choice(
                ["Open", "Escalated to Case", "Closed - False Positive", "Closed - No Issue"],
                p=[0.18, 0.32, 0.30, 0.20],
            ))
    alerts["status"] = statuses

    cols = ["alert_id", "customer_id", "matter_id", "alert_date", "typology",
            "risk_rating", "composite_score", "amount_aud", "reason", "txn_ids", "status"]
    return alerts[cols]
