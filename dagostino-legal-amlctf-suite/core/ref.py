"""Static reference data (analysts, branches, clients, named entities, typologies).
Everything time-varying is generated in core/model.py from this reference set so that
every number in the dashboard reconciles to one source of truth.

Fictional world note: this is the same fictional firm as the companion project
(D'Agostino Legal — Financial Operations Dashboard). This app is its back-office
AML/CTF compliance function, built to demonstrate the analyst-side workflow created
by Australia's AML/CTF Tranche 2 reforms, which bring law firms performing trust
account services, conveyancing and business structuring into AUSTRAC's regulated
population as reporting entities from 1 July 2026.
"""
import pandas as pd

AS_OF = pd.Timestamp("2025-09-17")           # "today" for the sample data
START = pd.Timestamp("2023-07-01")           # first month of history
NAV_ITEMS = ["Overview", "KYC", "Monitoring", "Triage", "SMR", "UBO", "Team", "Simulator"]
USER_NAME, USER_ROLE = "Brian Phu", "AML/CTF Compliance Analyst"

BRANCHES = [
    {"name": "Richmond", "council": "Hawkesbury City Council"},
    {"name": "Camden", "council": "Camden Council"},
    {"name": "Liverpool", "council": "Liverpool City Council"},
]
BRANCH_NAMES = [b["name"] for b in BRANCHES]

# Compliance team — the analysts who work the alert queue and case register. Capacity is the analyst's
# monthly alert caseload cap (a boutique firm's team, not a bank's), sized so the team runs with headroom
# at the current thresholds but is genuinely stretched if thresholds are loosened firm-wide.
ANALYSTS = [
    {"name": "Sofia Marchetti", "short": "Marchetti, S.", "role": "Compliance Manager", "branch": "Richmond", "start": "2022-03-01", "capacity": 4, "avg_hours": 2.6},
    {"name": "Priya Anand", "short": "Anand, P.", "role": "Senior AML Analyst", "branch": "Richmond", "start": "2022-08-01", "capacity": 9, "avg_hours": 2.1},
    {"name": "Marcus Webb", "short": "Webb, M.", "role": "Senior AML Analyst", "branch": "Camden", "start": "2023-01-01", "capacity": 9, "avg_hours": 2.2},
    {"name": "Daniel Okafor", "short": "Okafor, D.", "role": "AML Analyst", "branch": "Camden", "start": "2023-06-01", "capacity": 7, "avg_hours": 2.5},
    {"name": "Grace Lin", "short": "Lin, G.", "role": "AML Analyst", "branch": "Liverpool", "start": "2023-09-01", "capacity": 7, "avg_hours": 2.4},
    {"name": "Ethan Walsh", "short": "Walsh, E.", "role": "AML Analyst", "branch": "Liverpool", "start": "2024-05-01", "capacity": 6, "avg_hours": 2.7},
]
ANALYST_SHORT = [a["short"] for a in ANALYSTS]

# ------------------------------------------------------------- AUSTRAC 4-factor risk model ----
CUSTOMER_TYPES = {  # name: (base risk points 0-100, share of new customers)
    "Individual": (18, 0.42), "Company": (38, 0.24), "Trust": (52, 0.13), "SMSF": (30, 0.09),
    "Partnership": (34, 0.07), "Foreign Entity": (74, 0.05),
}
CHANNELS = {  # delivery/service channel
    "Face-to-face": (10, 0.46), "Non face-to-face (digital)": (48, 0.30), "Introduced / referral": (30, 0.16), "Third-party intermediary": (62, 0.08),
}
# Foreign dimension — fictional jurisdiction tiers (no real country is characterised as high-risk here).
FOREIGN_TIERS = {
    "Domestic only": (8, 0.58, []),
    "Tier 1 — low-risk foreign link": (28, 0.24, ["Corvenia", "Meridia", "Nova Republic", "Aldwyn"]),
    "Tier 2 — elevated foreign link": (55, 0.12, ["Bassano", "Ostralia", "Drammen Isles"]),
    "Tier 3 — FATF-monitored jurisdiction": (85, 0.06, ["Kalvara", "Rennport", "Ilsenberg"]),
}
PRODUCTS = {  # products / services
    "Conveyancing (trust transfer)": (26, 0.34), "Trust account services": (46, 0.22), "Business structuring": (58, 0.19),
    "Safe custody / controlled money": (40, 0.13), "Trust & estate administration": (32, 0.12),
}
RISK_WEIGHTS_DEFAULT = {"type": 0.28, "channel": 0.22, "foreign": 0.27, "product": 0.23}     # sum to 1.0
RISK_TIER_BOUNDS = (28.0, 42.0)     # < lo = Low, lo..hi = Medium, > hi = High

