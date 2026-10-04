-- Dimensional model (star schema) for the simulated AML/CTF compliance dataset.
-- SQLite dialect. Surrogate keys are integers assigned deterministically by the loader;
-- natural/business keys are kept as UNIQUE columns. See docs/DATA_MODEL.md.
PRAGMA foreign_keys = ON;

CREATE TABLE etl_meta (
    meta_key   TEXT PRIMARY KEY,
    meta_value TEXT NOT NULL
);

CREATE TABLE etl_load_audit (
    table_name TEXT PRIMARY KEY,
    row_count  INTEGER NOT NULL
);

-- ---------------------------------------------------------------- dimensions
CREATE TABLE dim_date (
    date_key          INTEGER PRIMARY KEY,          -- yyyymmdd
    full_date         TEXT NOT NULL UNIQUE,         -- ISO yyyy-mm-dd
    year              INTEGER NOT NULL,
    quarter           INTEGER NOT NULL,
    month             INTEGER NOT NULL,
    month_name        TEXT NOT NULL,
    month_start_date  TEXT NOT NULL,
    day_of_month      INTEGER NOT NULL,
    day_of_week       INTEGER NOT NULL,             -- 1 = Monday .. 7 = Sunday
    day_name          TEXT NOT NULL,
    is_weekend        INTEGER NOT NULL CHECK (is_weekend IN (0, 1)),
    is_month_end      INTEGER NOT NULL CHECK (is_month_end IN (0, 1)),
    fy_start_year     INTEGER NOT NULL,             -- Australian financial year (1 Jul - 30 Jun)
    fy_label          TEXT NOT NULL,                -- e.g. FY26
    fy_quarter        INTEGER NOT NULL              -- 1 = Jul-Sep
);

CREATE TABLE dim_branch (
    branch_key   INTEGER PRIMARY KEY,
    branch_name  TEXT NOT NULL UNIQUE,
    council_area TEXT NOT NULL
);

CREATE TABLE dim_risk_tier (
    risk_tier_key        INTEGER PRIMARY KEY,
    risk_tier            TEXT NOT NULL UNIQUE,
    tier_rank            INTEGER NOT NULL,          -- 1 = Low .. 3 = High
    score_lower_bound    REAL,                      -- NULL = open-ended
    score_upper_bound    REAL,                      -- NULL = open-ended
    bounds_rule          TEXT NOT NULL,             -- exact inclusive/exclusive rule, as in core/model.py::_tier
    review_cycle_months  INTEGER NOT NULL
);

CREATE TABLE dim_typology (
    typology_key          INTEGER PRIMARY KEY,
    typology_name         TEXT NOT NULL UNIQUE,
    description           TEXT NOT NULL,
    model_base_rate       REAL NOT NULL,            -- generator parameter: alerts per active client per month
    model_fp_rate_param   REAL NOT NULL,            -- generator parameter (NOT an observed rate)
    model_avg_hours_param REAL NOT NULL
);

CREATE TABLE dim_disposition (
    disposition_key   INTEGER PRIMARY KEY,
    disposition       TEXT NOT NULL UNIQUE,
    outcome_group     TEXT NOT NULL,                -- Pending / Escalated / Closed
    is_closed         INTEGER NOT NULL CHECK (is_closed IN (0, 1)),
    is_false_positive INTEGER NOT NULL CHECK (is_false_positive IN (0, 1)),
    is_escalated      INTEGER NOT NULL CHECK (is_escalated IN (0, 1))
);

CREATE TABLE dim_analyst (
    analyst_key      INTEGER PRIMARY KEY,
    analyst_short    TEXT NOT NULL UNIQUE,
    analyst_name     TEXT NOT NULL,
    role             TEXT NOT NULL,
    home_branch_key  INTEGER NOT NULL REFERENCES dim_branch (branch_key),
    start_date_key   INTEGER NOT NULL REFERENCES dim_date (date_key),
    monthly_capacity INTEGER NOT NULL,
    avg_hours_param  REAL NOT NULL
);

CREATE TABLE dim_customer (
    customer_key             INTEGER PRIMARY KEY,
    customer_id              TEXT NOT NULL UNIQUE,  -- business key CL-00001
    customer_name            TEXT NOT NULL,         -- NOT unique in the source
    customer_type            TEXT NOT NULL,
    channel                  TEXT NOT NULL,
    foreign_tier             TEXT NOT NULL,
    linked_jurisdiction      TEXT,                  -- fictional jurisdiction; NULL if domestic
    product                  TEXT NOT NULL,
    state                    TEXT NOT NULL,
    branch_key               INTEGER NOT NULL REFERENCES dim_branch (branch_key),
    risk_tier_key            INTEGER NOT NULL REFERENCES dim_risk_tier (risk_tier_key),
    risk_score               REAL NOT NULL CHECK (risk_score BETWEEN 1 AND 100),
    is_named_customer        INTEGER NOT NULL CHECK (is_named_customer IN (0, 1)),
    onboarded_date_key       INTEGER NOT NULL REFERENCES dim_date (date_key),
    last_review_date_key     INTEGER NOT NULL REFERENCES dim_date (date_key),
    next_review_due_date_key INTEGER NOT NULL REFERENCES dim_date (date_key),
    review_overdue_flag      INTEGER NOT NULL CHECK (review_overdue_flag IN (0, 1))
);

