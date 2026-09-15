"""
theme.py
Shared visual theme helpers for the AML Compliance Suite.

WARM LIGHT MODE v4 — teal / cream / brown / white palette. Soft cream
background with a gentle teal-and-brown wash, crisp white glass cards,
warm brown-toned shadows (instead of harsh black) for real depth, and a
deep teal accent that reads as premium rather than corporate-flat.

Charts get genuine dimensionality rather than solid flat bars:
- `apply_3d_bar_caps()` adds a lighter "lid" strip on top of every bar
  (or at the far edge of horizontal bars) to fake a beveled, extruded
  box look under a top-down light source.
- `apply_gradient_fill()` uses Plotly's native vertical fillgradient so
  area charts shade smoothly from a saturated top to a soft, pale base
  instead of a single flat fill color.
- Every chart still gets unified hover, spike lines, a visible
  zoom/pan/reset modebar, legend click-to-isolate, and a smooth
  transition on re-render.

Backwards-compatibility aliases (NAVY, BRASS, INK, MUTED, PAPER, PANEL,
BORDER) are kept so older pages that reference the previous palette
keep working without edits.
"""

import textwrap
import streamlit as st

# ---------------------------------------------------------------- PALETTE
# Warm cream backdrop, layered so the teal/brown wash has room to breathe.
BG_GRADIENT_1 = "#FBF6EC"
BG_GRADIENT_2 = "#F5ECDA"
BG_GRADIENT_3 = "#EFE3CC"

# Crisp glass-white cards — slightly translucent so the warm wash shows
# through, combined with backdrop-filter blur (applied in CSS below).
CARD_BG        = "rgba(255, 255, 255, 0.80)"
CARD_BG_SOLID  = "#FFFFFF"
CARD_BORDER    = "rgba(139, 94, 60, 0.18)"
CARD_BORDER_HI = "rgba(31, 111, 111, 0.45)"

# Warm brown-toned shadows (not black) for a soft, tactile depth, plus a
# faint teal glow ring so cards feel lit from the accent color.
CARD_SHADOW   = "0 8px 22px rgba(107, 74, 50, 0.14), 0 1px 0 rgba(255,255,255,0.7) inset"
CHART_SHADOW       = ("0 20px 42px rgba(107, 74, 50, 0.20), "
                       "0 4px 12px rgba(75, 50, 30, 0.12), "
                       "0 0 0 1px rgba(139,94,60,0.10), "
                       "0 0 26px rgba(31, 111, 111, 0.10)")
CHART_SHADOW_HOVER = ("0 30px 58px rgba(107, 74, 50, 0.26), "
                       "0 8px 18px rgba(75, 50, 30, 0.16), "
                       "0 0 0 1px rgba(31,111,111,0.4), "
                       "0 0 38px rgba(31, 111, 111, 0.24)")

# Accent ramp — deep teal as the primary accent, warm brown as the
# secondary, both legible on cream/white.
TEAL_DARK     = "#1F6F6F"
TEAL_MID      = "#2E8B8B"
TEAL_LIGHT    = "#6FB8B8"
TEAL_PALE     = "#BEE3E3"
TEAL_SOFT     = "rgba(31, 111, 111, 0.12)"

BROWN_DARK    = "#4A3222"
BROWN_MID     = "#6B4A32"
BROWN_LIGHT   = "#9C7B5C"
BROWN_PALE    = "#E4D3B8"
BROWN_SOFT    = "rgba(107, 74, 50, 0.12)"

TEXT_PRIMARY  = "#3B2A1E"
TEXT_MUTED    = "#8C7B6B"
TEXT_ALERT    = "#B0413E"

CRITICAL      = "#B0413E"
HIGH          = "#C1702E"
MEDIUM        = "#A9822B"
LOW           = "#3F7D5C"
INFO          = "#2E8B8B"

CHART_GRID    = "rgba(139, 94, 60, 0.14)"
CHART_SEQ     = ["#1F6F6F", "#6B4A32", "#2E8B8B", "#9C7B5C", "#3F7D5C", "#C1702E",
                 "#A9822B", "#B0413E", "#6FB8B8", "#4A3222"]

