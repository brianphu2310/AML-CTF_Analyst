-- Ageing of the open alert queue (open + under investigation) as at the as-of date, against the SLA.
-- Techniques: CTEs, scalar as-of lookup, JULIANDAY, CASE buckets, window COUNT/SUM, ROW_NUMBER for oldest-first.
WITH asof AS (
    SELECT meta_value AS as_of, CAST(
        (SELECT meta_value FROM etl_meta WHERE meta_key = 'sla_days') AS INTEGER) AS sla_days
    FROM etl_meta WHERE meta_key = 'as_of_date'
),
queue AS (
    SELECT a.alert_id, t.typology_name, c.customer_name, rt.risk_tier, n.analyst_name, dp.disposition,
           d.full_date AS opened_date,
           CAST(JULIANDAY(x.as_of) - JULIANDAY(d.full_date) AS INTEGER) AS age_days, x.sla_days
    FROM fact_alert a
    JOIN dim_disposition dp ON dp.disposition_key = a.disposition_key AND dp.outcome_group = 'Pending'
    JOIN dim_typology t  ON t.typology_key = a.typology_key
    JOIN dim_customer c  ON c.customer_key = a.customer_key
    JOIN dim_risk_tier rt ON rt.risk_tier_key = c.risk_tier_key
    JOIN dim_analyst n   ON n.analyst_key = a.analyst_key
    JOIN dim_date d      ON d.date_key = a.opened_date_key
    CROSS JOIN asof x
)
SELECT ROW_NUMBER() OVER (ORDER BY age_days DESC, alert_id) AS oldest_first,
       alert_id, typology_name, customer_name, risk_tier, analyst_name, disposition, opened_date, age_days,
       CASE WHEN age_days > sla_days THEN 'Past SLA' WHEN age_days >= sla_days - 3 THEN 'Due soon' ELSE 'Within SLA' END AS sla_status,
       CASE WHEN age_days <= 3 THEN '0-3 days' WHEN age_days <= 7 THEN '4-7 days' WHEN age_days <= 14 THEN '8-14 days' ELSE '15+ days' END AS age_bucket,
       COUNT(*) OVER (PARTITION BY analyst_name) AS analyst_open_count
FROM queue
ORDER BY oldest_first;