# ------------------------------------------------------------------- typologies ----
TYPOLOGIES = {
    "Structuring / smurfing": {"desc": "Multiple transactions kept just under the AUD 10,000 reporting threshold.", "base_rate": 0.038, "fp_rate": 0.62, "hours": 2.4},
    "Rapid movement of funds": {"desc": "Funds received into trust and disbursed again within an unusually short window.", "base_rate": 0.029, "fp_rate": 0.55, "hours": 2.0},
    "High-risk jurisdiction transfer": {"desc": "Trust transfers to or from a Tier 2/3 jurisdiction with no clear commercial rationale.", "base_rate": 0.021, "fp_rate": 0.48, "hours": 2.9},
    "Cash-intensive pattern": {"desc": "Cash-equivalent settlement volume inconsistent with the client's stated profile.", "base_rate": 0.025, "fp_rate": 0.58, "hours": 2.1},
    "Trade-based ML indicator": {"desc": "Under/over-valuation or circular invoicing across related-party structuring matters.", "base_rate": 0.014, "fp_rate": 0.44, "hours": 3.2},
}
TYPOLOGY_NAMES = list(TYPOLOGIES)

DISPOSITIONS = ["Open", "Under investigation", "Escalated to SMR", "Closed — false positive", "Closed — no further action"]
SLA_DAYS = 10          # target analyst turnaround, alert open -> disposition

# Named "key" customers — reused from the companion operations dashboard's client base where the
# entity also engages the firm's regulated trust/conveyancing/structuring services, plus a few
# AML-specific names, so a handful of matters reconcile across both dashboards.
NAMED_CUSTOMERS = [
    # name, type, channel, foreign_tier, product, onboarded, risk_tier_hint
    ("Meridian Holdings Ltd.", "Trust", "Introduced / referral", "Domestic only", "Business structuring", "2017-03-11"),
    ("Meridian Pacific Trust", "Trust", "Non face-to-face (digital)", "Tier 2 — elevated foreign link", "Trust account services", "2023-05-02"),
    ("Global Trust Bank", "Company", "Face-to-face", "Domestic only", "Trust account services", "2020-02-14"),
    ("Singapore Trading Group", "Foreign Entity", "Introduced / referral", "Tier 1 — low-risk foreign link", "Business structuring", "2022-04-19"),
    ("London Capital Partners", "Foreign Entity", "Third-party intermediary", "Tier 1 — low-risk foreign link", "Business structuring", "2023-08-03"),
    ("Halcyon Systems", "Company", "Face-to-face", "Domestic only", "Conveyancing (trust transfer)", "2016-06-01"),
    ("Vertex Industries", "Company", "Face-to-face", "Domestic only", "Trust account services", "2018-06-14"),
    ("Blackwood Realty", "Company", "Face-to-face", "Domestic only", "Conveyancing (trust transfer)", "2021-02-20"),
    ("Kalvara Ventures Pty Ltd", "Foreign Entity", "Third-party intermediary", "Tier 3 — FATF-monitored jurisdiction", "Business structuring", "2024-11-07"),
    ("Rennport Maritime Holdings", "Trust", "Non face-to-face (digital)", "Tier 3 — FATF-monitored jurisdiction", "Trust & estate administration", "2025-01-22"),
]

# UBO network — a handful of named matters with layered beneficial ownership, for the network page.
UBO_ENTITIES = {
    "Meridian Pacific Trust": [("Meridian Holdings Ltd.", 55), ("C. Ashworth (individual)", 25), ("Bassano Nominees Ltd", 20)],
    "Meridian Holdings Ltd.": [("J. Meridian (individual)", 62), ("R. Okonkwo (individual)", 38)],
    "Kalvara Ventures Pty Ltd": [("Rennport Maritime Holdings", 40), ("Ilsenberg Capital SA", 35), ("D. Voss (individual)", 25)],
    "Rennport Maritime Holdings": [("A. Bergqvist (individual)", 70), ("Ilsenberg Capital SA", 30)],
    "Singapore Trading Group": [("W. Tanaka (individual)", 48), ("Corvenia Trading Pte", 32), ("L. Marsh (individual)", 20)],
}

AUSTRAC_STATUSES = ["Draft", "Submitted", "Acknowledged"]

# Customer's registered state/territory (a national client base even though the three offices are all in
# Greater Sydney) — population-weighted so the geographic mix looks like a real Australian client book.
# Assigned with an independent RNG stream in core.model so it never perturbs the existing onboarding /
# risk-scoring / alert-generation sequence (and the numbers in README's "Example findings" stay unchanged).
AU_STATES = {"NSW": 0.31, "VIC": 0.26, "QLD": 0.20, "WA": 0.11, "SA": 0.07, "TAS": 0.02, "ACT": 0.02, "NT": 0.01}
AU_STATE_NAMES = list(AU_STATES)
