"""Design tokens + global CSS (kept in one place so every page looks the same).

Dark "lime" theme: near-black canvas, charcoal cards with a thin lime outline, lime as the
primary data colour and KPI accent, teal/sky/slate as supporting series, pale-teal card titles.
Risk tiers keep traffic-light semantics (Low = teal, Medium = amber, High = red) because a
compliance reader expects red to mean high risk.
The Streamlit widget theme (dropdowns, pills, tabs, tables) is set to match in .streamlit/config.toml.
"""
import streamlit as st

# ---- surfaces ----
BG = "#0b0c0e"          # page canvas
CARD = "#15171a"        # card surface
CARD_2 = "#1e2125"      # inset surface (tracks, table total row, pills)
BORDER = "#2a2e34"      # hairlines inside cards
EDGE = "rgba(181,211,52,0.55)"   # thin lime card outline
GRID = "#24282d"        # chart gridlines
# ---- accents ----
LIME = "#b5d334"; LIME_DIM = "#7f9425"; LIME_TINT = "rgba(181,211,52,0.12)"
TEAL = "#3fa7b4"; SKY = "#8cc8da"; SLATE = "#7a8fc0"; SILVER = "#d9dde2"
TITLE = "#9ec7d3"       # card titles (pale teal, as in the reference report)
# ---- text ----
INK = "#eef0f2"; MUTED = "#a4abb4"; FAINT = "#6f7780"
# ---- semantic ----
GREEN = LIME; RED = "#ef5d52"; AMBER = "#f2b33d"
GREEN_TINT = "rgba(181,211,52,0.12)"; RED_TINT = "rgba(239,93,82,0.14)"; AMBER_TINT = "rgba(242,179,61,0.14)"
SHADOW = "0 8px 24px rgba(0,0,0,0.45)"
SERIES = [LIME, TEAL, SKY, SLATE, SILVER, AMBER, FAINT]        # default chart palette
TIER_COLORS = {"Low": "#4f9fb0", "Medium": AMBER, "High": RED}
TYP_COLORS = [LIME, TEAL, SKY, SLATE, SILVER]
SMR_COLOR = LIME        # an SMR is the pipeline's end product — same lime as the pipeline bars


