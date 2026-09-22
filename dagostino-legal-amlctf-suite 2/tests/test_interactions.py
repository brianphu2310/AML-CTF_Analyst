"""Clicks and edits in the running app (Streamlit AppTest): the things a plain 'does it render' test misses."""
import os
import sys

import pytest
from streamlit.testing.v1 import AppTest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import simulate as S
from core.model import build_model

APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


def new(**state):
    at = AppTest.from_file(APP, default_timeout=120)
    for k, v in state.items():
        at.session_state[k] = v
    return at.run()


def button(at, key):
    return next(b for b in at.button if b.key == key)


def sim():
    return new(view_name="Simulator", sim_mode="Alert-model tuning")


def ok(at):
    assert not at.exception, [e.value for e in at.exception]


def test_reset_levers_button_works():
    at = sim()
    at.slider(key="sim_thresh_struct").set_value(15.0).run()
    assert at.session_state["sim_thresh_struct"] == 15.0
    button(at, "act_reset").click().run()
    ok(at)
    assert at.session_state["sim_thresh_struct"] == 0.0
    assert at.session_state["sim_weight_foreign"] == 0.0


def test_preset_buttons_load_their_levers():
    at = sim()
    names = list(S.PRESETS)
    for i, name in enumerate(names):
        button(at, f"act_preset_{i}").click().run()
        ok(at)
        for k, v in S.preset_state(name).items():
            assert at.session_state[k] == v, (name, k)


def test_levers_survive_leaving_and_returning_to_the_page():
    at = sim()
    at.slider(key="sim_thresh_velocity").set_value(-10.0).run()
    at.session_state["view_name"] = "Team"; at.run(); ok(at)
    at.session_state["view_name"] = "Simulator"; at.run(); ok(at)
    assert at.slider(key="sim_thresh_velocity").value == -10.0


def test_goal_seek_apply_button_is_disabled_when_unreachable_alone():
    at = sim()
    at.number_input(key="sim_goal_target").set_value(1.0).run()      # far below what any single lever can reach alone
    ok(at)
    assert button(at, "act_apply_sim_thresh_struct").disabled


def test_goal_seek_apply_button_is_enabled_for_a_modest_reachable_target():
    at = sim()
    ok(at)
    assert not button(at, "act_apply_sim_weight_foreign").disabled


def test_goal_seek_apply_moves_the_lever_and_meets_the_target():
    at = sim()
    b = button(at, "act_apply_sim_weight_foreign")
    b.click().run()
    ok(at)
    M = build_model()
    _, f = S.base_actuals(M)
    s = {k: at.session_state[k] for k in S.DEFAULTS}
    target = at.session_state["sim_goal_target"]
    assert S.project(f, s)["alerts1"] <= target + 0.05 or s["sim_weight_foreign"] == S.BOUNDS["sim_weight_foreign"][0]


def test_new_hire_slider_moves_projected_hours():
    at = sim()
    at.slider(key="sim_hires").set_value(2).run()
    ok(at)
    assert at.session_state["sim_hires"] == 2


def test_overview_call_to_action_opens_the_simulator():
    at = new(view_name="Overview")
    button(at, "act_cta_ov").click().run()
    ok(at)
    assert at.session_state["view_name"] == "Simulator"


def test_team_call_to_action_loads_the_hire_preset():
    at = new(view_name="Team")
    button(at, "act_cta_team").click().run()
    ok(at)
    assert at.session_state["view_name"] == "Simulator" and at.session_state["sim_hires"] == 1


def test_kyc_call_to_action_loads_the_foreign_weight_preset():
    at = new(view_name="KYC")
    button(at, "act_cta_kyc").click().run()
    ok(at)
    assert at.session_state["view_name"] == "Simulator" and at.session_state["sim_weight_foreign"] == 8.0


def test_sla_status_is_computed_relative_to_the_selected_period_end():
    """Regression: SLA status for the open queue must use the period end date, not always today, so a
    historical period doesn't show every item as 'on track' just because it's since been closed."""
    at = new(view_name="Triage", period_preset="Last 12 months", compare_mode="No comparison")
    ok(at)


# ------------------------------------------------------------ case decision → escalation → SMR ----
def test_simulator_opens_in_case_decision_mode_with_a_loaded_case():
    at = new(view_name="Simulator")
    ok(at)
    assert at.session_state["sim_mode"] == "Case decision"
    assert at.session_state["case_meta"]["alert_id"] and at.session_state["case_client"]


def _shown_score(at):
    import re
    g = next(m.value for m in at.markdown if "suspicion score" in m.value)
    return int(re.search(r'font-size="40"[^>]*>(\d+)</text>', g).group(1))


def _shown_decision(at):
    import re
    d = next(m.value for m in at.markdown if "decision-title" in m.value)
    return re.search(r'decision-title">([^<]+)<', d).group(1)


def test_ticking_verification_lowers_the_score_live():
    at = new(view_name="Simulator")
    at.session_state["case_flags"] = ["Split cash under $10k", "Reluctant client", "Third-party payment"]
    at.session_state["case_mits"] = []
    at.run(); ok(at)
    s0, d0 = _shown_score(at), _shown_decision(at)
    at.session_state["case_mits"] = ["Source of funds verified", "Rationale documented"]
    at.run(); ok(at)
    s1, d1 = _shown_score(at), _shown_decision(at)
    assert s1 == s0 - 20 and d0 != d1


def test_escalate_then_mlro_decides_on_the_triage_page():
    at = new(view_name="Simulator")
    at.session_state["case_flags"] = ["Split cash under $10k", "Reluctant client", "Third-party payment", "Adverse media"]
    at.run()
    at.text_area(key="case_rationale").input("Deposits split across three branches.").run()
    button(at, "act_case_escalate").click().run(); ok(at)
    recs = at.session_state["escalations"]
    assert len(recs) == 1 and recs[0]["status"] == "Awaiting MLRO decision" and recs[0]["rationale"] == "Deposits split across three branches."
    button(at, "act_case_queue").click().run(); ok(at)
    assert at.session_state["view_name"] == "Triage"
    button(at, "act_esc_s_0").click().run(); ok(at)
    rec = at.session_state["escalations"][0]
    assert rec["status"].startswith("Suspicion formed") and rec["smr_due"] is not None
    assert button(at, "act_esc_s_0").disabled                              # decided once, buttons lock


def test_triage_open_in_simulator_loads_that_alert():
    at = new(view_name="Triage"); ok(at)
    pick = at.selectbox(key="tri_pick").value
    button(at, "act_tri_open").click().run(); ok(at)
    assert at.session_state["view_name"] == "Simulator" and at.session_state["sim_mode"] == "Case decision"
    assert at.session_state["case_meta"]["alert_id"] == pick


def test_smr_page_offers_a_word_download_for_the_selected_smr():
    at = new(view_name="SMR"); ok(at)
    assert at.selectbox(key="smr_pick").value.startswith("SMR-")
    assert any(getattr(d, "key", None) == "act_smr_doc" for d in at.get("download_button"))
