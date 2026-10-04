# Data dictionary and source-to-target mapping

Every column in `warehouse/schema.sql`, with the simulated source field it comes from and the transformation rule applied by `warehouse/build.py`.
All source fields come from the app's fixed-seed generator (`core.model.build_model()`): `cust` = client register, `alerts` = alert ledger, `smrs` = SMR register, `stock` = monthly stock frame.
**All data is simulated.** "Generator parameter" columns hold simulation inputs, not observed rates. A test (`tests/test_docs.py`) fails if a warehouse column is missing from this file.

## dim_date
4,749 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `date_key` | INTEGER | PK | Surrogate key, yyyymmdd integer | Generated: calendar spine, whole years covering the earliest to latest date in the data |
| `full_date` | TEXT |  | ISO date | Generated |
| `year` | INTEGER |  | Calendar year | Generated |
| `quarter` | INTEGER |  | Calendar quarter 1-4 | Generated |
| `month` | INTEGER |  | Calendar month 1-12 | Generated |
| `month_name` | TEXT |  | Month name | Generated |
| `month_start_date` | TEXT |  | First day of the month (ISO) | Generated; join key for monthly rollups |
| `day_of_month` | INTEGER |  | Day of month | Generated |
| `day_of_week` | INTEGER |  | 1 = Monday .. 7 = Sunday | Generated |
| `day_name` | TEXT |  | Weekday name | Generated |
| `is_weekend` | INTEGER |  | 1 if Saturday/Sunday | day_of_week >= 6 |
| `is_month_end` | INTEGER |  | 1 if last day of month | Generated |
| `fy_start_year` | INTEGER |  | Australian FY start year (FY runs 1 Jul - 30 Jun) | year if month >= 7 else year - 1 |
| `fy_label` | TEXT |  | FY label e.g. FY26 | "FY" + two-digit (fy_start_year + 1) |
| `fy_quarter` | INTEGER |  | Fiscal quarter, 1 = Jul-Sep | ((month - 7) mod 12) div 3 + 1 |

## dim_branch
3 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `branch_key` | INTEGER | PK | Surrogate key | Row order of core.ref.BRANCHES, from 1 |
| `branch_name` | TEXT |  | Office name | BRANCHES[].name |
| `council_area` | TEXT |  | Local council area | BRANCHES[].council |

## dim_risk_tier
3 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `risk_tier_key` | INTEGER | PK | Surrogate key | Fixed 1-3 |
| `risk_tier` | TEXT |  | Low / Medium / High | Tier names from core.model._tier |
| `tier_rank` | INTEGER |  | 1 = Low .. 3 = High | Fixed |
| `score_lower_bound` | REAL |  | Lower score bound; NULL = open | core.ref.RISK_TIER_BOUNDS |
| `score_upper_bound` | REAL |  | Upper score bound; NULL = open | core.ref.RISK_TIER_BOUNDS |
| `bounds_rule` | TEXT |  | Exact inclusive/exclusive rule text | Generated from bounds |
| `review_cycle_months` | INTEGER |  | Periodic CDD review cycle for the tier | core.model.REVIEW_CYCLE_MONTHS |

## dim_typology
5 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `typology_key` | INTEGER | PK | Surrogate key | Row order of core.ref.TYPOLOGIES, from 1 |
| `typology_name` | TEXT |  | Monitoring rule / ML typology | TYPOLOGIES key |
| `description` | TEXT |  | What the rule looks for | TYPOLOGIES[].desc |
| `model_base_rate` | REAL |  | Generator parameter: alerts per active client per month | TYPOLOGIES[].base_rate (a simulation input, not an observed rate) |
| `model_fp_rate_param` | REAL |  | Generator parameter for false-positive share (NOT observed) | TYPOLOGIES[].fp_rate |
| `model_avg_hours_param` | REAL |  | Generator parameter for mean handling hours | TYPOLOGIES[].hours |

