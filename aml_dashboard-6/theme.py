"""
theme.py
Shared visual theme helpers for the AML Compliance Suite.

v4: PROFESSIONAL TEAL / CREAM / BROWN THEME.
A warm, paper-like cream background, deep teal as the primary brand
color, and a rich brown as the secondary accent - a confident,
document-led palette rather than a consumer "fintech" look.

Every chart in the suite is built from a single 3D chart engine at the
bottom of this file: genuine Plotly Mesh3d / Surface / Scatter3d scenes
(extruded bars, a ribbon surface, a connected waterfall, a 3D scatter,
and a 3D ownership network) rather than 2D charts. Because these are
real 3D traces, they are natively draggable-to-rotate, scroll-to-zoom,
and hoverable in the browser - no extra interaction code required on
the page that calls them.

No icons or emoji are used anywhere in this module, and none should be
introduced on any page that imports it - typography, color and
geometry carry the visual weight instead.

Backwards-compat aliases (NAVY, BRASS, INK, MUTED, PAPER, PANEL, BORDER)
are kept so older pages that reference the previous palette names keep
working without edits.
"""

import textwrap
import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------- PALETTE
# Warm cream background, white-paper cards, teal primary + brown accent.
BG_GRADIENT_1 = "#F3ECDD"
BG_GRADIENT_2 = "#F8F2E6"
CARD_BG       = "#FFFDF8"
CARD_BORDER   = "#E4D8BF"
CARD_SHADOW   = "0 1px 3px rgba(74,52,28,0.08), 0 1px 2px rgba(74,52,28,0.05)"

# Layered warm shadow + teal highlight ring for elevated chart cards -
# reads as a raised, "3D" card even before the chart geometry inside it.
CHART_SHADOW       = "0 14px 30px rgba(74,52,28,0.14), 0 4px 10px rgba(74,52,28,0.08)"
CHART_SHADOW_HOVER = "0 22px 44px rgba(74,52,28,0.20), 0 0 0 1px rgba(31,94,91,0.20), 0 6px 16px rgba(31,94,91,0.10)"

# Primary teal family.
TEAL_DARK     = "#1F5E5B"
TEAL_MID      = "#2E7A73"
TEAL_LIGHT    = "#6FA79C"
TEAL_PALE     = "#B9D6CC"
TEAL_SOFT     = "#E7F0EA"
TEAL_GLOW     = "#1F5E5B"    # kept as an alias so pages that adopted the
TEAL_NEON     = "#2E7A73"    # v3 accent names still resolve sensibly.

# Secondary brown family.
BROWN_DARK    = "#5A3A22"
BROWN_MID     = "#8A5A34"
BROWN_LIGHT   = "#C79A6B"
BROWN_SOFT    = "#F3E6D5"

TEXT_PRIMARY  = "#2E241A"
TEXT_MUTED    = "#7C6E5C"
TEXT_ALERT    = "#8B2E2E"

CRITICAL      = "#8B2E2E"
HIGH          = "#B5651D"
MEDIUM        = "#9C7A24"
LOW           = "#3F7A5D"
INFO          = "#2C6E68"

CHART_GRID    = "#E6DCC6"
CHART_SEQ     = ["#1F5E5B", "#8A5A34", "#6FA79C", "#B5651D", "#3F7A5D",
                 "#9C7A24", "#2E7A73", "#8B2E2E", "#C79A6B", "#5A3A22"]

CHART_SEQ_EXT = CHART_SEQ + ["#4C8C82", "#A9744F"]

RISK_COLOR_MAP = {
    "Low":      LOW,
    "Medium":   MEDIUM,
    "High":     HIGH,
    "Critical": CRITICAL,
}

