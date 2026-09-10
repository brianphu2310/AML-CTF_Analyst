# AML Compliance Suite

A multi-page Streamlit application for AML/CTF compliance workflows: customer
risk rating, watchlist screening, transaction monitoring, case management,
UBO network mapping, and business KYC — plus one-click drafting of an
AUSTRAC-aligned Suspicious Matter Report (SMR).

## Pages

| Page | Purpose |
|---|---|
| `Home.py` | Portfolio-level KPIs and trend charts |
| `pages/1_Customer_Risk.py` | Risk-based customer register, filterable by industry/country/risk/status |
| `pages/2_Screening.py` | PEP, Sanctions and Adverse Media hit queue with disposition status |
| `pages/3_Transaction_Monitoring.py` | Automated detection: structuring, rapid movement, high-risk wires, plus per-customer drill-down |
| `pages/4_Case_Management_SAR.py` | Investigation queue + automated AUSTRAC-format SMR narrative generator (.txt / .docx export) |
| `pages/5_UBO_Network.py` | Interactive beneficial-ownership graph with PEP exposure flags |
| `pages/6_Business_KYC.py` | Corporate KYC register and EDD refresh tracking |
| `pages/7_New_Client_Onboarding.py` | Guided step-by-step CDD workflow to onboard a new client, with automated screening, risk scoring and CDD record generation |

## Quick start (demo mode — no database needed)

```bash
pip install -r requirements.txt
streamlit run Home.py
```

The app ships with `USE_DEMO_DATA = True` in `db_utils.py`, which generates a
realistic, internally-consistent synthetic dataset (customers, transactions,
screening hits, cases, businesses, UBOs) on first load — including injected
structuring, rapid-movement and high-risk-wire patterns so the detection
logic and SMR generator have real findings to work with.

## Connecting to a live database

1. Open `db_utils.py`.
2. Set `USE_DEMO_DATA = False`.
3. Fill in `DB_CONFIG` with your Postgres host/port/dbname/user/password.
4. Ensure the following tables exist with (at minimum) these columns:
   - `customers(customer_id, name, customer_type, occupation, industry, country, risk_score, risk_level, status, onboarding_date)`
   - `transactions(txn_id, customer_id, txn_date, amount, direction, channel, counterparty_country, description)`
   - `screening_hits(screening_id, customer_id, match_type, match_detail, list_source, match_score, status, screened_date)`
   - `cases(case_id, customer_id, opened_date, priority, status, assigned_analyst, typology)`
   - `businesses(business_id, legal_name, abn, industry, incorporation_country, incorporation_date, structure_type, risk_rating, risk_score)`
   - `ubo(ubo_id, business_id, owner_name, owner_type, ownership_pct, is_pep, nationality)`

No other code changes are required — every page reads exclusively through
`db_utils.load_all()`.

## About the SMR generator (`report_utils.py`)

`build_smr()` runs three detectors over a customer's transaction history:

- **Structuring / smurfing** — clusters of cash deposits just under the
  $10,000 threshold within a short window.
- **Rapid movement of funds** — a large inbound credit substantially
  depleted by outbound transfers within days.
- **High-risk corridor wires** — repeated international wires to/from
  jurisdictions flagged as higher risk.

Findings are woven into a Grounds-for-Suspicion narrative structured under
AUSTRAC's recommended **Who / What / When / Where / How / Why** headings, in
standard case (not ALL CAPS), alongside Part A (reporting entity), Part C
(suspicious person/entity) and a transaction summary — plus the statutory 3
business day / 24 hour (terrorism financing) lodgement reminder and an
officer-certification block.

**This output is a drafting aid, not a lodgement-ready report.** Every
generated SMR carries an explicit warning that a qualified compliance
officer / MLRO must review, complete the bracketed fields, and approve the
narrative before submission via AUSTRAC Online.

## About the onboarding workflow (`onboarding_utils.py`)

`pages/7_New_Client_Onboarding.py` is a 5-step wizard (Customer Type →
Identity → Ownership & Control → Relationship & Activity → Review & Run
Checks) that asks the standard questions an AML/CTF Program requires at
onboarding: identity details, beneficial ownership (25%+ owners, directors,
trustees for business customers), purpose of the relationship, source of
funds/wealth, and expected transaction profile (volume, channels,
counterparty countries).

On "Run Onboarding Compliance Checks" it automatically:

1. **Screens** the customer name for PEP / Sanctions / Adverse Media
   matches (`run_screening()` - a deterministic stand-in for a real
   watchlist provider such as Dow Jones or World-Check).
2. **Scores risk** with a transparent, weighted rule engine
   (`score_onboarding()`) covering customer type, structure, beneficial
   ownership, geography, industry, delivery channel, source of funds,
   expected activity and any screening hits - and shows the exact factor
   breakdown, not just a black-box number.
3. **Determines the CDD tier** (Simplified / Standard / Enhanced +
   senior sign-off) and a plain-language onboarding decision, including an
   automatic "do not onboard, refer to MLRO" stop on any sanctions match.
4. **Generates a Customer Due Diligence (CDD) record** (.txt / .docx) that
   documents everything captured plus the risk assessment and decision,
   ready for the compliance file.

As with the SMR generator, this is a drafting and decisioning aid - any
Critical/High risk rating or screening hit is flagged for MLRO review
before the account is actually activated.

## Theming

`theme.py` centralises the dark, teal-accented visual style (KPI cards, risk
pills, section headers) via `.streamlit/config.toml` and a shared CSS
injector — import `inject_css()` and `page_header()` at the top of any new
page to stay consistent.