def base_css():
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class^="css"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: {BG}; color:{INK}; }}
.block-container {{ padding-top: 0.5rem; padding-bottom: 0.1rem; padding-left: 1rem; padding-right: 1rem; max-width: 100%; }}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {{ width: 212px !important; min-width: 212px !important; background: {BG} !important; }}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{ display: none !important; }}
section[data-testid="stSidebar"] > div {{ padding: 8px 6px 6px 8px; background: {BG} !important; }}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
    background: {CARD} !important; border-radius: 10px; padding: 14px 12px 10px 12px; border: 1px solid {EDGE};
    box-sizing: border-box; min-height: calc(100vh - 19px);
}}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] p,
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] label,
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] span {{ color: {INK} !important; }}
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {{ gap: 0.2rem; }}
.sidebar-brand {{ display:flex; align-items:center; gap:9px; margin-bottom:8px; }}
.sidebar-brand-badge {{
    background:{LIME}; width:28px; height:28px; border-radius:7px;
    display:flex; align-items:center; justify-content:center; color:#0b0c0e; font-weight:800; font-size:15px; flex-shrink:0;
}}
section[data-testid="stSidebar"] .sidebar-brand-badge {{ color:#0b0c0e !important; }}
.sidebar-brand-name {{ font-weight:700; font-size:13px; color:{INK} !important; line-height:1.2; }}
.sidebar-brand-tag {{ font-size:10px; color:{LIME}; font-weight:600; letter-spacing:.02em; }}
.sidebar-label {{ font-size:11px; font-weight:700; color:{TITLE}; margin-bottom:2px; letter-spacing:.02em; }}
.sidebar-sub {{ font-size:10.5px; color:{FAINT}; margin-bottom:8px; line-height:1.45; }}
.sidebar-divider {{ height: 1px; margin: 8px 0 8px; background: {BORDER}; }}
.sb-tier-row {{ display:flex; align-items:center; gap:7px; font-size:11px; color:{MUTED}; margin-bottom:5px; }}
.sb-tier-dot {{ width:9px; height:9px; border-radius:50%; flex-shrink:0; }}
.sb-stat {{ display:flex; justify-content:space-between; font-size:11px; color:{MUTED}; margin-bottom:5px; }}
.sb-stat b {{ color:{INK}; font-weight:700; }}
.sb-radial svg {{ display:block; width:100%; max-width:168px; height:auto; margin:2px auto 0; }}

#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}
/* Streamlit pulls every markdown block up 16px to cancel a trailing paragraph margin; our HTML-only blocks
   have no paragraph, so that pull made consecutive blocks overlap (sidebar labels, KPI rail). Cancel it. */
[data-testid="stMarkdownContainer"]:not(:has(> p)) {{ margin-bottom: 0 !important; }}
div[data-testid="stVerticalBlock"] {{ gap: 0.35rem; }}

/* ---------- cards: charcoal with a thin lime outline ---------- */
div[class*="st-key-cardblock_"] {{
    background:{CARD} !important; border-radius: 8px !important;
    box-shadow: {SHADOW} !important; border: 1px solid {EDGE} !important; padding: 0.6rem 0.7rem !important;
}}

.user-row {{ display:flex; align-items:center; gap:8px; justify-content:flex-end; height:34px; white-space:nowrap; }}
.avatar-initials {{
    width:30px; height:30px; border-radius:15px; background:{LIME}; color:#0b0c0e; font-weight:800; font-size:11px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
}}
.user-name {{ font-weight:600; font-size:12px; color:{INK}; line-height:1.2; white-space:nowrap; }}
.user-role {{ font-size:9.5px; color:{FAINT}; line-height:1.2; white-space:nowrap; }}

/* ---------- top bar ---------- */
.st-key-topbar div[data-testid="stButton"] button {{
    border-radius: 6px !important; font-weight: 600 !important; font-size: 12px !important;
    padding: 5px 2px !important; border: 1px solid transparent !important; min-height: 32px !important;
    background: transparent !important; color: {MUTED} !important; box-shadow: none !important;
    white-space: nowrap !important; overflow: visible !important;
}}
.st-key-topbar div[data-testid="stButton"] button p {{ color: inherit !important; }}
.st-key-topbar div[data-testid="stButton"] button:hover {{ color:{INK} !important; border-color:{BORDER} !important; }}
.st-key-topbar div[data-testid="stButton"] button[kind="primary"] {{
    background:{LIME} !important; color:#0b0c0e !important; border:1px solid {LIME} !important;
}}
.st-key-topbar {{
    background:{CARD} !important; border-radius:8px !important; padding:6px 14px !important;
    border:1px solid {EDGE} !important; box-shadow: {SHADOW} !important;
}}

/* ---------- KPI cards ---------- */
.kpi-card {{ background:{CARD}; border:1px solid {EDGE}; border-radius:8px; padding:6px 10px; height:100%; box-shadow:{SHADOW}; margin-bottom:14px; }}
.kpi-label {{ font-size:11px; font-weight:600; color:{TITLE}; margin-bottom:1px; }}
.kpi-bottom {{ display:flex; align-items:flex-end; justify-content:space-between; gap:8px; }}
.kpi-value {{ font-size:18px; font-weight:700; color:{LIME}; white-space:nowrap; }}
.kpi-trend {{ display:flex; align-items:center; gap:4px; margin-top:0px; white-space:nowrap; }}
.kpi-trend .pct {{ font-size:10.5px; font-weight:600; }}
.kpi-trend .vs {{ font-size:9.5px; color:{FAINT}; }}
.kpi-sub {{ font-size:10px; color:{FAINT}; margin-top:1px; }}
.kpi-accent {{ border-top:3px solid var(--acc, {LIME}); }}

.card-title {{ font-size:14px; font-weight:600; color:{TITLE}; margin-bottom:2px; white-space:nowrap; letter-spacing:.01em; }}
.section-title {{ font-size:19px; font-weight:800; color:{INK}; margin: 2px 0 0 0; }}
.section-sub {{ font-size:12.5px; color:{MUTED}; margin-bottom: 8px; }}
.spacer {{ height: 10px; }}
.legend-row {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; }}
.legend-item {{ display:flex; gap:6px; align-items:center; font-size:11px; color:{MUTED}; }}
.legend-dot {{ width:8px; height:8px; border-radius:99px; display:inline-block; }}
.legend-sq {{ width:10px; height:10px; border-radius:2px; display:inline-block; }}
.donut-legend-item {{ display:flex; gap:6px; align-items:center; font-size:11px; font-weight:600; color:{INK}; margin-bottom:8px; }}

.insight-kicker {{ font-size:11px; font-weight:600; color:{LIME}; letter-spacing:0.02em; }}
.insight-headline {{ font-size:14px; font-weight:700; color:{INK}; margin:2px 0; }}
.insight-desc {{ font-size:12px; color:{MUTED}; }}

table.matrix {{ width:100%; border-collapse:collapse; font-size:11.5px; }}
table.matrix th {{ background:{CARD_2}; font-weight:600; color:{MUTED}; padding:5px 4px; text-align:center; font-size:10.5px; }}
table.matrix td {{ border:0.5px solid {BORDER}; height:27px; text-align:center; font-weight:500; color:{INK}; }}

table.simple {{ width:100%; border-collapse:collapse; font-size:12px; }}
table.simple th {{ text-align:left; color:{TITLE}; font-weight:600; padding:6px 8px; font-size:11px; border-bottom:1px solid {LIME_DIM}; background:{CARD_2}; }}
table.simple td {{ padding:5px 8px; border-bottom:1px solid {BORDER}; color:{INK}; }}
table.simple td.num, table.simple th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
table.simple tr.total td {{ font-weight:800; border-top:1px solid {LIME}; background:{LIME}; color:#0b0c0e; }}

.bar-row {{ margin-bottom: 14px; }}
.bar-head {{ display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; }}
.bar-head .lbl {{ color:{MUTED}; }}
.bar-head .val {{ color:{INK}; font-weight:700; }}
.bar-track {{ background:{CARD_2}; height:8px; border-radius:4px; overflow:hidden; }}
.bar-fill {{ height:100%; border-radius:4px; }}

.status-pill {{ padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600; display:inline-block; }}
.chip {{ padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600; background:{CARD_2}; color:{MUTED}; display:inline-block; margin:2px 4px 2px 0; }}

.analyst-card {{ background:{CARD}; border:1px solid {EDGE}; border-radius:8px; padding:14px; text-align:center; box-shadow:{SHADOW}; }}
.analyst-avatar {{
    width:42px; height:42px; border-radius:21px; background:{LIME}; color:#0b0c0e; font-weight:800; font-size:14px;
    display:flex; align-items:center; justify-content:center; margin: 0 auto 8px auto;
}}
</style>
"""


EXTRA = f"""<style>
.page-head {{ display:flex; align-items:flex-end; justify-content:space-between; gap:12px; margin:2px 0 14px 0; }}
.page-title {{ font-size:19px; font-weight:800; color:{INK}; line-height:1.15; }}
.page-sub {{ font-size:12px; color:{MUTED}; margin-top:1px; }}
.page-tag {{ font-size:11px; font-weight:600; color:{MUTED}; background:{CARD}; border:1px solid {BORDER}; border-radius:999px; padding:3px 10px; white-space:nowrap; }}
.note {{ font-size:11.5px; color:{MUTED}; background:{CARD_2}; border-left:3px solid {FAINT}; border-radius:6px; padding:6px 10px; margin:4px 0; }}
.note.warn {{ background:{AMBER_TINT}; border-left-color:{AMBER}; color:#f6d38f; }}
.note.good {{ background:{GREEN_TINT}; border-left-color:{LIME}; color:#d6e98f; }}
.note.bad {{ background:{RED_TINT}; border-left-color:{RED}; color:#f5aaa4; }}
.pill {{ display:inline-block; padding:2px 9px; border-radius:999px; font-size:11px; font-weight:700; white-space:nowrap; }}

.stTabs [data-baseweb="tab-list"] {{ gap:4px; border-bottom:1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{ padding:6px 12px; font-size:12.5px; font-weight:600; color:{MUTED}; }}
.stTabs [aria-selected="true"] {{ color:{LIME} !important; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color:{LIME} !important; }}

.st-key-topbar [data-testid="stPopover"] button {{ width:100%; border-radius:6px !important; background:{CARD_2} !important;
    color:{INK} !important; border:1px solid {BORDER} !important; font-size:12px !important; font-weight:600 !important; padding:5px 10px !important; }}
.st-key-topbar [data-testid="stPopover"] button:hover {{ border-color:{LIME} !important; }}
.st-key-topbar [data-testid="stPopover"] button p {{ color:{INK} !important; }}

.stDownloadButton button, div[class*="st-key-act_"] button {{ border-radius:6px !important; border:1px solid {LIME} !important; color:{LIME} !important; background:transparent !important; font-size:12px !important; font-weight:600 !important; padding:4px 12px !important; }}
.stDownloadButton button:hover, div[class*="st-key-act_"] button:hover {{ background:{LIME_TINT} !important; }}
[data-testid="stDataFrame"] {{ border-radius:6px; overflow:hidden; border:1px solid {BORDER}; }}

@media (max-width:1300px) {{ .st-key-topbar div[data-testid="stButton"] button {{ padding-left:6px !important; padding-right:6px !important; font-size:12px !important; }} }}

/* ---------- Simulator nav highlight (static, no animation): lime outline, filled when active ---------- */
.st-key-topbar .st-key-nav_Simulator div[data-testid="stButton"] button {{ background:{LIME_TINT} !important; color:{LIME} !important; font-weight:800 !important;
    border:1px solid {LIME} !important; box-shadow:0 0 0 1px rgba(181,211,52,.25), 0 0 14px rgba(181,211,52,.18) !important; }}
.st-key-topbar .st-key-nav_Simulator div[data-testid="stButton"] button:hover {{ background:rgba(181,211,52,.2) !important; color:{LIME} !important; }}
.st-key-topbar .st-key-nav_Simulator div[data-testid="stButton"] button p {{ color:inherit !important; font-weight:800 !important; }}
.st-key-topbar .st-key-nav_Simulator div[data-testid="stButton"] button[kind="primary"] {{ background:{LIME} !important; color:#0b0c0e !important; }}
.sim-hero {{ display:flex; align-items:center; justify-content:space-between; gap:18px; padding:14px 22px; border-radius:8px; color:{INK}; margin:2px 0 10px 0;
    background:linear-gradient(100deg,#1d2410 0%,{CARD} 70%); border:1px solid {EDGE}; box-shadow:{SHADOW}; }}
.sim-hero-kicker {{ font-size:10.5px; font-weight:800; letter-spacing:1.4px; color:{LIME}; }}
.sim-hero-title {{ font-size:22px; font-weight:800; line-height:1.15; color:{INK}; }}
.sim-hero-sub {{ font-size:12px; color:{MUTED}; margin-top:2px; max-width:720px; }}
.sim-hero-tag {{ font-size:11px; font-weight:700; color:{LIME}; background:{LIME_TINT}; border:1px solid {LIME_DIM}; border-radius:999px; padding:4px 12px; white-space:nowrap; }}
.sim-cta {{ font-size:12.5px; color:{MUTED}; background:{CARD}; border:1px solid {EDGE}; border-radius:8px; padding:8px 12px; }}
.sim-cta-star {{ color:{LIME}; font-weight:800; }}
div[class*="st-key-act_"] button:disabled {{ opacity:.35 !important; cursor:not-allowed !important; background:transparent !important; }}
.goal-txt {{ font-size:12.5px; color:{INK}; line-height:1.3; }}
.goal-row {{ display:flex; align-items:center; gap:10px; padding:7px 4px; border-bottom:1px solid {BORDER}; font-size:12.5px; }}
.goal-row .lv {{ flex:0 0 200px; font-weight:600; color:{INK}; }} .goal-row .need {{ flex:1; color:{INK}; }}

/* ---------- Overview ---------- */
.st-key-ov_header {{ background:{CARD}; border:1px solid {EDGE}; border-radius:8px; padding:6px 14px 6px 14px; box-shadow:{SHADOW}; margin-bottom:2px; }}
.ov-brand {{ display:flex; align-items:center; gap:10px; min-width:0; height:36px; }}
.ov-brand-badge {{ background:{LIME}; width:32px; height:32px; border-radius:8px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; color:#0b0c0e; font-weight:800; font-size:16px; }}
.ov-brand-title {{ font-size:16px; font-weight:700; color:{TITLE}; line-height:1.15; white-space:nowrap; }}
.ov-brand-sub {{ font-size:10.5px; color:{FAINT}; white-space:nowrap; }}
.st-key-ov_header [data-testid="stSelectbox"] label {{ display:none; }}
.st-key-ov_header div[data-baseweb="select"] > div {{ border-radius:6px !important; font-size:12px !important; min-height:32px !important; }}
.st-key-ov_header [data-baseweb="select"] *, .st-key-ov_header [data-testid="stSelectbox"] input {{ font-size:12.5px !important; }}
.st-key-ov_header [data-testid="stSelectbox"] [role="group"] {{ min-height:32px !important; border-radius:6px !important; }}
.st-key-ov_header [data-testid="stButtonGroup"] button {{ padding:2px 11px !important; min-height:30px !important; }}
.st-key-ov_header [data-testid="stButtonGroup"] button p {{ font-size:12px !important; }}
.ov-filter-cap {{ font-size:9.5px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:{FAINT}; margin-bottom:-2px; }}

.kpi-rail-wrap {{ display:flex; flex-direction:column; height:100%; }}
.kpi-rail {{ display:flex; flex-direction:column; gap:7px; flex:1; }}
/* stretch the rail to the pipeline card's height: every wrapper between the column and the rail fills it */
div[data-testid="stColumn"]:has(.kpi-rail) div:has(.kpi-rail) {{ height:100%; }}
.kpi-rail-card {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.kpi-rail-title {{ font-size:10.5px; font-weight:800; letter-spacing:1.1px; color:{TITLE}; margin:2px 0 5px; }}
.kpi-rail-card {{ background:{CARD}; border:1px solid {EDGE}; border-radius:8px; padding:5px 12px 6px; box-shadow:{SHADOW}; }}
.kpi-rail-value {{ font-size:22px; font-weight:700; color:{LIME}; line-height:1.05; }}
.kpi-rail-label {{ font-size:11px; font-weight:600; color:{INK}; margin-top:2px; }}
.kpi-rail-sub {{ font-size:10px; color:{FAINT}; margin-top:0; }}

.bd-label {{ font-size:9.5px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:{FAINT}; }}
.pipeline-note {{ font-size:10.5px; color:{FAINT}; }}

/* ---------- Simulator · case decision ---------- */
.case-meta {{ font-size:11px; color:{MUTED}; background:{CARD_2}; border-radius:6px; padding:5px 9px; margin:2px 0 4px; }}
.case-meta b {{ color:{LIME}; }}
.case-sec {{ font-size:10px; font-weight:800; letter-spacing:.09em; text-transform:uppercase; color:{TITLE}; margin:8px 0 0; }}
.case-sec.hard {{ color:{RED}; }}
.gauge-wrap svg {{ width:100%; height:auto; display:block; }}
.decision {{ border-left:4px solid var(--tone); padding:4px 0 4px 12px; }}
.decision-title {{ font-size:17px; font-weight:800; color:var(--tone); line-height:1.2; margin-bottom:6px; }}
.decision-steps {{ margin:0; padding-left:18px; font-size:12px; color:{INK}; line-height:1.45; }}
.decision-steps li {{ margin-bottom:3px; }}
.clocks {{ margin-top:8px; border-top:1px solid {BORDER}; padding-top:6px; }}
.clock {{ display:flex; justify-content:space-between; gap:10px; font-size:12px; padding:3px 0; color:{MUTED}; }}
.clock-d {{ color:{INK}; font-weight:700; white-space:nowrap; }}
.clock-n {{ color:{FAINT}; font-weight:500; }}
.wi-row {{ display:flex; justify-content:space-between; gap:10px; font-size:12px; padding:6px 8px; border-radius:6px; color:{MUTED}; border-bottom:1px solid {BORDER}; }}
.wi-row.wi-hit {{ background:{LIME_TINT}; color:{INK}; border-bottom-color:transparent; }}
.wi-row.wi-hit b {{ color:{LIME}; }}
.wi-verb {{ color:{FAINT}; font-weight:600; margin-right:4px; }}
.wi-r {{ white-space:nowrap; }}
.wi-r b {{ color:{INK}; }}
.precedent {{ font-size:12px; color:{MUTED}; margin-top:8px; padding:6px 9px; border-radius:6px; background:{CARD_2}; }}
.precedent b {{ color:{INK}; }}
.esc-row {{ display:grid; grid-template-columns: 1.1fr 1.6fr 1.4fr 0.7fr 1.6fr; gap:10px; align-items:center; font-size:12px; color:{INK};
    padding:6px 4px; border-bottom:1px solid {BORDER}; }}
.esc-id {{ font-weight:800; color:{LIME}; }}
.esc-sub {{ font-size:10.5px; color:{FAINT}; }}
.esc-status {{ font-weight:700; }}
.sb-mini svg {{ display:block; width:100%; height:auto; }}
.sb-foot {{ font-size:9.5px; color:{FAINT}; line-height:1.4; margin-top:8px; }}

table.simple.compact {{ font-size:11.5px; }}
table.simple.compact th {{ padding:4px 7px; font-size:10.5px; white-space:nowrap; }}
table.simple.compact td {{ padding:2px 7px; line-height:1.55; }}
table.simple tr.sub td:first-child {{ padding-left:20px; color:{MUTED}; }}
table.simple tr.grp td:first-child {{ font-weight:700; color:{INK}; }}
</style>"""


def _compact(css):
    return "\n".join(l for l in css.splitlines() if l.strip())


def inject_css(css):
    """Inject a <style> block without going through Markdown (Markdown can end an HTML block early and print CSS as text)."""
    st.html('<span class="fit-css"></span>' + _compact(css))


HIDE_CSS = """<style>
div[data-testid="stElementContainer"]:has(.fit-css), .element-container:has(.fit-css) { display:none !important; }
</style>"""


def widget_dark_css():
    """Fallback when .streamlit/config.toml is missing (for example when the repo was uploaded by drag-and-drop
    on GitHub, which skips dot-folders): force Streamlit's own widgets onto the dark palette so the app still
    looks like the screenshots. With the config file present this only repeats what the theme already does."""
    return f"""<style>
[data-testid="stSelectbox"] [role="group"], [data-testid="stNumberInput"] input, [data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] {{
    background:{CARD_2} !important; color:{INK} !important; border-color:{BORDER} !important; }}
[data-testid="stSelectbox"] input, [data-testid="stSelectbox"] svg, [data-testid="stNumberInput"] button svg {{ color:{INK} !important; fill:{INK} !important; }}
[data-baseweb="popover"] li, [data-baseweb="menu"], [role="listbox"] {{ background:{CARD} !important; color:{INK} !important; }}
[data-baseweb="popover"] li:hover, [role="option"]:hover {{ background:{CARD_2} !important; }}
[data-testid="stButtonGroup"] button {{ background:{CARD_2} !important; color:{MUTED} !important; border-color:{BORDER} !important; }}
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[aria-selected="true"] {{
    background:{LIME_TINT} !important; color:{LIME} !important; border-color:{LIME} !important; }}
[data-testid="stNumberInput"] button {{ background:{CARD_2} !important; border-color:{BORDER} !important; }}
[data-testid="stDataFrame"], [data-testid="stDataFrame"] * {{ color-scheme: dark; }}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{ background:{LIME} !important; }}
[data-testid="stTooltipContent"], [data-baseweb="tooltip"] {{ background:{CARD} !important; color:{INK} !important; }}
label, .stMarkdown p {{ color:{MUTED}; }}
</style>"""


def _theme_is_dark():
    try:
        return (st.get_option("theme.base") or "").lower() == "dark"
    except Exception:
        return False


def apply_theme():
    css = HIDE_CSS + base_css() + EXTRA
    if not _theme_is_dark():                 # no .streamlit/config.toml (or a light theme): dress the widgets ourselves
        css += widget_dark_css()
    inject_css(css)
