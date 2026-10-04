-- Repeat structuring alerts: clients whose structuring alerts recur within 90 days (a typical escalation trigger).
-- Techniques: CTEs, LAG over a PARTITION to get the gap to the previous alert, JULIANDAY date arithmetic,
-- ROW_NUMBER, window COUNT, RANK.
WITH struct AS (
    SELECT a.alert_id, a.customer_key, d.full_date AS opened_date, dp.disposition
    FROM fact_alert a
    JOIN dim_typology t     ON t.typology_key = a.typology_key AND t.typology_name = 'Structuring / smurfing'
    JOIN dim_date d         ON d.date_key = a.opened_date_key
    JOIN dim_disposition dp ON dp.disposition_key = a.disposition_key
),
gapped AS (
    SELECT s.*,
           ROW_NUMBER() OVER (PARTITION BY customer_key ORDER BY opened_date, alert_id) AS seq,
           COUNT(*)     OVER (PARTITION BY customer_key)                                AS client_total,
           CAST(JULIANDAY(opened_date) - JULIANDAY(LAG(opened_date) OVER (PARTITION BY customer_key ORDER BY opened_date, alert_id)) AS INTEGER) AS days_since_prev
    FROM struct s
),
repeaters AS (
    SELECT customer_key, COUNT(*) AS structuring_alerts, MIN(opened_date) AS first_alert, MAX(opened_date) AS last_alert,
           SUM(CASE WHEN days_since_prev <= 90 THEN 1 ELSE 0 END) AS repeats_within_90d,
           MIN(days_since_prev) AS shortest_gap_days
    FROM gapped
    WHERE client_total >= 2
    GROUP BY customer_key
)
SELECT c.customer_id, c.customer_name, c.customer_type, t.risk_tier, b.branch_name,
       r.structuring_alerts, r.repeats_within_90d, r.shortest_gap_days, r.first_alert, r.last_alert,
       RANK() OVER (ORDER BY r.repeats_within_90d DESC, r.structuring_alerts DESC) AS priority_rank
FROM repeaters r
JOIN dim_customer c  ON c.customer_key = r.customer_key
JOIN dim_risk_tier t ON t.risk_tier_key = c.risk_tier_key
JOIN dim_branch b    ON b.branch_key = c.branch_key
ORDER BY priority_rank, c.customer_id;
