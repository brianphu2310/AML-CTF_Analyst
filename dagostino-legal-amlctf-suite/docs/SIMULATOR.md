# Alert Threshold & Model Tuning Simulator

The Simulator answers "what should we do about the alert queue?" It takes the last 12 months of actuals as the
base, lets you move the levers a compliance function actually controls, and shows the effect on alert volume,
false-positive rate, analyst hours and SLA-breach risk.

![Simulator](screenshots/08-simulator.png)

## Use it in two minutes

1. Open **★ Simulator** in the top bar (or follow a "Try it in the Simulator" link from Overview, KYC or Team).
2. Click a card under **Start from a scenario**, or move the sliders yourself.
3. Read the five projected KPIs: alerts a month, false-positive rate, analyst hours, capacity utilisation and
   detection coverage.
4. Scroll to the bridge chart to see which typologies are driving the change, and the tornado chart to see
   which lever moves alert volume the most.
5. Under **What would it take?**, choose a target (alert volume or analyst hours) and click **Apply** on the
   lever you would rather pull.
6. Check the **delivery-risk** view to see the result if only 100% / 75% / 50% of a tuning change lands by
   go-live.

## The levers

| Lever | Range | What it changes |
|---|---|---|
| Structuring / smurfing threshold | −30% to +30% | Sensitivity of the structuring rule (negative = catches more) |
| Rapid movement of funds threshold | −30% to +30% | Sensitivity of the velocity rule |
| High-risk jurisdiction threshold | −30% to +30% | Sensitivity of the jurisdiction-transfer rule |
| Cash-intensive pattern threshold | −30% to +30% | Sensitivity of the cash-intensity rule |
| Trade-based ML threshold | −30% to +30% | Sensitivity of the TBML rule |
| Foreign-dimension weight | −15 to +15 pp | The 4-factor risk model's foreign-dimension weight, which also shifts alert volume and coverage |
| New AML analysts | 0 to 3 | Adds monthly alert capacity (10 alerts × 2.4h each per hire) |
| Handling-time change | −20% to +20% | Average minutes an analyst spends per alert, across every typology |

## Worked example: cutting alert fatigue

On the sample data the base run-rate is **22.8 alerts a month**, a **55.2% false-positive rate**, **55 analyst
hours a month** (55.2% of team capacity) and **79.0% detection coverage**. The **Tighten thresholds** preset
(raises all five thresholds by 10%, and the foreign-dimension weight by 2 pp) projects to **19.9 alerts a
month**, a **51.2% false-positive rate** and **49 hours** — fewer low-value alerts without walking away from
detection coverage.

Under **What would it take?**, with a target of 21.8 alerts a month (a modest 4% cut), each lever on its own
would need to move by:

| Lever | Needed | Verdict |
|---|---|---|
| Structuring threshold | +13.2% | Comfortable |
| Rapid movement of funds threshold | +16.0% | Comfortable |
| Cash-intensive threshold | +17.1% | Comfortable |
| High-risk jurisdiction threshold | +18.7% | Comfortable |
| Foreign-dimension weight | −7.0 pp | Comfortable |
| Trade-based ML threshold | not enough on its own | n/a |

The tornado chart shows why the structuring lever is the most efficient single dial: raising it 5% alone cuts
about 0.36 alerts a month, more than double the effect of the same 5% move on the trade-based ML threshold
(0.12 alerts a month) — TBML alerts are the rarest of the five typologies, so its lever has the least
leverage. No single lever, at its full ±30% range, can cut the queue by more than roughly 10–15% on its own;
a double-digit reduction needs several levers moving together, which is exactly what the **Tighten thresholds**
preset does.

## Worked example: should we hire?

Load **Hire an AML analyst** (one additional analyst). Team monthly capacity rises from **100 hours to 124
hours**, so utilisation at the base alert volume falls from **55.2% to 44.5%** — meaningful headroom against
the SLA, without touching detection thresholds at all. Unlike a threshold change, a hire's headcount and pay
are treated as committed on day one in the delivery-risk view: only the threshold/weight tuning work is
modelled as being able to slip.

## Delivery risk, applied to the tighten scenario

| Delivery | Alerts / month | Hours / month | SLA-breach risk |
|---|---|---|---|
| 100% | 19.9 | 48.8 | 0% |
| 75% | 20.6 | 50.4 | 0% |
| 50% | 21.3 | 51.9 | 0% |

Even a stalled roll-out of the tightening work still reduces the queue somewhat, and the base scenario has
enough headroom (55% utilisation) that no combination of these delivery levels pushes SLA-breach risk above
zero — the risk view starts to matter once several loosening levers or a growth in the client base push
utilisation past 60%.

## How the numbers are built

See [METHODOLOGY.md, section 3](METHODOLOGY.md#3-simulator-projection-formulas) for the formulas. In short:

* Base = the trailing last-12-months actuals, day-weighted like every other page.
* With every lever at zero the scenario equals the base exactly (tested).
* **Goal-seek** solves each lever on its own, holding every other lever at its current value, by bisection,
  then rounds the answer to the nearest slider step. A lever is reported "Not reachable on its own" when the
  target sits outside what that lever can produce across its full range.
* **Delivery** scales the *magnitude* of threshold and foreign-weight changes only; a new hire's headcount is
  never softened, since it is committed on day one.

## Limits

* It is a monthly run-rate projection from historical typology behaviour, not a forecast of future criminal
  typologies or a substitute for an AML/CTF program's independent review.
* It holds the client base, product mix and criminal behaviour constant apart from the levers moved, and
  assumes new hires can be onboarded and trained in time.
* Thresholds are capped at a realistic ±30% band; the tool does not let you propose turning detection off
  altogether.
* Results are only as good as the base data; the sample data is entirely synthetic.