## dim_disposition
5 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `disposition_key` | INTEGER | PK | Surrogate key | Row order of core.ref.DISPOSITIONS, from 1 |
| `disposition` | TEXT |  | Alert outcome label | DISPOSITIONS |
| `outcome_group` | TEXT |  | Pending / Escalated / Closed | CASE: Open and Under investigation = Pending; starts with Escalated = Escalated; else Closed |
| `is_closed` | INTEGER |  | 1 for Closed - false positive / no further action | disposition starts with "Closed" |
| `is_false_positive` | INTEGER |  | 1 for Closed - false positive | disposition = "Closed — false positive" |
| `is_escalated` | INTEGER |  | 1 for Escalated to SMR | disposition starts with "Escalated" |

## dim_analyst
6 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `analyst_key` | INTEGER | PK | Surrogate key | Row order of core.ref.ANALYSTS, from 1 |
| `analyst_short` | TEXT |  | Short name used in the alert ledger (business key) | ANALYSTS[].short |
| `analyst_name` | TEXT |  | Full name (fictional) | ANALYSTS[].name |
| `role` | TEXT |  | Job role | ANALYSTS[].role |
| `home_branch_key` | INTEGER | FK -> dim_branch.branch_key | FK to dim_branch | Lookup by ANALYSTS[].branch |
| `start_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date: first day in team | ANALYSTS[].start -> yyyymmdd |
| `monthly_capacity` | INTEGER |  | Alert caseload cap per month | ANALYSTS[].capacity |
| `avg_hours_param` | REAL |  | Generator parameter: average handling hours | ANALYSTS[].avg_hours |

## dim_customer
236 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `customer_key` | INTEGER | PK | Surrogate key | Dense 1..n, ordered by customer_id |
| `customer_id` | TEXT |  | Business key CL-00001.. | cust.customer_id |
| `customer_name` | TEXT |  | Client name; NOT unique (the simulator can repeat names) | cust.name |
| `customer_type` | TEXT |  | AUSTRAC customer-type factor value | cust.type |
| `channel` | TEXT |  | Delivery-channel factor value | cust.channel |
| `foreign_tier` | TEXT |  | Foreign-dimension tier | cust.foreign_tier |
| `linked_jurisdiction` | TEXT |  | Fictional linked jurisdiction; NULL if domestic | cust.fatf_jurisdiction; the placeholder "—" becomes NULL |
| `product` | TEXT |  | Product/service factor value | cust.product |
| `state` | TEXT |  | Registered Australian state/territory | cust.state |
| `branch_key` | INTEGER | FK -> dim_branch.branch_key | FK to dim_branch | Lookup cust.branch |
| `risk_tier_key` | INTEGER | FK -> dim_risk_tier.risk_tier_key | FK to dim_risk_tier | Lookup cust.risk_tier |
| `risk_score` | REAL |  | 4-factor risk score 1-100 | cust.risk_score rounded to 4 dp |
| `is_named_customer` | INTEGER |  | 1 if one of the hand-defined named clients | cust.named -> 0/1 |
| `onboarded_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date | cust.onboarded -> yyyymmdd |
| `last_review_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date | cust.last_review -> yyyymmdd |
| `next_review_due_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date | cust.next_review_due -> yyyymmdd |
| `review_overdue_flag` | INTEGER |  | 1 if next review due before the as-of date | cust.review_overdue -> 0/1 |

## fact_alert
388 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `alert_key` | INTEGER | PK | Surrogate key | Dense 1..n, ordered by alert_id |
| `alert_id` | TEXT |  | Business key ALT-2025000.. | alerts.alert_id |
| `customer_key` | INTEGER | FK -> dim_customer.customer_key | FK to dim_customer | Lookup alerts.customer_id |
| `typology_key` | INTEGER | FK -> dim_typology.typology_key | FK to dim_typology | Lookup alerts.typology |
| `analyst_key` | INTEGER | FK -> dim_analyst.analyst_key | FK to dim_analyst | Lookup alerts.analyst |
| `branch_key` | INTEGER | FK -> dim_branch.branch_key | FK to dim_branch (client branch) | Lookup alerts.branch |
| `disposition_key` | INTEGER | FK -> dim_disposition.disposition_key | FK to dim_disposition | Lookup alerts.disposition |
| `opened_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date | alerts.opened -> yyyymmdd |
| `closed_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date; NULL while pending | alerts.closed -> yyyymmdd; NaT -> NULL |
| `handling_hours` | REAL |  | Analyst hours spent | alerts.hours |
| `days_to_close` | INTEGER |  | Calendar days opened -> closed; NULL while pending | closed - opened in days |
| `sla_breach_flag` | INTEGER |  | 1 if turnaround exceeded the SLA (10 days) | alerts.sla_breach -> 0/1 |

