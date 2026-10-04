-- Structuring / smurfing (threshold-avoidance) alert trend by month.
-- NOTE: the simulated dataset has alert-level data only (no transaction ledger), so this analyses the monitoring
-- rule's alert pattern, not the underlying cash deposits.
-- Techniques: CTEs, date dimension join, LAG (MoM), 3-month moving average via ROWS frame, running total, YTD by FY.
WITH monthly AS (
    SELECT d.month_start_date AS month_start,
           COUNT(*) AS structuring_alerts,
           SUM(dp.is_false_positive) AS false_positives,
           SUM(dp.is_escalated)      AS escalated
    FROM fact_alert a
    JOIN dim_typology t     ON t.typology_key = a.typology_key AND t.typology_name = 'Structuring / smurfing'
    JOIN dim_date d         ON d.date_key = a.opened_date_key
    JOIN dim_disposition dp ON dp.disposition_key = a.disposition_key
    GROUP BY d.month_start_date
),
with_clients AS (   -- month spine from the snapshot fact so months with zero alerts still appear (keeps LAG/moving averages honest)
    SELECT sd.full_date AS month_start, sd.fy_label, s.customers_active,
           COALESCE(m.structuring_alerts, 0) AS structuring_alerts,
           COALESCE(m.false_positives, 0)    AS false_positives,
           COALESCE(m.escalated, 0)          AS escalated
    FROM fact_monthly_snapshot s
    JOIN dim_date sd ON sd.date_key = s.month_start_date_key
    LEFT JOIN monthly m ON m.month_start = sd.full_date
)
SELECT month_start, fy_label, structuring_alerts, false_positives, escalated, customers_active,
       ROUND(100.0 * structuring_alerts / customers_active, 2)                     AS alerts_per_100_clients,
       structuring_alerts - LAG(structuring_alerts) OVER (ORDER BY month_start)    AS mom_change,
       ROUND(AVG(structuring_alerts) OVER (ORDER BY month_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m,
       SUM(structuring_alerts) OVER (ORDER BY month_start)                         AS running_total,
       SUM(structuring_alerts) OVER (PARTITION BY fy_label ORDER BY month_start)   AS fy_ytd
FROM with_clients
ORDER BY month_start;