-- --------------------------------------------------------------------- facts
-- Grain: one row per monitoring alert.
CREATE TABLE fact_alert (
    alert_key        INTEGER PRIMARY KEY,
    alert_id         TEXT NOT NULL UNIQUE,          -- degenerate / business key
    customer_key     INTEGER NOT NULL REFERENCES dim_customer (customer_key),
    typology_key     INTEGER NOT NULL REFERENCES dim_typology (typology_key),
    analyst_key      INTEGER NOT NULL REFERENCES dim_analyst (analyst_key),
    branch_key       INTEGER NOT NULL REFERENCES dim_branch (branch_key),
    disposition_key  INTEGER NOT NULL REFERENCES dim_disposition (disposition_key),
    opened_date_key  INTEGER NOT NULL REFERENCES dim_date (date_key),
    closed_date_key  INTEGER REFERENCES dim_date (date_key),   -- NULL while open / under investigation
    handling_hours   REAL NOT NULL CHECK (handling_hours > 0),
    days_to_close    INTEGER CHECK (days_to_close >= 0),
    sla_breach_flag  INTEGER NOT NULL CHECK (sla_breach_flag IN (0, 1))
);

-- Grain: one row per suspicious matter report (SMR) in the register.
CREATE TABLE fact_smr (
    smr_key                 INTEGER PRIMARY KEY,
    smr_id                  TEXT NOT NULL UNIQUE,
    alert_key               INTEGER NOT NULL UNIQUE REFERENCES fact_alert (alert_key),
    customer_key            INTEGER NOT NULL REFERENCES dim_customer (customer_key),
    typology_key            INTEGER NOT NULL REFERENCES dim_typology (typology_key),
    analyst_key             INTEGER NOT NULL REFERENCES dim_analyst (analyst_key),
    branch_key              INTEGER NOT NULL REFERENCES dim_branch (branch_key),
    escalated_date_key      INTEGER NOT NULL REFERENCES dim_date (date_key),
    submitted_date_key      INTEGER REFERENCES dim_date (date_key),   -- NULL while Draft
    acknowledged_date_key   INTEGER REFERENCES dim_date (date_key),   -- NULL until acknowledged
    status                  TEXT NOT NULL CHECK (status IN ('Draft', 'Submitted', 'Acknowledged')),
    days_alert_close_to_submit  INTEGER,            -- calendar days
    bdays_alert_close_to_submit INTEGER,            -- Mon-Fri days, no public holidays
    days_submit_to_ack      INTEGER
);

-- Grain: one row per calendar month (point-in-time stock snapshot from the model's `stock` frame).
CREATE TABLE fact_monthly_snapshot (
    month_start_date_key INTEGER PRIMARY KEY REFERENCES dim_date (date_key),
    snapshot_date_key    INTEGER NOT NULL REFERENCES dim_date (date_key),
    customers_active     INTEGER NOT NULL,
    customers_low        INTEGER NOT NULL,
    customers_medium     INTEGER NOT NULL,
    customers_high       INTEGER NOT NULL,
    active_alerts        INTEGER NOT NULL,
    open_investigations  INTEGER NOT NULL,
    overdue_reviews      INTEGER NOT NULL
);

-- ------------------------------------------------------------------- indexes
CREATE INDEX ix_customer_branch   ON dim_customer (branch_key);
CREATE INDEX ix_customer_tier     ON dim_customer (risk_tier_key);
CREATE INDEX ix_alert_customer    ON fact_alert (customer_key);
CREATE INDEX ix_alert_typology    ON fact_alert (typology_key);
CREATE INDEX ix_alert_analyst     ON fact_alert (analyst_key);
CREATE INDEX ix_alert_branch      ON fact_alert (branch_key);
CREATE INDEX ix_alert_disposition ON fact_alert (disposition_key);
CREATE INDEX ix_alert_opened      ON fact_alert (opened_date_key);
CREATE INDEX ix_alert_closed      ON fact_alert (closed_date_key);
CREATE INDEX ix_smr_customer      ON fact_smr (customer_key);
CREATE INDEX ix_smr_typology      ON fact_smr (typology_key);
CREATE INDEX ix_smr_analyst       ON fact_smr (analyst_key);
CREATE INDEX ix_smr_submitted     ON fact_smr (submitted_date_key);
