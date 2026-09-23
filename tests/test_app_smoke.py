"""Smoke test: every page renders without raising an exception (Streamlit's headless AppTest),
across several period/filter combinations including edge cases."""
import datetime as dt
import os
import sys

import pytest
from streamlit.testing.v1 import AppTest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.ref import NAV_ITEMS

APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


def _run(**state):
    at = AppTest.from_file(APP, default_timeout=120)
    for k, v in state.items():
        at.session_state[k] = v
    return at.run()


@pytest.mark.parametrize("page", NAV_ITEMS)
def test_page_renders(page):
    at = _run(view_name=page)
    assert not at.exception, [e.value for e in at.exception]


@pytest.mark.parametrize("preset,compare", [("This month (MTD)", "Same period last year"), ("Last 12 months", "No comparison"),
                                             ("This quarter (QTD)", "Prior period")])
def test_period_settings_do_not_break_pages(preset, compare):
    for page in NAV_ITEMS:
        at = _run(view_name=page, period_preset=preset, compare_mode=compare)
        assert not at.exception, (page, [e.value for e in at.exception])


EDGE_RANGES = [("single day", dt.date(2025, 9, 17), dt.date(2025, 9, 17)), ("weekend", dt.date(2025, 9, 13), dt.date(2025, 9, 14)),
               ("reversed", dt.date(2025, 9, 17), dt.date(2025, 9, 1)), ("first day of data", dt.date(2023, 7, 1), dt.date(2023, 7, 1))]


@pytest.mark.parametrize("label,start,end", EDGE_RANGES)
@pytest.mark.parametrize("compare", ["Prior period", "Same period last year"])
def test_pages_survive_periods_with_no_or_little_activity(label, start, end, compare):
    """Regression guard: an empty period (no alerts opened, no customers onboarded) must not crash any page —
    division-by-zero and empty-dataframe paths are the usual culprits."""
    for page in NAV_ITEMS:
        at = _run(view_name=page, period_preset="Custom range", custom_start=start, custom_end=end, compare_mode=compare)
        assert not at.exception, (label, page, [e.value for e in at.exception])


# ------------------------------------------------------ Overview: geo toggle + header filters ----
@pytest.mark.parametrize("dim", ["State", "Risk Tier", "Typology", "Channel"])
def test_overview_geo_toggle_states_render(dim):
    """Each Customers-by-State toggle state (which also drives the Compliance Metrics table's grouping)
    must render without exception, including the non-State dims where the map recolours by a subset metric."""
    at = _run(view_name="Overview", ov_geo_dim=dim)
    assert not at.exception, (dim, [e.value for e in at.exception])


@pytest.mark.parametrize("status,branch,tier,typ", [
    ("All", "All", "All", "All"),
    ("Escalated to SMR", "Richmond", "High", "Structuring / smurfing"),
    ("Open", "All", "Low", "All"),
    ("Closed — false positive", "Camden", "Medium", "Rapid movement of funds"),
])
def test_overview_header_filter_combinations_render(status, branch, tier, typ):
    """The Overview header's Alert status / Branch / Risk tier / Typology dropdowns, alone and combined,
    must never break the pipeline visual or the underlying alert filtering — including a combo that yields
    zero matching alerts (Low risk tier alerts are rare/absent by construction)."""
    at = _run(view_name="Overview", ov_f_status=status, ov_f_branch=branch, ov_f_tier=tier, ov_f_typ=typ)
    assert not at.exception, ((status, branch, tier, typ), [e.value for e in at.exception])


def test_overview_geo_toggle_and_filters_combined():
    at = _run(view_name="Overview", ov_geo_dim="Typology", ov_f_status="Escalated to SMR", ov_f_tier="High")
    assert not at.exception, [e.value for e in at.exception]


@pytest.mark.parametrize("page", NAV_ITEMS)
def test_ui_calls_them_clients_not_customers(page):
    """A law firm has clients. Every label, heading, table header and tab on every page must say
    "client"; the KYC acronym and the Act's term "customer due diligence" are the only places the word survives."""
    at = _run(view_name=page)
    texts = [e.value for e in at.markdown] + [e.value for e in at.caption] + [t.label for t in at.tabs]
    texts += [str(c) for df in at.dataframe for c in df.value.columns]
    # "customer due diligence" is the Act's defined term (CDD) and stays as written
    offenders = [t for t in texts if "customer" in str(t).lower().replace("customer due diligence", "")]
    assert not offenders, offenders[:5]


def test_sidebar_radial_chart_shows_the_whole_risk_book():
    """The sidebar radial chart under the logo: one ring per risk tier, centre = active clients,
    and the three ring counts add back up to that centre total."""
    import re
    from core.metrics import risk_tier_breakdown
    from core.model import build_model
    from core.ref import AS_OF
    tiers = risk_tier_breakdown(build_model(), AS_OF)
    total = int(sum(tiers.values()))
    at = _run(view_name="Overview")
    assert not at.exception
    html = " ".join(m.value for m in at.sidebar.markdown)
    assert "sb-radial" in html and f">{total}</text>" in html
    rings = re.findall(r"<title>(Low|Medium|High) risk: (\d+) ", html)
    assert [t for t, _ in rings] == ["Low", "Medium", "High"]
    assert sum(int(v) for _, v in rings) == total
