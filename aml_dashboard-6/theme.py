"""
theme.py
Shared visual theme helpers for the AML Compliance Suite.

DARK MODE v3 — deep-space navy background with an animated aurora glow,
frosted-glass ("glassmorphism") cards, layered neon-adjacent shadows for a
3D "floating panel" feel, and a cyan/teal accent that pops against the
dark surface. Every Plotly chart gets a shared dark layout with unified
hover, spike lines, smooth transitions, and a subtle "lift + glow" on
hover so the whole suite reads as interactive, not static.

Backwards-compatibility aliases (NAVY, BRASS, INK, MUTED, PAPER, PANEL,
BORDER) are kept so older pages that reference the previous palette
keep working without edits.
"""

import textwrap
import streamlit as st

# ---------------------------------------------------------------- PALETTE
# Deep space navy backdrop, layered so the aurora glow has room to breathe.
BG_GRADIENT_1 = "#060B14"
BG_GRADIENT_2 = "#0B1524"
BG_GRADIENT_3 = "#0E1B2E"

# Frosted glass cards — semi-transparent so the aurora glow shows through,
# combined with backdrop-filter blur (applied in CSS below).
CARD_BG        = "rgba(20, 30, 48, 0.62)"
CARD_BG_SOLID  = "#121D2E"
CARD_BORDER    = "rgba(148, 178, 214, 0.16)"
CARD_BORDER_HI = "rgba(45, 212, 191, 0.45)"

# Layered shadows: a soft dark drop shadow for depth + a faint accent glow
# so cards feel like they're floating just above the background.
CARD_SHADOW   = "0 8px 24px rgba(0, 0, 0, 0.45), 0 1px 0 rgba(255,255,255,0.03) inset"
CHART_SHADOW       = ("0 22px 45px rgba(0, 0, 0, 0.55), "
                       "0 4px 14px rgba(0, 0, 0, 0.35), "
                       "0 0 0 1px rgba(148,178,214,0.08), "
                       "0 0 32px rgba(45, 212, 191, 0.06)")
CHART_SHADOW_HOVER = ("0 32px 64px rgba(0, 0, 0, 0.65), "
                       "0 8px 20px rgba(0, 0, 0, 0.4), "
                       "0 0 0 1px rgba(45,212,191,0.35), "
                       "0 0 46px rgba(45, 212, 191, 0.28)")

# Accent ramp — bright cyan/teal that glows on a dark surface.
TEAL_DARK     = "#2DD4BF"   # primary accent (was the "dark" corporate teal)
TEAL_MID      = "#22D3EE"   # secondary accent, slightly more blue
TEAL_LIGHT    = "#67E8CE"
TEAL_PALE     = "#99F0DF"
TEAL_SOFT     = "rgba(45, 212, 191, 0.14)"

TEXT_PRIMARY  = "#E7EDF5"
TEXT_MUTED    = "#8FA1BC"
TEXT_ALERT    = "#FB7185"

CRITICAL      = "#FB7185"
HIGH          = "#FB923C"
MEDIUM        = "#FBBF24"
LOW           = "#34D399"
INFO          = "#38BDF8"

CHART_GRID    = "rgba(148, 178, 214, 0.12)"
CHART_SEQ     = ["#2DD4BF", "#38BDF8", "#A78BFA", "#FB923C", "#34D399", "#22D3EE",
                 "#FBBF24", "#FB7185", "#67E8CE", "#818CF8"]

CHART_SEQ_EXT = [
    "#2DD4BF", "#38BDF8", "#A78BFA", "#FB923C", "#34D399", "#22D3EE",
    "#FBBF24", "#FB7185", "#67E8CE", "#818CF8", "#F472B6", "#4ADE80",
]

RISK_COLOR_MAP = {
    "Low":      LOW,
    "Medium":   MEDIUM,
    "High":     HIGH,
    "Critical": CRITICAL,
}

MAP_COLOR     = "#3D5F78"
MAP_OPACITY   = "0.5"


