"""Single source of truth. Everything the dashboards show is derived from this deterministic model:

    customer onboarding (4-factor risk score) → risk tier → periodic-review schedule
    typology base rates × active/high-risk customer base → monthly alerts → analyst triage → disposition
    escalated alerts → SMR register → AUSTRAC lodgement tracking

A fixed random seed makes every run identical, so the numbers on every page — and in the README's
"Example findings" — always reconcile to the same synthetic population.
"""
import numpy as np
import pandas as pd

from .ref import (AS_OF, START, ANALYSTS, BRANCHES, CUSTOMER_TYPES, CHANNELS, FOREIGN_TIERS, PRODUCTS,
                  RISK_WEIGHTS_DEFAULT, RISK_TIER_BOUNDS, TYPOLOGIES, TYPOLOGY_NAMES, NAMED_CUSTOMERS,
                  SLA_DAYS, AUSTRAC_STATUSES, AU_STATES)

SEED = 830115
REVIEW_CYCLE_MONTHS = {"Low": 36, "Medium": 18, "High": 12}
ESCALATE_SHARE = 0.58            # of true-positive alerts, share that becomes an SMR (rest closed "no further action")
GROWTH = 0.55                    # customer-base growth over the history window (index units, applied across T months)
_FIRST = ["Amelia", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Mia", "Lucas", "Grace", "Henry", "Chloe", "Jack",
          "Isla", "Leo", "Zoe", "Ryan", "Nina", "Owen", "Freya", "Cole", "Priya", "Wei", "Santiago", "Ines"]
_LAST = ["Whitfield", "Marlowe", "Castellan", "Dupree", "Sarantos", "Voss", "Halloran", "Okafor", "Marchetti",
         "Bergqvist", "Tanaka", "Nkosi", "Delacroix", "Rourke", "Pemberton", "Souza", "Lindqvist", "Abernathy"]
_CO_SUFFIX = ["Holdings Pty Ltd", "Group Pty Ltd", "Pty Ltd", "Nominees Pty Ltd", "Ventures Pty Ltd", "Capital Pty Ltd", "Trading Co."]
_CO_WORD = ["Ashfield", "Coral Bay", "Northgate", "Silverline", "Eastwind", "Harbour", "Redgum", "Bluepeak", "Fernvale",
            "Marlowe", "Kestrel", "Brightwater", "Stonecroft", "Ironbark", "Amberfield", "Cedarview"]


def fy_start_year(ts):
    return ts.year if ts.month >= 7 else ts.year - 1


def _risk_score(rng, ctype, channel, ftier, product, weights):
    t = CUSTOMER_TYPES[ctype][0]; c = CHANNELS[channel][0]; f = FOREIGN_TIERS[ftier][0]; p = PRODUCTS[product][0]
    raw = t * weights["type"] + c * weights["channel"] + f * weights["foreign"] + p * weights["product"]
    noise = rng.normal(0, 4.0)
    return float(np.clip(raw + noise, 1, 100))


def _tier(score, bounds=RISK_TIER_BOUNDS):
    lo, hi = bounds
    return "Low" if score < lo else ("High" if score > hi else "Medium")


def _review_dates(rng, onboarded, tier):
    """Periodic-review schedule for one customer. Most reviews happen on time; a share of customers whose
    review has already come due once are genuinely behind (the analyst backlog the Overview page reports)."""
    cycle = REVIEW_CYCLE_MONTHS[tier]
    last = onboarded
    nxt = onboarded + pd.DateOffset(months=cycle)
    n_cycles = 0
    while nxt <= AS_OF:
        last = nxt
        nxt = nxt + pd.DateOffset(months=cycle)
        n_cycles += 1
    if n_cycles > 0 and rng.random() < 0.22:                 # genuinely overdue: the due review was never completed
        nxt = last
        last = last - pd.DateOffset(months=cycle)
        return last, nxt
    jitter = int(rng.integers(-10, 10))
    return last, nxt + pd.Timedelta(days=jitter)


def _company_name(rng):
    return f"{rng.choice(_CO_WORD)} {rng.choice(_CO_SUFFIX)}"


def _person_name(rng):
    return f"{rng.choice(_FIRST)} {rng.choice(_LAST)}"