## fact_smr
98 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `smr_key` | INTEGER | PK | Surrogate key | Dense 1..n, ordered by smr_id |
| `smr_id` | TEXT |  | Business key SMR-2025100.. | smrs.smr_id |
| `alert_key` | INTEGER | FK -> fact_alert.alert_key | FK to fact_alert (1:1) | Lookup smrs.alert_id |
| `customer_key` | INTEGER | FK -> dim_customer.customer_key | FK to dim_customer | Lookup smrs.customer_id |
| `typology_key` | INTEGER | FK -> dim_typology.typology_key | FK to dim_typology | Lookup smrs.typology |
| `analyst_key` | INTEGER | FK -> dim_analyst.analyst_key | FK to dim_analyst | Lookup smrs.analyst |
| `branch_key` | INTEGER | FK -> dim_branch.branch_key | FK to dim_branch | Lookup smrs.branch |
| `escalated_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date | smrs.escalated -> yyyymmdd |
| `submitted_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date; NULL while Draft | smrs.submitted -> yyyymmdd |
| `acknowledged_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date; NULL until acknowledged | smrs.acknowledged -> yyyymmdd |
| `status` | TEXT |  | Draft / Submitted / Acknowledged | smrs.status |
| `days_alert_close_to_submit` | INTEGER |  | Calendar days from alert closed to submission | submitted - alerts.closed (via alert_id) |
| `bdays_alert_close_to_submit` | INTEGER |  | Mon-Fri days from alert closed to submission (no public holidays) | numpy.busday_count(alerts.closed, submitted) |
| `days_submit_to_ack` | INTEGER |  | Calendar days submitted -> acknowledged | acknowledged - submitted |

## fact_monthly_snapshot
27 rows.

| Column | Type | Key | Description | Source -> transformation rule |
|---|---|---|---|---|
| `month_start_date_key` | INTEGER | PK -> dim_date.date_key | PK and FK to dim_date: first day of month | stock index (month start) -> yyyymmdd |
| `snapshot_date_key` | INTEGER | FK -> dim_date.date_key | FK to dim_date: the as-at date of the stock (month end, or the as-of date for the current month) | stock.date -> yyyymmdd |
| `customers_active` | INTEGER |  | Clients onboarded by snapshot date | stock.customers_active |
| `customers_low` | INTEGER |  | ...of which Low risk | stock.customers_low |
| `customers_medium` | INTEGER |  | ...of which Medium risk | stock.customers_medium |
| `customers_high` | INTEGER |  | ...of which High risk | stock.customers_high |
| `active_alerts` | INTEGER |  | Alerts open at snapshot date | stock.active_alerts |
| `open_investigations` | INTEGER |  | Alerts under investigation at snapshot date | stock.open_investigations |
| `overdue_reviews` | INTEGER |  | Clients with a review overdue at snapshot date | stock.overdue_reviews |

## Transformations applied across tables

* **Surrogate keys** are dense integers assigned in business-key order, so rebuilds are byte-for-byte reproducible.
* **Dates** become `yyyymmdd` integer keys into `dim_date`; missing dates (open alerts, draft SMRs) stay NULL rather than a sentinel date.
* **Booleans** become 0/1 integers with CHECK constraints.
* **Denormalised source columns dropped:** `alerts.risk_tier`, `alerts.state`, `alerts.channel`, `alerts.customer` (name) are attributes of the client and are reached through `dim_customer`; the data-quality suite checks they agree with the source.
* **`alerts.is_false_positive` (hidden generator label) is not loaded.** It is drawn even for alerts that are still open, so it is not an observed outcome. False positives are derived from the disposition (`dim_disposition.is_false_positive`), exactly as the app does.
* **`stock.date` / month index** become the snapshot grain; `core.model` rescales the in-progress month in the `fin` frame for the app, but `fin` is not loaded (it is derivable from the facts and is reconciled instead).
* **Not modelled (no source data):** individual transactions, cash amounts, counterparties. The structuring analysis therefore uses alert counts, not transaction values.
