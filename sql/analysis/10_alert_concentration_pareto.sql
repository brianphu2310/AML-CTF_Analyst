-- Alert concentration: which clients generate the alerts? Pareto / cumulative-share analysis.
-- Techniques: CTEs, RANK, running SUM over an ordered window, cumulative share, CASE tiering, PERCENT_RANK.
WITH per_client AS (
    SELECT c.customer_id, c.customer_name, t.risk_tier, c.customer_type, COUNT(*) AS alerts,
           SUM(d.is_escalated) AS escalated, SUM(d.is_false_positive) AS false_positives
    FROM fact_alert a
    JOIN dim_customer c  ON c.customer_key = a.customer_key
    JOIN dim_risk_tier t ON t.risk_tier_key = c.risk_tier_key
    JOIN dim_disposition d ON d.disposition_key = a.disposition_key
    GROUP BY c.customer_id, c.customer_name, t.risk_tier, c.customer_type
),
ordered AS (
    SELECT p.*, RANK() OVER (ORDER BY alerts DESC) AS alert_rank,
           ROW_NUMBER() OVER (ORDER BY alerts DESC, customer_id) AS rn,
           SUM(alerts) OVER (ORDER BY alerts DESC, customer_id ROWS UNBOUNDED PRECEDING) AS running_alerts,
           SUM(alerts) OVER () AS total_alerts,
           COUNT(*) OVER () AS clients_with_alerts,
           PERCENT_RANK() OVER (ORDER BY alerts) AS alerts_percent_rank
    FROM per_client p
)
SELECT rn AS position, customer_id, customer_name, risk_tier, customer_type, alerts, escalated, false_positives,
       alert_rank, running_alerts,
       ROUND(100.0 * running_alerts / total_alerts, 1)  AS cumulative_pct_of_alerts,
       ROUND(100.0 * rn / clients_with_alerts, 1)       AS cumulative_pct_of_clients,
       CASE WHEN 1.0 * running_alerts / total_alerts <= 0.5 THEN 'Top half of alerts'
            WHEN 1.0 * running_alerts / total_alerts <= 0.8 THEN 'Next 30%' ELSE 'Long tail' END AS pareto_band
FROM ordered
WHERE rn <= 25
ORDER BY rn;
