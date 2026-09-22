"""Escalation register — analyst → MLRO hand-offs and the MLRO's decision on each.

Two sources, one table:
  * history: every SMR in the model began as an escalation the MLRO accepted (escalated date, analyst,
    lodgement status all come from core.model), so past escalations reconcile with the SMR register;
  * this session: cases the user escalates from the Simulator's case-decision mode, which the MLRO can then
    decide on the Triage page (form a suspicion → SMR due in 3 business days / 24 hours, return for more
    information, or close with no suspicion).
Session escalations live in st.session_state (a portfolio demo has no database); the functions here are pure.
"""
import pandas as pd

from . import case as C
from .ref import MLRO_NAME

STATUS_AWAITING = "Awaiting MLRO decision"
STATUS_SUSPICION = "Suspicion formed — SMR to lodge"
STATUS_RETURNED = "Returned for more information"
STATUS_CLOSED = "Closed — no suspicion formed"
DECISIONS = {"suspicion": STATUS_SUSPICION, "return": STATUS_RETURNED, "close": STATUS_CLOSED}


def new_escalation(existing, case, today, analyst, rationale=""):
    """A new session escalation record (does not mutate `existing`)."""
    res = C.assess(case, today)
    n = len(existing) + 1
    return dict(esc_id=f"ESC-S{n:03d}", source="This session", alert_id=case.get("alert_id") or "Manual",
                client=case.get("client") or "—", typology=case.get("typology"), score=round(res["score"]),
                recommendation=res["title"], analyst=analyst, mlro=MLRO_NAME, escalated=pd.Timestamp(today),
                status=STATUS_AWAITING, decided=None, smr_due=None, rationale=rationale.strip(),
                terrorism="terrorism" in case.get("hard", []), case=dict(case))


def decide(record, decision, today):
    """Apply an MLRO decision to a session escalation record (returns an updated copy)."""
    r = dict(record)
    r["status"] = DECISIONS[decision]
    r["decided"] = pd.Timestamp(today)
    if decision == "suspicion":
        r["smr_due"] = (pd.Timestamp(today) + pd.Timedelta(hours=24)) if r.get("terrorism") else C.add_business_days(today, 3)
    else:
        r["smr_due"] = None
    return r


def history(M):
    """Past escalations reconstructed from the SMR register — each one the MLRO accepted."""
    s = M["smrs"]
    lodged = {"Submitted": "SMR lodged", "Acknowledged": "SMR lodged · acknowledged", "Draft": STATUS_SUSPICION}
    df = pd.DataFrame(dict(
        esc_id=["ESC-" + x.replace("SMR-", "") for x in s["smr_id"]], source="History", alert_id=s["alert_id"],
        client=s["customer"], typology=s["typology"], analyst=s["analyst"], mlro=MLRO_NAME, escalated=s["escalated"],
        status=s["status"].map(lodged), decided=s["escalated"],
        smr_due=[C.add_business_days(d, 3) for d in s["escalated"]], smr_id=s["smr_id"], submitted=s["submitted"]))
    return df.sort_values("escalated", ascending=False).reset_index(drop=True)


def register(M, session_records):
    """Session escalations (newest first) on top of the history."""
    cols = ["esc_id", "source", "alert_id", "client", "typology", "analyst", "escalated", "status", "smr_due"]
    ses = pd.DataFrame([{k: r.get(k) for k in cols} for r in reversed(session_records)], columns=cols)
    return pd.concat([ses, history(M)[cols]], ignore_index=True)
