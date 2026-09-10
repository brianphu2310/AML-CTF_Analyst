"""
theme.py
Shared visual theme helpers for the AML Compliance Suite.

Design direction: Power BI-style corporate banking dashboard.
Light neutral background with a subtle world-map watermark, white cards
with soft borders and shadows, muted teal accent palette, fully
transparent charts with pale gridlines. No decorative icons - all
typography and colour only.
"""

import textwrap
import streamlit as st

# ---------------------------------------------------------------- PALETTE
# Backgrounds
BG_GRADIENT_1 = "#EEF2F4"
BG_GRADIENT_2 = "#F6F8FA"
CARD_BG       = "#FFFFFF"
CARD_BORDER   = "#D6DDE3"
CARD_SHADOW   = "0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04)"

# Teal spectrum
TEAL_DARK     = "#3D5F6E"
TEAL_MID      = "#4A6E7E"
TEAL_LIGHT    = "#7BA8B8"
TEAL_PALE     = "#A8C4CE"
TEAL_SOFT     = "#DCE8EC"

# Text
TEXT_PRIMARY  = "#2C3E50"
TEXT_MUTED    = "#6B7A8A"
TEXT_ALERT    = "#A93226"
TEXT_LIGHT    = "#5A6B7A"

# Status colors
CRITICAL      = "#A93226"
HIGH          = "#C1622E"
MEDIUM        = "#8A6D1D"
LOW           = "#2E7D5B"
INFO          = "#4A6E7E"

# Chart
CHART_GRID    = "#E5E9EC"
CHART_SEQ     = ["#3D5F6E", "#7BA8B8", "#A8C4CE", "#5B8A9C", "#8FA9B5", "#4A6E7E"]

