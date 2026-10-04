"""ETL: simulated model (core.model.build_model, fixed seed) -> SQLite star schema.

    python -m warehouse.build                 # writes ./warehouse.db (gitignored)
    python -m warehouse.build --db other.db

Pipeline stages (each a pure function so it can be unit-tested):
    extract()   -> raw pandas frames straight from the simulator (no cleaning)
    transform() -> conformed dimensions + facts with surrogate keys, flags and derived measures
    load()      -> DDL from schema.sql, then bulk insert in FK order with foreign keys enforced

All data is SIMULATED. Nothing is fetched from any external source.
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from core.model import SEED, REVIEW_CYCLE_MONTHS, build_model
from core.ref import (AS_OF, ANALYSTS, BRANCHES, DISPOSITIONS, RISK_TIER_BOUNDS, SLA_DAYS, START, TYPOLOGIES)

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DEFAULT_DB = ROOT / "warehouse.db"

# Dimension / fact load order (parents before children, so FK enforcement is never relaxed).
LOAD_ORDER = ["dim_date", "dim_branch", "dim_risk_tier", "dim_typology", "dim_disposition", "dim_analyst",
              "dim_customer", "fact_alert", "fact_smr", "fact_monthly_snapshot"]


# ------------------------------------------------------------------ helpers --
def date_key(s: pd.Series) -> pd.Series:
    """Timestamp -> yyyymmdd integer; NaT -> <NA> (nullable Int64)."""
    out = s.dt.year * 10000 + s.dt.month * 100 + s.dt.day
    return out.astype("Int64")


def build_dim_date(start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Calendar dimension covering whole years from `start` to `end` (Australian financial-year attributes)."""
    days = pd.date_range(pd.Timestamp(start.year, 1, 1), pd.Timestamp(end.year, 12, 31), freq="D")
    d = pd.DataFrame({"full_ts": days})
    d["date_key"] = date_key(d["full_ts"]).astype(int)
    d["full_date"] = d["full_ts"].dt.strftime("%Y-%m-%d")
    d["year"] = d["full_ts"].dt.year
    d["quarter"] = d["full_ts"].dt.quarter
    d["month"] = d["full_ts"].dt.month
    d["month_name"] = d["full_ts"].dt.strftime("%B")
    d["month_start_date"] = d["full_ts"].dt.strftime("%Y-%m-01")
    d["day_of_month"] = d["full_ts"].dt.day
    d["day_of_week"] = d["full_ts"].dt.dayofweek + 1
    d["day_name"] = d["full_ts"].dt.strftime("%A")
    d["is_weekend"] = (d["day_of_week"] >= 6).astype(int)
    d["is_month_end"] = d["full_ts"].dt.is_month_end.astype(int)
    d["fy_start_year"] = np.where(d["month"] >= 7, d["year"], d["year"] - 1)
    d["fy_label"] = "FY" + ((d["fy_start_year"] + 1) % 100).astype(str).str.zfill(2)
    d["fy_quarter"] = ((d["month"] - 7) % 12) // 3 + 1
    return d.drop(columns="full_ts")


def business_days(start: pd.Series, end: pd.Series) -> pd.Series:
    """Mon-Fri days between two date columns (end exclusive, like numpy.busday_count); no public holidays."""
    ok = start.notna() & end.notna()
    out = pd.Series(pd.array([pd.NA] * len(start), dtype="Int64"), index=start.index)
    if ok.any():
        s = start[ok].values.astype("datetime64[D]")
        e = end[ok].values.astype("datetime64[D]")
        out[ok] = np.busday_count(s, e)
    return out


def _days(a: pd.Series, b: pd.Series) -> pd.Series:
    return (b - a).dt.days.astype("Int64")


# ------------------------------------------------------------------ extract --
def extract(model: dict | None = None) -> dict:
    """Raw frames from the simulator. Uses the app's own fixed-seed generator, unchanged."""
    M = model if model is not None else build_model()
    return {"cust": M["cust"].copy(), "alerts": M["alerts"].copy(), "smrs": M["smrs"].copy(),
            "stock": M["stock"].copy(), "months": M["months"]}


