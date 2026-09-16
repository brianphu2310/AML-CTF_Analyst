# AML Compliance Suite

An end-to-end, multi-page **AML/KYC & Transaction Monitoring** workspace built with Streamlit — covering the full customer lifecycle from onboarding and screening through transaction monitoring, alert triage, case investigation, AUSTRAC-aligned SMR drafting, UBO network mapping, periodic review, and audit trail record-keeping.

Built as a portfolio project to demonstrate practical AML/KYC and data analyst skills: designing a compliance data model, implementing rule-based typology detection, and turning raw transaction data into decision-ready dashboards and reports.

> **Demo data notice:** everything in this app — customers, transactions, screening hits, cases — is synthetic data generated on the fly. No real customer, transaction or regulatory data is used anywhere in this project.

<!-- 
  Add a screenshot or GIF walkthrough here once you have one, e.g.:
  ![Dashboard overview](docs/screenshot-home.png)
-->

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Data Modes: Demo vs. Live Database](#data-modes-demo-vs-live-database)
- [How to Use the App](#how-to-use-the-app)
- [AML/CTF Concepts Explained](#amlctf-concepts-explained)
- [Technical Reference: Every Function, Module by Module](#technical-reference-every-function-module-by-module)
- [Disclaimer](#disclaimer)
- [Roadmap](#roadmap)
- [Author](#author)

## Overview

The suite models the AML/CTF program lifecycle a compliance team runs day to day:

**Onboarding → Ongoing Monitoring → Alert Triage → Investigation → Escalation → SMR Reporting → Periodic Review → Record Keeping**

Every stage is a working page backed by the same synthetic dataset, not a static mockup — filters, drill-downs, dispositions and case actions are all live and write back to session state, with every action logged to a real audit trail.

## Features

| Page | What it does |
|---|---|
| **Home** | Portfolio-level KPI overview: risk distribution, transaction volume trend, case load by analyst, customer lifecycle waterfall, and compliance health targets. |
| **Customer Risk** | Risk-based customer register with score distribution by risk level, filterable by industry, country, risk level and status. |
| **Screening** | PEP, sanctions and adverse media match queue with disposition workflow (Open → Under Review → Escalated → Cleared). |
| **Transaction Monitoring** | Rule-based typology detection across the full ledger: structuring/smurfing, rapid movement of funds, and high-risk corridor wires, plus a per-customer transaction drill-down. |
| **Case Management & SMR** | Case investigation workspace with an **auto-drafted, AUSTRAC-aligned Suspicious Matter Report** (Who/What/When/Where/How/Why grounds-for-suspicion narrative), exportable to `.docx`. |
| **UBO Network** | Beneficial ownership structure mapping with PEP exposure flags across corporate customers. |
| **Business KYC** | Corporate due diligence register: structure type, incorporation country, EDD refresh tracking. |
| **New Client Onboarding** | CDD/EDD intake workflow and onboarding decisioning. |
| **Alerts & Triage** | Unified queue combining watchlist-screening hits and transaction-monitoring detections, with analyst disposition and one-click case escalation. |
| **Periodic Review** | Risk-based re-verification scheduling (Low 24mo / Medium 12mo / High 6mo / Critical 3mo) with a remediation checklist workflow. |
| **Audit Trail** | Consolidated, filterable record-keeping log of every decision, escalation and lodgement across the suite, with CSV export. |
| **Process Map** | A clickable map of the full AML/CTF lifecycle this suite implements, linking each stage to its working page. |

Charts throughout the suite use a shared, harmonized teal / cream / brown / white visual theme with unified hover, interactive legends, and smooth transitions.

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — multi-page app framework
- **[pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/)** — data modeling and the synthetic data generator
- **[Plotly](https://plotly.com/python/)** — interactive charts (bar, grouped bar, area/trend, waterfall, gauge, scatter, network)
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — optional live-database layer (PostgreSQL)
- **[python-docx](https://python-docx.readthedocs.io/)** — automated SMR report generation as a formatted Word document

## Project Structure

```
├── Home.py                        # Portfolio-level dashboard (entry point)
├── pages/
│   ├── 1_Customer_Risk.py
│   ├── 2_Screening.py
│   ├── 3_Transaction_Monitoring.py
│   ├── 4_Case_Management_SAR.py
│   ├── 5_UBO_Network.py
│   ├── 6_Business_KYC.py
│   ├── 7_New_Client_Onboarding.py
│   ├── 8_Alerts_Triage.py
│   ├── 9_Periodic_Review.py
│   ├── 10_Audit_Trail.py
│   └── 11_Process_Map.py
├── theme.py                        # Shared visual theme + chart engine
├── db_utils.py                     # Data access layer (demo data generator / live DB switch)
├── report_utils.py                 # Typology detection + AUSTRAC SMR narrative builder
├── workflow_utils.py                # Session-state workflow engine + audit logging
└── onboarding_utils.py             # Onboarding/CDD workflow helpers
```

## Getting Started

**Requirements:** Python 3.10+

```bash
# 1. Clone the repository
git clone https://github.com/brianphu2310/<repo-name>.git
cd <repo-name>

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install streamlit pandas numpy plotly sqlalchemy python-docx

# 4. Run the app
streamlit run Home.py
```

The app opens at `http://localhost:8501`. No database setup is required — it runs entirely on generated demo data out of the box.

## Data Modes: Demo vs. Live Database

`db_utils.py` is the single data-access layer every page imports from, so switching modes only means editing one file:

- **Demo mode (default):** `USE_DEMO_DATA = True` — generates a realistic, internally consistent synthetic dataset (customers, transactions, screening hits, cases, businesses, UBOs) on the fly, cached per session.
- **Live mode:** set `USE_DEMO_DATA = False` and fill in `DB_CONFIG` to point at a PostgreSQL warehouse with matching `customers`, `transactions`, `screening_hits`, `cases`, `businesses` and `ubo` tables.

## How to Use the App

### Running the App

```bash
pip install streamlit pandas numpy plotly sqlalchemy python-docx
streamlit run Home.py
```

This opens the app in your browser at `http://localhost:8501`. The left sidebar (visible on most pages) holds filters; the main panel holds KPIs, charts, and data tables. Every page loads the same underlying demo dataset, so a customer you see flagged on one page will show up consistently everywhere else.

**One thing to know before you start:** actions you take (triaging an alert, escalating a case, completing a review) are saved for your current session only — they live in Streamlit's `session_state`, not a database. Refreshing the page resets to the original demo data.

### Page-by-Page Guide

### Home
Your starting point. Five KPI cards across the top (total customers, high/critical risk count, open screening alerts, active cases, pending SMR lodgements) give you the state of the whole book at a glance. Below that:
- **Portfolio Risk Distribution** — toggle between "Avg Risk Score" and "Customer Count" to see the industry breakdown either way.
- **Transaction Volume Trend** — switch the time window (30D/90D/180D/1Y) to zoom the trend chart.
- **Customer Lifecycle Waterfall** — shows how the book narrows from "Total Customers" down through screening, cases, escalation, SMR lodgement and closure.
- **Compliance Health Targets** — three gauges against target thresholds.
- **Case Load by Analyst** — sort by count or by name to see workload distribution.

Use this page to decide *where* to dig in next, then head to the relevant page below.

### Customer Risk
The full customer register. Use the sidebar to filter by industry, country, risk level, status, or search by name/ID. The **Risk Score Distribution** chart bins customers into 10-point score ranges, colored by risk level — useful for spotting where your book actually clusters. Click **Download filtered list (CSV)** to export whatever you've filtered to.

### Screening
The PEP/Sanctions/Adverse Media match queue. Filter by match type, status, or a minimum match score. Each row shows the list source (e.g. DFAT Consolidated List, World-Check), the match score, and the current disposition status. This page is read-only for browsing — dispositioning happens through the **Alerts & Triage** page, which pulls the same underlying screening hits into its unified queue.

### Transaction Monitoring
Four tabs, each running one of the automated typology detectors live against the full transaction ledger:
1. **Structuring** — customers with clustered sub-threshold cash deposits.
2. **Rapid Movement** — customers where a large inbound credit was drained shortly after.
3. **High-Risk Wires** — customers with wire activity in high-risk corridors, plus a volume-by-country chart.
4. **Customer Drill-down** — pick any customer from the dropdown to see their full transaction scatter plot and table, colored by direction.

If a tab shows "No patterns detected," that typology simply didn't trigger for the current filtered dataset — try a different customer or check the other tabs.

### Alerts & Triage
The single queue where analyst action actually happens for alerts. Steps:
1. Filter by source, severity, or disposition in the sidebar if the queue is long.
2. Scroll to **Triage an Alert**, pick one from the dropdown.
3. Read the customer/source/type/severity/detail on the left, optionally add an analyst note.
4. Pick a new disposition on the right: **False Positive**, **Requires Investigation**, or **Escalated to Case**.
5. Click **Apply Disposition**. If you escalate, a new case is automatically created and you'll see a success message with the new case ID — head to **Case Management & SMR** to continue working it.

### Case Management & SMR
Four tabs covering the full investigation lifecycle:
1. **Investigation Queue** — browse/filter all cases by priority, status, analyst, or minimum customer risk score.
2. **Investigation Workspace** — select a case to see the customer's full profile, prior alerts, screening hits and transaction history side by side. Write source-of-funds/source-of-wealth review notes and save them, or escalate the case to senior review directly from here.
3. **Escalation & Senior Review** — select an escalated case, record the senior decision (Close Case / Continue Monitoring / Restrict-Exit Relationship), and sign off. "Continue Monitoring" moves the case to `Pending SMR Lodgement`.
4. **SMR Assessment, Drafting & Submission** — select a case eligible for SMR work, tick the "reasonable grounds" checkbox, click **Generate SMR Narrative**. Review the auto-drafted WHO/WHAT/WHEN/WHERE/HOW/WHY narrative in the editable text box, download it as `.txt` or `.docx`, then mark it as lodged with an AUSTRAC reference number once ready.

### UBO Network
Pick a business from the dropdown to see its ownership structure. The center node is the reporting entity; surrounding nodes are its beneficial owners, sized by ownership percentage and colored by type (individual/corporate/PEP). A PEP-linked owner triggers a red warning banner below the graph flagging that EDD and senior sign-off are required.

### Business KYC
The corporate due diligence register. Filter by incorporation country, structure type, or risk rating. Select any entity at the bottom to see its full profile and beneficial owner table side by side — this page and UBO Network cover the same entities from two different angles (register view vs. ownership graph view).

### New Client Onboarding
A guided intake form that runs the same risk-scoring engine a real onboarding decision would use. Fill in customer type, geography, industry, purpose of the relationship, source of funds, expected activity, and (for business customers) beneficial owners. Submitting runs simulated watchlist screening and the CDD scoring model, then shows you the resulting risk rating, required CDD tier, and onboarding decision — download the full CDD record as text or `.docx`.

### Periodic Review
On **Periodic Review**, the register shows every active customer's review due date (Overdue / Due within 30 days / Scheduled), computed from their risk level. Filter down to the customers you want, select one at the bottom, tick off the remediation checklist items completed, record the outcome, and click **Mark Review Complete**.

### Audit Trail
The consolidated log of everything, everywhere, all session. Filter by entity type, actor, date range, or free-text search. Export the filtered view as CSV. Every action you took on any other page (triage, escalation, SMR lodgement, review completion) shows up here immediately, tagged with what changed and why.

### Process Map
A read-only reference: the full lifecycle laid out phase by phase, each step linking directly to the page that implements it. Use this if you're not sure which page handles a given stage of the AML/CTF process.

### Worked Example: Follow One Suspicious Customer End to End

1. Go to **Home** → note a customer showing up in the "High / Critical Risk" KPI.
2. Go to **Screening** → filter Status = "Open" to find a customer with an unresolved PEP or sanctions hit.
3. Go to **Transaction Monitoring** → **Customer Drill-down** tab → select that same customer → check whether structuring or rapid-movement patterns appear in their transaction scatter plot.
4. Go to **Alerts & Triage** → find that customer's alert in the queue → set disposition to **Escalated to Case** → note the new case ID shown.
5. Go to **Case Management & SMR** → **Investigation Workspace** tab → select the new case → review the customer's full profile, alerts, and transactions together → write investigation notes → escalate to senior review.
6. **Escalation & Senior Review** tab → select the case → record decision **Continue Monitoring**.
7. **SMR Assessment, Drafting & Submission** tab → select the case → tick "reasonable grounds" → **Generate SMR Narrative** → review the auto-drafted narrative → download as `.docx` → mark as lodged with a reference number.
8. Go to **Audit Trail** → search for the case ID → see every single action above, timestamped and attributed, in one place.

---

## AML/CTF Concepts Explained

### What Is Money Laundering, Actually?

Money laundering is the process of making money that came from crime look like it came from a legitimate source. It's traditionally described in three stages:

1. **Placement** — getting "dirty" cash into the financial system in the first place (e.g. depositing cash at a bank).
2. **Layering** — moving that money around through multiple transactions, accounts, or jurisdictions to obscure where it originally came from.
3. **Integration** — the money re-emerges looking clean, e.g. used to buy property or invested in a legitimate business.

**Terrorism financing** is a related but distinct concern: moving money to fund terrorist activity. The money involved isn't necessarily illegally obtained (it might be legitimate donations), which is why AML and CTF ("Counter-Terrorism Financing") are usually regulated together but require slightly different detection approaches.

### Why Financial Businesses Have to Care

Any business that provides financial services — banks, remittance providers, digital currency exchanges, casinos, and more — is a potential entry point for laundering money, whether they want to be or not. Governments require these "reporting entities" to run an **AML/CTF Program**: a documented set of controls (customer checks, transaction monitoring, staff training, reporting obligations) designed to detect and prevent their services being misused. In Australia, this is enforced under the **AML/CTF Act 2006 (Cth)**, regulated by **AUSTRAC**. Failing to run an adequate program carries serious civil and criminal penalties for the business and, in some cases, individuals.

This app models what the *operational* side of that program looks like day to day for a compliance team.

### Core Concepts, One at a Time

### Risk-Based Approach (RBA)
The core idea underpinning everything else: not every customer carries the same risk, so it doesn't make sense to check them all the same way. A student opening a savings account and an import/export business wiring money to six countries don't need the same level of scrutiny. The RBA means: **assess risk first, then apply controls proportionate to that risk.**
*In the app:* `onboarding_utils.score_onboarding()` builds a risk score from weighted factors, and that score decides everything downstream — how much verification is required, how the case is handled if something goes wrong, and how often the customer gets re-checked.

### KYC vs. CDD vs. EDD vs. SDD
These four terms get used almost interchangeably, but they're layered:
- **KYC (Know Your Customer)** — the umbrella term: knowing who your customer actually is.
- **CDD (Customer Due Diligence)** — the standard process of verifying identity and understanding the relationship (purpose, expected activity) for a typical-risk customer.
- **EDD (Enhanced Due Diligence)** — extra steps for higher-risk customers: verifying source of funds/wealth, more senior approval, more frequent monitoring.
- **SDD (Simplified Due Diligence)** — a lighter-touch version for genuinely low-risk, low-value relationships.
*In the app:* the `cdd_tier` field on every `OnboardingResult` is literally one of these four, chosen automatically based on the calculated risk level.

### PEP (Politically Exposed Person)
Someone who holds — or has held — a prominent public role (politicians, senior government officials, judges, military leaders), or their close family/associates. PEPs aren't inherently criminals, but their position creates elevated bribery and corruption risk, so relationships with them require EDD by default.
*Example in the app:* on the **UBO Network** page, if a beneficial owner is flagged as a PEP, the app raises a warning that EDD and senior sign-off are required for that entity.

### Sanctions Screening
Checking a customer's name against government and international sanctions lists — people, entities, and sometimes whole countries that are legally prohibited from being serviced (this can include asset freezes, trade bans, or outright prohibition on doing business with them). A genuine sanctions match isn't a "proceed with caution" situation — it typically means **do not provide the service** until the match is formally cleared.
*In the app:* a sanctions hit is the one factor that overrides the numeric risk score entirely — `score_onboarding()` returns a hard "DO NOT ONBOARD" decision whenever one exists, no matter how low the rest of the score is.

### Adverse Media Screening
Searching news archives and public records for negative coverage linked to a customer — fraud investigations, bribery allegations, asset seizures. Unlike a sanctions or PEP list, this isn't a fixed database; it's closer to "does searching this person's name turn up anything concerning."

### Structuring (a.k.a. Smurfing)
Deliberately splitting a transaction into smaller pieces to dodge a reporting threshold. In Australia, a single cash transaction of **AUD $10,000 or more** automatically triggers a Threshold Transaction Report (TTR) — no suspicion required, it's just automatic. Structuring means depositing, say, four lots of $9,200 instead of one $36,800 deposit, specifically to stay under that automatic trigger.
*Concrete example the app detects:* `report_utils.detect_structuring()` looks for 3+ cash deposits between $8,500–$9,999.99 within any 10-day window — exactly this pattern.

### Layering / Rapid Movement of Funds
Moving money quickly through an account with no clear business reason, to make its origin harder to trace. A red flag isn't that money moved — it's that it moved *fast*, *out again quickly*, with no explanation matching the customer's stated profile.
*Concrete example the app detects:* `report_utils.detect_rapid_movement()` flags any inbound credit of $25,000+ where 60%+ of it left the account again within 3 days.

### UBO (Ultimate Beneficial Owner)
The real human being(s) who actually own or control a company or trust — even if that control is hidden behind several layers of corporate structure (a company owned by a trust owned by another company, say). Identifying UBOs stops people from using complex corporate structures to hide who's really behind a transaction.
*In the app:* the **UBO Network** page visualizes exactly this — tracing each business back to its individual owners, however many layers it takes.

### SMR (Suspicious Matter Report) & AUSTRAC
Once a reporting entity forms **reasonable grounds to suspect** a transaction or customer relates to money laundering, terrorism financing, or certain other offences, it must lodge a formal report — in Australia, an **SMR**, lodged with **AUSTRAC** (the Australian Transaction Reports and Analysis Centre, the national financial intelligence agency). This has to happen within **3 business days** of forming the suspicion (**24 hours** if terrorism financing is involved) — this isn't optional, and the deadline runs from when suspicion is formed, not when the investigation is finished.
*In the app:* the SMR narrative `4_Case_Management_SAR.py` generates follows AUSTRAC's expected structure — a WHO/WHAT/WHEN/WHERE/HOW/WHY narrative — and both statutory deadlines are stated explicitly in the generated draft.

### MLRO (Money Laundering Reporting Officer)
The person formally designated as accountable for a business's AML/CTF Program — approving escalated cases, authorising SMR lodgement, and acting as the point of contact with the regulator. Every "senior review" and "critical risk" decision point in this app is modeled as requiring MLRO sign-off, because in a real program, it would.

### Periodic Review / Ongoing Due Diligence
AML/CTF obligations don't stop the day a customer is onboarded. Risk profiles change — a low-risk customer today might not be low-risk in two years — so customer information and risk ratings get re-verified on a schedule proportionate to their current risk level.
*In the app:* `workflow_utils.review_due_date()` implements a Low = 24 months / Medium = 12 months / High = 6 months / Critical = 3 months review cadence.

### TTR (Threshold Transaction Report) / IFTI (International Funds Transfer Instruction)
Two categories of report that are triggered **automatically by the transaction itself**, with no suspicion required: a TTR fires on any cash transaction ≥ $10,000 in Australia; an IFTI report covers instructions to transfer funds into or out of Australia. These exist alongside SMRs (which require suspicion) as a separate, mechanical layer of reporting.

### Record Keeping
The obligation to retain evidence of every decision, screening result, investigation, and report made — in a form a regulator or internal auditor can retrieve later. This is what makes an AML/CTF Program defensible: it's not enough to have made the right call, you have to be able to prove you made it, when, and why.
*In the app:* every single action across every page writes to the audit trail via `workflow_utils.log_audit()`, visible and exportable on the **Audit Trail** page.

### Frequently Asked Questions

**Q: If the total amount is the same, why does splitting a deposit into smaller pieces matter?**
Because the $10,000 threshold isn't a risk judgment — it's an automatic trigger. The law wants *every* transaction at or above that amount reported, no exceptions, specifically so a database of large cash movements exists for financial intelligence purposes. Deliberately staying under it defeats that reporting mechanism, which is itself treated as a red flag regardless of whether the underlying money is actually illicit.

**Q: What's the practical difference between a PEP hit and a sanctions hit?**
A PEP hit means "apply more scrutiny" — you can still service the customer, just with EDD. A sanctions hit typically means "do not service this customer at all" until the match is formally cleared as a false positive. They're both "watchlist hits" in this app's data model, but they carry very different consequences.

**Q: What actually happens after an SMR is lodged?**
The reporting entity's obligation shifts from "detect and report" to **"don't tip off the customer, and keep monitoring."** AUSTRAC receives the report as financial intelligence — it isn't a request for permission, and the reporting entity doesn't typically find out what (if anything) happens next. The case moves to Post-SMR Monitoring in this app to reflect that the relationship is still being watched even though the report has already gone out.

**Q: Does escalating an alert always mean something bad happened?**
No — most escalations turn out to be false positives after investigation, which is exactly why the workflow exists: to separate genuine risk from noise *before* anything gets reported. A high volume of alerts is normal and expected; the whole point of triage is filtering that volume down to what actually warrants deeper review.

**Q: Why does risk level affect how often a customer gets reviewed, not just how they're onboarded?**
Because risk isn't static. A legitimate business can start doing something new and riskier; a dormant account can suddenly become active. Reviewing higher-risk customers more frequently is how a program catches that drift instead of relying entirely on a point-in-time decision made at onboarding.

## Technical Reference: Every Function, Module by Module

A function-by-function reference for every module in the codebase — what each function does, its signature, and the AML/CTF logic it implements.

#### Architecture at a Glance

```
db_utils.py  ──────────► generates/loads every DataFrame (customers, transactions,
                          screening, cases, businesses, ubo, alerts, audit_log)
     │
     ▼
pages/*.py   ──────────► read data via load_all(), filter/display it, and call
     │                    into the three "engine" modules below for anything
     │                    that isn't a plain lookup
     │
     ├──► report_utils.py      (typology detection + AUSTRAC SMR drafting)
     ├──► onboarding_utils.py  (CDD/EDD risk scoring at intake)
     ├──► workflow_utils.py    (case/alert state machine + audit trail)
     └──► theme.py             (styling + every chart on every page)
```

Every page is a **read-and-act** script: it loads data once (cached), lets the analyst filter/select, and any action (triage an alert, escalate a case, complete a review) goes through `workflow_utils.log_audit()` so it lands in the Audit Trail page automatically. Nothing is a silent side effect.

---

### `db_utils.py` — Data Access Layer

The single place every page imports data from. Swapping `USE_DEMO_DATA` between `True`/`False` is the only change needed to point the whole suite at a real Postgres warehouse instead of synthetic data — no page needs to change.

| Function | Signature | What it does |
|---|---|---|
| `get_engine()` | `() -> Engine` | Cached SQLAlchemy engine for the live-database mode, built from `DB_CONFIG`. |
| `run_query()` | `(sql: str, params: dict = None) -> pd.DataFrame` | Executes raw SQL against the live database. Only used when `USE_DEMO_DATA = False`. |
| `load_customers()` | `(n: int = 260) -> pd.DataFrame` | Generates the synthetic customer book. Each customer's `risk_score` is built additively: a random base (5–55) plus a penalty if their country is in `_HIGH_RISK_COUNTRIES` (+15–30) plus a penalty if their industry is cash-intensive/typology-prone (+10–25) — the same additive, weighted-factor logic a real risk model uses, just compressed into one function. |
| `load_transactions()` | `(customers, seed=2) -> pd.DataFrame` | Generates 15–45+ transactions per customer (volume scales with risk score), **then deliberately injects three typology patterns** into a subset of higher-risk customers so the detectors in `report_utils.py` have real patterns to find: a burst of cash deposits just under $10,000 (structuring), a large inbound wire quickly drained (rapid movement), and wires to/from high-risk jurisdictions. |
| `load_screening()` | `(customers, seed=3) -> pd.DataFrame` | Generates PEP / Sanctions / Adverse Media watchlist hits, weighted so higher-risk customers are far more likely to have one or more open hits. |
| `load_cases()` | `(customers, screening, seed=4) -> pd.DataFrame` | Builds the case register from customers who are either high-risk or have an open/escalated screening hit, and randomly distributes them across every stage of `workflow_utils.CASE_STATUSES` so every page of the lifecycle has real examples to show. |
| `load_businesses()` | `(n=55, seed=5) -> pd.DataFrame` | Generates the corporate customer register (legal name, ABN, structure type, incorporation country/date, risk rating). |
| `load_ubo()` | `(businesses, seed=6) -> pd.DataFrame` | Generates a simplified beneficial-ownership register: 1–3 owners per business, ownership percentages summing to 100%, each owner randomly flagged as a PEP (~6% chance) — the data `5_UBO_Network.py` visualizes. |
| `load_txn_alerts()` | `(customers, transactions, seed=7) -> pd.DataFrame` | Runs `report_utils.run_all_detections()` across every customer's transactions and turns each `Finding` into a triage-able alert row — this is the bridge between "a rule fired" and "an analyst has something to action." |
| `load_alerts()` | `(customers, transactions, screening) -> pd.DataFrame` | Merges transaction-monitoring alerts and watchlist-screening hits into **one normalized queue** (same schema, same disposition states) — this is exactly what `8_Alerts_Triage.py` displays. |
| `load_audit_log()` | `(customers, cases, alerts, seed=8) -> pd.DataFrame` | Backfills a plausible historical audit trail (onboarding entries, periodic reviews, alert triage, case escalation, SMR lodgement, case closure) so `10_Audit_Trail.py` has real history before the current session adds anything. |
| `load_all()` | `() -> dict[str, pd.DataFrame]` | The one function every page actually calls. Assembles and returns all eight DataFrames above, switching transparently between demo generation and live SQL based on `USE_DEMO_DATA`. |

---

### `report_utils.py` — Typology Detection & SMR Builder

This module has two jobs: (1) find suspicious transaction patterns automatically, and (2) turn any findings into an AUSTRAC-formatted Suspicious Matter Report draft.

### Typology detectors

| Function | Signature | Detection logic |
|---|---|---|
| `detect_structuring()` | `(txns: pd.DataFrame) -> Finding \| None` | Filters cash deposits between $8,500–$9,999.99 (just under the $10,000 `REPORTING_THRESHOLD`), buckets them into rolling 10-day windows, and flags any window with **3 or more** such deposits — the classic "smurfing" pattern of splitting a large cash sum into sub-threshold pieces to avoid triggering a Threshold Transaction Report. |
| `detect_rapid_movement()` | `(txns: pd.DataFrame) -> Finding \| None` | For every inbound credit ≥ $25,000, checks whether ≥60% of that amount left the account again via outbound transactions within 3 days — money moving through an account quickly with no apparent business rationale is a classic layering/pass-through indicator. |
| `detect_high_risk_wires()` | `(txns, high_risk_countries: set) -> Finding \| None` | Flags customers with 2+ international wires to/from a jurisdiction in the high-risk set (`HIGH_RISK_COUNTRIES_DEFAULT`), and sums the total exposure. |
| `run_all_detections()` | `(txns: pd.DataFrame) -> list[Finding]` | Runs all three detectors above and returns whichever fired — the single entry point `load_txn_alerts()` and `build_smr()` both call. |

Each detector returns a `Finding` dataclass (`typology`, `summary`, `evidence` DataFrame, `severity`) rather than a raw boolean, so the same result can be shown in a table, folded into an alert, or narrated into an SMR without re-deriving anything.

### SMR (Suspicious Matter Report) narrative builder

`SMRReport` is a dataclass that assembles a full AUSTRAC-aligned draft from a customer row, their `Finding`s, and their screening hits:

| Method | What it builds |
|---|---|
| `part_a_reporting_entity()` | Reporting entity details, AUSTRAC reference placeholders, report reference, timestamp. |
| `part_c_suspicious_person()` | Customer identification block: ID, name, type, occupation/industry, country, relationship history, current risk rating. |
| `part_b_transaction_summary()` | Bullet list of every triggered typology and its `Finding.summary`. |
| `grounds_for_suspicion()` | The **WHO / WHAT / WHEN / WHERE / HOW / WHY** narrative AUSTRAC expects, built programmatically: `_when_range()` derives the date span from the evidence, `_where_summary()` lists channels/countries involved, `_how_summary()` describes the mechanism per typology, and the WHY section cites the specific regulatory basis for suspicion (e.g. explicitly referencing structuring under s.142 of the AML/CTF Act when that typology fired). |
| `full_text()` | Concatenates every section into one submission-ready draft, with a bolded statutory-timeframe reminder (3 business days for ML/structuring, 24 hours if terrorism financing is suspected) and an explicit "do not submit unedited" warning. |

| Function | Signature | Purpose |
|---|---|---|
| `build_smr()` | `(customer_row, txns, screening_hits) -> SMRReport` | The single entry point `4_Case_Management_SAR.py` calls: pulls the customer's own transactions and screening hits, runs detection, and returns a ready-to-render `SMRReport`. |
| `smr_to_docx_bytes()` | `(report: SMRReport) -> bytes` | Renders the same report as a formatted Word document (headings, a red "DRAFT ONLY" warning banner, and an evidence table of the first 8 flagged transactions per typology) via `python-docx`, returned as in-memory bytes for `st.download_button`. |

---

### `onboarding_utils.py` — CDD/EDD Scoring Engine

Powers `7_New_Client_Onboarding.py`. The design goal stated in the module docstring is **transparency**: every point added to a customer's risk score is a named, explained `RiskFactor`, so a compliance officer (or an interviewer reviewing this project) can see exactly why a score landed where it did — mirroring how a real AML/CTF Program documents its customer risk assessment methodology.

| Function | Signature | What it does |
|---|---|---|
| `run_screening()` | `(full_name, is_business, self_declared_pep) -> list[dict]` | Simulates a real-time PEP/Sanctions/Adverse Media watchlist check. A self-declared PEP is always flagged; sanctions/adverse-media/PEP database "matches" use a deterministic hash of the name (`_name_hash_signal`) so results are reproducible in the demo rather than truly random — standing in for a real provider like Dow Jones or World-Check. |
| `score_onboarding()` | `(answers: dict, screening_hits: list[dict]) -> OnboardingResult` | The core risk model. Walks through every standard AML/CTF risk category in order and appends a `RiskFactor` for each one that applies: customer type & structure (trusts/foreign subsidiaries score higher; a PEP among beneficial owners adds +30), geography, industry, purpose of the relationship, source of funds/wealth, expected transaction volume and channels, non-face-to-face verification, and any screening hits (sanctions +60, PEP +30, adverse media +20). Sums to a 0–100 score, maps that to a risk level and CDD tier, and derives an onboarding decision — including an automatic **"DO NOT ONBOARD"** decision if any sanctions hit exists, regardless of the numeric score. |
| `cdd_record_text()` | `(answers, result) -> str` | Renders the full CDD file as plain text: identification, beneficial ownership (if a business), relationship/activity profile, screening results, the itemized risk-factor table, the final decision, and a sign-off block. |
| `cdd_record_to_docx_bytes()` | `(answers, result) -> bytes` | The same record as a formatted Word document, with the risk rating color-coded (green/amber/orange/red by level) and structured tables for beneficial owners, screening hits, and risk factors. |

`OnboardingResult` (the dataclass returned by `score_onboarding`) carries `factors`, `score`, `risk_level`, `cdd_tier`, `decision`, and `screening_hits` together, plus a `factor_table()` helper that turns the factor list into a display-ready DataFrame.

---

### `workflow_utils.py` — Workflow State & Audit Logging

There's no backing database transaction layer in this demo, so every mutable piece of state (alert dispositions, case status changes, completed reviews) lives in `st.session_state`, seeded once from the synthetic data. This module is the thin state-machine layer that makes that safe and consistent.

| Function | Signature | What it does |
|---|---|---|
| `init_state()` | `(key: str, loader) -> DataFrame \| list` | Seeds `st.session_state[key]` from `loader()` exactly once per session, then returns the same live, mutable object on every later call — the pattern every page uses to get a "live" copy of cases/alerts/reviews that survives reruns and reflects edits. |
| `log_audit()` | `(action, entity_type, entity_id, detail, actor="Current User")` | Appends one timestamped record-keeping entry to `st.session_state["audit_log_live"]`. Every state-changing action in the suite — triaging an alert, escalating a case, recording a senior decision, lodging an SMR, completing a periodic review — calls this, which is what satisfies the AML/CTF "who did what, when, and why" record-keeping obligation. |
| `full_audit_log()` | `(seed_df: pd.DataFrame) -> pd.DataFrame` | Concatenates the seeded historical log with anything logged live this session, sorted newest-first — what `10_Audit_Trail.py` actually displays. |
| `review_due_date()` | `(onboarding_date, risk_level: str) -> pd.Timestamp` | Applies the risk-based periodic review schedule (`REVIEW_INTERVAL_MONTHS`: Low 24mo / Medium 12mo / High 6mo / Critical 3mo) to compute when a customer's next review falls due. |
| `status_pill_html()` | `(status: str) -> str` | Maps any workflow status string to a themed colored "pill" badge (e.g. anything containing "closed" + "restrict" renders as a critical-red pill) — shared across every page that displays a status column. |

Module-level constants worth knowing: `CASE_STATUSES` (the 8-stage case lifecycle), `ALERT_DISPOSITIONS`, `SENIOR_DECISIONS`, and `STAGE_TO_PAGE` — a lookup used by `11_Process_Map.py` to link each lifecycle stage to the page that implements it.

---

### `theme.py` — Visual Theme & Chart Engine

Every page imports its styling and charts from here, so the whole suite reads as one visually consistent system rather than 11 separately-styled pages. Current palette: teal / cream / brown / white, with every chart drawing from the same harmonized color generators.

| Function | Purpose |
|---|---|
| `inject_css()` | Injects the shared stylesheet (glass cards, warm shadows, pill badges, sidebar styling) and the world-map watermark background into every page. |
| `page_header()`, `section_title()`, `section_toolbar()`, `kpi_card()` | Layout primitives: the top banner, section dividers, a title-plus-interactive-control row, and the KPI stat cards used across every page. |
| `risk_pill()` | Maps a risk level string (`Low`/`Medium`/`High`/`Critical`) to a themed colored badge — used on every register/queue table in the suite. |
| `chart_layout_2d()` | The single shared Plotly layout every chart is built from: transparent background so the white card shows through, warm gridlines, unified hover with spike lines, and a smooth transition on re-render. |
| `enable_rich_interaction()` | Layers legend click-to-isolate and marker-opacity tuning onto any figure. |
| `teal_gradient()` / `brown_gradient()` | Map a numeric sequence onto a pale→deep teal or brown color ramp, so magnitude and color both reinforce each other on any non-semantic bar chart. |
| `bar3d_chart()` | A single-series bar chart, colored from the harmonized palette. (Named `bar3d_chart` for backwards compatibility with an earlier 3D version of the engine — every page calls it with the same arguments regardless of the underlying rendering.) |
| `grouped_bar3d_chart()` | A clustered bar chart — one bar per series per category, e.g. risk level breakdown by industry. |
| `target_bar3d()` | A radial gauge with a target threshold line, used for the Home page's compliance health metrics. |
| `ribbon3d_chart()` | A multi-series area/trend chart with a genuine vertical gradient fill per series. |
| `waterfall3d_chart()` | A waterfall chart (Plotly's native `Waterfall` trace) for the customer lifecycle drop-off view on Home. |
| `scatter3d_chart()` | A scatter plot for the transaction drill-down, with group coloring and per-point symbols. |
| `network3d_chart()` | A radial node-link diagram for the UBO ownership structure view, with node size driven by ownership percentage. |

---


## Disclaimer

This project is built for **portfolio and educational purposes**. AUSTRAC references, SMR formatting and AML/CTF terminology are used to demonstrate familiarity with an Australian regulatory context, but:

- The generated SMR draft is explicitly labeled as a draft requiring review and sign-off by a qualified compliance officer/MLRO before any real-world use.
- This is **not** a certified or production-ready compliance tool, and should not be used to make real AML/CTF decisions.
- All data is synthetic; no real customer, transaction or case information is included anywhere in this repository.

## Roadmap

- [ ] Add automated tests for the typology detection logic in `report_utils.py`
- [ ] Add a Dockerfile for one-command setup
- [ ] Expand the live-database schema and add a seed script for PostgreSQL


## Author

**Brian Phu**
GitHub: [github.com/brianphu2310](https://github.com/brianphu2310)

If you're a recruiter or fellow analyst looking at this project — feel free to open an issue or reach out via GitHub with any questions.
