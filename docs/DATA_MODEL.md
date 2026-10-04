# Data model

A Kimball-style star schema in SQLite (`warehouse.db`, built by `python -m warehouse.build`, gitignored). It is loaded from the
**simulated** dataset in `core/model.py` (fixed seed), not from any real firm or AUSTRAC data. DDL: [`warehouse/schema.sql`](../warehouse/schema.sql).
Column-level detail and the source-to-target mapping: [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

```mermaid
erDiagram
    dim_date ||--o{ fact_alert : "opened / closed"
    dim_date ||--o{ fact_smr : "escalated / submitted / acknowledged"
    dim_date ||--o{ dim_customer : "onboarded / last review / next review due"
    dim_date ||--o{ fact_monthly_snapshot : "month start / snapshot date"
    dim_date ||--o{ dim_analyst : "start date"
    dim_branch ||--o{ dim_customer : "serves"
    dim_branch ||--o{ dim_analyst : "home branch"
    dim_branch ||--o{ fact_alert : ""
    dim_branch ||--o{ fact_smr : ""
    dim_risk_tier ||--o{ dim_customer : "rated"
    dim_customer ||--o{ fact_alert : "subject of"
    dim_customer ||--o{ fact_smr : ""
    dim_typology ||--o{ fact_alert : "rule that fired"
    dim_typology ||--o{ fact_smr : ""
    dim_analyst ||--o{ fact_alert : "worked by"
    dim_analyst ||--o{ fact_smr : ""
    dim_disposition ||--o{ fact_alert : "outcome"
    fact_alert ||--o| fact_smr : "escalated to"

    dim_customer {
        int customer_key PK
        text customer_id UK
        text customer_name
        text customer_type
        text channel
        text foreign_tier
        text product
        text state
        int branch_key FK
        int risk_tier_key FK
        real risk_score
        int onboarded_date_key FK
        int next_review_due_date_key FK
        int review_overdue_flag
    }
    fact_alert {
        int alert_key PK
        text alert_id UK
        int customer_key FK
        int typology_key FK
        int analyst_key FK
        int branch_key FK
        int disposition_key FK
        int opened_date_key FK
        int closed_date_key FK
        real handling_hours
        int days_to_close
        int sla_breach_flag
    }
    fact_smr {
        int smr_key PK
        text smr_id UK
        int alert_key FK
        int escalated_date_key FK
        int submitted_date_key FK
        int acknowledged_date_key FK
        text status
        int bdays_alert_close_to_submit
        int days_submit_to_ack
    }
    fact_monthly_snapshot {
        int month_start_date_key PK
        int snapshot_date_key FK
        int customers_active
        int active_alerts
        int overdue_reviews
    }
    dim_typology {
        int typology_key PK
        text typology_name UK
    }
    dim_analyst {
        int analyst_key PK
        text analyst_short UK
        int home_branch_key FK
    }
    dim_disposition {
        int disposition_key PK
        text disposition UK
        text outcome_group
    }
    dim_risk_tier {
        int risk_tier_key PK
        text risk_tier UK
        int review_cycle_months
    }
    dim_branch {
        int branch_key PK
        text branch_name UK
    }
    dim_date {
        int date_key PK
        text full_date UK
        text fy_label
    }
```

(The diagram shows keys and principal attributes only; every column is listed in the data dictionary.)

## Grain

| Table | Type | Grain (one row per...) | Natural / business key | Surrogate key |
|---|---|---|---|---|
| `fact_alert` | Transaction fact | monitoring alert | `alert_id` | `alert_key` |
| `fact_smr` | Transaction fact | suspicious matter report in the register (1:1 with an escalated alert) | `smr_id`, `alert_key` | `smr_key` |
| `fact_monthly_snapshot` | Periodic snapshot fact | calendar month (stock at month end, or at the as-of date for the current month) | month start date | `month_start_date_key` |
| `dim_customer` | Dimension (type 1) | client | `customer_id` (names are not unique) | `customer_key` |
| `dim_analyst` | Dimension | compliance analyst | `analyst_short` | `analyst_key` |
| `dim_typology` | Dimension | monitoring rule / typology | `typology_name` | `typology_key` |
| `dim_disposition` | Dimension | alert outcome | `disposition` | `disposition_key` |
| `dim_risk_tier` | Dimension | risk tier (Low / Medium / High) | `risk_tier` | `risk_tier_key` |
| `dim_branch` | Dimension | office | `branch_name` | `branch_key` |
| `dim_date` | Date dimension | calendar day (contiguous, with Australian financial-year attributes) | `full_date` | `date_key` = yyyymmdd |

## Design decisions

* **Additive vs non-additive measures.** `handling_hours`, `days_to_close` and the flags are additive or averageable across the alert grain. The snapshot fact's stocks (`customers_active`, `active_alerts`...) are **semi-additive**: sum across dimensions, never across months.
* **Role-playing dates.** `dim_date` is joined several times under different roles (opened, closed, submitted, acknowledged, onboarded, ...). Role is encoded in the key column name.
* **Nullable date keys instead of a sentinel row.** Open alerts have no closed date and Draft SMRs have no submitted date. The schema allows NULL only on those keys and the quality suite verifies NULL occurs if and only if the lifecycle state says so.
* **Type-1 customer dimension.** The simulator holds one current row per client, so history of risk-tier changes is not modelled. (A real implementation would use a type-2 slowly changing dimension; this is deliberately not faked here.)
* **No transaction fact.** The simulator generates alerts, not the underlying transactions, so there is no `fact_transaction`.
* **Integrity.** Foreign keys are enforced at load (`PRAGMA foreign_keys = ON` and a `foreign_key_check` after load); CHECK constraints guard flags, status, score range and hours; indexes cover every fact foreign key and the date columns used by the analysis queries.
* **Lineage / audit.** `etl_meta` records the data origin (SIMULATED), seed and as-of date; `etl_load_audit` records the row count loaded into every table.

## Pipeline

```mermaid
flowchart LR
    gen["core/model.py<br/>build_model() - fixed seed"] --> ext["warehouse/build.py<br/>extract()"]
    ext --> tr["transform()<br/>keys, flags, business-day measures, date spine"]
    tr --> ld["load()<br/>schema.sql DDL, FK-ordered bulk insert,<br/>foreign_key_check"]
    ld --> db[("warehouse.db<br/>(gitignored)")]
    db --> dq["warehouse/quality.py<br/>docs/DATA_QUALITY.md"]
    db --> sql["sql/analysis/*.sql<br/>sql/run_queries.py"]
    sql --> csv["docs/query_results/*.csv"]
```