# --------------------------------------------------------------------------
# BACKWARDS-COMPAT ALIASES
# --------------------------------------------------------------------------
NAVY      = TEAL_DARK
NAVY_DARK = TEAL_DARK
BRASS     = TEAL_LIGHT
INK       = TEXT_PRIMARY
MUTED     = TEXT_MUTED
PAPER     = CARD_BG
PANEL     = BG_GRADIENT_2
BORDER    = CARD_BORDER


# --------------------------------------------------------------------------
# WORLD MAP SVG WATERMARK
# --------------------------------------------------------------------------
_WORLD_MAP_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1000"
     preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;">
  <defs>
    <pattern id="dots" x="0" y="0" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.1" fill="COLOR"/>
    </pattern>
    <radialGradient id="fade" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#060B14" stop-opacity="0"/>
      <stop offset="70%" stop-color="#060B14" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#060B14" stop-opacity="0.96"/>
    </radialGradient>
  </defs>
  <g opacity="0.55">
    <path d="M180,220 C260,180 380,170 470,200 C520,220 540,270 520,330
             C500,390 440,430 370,440 C300,450 220,420 190,360
             C160,300 150,250 180,220 Z" fill="url(#dots)"/>
    <path d="M420,520 C480,510 540,540 560,600 C580,670 560,760 520,830
             C490,890 440,910 410,870 C380,820 380,740 390,660
             C395,600 400,560 420,520 Z" fill="url(#dots)"/>
    <path d="M900,180 C960,170 1030,180 1060,220 C1080,260 1060,310 1010,330
             C960,350 900,340 870,300 C850,260 860,200 900,180 Z" fill="url(#dots)"/>
    <path d="M920,400 C990,390 1080,410 1110,480 C1140,560 1120,680 1060,760
             C1020,810 960,820 930,770 C900,710 890,620 890,540
             C890,470 900,420 920,400 Z" fill="url(#dots)"/>
    <path d="M1120,200 C1250,180 1420,190 1520,240 C1620,300 1680,400 1650,480
             C1620,560 1540,600 1440,600 C1340,600 1240,560 1180,500
             C1120,440 1090,320 1120,200 Z" fill="url(#dots)"/>
    <path d="M1520,700 C1590,690 1680,710 1710,760 C1740,810 1700,860 1630,870
             C1560,880 1480,850 1460,800 C1440,760 1470,710 1520,700 Z" fill="url(#dots)"/>
  </g>
  <g fill="none" stroke="COLOR" stroke-width="1.1" opacity="0.55" stroke-dasharray="3 5">
    <path d="M320,320 Q600,120 960,260"/>
    <path d="M960,260 Q1300,180 1560,420"/>
    <path d="M960,260 Q900,520 950,600"/>
    <path d="M320,320 Q620,560 950,600"/>
    <path d="M1560,420 Q1650,600 1640,780"/>
    <path d="M950,600 Q1200,700 1640,780"/>
    <path d="M320,320 Q240,500 430,600"/>
  </g>
  <g fill="COLOR" opacity="0.9">
    <circle cx="320"  cy="320" r="4.5"/>
    <circle cx="960"  cy="260" r="5.5"/>
    <circle cx="1560" cy="420" r="4.5"/>
    <circle cx="950"  cy="600" r="4"/>
    <circle cx="430"  cy="600" r="3.5"/>
    <circle cx="1640" cy="780" r="4"/>
  </g>
  <rect width="2000" height="1000" fill="url(#fade)"/>
</svg>
"""


# --------------------------------------------------------------------------
# CSS TEMPLATE
# --------------------------------------------------------------------------
_CSS_TEMPLATE = """<style>
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: {TEXT_PRIMARY};
}}

/* ---------------------------------------------------------------
   ANIMATED AURORA BACKGROUND
   A slow-drifting radial-gradient wash behind everything, giving the
   dark theme depth and a subtle sense of motion without being noisy.
--------------------------------------------------------------- */
@keyframes auroraDrift {{
    0%   {{ background-position: 0% 0%, 100% 100%, 50% 50%; }}
    50%  {{ background-position: 100% 30%, 0% 70%, 60% 40%; }}
    100% {{ background-position: 0% 0%, 100% 100%, 50% 50%; }}
}}
.stApp {{
    background-color: {BG_GRADIENT_1};
    background-image:
        radial-gradient(circle at 15% 15%, rgba(45,212,191,0.10) 0%, transparent 45%),
        radial-gradient(circle at 85% 80%, rgba(56,189,248,0.09) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(167,139,250,0.05) 0%, transparent 60%),
        linear-gradient(180deg, {BG_GRADIENT_1} 0%, {BG_GRADIENT_2} 55%, {BG_GRADIENT_3} 100%);
    background-size: 200% 200%, 200% 200%, 200% 200%, 100% 100%;
    background-attachment: fixed;
    animation: auroraDrift 34s ease-in-out infinite;
}}
.ampl-map-bg {{
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
    opacity: {MAP_OPACITY};
}}
section.main > div,
section.main .block-container,
section[data-testid="stAppViewContainer"] > .main {{
    position: relative; z-index: 1;
}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.block-container {{ padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1280px; }}
h1, h2, h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK}; font-weight: 600;
}}
::selection {{ background: rgba(45,212,191,0.35); color: #FFFFFF; }}

/* ---------------------------------------------------------------
   HEADER — glass panel with an accent glow edge
--------------------------------------------------------------- */
.suite-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.3rem 1.8rem;
    background: {CARD_BG};
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW}, 0 0 26px rgba(45,212,191,0.10);
    border-radius: 10px;
    margin-bottom: 1.6rem;
}}
.suite-header h1 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.55rem; font-weight: 700;
    margin: 0; color: #F5FAFA;
    text-shadow: 0 0 22px rgba(45,212,191,0.35);
}}
.suite-header p {{
    margin: 0.3rem 0 0 0;
    color: {TEXT_MUTED}; font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
}}
.suite-badge {{
    background: {TEAL_SOFT}; color: {TEAL_PALE};
    border: 1px solid {CARD_BORDER_HI};
    padding: 0.3rem 0.9rem; border-radius: 20px;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    white-space: nowrap;
    box-shadow: 0 0 16px rgba(45,212,191,0.25);
}}

