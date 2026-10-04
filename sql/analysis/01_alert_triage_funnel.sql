-- Alert triage funnel by typology: how many alerts survive each stage from monitoring hit to AUSTRAC acknowledgement.
-- Stages: opened -> dispositioned (closed/escalated) -> escalated to SMR -> SMR submitted -> SMR acknowledged.
-- Techniques: CTEs, conditional aggregation, window SUM() OVER () for share-of-total, RANK().
WITH alert_stage AS (
    SELECT a.alert_key, t.typology_name,
           1                                                     AS opened,
           CASE WHEN a.closed_date_key IS NOT NULL THEN 1 ELSE 0 END AS dispositioned,
           d.is_escalated                                        AS escalated,
           CASE WHEN s.submitted_date_key IS NOT NULL THEN 1 ELSE 0 END AS smr_submitted,
           CASE WHEN s.acknowledged_date_key IS NOT NULL THEN 1 ELSE 0 END AS smr_acknowledged
    FROM fact_alert a
    JOIN dim_typology t     ON t.typology_key = a.typology_key
    JOIN dim_disposition d  ON d.disposition_key = a.disposition_key
    LEFT JOIN fact_smr s    ON s.alert_key = a.alert_key
),
funnel AS (
    SELECT typology_name,
           SUM(opened) AS opened, SUM(dispositioned) AS dispositioned, SUM(escalated) AS escalated,
           SUM(smr_submitted) AS smr_submitted, SUM(smr_acknowledged) AS smr_acknowledged
    FROM alert_stage
    GROUP BY typology_name
)
SELECT typology_name, opened, dispositioned, escalated, smr_submitted, smr_acknowledged,
       ROUND(100.0 * dispositioned / opened, 1)                      AS pct_dispositioned,
       ROUND(100.0 * escalated / NULLIF(dispositioned, 0), 1)        AS pct_of_dispositioned_escalated,
       ROUND(100.0 * smr_acknowledged / NULLIF(escalated, 0), 1)     AS pct_escalated_acknowledged,
       ROUND(100.0 * opened / SUM(opened) OVER (), 1)                AS pct_of_all_alerts,
       RANK() OVER (ORDER BY opened DESC)                            AS volume_rank
FROM funnel
ORDER BY volume_rank;