MAP_COLOR     = "#C9B896"
MAP_OPACITY   = "0.28"


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
# WORLD MAP SVG WATERMARK (recolored - warm tan on cream)
# --------------------------------------------------------------------------
_WORLD_MAP_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1000"
     preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;">
  <defs>
    <pattern id="dots" x="0" y="0" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.1" fill="COLOR"/>
    </pattern>
    <radialGradient id="fade" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#F8F2E6" stop-opacity="0"/>
      <stop offset="70%" stop-color="#F8F2E6" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#F8F2E6" stop-opacity="0.95"/>
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
# CSS TEMPLATE
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
.suite-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.3rem 1.8rem;
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {BROWN_MID};
    box-shadow: {CARD_SHADOW};
    margin-bottom: 1.6rem;
}}
.suite-header h1 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.5rem; font-weight: 700;
    margin: 0; color: {TEAL_DARK};
}}
.suite-header p {{
    margin: 0.3rem 0 0 0;
    color: {TEXT_MUTED}; font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
}}
.suite-badge {{
    background: {BROWN_SOFT}; color: {BROWN_DARK};
    border: 1px solid {BROWN_LIGHT};
    padding: 0.3rem 0.9rem;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    white-space: nowrap;
}}
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 1rem 1.2rem; height: 100%;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}}
.kpi-card:hover {{
    box-shadow: {CHART_SHADOW};
    transform: translateY(-2px);
}}
.kpi-label {{
    color: {TEXT_MUTED};
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.09em; font-weight: 600;
    margin-bottom: 0.45rem;
}}
.kpi-value {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK};
    font-size: 1.85rem; font-weight: 700;
    line-height: 1.1; letter-spacing: -0.01em;
}}
.kpi-sub {{
    font-size: 0.76rem; margin-top: 0.4rem;
    color: {TEXT_MUTED};
}}
.section-title {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.08rem; font-weight: 700;
    color: {TEAL_DARK};
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {BROWN_LIGHT};
}}
.section-toolbar {{
    display: flex; align-items: flex-end; justify-content: space-between;
    gap: 1rem;
    margin: 1.8rem 0 0.7rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {BROWN_LIGHT};
}}
.section-toolbar .section-title {{
    margin: 0; padding: 0; border: none;
}}
/* -------------------------------------------------------------------
   ELEVATED 3D CHART CARDS
   Every Plotly chart is wrapped by Streamlit in a
   div[data-testid="stPlotlyChart"] - styling it directly gives every
   chart a consistent raised panel with a soft warm shadow and a teal
   glow ring on hover, no per-chart code changes required. The charts
   themselves are also genuine 3D scenes, so this shell frames real
   geometry rather than a flat image with a fake shadow.
------------------------------------------------------------------- */
div[data-testid="stPlotlyChart"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 10px;
    box-shadow: {CHART_SHADOW};
    padding: 0.75rem;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}}
