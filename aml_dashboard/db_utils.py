"""
Shared database connection + queries used across all pages of the
AML/KYC Intelligence Dashboard.

Edit DB_CONFIG below with your local Postgres credentials.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "aml_platform",
    "user": "postgres",       # change if different
    "password": "",           # set your password
}


@st.cache_resource
def get_engine():
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    return create_engine(url)


@st.cache_data(ttl=300)
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})


# ------------------------------------------------------------------
# Reusable SQL blocks
# ------------------------------------------------------------------

RISK_SCORE_SQL = """
WITH structuring AS (
    SELECT customer_id, COUNT(*) AS structuring_count, SUM(amount) AS structuring_total
    FROM transactions
    WHERE transaction_type = 'Cash Deposit' AND amount BETWEEN 9000 AND 9999
    GROUP BY customer_id
    HAVING COUNT(*) >= 3
),
rapid AS (
    SELECT DISTINCT t1.customer_id
    FROM transactions t1
    JOIN transactions t2
      ON t1.customer_id = t2.customer_id
     AND t2.transaction_type IN ('Wire Transfer','Withdrawal')
     AND t2.transaction_date > t1.transaction_date
     AND t2.transaction_date <= t1.transaction_date + INTERVAL '2 days'
    WHERE t1.transaction_type = 'Deposit' AND t1.amount >= 8000
),
highrisk AS (
    SELECT DISTINCT customer_id
    FROM transactions
    WHERE transaction_type = 'Wire Transfer'
      AND counterparty_country IN ('Iran','North Korea','Myanmar','Syria','Yemen')
),
screening_flag AS (
    SELECT DISTINCT customer_id
    FROM screening_results
    WHERE status IN ('Potential Match','Confirmed Match')
)
SELECT
    c.customer_id, c.full_name, c.customer_type, c.country, c.residency_country,
    c.industry, c.occupation, c.annual_income, c.account_open_date, c.customer_status,
    CASE WHEN s.customer_id IS NOT NULL THEN 1 ELSE 0 END AS structuring,
    COALESCE(s.structuring_count, 0) AS structuring_count,
    COALESCE(s.structuring_total, 0) AS structuring_total,
    CASE WHEN r.customer_id IS NOT NULL THEN 1 ELSE 0 END AS rapid_movement,
    CASE WHEN h.customer_id IS NOT NULL THEN 1 ELSE 0 END AS high_risk_country,
    CASE WHEN sc.customer_id IS NOT NULL THEN 1 ELSE 0 END AS screening_hit,
    (CASE WHEN s.customer_id IS NOT NULL THEN 1 ELSE 0 END
     + CASE WHEN r.customer_id IS NOT NULL THEN 1 ELSE 0 END
     + CASE WHEN h.customer_id IS NOT NULL THEN 1 ELSE 0 END
     + CASE WHEN sc.customer_id IS NOT NULL THEN 1 ELSE 0 END) AS risk_score
FROM customers c
LEFT JOIN structuring s ON c.customer_id = s.customer_id
LEFT JOIN rapid r ON c.customer_id = r.customer_id
LEFT JOIN highrisk h ON c.customer_id = h.customer_id
LEFT JOIN screening_flag sc ON c.customer_id = sc.customer_id
ORDER BY risk_score DESC, c.customer_id;
"""

SCREENING_DETAIL_SQL = """
SELECT screening_id, customer_id, screening_type, status, screening_date, match_details
FROM screening_results
ORDER BY customer_id, screening_type;
"""

TRANSACTIONS_SQL = """
SELECT transaction_id, customer_id, transaction_date, transaction_type,
       amount, currency, counterparty_country, channel
FROM transactions
ORDER BY customer_id, transaction_date;
"""

OWNERSHIP_SQL = """
SELECT business_id, chain_id, level, owner_id, owner_name, owner_type,
       ownership_percentage, is_ubo, parent_owner_id
FROM ownership
ORDER BY business_id, level;
"""


def customer_transactions(customer_id: str) -> pd.DataFrame:
    sql = """
        SELECT transaction_date, transaction_type, amount, currency,
               counterparty_country, channel
        FROM transactions
        WHERE customer_id = :cid
        ORDER BY transaction_date;
    """
    return run_query(sql, {"cid": customer_id})


def customer_screening(customer_id: str) -> pd.DataFrame:
    sql = """
        SELECT screening_type, status, screening_date, match_details
        FROM screening_results
        WHERE customer_id = :cid
        ORDER BY screening_type;
    """
    return run_query(sql, {"cid": customer_id})


def customer_profile(customer_id: str) -> pd.DataFrame:
    sql = "SELECT * FROM customers WHERE customer_id = :cid;"
    return run_query(sql, {"cid": customer_id})
