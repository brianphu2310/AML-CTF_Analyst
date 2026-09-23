"""Alert Threshold & Model Tuning Simulator — the flagship page.

Pure functions (no Streamlit) so every number can be unit-tested. Levers are stored in the units the
analyst sees: percent threshold change (lower = more sensitive), percentage points of factor weight,
number of new analyst hires, and percent change in average handling time.

The domain logic: raising a monitoring-rule threshold catches fewer, higher-conviction alerts (lower
false-positive rate, lower analyst workload) but also lower detection coverage; lowering it does the
opposite. This is the model-governance trade-off an AML analyst tunes and has to defend to a Compliance
Committee — this page makes the trade-off numeric instead of a judgement call.
"""
import numpy as np
import pandas as pd

from .metrics import fin_sum
from .model import REVIEW_CYCLE_MONTHS
from .period import Period
from .ref import AS_OF, START, TYPOLOGIES, TYPOLOGY_NAMES, ANALYSTS

LEVER_TYPOLOGY = {"sim_thresh_struct": "Structuring / smurfing", "sim_thresh_velocity": "Rapid movement of funds",
                   "sim_thresh_jurisdiction": "High-risk jurisdiction transfer", "sim_thresh_cash": "Cash-intensive pattern",
                   "sim_thresh_tbml": "Trade-based ML indicator"}
THRESH_LEVERS = list(LEVER_TYPOLOGY)
DEFAULTS = dict(sim_thresh_struct=0.0, sim_thresh_velocity=0.0, sim_thresh_jurisdiction=0.0, sim_thresh_cash=0.0,
                sim_thresh_tbml=0.0, sim_weight_foreign=0.0, sim_hires=0, sim_handle_time=0.0)
BOUNDS = dict(sim_thresh_struct=(-30.0, 30.0, 5.0), sim_thresh_velocity=(-30.0, 30.0, 5.0), sim_thresh_jurisdiction=(-30.0, 30.0, 5.0),
              sim_thresh_cash=(-30.0, 30.0, 5.0), sim_thresh_tbml=(-30.0, 30.0, 5.0), sim_weight_foreign=(-15.0, 15.0, 1.0),
              sim_hires=(0, 3, 1), sim_handle_time=(-20.0, 20.0, 2.0))
LEVER_LABEL = {"sim_thresh_struct": "Structuring threshold (%)", "sim_thresh_velocity": "Velocity threshold (%)",
               "sim_thresh_jurisdiction": "Jurisdiction-transfer threshold (%)", "sim_thresh_cash": "Cash-intensity threshold (%)",
               "sim_thresh_tbml": "Trade-based ML threshold (%)", "sim_weight_foreign": "Foreign-dimension risk weight (pp)",
               "sim_hires": "New AML analysts", "sim_handle_time": "Avg handling time (%)"}

PRESETS = {
    "Tighten thresholds (cut alert fatigue)": dict(sim_thresh_struct=15.0, sim_thresh_velocity=15.0, sim_thresh_cash=15.0),
    "Loosen thresholds (regulator pressure)": dict(sim_thresh_struct=-15.0, sim_thresh_velocity=-15.0, sim_thresh_jurisdiction=-15.0),
    "Raise foreign-dimension weight": dict(sim_weight_foreign=8.0),
    "Hire an AML analyst": dict(sim_hires=1),
    "Efficiency drive (-15% handling time)": dict(sim_handle_time=-15.0),
    "Widen jurisdiction sensitivity only": dict(sim_thresh_jurisdiction=-20.0),
}
PRESET_HELP = {"Tighten thresholds (cut alert fatigue)": "Structuring, velocity and cash thresholds all +15%: fewer, higher-conviction alerts",
               "Loosen thresholds (regulator pressure)": "Three thresholds -15%: catches more, at the cost of analyst hours and FP rate",
               "Raise foreign-dimension weight": "+8pp on the foreign-dimension factor in the 4-factor risk model",
               "Hire an AML analyst": "One additional analyst at the team's average capacity",
               "Efficiency drive (-15% handling time)": "Faster triage via better case-management tooling",
               "Widen jurisdiction sensitivity only": "Jurisdiction-transfer threshold -20%, everything else unchanged"}

NEW_HIRE_CAPACITY, NEW_HIRE_HOURS = 10, 2.4     # a new analyst's monthly alert capacity and avg hours/alert
THRESH_ELASTICITY = 1.15                        # % change in alert volume per 1% change in threshold (inverse direction)
FP_SENSITIVITY = 0.35                           # pp change in false-positive rate per 1% threshold change
COVERAGE_SENSITIVITY = 0.28                     # pp change in detection coverage per 1% threshold change
BASE_COVERAGE = 0.79                            # assumed baseline share of genuinely suspicious activity the current ruleset catches


def base_period():
    return Period(AS_OF.replace(day=1) - pd.DateOffset(months=11), AS_OF, "Last 12 months")


def base_actuals(M):
    p = base_period()
    return p, fin_sum(M, p)