# Map watermark
MAP_COLOR     = "#B8C6CE"
MAP_OPACITY   = "0.35"


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
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.95"/>
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

  <g fill="none" stroke="COLOR" stroke-width="1.1" opacity="0.5" stroke-dasharray="3 5">
    <path d="M320,320 Q600,120 960,260"/>
    <path d="M960,260 Q1300,180 1560,420"/>
    <path d="M960,260 Q900,520 950,600"/>
    <path d="M320,320 Q620,560 950,600"/>
    <path d="M1560,420 Q1650,600 1640,780"/>
    <path d="M950,600 Q1200,700 1640,780"/>
    <path d="M320,320 Q240,500 430,600"/>
  </g>

  <g fill="COLOR" opacity="0.85">
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
# CSS
# --------------------------------------------------------------------------
_CSS_TEMPLATE = """<style>
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: {TEXT_PRIMARY};
}}

.stApp {{
    background: linear-gradient(180deg, {BG_GRADIENT_1} 0%, {BG_GRADIENT_2} 100%);
    background-attachment: fixed;
}}

.ampl-map-bg {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    opacity: {MAP_OPACITY};
}}

section.main > div,
section.main .block-container,
section[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

.block-container {{
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}}

h1, h2, h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-weight: 600;
}}

/* Header banner */
.suite-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.3rem 1.8rem;
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    margin-bottom: 1.6rem;
}}
.suite-header h1 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    color: {TEAL_DARK};
    letter-spacing: 0.005em;
}}
.suite-header p {{
    margin: 0.3rem 0 0 0;
    color: {TEXT_MUTED};
    font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
}}
.suite-badge {{
    background: {TEAL_SOFT};
    color: {TEAL_DARK};
    border: 1px solid {TEAL_LIGHT};
    padding: 0.3rem 0.9rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    white-space: nowrap;
}}

/* KPI cards */
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 1rem 1.2rem;
    height: 100%;
}}
.kpi-label {{
    color: {TEXT_MUTED};
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 600;
    margin-bottom: 0.45rem;
}}
.kpi-value {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.01em;
}}
.kpi-sub {{
    font-size: 0.76rem;
    margin-top: 0.4rem;
    color: {TEXT_MUTED};
}}

/* Section headers */
.section-title {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.08rem;
    font-weight: 700;
    color: {TEAL_DARK};
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {TEAL_LIGHT};
}}

/* Status pills */
.pill {{
    display: inline-block;
    padding: 0.16rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-radius: 2px;
    border: 1px solid;
}}
.pill-critical {{ background: #FBEAEA; color: {CRITICAL}; border-color: #E3B8B8; }}
.pill-high     {{ background: #FCEEE3; color: {HIGH};     border-color: #E9C6A6; }}
.pill-medium   {{ background: #FBF3DD; color: {MEDIUM};   border-color: #E4D093; }}
.pill-low      {{ background: #E7F3EC; color: {LOW};      border-color: #B7D9C6; }}
.pill-info     {{ background: {TEAL_SOFT}; color: {INFO}; border-color: {TEAL_PALE}; }}

/* Native metric */
div[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 0.9rem 1.05rem;
    border-radius: 2px;
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-weight: 700;
}}
div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED};
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.07em;
    font-weight: 600;
}}

/* Tables */
table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 0.85rem;
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    box-shadow: {CARD_SHADOW};
}}
table thead th {{
    background: {TEAL_DARK};
    color: #F5F7F9;
    text-align: left;
    padding: 0.6rem 0.75rem;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid {TEAL_MID};
}}
table tbody td {{
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid {CHART_GRID};
    color: {TEXT_PRIMARY};
}}
table tbody tr:nth-child(even) {{ background: #FAFBFC; }}
table tbody tr:hover {{ background: {TEAL_SOFT}; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    border-bottom: 1px solid {CARD_BORDER};
    background: transparent;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent;
    border-radius: 0;
    padding: 0.65rem 1.15rem;
    font-weight: 600;
    color: {TEXT_MUTED};
    font-size: 0.88rem;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {TEAL_MID};
    background: {TEAL_SOFT};
}}
.stTabs [aria-selected="true"] {{
    color: {TEAL_DARK} !important;
    border-bottom: 3px solid {TEAL_DARK} !important;
    background: transparent !important;
}}

/* Buttons */
.stButton>button, .stDownloadButton>button {{
    border-radius: 2px;
    border: 1px solid {TEAL_LIGHT};
    background: {CARD_BG};
    color: {TEAL_DARK};
    font-weight: 600;
    font-size: 0.86rem;
    transition: all 0.15s ease;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {TEAL_SOFT};
    border-color: {TEAL_MID};
    color: {TEAL_DARK};
}}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] {{
    background: {TEAL_DARK};
    border-color: {TEAL_DARK};
    color: #F5F7F9;
}}
.stButton>button[kind="primary"]:hover {{
    background: {TEAL_MID};
    border-color: {TEAL_MID};
    color: #FFFFFF;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {CARD_BG};
    border-right: 1px solid {CARD_BORDER};
}}
section[data-testid="stSidebar"] h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1rem;
    color: {TEAL_DARK};
    font-weight: 700;
}}
section[data-testid="stSidebar"] label {{
    color: {TEXT_MUTED};
    font-size: 0.8rem;
    font-weight: 600;
}}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
    border-radius: 2px;
    border-color: {CARD_BORDER};
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {TEAL_MID} !important;
    box-shadow: 0 0 0 1px {TEAL_MID} !important;
}}

/* Alerts */
div[data-testid="stAlert"] {{
    border-radius: 2px;
    border-left: 4px solid {TEAL_DARK};
}}

hr {{
    border-color: {CARD_BORDER};
    margin: 1.5rem 0;
}}
</style>"""


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
        CARD_BG=CARD_BG,
        CARD_BORDER=CARD_BORDER,
        CARD_SHADOW=CARD_SHADOW,
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
<div>
<h1>{title}</h1>
<p>{subtitle}</p>
</div>
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


def plotly_layout_defaults() -> dict:
    """Common layout kwargs to keep every chart on-brand.

    Transparent background so the world-map watermark shows through, with
    pale grey gridlines and dark slate text to match the Power BI look.
    """
    return dict(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(
            gridcolor=CHART_GRID,
            zerolinecolor=CHART_GRID,
            linecolor=CARD_BORDER,
            tickfont=dict(color=TEXT_MUTED, size=11),
            title_font=dict(color=TEXT_MUTED, size=11),
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
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor=CARD_BORDER,
            borderwidth=1,
        ),
    )


def chart_color_sequence():
    """Muted teal-forward palette for multi-series charts."""
    return CHART_SEQ
# Status colors (muted, matching palette)
CRITICAL      = "#A93226"
HIGH          = "#C1622E"
MEDIUM        = "#8A6D1D"
LOW           = "#2E7D5B"
INFO          = "#4A6E7E"