CHART_SEQ_EXT = [
    "#1F6F6F", "#6B4A32", "#2E8B8B", "#9C7B5C", "#3F7D5C", "#C1702E",
    "#A9822B", "#B0413E", "#6FB8B8", "#4A3222", "#8FA98C", "#D9A15B",
]

RISK_COLOR_MAP = {
    "Low":      LOW,
    "Medium":   MEDIUM,
    "High":     HIGH,
    "Critical": CRITICAL,
}

MAP_COLOR     = "#9C7B5C"
MAP_OPACITY   = "0.30"


# --------------------------------------------------------------------------
# BACKWARDS-COMPAT ALIASES
# --------------------------------------------------------------------------
NAVY      = TEAL_DARK
NAVY_DARK = TEAL_DARK
BRASS     = BROWN_MID
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
      <stop offset="0%" stop-color="#FBF6EC" stop-opacity="0"/>
      <stop offset="70%" stop-color="#FBF6EC" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#FBF6EC" stop-opacity="0.97"/>
    </radialGradient>
  </defs>
  <g opacity="0.5">
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
  <g fill="none" stroke="COLOR" stroke-width="1.1" opacity="0.4" stroke-dasharray="3 5">
    <path d="M320,320 Q600,120 960,260"/>
    <path d="M960,260 Q1300,180 1560,420"/>
    <path d="M960,260 Q900,520 950,600"/>
    <path d="M320,320 Q620,560 950,600"/>
    <path d="M1560,420 Q1650,600 1640,780"/>
    <path d="M950,600 Q1200,700 1640,780"/>
    <path d="M320,320 Q240,500 430,600"/>
  </g>
  <g fill="COLOR" opacity="0.75">
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
   SLOW-DRIFTING WARM WASH BACKGROUND
   Soft teal + brown radial washes over a cream base, giving the
   light theme depth and gentle motion without looking neon.
--------------------------------------------------------------- */
@keyframes washDrift {{
    0%   {{ background-position: 0% 0%, 100% 100%, 50% 50%; }}
    50%  {{ background-position: 100% 30%, 0% 70%, 60% 40%; }}
    100% {{ background-position: 0% 0%, 100% 100%, 50% 50%; }}
}}
.stApp {{
    background-color: {BG_GRADIENT_1};
    background-image:
        radial-gradient(circle at 12% 12%, rgba(31,111,111,0.10) 0%, transparent 45%),
        radial-gradient(circle at 88% 82%, rgba(107,74,50,0.09) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(212,177,109,0.07) 0%, transparent 60%),
        linear-gradient(180deg, {BG_GRADIENT_1} 0%, {BG_GRADIENT_2} 55%, {BG_GRADIENT_3} 100%);
    background-size: 200% 200%, 200% 200%, 200% 200%, 100% 100%;
    background-attachment: fixed;
    animation: washDrift 36s ease-in-out infinite;
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
::selection {{ background: rgba(31,111,111,0.22); color: {TEXT_PRIMARY}; }}

/* ---------------------------------------------------------------
   HEADER — glass panel, embossed serif title, teal edge
--------------------------------------------------------------- */
.suite-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.3rem 1.8rem;
    background: {CARD_BG};
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW}, 0 0 22px rgba(31,111,111,0.08);
    border-radius: 12px;
    margin-bottom: 1.6rem;
}}
.suite-header h1 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.55rem; font-weight: 700;
    margin: 0; color: {TEAL_DARK};
    text-shadow: 0 1px 0 rgba(255,255,255,0.8), 0 2px 5px rgba(107,74,50,0.18);
}}
.suite-header p {{
    margin: 0.3rem 0 0 0;
    color: {TEXT_MUTED}; font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
}}
.suite-badge {{
    background: {BROWN_PALE}; color: {BROWN_DARK};
    border: 1px solid {BROWN_LIGHT};
    padding: 0.3rem 0.9rem; border-radius: 20px;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(107,74,50,0.2);
}}

/* ---------------------------------------------------------------
   KPI CARDS — glass + lift + warm glow on hover (the "3D" feel)
--------------------------------------------------------------- */
.kpi-card {{
    background: {CARD_BG};
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    border-radius: 12px;
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
}}
.kpi-value {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {BROWN_DARK};
    font-size: 1.9rem; font-weight: 700;
    line-height: 1.1; letter-spacing: -0.01em;
    text-shadow: 0 1px 0 rgba(255,255,255,0.7), 0 2px 4px rgba(107,74,50,0.14);
}}
.kpi-sub {{
    font-size: 0.76rem; margin-top: 0.4rem;
    color: {TEXT_MUTED};
}}