def team_capacity():
    cap_alerts = sum(a["capacity"] for a in ANALYSTS)
    cap_hours = sum(a["capacity"] * a["avg_hours"] for a in ANALYSTS)
    return cap_alerts, cap_hours


def preset_state(name):
    return {**DEFAULTS, **PRESETS[name]}


def haircut(s, delivery):
    """Deliver only `delivery` (0-1) of the planned tuning change. A hire's headcount and pay are committed
    on day one and are never softened; the magnitude of threshold and weight changes is."""
    if delivery >= 1.0:
        return dict(s)
    t = dict(s)
    for k in THRESH_LEVERS + ["sim_weight_foreign", "sim_handle_time"]:
        t[k] = t[k] * delivery
    return t


def project(f, s, delivery=1.0):
    """Projected monthly run-rate under the scenario. f = last-12-month actuals (fin_sum Series); s = lever values."""
    s = haircut(s, delivery)
    cap_alerts0, cap_hours0 = team_capacity()
    weight_shift = s["sim_weight_foreign"] / 100.0 * 0.6      # +1pp of foreign weight -> ~0.6% more monitoring intensity firm-wide

    rows = []
    total0 = total1 = 0.0
    fp_num0 = fp_num1 = 0.0
    cov0 = cov1 = 0.0
    for typ in TYPOLOGY_NAMES:
        lever = {v: k for k, v in LEVER_TYPOLOGY.items()}[typ]
        pct = s[lever]
        vol0 = float(f[f"alerts_{typ}"]) / 12.0
        mult = np.clip(1 - (pct / 100.0) * THRESH_ELASTICITY, 0.15, 3.5) * (1 + weight_shift)
        vol1 = vol0 * mult
        fp0 = TYPOLOGIES[typ]["fp_rate"]
        fp1 = float(np.clip(fp0 - (pct / 100.0) * FP_SENSITIVITY + (weight_shift * -0.10), 0.05, 0.92))
        covt0 = BASE_COVERAGE
        covt1 = float(np.clip(covt0 - (pct / 100.0) * COVERAGE_SENSITIVITY + weight_shift * 0.15, 0.20, 0.99))
        rows.append(dict(typology=typ, lever=lever, vol0=vol0, vol1=vol1, fp0=fp0, fp1=fp1, cov0=covt0, cov1=covt1))
        total0 += vol0; total1 += vol1
        fp_num0 += vol0 * fp0; fp_num1 += vol1 * fp1
        cov0 += covt0 / len(TYPOLOGY_NAMES); cov1 += covt1 / len(TYPOLOGY_NAMES)

    hires = int(s["sim_hires"])
    cap_alerts1 = cap_alerts0 + hires * NEW_HIRE_CAPACITY
    cap_hours1 = cap_hours0 + hires * NEW_HIRE_CAPACITY * NEW_HIRE_HOURS
    avg_hours0 = float((f[[f"alerts_{t}" for t in TYPOLOGY_NAMES]].sum() and sum(TYPOLOGIES[t]["hours"] * float(f[f"alerts_{t}"]) for t in TYPOLOGY_NAMES) / max(total0 * 12, 1e-9)) or 2.3)
    handle_mult = 1 + s["sim_handle_time"] / 100.0
    hours0 = sum(r["vol0"] * TYPOLOGIES[r["typology"]]["hours"] for r in rows)
    hours1 = sum(r["vol1"] * TYPOLOGIES[r["typology"]]["hours"] * handle_mult for r in rows)
    util0 = hours0 / cap_hours0 if cap_hours0 else np.nan
    util1 = hours1 / cap_hours1 if cap_hours1 else np.nan
    sla0 = float(np.clip((util0 - 0.60) / 0.35, 0, 1)) if not np.isnan(util0) else np.nan
    sla1 = float(np.clip((util1 - 0.60) / 0.35, 0, 1)) if not np.isnan(util1) else np.nan
    fp_rate0 = fp_num0 / total0 if total0 else np.nan
    fp_rate1 = fp_num1 / total1 if total1 else np.nan

    return dict(rows=rows, alerts0=total0, alerts1=total1, fp_rate0=fp_rate0, fp_rate1=fp_rate1, coverage0=cov0, coverage1=cov1,
                hours0=hours0, hours1=hours1, cap_hours0=cap_hours0, cap_hours1=cap_hours1, cap_alerts0=cap_alerts0, cap_alerts1=cap_alerts1,
                util0=util0, util1=util1, sla_breach_risk0=sla0, sla_breach_risk1=sla1, hires=hires)


# ------------------------------------------------------------------ goal seek ----
def _solve(fn, lo, hi, target, iters=60):
    """x in [lo, hi] with fn(x) == target, for a monotone (increasing or decreasing) fn. None if `target` is
    outside the range fn actually reaches over [lo, hi]."""
    flo, fhi = fn(lo), fn(hi)
    if (target - flo) * (target - fhi) > 0:            # target is outside [min(flo,fhi), max(flo,fhi)]
        return None
    a, b, fa = lo, hi, flo
    for _ in range(iters):
        mid = (a + b) / 2
        fm = fn(mid)
        if (fm - target) * (fa - target) <= 0:
            b = mid
        else:
            a, fa = mid, fm
    return b


