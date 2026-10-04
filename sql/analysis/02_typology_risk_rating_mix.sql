-- Typology x customer risk-tier mix: is alert volume concentrated where the risk model says it should be?
-- Compares each tier's share of clients with its share of alerts (an "alert intensity index" of 1.0 = proportional).
-- Techniques: CTEs, CROSS JOIN, window SUM() OVER (PARTITION BY), RANK() within typology.
WITH tier_clients AS (
    SELECT t.risk_tier, t.tier_rank, COUNT(*) AS clients,
           1.0 * COUNT(*) / SUM(COUNT(*)) OVER () AS client_share
    FROM dim_customer c JOIN dim_risk_tier t ON t.risk_tier_key = c.risk_tier_key
    GROUP BY t.risk_tier, t.tier_rank
),
alert_mix AS (
    SELECT ty.typology_name, t.risk_tier, COUNT(*) AS alerts
    FROM fact_alert a
    JOIN dim_typology ty ON ty.typology_key = a.typology_key
    JOIN dim_customer c  ON c.customer_key = a.customer_key
    JOIN dim_risk_tier t ON t.risk_tier_key = c.risk_tier_key
    GROUP BY ty.typology_name, t.risk_tier
),
shares AS (
    SELECT m.typology_name, m.risk_tier, m.alerts,
           1.0 * m.alerts / SUM(m.alerts) OVER (PARTITION BY m.typology_name) AS share_within_typology,
           SUM(m.alerts) OVER (PARTITION BY m.risk_tier)                      AS tier_alerts_all_typologies
    FROM alert_mix m
)
SELECT s.typology_name, s.risk_tier, tc.clients AS clients_in_tier, s.alerts,
       ROUND(100 * s.share_within_typology, 1)                   AS pct_of_typology_alerts,
       ROUND(100 * tc.client_share, 1)                           AS pct_of_clients,
       ROUND(s.share_within_typology / tc.client_share, 2)       AS alert_intensity_index,
       RANK() OVER (PARTITION BY s.typology_name ORDER BY s.alerts DESC) AS tier_rank_in_typology,
       CASE WHEN s.share_within_typology / tc.client_share >= 1.5 THEN 'Over-represented'
            WHEN s.share_within_typology / tc.client_share <= 0.67 THEN 'Under-represented'
            ELSE 'Proportional' END                               AS representation
FROM shares s JOIN tier_clients tc ON tc.risk_tier = s.risk_tier
ORDER BY s.typology_name, tc.tier_rank;
