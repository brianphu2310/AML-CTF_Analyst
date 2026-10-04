-- Analyst workload and SLA performance with rankings and quarterly running hours.
-- Techniques: CTEs, window SUM running totals partitioned by analyst, RANK, PERCENT_RANK, NTILE, CASE.
WITH per_analyst AS (
    SELECT n.analyst_key, n.analyst_name, n.role, b.branch_name AS home_branch, n.monthly_capacity,
           COUNT(*) AS alerts, ROUND(SUM(a.handling_hours), 1) AS hours,
           SUM(CASE WHEN a.closed_date_key IS NOT NULL THEN 1 ELSE 0 END) AS closed_alerts,
           SUM(CASE WHEN a.closed_date_key IS NOT NULL AND a.sla_breach_flag = 1 THEN 1 ELSE 0 END) AS sla_breaches,
           ROUND(AVG(a.days_to_close), 2) AS avg_days_to_close,
           SUM(d.is_escalated) AS escalated
    FROM fact_alert a
    JOIN dim_analyst n ON n.analyst_key = a.analyst_key
    JOIN dim_branch b  ON b.branch_key = n.home_branch_key
    JOIN dim_disposition d ON d.disposition_key = a.disposition_key
    GROUP BY n.analyst_key, n.analyst_name, n.role, b.branch_name, n.monthly_capacity
)
SELECT analyst_name, role, home_branch, monthly_capacity, alerts, hours, closed_alerts, sla_breaches,
       ROUND(100.0 * sla_breaches / NULLIF(closed_alerts, 0), 1)  AS sla_breach_pct,
       avg_days_to_close,
       ROUND(100.0 * escalated / alerts, 1)                       AS escalation_pct,
       RANK() OVER (ORDER BY hours DESC)                          AS workload_rank,
       RANK() OVER (ORDER BY 1.0 * sla_breaches / NULLIF(closed_alerts, 0) DESC) AS sla_breach_rank_worst_first,
       ROUND(PERCENT_RANK() OVER (ORDER BY avg_days_to_close), 2) AS speed_percent_rank,
       NTILE(3) OVER (ORDER BY monthly_capacity DESC)             AS capacity_band,
       ROUND(100.0 * hours / SUM(hours) OVER (), 1)               AS pct_of_team_hours,
       CASE WHEN 1.0 * sla_breaches / NULLIF(closed_alerts, 0) > 0.30 THEN 'Coach / rebalance' ELSE 'On track' END AS flag
FROM per_analyst
ORDER BY workload_rank;