# Chart
CHART_GRID    = "#E5E9EC"
CHART_SEQ     = ["#3D5F6E", "#7BA8B8", "#A8C4CE", "#5B8A9C", "#8FA9B5", "#4A6E7E"]

# Map watermark
MAP_COLOR     = "#B8C6CE"
MAP_OPACITY   = "0.35"


# --------------------------------------------------------------------------
# WORLD MAP SVG WATERMARK
# --------------------------------------------------------------------------
# Minimal stylised world map drawn as dots + connector lines. Rendered as a
# fixed background layer behind the app content (opacity ~0.35) to mimic the
# muted map watermark seen in corporate Power BI dashboards.
_WORLD_MAP_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1000"
     preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;">
  <defs>
    <pattern id="dots" x="0" y="0" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.1" fill="COLOR"/>
    </pattern>
    <radialGradient id="fade" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.95"/>
    </radialGradient>
  </defs>

  <!-- Continent silhouettes as dotted masses (simplified) -->
  <g opacity="0.55">
    <!-- North America -->
    <path d="M180,220 C260,180 380,170 470,200 C520,220 540,270 520,330
             C500,390 440,430 370,440 C300,450 220,420 190,360
             C160,300 150,250 180,220 Z" fill="url(#dots)"/>
    <!-- South America -->
    <path d="M420,520 C480,510 540,540 560,600 C580,670 560,760 520,830
             C490,890 440,910 410,870 C380,820 380,740 390,660
             C395,600 400,560 420,520 Z" fill="url(#dots)"/>
    <!-- Europe -->
    <path d="M900,180 C960,170 1030,180 1060,220 C1080,260 1060,310 1010,330
             C960,350 900,340 870,300 C850,260 860,200 900,180 Z" fill="url(#dots)"/>
    <!-- Africa -->
    <path d="M920,400 C990,390 1080,410 1110,480 C1140,560 1120,680 1060,760
             C1020,810 960,820 930,770 C900,710 890,620 890,540
             C890,470 900,420 920,400 Z" fill="url(#dots)"/>
    <!-- Asia -->
    <path d="M1120,200 C1250,180 1420,190 1520,240 C1620,300 1680,400 1650,480
             C1620,560 1540,600 1440,600 C1340,600 1240,560 1180,500
             C1120,440 1090,320 1120,200 Z" fill="url(#dots)"/>
    <!-- Australia -->
    <path d="M1520,700 C1590,690 1680,710 1710,760 C1740,810 1700,860 1630,870
             C1560,880 1480,850 1460,800 C1440,760 1470,710 1520,700 Z" fill="url(#dots)"/>
  </g>

  <!-- Flight/transaction arcs between financial hubs -->
  <g fill="none" stroke="COLOR" stroke-width="1.1" opacity="0.5" stroke-dasharray="3 5">
    <path d="M320,320 Q600,120 960,260"/>
    <path d="M960,260 Q1300,180 1560,420"/>
    <path d="M960,260 Q900,520 950,600"/>
    <path d="M320,320 Q620,560 950,600"/>
    <path d="M1560,420 Q1650,600 1640,780"/>
    <path d="M950,600 Q1200,700 1640,780"/>
    <path d="M320,320 Q240,500 430,600"/>
  </g>

  <!-- Hub markers -->
  <g fill="COLOR" opacity="0.85">
    <circle cx="320"  cy="320" r="4.5"/>
    <circle cx="960"  cy="260" r="5.5"/>
    <circle cx="1560" cy="420" r="4.5"/>
    <circle cx="950"  cy="600" r="4"/>
    <circle cx="430"  cy="600" r="3.5"/>
    <circle cx="1640" cy="780" r="4"/>
  </g>

  <!-- Vignette to fade map at edges -->
  <rect width="2000" height="1000" fill="url(#fade)"/>
</svg>
"""


# --------------------------------------------------------------------------
# CSS INJECTION
# --------------------------------------------------------------------------
# IMPORTANT: The CSS template below intentionally has NO leading indentation
# so Markdown does not mistake it for a code block (which would render the
# CSS as literal text instead of applying it). textwrap.dedent() is applied
# as a safety net in case future edits re-introduce indentation.
_CSS_TEMPLATE = """<style>
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: {TEXT_PRIMARY};
}}

/* App background with subtle gradient */
.stApp {{
    background: linear-gradient(180deg, {BG_GRADIENT_1} 0%, {BG_GRADIENT_2} 100%);
    background-attachment: fixed;
}}

/* Map watermark layer - fixed full-viewport, behind content */
.ampl-map-bg {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    opacity: {MAP_OPACITY};
}}

/* Ensure Streamlit content sits above the map */
section.main > div,
section.main .block-container,
section[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

.block-container {{
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}}

h1, h2, h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-weight: 600;
}}

/* ------------------ Header banner ------------------ */
.suite-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.3rem 1.8rem;
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    margin-bottom: 1.6rem;
}}
.suite-header h1 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    color: {TEAL_DARK};
    letter-spacing: 0.005em;
}}
.suite-header p {{
    margin: 0.3rem 0 0 0;
    color: {TEXT_MUTED};
    font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
}}
.suite-badge {{
    background: {TEAL_SOFT};
    color: {TEAL_DARK};
    border: 1px solid {TEAL_LIGHT};
    padding: 0.3rem 0.9rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    white-space: nowrap;
}}