div[data-testid="stPlotlyChart"]:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    transform: translateY(-4px);
}}
div[data-testid="stPlotlyChart"] .plotly {{
    border-radius: 8px;
}}
.pill {{
    display: inline-block;
    padding: 0.16rem 0.6rem;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.04em; text-transform: uppercase;
    border-radius: 3px; border: 1px solid;
}}
.pill-critical {{ background: #F7E7E5; color: {CRITICAL}; border-color: #DCB3AE; }}
.pill-high     {{ background: #FBEEDD; color: {HIGH};     border-color: #E7C295; }}
.pill-medium   {{ background: #FAF1D6; color: {MEDIUM};   border-color: #E0CE8E; }}
.pill-low      {{ background: #E4F0E9; color: {LOW};      border-color: #A9CDB9; }}
.pill-info     {{ background: {TEAL_SOFT}; color: {INFO}; border-color: {TEAL_PALE}; }}
div[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {TEAL_DARK};
    box-shadow: {CARD_SHADOW};
    padding: 0.9rem 1.05rem; border-radius: 6px;
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Source Serif 4', Georgia, serif;
    color: {TEAL_DARK}; font-weight: 700;
}}
div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED}; text-transform: uppercase;
    font-size: 0.72rem; letter-spacing: 0.07em; font-weight: 600;
}}
table {{
    border-collapse: collapse; width: 100%;
    font-size: 0.85rem; background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    box-shadow: {CARD_SHADOW};
}}
table thead th {{
    background: {TEAL_DARK}; color: {BG_GRADIENT_2};
    text-align: left; padding: 0.6rem 0.75rem;
    font-weight: 600; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.05em;
    border-bottom: 1px solid {TEAL_MID};
}}
table tbody td {{
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid {CHART_GRID};
    color: {TEXT_PRIMARY};
}}
table tbody tr:nth-child(even) {{ background: {BG_GRADIENT_2}; }}
table tbody tr:hover {{ background: {TEAL_SOFT}; }}
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px; border-bottom: 1px solid {CARD_BORDER};
    background: transparent;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent; border-radius: 0;
    padding: 0.65rem 1.15rem; font-weight: 600;
    color: {TEXT_MUTED}; font-size: 0.88rem;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {TEAL_DARK}; background: {TEAL_SOFT};
}}
.stTabs [aria-selected="true"] {{
    color: {TEAL_DARK} !important;
    border-bottom: 3px solid {BROWN_MID} !important;
    background: transparent !important;
}}
.stButton>button, .stDownloadButton>button {{
    border-radius: 4px;
    border: 1px solid {TEAL_DARK};
    background: {CARD_BG};
    color: {TEAL_DARK}; font-weight: 600;
    font-size: 0.86rem;
    transition: all 0.15s ease;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {TEAL_SOFT}; border-color: {TEAL_MID};
    color: {TEAL_DARK};
}}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] {{
    background: {TEAL_DARK}; border-color: {TEAL_DARK};
    color: {BG_GRADIENT_2};
}}
.stButton>button[kind="primary"]:hover {{
    background: {BROWN_MID}; border-color: {BROWN_MID};
    color: #FFFFFF;
}}
/* -------------------------------------------------------------------
   SEGMENTED TOOLBAR CONTROLS - pill toggle for interactive controls
   sitting at the top of each section.
------------------------------------------------------------------- */
div[data-testid="stRadio"] > div {{
    gap: 0.3rem;
    background: {TEAL_SOFT};
    border: 1px solid {TEAL_PALE};
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
    color: {TEAL_DARK};
    transition: all 0.15s ease;
}}
div[data-testid="stRadio"] label:hover {{
    background: rgba(255,255,255,0.6);
}}
div[data-testid="stRadio"] label:has(input:checked) {{
    background: {TEAL_DARK};
    box-shadow: 0 2px 8px rgba(31,94,91,0.35);
}}
div[data-testid="stRadio"] label:has(input:checked) p {{
    color: #FFFFFF !important; font-weight: 600;
}}
section[data-testid="stSidebar"] {{
    background: {CARD_BG};
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
    border-radius: 4px; border-color: {CARD_BORDER};
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {TEAL_MID} !important;
    box-shadow: 0 0 0 1px {TEAL_MID} !important;
}}
div[data-testid="stAlert"] {{
    border-radius: 4px; border-left: 4px solid {TEAL_DARK};
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
        CARD_BG=CARD_BG,
        CARD_BORDER=CARD_BORDER,
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


def kpi_card(label: str, value: str, sub: str = "", sub_color: str = None):
    sub_color = sub_color or TEXT_MUTED
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
    top of the section, above any chart beneath it. `control_fn` is a
    zero-arg callable that renders a Streamlit widget and returns its
    value (e.g. a lambda calling st.radio(...)).
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
# SHARED 2D CHART LAYOUT
# --------------------------------------------------------------------------
def chart_layout_2d(height: int = 340, title: str = "") -> dict:
    """
    Base layout for every 2D chart in the suite: transparent background
    (so the white chart card shows through), warm brown-tinted gridlines,
    unified hover with dotted spike lines for a genuinely interactive
    feel, and a smooth transition so re-sorted / re-filtered data
    animates in rather than snapping.
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
        transition=dict(duration=400, easing="cubic-in-out"),
        uniformtext=dict(minsize=9, mode="hide"),
        xaxis=dict(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID, linecolor=CARD_BORDER,
                   tickfont=dict(color=TEXT_MUTED, size=11), title_font=dict(color=TEXT_MUTED, size=11),
                   showspikes=True, spikecolor=TEAL_MID, spikethickness=1, spikedash="dot", spikemode="across"),
        yaxis=dict(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID, linecolor=CARD_BORDER,
                   tickfont=dict(color=TEXT_MUTED, size=11), title_font=dict(color=TEXT_MUTED, size=11)),
        legend=dict(font=dict(color=TEXT_PRIMARY, size=11), bgcolor="rgba(255,255,255,0.85)",
                    bordercolor=CARD_BORDER, borderwidth=1),
        hoverlabel=dict(bgcolor=CARD_BG, bordercolor=TEAL_MID,
                        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12)),
    )
    if title:
        layout["title"] = dict(text=title, font=dict(family="Source Serif 4, Georgia, serif", size=15, color=TEAL_DARK),
                                x=0.01, xanchor="left", y=0.97)
    return layout


def plotly_layout_defaults() -> dict:
    return chart_layout_2d()


def chart_color_sequence():
    return CHART_SEQ


def chart_color_sequence_ext():
    return CHART_SEQ_EXT


def apply_shadow(fig, marker=True, bar=True):
    if bar:
        fig.update_traces(marker=dict(line=dict(width=0.5, color=CARD_BORDER)), selector=dict(type="bar"))
    if marker:
        fig.update_traces(marker=dict(line=dict(width=0.5, color="white")), selector=dict(type="scatter"))
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
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    return _rgb_to_hex((r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t))


def teal_gradient(values, dark: str = TEAL_DARK, light: str = TEAL_PALE):
    """Map a numeric sequence onto a single-hue teal ramp (pale -> deep as
    the value rises) so every non-semantic bar chart shares one family."""
    values = list(values)
    if not values:
        return []
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1
    return [interpolate_color(light, dark, (v - vmin) / span) for v in values]


def brown_gradient(values, dark: str = BROWN_DARK, light: str = BROWN_LIGHT):
    """Same idea as teal_gradient but in the brown accent family - useful
    for a second series sitting alongside a teal one in a grouped chart."""
    values = list(values)
    if not values:
        return []
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1
    return [interpolate_color(light, dark, (v - vmin) / span) for v in values]


# --------------------------------------------------------------------------
# INTERACTION HELPERS (shared "make it feel alive" settings)
# --------------------------------------------------------------------------
PLOTLY_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "scrollZoom": True,
}


def enable_rich_interaction(fig, hover_glow: bool = True):
    """Legend click-to-isolate + slightly tuned marker opacity, layered on
    top of the unified hover / spike lines already set by chart_layout_2d."""
    fig.update_layout(
        hoverlabel_align="left",
        legend=dict(itemclick="toggleothers", itemdoubleclick="toggle"),
    )
    if hover_glow:
        fig.update_traces(marker=dict(opacity=0.94), selector=dict(type="bar"))
    return fig


# ==========================================================================
# 2D CHART ENGINE
# Every chart in the suite is built from these primitives. They keep the
# same function names and call signatures as the previous 3D (Mesh3d /
# Surface) engine, so no page needs to change - only the rendering
# underneath switched from extruded 3D geometry to clean, flat 2D traces.
# Every chart still draws from the same harmonized teal / brown palette
# (via teal_gradient / brown_gradient / RISK_COLOR_MAP / CHART_SEQ) so the
# whole suite reads as one consistent, color-coordinated system, and every
# chart keeps unified hover, spike lines, a smooth transition on
# re-render, and legend click-to-isolate.
# ==========================================================================
def chart_layout_3d(height: int = 500, title: str = "") -> dict:
    """Compatibility alias - now just the shared 2D layout."""
    return chart_layout_2d(height=height, title=title)


def bar3d_chart(categories, values, colors=None, height=420, value_fmt=None,
                 bar_ratio=0.62, depth_ratio=0.5, camera=None, shadow=True, z_title=""):
    """
    A single-series 2D bar chart. `bar_ratio`, `depth_ratio`, `camera` and
    `shadow` are accepted for backwards compatibility with callers written
    for the old 3D engine but no longer change the rendering; `bar_ratio`
    still maps to Plotly's bargap so bar width stays adjustable.
    """
    categories = list(categories)
    values = [float(v) for v in values]
    if colors is None:
        colors = teal_gradient(values)
    if isinstance(colors, str):
        colors = [colors] * len(values)

    fmt = value_fmt or (lambda v: f"{v:,.0f}")
    fig = go.Figure(go.Bar(
        x=categories, y=values,
        marker=dict(color=colors, line=dict(width=0.8, color="rgba(46,36,26,0.35)")),
        text=[fmt(v) for v in values],
        textposition="outside",
        textfont=dict(color=TEXT_MUTED, size=11),
        hovertemplate="<b>%{x}</b><br>" + (z_title or "Value") + ": %{y:,.2f}<extra></extra>",
    ))
    fig.update_layout(**chart_layout_2d(height=height))
    fig.update_layout(showlegend=False, hovermode="x", bargap=max(0.05, 1 - bar_ratio),
                       yaxis=dict(title=dict(text=z_title)))
    return enable_rich_interaction(fig)


def grouped_bar3d_chart(categories, series: dict, colors: dict = None, height=420,
                         value_fmt=None, bar_ratio=0.34, gap=0.05, z_title=""):
    """
    A clustered 2D bar chart: each category on the x-axis holds one bar
    per series, grouped side by side and colored from the shared
    harmonized palette (falling back to CHART_SEQ for any series without
    an explicit color).
    """
    categories = list(categories)
    names = list(series.keys())
    colors = colors or {}
    fmt = value_fmt or (lambda v: f"{v:,.0f}")

    fig = go.Figure()
    for s_idx, name in enumerate(names):
        vals = [float(v) for v in series[name]]
        col = colors.get(name, CHART_SEQ[s_idx % len(CHART_SEQ)])
        fig.add_trace(go.Bar(
            x=categories, y=vals, name=str(name),
            marker=dict(color=col, line=dict(width=0.8, color="rgba(46,36,26,0.35)")),
            hovertemplate="<b>%{x}</b><br>" + str(name) + ": %{y:,.2f}<extra></extra>",
        ))

    fig.update_layout(**chart_layout_2d(height=height))
    fig.update_layout(barmode="group", bargap=0.2, bargroupgap=gap, hovermode="x unified",
                       yaxis=dict(title=dict(text=z_title)))
    return enable_rich_interaction(fig)


def target_bar3d(value, target, label, color, max_value=100, height=280, suffix="%"):
    """A radial gauge with a target threshold line - the 2D replacement
    for the old 3D 'thermometer' bar, in the same harmonized colors."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix=suffix, font=dict(color=BROWN_DARK, size=28,
                                              family="Source Serif 4, Georgia, serif")),
        title=dict(text=label, font=dict(color=TEXT_MUTED, size=12)),
        gauge=dict(
            axis=dict(range=[0, max_value], tickcolor=TEXT_MUTED, tickfont=dict(color=TEXT_MUTED, size=10)),
            bar=dict(color=color, thickness=0.28),
            bgcolor="rgba(255,255,255,0.6)",
            borderwidth=1, bordercolor=CARD_BORDER,
            steps=[
                dict(range=[0, max_value * 0.4], color="rgba(90,58,34,0.08)"),
                dict(range=[max_value * 0.4, max_value * 0.7], color="rgba(90,58,34,0.14)"),
                dict(range=[max_value * 0.7, max_value], color="rgba(90,58,34,0.20)"),
            ],
            threshold=dict(line=dict(color=CRITICAL, width=3), thickness=0.75, value=target),
        ),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY),
        margin=dict(t=40, b=10, l=20, r=20),
        height=height,
        transition=dict(duration=450, easing="cubic-in-out"),
    )
    return fig


