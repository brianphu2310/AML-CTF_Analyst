"""Case Decision engine — the logic behind the Simulator's "Case decision" mode.

An analyst enters (or loads) a case: who the client is, what moved through trust, which red flags were
observed and what has been verified. The engine turns that into a 0-100 suspicion score, a recommended
next step, the regulatory clocks that start running, and a what-if list ("verify source of funds and the
recommendation drops from Escalate to Enhanced CDD").

Pure functions only (no Streamlit), so every rule is unit-tested.

Regulatory anchors used in the wording (Australian AML/CTF Act 2006):
  * SMR — lodge within 3 business days of forming the suspicion; within 24 hours if it relates to
    terrorism financing (s41).
  * TTR — a threshold transaction report for physical currency of AUD 10,000 or more, within 10 business days.
  * Tipping off — disclosing that an SMR has been or will be lodged is prohibited (s123).
  * Records — keep transaction and CDD records for 7 years.
The scoring weights themselves are an illustrative, documented model for this portfolio project — not an
AUSTRAC-published formula. The engine recommends; the MLRO decides whether a suspicion is formed.
"""
import hashlib

import numpy as np
import pandas as pd

from .ref import (CUSTOMER_TYPES, CHANNELS, FOREIGN_TIERS, PRODUCTS, RISK_WEIGHTS_DEFAULT, TYPOLOGY_NAMES,
                  RISK_TIER_BOUNDS, UBO_ENTITIES, MLRO_NAME)

# ------------------------------------------------------------------ inputs ----
# key: (label, points, typology hint)
RED_FLAGS = {
    "structuring": ("Several cash or cash-equivalent payments just under AUD 10,000", 22, "Structuring / smurfing"),
    "rapid_movement": ("Funds paid into trust and out again within days, no matter progress", 18, "Rapid movement of funds"),
    "high_risk_jurisdiction": ("Transfer to or from a FATF-monitored jurisdiction", 18, "High-risk jurisdiction transfer"),
    "inconsistent_profile": ("Activity inconsistent with the client's known profile or means", 16, "Cash-intensive pattern"),
    "third_party": ("Payment from or to an unrelated third party", 14, None),
    "reluctant": ("Client reluctant to give ID, source-of-funds or ownership details", 14, None),
    "adverse_media": ("Adverse media linking the client or an owner to crime", 16, None),
    "complex_structure": ("Complex or opaque ownership with no clear commercial reason", 12, "Trade-based ML indicator"),
    "invoice_mismatch": ("Invoice values out of line with the goods or services", 14, "Trade-based ML indicator"),
    "refund_request": ("Matter abandoned; refund of trust money asked to a different account", 12, None),
    "pep": ("Client or beneficial owner is a politically exposed person (PEP)", 10, None),
    "sanctions_possible": ("Possible (unconfirmed) sanctions-list match", 20, None),
}
MITIGANTS = {
    "sof_verified": ("Source of funds verified with documents", 12),
    "rationale_documented": ("Clear commercial rationale documented", 8),
    "ubo_verified": ("All beneficial owners identified and verified", 6),
    "sow_verified": ("Source of wealth explained", 6),
}
# short labels for the pill selectors in the Simulator's case form
FLAG_SHORT = {"structuring": "Split cash under $10k", "rapid_movement": "In and out of trust fast",
              "high_risk_jurisdiction": "FATF-monitored jurisdiction", "inconsistent_profile": "Out of profile",
              "third_party": "Third-party payment", "reluctant": "Reluctant client", "adverse_media": "Adverse media",
              "complex_structure": "Opaque ownership", "invoice_mismatch": "Invoice mismatch",
              "refund_request": "Refund to another account", "pep": "PEP", "sanctions_possible": "Possible sanctions hit"}
MITIGANT_SHORT = {"sof_verified": "Source of funds verified", "rationale_documented": "Rationale documented",
                  "ubo_verified": "Owners verified", "sow_verified": "Source of wealth explained"}
HARD_SHORT = {"sanctions_confirmed": "Confirmed sanctions match", "terrorism": "Terrorism-financing indicators"}
HARD_TRIGGERS = {
    "sanctions_confirmed": "Confirmed sanctions-list match",
    "terrorism": "Indicators linked to terrorism financing",
}

# ------------------------------------------------------------------ bands ----
BANDS = [  # (lower bound, key, title, colour role)
    (0, "close", "Close — no further action", "ok"),
    (25, "edd", "Enhanced CDD — request information", "watch"),
    (45, "escalate", "Escalate to the MLRO", "alert"),
    (65, "smr", "Escalate to the MLRO with an SMR draft", "critical"),
]
BAND_KEYS = [b[1] for b in BANDS]

