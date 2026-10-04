"""Every analytical query in sql/analysis/ must execute, return sensible rows, and agree with the warehouse totals."""
import csv
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "sql"))

import run_queries as RQ
from core.model import build_model
from warehouse.build import build_warehouse

M = build_model()
FILES = RQ.query_files()


@pytest.fixture(scope="module")
def con():
    c = build_warehouse(":memory:", model=M)
    yield c
    c.close()


def result(con, stem):
    cols, rows = RQ.run_query(con, next(p for p in FILES if p.stem == stem))
    return [dict(zip(cols, r)) for r in rows]


def test_between_8_and_10_queries_exist():
    assert 8 <= len(FILES) <= 10


@pytest.mark.parametrize("path", FILES, ids=[p.stem for p in FILES])
def test_query_executes_and_returns_rows(con, path):
    cols, rows = RQ.run_query(con, path)
    assert cols and rows
    assert len(cols) == len(set(cols)), "duplicate output column names"


@pytest.mark.parametrize("path", FILES, ids=[p.stem for p in FILES])
def test_query_is_commented_and_uses_cte(path):
    sql = path.read_text()
    assert sql.lstrip().startswith("--"), "each query starts with a comment describing the question"
    assert re.search(r"^\s*WITH\b", sql, re.I | re.M)


def test_portfolio_uses_the_required_sql_features():
    allsql = "\n".join(p.read_text() for p in FILES).upper()
    for feature in ("RANK()", "LAG(", "PERCENT_RANK()", "NTILE(", "SUM(", " OVER (", "CASE", "LEFT JOIN", "CROSS JOIN", "ROWS BETWEEN"):
        assert feature in allsql, feature


def test_funnel_reconciles_to_alert_counts(con):
    rows = result(con, "01_alert_triage_funnel")
    assert sum(r["opened"] for r in rows) == len(M["alerts"])
    assert sum(r["escalated"] for r in rows) == len(M["smrs"])
    assert sum(r["smr_acknowledged"] for r in rows) == int((M["smrs"]["status"] == "Acknowledged").sum())
    assert all(r["opened"] >= r["dispositioned"] >= r["escalated"] >= r["smr_submitted"] >= r["smr_acknowledged"] for r in rows)


def test_risk_mix_shares_sum_to_100_per_typology(con):
    rows = result(con, "02_typology_risk_rating_mix")
    by = {}
    for r in rows:
        by[r["typology_name"]] = by.get(r["typology_name"], 0) + r["pct_of_typology_alerts"]
    assert len(by) == 5 and all(abs(v - 100) < 0.5 for v in by.values())


def test_smr_timeliness_counts_submitted_smrs(con):
    rows = result(con, "03_smr_timeliness")
    assert sum(r["smrs_submitted"] for r in rows) == int(M["smrs"]["submitted"].notna().sum())
    assert rows[-1]["cumulative_smrs"] == sum(r["smrs_submitted"] for r in rows)
    assert rows[0]["qoq_change_pct_pts"] is None


def test_structuring_trend_covers_every_month_and_totals_match(con):
    rows = result(con, "04_structuring_monthly_trend")
    assert len(rows) == len(M["months"])
    expected = int((M["alerts"]["typology"] == "Structuring / smurfing").sum())
    assert rows[-1]["running_total"] == expected == sum(r["structuring_alerts"] for r in rows)


def test_repeat_clients_have_multiple_alerts_and_are_ranked(con):
    rows = result(con, "05_structuring_repeat_clients")
    assert rows and all(r["structuring_alerts"] >= 2 for r in rows)
    ranks = [r["priority_rank"] for r in rows]
    assert ranks == sorted(ranks)
    s = M["alerts"][M["alerts"]["typology"] == "Structuring / smurfing"].groupby("customer_id").size()
    assert len(rows) == int((s >= 2).sum())


def test_rule_performance_matches_app_alert_counts(con):
    rows = {r["typology_name"]: r for r in result(con, "06_rule_hit_rate_false_positive")}
    for typ, n in M["alerts"]["typology"].value_counts().items():
        assert rows[typ]["alerts"] == n
    assert all(0 <= r["fp_rate_pct"] <= 100 for r in rows.values())


def test_analyst_hours_sum_to_total(con):
    rows = result(con, "07_analyst_workload_sla")
    assert abs(sum(r["hours"] for r in rows) - M["alerts"]["hours"].sum()) < 0.5
    assert abs(sum(r["pct_of_team_hours"] for r in rows) - 100) < 0.6


def test_review_backlog_matches_overdue_flag(con):
    rows = result(con, "08_review_backlog")
    assert sum(r["overdue_clients"] for r in rows) == int(M["cust"]["next_review_due"].lt(M["stock"]["date"].iloc[-1]).sum())


def test_open_queue_matches_pending_alerts(con):
    rows = result(con, "09_open_alert_ageing")
    assert len(rows) == int(M["alerts"]["closed"].isna().sum())
    assert [r["oldest_first"] for r in rows] == list(range(1, len(rows) + 1))


def test_pareto_is_cumulative_and_monotonic(con):
    rows = result(con, "10_alert_concentration_pareto")
    cum = [r["cumulative_pct_of_alerts"] for r in rows]
    assert cum == sorted(cum) and cum[-1] <= 100
    assert [r["alerts"] for r in rows] == sorted((r["alerts"] for r in rows), reverse=True)


def test_committed_csv_outputs_are_current(con, tmp_path):
    RQ.run_all(con, tmp_path)
    for p in FILES:
        committed = (RQ.OUT_DIR / f"{p.stem}.csv").read_text()
        assert committed == (tmp_path / f"{p.stem}.csv").read_text(), f"{p.stem}.csv is stale - run: python sql/run_queries.py"
    assert {f.name for f in RQ.OUT_DIR.glob("*.csv")} == {f"{p.stem}.csv" for p in FILES}


def test_csv_has_header_and_rows(tmp_path, con):
    RQ.run_all(con, tmp_path)
    with open(tmp_path / "01_alert_triage_funnel.csv", newline="") as f:
        r = list(csv.reader(f))
    assert r[0][0] == "typology_name" and len(r) == 6
