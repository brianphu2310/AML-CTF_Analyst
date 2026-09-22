"""Reconciliation tests: the numbers on different pages must agree with each other.

Run from the project folder:  python -m pytest -q
"""
import os
import sys

import numpy as np
import pytest
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import metrics as X
from core.model import build_model
from core.period import Period, presets, delta
from core.ref import AS_OF, SLA_DAYS

M = build_model()
CUST, ALERTS, SMRS, FIN, STOCK = M["cust"], M["alerts"], M["smrs"], M["fin"], M["stock"]


def close(a, b, tol=1.0):
    assert abs(a - b) <= tol, f"{a} != {b} (tol {tol})"


# ------------------------------------------------------------------ model ----
def test_customer_population_reconciles():
    assert int(STOCK["customers_active"].iloc[-1]) == len(CUST)
    tiers = STOCK[["customers_low", "customers_medium", "customers_high"]].iloc[-1].sum()
    close(tiers, len(CUST), 0.5)


def test_risk_tier_matches_bounds():
    from core.ref import RISK_TIER_BOUNDS
    lo, hi = RISK_TIER_BOUNDS
    assert (CUST.loc[CUST["risk_tier"] == "Low", "risk_score"] < lo).all()
    assert (CUST.loc[CUST["risk_tier"] == "High", "risk_score"] > hi).all()
    med = CUST.loc[CUST["risk_tier"] == "Medium", "risk_score"]
    assert ((med >= lo) & (med <= hi)).all()


def test_alerts_never_precede_customer_onboarding():
    merged = ALERTS.merge(CUST[["customer_id", "onboarded"]], on="customer_id", how="left")
    assert (merged["opened"] >= merged["onboarded"]).all()


def test_every_smr_traces_to_an_escalated_alert():
    esc = set(ALERTS.loc[ALERTS["disposition"] == "Escalated to SMR", "alert_id"])
    assert set(SMRS["alert_id"]) <= esc
    assert len(SMRS) == len(esc)


def test_sla_breach_flag_matches_turnaround():
    closed = ALERTS[ALERTS["closed"].notna()]
    turnaround = (closed["closed"] - closed["opened"]).dt.days
    assert ((turnaround > SLA_DAYS) == closed["sla_breach"]).all()


def test_overdue_reviews_are_genuinely_in_the_past():
    overdue = CUST[CUST["review_overdue"]]
    assert (overdue["next_review_due"] < AS_OF).all()


def test_fin_alert_columns_sum_to_total():
    from core.ref import TYPOLOGY_NAMES
    close(FIN[[f"alerts_{t}" for t in TYPOLOGY_NAMES]].sum(axis=1).sum(), FIN["alerts_opened"].sum(), 0.01)


# ----------------------------------------------------------------- periods ----
def test_period_presets():
    pre = presets()
    qtd, _ = pre["This quarter (QTD)"]
    assert (qtd.start, qtd.end) == (pd.Timestamp("2025-07-01"), AS_OF)


def test_quarters_add_up_to_year():
    q = [Period(pd.Timestamp(a), pd.Timestamp(b), "q") for a, b in [("2024-07-01", "2024-09-30"), ("2024-10-01", "2024-12-31"), ("2025-01-01", "2025-03-31"), ("2025-04-01", "2025-06-30")]]
    fy = Period(pd.Timestamp("2024-07-01"), pd.Timestamp("2025-06-30"), "fy")
    close(sum(X.fin_sum(M, p)["alerts_opened"] for p in q), X.fin_sum(M, fy)["alerts_opened"], 1.0)


# ------------------------------------------------------------------ metrics ----
def test_headline_active_alerts_matches_alert_queue():
    cur, cmp = presets()["This quarter (QTD)"][0], None
    H = X.headline(M, cur, cmp)
    q = X.alert_queue(M, cur.end)
    close(H["active_alerts"], len(q), 0.5)


def test_typology_table_sums_to_period_total():
    cur, _ = presets()["This quarter (QTD)"]
    tt = X.typology_table(M, cur)
    a = X.alerts_in(M, cur)
    close(tt["alerts"].sum(), len(a), 0.5)


def test_analyst_table_sums_to_period_alerts():
    cur, _ = presets()["Last 12 months"]
    at = X.analyst_table(M, cur)
    a = X.alerts_in(M, cur)
    close(at["alerts"].sum(), len(a), 0.5)
    close(at["hours"].sum(), a["hours"].sum(), 0.5)


def test_smr_register_matches_austrac_status_counts():
    cur, _ = presets()["Last 12 months"]
    reg = X.smr_register(M, cur)
    assert set(reg["status"]) <= {"Draft", "Submitted", "Acknowledged"}


def test_disposition_table_sums_to_alerts_in_period():
    cur, _ = presets()["This quarter (QTD)"]
    dt = X.disposition_table(M, cur)
    a = X.alerts_in(M, cur)
    close(dt.sum(), len(a), 0.01)


if __name__ == "__main__":
    tests = [(n, fn) for n, fn in sorted(globals().items()) if n.startswith("test_") and callable(fn)]
    for n, fn in tests:
        fn(); print("PASS", n)
    print(f"{len(tests)} tests passed")


@pytest.mark.parametrize("preset", list(presets().keys()))
def test_overview_pipeline_funnel_reconciles(preset):
    """Overview pipeline: each stage can only hold alerts that reached the stage before it, and every
    drop-off shown under a stage accounts exactly for the gap to the next stage."""
    p = presets()[preset][0]
    pf = X.pipeline_flow(M, p)
    stages = [pf["total"], pf["triaged"], pf["l2"], pf["mlro"], pf["smr_lodged"]]
    assert all(a >= b >= 0 for a, b in zip(stages, stages[1:])), stages
    assert pf["total"] - pf["triaged"] == pf["open"]
    assert pf["triaged"] - pf["l2"] == pf["closed_fp"]
    assert pf["l2"] - pf["mlro"] == pf["closed_nfa"] + pf["under_investigation"]
    assert pf["mlro"] - pf["smr_lodged"] == pf["smr_drafting"]
    assert sum(pf["by_typology"].values()) == pf["total"]