def ribbon3d_chart(x_labels, series: dict, height=380, z_title="Amount"):
    """
    A 2D stacked-area trend chart for two or more series - the flat
    replacement for the old Surface 'ribbon'. Each series gets a genuine
    vertical gradient fill (Plotly's native fillgradient) in the
    harmonized teal / brown family so the trend still reads with real
    dimensionality, without the exaggerated 3D surface.
    """
    names = list(series.keys())
    palette = [TEAL_DARK, BROWN_MID, TEAL_LIGHT, BROWN_LIGHT] + CHART_SEQ
    fig = go.Figure()
    for idx, name in enumerate(names):
        vals = list(series[name])
        line_color = palette[idx % len(palette)]
        r, g, b = _hex_to_rgb(line_color)
        fig.add_trace(go.Scatter(
            x=list(x_labels), y=vals, name=str(name), mode="lines",
            line=dict(width=2.2, color=line_color),
            fill="tozeroy",
            fillgradient=dict(type="vertical", colorscale=[
                [0, f"rgba({r},{g},{b},0.45)"], [1, f"rgba({r},{g},{b},0.03)"],
            ]),
            hovertemplate="%{x}<br>" + str(name) + ": %{y:,.0f}<extra></extra>",
        ))
    fig.update_layout(**chart_layout_2d(height=height))
    fig.update_layout(hovermode="x unified", yaxis=dict(title=dict(text=z_title)))
    return enable_rich_interaction(fig)


