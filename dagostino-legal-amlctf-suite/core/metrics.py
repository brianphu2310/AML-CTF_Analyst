"""KPI and analysis functions computed from the model for any reporting period."""
import numpy as np
import pandas as pd

from .ref import AS_OF, START, TYPOLOGY_NAMES, ANALYSTS, SLA_DAYS, AU_STATE_NAMES
from .period import Period, month_weights, flow, stock_at, has_data, months_in, delta

ANALYST_SHORT = [a["short"] for a in ANALYSTS]


# ------------------------------------------------------------------ flows -----
def fin_sum(M, p):
    return flow(M["fin"], p, list(M["fin"].columns)) if has_data(p) else None


def alerts_in(M, p):
    a = M["alerts"]
    return a[(a["opened"] >= p.start) & (a["opened"] <= p.end)].copy()


def smrs_in(M, p, date_col="submitted"):
    s = M["smrs"]
    d = s[date_col]
    return s[(d.notna()) & (d >= p.start) & (d <= p.end)].copy()


def customers_onboarded_in(M, p):
    c = M["cust"]
    return c[(c["onboarded"] >= p.start) & (c["onboarded"] <= p.end)].copy()


# ------------------------------------------------------------ headline KPIs ---
def headline(M, cur, cmp):
    fc, fp = fin_sum(M, cur), fin_sum(M, cmp) if cmp else None
    stk = M["stock"]
    active_c = stock_at(stk, "customers_active", cur.end)
    active_p = stock_at(stk, "customers_active", cmp.end) if cmp and has_data(cmp) else None
    active_alerts = stock_at(stk, "active_alerts", cur.end)
    active_alerts_p = stock_at(stk, "active_alerts", cmp.end) if cmp and has_data(cmp) else None
    open_inv = stock_at(stk, "open_investigations", cur.end)
    open_inv_p = stock_at(stk, "open_investigations", cmp.end) if cmp and has_data(cmp) else None
    overdue = stock_at(stk, "overdue_reviews", cur.end)
    overdue_p = stock_at(stk, "overdue_reviews", cmp.end) if cmp and has_data(cmp) else None
    high_c = stock_at(stk, "customers_high", cur.end)
    high_p = stock_at(stk, "customers_high", cmp.end) if cmp and has_data(cmp) else None

    fy_start = pd.Timestamp(year=(cur.end.year if cur.end.month >= 7 else cur.end.year - 1), month=7, day=1)
    ytd = Period(max(fy_start, START), cur.end, "FY-to-date")
    smrs_ytd = len(smrs_in(M, ytd)) if has_data(ytd) else 0

    typ_counts = {t: fc[f"alerts_{t}"] for t in TYPOLOGY_NAMES} if fc is not None else {}
    return dict(fc=fc, fp=fp, active_customers=active_c, active_customers_p=active_p, active_alerts=active_alerts,
                active_alerts_p=active_alerts_p, open_investigations=open_inv, open_investigations_p=open_inv_p,
                overdue_reviews=overdue, overdue_reviews_p=overdue_p, high_risk_customers=high_c, high_risk_customers_p=high_p,
                smrs_ytd=smrs_ytd, typ_counts=typ_counts)


def monthly(M, col, end, n=12, source="fin"):
    df = M[source]
    m1 = pd.Timestamp(end).replace(day=1)
    s = df[col].loc[m1 - pd.DateOffset(months=n - 1):m1]
    return s[~s.isna()]


def spark(M, col, end, n=12, source="fin"):
    s = monthly(M, col, end, n, source)
    return s.values.tolist() if len(s) > 1 else [0, 0]


# --------------------------------------------------------------- KYC / risk ---
def risk_tier_breakdown(M, date):
    stk = M["stock"]
    return {t: stock_at(stk, f"customers_{t.lower()}", date) for t in ("Low", "Medium", "High")}