/* ------------------ KPI cards ------------------ */
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 1rem 1.2rem;
    height: 100%;
}}
.kpi-label {{
    color: {TEXT_MUTED};
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 600;
    margin-bottom: 0.45rem;
}}
.kpi-value {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.01em;
}}
.kpi-sub {{
    font-size: 0.76rem;
    margin-top: 0.4rem;
    color: {TEXT_MUTED};
}}

/* ------------------ Section headers ------------------ */
.section-title {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.08rem;
    font-weight: 700;
    color: {TEAL_DARK};
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {TEAL_LIGHT};
}}

/* ------------------ Status / risk pills ------------------ */
.pill {{
    display: inline-block;
    padding: 0.16rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-radius: 2px;
    border: 1px solid;
}}
.pill-critical {{ background: #FBEAEA; color: {CRITICAL}; border-color: #E3B8B8; }}
.pill-high     {{ background: #FCEEE3; color: {HIGH};     border-color: #E9C6A6; }}
.pill-medium   {{ background: #FBF3DD; color: {MEDIUM};   border-color: #E4D093; }}
.pill-low      {{ background: #E7F3EC; color: {LOW};      border-color: #B7D9C6; }}
.pill-info     {{ background: {TEAL_SOFT}; color: {INFO}; border-color: {TEAL_PALE}; }}

/* ------------------ Native metric widget ------------------ */
div[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 0.9rem 1.05rem;
    border-radius: 2px;
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-weight: 700;
}}
div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED};
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.07em;
    font-weight: 600;
}}

/* ------------------ Tables (via to_html) ------------------ */
table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 0.85rem;
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    box-shadow: {CARD_SHADOW};
}}
table thead th {{
    background: {TEAL_DARK};
    color: #F5F7F9;
    text-align: left;
    padding: 0.6rem 0.75rem;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid {TEAL_MID};
}}
table tbody td {{
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid {CHART_GRID};
    color: {TEXT_PRIMARY};
}}
table tbody tr:nth-child(even) {{ background: #FAFBFC; }}
table tbody tr:hover {{ background: {TEAL_SOFT}; }}

/* ------------------ Tabs ------------------ */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    border-bottom: 1px solid {CARD_BORDER};
    background: transparent;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent;
    border-radius: 0;
    padding: 0.65rem 1.15rem;
    font-weight: 600;
    color: {TEXT_MUTED};
    font-size: 0.88rem;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {TEAL_MID};
    background: {TEAL_SOFT};
}}
.stTabs [aria-selected="true"] {{
    color: {TEAL_DARK} !important;
    border-bottom: 3px solid {TEAL_DARK} !important;
    background: transparent !important;
}}

/* ------------------ Buttons ------------------ */
.stButton>button, .stDownloadButton>button {{
    border-radius: 2px;
    border: 1px solid {TEAL_LIGHT};
    background: {CARD_BG};
    color: {TEAL_DARK};
    font-weight: 600;
    font-size: 0.86rem;
    transition: all 0.15s ease;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {TEAL_SOFT};
    border-color: {TEAL_MID};
    color: {TEAL_DARK};
}}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] {{
    background: {TEAL_DARK};
    border-color: {TEAL_DARK};
    color: #F5F7F9;
}}
.stButton>button[kind="primary"]:hover {{
    background: {TEAL_MID};
    border-color: {TEAL_MID};
    color: #FFFFFF;
}}

/* ------------------ Sidebar ------------------ */
section[data-testid="stSidebar"] {{
    background: {CARD_BG};
    border-right: 1px solid {CARD_BORDER};
}}
section[data-testid="stSidebar"] h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1rem;
    color: {TEAL_DARK};
    font-weight: 700;
}}
section[data-testid="stSidebar"] label {{
    color: {TEXT_MUTED};
    font-size: 0.8rem;
    font-weight: 600;
}}

