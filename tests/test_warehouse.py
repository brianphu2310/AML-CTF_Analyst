"""Tests for the dimensional warehouse (ETL, schema constraints, data-quality suite). Pure Python, no Streamlit UI."""
import hashlib
import os
import sqlite3
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.model import build_model
from core.ref import AS_OF
from warehouse import build as W
from warehouse import quality as Q

M = build_model()


@pytest.fixture(scope="module")
def con():
    c = W.build_warehouse(":memory:", model=M)
    yield c
    c.close()


def fresh():
    return W.build_warehouse(":memory:", model=M)


def count(c, table):
    return c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


# --------------------------------------------------------------------- ETL --
def test_row_counts_match_the_simulator(con):
    assert count(con, "dim_customer") == len(M["cust"])
    assert count(con, "fact_alert") == len(M["alerts"])
    assert count(con, "fact_smr") == len(M["smrs"])
    assert count(con, "fact_monthly_snapshot") == len(M["stock"])
    assert count(con, "dim_analyst") == len(M["analysts"])


def test_audit_table_records_every_load(con):
    audit = dict(con.execute("SELECT table_name, row_count FROM etl_load_audit"))
    assert set(audit) == set(W.LOAD_ORDER)
    assert all(audit[t] == count(con, t) for t in audit)


def test_meta_labels_data_as_simulated(con):
    meta = dict(con.execute("SELECT meta_key, meta_value FROM etl_meta"))
    assert meta["data_origin"].startswith("SIMULATED")
    assert meta["as_of_date"] == AS_OF.strftime("%Y-%m-%d")


def test_surrogate_keys_are_dense_and_start_at_one(con):
    for table, key in [("dim_customer", "customer_key"), ("fact_alert", "alert_key"), ("fact_smr", "smr_key"),
                       ("dim_analyst", "analyst_key"), ("dim_typology", "typology_key")]:
        lo, hi, n = con.execute(f"SELECT MIN({key}), MAX({key}), COUNT(*) FROM {table}").fetchone()
        assert (lo, hi) == (1, n), table


def test_build_is_deterministic():
    def digest(c):
        h = hashlib.sha256()
        for t in W.LOAD_ORDER:
            for row in c.execute(f"SELECT * FROM {t} ORDER BY 1"):
                h.update(repr(row).encode())
        return h.hexdigest()
    assert digest(fresh()) == digest(fresh())


def test_on_disk_build_creates_file_and_overwrites(tmp_path):
    p = tmp_path / "wh.db"
    W.build_warehouse(p, model=M).close()
    W.build_warehouse(p, model=M).close()          # second run must not fail on existing tables
    c = sqlite3.connect(p)
    assert count(c, "fact_alert") == len(M["alerts"])


def test_transform_derives_flags_and_measures():
    T = W.transform(W.extract(M))
    a = T["fact_alert"].merge(T["dim_disposition"], on="disposition_key")
    assert (a["is_escalated"] == (a["disposition"] == "Escalated to SMR")).all()
    closed = a[a["closed_date_key"].notna()]
    assert (closed["days_to_close"] >= 0).all()
    assert a.loc[a["closed_date_key"].isna(), "days_to_close"].isna().all()
    smr = T["fact_smr"]
    assert smr.loc[smr["status"] == "Draft", "submitted_date_key"].isna().all()


def test_business_days_ignores_weekends():
    s = pd.Series(pd.to_datetime(["2025-09-12", "2025-09-12", None]))      # Friday
    e = pd.Series(pd.to_datetime(["2025-09-15", "2025-09-16", "2025-09-16"]))
    out = W.business_days(s, e)
    assert out.iloc[0] == 1 and out.iloc[1] == 2            # Fri->Mon = 1 working day; Fri->Tue = 2
    assert pd.isna(out.iloc[2])


# ---------------------------------------------------------------- dim_date --
def test_dim_date_is_contiguous_and_has_australian_fy(con):
    n, span = con.execute("SELECT COUNT(*), julianday(MAX(full_date)) - julianday(MIN(full_date)) + 1 FROM dim_date").fetchone()
    assert n == span
    row = con.execute("SELECT fy_label, fy_quarter, day_name, is_weekend FROM dim_date WHERE full_date = '2025-07-01'").fetchone()
    assert row == ("FY26", 1, "Tuesday", 0)
    assert con.execute("SELECT fy_label, fy_quarter FROM dim_date WHERE full_date = '2026-06-30'").fetchone() == ("FY26", 4)
    assert con.execute("SELECT is_weekend FROM dim_date WHERE full_date = '2025-09-13'").fetchone()[0] == 1      # Saturday