def waterfall3d_chart(labels, values, height=420, colors=None):
    """
    A 2D waterfall using Plotly's native Waterfall trace - `values[0]` is
    an absolute starting total, each subsequent value a relative delta
    on the running total, in the harmonized teal / brown / critical-red
    palette.
    """
    colors = colors or {}
    inc_color = colors.get("increasing", TEAL_DARK)
    dec_color = colors.get("decreasing", HIGH)
    tot_color = colors.get("total", BROWN_MID)

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute"] + ["relative"] * (len(values) - 1),
        x=list(labels),
        y=list(values),
        text=[f"{v:+,}" if i > 0 else f"{v:,}" for i, v in enumerate(values)],
        textposition="outside",
        textfont=dict(color=TEXT_PRIMARY, size=11),
        connector=dict(line=dict(color=CARD_BORDER, width=1)),
        increasing=dict(marker=dict(color=inc_color, line=dict(width=0.6, color="rgba(255,255,255,0.6)"))),
        decreasing=dict(marker=dict(color=dec_color, line=dict(width=0.6, color="rgba(255,255,255,0.6)"))),
        totals=dict(marker=dict(color=tot_color, line=dict(width=0.6, color="rgba(255,255,255,0.6)"))),
        hovertemplate="<b>%{x}</b><br>%{y:+,}<extra></extra>",
    ))
    fig.update_layout(**chart_layout_2d(height=height))
    fig.update_layout(hovermode="x", showlegend=False)
    return enable_rich_interaction(fig, hover_glow=False)