/* ------------------ Inputs ------------------ */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
    border-radius: 2px;
    border-color: {CARD_BORDER};
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {TEAL_MID} !important;
    box-shadow: 0 0 0 1px {TEAL_MID} !important;
}}

/* ------------------ Alerts ------------------ */
div[data-testid="stAlert"] {{
    border-radius: 2px;
    border-left: 4px solid {TEAL_DARK};
}}

/* ------------------ Divider ------------------ */
hr {{
    border-color: {CARD_BORDER};
    margin: 1.5rem 0;
}}
</style>"""


def inject_css():
    """Inject the stylesheet AND the world-map watermark background."""
    # 1. Insert the map SVG as a fixed, full-viewport background layer.
    map_svg = _WORLD_MAP_SVG.replace("COLOR", MAP_COLOR)
    st.markdown(
        f'<div class="ampl-map-bg">{map_svg}</div>',
        unsafe_allow_html=True,
    )

    # 2. Inject the main stylesheet.
    css = _CSS_TEMPLATE.format(
        TEXT_PRIMARY=TEXT_PRIMARY,
        TEXT_MUTED=TEXT_MUTED,
        BG_GRADIENT_1=BG_GRADIENT_1,
        BG_GRADIENT_2=BG_GRADIENT_2,
        CARD_BG=CARD_BG,
        CARD_BORDER=CARD_BORDER,
        CARD_SHADOW=CARD_SHADOW,
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
<div>
<h1>{title}</h1>
<p>{subtitle}</p>
</div>
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


def plotly_layout_defaults() -> dict:
    """Common layout kwargs to keep every chart on-brand.

    Transparent background so the world-map watermark shows through, with
    pale grey gridlines and dark slate text to match the Power BI aesthetic.
    """
    return dict(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(
            gridcolor=CHART_GRID,
            zerolinecolor=CHART_GRID,
            linecolor=CARD_BORDER,
            tickfont=dict(color=TEXT_MUTED, size=11),
            title_font=dict(color=TEXT_MUTED, size=11),
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
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor=CARD_BORDER,
            borderwidth=1,
        ),
    )


def chart_color_sequence():
    """Muted teal-forward palette for multi-series charts."""
    return CHART_SEQ# CSS INJECTION
# --------------------------------------------------------------------------
# IMPORTANT: The CSS string must not be passed to st.markdown with leading
# whitespace on any line, because Markdown treats 4+ leading spaces as a
# code block and will render the CSS as literal text instead of applying it
# as a stylesheet (this ignores unsafe_allow_html). We avoid the problem two
# ways at once:
#   1. Build the CSS with NO indentation at all (see _CSS_TEMPLATE below).
#   2. Still run textwrap.dedent() as a safety net in case a future edit
#      re-introduces indentation.
_CSS_TEMPLATE = """<style>
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: {INK};
}}
.stApp {{
    background-color: {PAPER};
}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.block-container {{
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}}
h1, h2, h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {NAVY_DARK};
}}