/* ---------------------------------------------------------------
   KPI CARDS — glass + lift + glow on hover (the "3D" feel)
--------------------------------------------------------------- */
.kpi-card {{
    background: {CARD_BG};
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    border-radius: 10px;
    padding: 1rem 1.2rem; height: 100%;
    transition: box-shadow 0.25s ease, transform 0.25s ease, border-color 0.25s ease;
    transform-style: preserve-3d;
}}
.kpi-card:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    border-color: {CARD_BORDER_HI};
    transform: translateY(-4px) perspective(600px) rotateX(2deg);
}}
.kpi-label {{
    color: {TEXT_MUTED};
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.09em; font-weight: 600;
    margin-bottom: 0.45rem;
}}
.kpi-value {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: #F5FAFA;
    font-size: 1.9rem; font-weight: 700;
    line-height: 1.1; letter-spacing: -0.01em;
    text-shadow: 0 0 18px rgba(45,212,191,0.25);
}}
.kpi-sub {{
    font-size: 0.76rem; margin-top: 0.4rem;
    color: {TEXT_MUTED};
}}

.section-title {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.1rem; font-weight: 700;
    color: #F5FAFA;
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(45,212,191,0.35);
    text-shadow: 0 0 14px rgba(45,212,191,0.18);
}}
.section-toolbar {{
    display: flex; align-items: flex-end; justify-content: space-between;
    gap: 1rem;
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid rgba(45,212,191,0.35);
}}
.section-toolbar .section-title {{
    margin: 0; padding: 0; border: none;
}}

/* ---------------------------------------------------------------
   ELEVATED, INTERACTIVE CHART CARDS
   Deep layered shadow + faint glow ring so every chart on every
   page reads as a floating glass panel; a stronger hover state
   (lift + brighter glow + slight scale) makes hovering feel alive.
--------------------------------------------------------------- */
div[data-testid="stPlotlyChart"] {{
    background: {CARD_BG};
    backdrop-filter: blur(16px) saturate(140%);
    -webkit-backdrop-filter: blur(16px) saturate(140%);
    border: 1px solid {CARD_BORDER};
    border-radius: 12px;
    box-shadow: {CHART_SHADOW};
    padding: 0.9rem 1rem 0.3rem 1rem;
    transition: box-shadow 0.3s cubic-bezier(.22,1,.36,1),
                transform 0.3s cubic-bezier(.22,1,.36,1),
                border-color 0.3s ease;
}}
div[data-testid="stPlotlyChart"]:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    border-color: {CARD_BORDER_HI};
    transform: translateY(-5px) scale(1.004);
}}
div[data-testid="stPlotlyChart"] .plotly {{
    border-radius: 8px;
}}

