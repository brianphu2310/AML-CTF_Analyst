-- SMR timeliness: business days from the alert decision (alert closed) to AUSTRAC submission, by quarter.
-- Benchmark of 3 business days follows the SMR rule described in the README (after suspicion is formed);
-- the simulator's own lag is random, so this demonstrates the analysis, not real firm performance.
-- Techniques: CTEs, NTILE quartiles, PERCENT_RANK, LAG for quarter-on-quarter change, CASE bands.
WITH submitted AS (
    SELECT s.smr_id, d.fy_label, d.fy_quarter, d.fy_start_year,
           s.bdays_alert_close_to_submit AS bdays,
           CASE WHEN s.bdays_alert_close_to_submit <= 3 THEN 1 ELSE 0 END AS on_time
    FROM fact_smr s JOIN dim_date d ON d.date_key = s.submitted_date_key
    WHERE s.submitted_date_key IS NOT NULL
),
ranked AS (
    SELECT *, NTILE(4) OVER (ORDER BY bdays) AS lag_quartile,
              PERCENT_RANK() OVER (ORDER BY bdays) AS lag_pct_rank
    FROM submitted
),
by_quarter AS (
    SELECT fy_label, fy_quarter, fy_start_year,
           COUNT(*) AS smrs_submitted, ROUND(AVG(bdays), 2) AS avg_bdays, MAX(bdays) AS max_bdays,
           SUM(on_time) AS on_time_count,
           ROUND(100.0 * SUM(on_time) / COUNT(*), 1) AS pct_within_3_bdays,
           SUM(CASE WHEN bdays > 5 THEN 1 ELSE 0 END) AS over_5_bdays
    FROM ranked
    GROUP BY fy_label, fy_quarter, fy_start_year
)
SELECT fy_label || ' Q' || fy_quarter AS fiscal_quarter, smrs_submitted, avg_bdays, max_bdays,
       pct_within_3_bdays, over_5_bdays,
       ROUND(pct_within_3_bdays - LAG(pct_within_3_bdays) OVER (ORDER BY fy_start_year, fy_quarter), 1) AS qoq_change_pct_pts,
       SUM(smrs_submitted) OVER (ORDER BY fy_start_year, fy_quarter) AS cumulative_smrs,
       CASE WHEN pct_within_3_bdays >= 80 THEN 'Green' WHEN pct_within_3_bdays >= 60 THEN 'Amber' ELSE 'Red' END AS rag
FROM by_quarter
ORDER BY fy_start_year, fy_quarter;
