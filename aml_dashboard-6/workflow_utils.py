"""
workflow_utils.py
Shared workflow state machine + in-session persistence + audit logging for
the full AML lifecycle: Alert Generation -> Alert Triage -> Investigation ->
Escalation -> Senior Review -> SMR Assessment -> SMR Submission -> Post-SMR
Monitoring -> Periodic Review / Remediation -> Record Keeping.

This is a demo app with no backing database transaction layer, so mutable
workflow state (alert dispositions, case status changes, review outcomes,
audit trail) lives in `st.session_state`, seeded once from the synthetic
data in db_utils.py. Every action that changes state also appends an entry
to the audit trail so the Record Keeping / Audit Trail page has a real,
consistent log to show - this mirrors the "who did what, when, and why"
record-keeping obligation under an AML/CTF Program.
"""

from __future__ import annotations
from datetime import datetime
import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------
# PIPELINE CONSTANTS
# --------------------------------------------------------------------------
CASE_STATUSES = [
    "Open",
    "Under Investigation",
    "Escalated - Senior Review",
    "Pending SMR Lodgement",
    "SMR Lodged",
    "Post-SMR Monitoring",
    "Closed - No Action",
    "Closed - Restricted / Exited",
]

ALERT_DISPOSITIONS = ["New", "False Positive", "Requires Investigation", "Escalated to Case"]

SENIOR_DECISIONS = ["Close Case", "Continue Monitoring", "Restrict / Exit Relationship"]

REVIEW_INTERVAL_MONTHS = {"Low": 24, "Medium": 12, "High": 6, "Critical": 3}

STAGE_TO_PAGE = {
    "Client onboarding": "7_New_Client_Onboarding.py",
    "KYC / Identity Verification": "7_New_Client_Onboarding.py",
    "KYB": "6_Business_KYC.py",
    "Beneficial Ownership / UBO": "5_UBO_Network.py",
    "PEP Screening": "2_Screening.py",
    "Sanctions Screening": "2_Screening.py",
    "Adverse Media Screening": "2_Screening.py",
    "Customer Risk Assessment": "1_Customer_Risk.py",
    "CDD": "7_New_Client_Onboarding.py",
    "EDD": "7_New_Client_Onboarding.py",
    "Customer Approval / Onboarding Decision": "7_New_Client_Onboarding.py",
    "Ongoing Monitoring": "1_Customer_Risk.py",
    "Transaction Monitoring": "3_Transaction_Monitoring.py",
    "Alert Generation": "8_Alerts_Triage.py",
    "Alert Triage": "8_Alerts_Triage.py",
    "Investigation": "4_Case_Management_SAR.py",
    "Source of Funds / Source of Wealth Review": "4_Case_Management_SAR.py",
    "EDD / Additional Information": "4_Case_Management_SAR.py",
    "Escalation": "4_Case_Management_SAR.py",
    "Senior Review / Decision": "4_Case_Management_SAR.py",
    "SMR Assessment": "4_Case_Management_SAR.py",
    "SMR Preparation": "4_Case_Management_SAR.py",
    "SMR Submission": "4_Case_Management_SAR.py",
    "Post-SMR / Ongoing Monitoring": "4_Case_Management_SAR.py",
    "Periodic Review / Remediation": "9_Periodic_Review.py",
    "Record Keeping / Audit Trail": "10_Audit_Trail.py",
}


def init_state(key: str, loader):
    """Seed st.session_state[key] once from `loader()` (a DataFrame or list),
    then return the live mutable copy on every subsequent call."""
    if key not in st.session_state:
        val = loader()
        st.session_state[key] = val.copy() if isinstance(val, pd.DataFrame) else list(val)
    return st.session_state[key]


def log_audit(action: str, entity_type: str, entity_id: str, detail: str, actor: str = "Current User"):
    """Append one record-keeping entry to the audit trail."""
    if "audit_log_live" not in st.session_state:
        st.session_state["audit_log_live"] = []
    st.session_state["audit_log_live"].append({
        "timestamp": datetime.now(),
        "actor": actor,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "detail": detail,
    })


def full_audit_log(seed_df: pd.DataFrame) -> pd.DataFrame:
    """Seeded historical entries + anything logged live this session, newest first."""
    live = pd.DataFrame(st.session_state.get("audit_log_live", []))
    if live.empty:
        combined = seed_df
    else:
        combined = pd.concat([seed_df, live], ignore_index=True)
    return combined.sort_values("timestamp", ascending=False).reset_index(drop=True)


def review_due_date(onboarding_date, risk_level: str) -> pd.Timestamp:
    months = REVIEW_INTERVAL_MONTHS.get(risk_level, 12)
    return pd.Timestamp(onboarding_date) + pd.DateOffset(months=months)


def status_pill_html(status: str) -> str:
    """Map any workflow status string to a themed pill class."""
    s = status.lower()
    if "closed" in s and "restrict" in s:
        cls = "pill-critical"
    elif "closed" in s:
        cls = "pill-low"
    elif "smr lodged" in s or "post-smr" in s:
        cls = "pill-info"
    elif "pending" in s or "escalat" in s:
        cls = "pill-high"
    elif "investigation" in s:
        cls = "pill-medium"
    else:
        cls = "pill-info"
    return f'<span class="pill {cls}">{status}</span>'