CLIENT_BASE_MAX = 25          # the client's 4-factor risk score contributes up to this many points
AMOUNT_POINTS = [(500_000, 8), (250_000, 6), (100_000, 4), (50_000, 2)]   # size of money moved
TTR_THRESHOLD = 10_000


def blank_case():
    return dict(ref="New case", alert_id=None, client="", client_id=None, client_type="Company",
                channel="Face-to-face", foreign_tier="Domestic only", product="Trust account services",
                state="NSW", typology=TYPOLOGY_NAMES[0], amount=0.0, n_txns=1, largest_cash=0.0,
                flags=[], mitigants=[], hard=[], opened=None, transactions=[])


# --------------------------------------------------------------- scoring ----
def client_risk_score(c):
    """The client's AUSTRAC 4-factor score (0-100), same weights as the KYC page, no noise."""
    w = RISK_WEIGHTS_DEFAULT
    return (CUSTOMER_TYPES[c["client_type"]][0] * w["type"] + CHANNELS[c["channel"]][0] * w["channel"]
            + FOREIGN_TIERS[c["foreign_tier"]][0] * w["foreign"] + PRODUCTS[c["product"]][0] * w["product"])


def client_tier(c):
    s = client_risk_score(c)
    lo, hi = RISK_TIER_BOUNDS
    return "Low" if s < lo else ("High" if s > hi else "Medium")


def _amount_points(amount):
    for lim, pts in AMOUNT_POINTS:
        if amount >= lim:
            return pts
    return 0


def contributions(c):
    """Every term of the score, largest first: [(label, points, kind)] where kind is client/amount/flag/mitigant."""
    rows = [("Client risk profile (4-factor model)", round(client_risk_score(c) / 100 * CLIENT_BASE_MAX, 1), "client")]
    ap = _amount_points(c.get("amount", 0))
    if ap:
        rows.append((f"Value moved (AUD {c['amount']:,.0f})", ap, "amount"))
    rows += [(RED_FLAGS[f][0], RED_FLAGS[f][1], "flag") for f in c.get("flags", []) if f in RED_FLAGS]
    rows += [(MITIGANTS[m][0], -MITIGANTS[m][1], "mitigant") for m in c.get("mitigants", []) if m in MITIGANTS]
    return sorted(rows, key=lambda r: -abs(r[1]))


def score(c):
    return float(np.clip(sum(p for _, p, _ in contributions(c)), 0, 100))


def band_for(s):
    b = BANDS[0]
    for lo, *rest in BANDS:
        if s >= lo:
            b = (lo, *rest)
    return b


def add_business_days(date, n):
    return pd.Timestamp(np.busday_offset(pd.Timestamp(date).date(), n, roll="forward"))


def assess(c, today):
    """Score + recommendation + regulatory clocks for a case, as of `today`."""
    s = score(c)
    _, key, title, tone = band_for(s)
    hard = [h for h in c.get("hard", []) if h in HARD_TRIGGERS]
    steps, clocks = [], []
    if "sanctions_confirmed" in hard:
        key, title, tone = "stop", "Stop — do not proceed with the matter", "critical"
        steps = ["Do not act on the instruction or move any funds.",
                 "Freeze the funds held and notify the Australian Sanctions Office (DFAT).",
                 f"Escalate to the MLRO ({MLRO_NAME}) today and prepare an SMR."]
    elif "terrorism" in hard:
        key, title, tone = "smr_tf", "Escalate now — terrorism-financing SMR", "critical"
        steps = [f"Escalate to the MLRO ({MLRO_NAME}) immediately.",
                 "If the MLRO forms a suspicion, the SMR is due within 24 hours.",
                 "Do not tip off the client or any third party."]
    elif key == "smr":
        steps = [f"Escalate to the MLRO ({MLRO_NAME}) with the SMR draft attached.",
                 "Put the matter on hold; do not release trust money pending the MLRO's decision.",
                 "Do not tip off the client that a report is being considered."]
    elif key == "escalate":
        steps = [f"Escalate to the MLRO ({MLRO_NAME}) with your case notes.",
                 "Request the missing verification (see what would change the decision).",
                 "Do not tip off the client that the matter is under review."]
    elif key == "edd":
        steps = ["Apply enhanced customer due diligence: request source-of-funds evidence and ownership documents.",
                 "Re-assess once the documents are in; escalate if they are not provided.",
                 "Record the rationale on the case file."]
    else:
        steps = ["Close the alert with a documented rationale.",
                 "No report required on the information available.",
                 "Keep the case record for 7 years."]

    if key in ("smr", "escalate", "stop"):
        clocks.append(("SMR due if the MLRO forms a suspicion today", add_business_days(today, 3), "3 business days"))
    if key == "smr_tf":
        clocks.append(("SMR due (terrorism financing)", pd.Timestamp(today) + pd.Timedelta(hours=24), "24 hours"))
    ttr = c.get("largest_cash", 0) >= TTR_THRESHOLD
    if ttr:
        clocks.append(("Threshold transaction report (physical cash ≥ AUD 10,000)", add_business_days(today, 10), "10 business days"))
    return dict(score=s, key=key, title=title, tone=tone, steps=steps, clocks=clocks, ttr=ttr, hard=hard,
                smr_recommended=key in ("smr", "smr_tf", "stop"), escalate=key in ("escalate", "smr", "smr_tf", "stop"),
                client_score=client_risk_score(c), client_tier=client_tier(c))