.section-title {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.1rem; font-weight: 700;
    color: {TEAL_DARK};
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(31,111,111,0.35);
}}
.section-toolbar {{
    display: flex; align-items: flex-end; justify-content: space-between;
    gap: 1rem;
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid rgba(31,111,111,0.35);
}}
.section-toolbar .section-title {{
    margin: 0; padding: 0; border: none;
}}

/* ---------------------------------------------------------------
   ELEVATED, INTERACTIVE CHART CARDS
   Warm layered shadow + faint teal glow ring so every chart reads
   as a floating white panel; a stronger hover state (lift + deeper
   glow + slight scale) makes hovering feel alive.
--------------------------------------------------------------- */
div[data-testid="stPlotlyChart"] {{
    background: {CARD_BG_SOLID};
    border: 1px solid {CARD_BORDER};
    border-radius: 14px;
    box-shadow: {CHART_SHADOW};
    padding: 0.9rem 1rem 0.3rem 1rem;
    transition: box-shadow 0.3s cubic-bezier(.22,1,.36,1),
                transform 0.3s cubic-bezier(.22,1,.36,1),
                border-color 0.3s ease;
}}
div[data-testid="stPlotlyChart"]:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    border-color: {CARD_BORDER_HI};
    transform: translateY(-6px) scale(1.005);
}}
div[data-testid="stPlotlyChart"] .plotly {{
    border-radius: 10px;
}}

.pill {{
    display: inline-block;
    padding: 0.18rem 0.65rem;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.04em; text-transform: uppercase;
    border-radius: 20px; border: 1px solid;
}}
.pill-critical {{ background: rgba(176,65,62,0.10);  color: {CRITICAL}; border-color: rgba(176,65,62,0.35); }}
.pill-high     {{ background: rgba(193,112,46,0.10); color: {HIGH};     border-color: rgba(193,112,46,0.35); }}
.pill-medium   {{ background: rgba(169,130,43,0.10); color: {MEDIUM};   border-color: rgba(169,130,43,0.35); }}
.pill-low      {{ background: rgba(63,125,92,0.10);  color: {LOW};      border-color: rgba(63,125,92,0.35); }}
.pill-info     {{ background: {TEAL_SOFT}; color: {TEAL_DARK}; border-color: {CARD_BORDER_HI}; }}

div[data-testid="stMetric"] {{
    background: {CARD_BG};
    backdrop-filter: blur(14px);
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 0.9rem 1.05rem; border-radius: 12px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}}
div[data-testid="stMetric"]:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    transform: translateY(-3px);
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {BROWN_DARK}; font-weight: 700;
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
    border-radius: 10px; overflow: hidden;
}}
table thead th {{
    background: linear-gradient(90deg, {TEAL_DARK} 0%, {TEAL_MID} 100%);
    color: #FBF6EC;
    text-align: left; padding: 0.6rem 0.75rem;
    font-weight: 600; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.05em;
}}
table tbody td {{
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid {CHART_GRID};
    color: {TEXT_PRIMARY};
}}
table tbody tr:nth-child(even) {{ background: rgba(107,74,50,0.03); }}
table tbody tr:hover {{ background: {TEAL_SOFT}; }}

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
    color: {TEAL_DARK}; background: {TEAL_SOFT};
}}
.stTabs [aria-selected="true"] {{
    color: {TEAL_DARK} !important;
    border-bottom: 3px solid {TEAL_DARK} !important;
    background: transparent !important;
    font-weight: 700;
}}

.stButton>button, .stDownloadButton>button {{
    border-radius: 8px;
    border: 1px solid {CARD_BORDER_HI};
    background: {CARD_BG_SOLID};
    color: {TEAL_DARK}; font-weight: 600;
    font-size: 0.86rem;
    transition: all 0.2s ease;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {TEAL_SOFT}; border-color: {TEAL_DARK};
    color: {TEAL_DARK};
    box-shadow: 0 4px 16px rgba(31,111,111,0.25);
    transform: translateY(-1px);
}}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] {{
    background: linear-gradient(135deg, {TEAL_DARK}, {TEAL_MID});
    border-color: {TEAL_DARK};
    color: #FBF6EC; font-weight: 700;
}}
.stButton>button[kind="primary"]:hover {{
    box-shadow: 0 6px 20px rgba(31,111,111,0.35);
    transform: translateY(-1px);
}}

