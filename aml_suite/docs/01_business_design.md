# Project Redesign — AML/CTF Compliance Suite for a Law Firm
## Business Design Document (v1)

**Purpose of this document:** before touching code, this defines the compliance
methodology the app will actually implement — the same way an AML/CTF Compliance
Officer would document it before asking a developer (or a Streamlit app) to build
anything. Everything below is written to be defensible in a job interview: if
asked "why did the model flag this?", the answer should trace back to a rule in
this document, not to a random synthetic-data quirk.

---

## 1. Regulatory framing

**Entity type:** Mid-size Australian law firm providing designated services under
the *AML/CTF Act 2006 (Cth)*, newly captured as a reporting entity under the
**Tranche 2 reforms** (obligations commenced 1 July 2026; AUSTRAC enrolment
deadline 29 July 2026).

**Designated services in scope** (the firm is regulated only for *these*
activities, not "law" generally):
- Item 3 — receiving, holding, controlling or managing client money or property
  when assisting with planning or executing a transaction (**trust account
  activity** — the core of the project, and the part that maps directly onto
  your bookkeeping role)
- Item 4 — assisting clients with equity or debt financing transactions
- Item 7 — acting as, or arranging for someone to act as, a director, secretary,
  or trustee for a client entity
- Item 8 — acting as, or arranging for someone to act as, a nominee shareholder
- Item 9 — providing a registered office / principal place of business address

**Out of scope (deliberately):** general legal advice, litigation, and any matter
with no designated service attached. This distinction — "we regulate the
service, not the lawyer" — is a real AUSTRAC concept and worth stating explicitly
in the README; it shows you understand scope, not just "law firms now do AML."

**AML/CTF Program structure modeled:**
1. ML/TF Risk Assessment (the "centrepiece" — drives everything else)
2. Customer Due Diligence policy (initial CDD, ongoing CDD, Enhanced CDD triggers)
3. Transaction monitoring & alert procedures
4. Suspicious Matter Reporting (SMR) procedure
5. Governance: an AML/CTF Compliance Officer at management level, record-keeping
   (7-year retention), staff training register

The app will visibly implement pieces of (1)–(4). Governance (5) is documented
in the README as "how this would be operationalised" rather than built as a
feature — a portfolio project shouldn't pretend to be a full compliance
department, and overclaiming that is a bigger risk in interview than admitting
a boundary.

---

## 2. ML/TF Risk Assessment — the customer risk rating model

AUSTRAC requires risk to be assessed across four factor categories, and a
customer's rating to be derived from the *combination* of them, not any single
flag in isolation. The model below mirrors that structure.

### 2.1 Risk factor categories

| Category | What it captures | Example factors used in this project |
|---|---|---|
| **Customer type** | Who the client is | Individual vs. company vs. trust; complexity of ownership/control structure; PEP status (domestic/foreign, low-profile/high-profile); cash-intensive business; shell-company indicators |
| **Jurisdiction** | Where the client, their funds, or counterparties are connected | Client residency/incorporation; source-of-funds country; any FATF grey/black-listed or high-risk jurisdiction link |
| **Service/product** | What designated service is being provided | Trust account transaction vs. company formation vs. nominee director/shareholder arrangement — each has a different inherent risk (e.g. nominee arrangements are structurally higher risk than a standard conveyancing trust transaction) |
| **Delivery channel** | How the client engaged the firm | Face-to-face vs. fully remote onboarding; direct instruction vs. via an intermediary/referrer with no direct client contact |

### 2.2 Scoring approach

Each factor is scored **0 (no elevated risk) / 1 (medium) / 2 (high)** within
its category. Category scores are summed, not averaged, because AUSTRAC's
guidance is explicit that **the presence of a single high-risk factor can be
enough to drive a high overall rating**, regardless of how low the other
factors are — a risk model that "smooths out" one bad factor with three good
ones is a known real-world failure mode, so the model must not average it away.

```
if any single factor scores 2 (high)      -> overall rating = HIGH
elif sum of factor scores >= threshold_M  -> overall rating = MEDIUM
else                                       -> overall rating = LOW
```

