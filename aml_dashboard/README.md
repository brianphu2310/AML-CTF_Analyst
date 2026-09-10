# AML/KYC Transaction Monitoring Intelligence Dashboard

Multi-page Streamlit app for the AML/KYC pipeline portfolio project.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Edit `db_utils.py` and update `DB_CONFIG` with your local Postgres
   credentials (host, port, dbname, user, password). The database should
   already contain the `customers`, `businesses`, `ownership`,
   `screening_results`, and `transactions` tables from the earlier
   pipeline steps.

3. Run the app from this folder:
   ```bash
   streamlit run Home.py
   ```

   Streamlit will auto-discover the pages in the `pages/` folder and list
   them in the sidebar in this order:
   - Customer Risk
   - Screening
   - Transaction Monitoring
   - Case Management & SAR

## Folder structure

```
aml_dashboard/
├── Home.py                          # overview / landing page
├── db_utils.py                      # shared DB connection + queries
├── report_utils.py                  # SAR narrative generation logic
├── requirements.txt
└── pages/
    ├── 1_Customer_Risk.py
    ├── 2_Screening.py
    ├── 3_Transaction_Monitoring.py
    └── 4_Case_Management_SAR.py
```

## Case Management & SAR page

Select any customer from the flagged case queue (filterable by minimum
composite risk score) and click **Generate SAR Narrative** to produce a
formatted Suspicious Activity Report narrative — auto-populated from
that customer's profile, screening results, and transaction history
(structuring clusters, rapid movement pairs, high-risk country wires).
Download the result as `.txt` or `.docx`.
