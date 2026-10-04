# Skills demonstrated

Where each data analyst / data engineer skill is shown in this repository. Every path exists and is covered by tests.
All data is simulated (fixed seed); the skills are real, the dataset is not.

| Skill | Evidence |
|---|---|
| **SQL: CTEs, joins, CASE** | all ten queries in [`sql/analysis/`](../sql/analysis), e.g. `sql/analysis/02_typology_risk_rating_mix.sql` |
| **SQL: window functions** (RANK, LAG, NTILE, PERCENT_RANK, running totals, moving average frames) | `sql/analysis/04_structuring_monthly_trend.sql` (LAG, 3-month frame, running total/YTD), `sql/analysis/03_smr_timeliness.sql` (NTILE, PERCENT_RANK, LAG), `sql/analysis/10_alert_concentration_pareto.sql` (cumulative share), `sql/analysis/07_analyst_workload_sla.sql` |
| **SQL: date arithmetic and month spines** | `sql/analysis/05_structuring_repeat_clients.sql` (gap to previous alert), `sql/analysis/04_structuring_monthly_trend.sql` (zero-filled spine) |
| **Dimensional modelling** (star schema, grain, surrogate keys, role-playing dates, snapshot fact) | `warehouse/schema.sql`, `docs/DATA_MODEL.md` |
| **Data mapping** (source-to-target, transformation rules) | `docs/DATA_DICTIONARY.md`, `warehouse/build.py` |
| **ETL / pipeline design** (extract, transform, load; idempotent rebuild; audit tables) | `warehouse/build.py` (`extract`, `transform`, `load`, `etl_load_audit`, `etl_meta`) |
| **Data quality** (completeness, uniqueness, referential integrity, validity, reconciliation to app metrics) | `warehouse/quality.py`, `docs/DATA_QUALITY.md` |
| **Constraints and performance** (PK/FK/CHECK/UNIQUE, indexes, query-plan test) | `warehouse/schema.sql`, `tests/test_warehouse.py` |
| **Testing** (unit, integration, fault injection, doc-drift and output-freshness tests) | `tests/test_warehouse.py`, `tests/test_sql_queries.py`, `tests/test_docs.py`, plus the app's `tests/test_reconciliation.py` |
| **CI** (tests plus warehouse build, DQ suite and queries on every push) | `.github/workflows/ci.yml` |
| **Reproducibility** (fixed seed, deterministic outputs, committed result files) | `core/model.py`, `docs/query_results/01_alert_triage_funnel.csv` |
| **Python / pandas / NumPy** | `warehouse/build.py`, `core/model.py`, `core/metrics.py` |
| **Dashboarding / BI** | `app.py`, `core/metrics.py` (Streamlit, Plotly) |
| **AML/CTF domain** (4-factor risk rating, typologies, alert triage, SMR timeliness, periodic CDD review) | `core/ref.py`, `docs/METHODOLOGY.md`, `sql/analysis/01_alert_triage_funnel.sql`, `sql/analysis/03_smr_timeliness.sql`, `sql/analysis/06_rule_hit_rate_false_positive.sql` |
| **Documentation** | `README.md`, `docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md` |

## Not claimed

* No real data, no API or web ingestion, no production database or cloud warehouse: the target is SQLite on simulated data.
* No orchestration tool (Airflow, dbt, etc.); the pipeline is a plain Python module run from the command line and CI.
* No transaction-level data: the simulator generates alerts, so the structuring analysis is alert-pattern analysis only.
* The customer dimension is type 1 (no history); a type-2 design is described but not faked.