def what_if(c, today):
    """What would move the recommendation: each unverified mitigant as if verified, each observed red flag as
    if cleared. Only changes that move the score are returned, biggest first."""
    base = assess(c, today)
    out = []
    for m, (label, _) in MITIGANTS.items():
        if m not in c.get("mitigants", []):
            alt = assess({**c, "mitigants": list(c.get("mitigants", [])) + [m]}, today)
            out.append(("verify", label, alt["score"], alt["title"], alt["key"] != base["key"]))
    for f in c.get("flags", []):
        if f in RED_FLAGS:
            alt = assess({**c, "flags": [x for x in c["flags"] if x != f]}, today)
            out.append(("clear", RED_FLAGS[f][0], alt["score"], alt["title"], alt["key"] != base["key"]))
    out = [o for o in out if abs(o[2] - base["score"]) > 1e-9]
    return sorted(out, key=lambda o: (not o[4], o[2] if o[0] == "verify" else -o[2]))


def history_base_rate(M, typology, risk_tier):
    """How past alerts of the same typology on clients of the same risk tier ended — the precedent an MLRO asks about."""
    a = M["alerts"]
    sub = a[(a["typology"] == typology) & (a["risk_tier"] == risk_tier) & (a["disposition"] != "Open")
            & (a["disposition"] != "Under investigation")]
    n = len(sub)
    smr = int((sub["disposition"] == "Escalated to SMR").sum())
    return dict(n=n, smr=smr, rate=smr / n if n else float("nan"))


# ----------------------------------------------------------- from an alert ----
TYP_DEFAULT_FLAGS = {
    "Structuring / smurfing": ["structuring"],
    "Rapid movement of funds": ["rapid_movement", "third_party"],
    "High-risk jurisdiction transfer": ["high_risk_jurisdiction"],
    "Cash-intensive pattern": ["inconsistent_profile"],
    "Trade-based ML indicator": ["invoice_mismatch", "complex_structure"],
}
FOREIGN_PLACES = {k: v[2] for k, v in FOREIGN_TIERS.items()}


def _rng(key):
    return np.random.default_rng(int(hashlib.sha256(str(key).encode()).hexdigest()[:12], 16))


def synth_transactions(alert_id, typology, opened, foreign_tier):
    """Deterministic, typology-shaped trust-account movements behind an alert (synthetic)."""
    r = _rng(alert_id)
    opened = pd.Timestamp(opened)
    places = FOREIGN_PLACES.get(foreign_tier) or ["Kalvara"]
    tx = []
    if typology == "Structuring / smurfing":
        for i in range(int(r.integers(4, 7))):
            tx.append((opened - pd.Timedelta(days=int(r.integers(1, 14))), "Cash deposit to trust", float(r.integers(90, 99)) * 100 + float(r.integers(0, 99)), "In", "Branch counter"))
    elif typology == "Rapid movement of funds":
        amt = float(r.integers(18, 65)) * 10_000
        d0 = opened - pd.Timedelta(days=int(r.integers(4, 9)))
        tx.append((d0, "EFT into trust", amt, "In", "Unrelated company account"))
        tx.append((d0 + pd.Timedelta(days=int(r.integers(1, 4))), "EFT out of trust", round(amt * 0.97, -2), "Out", "Third-party account"))
    elif typology == "High-risk jurisdiction transfer":
        amt = float(r.integers(45, 400)) * 1_000
        place = places[int(r.integers(0, len(places)))]
        tx.append((opened - pd.Timedelta(days=int(r.integers(1, 6))), f"International transfer ({place})", amt, "In" if r.random() < 0.5 else "Out", place))
    elif typology == "Cash-intensive pattern":
        for i in range(int(r.integers(2, 5))):
            tx.append((opened - pd.Timedelta(days=int(r.integers(1, 20))), "Cash / bank cheque settlement", float(r.integers(12, 35)) * 1_000, "In", "Client"))
    else:  # trade-based
        for i in range(int(r.integers(2, 4))):
            tx.append((opened - pd.Timedelta(days=int(r.integers(2, 30))), "Invoice payment (related party)", float(r.integers(6, 25)) * 10_000, "Out", "Related-party entity"))
    return sorted(tx, key=lambda t: t[0])


