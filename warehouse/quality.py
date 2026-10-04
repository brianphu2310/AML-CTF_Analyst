"""Data-quality check suite for the warehouse. Writes docs/DATA_QUALITY.md.

    python -m warehouse.quality               # build (in memory), run all checks, rewrite docs/DATA_QUALITY.md
    python -m warehouse.quality --db warehouse.db

Check families: completeness (nulls), uniqueness (duplicates), referential integrity, validity/consistency
(business rules) and reconciliation of warehouse totals to the Streamlit app's own metric functions
(core/metrics.py), so the warehouse can never silently drift from what the dashboards show.
Output is deterministic (no timestamps) so the committed report only changes when the data/logic does.
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from core import metrics as X
from core.model import build_model
from core.period import Period
from core.ref import AS_OF, RISK_TIER_BOUNDS, SLA_DAYS, START
from warehouse.build import ROOT, build_warehouse

REPORT_PATH = ROOT / "docs" / "DATA_QUALITY.md"

# (table, column) pairs that must never be NULL beyond the schema's own NOT NULL constraints being the only guard.
REQUIRED = {
    "dim_customer": ["customer_id", "customer_name", "customer_type", "channel", "foreign_tier", "product", "state",
                     "branch_key", "risk_tier_key", "risk_score", "onboarded_date_key", "next_review_due_date_key"],
    "fact_alert": ["alert_id", "customer_key", "typology_key", "analyst_key", "branch_key", "disposition_key",
                   "opened_date_key", "handling_hours", "sla_breach_flag"],
    "fact_smr": ["smr_id", "alert_key", "customer_key", "escalated_date_key", "status"],
}
UNIQUE = {
    "dim_customer": ["customer_id"], "fact_alert": ["alert_id"], "fact_smr": ["smr_id", "alert_key"],
    "dim_analyst": ["analyst_short"], "dim_typology": ["typology_name"], "dim_date": ["full_date"],
}
# child table, child column, parent table, parent column
FOREIGN_KEYS = [
    ("dim_customer", "branch_key", "dim_branch", "branch_key"),
    ("dim_customer", "risk_tier_key", "dim_risk_tier", "risk_tier_key"),
    ("dim_customer", "onboarded_date_key", "dim_date", "date_key"),
    ("dim_customer", "last_review_date_key", "dim_date", "date_key"),
    ("dim_customer", "next_review_due_date_key", "dim_date", "date_key"),
    ("dim_analyst", "home_branch_key", "dim_branch", "branch_key"),
    ("dim_analyst", "start_date_key", "dim_date", "date_key"),
    ("fact_alert", "customer_key", "dim_customer", "customer_key"),
    ("fact_alert", "typology_key", "dim_typology", "typology_key"),
    ("fact_alert", "analyst_key", "dim_analyst", "analyst_key"),
    ("fact_alert", "branch_key", "dim_branch", "branch_key"),
    ("fact_alert", "disposition_key", "dim_disposition", "disposition_key"),
    ("fact_alert", "opened_date_key", "dim_date", "date_key"),
    ("fact_alert", "closed_date_key", "dim_date", "date_key"),
    ("fact_smr", "alert_key", "fact_alert", "alert_key"),
    ("fact_smr", "customer_key", "dim_customer", "customer_key"),
    ("fact_smr", "typology_key", "dim_typology", "typology_key"),
    ("fact_smr", "analyst_key", "dim_analyst", "analyst_key"),
    ("fact_smr", "branch_key", "dim_branch", "branch_key"),
    ("fact_smr", "escalated_date_key", "dim_date", "date_key"),
    ("fact_smr", "submitted_date_key", "dim_date", "date_key"),
    ("fact_smr", "acknowledged_date_key", "dim_date", "date_key"),
    ("fact_monthly_snapshot", "month_start_date_key", "dim_date", "date_key"),
    ("fact_monthly_snapshot", "snapshot_date_key", "dim_date", "date_key"),
]


@dataclass
class Check:
    family: str
    name: str
    expected: str
    actual: str
    passed: bool


def _scalar(con, sql, *args):
    return con.execute(sql, args).fetchone()[0]


def _chk(family, name, expected, actual, passed=None) -> Check:
    return Check(family, name, str(expected), str(actual), (expected == actual) if passed is None else passed)


# ------------------------------------------------------------------ families --
def completeness(con):
    for table, cols in REQUIRED.items():
        for col in cols:
            n = _scalar(con, f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
            yield _chk("Completeness", f"{table}.{col} has no NULLs", 0, n)
    # conditional completeness: the NULLs that ARE allowed must be explained by lifecycle state
    n = _scalar(con, """SELECT COUNT(*) FROM fact_alert a JOIN dim_disposition d USING (disposition_key)
                        WHERE (d.is_closed = 1 OR d.is_escalated = 1) AND a.closed_date_key IS NULL""")
    yield _chk("Completeness", "closed/escalated alerts always have a closed date", 0, n)
    n = _scalar(con, """SELECT COUNT(*) FROM fact_alert a JOIN dim_disposition d USING (disposition_key)
                        WHERE d.outcome_group = 'Pending' AND a.closed_date_key IS NOT NULL""")
    yield _chk("Completeness", "open/under-investigation alerts have no closed date", 0, n)
    n = _scalar(con, "SELECT COUNT(*) FROM fact_smr WHERE (status = 'Draft') <> (submitted_date_key IS NULL)")
    yield _chk("Completeness", "SMR submitted date is NULL if and only if status = Draft", 0, n)
    n = _scalar(con, "SELECT COUNT(*) FROM fact_smr WHERE (status = 'Acknowledged') <> (acknowledged_date_key IS NOT NULL)")
    yield _chk("Completeness", "SMR acknowledged date is present if and only if status = Acknowledged", 0, n)


def uniqueness(con):
    for table, cols in UNIQUE.items():
        for col in cols:
            n = _scalar(con, f"SELECT COUNT(*) FROM (SELECT {col} FROM {table} GROUP BY {col} HAVING COUNT(*) > 1)")
            yield _chk("Uniqueness", f"{table}.{col} has no duplicates", 0, n)
    n = _scalar(con, """SELECT COUNT(*) FROM (SELECT customer_key, typology_key, opened_date_key, analyst_key, handling_hours
                        FROM fact_alert GROUP BY 1, 2, 3, 4, 5 HAVING COUNT(*) > 1)""")
    yield _chk("Uniqueness", "no duplicate alerts on (customer, typology, opened date, analyst, hours)", 0, n)


def referential_integrity(con):
    yield _chk("Referential integrity", "PRAGMA foreign_key_check returns no violations", 0, len(con.execute("PRAGMA foreign_key_check").fetchall()))
    for ct, cc, pt, pc in FOREIGN_KEYS:
        n = _scalar(con, f"SELECT COUNT(*) FROM {ct} c LEFT JOIN {pt} p ON c.{cc} = p.{pc} WHERE c.{cc} IS NOT NULL AND p.{pc} IS NULL")
        yield _chk("Referential integrity", f"no orphans: {ct}.{cc} -> {pt}.{pc}", 0, n)
    n = _scalar(con, """SELECT COUNT(*) FROM fact_smr s JOIN fact_alert a USING (alert_key) JOIN dim_disposition d USING (disposition_key)
                        WHERE d.is_escalated = 0""")
    yield _chk("Referential integrity", "every SMR traces to an alert dispositioned 'Escalated to SMR'", 0, n)
    n = _scalar(con, """SELECT COUNT(*) FROM fact_alert a JOIN dim_disposition d USING (disposition_key)
                        LEFT JOIN fact_smr s USING (alert_key) WHERE d.is_escalated = 1 AND s.smr_key IS NULL""")
    yield _chk("Referential integrity", "every escalated alert has exactly one SMR", 0, n)


def validity(con):
    yield _chk("Validity", "alert closed date is not before opened date", 0, _scalar(con,
               "SELECT COUNT(*) FROM fact_alert WHERE closed_date_key IS NOT NULL AND closed_date_key < opened_date_key"))
    yield _chk("Validity", "SMR dates are ordered: escalated <= submitted <= acknowledged", 0, _scalar(con,
               """SELECT COUNT(*) FROM fact_smr WHERE (submitted_date_key IS NOT NULL AND submitted_date_key < escalated_date_key)
                  OR (acknowledged_date_key IS NOT NULL AND acknowledged_date_key < submitted_date_key)"""))
    yield _chk("Validity", f"sla_breach_flag agrees with days_to_close > {SLA_DAYS} on closed alerts", 0, _scalar(con,
               f"SELECT COUNT(*) FROM fact_alert WHERE closed_date_key IS NOT NULL AND sla_breach_flag <> (days_to_close > {SLA_DAYS})"))
    lo, hi = RISK_TIER_BOUNDS
    yield _chk("Validity", "customer risk tier agrees with score bounds", 0, _scalar(con,
               f"""SELECT COUNT(*) FROM dim_customer c JOIN dim_risk_tier t USING (risk_tier_key)
                   WHERE t.risk_tier <> CASE WHEN c.risk_score < {lo} THEN 'Low' WHEN c.risk_score > {hi} THEN 'High' ELSE 'Medium' END"""))
    yield _chk("Validity", "risk_score within 1-100", 0, _scalar(con, "SELECT COUNT(*) FROM dim_customer WHERE risk_score NOT BETWEEN 1 AND 100"))
    yield _chk("Validity", "handling_hours within 0.5-8.0", 0, _scalar(con, "SELECT COUNT(*) FROM fact_alert WHERE handling_hours NOT BETWEEN 0.5 AND 8.0"))
    yield _chk("Validity", "no alert opened before the customer was onboarded", 0, _scalar(con,
               "SELECT COUNT(*) FROM fact_alert a JOIN dim_customer c USING (customer_key) WHERE a.opened_date_key < c.onboarded_date_key"))
    yield _chk("Validity", "no alert opened after the as-of date", 0, _scalar(con,
               "SELECT COUNT(*) FROM fact_alert WHERE opened_date_key > ?", int(AS_OF.strftime("%Y%m%d"))))
    yield _chk("Validity", "alert owner analyst had started before the alert opened", 0, _scalar(con,
               "SELECT COUNT(*) FROM fact_alert a JOIN dim_analyst n USING (analyst_key) WHERE a.opened_date_key < n.start_date_key"))
    yield _chk("Validity", "alert branch equals its customer's branch", 0, _scalar(con,
               "SELECT COUNT(*) FROM fact_alert a JOIN dim_customer c USING (customer_key) WHERE a.branch_key <> c.branch_key"))
    yield _chk("Validity", "SMR typology/customer/analyst equal its alert's", 0, _scalar(con,
               """SELECT COUNT(*) FROM fact_smr s JOIN fact_alert a USING (alert_key)
                  WHERE s.typology_key <> a.typology_key OR s.customer_key <> a.customer_key OR s.analyst_key <> a.analyst_key"""))
    yield _chk("Validity", "review_overdue_flag agrees with next review due < as-of date", 0, _scalar(con,
               "SELECT COUNT(*) FROM dim_customer WHERE review_overdue_flag <> (next_review_due_date_key < ?)", int(AS_OF.strftime("%Y%m%d"))))
    yield _chk("Validity", "dim_date has contiguous dates (rows = days between min and max)", 0, _scalar(con,
               "SELECT (julianday(MAX(full_date)) - julianday(MIN(full_date)) + 1) - COUNT(*) FROM dim_date"))


def reconciliation(con, M):
    """Warehouse totals vs the app's own metric functions over the full history window."""
    p = Period(START, AS_OF, "Full history")
    out = []
    alerts = M["alerts"]
    out.append(_chk("Reconciliation", "dim_customer rows = model client register rows", len(M["cust"]), _scalar(con, "SELECT COUNT(*) FROM dim_customer")))
    out.append(_chk("Reconciliation", "fact_alert rows = model alert ledger rows", len(alerts), _scalar(con, "SELECT COUNT(*) FROM fact_alert")))
    out.append(_chk("Reconciliation", "fact_smr rows = model SMR register rows", len(M["smrs"]), _scalar(con, "SELECT COUNT(*) FROM fact_smr")))
    out.append(_chk("Reconciliation", "sum(handling_hours) = model alert hours", round(float(alerts["hours"].sum()), 2),
                    round(_scalar(con, "SELECT SUM(handling_hours) FROM fact_alert"), 2)))
    last = con.execute("SELECT customers_active, customers_low, customers_medium, customers_high, active_alerts, open_investigations, overdue_reviews "
                       "FROM fact_monthly_snapshot ORDER BY month_start_date_key DESC LIMIT 1").fetchone()
    tiers = X.risk_tier_breakdown(M, AS_OF)
    out.append(_chk("Reconciliation", "dim_customer count by risk tier = app risk_tier_breakdown()", tiers,
                    dict(con.execute("SELECT risk_tier, COUNT(*) FROM dim_customer JOIN dim_risk_tier USING (risk_tier_key) GROUP BY 1").fetchall())))
    out.append(_chk("Reconciliation", "latest snapshot: active customers = dim_customer rows", last[0], _scalar(con, "SELECT COUNT(*) FROM dim_customer")))
    out.append(_chk("Reconciliation", "latest snapshot: low+medium+high = active customers", last[0], last[1] + last[2] + last[3]))
    out.append(_chk("Reconciliation", "overdue reviews: dim_customer flag count = app overdue_customers()", len(X.overdue_customers(M, AS_OF)),
                    _scalar(con, "SELECT COUNT(*) FROM dim_customer WHERE review_overdue_flag = 1")))
    out.append(_chk("Reconciliation", "latest snapshot overdue_reviews = app overdue_customers()", len(X.overdue_customers(M, AS_OF)), last[6]))
    out.append(_chk("Reconciliation", "open queue (open + under investigation) = app alert_queue()", len(X.alert_queue(M, AS_OF)),
                    _scalar(con, "SELECT COUNT(*) FROM fact_alert JOIN dim_disposition USING (disposition_key) WHERE outcome_group = 'Pending'")))
    out.append(_chk("Reconciliation", "latest snapshot active_alerts = warehouse pending alerts", last[4],
                    _scalar(con, "SELECT COUNT(*) FROM fact_alert JOIN dim_disposition USING (disposition_key) WHERE outcome_group = 'Pending'")))

    disp = X.disposition_table(M, p)
    wh_disp = dict(con.execute("SELECT disposition, COUNT(*) FROM fact_alert JOIN dim_disposition USING (disposition_key) GROUP BY 1").fetchall())
    for d, n in disp.items():
        out.append(_chk("Reconciliation", f"disposition '{d}' = app disposition_table()", int(n), wh_disp.get(d, 0)))

    ty = X.typology_table(M, p).set_index("typology")
    wh_ty = {r[0]: r[1:] for r in con.execute(
        """SELECT t.typology_name, COUNT(*), SUM(d.is_false_positive), SUM(d.is_escalated)
           FROM fact_alert a JOIN dim_typology t USING (typology_key) JOIN dim_disposition d USING (disposition_key) GROUP BY 1""")}
    for name, row in ty.iterrows():
        n, fp, esc = wh_ty[name]
        out.append(_chk("Reconciliation", f"typology '{name}': alerts / false positives / escalated = app typology_table()",
                        (int(row["alerts"]), int(row["false_positives"]), int(row["escalated"])), (n, int(fp), int(esc))))

    st = X.austrac_status_table(M, AS_OF)
    wh_st = dict(con.execute("SELECT status, COUNT(*) FROM fact_smr GROUP BY 1").fetchall())
    for status, n in st.items():
        out.append(_chk("Reconciliation", f"SMR status '{status}' = app austrac_status_table()", int(n), wh_st.get(status, 0)))

    sla = X.sla_table(M, p)
    closed, breach_n, avg_days = con.execute(
        "SELECT COUNT(closed_date_key), SUM(CASE WHEN closed_date_key IS NOT NULL THEN sla_breach_flag END), AVG(days_to_close) FROM fact_alert").fetchone()
    out.append(_chk("Reconciliation", "closed alerts = app sla_table()['closed']", int(sla["closed"]), closed))
    out.append(_chk("Reconciliation", "SLA breach rate = app sla_table()['breach_rate']", round(float(sla["breach_rate"]), 6), round(breach_n / closed, 6)))
    out.append(_chk("Reconciliation", "average days to close = app sla_table()['avg_days']", round(float(sla["avg_days"]), 6), round(avg_days, 6)))

    at = X.analyst_table(M, p).set_index("short")
    wh_an = {r[0]: r[1:] for r in con.execute(
        "SELECT analyst_short, COUNT(*), ROUND(SUM(handling_hours), 2) FROM fact_alert JOIN dim_analyst USING (analyst_key) GROUP BY 1")}
    for short, row in at.iterrows():
        n, h = wh_an.get(short, (0, 0.0))
        out.append(_chk("Reconciliation", f"analyst '{short}': alerts / hours = app analyst_table()", (int(row["alerts"]), round(float(row["hours"]), 2)), (n, round(h, 2))))
    return out