def risk_factor_table():
    from .ref import CUSTOMER_TYPES, CHANNELS, FOREIGN_TIERS, PRODUCTS
    return dict(type=CUSTOMER_TYPES, channel=CHANNELS, foreign=FOREIGN_TIERS, product=PRODUCTS)


def onboarding_funnel(M, p):
    f = fin_sum(M, p)
    if f is None:
        return [0, 0, 0, 0]
    return [max(int(round(f[c])), 1) for c in ("kyc_applications", "kyc_id_verified", "kyc_risk_assessed", "kyc_approved")]


def overdue_customers(M, date):
    c = M["cust"]
    return c[(c["onboarded"] <= date) & (c["next_review_due"] < date)].copy()


# --------------------------------------------------------- transaction monitoring ---
def typology_table(M, p):
    f = fin_sum(M, p)
    a = alerts_in(M, p)
    rows = []
    for t in TYPOLOGY_NAMES:
        sub = a[a["typology"] == t]
        opened = int(f[f"alerts_{t}"]) if f is not None else len(sub)
        fp = int((sub["disposition"] == "Closed — false positive").sum())
        closed = sub[sub["disposition"].str.startswith("Closed")]
        fp_rate = fp / len(closed) if len(closed) else np.nan
        rows.append(dict(typology=t, alerts=opened, false_positives=fp, fp_rate=fp_rate,
                         escalated=int((sub["disposition"] == "Escalated to SMR").sum()), avg_hours=sub["hours"].mean()))
    return pd.DataFrame(rows)


# ------------------------------------------------------------- alert triage ---
def alert_queue(M, date):
    a = M["alerts"]
    return a[(a["opened"] <= date) & (a["closed"].isna() | (a["closed"] > date))].copy()


def sla_table(M, p):
    a = alerts_in(M, p)
    closed = a[a["closed"].notna()]
    breach = closed["sla_breach"].mean() if len(closed) else np.nan
    return dict(closed=len(closed), breach_rate=breach, avg_days=(closed["closed"] - closed["opened"]).dt.days.mean() if len(closed) else np.nan)


def disposition_table(M, p):
    a = alerts_in(M, p)
    return a["disposition"].value_counts().reindex(
        ["Open", "Under investigation", "Escalated to SMR", "Closed — false positive", "Closed — no further action"]).fillna(0).astype(int)


# ------------------------------------------------------------------ SMR -----
def smr_register(M, p):
    return smrs_in(M, p, "escalated")


def austrac_status_table(M, date):
    s = M["smrs"]
    live = s[s["escalated"] <= date]
    return live["status"].value_counts().reindex(["Draft", "Submitted", "Acknowledged"]).fillna(0).astype(int)


# --------------------------------------------------------------------- team ---
def analyst_table(M, p):
    a = alerts_in(M, p)
    rows = []
    for an in ANALYSTS:
        sub = a[a["analyst"] == an["short"]]
        closed = sub[sub["closed"].notna()]
        rows.append(dict(analyst=an["name"], short=an["short"], role=an["role"], branch=an["branch"], capacity=an["capacity"],
                         alerts=len(sub), hours=sub["hours"].sum(), closed=len(closed),
                         sla_breach_rate=closed["sla_breach"].mean() if len(closed) else np.nan,
                         escalated=int((sub["disposition"] == "Escalated to SMR").sum())))
    df = pd.DataFrame(rows)
    df["utilisation"] = df["alerts"] / (df["capacity"].replace(0, np.nan) * max(p.days / 30.4, 0.1))
    return df


# ------------------------------------------------------------ reconciliation --
def customers_screened_total(M, p):
    f = fin_sum(M, p)
    return float(f["screenings"]) if f is not None else 0.0