# ---------------------------------------------------------------- transform --
def transform(raw: dict) -> dict[str, pd.DataFrame]:
    cust, alerts, smrs, stock = raw["cust"], raw["alerts"], raw["smrs"], raw["stock"]
    T: dict[str, pd.DataFrame] = {}

    # --- dim_date: spans every date that appears in the data (analyst start dates .. review due dates)
    all_dates = pd.concat([cust["onboarded"], cust["last_review"], cust["next_review_due"], alerts["opened"],
                           alerts["closed"], smrs["submitted"], smrs["acknowledged"], stock["date"],
                           pd.Series([pd.Timestamp(a["start"]) for a in ANALYSTS]), pd.Series([START, AS_OF])]).dropna()
    T["dim_date"] = build_dim_date(all_dates.min(), all_dates.max())

    # --- small reference dimensions (surrogate key = 1..n in reference order)
    T["dim_branch"] = pd.DataFrame([{"branch_key": i + 1, "branch_name": b["name"], "council_area": b["council"]}
                                    for i, b in enumerate(BRANCHES)])
    branch_key = dict(zip(T["dim_branch"]["branch_name"], T["dim_branch"]["branch_key"]))

    lo, hi = RISK_TIER_BOUNDS
    T["dim_risk_tier"] = pd.DataFrame([
        dict(risk_tier_key=1, risk_tier="Low", tier_rank=1, score_lower_bound=None, score_upper_bound=lo,
             bounds_rule=f"score < {lo:g}", review_cycle_months=REVIEW_CYCLE_MONTHS["Low"]),
        dict(risk_tier_key=2, risk_tier="Medium", tier_rank=2, score_lower_bound=lo, score_upper_bound=hi,
             bounds_rule=f"{lo:g} <= score <= {hi:g}", review_cycle_months=REVIEW_CYCLE_MONTHS["Medium"]),
        dict(risk_tier_key=3, risk_tier="High", tier_rank=3, score_lower_bound=hi, score_upper_bound=None,
             bounds_rule=f"score > {hi:g}", review_cycle_months=REVIEW_CYCLE_MONTHS["High"]),
    ])
    tier_key = dict(zip(T["dim_risk_tier"]["risk_tier"], T["dim_risk_tier"]["risk_tier_key"]))

    T["dim_typology"] = pd.DataFrame([
        dict(typology_key=i + 1, typology_name=n, description=s["desc"], model_base_rate=s["base_rate"],
             model_fp_rate_param=s["fp_rate"], model_avg_hours_param=s["hours"])
        for i, (n, s) in enumerate(TYPOLOGIES.items())])
    typ_key = dict(zip(T["dim_typology"]["typology_name"], T["dim_typology"]["typology_key"]))

    T["dim_disposition"] = pd.DataFrame([
        dict(disposition_key=i + 1, disposition=d,
             outcome_group="Pending" if d in ("Open", "Under investigation") else ("Escalated" if d.startswith("Escalated") else "Closed"),
             is_closed=int(d.startswith("Closed")), is_false_positive=int(d == "Closed — false positive"),
             is_escalated=int(d.startswith("Escalated")))
        for i, d in enumerate(DISPOSITIONS)])
    disp_key = dict(zip(T["dim_disposition"]["disposition"], T["dim_disposition"]["disposition_key"]))

    T["dim_analyst"] = pd.DataFrame([
        dict(analyst_key=i + 1, analyst_short=a["short"], analyst_name=a["name"], role=a["role"],
             home_branch_key=branch_key[a["branch"]], start_date_key=int(pd.Timestamp(a["start"]).strftime("%Y%m%d")),
             monthly_capacity=a["capacity"], avg_hours_param=a["avg_hours"])
        for i, a in enumerate(ANALYSTS)])
    analyst_key = dict(zip(T["dim_analyst"]["analyst_short"], T["dim_analyst"]["analyst_key"]))

    # --- dim_customer (type-1: the simulator holds one current row per client)
    c = cust.sort_values("customer_id", kind="stable").reset_index(drop=True)
    T["dim_customer"] = pd.DataFrame({
        "customer_key": np.arange(1, len(c) + 1),
        "customer_id": c["customer_id"],
        "customer_name": c["name"],
        "customer_type": c["type"],
        "channel": c["channel"],
        "foreign_tier": c["foreign_tier"],
        "linked_jurisdiction": c["fatf_jurisdiction"].where(c["fatf_jurisdiction"] != "—", None),
        "product": c["product"],
        "state": c["state"],
        "branch_key": c["branch"].map(branch_key),
        "risk_tier_key": c["risk_tier"].map(tier_key),
        "risk_score": c["risk_score"].round(4),
        "is_named_customer": c["named"].astype(int),
        "onboarded_date_key": date_key(c["onboarded"]),
        "last_review_date_key": date_key(c["last_review"]),
        "next_review_due_date_key": date_key(c["next_review_due"]),
        "review_overdue_flag": c["review_overdue"].astype(int),
    })
    cust_key = dict(zip(T["dim_customer"]["customer_id"], T["dim_customer"]["customer_key"]))

    # --- fact_alert
    a = alerts.sort_values("alert_id", kind="stable").reset_index(drop=True)
    T["fact_alert"] = pd.DataFrame({
        "alert_key": np.arange(1, len(a) + 1),
        "alert_id": a["alert_id"],
        "customer_key": a["customer_id"].map(cust_key),
        "typology_key": a["typology"].map(typ_key),
        "analyst_key": a["analyst"].map(analyst_key),
        "branch_key": a["branch"].map(branch_key),
        "disposition_key": a["disposition"].map(disp_key),
        "opened_date_key": date_key(a["opened"]),
        "closed_date_key": date_key(a["closed"]),
        "handling_hours": a["hours"],
        "days_to_close": _days(a["opened"], a["closed"]),
        "sla_breach_flag": a["sla_breach"].astype(int),
    })
    alert_key = dict(zip(T["fact_alert"]["alert_id"], T["fact_alert"]["alert_key"]))

    # --- fact_smr (business days measured from alert disposition date to AUSTRAC submission)
    s = smrs.sort_values("smr_id", kind="stable").reset_index(drop=True)
    alert_closed = s["alert_id"].map(dict(zip(alerts["alert_id"], alerts["closed"])))
    T["fact_smr"] = pd.DataFrame({
        "smr_key": np.arange(1, len(s) + 1),
        "smr_id": s["smr_id"],
        "alert_key": s["alert_id"].map(alert_key),
        "customer_key": s["customer_id"].map(cust_key),
        "typology_key": s["typology"].map(typ_key),
        "analyst_key": s["analyst"].map(analyst_key),
        "branch_key": s["branch"].map(branch_key),
        "escalated_date_key": date_key(s["escalated"]),
        "submitted_date_key": date_key(s["submitted"]),
        "acknowledged_date_key": date_key(s["acknowledged"]),
        "status": s["status"],
        "days_alert_close_to_submit": _days(pd.to_datetime(alert_closed), s["submitted"]),
        "bdays_alert_close_to_submit": business_days(pd.to_datetime(alert_closed), s["submitted"]),
        "days_submit_to_ack": _days(s["submitted"], s["acknowledged"]),
    })

    # --- fact_monthly_snapshot
    st = stock.reset_index().rename(columns={"index": "month_start"})
    T["fact_monthly_snapshot"] = pd.DataFrame({
        "month_start_date_key": date_key(st["month_start"]),
        "snapshot_date_key": date_key(st["date"]),
        "customers_active": st["customers_active"], "customers_low": st["customers_low"],
        "customers_medium": st["customers_medium"], "customers_high": st["customers_high"],
        "active_alerts": st["active_alerts"], "open_investigations": st["open_investigations"],
        "overdue_reviews": st["overdue_reviews"],
    })
    return T