.pill {{
    display: inline-block;
    padding: 0.18rem 0.65rem;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.04em; text-transform: uppercase;
    border-radius: 20px; border: 1px solid;
}}
.pill-critical {{ background: rgba(251,113,133,0.14); color: {CRITICAL}; border-color: rgba(251,113,133,0.4); box-shadow: 0 0 12px rgba(251,113,133,0.18); }}
.pill-high     {{ background: rgba(251,146,60,0.14);  color: {HIGH};     border-color: rgba(251,146,60,0.4);  box-shadow: 0 0 12px rgba(251,146,60,0.18); }}
.pill-medium   {{ background: rgba(251,191,36,0.14);  color: {MEDIUM};   border-color: rgba(251,191,36,0.4);  box-shadow: 0 0 12px rgba(251,191,36,0.18); }}
.pill-low      {{ background: rgba(52,211,153,0.14);  color: {LOW};      border-color: rgba(52,211,153,0.4);  box-shadow: 0 0 12px rgba(52,211,153,0.18); }}
.pill-info     {{ background: {TEAL_SOFT}; color: {TEAL_PALE}; border-color: {CARD_BORDER_HI}; box-shadow: 0 0 12px rgba(45,212,191,0.18); }}

div[data-testid="stMetric"] {{
    background: {CARD_BG};
    backdrop-filter: blur(14px);
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 0.9rem 1.05rem; border-radius: 10px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}}
div[data-testid="stMetric"]:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    transform: translateY(-3px);
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: #F5FAFA; font-weight: 700;
    text-shadow: 0 0 16px rgba(45,212,191,0.3);
}}
div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED}; text-transform: uppercase;
    font-size: 0.72rem; letter-spacing: 0.07em; font-weight: 600;
}}

table {{
    border-collapse: collapse; width: 100%;
    font-size: 0.85rem; background: {CARD_BG_SOLID};
    border: 1px solid {CARD_BORDER};
    box-shadow: {CARD_SHADOW};
    border-radius: 8px; overflow: hidden;
}}
table thead th {{
    background: linear-gradient(90deg, #0D2530 0%, #123645 100%);
    color: {TEAL_PALE};
    text-align: left; padding: 0.6rem 0.75rem;
    font-weight: 600; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.05em;
    border-bottom: 1px solid rgba(45,212,191,0.3);
}}
table tbody td {{
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid {CHART_GRID};
    color: {TEXT_PRIMARY};
}}
table tbody tr:nth-child(even) {{ background: rgba(255,255,255,0.02); }}
table tbody tr:hover {{ background: rgba(45,212,191,0.08); }}

.stTabs [data-baseweb="tab-list"] {{
    gap: 2px; border-bottom: 1px solid {CARD_BORDER};
    background: transparent;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent; border-radius: 8px 8px 0 0;
    padding: 0.65rem 1.15rem; font-weight: 600;
    color: {TEXT_MUTED}; font-size: 0.88rem;
    transition: color 0.2s ease, background 0.2s ease;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {TEAL_LIGHT}; background: {TEAL_SOFT};
}}
.stTabs [aria-selected="true"] {{
    color: #F5FAFA !important;
    border-bottom: 3px solid {TEAL_DARK} !important;
    background: transparent !important;
    text-shadow: 0 0 12px rgba(45,212,191,0.4);
}}

.stButton>button, .stDownloadButton>button {{
    border-radius: 8px;
    border: 1px solid {CARD_BORDER_HI};
    background: rgba(45,212,191,0.06);
    color: {TEAL_PALE}; font-weight: 600;
    font-size: 0.86rem;
    transition: all 0.2s ease;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {TEAL_SOFT}; border-color: {TEAL_DARK};
    color: #FFFFFF;
    box-shadow: 0 0 18px rgba(45,212,191,0.35);
    transform: translateY(-1px);
}}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] {{
    background: linear-gradient(135deg, {TEAL_DARK}, {TEAL_MID});
    border-color: {TEAL_DARK};
    color: #06131A; font-weight: 700;
}}
.stButton>button[kind="primary"]:hover {{
    box-shadow: 0 0 24px rgba(45,212,191,0.5);
    transform: translateY(-1px);
}}