# ----------------------------------------------------- pipeline (Overview funnel) ---
def pipeline_flow(M, p, alerts=None):
    """Alert pipeline stage counts for the period, for the Overview pipeline visual.

    Staged funnel — each alert is counted at every stage it reached:
      Alert generated -> L1 triage (everything not still awaiting triage)
      -> L2 investigation (triage did not discount it as a false positive)
      -> MLRO review (investigation formed a suspicion and escalated it)
      -> SMR lodged with AUSTRAC (status Submitted or Acknowledged).
    Also returns the drop-out at each stage and the average escalation-to-lodgement lag
    (same calendar-day definition as the SMR Register page)."""
    a = alerts if alerts is not None else alerts_in(M, p)
    disp = a["disposition"].value_counts()
    total = len(a)
    open_n = int(disp.get("Open", 0))
    uinv_n = int(disp.get("Under investigation", 0))
    esc_n = int(disp.get("Escalated to SMR", 0))
    fp_n = int(disp.get("Closed — false positive", 0))
    nfa_n = int(disp.get("Closed — no further action", 0))
    triaged_n = total - open_n
    by_typology = {t: int((a["typology"] == t).sum()) for t in TYPOLOGY_NAMES}
    s = M["smrs"]
    s = s[s["alert_id"].isin(a["alert_id"])]
    lodged = s[s["status"].isin(["Submitted", "Acknowledged"])]
    lag = (lodged["submitted"] - lodged["escalated"]).dt.days.dropna()
    return dict(total=total, open=open_n, triaged=triaged_n, investigated=triaged_n, under_investigation=uinv_n,
                escalated=esc_n, closed_fp=fp_n, closed_nfa=nfa_n, by_typology=by_typology,
                l2=esc_n + nfa_n + uinv_n, mlro=esc_n, smr_lodged=len(lodged),
                smr_drafting=max(esc_n - len(lodged), 0),
                smr_lag_days=float(lag.mean()) if len(lag) else float("nan"))


# ----------------------------------------------------- state / grouping (Overview) ---
GROUP_DIMS = {"State": "state", "Risk Tier": "risk_tier", "Typology": "typology", "Channel": "channel"}


def group_metrics_table(M, p, dim, alerts_filtered=None):
    """Clients/Alerts/SMRs/%SMR/Closed/%Closed by the selected grouping dimension, with a bold Total row.
    'Typology' is an alert-level attribute only (no client record carries one), so its "Clients" column
    is the count of distinct clients touched by that typology's alerts rather than a client-book count."""
    col = GROUP_DIMS.get(dim, "state")
    c = M["cust"]
    active = c[c["onboarded"] <= p.end]
    a = alerts_filtered if alerts_filtered is not None else alerts_in(M, p)
    if dim == "State":
        groups = AU_STATE_NAMES
    elif dim == "Typology":
        groups = TYPOLOGY_NAMES
    else:
        groups = sorted(active[col].dropna().unique())
    rows = []
    for g in groups:
        a_g = a[a[col] == g]
        cust_n = a_g["customer_id"].nunique() if dim == "Typology" else int((active[col] == g).sum())
        alerts_n = len(a_g)
        smr_n = int((a_g["disposition"] == "Escalated to SMR").sum())
        closed_n = int(a_g["disposition"].astype(str).str.startswith("Closed").sum())
        rows.append(dict(group=g, customers=cust_n, alerts=alerts_n, smrs=smr_n,
                         smr_rate=smr_n / alerts_n if alerts_n else np.nan,
                         closed=closed_n, closed_rate=closed_n / alerts_n if alerts_n else np.nan))
    df = pd.DataFrame(rows, columns=["group", "customers", "alerts", "smrs", "smr_rate", "closed", "closed_rate"])
    alerts_tot = max(int(df["alerts"].sum()), 1) if len(df) else 1
    tot = dict(group="Total", customers=int(df["customers"].sum()) if len(df) else 0, alerts=int(df["alerts"].sum()) if len(df) else 0,
              smrs=int(df["smrs"].sum()) if len(df) else 0, smr_rate=(df["smrs"].sum() / alerts_tot) if len(df) else np.nan,
              closed=int(df["closed"].sum()) if len(df) else 0, closed_rate=(df["closed"].sum() / alerts_tot) if len(df) else np.nan)
    return pd.concat([df, pd.DataFrame([tot])], ignore_index=True)
