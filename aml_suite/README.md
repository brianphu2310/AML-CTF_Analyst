# AML/CTF Compliance Suite — Meridian Legal Partners (demo)

A portfolio project simulating the AML/CTF compliance function of an
Australian law firm newly regulated under the **Tranche 2 reforms**
(AML/CTF Act 2006 (Cth), obligations effective 1 July 2026). Built to
demonstrate AML/KYC analyst and compliance officer skills: risk-based
customer due diligence, transaction typology detection, alert triage,
and financial analysis of trust account activity.

## Why this project

Tranche 2 extends AUSTRAC's AML/CTF regime to legal practitioners for the
first time, specifically for **designated services** — managing client
money in a transaction, company/trust formation, nominee director or
shareholder arrangements. This project models that exact scope: a firm's
trust account, its designated-service matters, and the compliance program
now legally required around them.

## What's implemented, and why

See `docs/01_business_design.md` for the full methodology write-up (read
this first if you're reviewing the project — it explains *why* each rule
exists, not just what the code does).

- **Customer risk rating** (`lib/risk_engine.py`) — AUSTRAC's four-factor
  model (customer type, jurisdiction, service/product, delivery channel).
  A single high-risk factor overrides to an overall High rating, per
  AUSTRAC's own worked guidance — the model does not average a bad factor
  away with good ones.
- **Transaction typology detection** — five named typologies (structuring,
  rapid movement of funds, third-party funding mismatch, unexplained
  source-of-funds jump, high-risk jurisdiction nexus), each producing a
  plain-language reason, not just a severity number.
- **Alert triage & case management** — mirrors a real analyst queue:
  alert → triage decision → case → SMR filing decision, with the AML/CTF
  Act's tipping-off prohibition respected in the workflow design.
- **Financial analysis** — matter-level trust ledger reconciliation
  (cash-flow reconstruction, sense checks against declared income) and
  portfolio-level reporting (funds under management, concentration,
  monthly trends) — the financial-analyst layer alongside the compliance
  workflow.

## Data

All data is synthetic (`lib/data_gen.py`, seeded for reproducibility).
About 7% of customers are seeded with a hidden typology pattern; the
detection logic is not told which customers these are — it has to find
them from transaction behaviour alone, the same constraint a real system
faces. On this dataset, detection recovers roughly 90% of the seeded
pattern at a customer-level false-positive rate around 45% — worse
sounding than it is: published industry AML alerting benchmarks are
routinely 90%+ false positive, so this is a deliberately tuned
improvement, not an accident. The tuning story (why a naive ">$10,000"
rule was rejected, what generated an unrealistic 40%+ "High risk"
population on the first pass, how thresholds were adjusted) is worth
walking through in an interview — it's the strongest evidence of
judgment, not just implementation.

## Running it

```bash
pip install -r requirements.txt
python lib/data_gen.py     # regenerate synthetic data (optional, already included)
streamlit run Home.py
```

## Structure

```
Home.py                          Executive overview
pages/
  1_Customer_Risk_Rating.py      Risk model + per-customer rationale
  2_Transaction_Monitoring.py    Typology detection
  3_Alert_Triage_and_Cases.py    Alert queue, case investigation, SMR decision
  4_Financial_Analysis.py        Trust ledger reconciliation + portfolio KPIs
lib/
  data_gen.py                    Synthetic data generator
  risk_engine.py                 Risk rating + typology detection logic
  theme.py                       Shared UI/chart styling
  data_access.py                 Cached data loading
data/
  customers.csv, transactions.csv
docs/
  01_business_design.md          Full methodology write-up
```

## Scope and limitations (stated deliberately, not hidden)

This models the *analytical and case-management* layer of an AML/CTF
program. It does not implement: AUSTRAC enrolment/reporting integration,
document verification for KYC, a full governance layer (AML/CTF
Compliance Officer sign-off workflows, training registers, independent
review), or real customer PII handling controls. These are named
explicitly here because overclaiming scope is a bigger risk in an
interview than stating a boundary clearly.