/* ---------------------------------------------------------------
   SEGMENTED TOOLBAR CONTROLS (st.radio as pill toggles)
--------------------------------------------------------------- */
div[data-testid="stRadio"] > div {{
    gap: 0.3rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid {CARD_BORDER};
    border-radius: 20px;
    padding: 0.2rem;
    display: inline-flex;
}}
div[data-testid="stRadio"] label {{
    background: transparent;
    border-radius: 16px;
    padding: 0.2rem 0.75rem !important;
    margin: 0 !important;
    font-size: 0.76rem !important;
    color: {TEXT_MUTED};
    transition: all 0.2s ease;
}}
div[data-testid="stRadio"] label:hover {{
    background: rgba(255,255,255,0.06);
    color: {TEAL_LIGHT};
}}
div[data-testid="stRadio"] label:has(input:checked) {{
    background: linear-gradient(135deg, {TEAL_DARK}, {TEAL_MID});
    box-shadow: 0 2px 14px rgba(45,212,191,0.45);
}}
div[data-testid="stRadio"] label:has(input:checked) p {{
    color: #06131A !important; font-weight: 700;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0A1220 0%, #0D1A2B 100%);
    border-right: 1px solid {CARD_BORDER};
}}
section[data-testid="stSidebar"] h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1rem; color: {TEAL_DARK}; font-weight: 700;
}}
section[data-testid="stSidebar"] label {{
    color: {TEXT_MUTED}; font-size: 0.8rem; font-weight: 600;
}}

.stTextInput input, .stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {{
    border-radius: 8px; border-color: {CARD_BORDER};
    background: rgba(255,255,255,0.03); color: {TEXT_PRIMARY};
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {TEAL_MID} !important;
    box-shadow: 0 0 0 2px rgba(34,211,238,0.35) !important;
}}

div[data-testid="stAlert"] {{
    border-radius: 8px; border-left: 4px solid {TEAL_DARK};
    background: {CARD_BG}; backdrop-filter: blur(10px);
    box-shadow: {CARD_SHADOW};
}}
hr {{ border-color: {CARD_BORDER}; margin: 1.5rem 0; }}
</style>"""


# --------------------------------------------------------------------------
# CSS INJECTION
# --------------------------------------------------------------------------
def inject_css():
    """Inject the stylesheet AND the world-map watermark background."""
    map_svg = _WORLD_MAP_SVG.replace("COLOR", MAP_COLOR)
    st.markdown(
        f'<div class="ampl-map-bg">{map_svg}</div>',
        unsafe_allow_html=True,
    )

    css = _CSS_TEMPLATE.format(
        TEXT_PRIMARY=TEXT_PRIMARY,
        TEXT_MUTED=TEXT_MUTED,
        BG_GRADIENT_1=BG_GRADIENT_1,
        BG_GRADIENT_2=BG_GRADIENT_2,
        BG_GRADIENT_3=BG_GRADIENT_3,
        CARD_BG=CARD_BG,
        CARD_BG_SOLID=CARD_BG_SOLID,
        CARD_BORDER=CARD_BORDER,
        CARD_BORDER_HI=CARD_BORDER_HI,
        CARD_SHADOW=CARD_SHADOW,
        CHART_SHADOW=CHART_SHADOW,
        CHART_SHADOW_HOVER=CHART_SHADOW_HOVER,
        TEAL_DARK=TEAL_DARK,
        TEAL_MID=TEAL_MID,
        TEAL_LIGHT=TEAL_LIGHT,
        TEAL_PALE=TEAL_PALE,
        TEAL_SOFT=TEAL_SOFT,
        CRITICAL=CRITICAL,
        HIGH=HIGH,
        MEDIUM=MEDIUM,
        LOW=LOW,
        INFO=INFO,
        CHART_GRID=CHART_GRID,
        MAP_OPACITY=MAP_OPACITY,
    )
    st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


# --------------------------------------------------------------------------
# UI HELPERS
# --------------------------------------------------------------------------
def page_header(title: str, subtitle: str = "", badge: str = ""):
    badge_html = f'<span class="suite-badge">{badge}</span>' if badge else ""
    html = f"""<div class="suite-header">