def case_from_alert(M, alert_id):
    a = M["alerts"].set_index("alert_id").loc[alert_id]
    cust = M["cust"].set_index("customer_id").loc[a["customer_id"]]
    tx = synth_transactions(alert_id, a["typology"], a["opened"], cust["foreign_tier"])
    cash = [t[2] for t in tx if t[1].startswith("Cash")]
    flags = list(TYP_DEFAULT_FLAGS.get(a["typology"], []))
    if cust["foreign_tier"].startswith("Tier 3") and "high_risk_jurisdiction" not in flags:
        flags.append("high_risk_jurisdiction")
    # What the investigation found, consistent with how the alert was actually resolved (synthetic): cases that
    # became SMRs picked up further indicators; false positives were cleared by verification.
    r = _rng(f"{alert_id}-findings")
    mitigants = []
    if a["disposition"] == "Escalated to SMR":
        pool = [f for f in ("reluctant", "third_party", "refund_request", "adverse_media", "inconsistent_profile") if f not in flags]
        flags += list(r.choice(pool, size=2, replace=False))
    elif a["disposition"] == "Closed — false positive":
        mitigants = ["sof_verified", "rationale_documented"] + (["ubo_verified"] if r.random() < 0.5 else [])
    elif a["disposition"] == "Closed — no further action":
        mitigants = ["sof_verified"]
    return dict(ref=alert_id, alert_id=alert_id, client=cust["name"], client_id=a["customer_id"], client_type=cust["type"],
                channel=cust["channel"], foreign_tier=cust["foreign_tier"], product=cust["product"], state=cust["state"],
                typology=a["typology"], amount=float(sum(t[2] for t in tx)), n_txns=len(tx),
                largest_cash=float(max(cash) if cash else 0.0), flags=[str(f) for f in flags], mitigants=mitigants, hard=[],
                opened=a["opened"], analyst=a["analyst"], branch=a["branch"], disposition=a["disposition"], transactions=tx)


def _lc(t):
    """Lower-case the first letter for use mid-sentence, but keep acronyms (SMSF, PEP, AUD) as written."""
    return t if t[:2] == t[:2].upper() else t[0].lower() + t[1:]


def grounds_narrative(c, res):
    """A first-draft 'grounds for suspicion' in plain English, built from the case facts. The analyst edits it."""
    paras = []
    who = c.get("client") or "The client"
    tx = c.get("transactions") or []
    if tx:
        start, end = min(t[0] for t in tx), max(t[0] for t in tx)
        paras.append(f"Between {start:%d %B %Y} and {end:%d %B %Y}, {len(tx)} transaction(s) totalling AUD {sum(t[2] for t in tx):,.0f} "
                     f"passed through the firm's trust account in connection with {who}'s {c['product'].lower()} matter.")
    else:
        paras.append(f"Transactions totalling AUD {c.get('amount', 0):,.0f} were identified in connection with {who}'s {c['product'].lower()} matter.")
    obs = [_lc(RED_FLAGS[f][0].rstrip(".")) for f in c.get("flags", []) if f in RED_FLAGS]
    if obs:
        paras.append("The following indicators were observed: " + "; ".join(obs) + ".")
    hard = [_lc(HARD_TRIGGERS[h]) for h in c.get("hard", []) if h in HARD_TRIGGERS]
    if hard:
        paras.append("In addition: " + "; ".join(hard) + ".")
    missing = [_lc(MITIGANTS[m][0]) for m in MITIGANTS if m not in c.get("mitigants", [])]
    if missing:
        paras.append("At the time of this report the firm has not been able to confirm the following: " + "; ".join(missing) + ".")
    paras.append(f"The client is rated {res['client_tier']} risk under the firm's AUSTRAC 4-factor model "
                 f"({_lc(c['client_type'])}, {_lc(c['channel'])}, {_lc(c['foreign_tier'].split(' — ')[0])} foreign dimension). "
                 f"Taken together, the activity has no apparent lawful commercial purpose that the firm has been able to establish.")
    return paras


def beneficial_owners(client):
    return UBO_ENTITIES.get(client, [])