def test_date_key_covers_every_fact_date(con):
    assert con.execute("PRAGMA foreign_key_check").fetchall() == []


# --------------------------------------------------------- schema constraints --
def test_foreign_keys_are_enforced(con):
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("INSERT INTO fact_smr (smr_key, smr_id, alert_key, customer_key, typology_key, analyst_key, branch_key, escalated_date_key, status) "
                    "VALUES (9999, 'SMR-X', 999999, 1, 1, 1, 1, 20250101, 'Draft')")
    con.rollback()


def test_check_constraints_reject_bad_values(con):
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("UPDATE dim_customer SET risk_score = 150 WHERE customer_key = 1")
    con.rollback()
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("UPDATE fact_smr SET status = 'Lost' WHERE smr_key = 1")
    con.rollback()


def test_unique_business_keys(con):
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("INSERT INTO dim_branch VALUES (99, 'Camden', 'x')")
    con.rollback()


def test_indexes_exist_on_fact_foreign_keys(con):
    idx = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'index'")}
    for name in ("ix_alert_customer", "ix_alert_typology", "ix_alert_opened", "ix_smr_submitted"):
        assert name in idx


def test_query_plan_uses_index_for_customer_lookup(con):
    plan = " ".join(str(r) for r in con.execute("EXPLAIN QUERY PLAN SELECT * FROM fact_alert WHERE customer_key = 5"))
    assert "ix_alert_customer" in plan


# ------------------------------------------------------------ quality suite --
def test_dq_suite_passes_on_clean_warehouse(con):
    checks = Q.run_checks(con, M)
    failed = [c for c in checks if not c.passed]
    assert not failed, failed
    assert {c.family for c in checks} == {"Completeness", "Uniqueness", "Referential integrity", "Validity", "Reconciliation"}
    assert len(checks) > 80


def _failures(c):
    return [x.name for x in Q.run_checks(c, M) if not x.passed]


def test_dq_detects_orphan_foreign_key():
    c = fresh()
    c.execute("PRAGMA foreign_keys = OFF")
    c.execute("UPDATE fact_alert SET customer_key = 99999 WHERE alert_key = 1")
    assert any("orphans" in n or "foreign_key_check" in n for n in _failures(c))


def unconstrain(c, table):
    """Rebuild `table` as a plain CTAS copy (no PK/UNIQUE/NOT NULL/CHECK) so a fault can be injected for the DQ suite to catch."""
    c.execute("PRAGMA foreign_keys = OFF")
    c.execute(f"CREATE TABLE _copy AS SELECT * FROM {table}")
    c.execute(f"DROP TABLE {table}")
    c.execute(f"ALTER TABLE _copy RENAME TO {table}")


def test_dq_detects_duplicate_business_key():
    c = fresh()
    unconstrain(c, "fact_alert")
    c.execute("INSERT INTO fact_alert SELECT * FROM fact_alert WHERE alert_key = 1")
    assert any("alert_id" in x.name for x in Q.uniqueness(c) if not x.passed)
    assert any("no duplicate alerts" in x.name for x in Q.uniqueness(c) if not x.passed)


def test_dq_detects_null_in_required_column():
    c = fresh()
    unconstrain(c, "dim_customer")
    c.execute("UPDATE dim_customer SET state = NULL WHERE customer_key = 3")
    assert any("dim_customer.state" in x.name for x in Q.completeness(c) if not x.passed)


def test_dq_detects_reconciliation_drift():
    c = fresh()
    c.execute("UPDATE fact_alert SET handling_hours = handling_hours + 1 WHERE alert_key = 1")
    assert any("handling_hours" in n for n in _failures(c))
    c = fresh()
    c.execute("UPDATE fact_alert SET disposition_key = 4 WHERE alert_key IN (SELECT alert_key FROM fact_alert WHERE disposition_key = 5 LIMIT 1)")
    assert any("disposition" in n or "typology" in n for n in _failures(c))


def test_dq_detects_business_rule_violation():
    c = fresh()
    c.execute("UPDATE fact_alert SET sla_breach_flag = 1 - sla_breach_flag WHERE alert_key = 1 AND closed_date_key IS NOT NULL")
    assert any("sla_breach_flag" in n for n in _failures(c))


def test_report_is_deterministic_and_committed_copy_is_current(con):
    md = Q.render_markdown(Q.run_checks(con, M))
    assert md == Q.render_markdown(Q.run_checks(con, M))
    assert "checks passed" in md and "FAIL" not in md
    committed = Q.REPORT_PATH.read_text().rstrip("\n")
    assert committed == md.rstrip("\n"), "docs/DATA_QUALITY.md is stale - run: python -m warehouse.quality"