def run_checks(con: sqlite3.Connection, model: dict | None = None) -> list[Check]:
    M = model if model is not None else build_model()
    checks: list[Check] = []
    for fam in (completeness, uniqueness, referential_integrity, validity):
        checks.extend(fam(con))
    checks.extend(reconciliation(con, M))
    return checks


# ------------------------------------------------------------------- report --
def render_markdown(checks: list[Check]) -> str:
    fams = list(dict.fromkeys(c.family for c in checks))
    passed = sum(c.passed for c in checks)
    lines = ["# Data quality report", "",
             "Generated by `python -m warehouse.quality` against `warehouse.db`, which is built from the **simulated**",
             "dataset (`core/model.py`, fixed seed). The report is deterministic, so it only changes if the data or the checks change.",
             "", f"**Result: {passed} of {len(checks)} checks passed.**", "",
             "| Family | Checks | Passed | Failed |", "|---|---:|---:|---:|"]
    for f in fams:
        cs = [c for c in checks if c.family == f]
        lines.append(f"| {f} | {len(cs)} | {sum(c.passed for c in cs)} | {sum(not c.passed for c in cs)} |")
    lines += ["", "Reconciliation checks compare warehouse SQL totals with the Streamlit app's own functions in `core/metrics.py` over the full history window",
              f"({START:%Y-%m-%d} to {AS_OF:%Y-%m-%d}). Business-day measures exclude weekends only (no public-holiday calendar).", ""]
    for f in fams:
        lines += [f"## {f}", "", "| Status | Check | Expected | Actual |", "|---|---|---|---|"]
        for c in (c for c in checks if c.family == f):
            lines.append(f"| {'PASS' if c.passed else '**FAIL**'} | {c.name} | `{c.expected}` | `{c.actual}` |")
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=":memory:", help="existing warehouse.db, or ':memory:' to build one on the fly")
    ap.add_argument("--report", default=str(REPORT_PATH))
    args = ap.parse_args(argv)
    if args.db == ":memory:":
        con = build_warehouse(":memory:")
    else:
        con = sqlite3.connect(args.db)
        con.execute("PRAGMA foreign_keys = ON")
    checks = run_checks(con)
    Path(args.report).write_text(render_markdown(checks) + "\n")
    failed = [c for c in checks if not c.passed]
    print(f"{len(checks) - len(failed)}/{len(checks)} checks passed -> {args.report}")
    for c in failed:
        print(f"  FAIL [{c.family}] {c.name}: expected {c.expected}, got {c.actual}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
