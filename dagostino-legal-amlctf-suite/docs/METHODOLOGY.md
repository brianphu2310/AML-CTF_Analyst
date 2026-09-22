# Methodology

Formula-level detail for the three things this app computes: the client risk score, the typology alert
generation logic, and the Simulator's projection formulas. All figures below are synthetic.

> **Terminology.** The AML/CTF Act and AUSTRAC's rules say *customer* (as in customer due diligence). A law firm calls the same people *clients*, so the app and these docs use "client" throughout; the two words mean the same thing here.

## 1. Client risk rating — the AUSTRAC 4-factor model

Every client's risk score is a weighted sum of four factor scores (each 0–100 points), plus a small amount
of random noise to avoid perfectly clustered scores:

```
risk_score = w_type    × points(customer_type)
           + w_channel × points(delivery_channel)
           + w_foreign × points(foreign_dimension)
           + w_product × points(products_and_services)
           + noise                              (~N(0, 4), clipped to [1, 100])
```

Default weights (`core/ref.py`, `RISK_WEIGHTS_DEFAULT`): client type 28%, delivery/service channel 22%,
foreign dimension 27%, products & services 23%. These are tunable in the Simulator (the foreign-dimension
weight is exposed as a lever; the others follow the same mechanism).

Factor points (`core/ref.py`):

| Factor | Low end | High end |
|---|---|---|
| Client type | Individual (18) | Foreign Entity (74) |
| Delivery/service channel | Face-to-face (10) | Third-party intermediary (62) |
| Foreign dimension | Domestic only (8) | Tier 3 FATF-monitored jurisdiction (85) |
| Products & services | Conveyancing/trust transfer (26) | Business structuring (58) |

**Risk tier** (`RISK_TIER_BOUNDS = (28, 42)`):

```
tier = Low     if risk_score < 28
       Medium  if 28 <= risk_score <= 42
       High    if risk_score > 42
```

**Periodic review cycle** by tier (`REVIEW_CYCLE_MONTHS`): High = 12 months, Medium = 18 months, Low = 36
months. A client whose review has genuinely lapsed (not just due soon) is flagged `review_overdue` — the
model gives roughly a 1-in-5 chance that a due review was not actually completed on schedule, so the
Overview page's "Overdue periodic reviews" KPI reflects a realistic analyst backlog, not a perfectly
on-schedule population.

## 2. Typology detection logic

Five typologies (`core/ref.py`, `TYPOLOGIES`), each with a base monthly alert rate per active client, a
baseline false-positive rate, and an average analyst handling time:

| Typology | What it looks for | Base rate | Baseline FP rate | Avg hours |
|---|---|---|---|---|
| Structuring / smurfing | Multiple transactions kept just under the AUD 10,000 threshold | 3.8% | 62% | 2.4h |
| Rapid movement of funds | Funds in and out of trust within an unusually short window | 2.9% | 55% | 2.0h |
| High-risk jurisdiction transfer | Trust transfers to/from a Tier 2/3 jurisdiction with no clear rationale | 2.1% | 48% | 2.9h |
| Cash-intensive pattern | Cash-equivalent volume inconsistent with the client's profile | 2.5% | 58% | 2.1h |
| Trade-based ML indicator | Under/over-valuation or circular invoicing across related-party matters | 1.4% | 44% | 3.2h |

For each month, the number of alerts of a given typology is drawn `Poisson(base_rate × active_customers ×
elapsed_fraction)`, weighted so Medium-risk clients are ~2× and High-risk clients are ~4.3× as likely to
be selected as Low-risk clients (`tier_mult = {Low: 0.55, Medium: 1.15, High: 2.35}`). Each alert is then
resolved to a disposition:

```
is_false_positive  ~ Bernoulli(fp_rate)
if false positive:      disposition = "Closed — false positive"
else:                    disposition = "Escalated to SMR"          with probability 0.58
                         disposition = "Closed — no further action" otherwise
```

Turnaround time is drawn `~N(6.5 days, 3.5 days)`, clipped to [1, 30]; an alert breaches its SLA if the
turnaround exceeds `SLA_DAYS = 10`.

## 3. Simulator projection formulas

The Simulator projects a monthly run-rate from the trailing last-12-months actuals. Let `pct` be a
threshold lever's value (percent; negative = more sensitive/lower threshold) and `w` be the
foreign-dimension weight lever (percentage points):

**Alert volume** per typology:

```
weight_shift = w / 100 × 0.6
volume_multiplier = clip(1 − (pct / 100) × 1.15, 0.15, 3.5) × (1 + weight_shift)
projected_volume = baseline_volume × volume_multiplier
```

**False-positive rate** per typology:

```
fp_rate = clip(baseline_fp − (pct / 100) × 0.35 − weight_shift × 0.10, 0.05, 0.92)
```

**Detection coverage** per typology (the share of genuinely suspicious activity the ruleset catches; a
synthetic baseline of 79%):

```
coverage = clip(0.79 − (pct / 100) × 0.28 + weight_shift × 0.15, 0.20, 0.99)
```

**Analyst hours**: `hours = Σ(projected_volume × typology_avg_hours) × (1 + handling_time_pct / 100)`.

**Capacity and SLA-breach risk**: team hour capacity is the sum of each analyst's monthly alert cap ×
their average handling time, plus `new_hires × 10 alerts/month × 2.4h`. Utilisation is `hours / capacity`,
and SLA-breach risk is a ramp function:

```
sla_breach_risk = clip((utilisation − 0.60) / 0.35, 0, 1)
```

i.e. 0% risk at or below 60% utilisation, rising linearly to 100% risk at 95% utilisation and beyond.

**Goal seek**: for a chosen target (alert volume or analyst hours), each lever is solved independently by
bisection — `core.simulate._solve` finds the lever value at which the projection function equals the target,
holding every other lever fixed at its current value — then rounded to the nearest slider step. A lever is
reported "Not reachable on its own" when the target falls outside the range that lever can produce across
its full slider bounds.

**Delivery-risk view**: a `delivery` fraction (100/75/50%) scales the *magnitude* of threshold and
foreign-weight changes (`core.simulate.haircut`) to model a tuning change that only partially lands by
go-live. A new hire's headcount and pay are never softened, since they are committed on day one; only the
threshold/weight validation work — which can genuinely slip — is treated as at-risk.