# --------------------------------------------------------------------- load --
def _py(v):
    """numpy / pandas scalar -> plain Python (None for missing) for sqlite3 binding."""
    if v is None or v is pd.NA or v is pd.NaT:
        return None
    if isinstance(v, float) and np.isnan(v):
        return None
    if isinstance(v, np.generic):
        return v.item()
    return v


def load(tables: dict[str, pd.DataFrame], db_path: str | Path = DEFAULT_DB, meta: dict | None = None) -> sqlite3.Connection:
    """Create a fresh database from schema.sql and bulk-load the tables. Returns an open connection."""
    db_path = str(db_path)
    if db_path != ":memory:":
        Path(db_path).unlink(missing_ok=True)
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA_PATH.read_text())
    with con:
        for name in LOAD_ORDER:
            df = tables[name]
            cols = list(df.columns)
            rows = [tuple(_py(v) for v in r) for r in df.itertuples(index=False, name=None)]
            con.executemany(f"INSERT INTO {name} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})", rows)
            con.execute("INSERT INTO etl_load_audit VALUES (?, ?)", (name, len(rows)))
        meta = {"data_origin": "SIMULATED (core/model.py, fixed seed) - no real clients, matters or transactions",
                "seed": str(SEED), "as_of_date": AS_OF.strftime("%Y-%m-%d"), "history_start": START.strftime("%Y-%m-%d"),
                "sla_days": str(SLA_DAYS), **(meta or {})}
        con.executemany("INSERT INTO etl_meta VALUES (?, ?)", list(meta.items()))
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    if fk:
        raise RuntimeError(f"foreign key violations after load: {fk[:5]}")
    return con


def build_warehouse(db_path: str | Path = DEFAULT_DB, model: dict | None = None) -> sqlite3.Connection:
    raw = extract(model)
    return load(transform(raw), db_path)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=str(DEFAULT_DB), help="output SQLite path (default: ./warehouse.db)")
    args = ap.parse_args(argv)
    con = build_warehouse(args.db)
    for name, n in con.execute("SELECT table_name, row_count FROM etl_load_audit"):
        print(f"{name:24s}{n:>8d}")
    con.close()
    print(f"warehouse written to {args.db}")


if __name__ == "__main__":
    main()
