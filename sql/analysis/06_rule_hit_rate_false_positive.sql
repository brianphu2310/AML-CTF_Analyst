-- Monitoring rule (typology) performance: hit rate, false-positive rate and precision, with ranking.
-- hit rate = alerts per 100 client-months of exposure (client-months from the monthly snapshot fact).
-- fp_rate = false positives / finalised alerts (closed or escalated; excludes still-open alerts). The app's Monitoring
-- page divides by Closed alerts only (escalations excluded), so that variant is also shown as app_fp_rate_of_closed_pct.
-- Compared against the generator's FP-rate PARAMETER to show the simulation behaves as configured.
-- Techniques: CTEs, conditional aggregation, RANK, PERCENT_RANK, CASE tuning recommendation.
WITH exposure AS (
    SELECT SUM(customers_active) AS client_months FROM fact_monthly_snapshot
),
outcomes AS (
    SELECT t.typology_key, t.typology_name, t.model_fp_rate_param,
           COUNT(*) AS alerts,
           SUM(CASE WHEN d.outcome_group <> 'Pending' THEN 1 ELSE 0 END) AS finalised,
           SUM(d.is_closed)         AS closed_alerts,
           SUM(d.is_false_positive) AS false_positives,
           SUM(d.is_escalated)      AS escalated,
           SUM(a.handling_hours)    AS hours
    FROM fact_alert a
    JOIN dim_typology t    ON t.typology_key = a.typology_key
    JOIN dim_disposition d ON d.disposition_key = a.disposition_key
    GROUP BY t.typology_key, t.typology_name, t.model_fp_rate_param
),
rates AS (
    SELECT o.*, ROUND(100.0 * o.alerts / e.client_months, 3) AS alerts_per_100_client_months,
           1.0 * o.false_positives / o.finalised AS fp_rate,
           1.0 * o.escalated / o.finalised       AS escalation_rate
    FROM outcomes o CROSS JOIN exposure e
)
SELECT typology_name, alerts, finalised, false_positives, escalated,
       ROUND(100.0 * false_positives / closed_alerts, 1) AS app_fp_rate_of_closed_pct,
       alerts_per_100_client_months,
       ROUND(100 * fp_rate, 1)               AS fp_rate_pct,
       ROUND(100 * model_fp_rate_param, 1)   AS generator_fp_param_pct,
       ROUND(100 * escalation_rate, 1)       AS escalation_rate_pct,
       ROUND(hours / NULLIF(escalated, 0), 1) AS analyst_hours_per_escalation,
       RANK() OVER (ORDER BY fp_rate DESC)   AS fp_rank_worst_first,
       ROUND(PERCENT_RANK() OVER (ORDER BY alerts), 2) AS volume_percent_rank,
       CASE WHEN fp_rate >= 0.60 AND alerts >= 40 THEN 'Review threshold: high volume, high false positives'
            WHEN fp_rate >= 0.60 THEN 'Watch: high false positives, lower volume'
            WHEN escalation_rate >= 0.25 THEN 'Effective: strong escalation yield'
            ELSE 'Monitor' END AS tuning_note
FROM rates
ORDER BY fp_rank_worst_first;