def build_model():
    rng = np.random.default_rng(SEED)
    months = pd.date_range(START, AS_OF.replace(day=1), freq="MS")
    T = len(months)
    weights = dict(RISK_WEIGHTS_DEFAULT)
    branches = [b["name"] for b in BRANCHES]
    branch_w = np.ones(len(branches)) / len(branches)

    # ---------------- customers ----------------
    types_k, types_p = list(CUSTOMER_TYPES), np.array([v[1] for v in CUSTOMER_TYPES.values()])
    chan_k, chan_p = list(CHANNELS), np.array([v[1] for v in CHANNELS.values()])
    ftier_k, ftier_p = list(FOREIGN_TIERS), np.array([v[1] for v in FOREIGN_TIERS.values()])
    prod_k, prod_p = list(PRODUCTS), np.array([v[1] for v in PRODUCTS.values()])

    rows = []
    for name, ctype, channel, ftier, product, onboarded in NAMED_CUSTOMERS:
        rows.append(dict(name=name, type=ctype, channel=channel, foreign_tier=ftier, product=product,
                         onboarded=pd.Timestamp(onboarded), branch=str(rng.choice(branches)), named=True))

    # monthly onboarding volume grows mildly over the window
    tt = np.arange(T)
    base_rate = 7.4 + GROWTH * tt / max(T - 1, 1) * 7.4
    for t in range(T):
        m0 = months[t]
        last = (m0 + pd.offsets.MonthEnd(0)).day if m0 < AS_OF.replace(day=1) else AS_OF.day
        n = int(rng.poisson(base_rate[t] * (last / m0.days_in_month)))
        for _ in range(n):
            ctype = str(rng.choice(types_k, p=types_p / types_p.sum()))
            is_company = ctype in ("Company", "Trust", "Partnership", "Foreign Entity", "SMSF")
            nm = _company_name(rng) if is_company else _person_name(rng)
            channel = str(rng.choice(chan_k, p=chan_p / chan_p.sum()))
            ftier = str(rng.choice(ftier_k, p=ftier_p / ftier_p.sum()))
            product = str(rng.choice(prod_k, p=prod_p / prod_p.sum()))
            day = int(rng.integers(0, last))
            rows.append(dict(name=nm, type=ctype, channel=channel, foreign_tier=ftier, product=product,
                             onboarded=m0 + pd.Timedelta(days=day), branch=str(rng.choice(branches, p=branch_w)), named=False))
    cust = pd.DataFrame(rows).sort_values("onboarded", kind="stable").reset_index(drop=True)
    cust["customer_id"] = [f"CL-{i + 1:05d}" for i in range(len(cust))]
    cust["risk_score"] = [_risk_score(rng, r.type, r.channel, r.foreign_tier, r.product, weights) for r in cust.itertuples()]
    cust["risk_tier"] = cust["risk_score"].map(_tier)
    rev = [_review_dates(rng, r.onboarded, r.risk_tier) for r in cust.itertuples()]
    cust["last_review"], cust["next_review_due"] = zip(*rev)
    cust["review_overdue"] = cust["next_review_due"] < AS_OF
    cust["fatf_jurisdiction"] = cust["foreign_tier"].map(lambda f: "; ".join(FOREIGN_TIERS[f][2][:1]) if FOREIGN_TIERS[f][2] else "—")

    # Registered state/territory — an independent RNG stream (not `rng`) so it never shifts the existing
    # onboarding/risk/alert draw sequence below.
    rng_state = np.random.default_rng(SEED + 7919)
    state_k, state_p = list(AU_STATES), np.array(list(AU_STATES.values()))
    cust["state"] = rng_state.choice(state_k, size=len(cust), p=state_p / state_p.sum())

    # ---------------- alerts ----------------
    active_by_month = np.array([(cust["onboarded"] <= (m + pd.offsets.MonthEnd(0))).sum() for m in months])
    tier_mult = {"Low": 0.55, "Medium": 1.15, "High": 2.35}
    cust_weight = cust["risk_tier"].map(tier_mult).values
    analyst_names = [a["short"] for a in ANALYSTS]
    analyst_start = {a["short"]: pd.Timestamp(a["start"]) for a in ANALYSTS}
    analyst_cap = {a["short"]: a["capacity"] for a in ANALYSTS}

    arows = []
    for t in range(T):
        m0 = months[t]
        last = (m0 + pd.offsets.MonthEnd(0)).day if m0 < AS_OF.replace(day=1) else AS_OF.day
        frac = last / m0.days_in_month
        pool = cust[cust["onboarded"] <= m0 + pd.offsets.MonthEnd(0)]
        if pool.empty:
            continue
        w = pool["risk_tier"].map(tier_mult).values
        w = w / w.sum()
        for typ, spec in TYPOLOGIES.items():
            lam = spec["base_rate"] * active_by_month[t] * frac
            n = int(rng.poisson(max(lam, 0.05)))
            if n == 0:
                continue
            idx = rng.choice(len(pool), size=n, p=w)
            avail = [a for a in analyst_names if analyst_start[a] <= m0]
            avail = avail or analyst_names
            acap = np.array([analyst_cap[a] for a in avail], float); acap = acap / acap.sum()
            for i in range(n):
                cust_row = pool.iloc[idx[i]]
                day_lo = (cust_row["onboarded"] - m0).days if cust_row["onboarded"] > m0 else 0
                day_lo = int(np.clip(day_lo, 0, last - 1))
                day = int(rng.integers(day_lo, last))
                opened = m0 + pd.Timedelta(days=day)
                analyst = str(rng.choice(avail, p=acap))
                hours = float(np.clip(rng.normal(spec["hours"], spec["hours"] * 0.22), 0.5, 8.0))
                is_fp = rng.random() < spec["fp_rate"]
                age_days = (AS_OF - opened).days
                if age_days < 3:
                    disp, closed, sla_breach = "Open", pd.NaT, False
                elif age_days < 12 and rng.random() < 0.35:
                    disp, closed, sla_breach = "Under investigation", pd.NaT, age_days > SLA_DAYS
                else:
                    turnaround = int(np.clip(rng.normal(6.5, 3.5), 1, 30))
                    closed = min(opened + pd.Timedelta(days=turnaround), AS_OF)
                    sla_breach = turnaround > SLA_DAYS
                    if is_fp:
                        disp = "Closed — false positive"
                    else:
                        disp = "Escalated to SMR" if rng.random() < ESCALATE_SHARE else "Closed — no further action"
                arows.append(dict(alert_id=None, opened=opened, typology=typ, customer=cust_row["name"], customer_id=cust_row["customer_id"],
                                  risk_tier=cust_row["risk_tier"], branch=cust_row["branch"], state=cust_row["state"], channel=cust_row["channel"],
                                  analyst=analyst, hours=round(hours, 2), disposition=disp, closed=closed, sla_breach=sla_breach, is_false_positive=is_fp))
    alerts = pd.DataFrame(arows).sort_values("opened", kind="stable").reset_index(drop=True)
    alerts["alert_id"] = [f"ALT-{2025000 + i}" for i in range(len(alerts))]

    # ---------------- SMR register ----------------
    esc = alerts[alerts["disposition"] == "Escalated to SMR"].copy()
    srows = []
    for i, r in enumerate(esc.itertuples()):
        lag = int(np.clip(rng.normal(3.5, 1.5), 1, 10))
        submit = r.opened + pd.Timedelta(days=lag) if pd.isna(r.closed) else r.closed + pd.Timedelta(days=lag)
        submit = min(submit, AS_OF + pd.Timedelta(days=2))
        if submit > AS_OF:
            status, ack = "Draft", pd.NaT
        else:
            ack_lag = int(np.clip(rng.normal(4, 2), 1, 12))
            ack_date = submit + pd.Timedelta(days=ack_lag)
            if ack_date <= AS_OF:
                status, ack = "Acknowledged", ack_date
            else:
                status, ack = "Submitted", pd.NaT
        srows.append(dict(smr_id=f"SMR-{2025100 + i}", alert_id=r.alert_id, customer=r.customer, customer_id=r.customer_id,
                          typology=r.typology, analyst=r.analyst, branch=r.branch, escalated=r.opened,
                          submitted=submit if status != "Draft" else pd.NaT, status=status, acknowledged=ack))
    smrs = pd.DataFrame(srows).sort_values("escalated", kind="stable").reset_index(drop=True)

    # ---------------- monthly flow frame (screening / KYC pipeline / alerts / hours) ----------------
    fin = pd.DataFrame(index=months)
    onboarded_m = np.array([((cust["onboarded"] >= m) & (cust["onboarded"] <= m + pd.offsets.MonthEnd(0))).sum() for m in months], float)
    fin["customers_onboarded"] = onboarded_m
    fin["kyc_applications"] = onboarded_m / 0.62
    fin["kyc_id_verified"] = onboarded_m / 0.78
    fin["kyc_risk_assessed"] = onboarded_m / 0.90
    fin["kyc_approved"] = onboarded_m
    fin["screenings"] = onboarded_m + np.array([((cust["last_review"] >= m) & (cust["last_review"] <= m + pd.offsets.MonthEnd(0))).sum() for m in months], float)
    for typ in TYPOLOGY_NAMES:
        fin[f"alerts_{typ}"] = np.array([((alerts["opened"] >= m) & (alerts["opened"] <= m + pd.offsets.MonthEnd(0)) & (alerts["typology"] == typ)).sum() for m in months], float)
    fin["alerts_opened"] = fin[[f"alerts_{t}" for t in TYPOLOGY_NAMES]].sum(axis=1)
    fin["alerts_closed_fp"] = np.array([((alerts["closed"] >= m) & (alerts["closed"] <= m + pd.offsets.MonthEnd(0)) & (alerts["disposition"] == "Closed — false positive")).sum() for m in months], float)
    fin["alerts_escalated"] = np.array([((alerts["opened"] >= m) & (alerts["opened"] <= m + pd.offsets.MonthEnd(0)) & (alerts["disposition"] == "Escalated to SMR")).sum() for m in months], float)
    fin["smrs_filed"] = np.array([((smrs["submitted"] >= m) & (smrs["submitted"] <= m + pd.offsets.MonthEnd(0))).sum() for m in months], float)
    fin["analyst_hours"] = np.array([((alerts["opened"] >= m) & (alerts["opened"] <= m + pd.offsets.MonthEnd(0))).astype(float) @ alerts["hours"].where((alerts["opened"] >= m) & (alerts["opened"] <= m + pd.offsets.MonthEnd(0)), 0.0) for m in months])
    # (the loop-based hours calc above is O(T*N); fine at this scale, replaced with a fast groupby for clarity/perf below)
    hrs_by_month = alerts.assign(_m=alerts["opened"].values.astype("datetime64[M]")).groupby("_m")["hours"].sum()
    fin["analyst_hours"] = pd.Series(months, index=months).map(lambda m: hrs_by_month.get(np.datetime64(m, "M"), 0.0)).astype(float)

    # `fin` above holds the *actual observed* count for each calendar month. core.period.flow() day-weights
    # each month by how much of it the requested period overlaps, on the assumption that a partial "current"
    # month is stored as a full-month-equivalent (i.e. already scaled up). Rescale the in-progress month here
    # so a period ending exactly at AS_OF reproduces the true observed count.
    frac_last = AS_OF.day / months[-1].days_in_month
    if frac_last > 0:
        fin.iloc[-1] = fin.iloc[-1] / frac_last

    # ---------------- monthly stock frame (point-in-time snapshots) ----------------
    mend = [AS_OF if m == months[-1] else m + pd.offsets.MonthEnd(0) for m in months]
    stock = pd.DataFrame(index=months)
    stock["date"] = pd.DatetimeIndex(mend)
    stock["customers_active"] = [int((cust["onboarded"] <= d).sum()) for d in mend]
    stock["customers_low"] = [int(((cust["onboarded"] <= d) & (cust["risk_tier"] == "Low")).sum()) for d in mend]
    stock["customers_medium"] = [int(((cust["onboarded"] <= d) & (cust["risk_tier"] == "Medium")).sum()) for d in mend]
    stock["customers_high"] = [int(((cust["onboarded"] <= d) & (cust["risk_tier"] == "High")).sum()) for d in mend]
    stock["active_alerts"] = [int(((alerts["opened"] <= d) & (alerts["closed"].isna() | (alerts["closed"] > d))).sum()) for d in mend]
    stock["open_investigations"] = [int(((alerts["opened"] <= d) & (alerts["closed"].isna() | (alerts["closed"] > d)) & (alerts["disposition"] == "Under investigation")).sum()) for d in mend]
    stock["overdue_reviews"] = [int(((cust["onboarded"] <= d) & (cust["next_review_due"] < d)).sum()) for d in mend]

    M = dict(months=months, T=T, T_act=T, cust=cust, alerts=alerts, smrs=smrs, fin=fin, stock=stock,
             weights=weights, analysts=ANALYSTS)
    return M