/* ---------------------------------------------------------------
   SEGMENTED TOOLBAR CONTROLS (st.radio as pill toggles)
--------------------------------------------------------------- */
div[data-testid="stRadio"] > div {{
    gap: 0.3rem;
    background: {BROWN_SOFT};
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
    color: {BROWN_MID};
    transition: all 0.2s ease;
}}
div[data-testid="stRadio"] label:hover {{
    background: rgba(255,255,255,0.6);
}}
div[data-testid="stRadio"] label:has(input:checked) {{
    background: linear-gradient(135deg, {TEAL_DARK}, {TEAL_MID});
    box-shadow: 0 2px 12px rgba(31,111,111,0.35);
}}
div[data-testid="stRadio"] label:has(input:checked) p {{
    color: #FBF6EC !important; font-weight: 700;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #FFFFFF 0%, {BG_GRADIENT_2} 100%);
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
    background: #FFFFFF; color: {TEXT_PRIMARY};
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {TEAL_MID} !important;
    box-shadow: 0 0 0 2px rgba(46,139,139,0.25) !important;
}}

div[data-testid="stAlert"] {{
    border-radius: 10px; border-left: 4px solid {TEAL_DARK};
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
        BROWN_DARK=BROWN_DARK,
        BROWN_MID=BROWN_MID,
        BROWN_LIGHT=BROWN_LIGHT,
        BROWN_PALE=BROWN_PALE,
        BROWN_SOFT=BROWN_SOFT,
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
    Base layout for 2D charts on the warm light theme: fully transparent
    bg (so the white chart card shows through), warm brown-tinted
    gridlines, unified hover with spike lines for a genuinely
    interactive feel, and a smooth transition so re-sorted /
    re-windowed data animates in rather than snapping.
    """
    layout = dict(
        template="plotly_white",
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
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=CARD_BORDER,
            borderwidth=1,
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=TEAL_MID,
            font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        ),
    )
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(family="Source Serif 4, Georgia, serif",
                      size=15, color=TEAL_DARK),
            x=0.01, xanchor="left", y=0.97,
        )
    return layout


def chart_layout_3d(height: int = 500, title: str = "") -> dict:
    """Base layout for 3D charts: transparent bg, warm-lit scene."""
    layout = dict(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=11),
        margin=dict(t=40 if title else 10, b=10, l=10, r=10),
        height=height,
        transition=dict(duration=450, easing="cubic-in-out"),
        scene=dict(
            xaxis=dict(
                backgroundcolor="rgba(31,111,111,0.04)",
                gridcolor=CHART_GRID,
                zerolinecolor=CHART_GRID,
                showbackground=True,
                tickfont=dict(color=TEXT_MUTED, size=10),
                title_font=dict(color=TEXT_MUTED, size=11),
            ),
            yaxis=dict(
                backgroundcolor="rgba(107,74,50,0.04)",
                gridcolor=CHART_GRID,
                zerolinecolor=CHART_GRID,
                showbackground=True,
                tickfont=dict(color=TEXT_MUTED, size=10),
                title_font=dict(color=TEXT_MUTED, size=11),
            ),
            zaxis=dict(
                backgroundcolor="rgba(212,177,109,0.06)",
                gridcolor=CHART_GRID,
                zerolinecolor=CHART_GRID,
                showbackground=True,
                tickfont=dict(color=TEXT_MUTED, size=10),
                title_font=dict(color=TEXT_MUTED, size=11),
            ),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=TEAL_MID,
            font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        ),
    )
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(family="Source Serif 4, Georgia, serif",
                      size=15, color=TEAL_DARK),
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
    """Add subtle borders to bars/scatter markers for a slight depth effect."""
    if bar:
        fig.update_traces(
            marker=dict(line=dict(width=0.6, color="rgba(255,255,255,0.55)")),
            selector=dict(type="bar"),
        )
    if marker:
        fig.update_traces(
            marker=dict(line=dict(width=0.6, color="#FFFFFF")),
            selector=dict(type="scatter"),
        )
    return fig


def enable_rich_interaction(fig, hover_glow: bool = True):
    """
    Apply a shared set of "make it feel alive" interaction settings to any
    figure: unified hover with spikes already come from chart_layout_2d,
    this layers on click-to-toggle legends and marker opacity tuning.
    """
    fig.update_layout(
        hoverlabel_align="left",
        legend=dict(itemclick="toggleothers", itemdoubleclick="toggle"),
    )
    if hover_glow:
        fig.update_traces(marker=dict(opacity=0.94), selector=dict(type="bar"))
    return fig


PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "scrollZoom": True,
}


# --------------------------------------------------------------------------
# GENUINE 3D-LOOK BAR / AREA HELPERS
# --------------------------------------------------------------------------
def apply_3d_bar_caps(fig, x_values, y_values, orientation: str = "v",
                       cap_color: str = "rgba(255,255,255,0.55)",
                       cap_frac: float = 0.05, name: str = "cap"):
    """
    Add a thin, lighter "lid" strip flush with the top (or far edge, for
    horizontal bars) of every bar, mimicking a top-down light source
    hitting a beveled/extruded box. This is what actually reads as
    "3D" rather than a flat single-color rectangle — plain marker
    colors alone don't create that illusion.

    x_values / y_values are the ORIGINAL bar values (same arrays used
    to build the base go.Bar/px.bar trace). orientation "v" = vertical
    bars (cap sits on top); "h" = horizontal bars (cap sits at the tip).
    """
    import plotly.graph_objects as go

    vals = list(y_values) if orientation == "v" else list(x_values)
    if not vals:
        return fig
    peak = max(abs(v) for v in vals) or 1
    cap_size = peak * cap_frac

    if orientation == "v":
        cap_base = [v - cap_size if v >= 0 else v for v in vals]
        fig.add_trace(go.Bar(
            x=list(x_values),
            y=[cap_size] * len(vals),
            base=cap_base,
            marker=dict(color=cap_color, line=dict(width=0)),
            hoverinfo="skip",
            showlegend=False,
            name=name,
        ))
    else:
        cap_base = [v - cap_size if v >= 0 else v for v in vals]
        fig.add_trace(go.Bar(
            y=list(y_values),
            x=[cap_size] * len(vals),
            base=cap_base,
            orientation="h",
            marker=dict(color=cap_color, line=dict(width=0)),
            hoverinfo="skip",
            showlegend=False,
            name=name,
        ))
    fig.update_layout(barmode="overlay")
    return fig


def apply_gradient_fill(fig, top_color: str, bottom_color: str, trace_name: str = None):
    """
    Give an area/scatter trace a genuine vertical gradient fill (dark/
    saturated at the top, fading to pale near the baseline) using
    Plotly's native fillgradient — a real dimensional wash rather than
    one flat translucent color.
    """
    selector = dict(name=trace_name) if trace_name else dict(type="scatter")
    fig.update_traces(
        selector=selector,
        fillgradient=dict(
            type="vertical",
            colorscale=[[0, top_color], [1, bottom_color]],
        ),
    )
    return fig


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
    Map a numeric sequence onto a single-hue teal ramp (pale -> deep
    accent as the value rises), so non-semantic bar/line charts still
    read as part of the same color family as the rest of the dashboard,
    while the shading itself reinforces value magnitude.
    """
    values = list(values)
    if not values:
        return []
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1
    return [interpolate_color(light, dark, (v - vmin) / span) for v in values]


def teal_gradient_reversed(values, dark: str = TEAL_DARK, light: str = TEAL_PALE):
    """Same as teal_gradient but darkest at the low end (for "smaller is
    better" metrics where you still want visual weight on the largest bar)."""
    return list(reversed(teal_gradient(list(reversed(list(values))), dark, light)))


def brown_gradient(values, dark: str = BROWN_DARK, light: str = BROWN_PALE):
    """Same idea as teal_gradient but in the warm brown family, for
    charts that sit alongside a teal chart and need visual separation."""
    values = list(values)
    if not values:
        return []
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1
    return [interpolate_color(light, dark, (v - vmin) / span) for v in values]                                      