def goal_seek(f, s, target_alerts=None, target_hours=None):
    """For each single lever: what value (holding the rest of the scenario fixed) reaches a target monthly
    alert volume or analyst-hours figure? Solved by bisection since every lever is monotonic in its effect."""
    assert (target_alerts is None) != (target_hours is None), "give exactly one target"
    metric = (lambda t: project(f, t)["alerts1"]) if target_alerts is not None else (lambda t: project(f, t)["hours1"])
    goal = target_alerts if target_alerts is not None else target_hours
    rows = []
    for lever in THRESH_LEVERS + ["sim_weight_foreign"]:
        lo, hi, _ = BOUNDS[lever]
        x = _solve(lambda v, lever=lever: metric({**s, lever: v}), lo, hi, goal)
        rows.append(_goal_row(lever, x, s[lever]))
    if target_hours is not None:
        lo, hi, _ = BOUNDS["sim_hires"]
        x = _solve(lambda v: metric({**s, "sim_hires": round(v)}), lo, hi, goal)
        rows.append(_goal_row("sim_hires", x, s["sim_hires"]))
    return pd.DataFrame(rows)


def _goal_row(lever, x, current):
    lo, hi, step = BOUNDS[lever]
    if x is None:
        return dict(lever=lever, label=LEVER_LABEL[lever], required=np.nan, change=np.nan, apply_value=np.nan, fits_slider=False, difficulty="Not reachable on its own")
    change = x - current
    if abs(change) < 1e-9:
        return dict(lever=lever, label=LEVER_LABEL[lever], required=x, change=0.0, apply_value=current, fits_slider=True, difficulty="Already met")
    rounded = float(np.clip(round(x / step) * step, lo, hi))
    fits = lo - 1e-9 <= x <= hi + 1e-9
    span = hi - lo
    share = abs(change) / span if span > 0 else 9
    difficulty = "Comfortable" if fits and share <= 0.45 else ("Stretch" if fits else "Beyond a realistic range")
    return dict(lever=lever, label=LEVER_LABEL[lever], required=x, change=change, apply_value=rounded if fits else None, fits_slider=fits, difficulty=difficulty)


# ------------------------------------------------------------ risk and ranking ----
def delivery_range(f, s, levels=(1.0, 0.75, 0.5)):
    base = project(f, DEFAULTS)
    rows = []
    for d in levels:
        r = project(f, s, delivery=d)
        rows.append(dict(delivery=d, alerts=r["alerts1"], hours=r["hours1"], sla_risk=r["sla_breach_risk1"], vs_base_alerts=r["alerts1"] - base["alerts0"]))
    return pd.DataFrame(rows)


LEVER_TESTS = {"+5% structuring threshold": dict(sim_thresh_struct=5.0), "+5% velocity threshold": dict(sim_thresh_velocity=5.0),
               "+5% jurisdiction threshold": dict(sim_thresh_jurisdiction=5.0), "+5% cash threshold": dict(sim_thresh_cash=5.0),
               "+5% trade-based ML threshold": dict(sim_thresh_tbml=5.0), "+1pp foreign-dimension weight": dict(sim_weight_foreign=1.0),
               "+1 analyst hire": dict(sim_hires=1), "-5% handling time": dict(sim_handle_time=-5.0)}


def lever_ranking(f):
    """Monthly alert-volume effect of one unit of each lever, measured from the neutral baseline — the tornado chart.
    Hires and handling-time change workload, not detection volume, so they are excluded from this ranking."""
    base_alerts = project(f, DEFAULTS)["alerts1"]
    out = []
    for name, t in LEVER_TESTS.items():
        if "hire" in name or "handling time" in name:
            continue
        out.append((name, project(f, {**DEFAULTS, **t})["alerts1"] - base_alerts))
    return sorted(out, key=lambda x: x[1])


def bridge_data(f, s):
    """Waterfall decomposition of the change in monthly alert volume from the neutral baseline to the scenario,
    one bar per lever that actually moved."""
    base = project(f, DEFAULTS)
    steps = [("Current run-rate", base["alerts0"])]
    running = dict(DEFAULTS)
    prev_total = base["alerts1"]
    for lever in THRESH_LEVERS + ["sim_weight_foreign"]:
        if abs(s[lever] - DEFAULTS[lever]) < 1e-9:
            continue
        running[lever] = s[lever]
        new_total = project(f, running)["alerts1"]
        steps.append((LEVER_LABEL[lever], new_total - prev_total))
        prev_total = new_total
    steps.append(("Tuned run-rate", project(f, s)["alerts1"]))
    return steps


def scenario_summary(name, r, s):
    changed = ", ".join(f"{LEVER_LABEL.get(k, k)}={v}" for k, v in s.items() if v != DEFAULTS[k])
    return dict(Scenario=name, AlertsPerMonth=r["alerts1"], FPRate=r["fp_rate1"], Coverage=r["coverage1"],
                Hours=r["hours1"], SLARisk=r["sla_breach_risk1"], Levers=changed or "none")