<div><h1>{title}</h1><p>{subtitle}</p></div>
{badge_html}
</div>"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", sub_color: str = TEXT_MUTED):
    html = f"""<div class="kpi-card">
<div class="kpi-label">{label}</div>
<div class="kpi-value">{value}</div>
<div class="kpi-sub" style="color:{sub_color};">{sub}</div>
</div>"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


def risk_pill(level: str) -> str:
    level_l = (level or "").lower()
    cls = {
        "critical": "pill-critical",
        "high": "pill-high",
        "medium": "pill-medium",
        "low": "pill-low",
    }.get(level_l, "pill-info")
    return f'<span class="pill {cls}">{level}</span>'


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def section_toolbar(title: str, control_fn=None):
    """
    Render a section title with an interactive control anchored at the
    top of the section, above any chart or table beneath it.

    `control_fn` is a zero-arg callable that renders a Streamlit widget
    (e.g. a lambda calling st.radio(...)) and returns its value. The
    control is rendered inside a right-aligned column on the same row
    as the title, so it visually reads as the section's toolbar.

    Usage:
        value = section_toolbar(
            "Transaction Volume Trend",
            lambda: st.radio("Window", ["30D", "90D", "180D"],
                              index=1, horizontal=True,
                              label_visibility="collapsed"),
        )
    """
    title_col, control_col = st.columns([2.4, 1])
    with title_col:
        st.markdown(
            f'<div class="section-title" style="margin-top:1.8rem;">{title}</div>',
            unsafe_allow_html=True,
        )
    result = None
    if control_fn is not None:
        with control_col:
            st.markdown('<div style="margin-top:2.05rem;"></div>', unsafe_allow_html=True)
            result = control_fn()
    return result


# --------------------------------------------------------------------------
# CHART STYLE HELPERS
# --------------------------------------------------------------------------
def chart_layout_2d(height: int = 340, title: str = "") -> dict:
    """
    Base layout for 2D charts on the dark theme: fully transparent bg
    (so the frosted glass card shows through), pale-on-dark gridlines,
    unified hover with spike lines for a genuinely interactive feel,
    and a smooth transition so re-sorted / re-windowed data animates
    in rather than snapping.
    """
    layout = dict(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        margin=dict(t=40 if title else 10, b=10, l=10, r=10),
        height=height,
        hovermode="x unified",
        hoverdistance=40,
        transition=dict(duration=450, easing="cubic-in-out"),
        uniformtext=dict(minsize=9, mode="hide"),
        xaxis=dict(
            gridcolor=CHART_GRID,
            zerolinecolor=CHART_GRID,
            linecolor=CARD_BORDER,
            tickfont=dict(color=TEXT_MUTED, size=11),
            title_font=dict(color=TEXT_MUTED, size=11),
            showspikes=True,
            spikecolor=TEAL_MID,
            spikethickness=1,
            spikedash="dot",
            spikemode="across",
        ),
        yaxis=dict(
            gridcolor=CHART_GRID,
            zerolinecolor=CHART_GRID,
            linecolor=CARD_BORDER,
            tickfont=dict(color=TEXT_MUTED, size=11),
            title_font=dict(color=TEXT_MUTED, size=11),
        ),
        legend=dict(
            font=dict(color=TEXT_PRIMARY, size=11),
            bgcolor="rgba(18,29,46,0.75)",
            bordercolor=CARD_BORDER,
            borderwidth=1,
        ),
        hoverlabel=dict(
            bgcolor="#0F1B2D",
            bordercolor=TEAL_MID,
            font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        ),
    )
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(family="Source Serif 4, Georgia, serif",
                      size=15, color=TEAL_PALE),
            x=0.01, xanchor="left", y=0.97,
        )
    return layout


def chart_layout_3d(height: int = 500, title: str = "") -> dict:
    """Base layout for 3D charts: transparent bg, glowing dark scene."""
    layout = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=11),
        margin=dict(t=40 if title else 10, b=10, l=10, r=10),
        height=height,
        transition=dict(duration=450, easing="cubic-in-out"),
        scene=dict(
            xaxis=dict(
                backgroundcolor="rgba(45,212,191,0.03)",
                gridcolor=CHART_GRID,
                zerolinecolor=CHART_GRID,
                showbackground=True,
                tickfont=dict(color=TEXT_MUTED, size=10),
                title_font=dict(color=TEXT_MUTED, size=11),
            ),
            yaxis=dict(
                backgroundcolor="rgba(56,189,248,0.03)",
                gridcolor=CHART_GRID,
                zerolinecolor=CHART_GRID,
                showbackground=True,
                tickfont=dict(color=TEXT_MUTED, size=10),
                title_font=dict(color=TEXT_MUTED, size=11),
            ),
            zaxis=dict(
                backgroundcolor="rgba(167,139,250,0.03)",
                gridcolor=CHART_GRID,
                zerolinecolor=CHART_GRID,
                showbackground=True,
                tickfont=dict(color=TEXT_MUTED, size=10),
                title_font=dict(color=TEXT_MUTED, size=11),
            ),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        ),
        hoverlabel=dict(
            bgcolor="#0F1B2D",
            bordercolor=TEAL_MID,
            font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        ),
    )
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(family="Source Serif 4, Georgia, serif",
                      size=15, color=TEAL_PALE),
            x=0.01, xanchor="left", y=0.97,
        )
    return layout


def plotly_layout_defaults() -> dict:
    """Backwards-compat alias for older pages."""
    return chart_layout_2d()


def chart_color_sequence():
    return CHART_SEQ


def chart_color_sequence_ext():
    return CHART_SEQ_EXT


def apply_shadow(fig, marker=True, bar=True):
    """Add subtle glow-edged borders to bars/scatter markers for depth."""
    if bar:
        fig.update_traces(
            marker=dict(line=dict(width=0.6, color="rgba(255,255,255,0.15)")),
            selector=dict(type="bar"),
        )
    if marker:
        fig.update_traces(
            marker=dict(line=dict(width=0.6, color="rgba(255,255,255,0.25)")),
            selector=dict(type="scatter"),
        )
    return fig


def enable_rich_interaction(fig, hover_glow: bool = True):
    """
    Apply a shared set of "make it feel alive" interaction settings to any
    figure: unified hover with spikes already come from chart_layout_2d,
    this layers on click-to-toggle legends, a visible modebar with the
    zoom/pan/reset tools, and (optionally) a slight marker glow that
    brightens on hover via opacity contrast.
    """
    fig.update_layout(
        hoverlabel_align="left",
        legend=dict(itemclick="toggleothers", itemdoubleclick="toggle"),
    )
    if hover_glow:
        fig.update_traces(marker=dict(opacity=0.92), selector=dict(type="bar"))
    return fig


PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "scrollZoom": True,
}


# --------------------------------------------------------------------------
# COLOR HARMONY HELPERS
# --------------------------------------------------------------------------
def _hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in rgb)


def interpolate_color(c1: str, c2: str, t: float) -> str:
    """Linear-interpolate between two hex colors at t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    return _rgb_to_hex((r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t))


def teal_gradient(values, dark: str = TEAL_DARK, light: str = TEAL_PALE):
    """
    Map a numeric sequence onto a single-hue teal/cyan ramp (pale -> bright
    accent as the value rises) so non-semantic bar/line charts still read
    as part of the same glowing accent family as the rest of the dark
    dashboard, while the shading reinforces value magnitude.
    """
    values = list(values)
    if not values:
        return []
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1
    return [interpolate_color(light, dark, (v - vmin) / span) for v in values]


def teal_gradient_reversed(values, dark: str = TEAL_DARK, light: str = TEAL_PALE):
    """Same as teal_gradient but brightest at the low end (for "smaller is
    better" metrics where you still want visual weight on the largest bar)."""
    return list(reversed(teal_gradient(list(reversed(list(values))), dark, light)))                                           