/* Header banner */
.suite-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.3rem 1.8rem;
    background: {NAVY_DARK};
    border-left: 5px solid {BRASS};
    margin-bottom: 1.6rem;
}}
.suite-header h1 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.55rem;
    font-weight: 600;
    margin: 0;
    color: #F5F6F8;
    letter-spacing: 0.01em;
}}
.suite-header p {{
    margin: 0.25rem 0 0 0;
    color: #B7C0CC;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}}
.suite-badge {{
    background: transparent;
    color: {BRASS};
    border: 1px solid {BRASS};
    padding: 0.28rem 0.85rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}}

/* KPI cards */
.kpi-card {{
    background: {PAPER};
    border: 1px solid {BORDER};
    border-top: 3px solid {NAVY};
    padding: 1rem 1.2rem;
    height: 100%;
}}
.kpi-label {{
    color: {MUTED};
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 0.4rem;
}}
.kpi-value {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {NAVY_DARK};
    font-size: 1.7rem;
    font-weight: 600;
    line-height: 1.1;
}}
.kpi-sub {{
    font-size: 0.78rem;
    margin-top: 0.4rem;
    color: {MUTED};
}}

/* Section headers */
.section-title {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.08rem;
    font-weight: 600;
    color: {NAVY_DARK};
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {NAVY};
}}

/* Status / risk tags */
.pill {{
    display: inline-block;
    padding: 0.16rem 0.55rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    border-radius: 2px;
    border: 1px solid;
}}
.pill-critical {{ background: #FBEAEA; color: {CRITICAL}; border-color: #E3B8B8; }}
.pill-high     {{ background: #FCEEE3; color: {HIGH};     border-color: #E9C6A6; }}
.pill-medium   {{ background: #FBF3DD; color: {MEDIUM};   border-color: #E4D093; }}
.pill-low      {{ background: #E7F3EC; color: {LOW};      border-color: #B7D9C6; }}
.pill-info     {{ background: #EAF0F6; color: {INFO};     border-color: #C3D3E3; }}

/* Native metric widget */
div[data-testid="stMetric"] {{
    background: {PAPER};
    border: 1px solid {BORDER};
    border-top: 3px solid {NAVY};
    padding: 0.8rem 1rem;
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {NAVY_DARK};
}}
div[data-testid="stMetricLabel"] {{
    color: {MUTED};
    text-transform: uppercase;
    font-size: 0.74rem;
    letter-spacing: 0.06em;
}}

/* Tables rendered via to_html */
table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 0.86rem;
}}
table thead th {{
    background: {NAVY_DARK};
    color: #F5F6F8;
    text-align: left;
    padding: 0.55rem 0.7rem;
    font-weight: 600;
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}
table tbody td {{
    padding: 0.5rem 0.7rem;
    border-bottom: 1px solid {BORDER};
}}
table tbody tr:nth-child(even) {{ background: {PANEL}; }}
table tbody tr:hover {{ background: #EEF1F5; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    border-bottom: 2px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent;
    border-radius: 0;
    padding: 0.6rem 1.1rem;
    font-weight: 600;
    color: {MUTED};
}}
.stTabs [aria-selected="true"] {{
    color: {NAVY_DARK} !important;
    border-bottom: 3px solid {BRASS} !important;
}}

/* Buttons */
.stButton>button, .stDownloadButton>button {{
    border-radius: 2px;
    border: 1px solid {NAVY};
    font-weight: 600;
}}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] {{
    background: {NAVY};
    border-color: {NAVY};
}}
.stButton>button[kind="primary"]:hover {{
    background: {NAVY_DARK};
    border-color: {NAVY_DARK};
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {PANEL};
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] h3 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1rem;
    color: {NAVY_DARK};
}}
</style>"""


def inject_css():
    css = _CSS_TEMPLATE.format(
        INK=INK, PAPER=PAPER, NAVY=NAVY, NAVY_DARK=NAVY_DARK,
        BRASS=BRASS, BORDER=BORDER, MUTED=MUTED, PANEL=PANEL,
        CRITICAL=CRITICAL, HIGH=HIGH, MEDIUM=MEDIUM, LOW=LOW, INFO=INFO,
    )
    st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


# --------------------------------------------------------------------------
# UI HELPERS
# --------------------------------------------------------------------------
def page_header(title: str, subtitle: str = "", badge: str = ""):
    badge_html = f'<span class="suite-badge">{badge}</span>' if badge else ""
    html = f"""<div class="suite-header">
<div>
<h1>{title}</h1>
<p>{subtitle}</p>
</div>
{badge_html}
</div>"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", sub_color: str = MUTED):
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


def plotly_layout_defaults() -> dict:
    """Common layout kwargs to keep every chart on-brand."""
    return dict(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=INK),
        margin=dict(t=10, b=10, l=10, r=10),
    )
