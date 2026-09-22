"""Simulator engine: goal-seek hits its target, delivery haircuts behave, presets are valid, thresholds are sane."""
import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import simulate as S
from core.model import build_model
from core.period import delta

M = build_model()
_, F = S.base_actuals(M)
Z = dict(S.DEFAULTS)
R0 = S.project(F, Z)


def test_every_preset_is_valid_and_within_slider_bounds():
    for name in S.PRESETS:
        st = S.preset_state(name)
        assert set(st) == set(S.DEFAULTS)
        for k, (lo, hi, _) in S.BOUNDS.items():
            assert lo <= st[k] <= hi, (name, k)
        S.project(F, st)                                    # runs without error


def test_threshold_bounds_are_sane():
    for lever in S.THRESH_LEVERS:
        lo, hi, step = S.BOUNDS[lever]
        assert lo < 0 < hi                                   # both tightening and loosening are on the table
        assert step > 0 and (hi - lo) % step == 0


def test_lowering_a_threshold_increases_alert_volume_and_raising_it_decreases_it():
    for lever in S.THRESH_LEVERS:
        lo = S.project(F, {**Z, lever: -10.0})["alerts1"]
        hi = S.project(F, {**Z, lever: 10.0})["alerts1"]
        assert lo > R0["alerts1"] > hi, lever


def test_raising_a_threshold_reduces_the_false_positive_rate():
    r = S.project(F, {**Z, "sim_thresh_struct": 20.0})
    assert r["fp_rate1"] < R0["fp_rate1"]


def test_raising_a_threshold_reduces_detection_coverage():
    r = S.project(F, {**Z, "sim_thresh_struct": 20.0})
    assert r["coverage1"] < R0["coverage1"]


def test_hiring_increases_capacity_but_not_volume():
    r = S.project(F, {**Z, "sim_hires": 2})
    assert r["alerts1"] == pytest.approx(R0["alerts1"])
    assert r["cap_hours1"] > R0["cap_hours1"]


def test_handle_time_changes_hours_but_not_volume():
    r = S.project(F, {**Z, "sim_handle_time": -15.0})
    assert r["alerts1"] == pytest.approx(R0["alerts1"])
    assert r["hours1"] < R0["hours1"]


def test_goal_seek_alert_target_is_met_exactly_by_the_reachable_lever():
    target = R0["alerts1"] * 0.96      # a modest reduction — reachable by moving one threshold lever within its slider range
    gs = S.goal_seek(F, Z, target_alerts=target)
    solved = gs[gs["required"].notna() & (gs["change"].abs() > 1e-9)]
    assert len(solved) >= 1
    for _, row in solved.iterrows():
        r = S.project(F, {**Z, row["lever"]: row["required"]})
        assert r["alerts1"] == pytest.approx(target, abs=0.05), row["lever"]


def test_goal_seek_hours_target():
    target = R0["hours1"] * 0.95
    gs = S.goal_seek(F, Z, target_hours=target)
    solved = gs[gs["required"].notna() & (gs["change"].abs() > 1e-9)]
    assert len(solved) >= 1


def test_goal_seek_apply_value_stays_close_to_the_target_after_rounding_to_a_slider_step():
    target = R0["alerts1"] * 0.97
    gs = S.goal_seek(F, Z, target_alerts=target)
    subset = gs[gs["apply_value"].notna() & (gs["difficulty"] != "Already met")]
    for _, row in subset.iterrows():
        lever = row["lever"]
        _, _, step = S.BOUNDS[lever]
        r = S.project(F, {**Z, lever: row["apply_value"]})
        assert abs(r["alerts1"] - target) <= step * 1.5, lever      # within about one slider step's worth of effect


def test_goal_seek_reports_when_already_met():
    scenario = {**Z, "sim_thresh_struct": 20.0}
    target = S.project(F, scenario)["alerts1"]                      # the current setting already produces exactly this
    gs = S.goal_seek(F, scenario, target_alerts=target)
    row = gs[gs["lever"] == "sim_thresh_struct"].iloc[0]
    assert row["difficulty"] == "Already met"


def test_goal_seek_says_unreachable_instead_of_inventing_an_answer():
    gs = S.goal_seek(F, Z, target_alerts=R0["alerts1"] * 0.05)
    assert (gs["difficulty"] != "Comfortable").all()


def test_delivery_haircut_scales_threshold_changes_only():
    up = {**Z, "sim_thresh_struct": 20.0}
    full, half = S.project(F, up, 1.0)["alerts1"], S.project(F, up, 0.5)["alerts1"]
    base = S.project(F, Z)["alerts1"]
    assert full < half < base                               # a tightened threshold cuts volume; half-delivered cuts it less


def test_delivery_haircut_never_softens_a_hire():
    hire = S.preset_state("Hire an AML analyst")
    full, half = S.project(F, hire, 1.0), S.project(F, hire, 0.5)
    assert full["cap_hours1"] == pytest.approx(half["cap_hours1"])


def test_delivery_range_is_ordered_by_delivery_level():
    dr = S.delivery_range(F, S.preset_state("Tighten thresholds (cut alert fatigue)"))
    assert list(dr["delivery"]) == [1.0, 0.75, 0.5]
    assert dr["alerts"].is_monotonic_increasing                # more delivery of a tightening scenario -> fewer alerts -> increasing as delivery drops


def test_lever_ranking_orders_by_effect_on_alert_volume():
    rank = S.lever_ranking(F)
    vals = [v for _, v in rank]
    assert vals == sorted(vals)
    assert len(rank) == len(S.THRESH_LEVERS) + 1              # 5 thresholds + foreign-weight (handling-time has ~0 volume effect, excluded by construction)


def test_bridge_data_starts_and_ends_on_the_run_rate():
    s = S.preset_state("Tighten thresholds (cut alert fatigue)")
    steps = S.bridge_data(F, s)
    assert steps[0][0] == "Current run-rate"
    assert steps[-1][0] == "Tuned run-rate"
    total = steps[0][1] + sum(v for _, v in steps[1:-1])
    assert total == pytest.approx(steps[-1][1], abs=0.05)


def test_zero_levers_equals_neutral_baseline():
    r = S.project(F, dict(S.DEFAULTS))
    assert r["alerts1"] == pytest.approx(r["alerts0"])


@pytest.mark.parametrize("cur,prev,expected", [(5, 0, None), (0, 0, None), (5, 10, -0.5), (3, 2.0, 0.5), (None, 3, None), (3, None, None), (float("nan"), 3, None), (np.int64(4), np.int64(0), None)])
def test_delta_never_divides_by_zero(cur, prev, expected):
    assert delta(cur, prev) == expected


if __name__ == "__main__":
    tests = [(n, fn) for n, fn in sorted(globals().items()) if n.startswith("test_") and callable(fn)]
    for n, fn in tests:
        fn(); print("PASS", n)
    print(f"{len(tests)} tests passed")
