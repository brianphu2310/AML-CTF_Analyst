"""D'Agostino Legal — AML/CTF Compliance Suite (entry point).

Run:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="D'Agostino Legal — AML/CTF Compliance", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

from core import theme, ui
from core.metrics import risk_tier_breakdown
from core.model import build_model
from core.period import current_periods, init_state, render_period_control
from core.ref import AS_OF, NAV_ITEMS, USER_NAME, USER_ROLE
from core.theme import TIER_COLORS
from views import overview, kyc, monitoring, triage, smr, ubo, team, simulator

PAGES = {"Overview": overview.render, "KYC": kyc.render, "Monitoring": monitoring.render, "Triage": triage.render,
         "SMR": smr.render, "UBO": ubo.render, "Team": team.render, "Simulator": simulator.render}


@st.cache_resource(show_spinner="Building the synthetic compliance dataset…")
def get_model():
    return build_model()


theme.apply_theme()
M = get_model()
init_state()
ss = st.session_state
ss.setdefault("view_name", "Overview")
ui.reset_card_counter()

# ----------------------------------------------------------------- sidebar ----
with st.sidebar:
    st.markdown('<div class="sidebar-brand"><div class="sidebar-brand-badge">D</div><div><div class="sidebar-brand-name">'
                "D'Agostino Legal</div><div class=\"sidebar-brand-tag\">AML/CTF Compliance</div></div></div>", unsafe_allow_html=True)
    tiers = risk_tier_breakdown(M, AS_OF)
    total = int(sum(tiers.values()))
    st.markdown('<div class="sidebar-label">Client risk book · today</div>', unsafe_allow_html=True)
    rings = [(f"{t} risk", int(tiers[t]), TIER_COLORS[t]) for t in ("Low", "Medium", "High")]
    st.markdown(f'<div class="sb-radial">{ui.radial_rings_svg(rings, total, "active clients")}</div>', unsafe_allow_html=True)
    rows = "".join(f'<div class="sb-tier-row"><span class="sb-tier-dot" style="background:{col}"></span>{lab}'
                   f'<span style="margin-left:auto;font-weight:700;color:#eef0f2;">{v}</span>'
                   f'<span style="width:34px;text-align:right;color:#6f7780;">{v / max(total, 1):.0%}</span></div>'
                   for lab, v, col in rings)
    st.markdown(f'<div style="margin:6px 0 4px;">{rows}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div><div class="sidebar-label">Reporting entity</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-stat" style="flex-direction:column;align-items:flex-start;gap:1px;"><span>Offices</span><b>Richmond · Camden · Liverpool</b></div>'
                '<div class="sb-stat"><span>Regulator</span><b>AUSTRAC</b></div>'
                '<div class="sb-stat"><span>Data as of</span><b>17 Sep 2025</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div><div class="sidebar-sub">Back-office AML/CTF function for the same firm as the '
                'Operations dashboard. Tranche 2 brings law firms into AUSTRAC\'s regulated population from 1 Jul 2026.</div>'
                '<div class="sidebar-sub" style="margin-bottom:0;">All clients, alerts and SMRs are synthetic and deterministically '
                'generated for this portfolio project. No real AUSTRAC data is used.</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------- top bar ----
with st.container(key="topbar"):
    nav_wrap, period_col, user_col = st.columns([6.6, 1.9, 1.5], vertical_alignment="center")
    with nav_wrap:
        for col, item in zip(st.columns([1.0 if i != "Simulator" else 1.5 for i in NAV_ITEMS]), NAV_ITEMS):
            with col:
                if st.button("★ Simulator" if item == "Simulator" else item, key=f"nav_{item}",
                              type="primary" if ss.view_name == item else "secondary", width="stretch"):
                    ss.view_name = item
                    st.rerun()
    with period_col:
        render_period_control()
    with user_col:
        initials = "".join(part[0] for part in USER_NAME.split()[:2]).upper()
        st.markdown(f'<div class="user-row"><div><div class="user-name" style="text-align:right;">Welcome, {USER_NAME}</div>'
                    f'<div class="user-role" style="text-align:right;">{USER_ROLE}</div></div><div class="avatar-initials">{initials}</div></div>', unsafe_allow_html=True)
ui.spacer(2)

# ------------------------------------------------------------------- router ----
cur, cmp = current_periods()
PAGES.get(ss.view_name, overview.render)(M, cur, cmp)
