-- Periodic CDD review backlog as at the as-of date: overdue clients by risk tier and branch, with ageing bands.
-- Techniques: CTE with scalar subquery for as-of date, JULIANDAY, CASE ageing buckets, NTILE, running total, RANK.
WITH asof AS (
    SELECT meta_value AS as_of FROM etl_meta WHERE meta_key = 'as_of_date'
),
overdue AS (
    SELECT c.customer_id, c.customer_name, t.risk_tier, t.tier_rank, b.branch_name, d.full_date AS review_due,
           CAST(JULIANDAY(a.as_of) - JULIANDAY(d.full_date) AS INTEGER) AS days_overdue
    FROM dim_customer c
    JOIN dim_risk_tier t ON t.risk_tier_key = c.risk_tier_key
    JOIN dim_branch b    ON b.branch_key = c.branch_key
    JOIN dim_date d      ON d.date_key = c.next_review_due_date_key
    CROSS JOIN asof a
    WHERE c.review_overdue_flag = 1
),
bucketed AS (
    SELECT o.*,
           CASE WHEN days_overdue <= 30 THEN '0-30 days' WHEN days_overdue <= 90 THEN '31-90 days'
                WHEN days_overdue <= 180 THEN '91-180 days' ELSE '180+ days' END AS ageing_bucket,
           NTILE(4) OVER (ORDER BY days_overdue DESC) AS severity_quartile
    FROM overdue o
)
SELECT risk_tier, branch_name, ageing_bucket, COUNT(*) AS overdue_clients,
       MAX(days_overdue) AS max_days_overdue, ROUND(AVG(days_overdue), 1) AS avg_days_overdue,
       SUM(COUNT(*)) OVER (ORDER BY tier_rank DESC, branch_name, ageing_bucket) AS running_total,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS size_rank
FROM bucketed
GROUP BY risk_tier, tier_rank, branch_name, ageing_bucket
ORDER BY tier_rank DESC, branch_name, ageing_bucket;