This "any-high-factor-triggers-high" rule is taken directly from AUSTRAC's own
worked example for a conveyancer's risk model and is the single most important
piece of methodology to get right — and to be able to explain — because it's
exactly the kind of question a compliance interviewer will ask ("walk me
through how your model handles one bad factor among good ones").

### 2.3 What the rating drives

The customer's rating is not cosmetic — it must visibly determine:
- **Initial CDD depth**: Low/Medium = standard KYC (verify identity, beneficial
  ownership for companies/trusts). High = **Enhanced CDD (EDD)**: source of
  wealth, source of funds, senior management sign-off, more frequent review.
- **Ongoing monitoring frequency**: Low = periodic review (e.g. 3-yearly),
  Medium = annual, High = 6-monthly or transaction-triggered.
- **Transaction monitoring sensitivity**: alert thresholds tighten for
  High-rated customers (this is the link between the risk model and the
  transaction monitoring engine in §3 — they must not be two disconnected
  features).

---

## 3. Transaction monitoring — typologies modeled

Real transaction monitoring systems detect **typologies** (known patterns), not
"big numbers." The project should implement a small, named, explainable set
rather than one generic "flag if > $10,000" rule, because that generic rule is
what every superficial student project does and is easy for a reviewer to spot
as shallow.

Given the law-firm trust-account context, the typologies below are the ones
that are actually realistic for *this* entity type (not copy-pasted bank
typologies like ATM cash-out rings, which don't apply here):

| Typology | Pattern | Why it matters for a law firm trust account |
|---|---|---|
| **Structuring** | Multiple deposits just under a reporting/internal threshold in a short window | Classic evasion of threshold transaction reporting |
| **Rapid movement of funds ("pass-through")** | Money received into trust and paid out again within an unusually short period, with no matching matter activity | Trust account used as a layering conduit rather than for its stated legal purpose |
| **Third-party funding mismatch** | Funds received from a party unrelated to the named client/matter, with no documented explanation | Possible nominee/straw-man arrangement |
| **Unexplained source-of-funds jump** | A client's inbound funds are materially inconsistent with their declared occupation/income profile at onboarding | Core "does the money match the story" check |
| **Round-dollar / repetitive-amount transactions** | Repeated identical or round amounts inconsistent with the matter type (e.g. conveyancing settlements are rarely round numbers) | Weak but real supporting indicator, used as a *contributing* signal, not standalone |
| **High-risk jurisdiction nexus** | Counterparty bank/entity linked to a high-risk jurisdiction | Direct AUSTRAC-listed risk factor |

**Design rule:** each alert must carry a `typology` field and a plain-English
`reason`, not just a severity score. An AML analyst's first question when
triaging an alert is always "what pattern is this," and the app should answer
that natively.

**Alert scoring:** each transaction gets a composite score from the typologies
above (weighted, not just counted), and only transactions crossing a threshold
generate an alert — this keeps the alert volume realistic (a bank generates
far more noise than signal; the project should demonstrate you understand
alert-to-case conversion rates matter, not just "flag everything").

---

## 4. Alert triage → case → SAR workflow

This is the operational backbone and should read like an actual analyst
queue, not a generic "kanban board":

```
Transaction Monitoring generates ALERT (system-generated, has typology + score)
        |
        v
ANALYST TRIAGE  ->  outcomes: [Escalate to Case] / [Close - False Positive] / [Close - No Issue, document rationale]
        |
        v (if escalated)
CASE  ->  investigation notes, linked customer profile + risk rating,
          linked prior alerts for same customer, financial analysis (see §5)
        |
        v
DECISION -> [File SMR with AUSTRAC] / [Close case - no SMR, rationale required] / [Request EDD refresh]
```

Two AUSTRAC-specific behaviours worth encoding because they're easy to miss and
strong signals of real domain knowledge:
- **No "tipping off"**: nothing in the case/alert UI should imply the customer
  is told about a pending SMR — this is a criminal offence for the reporting
  entity, so the workflow should show internal-only case notes.
- **SMR ≠ closing the client relationship automatically.** Filing an SMR is a
  reporting obligation, not an instruction to terminate the client — conflating
  the two is a common misunderstanding worth explicitly *not* making in the app.

---

## 5. Financial-analyst layer (the differentiator you asked for)

This is what will separate the project from a generic "AML dashboard" and
speak to the Financial Analyst angle:

**At the case level** (investigating a specific alert/customer):
- Simple cash-flow reconstruction for the matter: inflows vs. outflows over the
  investigation window, net position, and a running trust-ledger balance check
  (does money in/out reconcile to the matter's stated purpose — e.g. a
  property settlement should net to roughly the purchase price plus/minus
  agreed adjustments).
- Ratio-style sense checks: transaction value vs. the client's declared
  income/wealth band from onboarding; funding-source concentration (what % of
  inflow came from a single unrelated third party).

**At the portfolio level** (leadership-style reporting, matches your existing
Executive Dashboard):
- Alert volume and SMR-filing trend over time, alert-to-case conversion rate,
  case aging against the 3-business-day SMR filing expectation, risk-rating
  distribution across the client book, trust account funds-under-management
  trend. These are the KPIs a compliance/finance manager actually asks for at
  month-end, and they reuse the flat "BI-report" chart family already built in
  `theme.py` — no new chart engine needed, just the right metrics.

---

## 6. What "done" looks like for this stage

This document is complete when you're comfortable it matches how you'd explain
the project out loud in an interview. Next steps after your sign-off:

1. **Data model design** (`02_data_model.md`) — entities, fields, and how
   synthetic data will be generated so the typologies in §3 are genuinely
   *hidden in noise* rather than obviously injected.
2. **Rebuild plan** (`03_rebuild_plan.md`) — page-by-page mapping from this
   methodology to the Streamlit app, reusing `theme.py`'s existing 2D "BI
   report" chart family.
3. **README / case-study writeup** — the artifact a recruiter or hiring
   manager actually reads first.

Nothing gets coded until you've confirmed §2 and §3 make sense to you — those
two sections are the ones you need to be able to defend live in an interview.