def scatter3d_chart(x, y, z, color_labels=None, color_map=None, size=None,
                     hover_text=None, x_title="", y_title="", z_title="", height=420):
    """
    A 2D scatter (x vs y), colored by group exactly as before. The third
    dimension `z` (e.g. channel) - no longer a spatial axis - is instead
    encoded as marker symbol, so it stays visible at a glance and is
    still spelled out in the hover text. Accepts (and ignores) a later
    `fig.update_layout(scene=...)` call some pages still make, since an
    unused `scene` key on a 2D figure is harmless.
    """
    n = len(x)
    color_labels = list(color_labels) if color_labels is not None else ["All"] * n
    color_map = color_map or {}
    groups = list(dict.fromkeys(color_labels))
    default_colors = teal_gradient(list(range(len(groups))) or [0])

    symbols = ["circle", "square", "diamond", "triangle-up", "cross", "star",
               "hexagon", "triangle-down", "pentagon"]
    z_list = list(z)
    z_groups = list(dict.fromkeys(z_list))
    symbol_map = {zg: symbols[i % len(symbols)] for i, zg in enumerate(z_groups)}

    fig = go.Figure()
    for g_idx, g in enumerate(groups):
        idxs = [i for i, lab in enumerate(color_labels) if lab == g]
        col = color_map.get(g, default_colors[g_idx % len(default_colors)])
        marker_size = [size[i] for i in idxs] if size is not None else 9
        fig.add_trace(go.Scatter(
            x=[x[i] for i in idxs], y=[y[i] for i in idxs], mode="markers", name=str(g),
            marker=dict(size=marker_size, color=col, opacity=0.85,
                        symbol=[symbol_map[z_list[i]] for i in idxs],
                        line=dict(width=0.8, color="rgba(46,36,26,0.35)")),
            text=[hover_text[i] for i in idxs] if hover_text is not None else None,
            hoverinfo="text" if hover_text is not None else "x+y",
        ))

    fig.update_layout(**chart_layout_2d(height=height))
    fig.update_layout(
        xaxis=dict(title=dict(text=x_title)),
        yaxis=dict(title=dict(text=y_title)),
        hovermode="closest",
    )
    return enable_rich_interaction(fig)


def network3d_chart(center_label, center_kind, nodes, color_map, height=460):
    """
    A 2D ownership / relationship network: the reporting entity sits at
    the origin, each related node is placed around it in a circle (angle
    only - weight, e.g. ownership %, now drives marker size instead of
    elevation), with edges drawn as straight 2D lines.

    `nodes` is a list of dicts: {"label": str, "kind": str, "weight": float}.
    `color_map` maps kind -> color and must include `center_kind`.
    """
    import math

    n = max(len(nodes), 1)
    radius = 1.0
    edge_traces = []
    node_x, node_y = [0.0], [0.0]
    node_text, node_color, node_size = [center_label], [color_map.get(center_kind, TEAL_DARK)], [34]

    for idx, node in enumerate(nodes):
        angle = 2 * math.pi * idx / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        weight = float(node.get("weight", 0) or 0)
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node['label']} ({weight:.0f}%)" if weight else node["label"])
        node_color.append(color_map.get(node.get("kind"), TEXT_MUTED))
        node_size.append(16 + weight * 0.22)
        edge_traces.append(go.Scatter(
            x=[0, x], y=[0, y], mode="lines",
            line=dict(color=CARD_BORDER, width=2),
            hoverinfo="skip", showlegend=False,
        ))

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_text, textposition="top center",
        textfont=dict(color=TEXT_PRIMARY, size=11, family="Inter, sans-serif"),
        marker=dict(size=node_size, color=node_color, opacity=0.95,
                    line=dict(width=1.5, color=CARD_BG)),
        hoverinfo="text", showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(**chart_layout_2d(height=height))
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(visible=False, showgrid=False, zeroline=False, scaleanchor="x", scaleratio=1),
        hovermode="closest",
    )
    return fig
