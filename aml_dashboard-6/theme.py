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
    border-radius: 6px;
    box-shadow: {CARD_SHADOW};
    margin-bottom: 1.6rem;
    gap: 1rem; flex-wrap: wrap;
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
    border-radius: 6px;
    box-shadow: {CARD_SHADOW};
    padding: 1rem 1.2rem; height: 100%;
    transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}}
.kpi-card:hover {{
    box-shadow: {CHART_SHADOW};
    transform: translateY(-2px);
    border-color: {TEAL_PALE};
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
    padding: 0.4rem 0.45rem 0.15rem 0.45rem;
    transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
    overflow: hidden;
}}
div[data-testid="stPlotlyChart"]:hover {{
    box-shadow: {CHART_SHADOW_HOVER};
    transform: translateY(-3px);
    border-color: {TEAL_PALE};
}}
div[data-testid="stPlotlyChart"] .plotly,
div[data-testid="stPlotlyChart"] .js-plotly-plot,
div[data-testid="stPlotlyChart"] .plot-container {{
    border-radius: 7px;
    width: 100% !important;
}}
/* Charts should read as content that fills its card, not a small
   graphic floating inside a lot of empty frame - the figure's own
   margins are trimmed to match (see _base_scene_layout / chart_layout_2d),
   this just removes the outer whitespace duplication. */
div[data-testid="stPlotlyChart"] > div {{
    width: 100% !important;
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
    border-collapse: separate; border-spacing: 0; width: 100%;
    font-size: 0.85rem; background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 6px; overflow: hidden;
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
    transition: background 0.12s ease;
}}
table tbody tr:last-child td {{ border-bottom: none; }}
table tbody tr:nth-child(even) {{ background: {BG_GRADIENT_2}; }}
table tbody tr:hover td {{ background: {TEAL_SOFT}; }}
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
# LEGACY 2D LAYOUT HELPER (kept only for plotly_layout_defaults callers)
# --------------------------------------------------------------------------
def chart_layout_2d(height: int = 340, title: str = "") -> dict:
    layout = dict(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        margin=dict(t=40 if title else 10, b=10, l=10, r=10),
        height=height,
        xaxis=dict(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID, linecolor=CARD_BORDER,
                   tickfont=dict(color=TEXT_MUTED, size=11), title_font=dict(color=TEXT_MUTED, size=11)),
        yaxis=dict(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID, linecolor=CARD_BORDER,
                   tickfont=dict(color=TEXT_MUTED, size=11), title_font=dict(color=TEXT_MUTED, size=11)),
        legend=dict(font=dict(color=TEXT_PRIMARY, size=11), bgcolor="rgba(255,255,255,0.8)",
                    bordercolor=CARD_BORDER, borderwidth=1),
        hoverlabel=dict(bgcolor=CARD_BG, bordercolor=CARD_BORDER,
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


def _rank_positions(values):
    """Map each value to its percentile rank (0..1) rather than its raw
    magnitude. A handful of bars that are numerically close (e.g. 41,
    43, 44) still spread across the FULL colour range instead of
    bunching into three near-identical shades - this is what keeps
    adjacent bars visually distinct instead of collapsing together."""
    values = list(values)
    n = len(values)
    if n == 0:
        return []
    if n == 1:
        return [1.0]
    order = sorted(range(n), key=lambda i: values[i])
    positions = [0.0] * n
    for rank, idx in enumerate(order):
        positions[idx] = rank / (n - 1)
    return positions


def teal_gradient(values, dark: str = TEAL_DARK, light: str = TEAL_PALE):
    """Map a numeric sequence onto a single-hue teal ramp (pale -> deep
    for the lowest -> highest value) so every non-semantic bar chart
    shares one family, with every bar kept clearly distinguishable
    from its neighbours regardless of how close the underlying values
    are (see `_rank_positions`)."""
    positions = _rank_positions(values)
    return [interpolate_color(light, dark, p) for p in positions]


def brown_gradient(values, dark: str = BROWN_DARK, light: str = BROWN_LIGHT):
    """Same idea as teal_gradient but in the brown accent family - useful
    for a second series sitting alongside a teal one in a grouped chart."""
    positions = _rank_positions(values)
    return [interpolate_color(light, dark, p) for p in positions]


# ==========================================================================
# 3D CHART ENGINE
# Every chart in the suite is built from these primitives: extruded
# Mesh3d "cuboid" bars with a soft contact shadow, a Surface ribbon for
# trends, a connected 3D waterfall, a 3D scatter, and a 3D ownership
# network. Every figure returned here is a real 3D scene - drag to
# rotate, scroll to zoom, hover for values - with no additional
# interaction code needed on the calling page.
# ==========================================================================
def _cuboid_trace(x0, x1, y0, y1, z0, z1, color, opacity=1.0, hover=None):
    """A single extruded rectangular box, lit for a glossy 3D look."""
    xs = [x0, x0, x1, x1, x0, x0, x1, x1]
    ys = [y0, y1, y1, y0, y0, y1, y1, y0]
    zs = [z0, z0, z0, z0, z1, z1, z1, z1]
    i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
    return go.Mesh3d(
        x=xs, y=ys, z=zs, i=i, j=j, k=k,
        color=color, opacity=opacity, flatshading=True,
        lighting=dict(ambient=0.55, diffuse=0.85, specular=0.5, roughness=0.4, fresnel=0.15),
        lightposition=dict(x=150, y=250, z=350),
        hoverinfo="text" if hover else "skip",
        hovertext=hover,
        showlegend=False,
    )


def _base_scene_layout(height, title="", orthographic=True):
    """Shared 3D scene shell. `orthographic` removes perspective
    convergence (parallel edges stay parallel) so extruded bars and
    surfaces read as a clean, gently-tilted isometric diagram rather
    than a dramatic vanishing-point 3D render - the shapes stay
    legible and comparable at a glance while keeping real depth,
    rotate and zoom. The scene's own domain is stretched to the
    figure edges so the chart fills its card instead of floating in
    a wide inner margin."""
    layout = dict(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=11),
        margin=dict(t=34 if title else 4, b=4, l=4, r=4),
        height=height,
        scene=dict(
            domain=dict(x=[0, 1], y=[0, 1]),
            xaxis=dict(backgroundcolor="rgba(31,94,91,0.03)", gridcolor=CHART_GRID, zerolinecolor=CHART_GRID,
                       showbackground=True, tickfont=dict(color=TEXT_MUTED, size=10), title_font=dict(color=TEXT_MUTED, size=11)),
            yaxis=dict(backgroundcolor="rgba(31,94,91,0.03)", gridcolor=CHART_GRID, zerolinecolor=CHART_GRID,
                       showbackground=True, tickfont=dict(color=TEXT_MUTED, size=10), title_font=dict(color=TEXT_MUTED, size=11)),
            zaxis=dict(backgroundcolor="rgba(31,94,91,0.03)", gridcolor=CHART_GRID, zerolinecolor=CHART_GRID,
                       showbackground=True, tickfont=dict(color=TEXT_MUTED, size=10), title_font=dict(color=TEXT_MUTED, size=11)),
            camera=dict(
                eye=dict(x=1.3, y=-1.55, z=0.85),
                projection=dict(type="orthographic" if orthographic else "perspective"),
            ),
        ),
    )
    if title:
        layout["title"] = dict(text=title, font=dict(family="Source Serif 4, Georgia, serif", size=15, color=TEAL_DARK),
                                x=0.01, xanchor="left", y=0.97)
    return layout


def chart_layout_3d(height: int = 500, title: str = "") -> dict:
    """Public alias kept for any page building a custom 3D figure."""
    return _base_scene_layout(height, title)


def bar3d_chart(categories, values, colors=None, height=420, value_fmt=None,
                 bar_ratio=0.6, depth_ratio=0.5, camera=None, shadow=True, z_title=""):
    """A softly-extruded bar chart (Mesh3d). Depth is kept shallow and the
    camera near-orthographic and front-on, so it reads at a glance like a
    normal bar chart with a light 3D bevel, rather than a rotated diorama -
    while still being genuinely 3D (drag to rotate, scroll to zoom)."""
    categories = list(categories)
    values = [float(v) for v in values]
    n = max(len(categories), 1)
    if colors is None:
        colors = teal_gradient(values)
    if isinstance(colors, str):
        colors = [colors] * len(values)

    half_w, half_d = bar_ratio / 2, depth_ratio / 2
    top_val = max(values) if values else 1.0
    traces = []

    for idx, (cat, val, col) in enumerate(zip(categories, values, colors)):
        z1 = max(val, top_val * 0.006)
        fmt_val = value_fmt(val) if value_fmt else f"{val:,.0f}"
        if shadow:
            traces.append(_cuboid_trace(
                idx - half_w - 0.05, idx + half_w + 0.05,
                -half_d - 0.05, half_d + 0.05, -top_val * 0.012, 0,
                color="rgba(74,52,28,0.22)",
            ))
        traces.append(_cuboid_trace(
            idx - half_w, idx + half_w, -half_d, half_d, 0, z1,
            color=col, opacity=0.97, hover=f"{cat}: {fmt_val}",
        ))

    traces.append(go.Scatter3d(
        x=list(range(len(values))), y=[0] * len(values),
        z=[v + top_val * 0.09 for v in values],
        mode="text",
        text=[value_fmt(v) if value_fmt else f"{v:,.0f}" for v in values],
        textfont=dict(color=TEXT_PRIMARY, size=12, family="Inter, sans-serif"),
        hoverinfo="skip", showlegend=False,
    ))

    fig = go.Figure(data=traces)
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(tickvals=list(range(len(categories))), ticktext=categories, title=dict(text=""))
    layout["scene"]["yaxis"].update(showticklabels=False, title=dict(text=""), showbackground=False)
    layout["scene"]["zaxis"].update(title=dict(text=z_title))
    layout["scene"]["camera"] = camera or dict(
        eye=dict(x=0.35, y=-2.25, z=0.55),
        projection=dict(type="orthographic"),
    )
    layout["scene"]["aspectmode"] = "manual"
    layout["scene"]["aspectratio"] = dict(x=max(1.3, n / 2.6), y=0.55, z=0.7)
    fig.update_layout(**layout)
    fig.update_layout(showlegend=False)
    return fig


def grouped_bar3d_chart(categories, series: dict, colors: dict = None, height=420,
                         value_fmt=None, bar_ratio=0.34, gap=0.07, z_title=""):
    """
    A 3D grouped bar chart: each category on the x-axis holds one small
    extruded bar per series, arranged side-by-side along y. Use this in
    place of a stacked/grouped 2D bar chart (e.g. counts by category
    broken down by risk level).

    `series` is {series_name: [values aligned to categories]}.
    """
    categories = list(categories)
    names = list(series.keys())
    colors = colors or {}
    n_series = max(len(names), 1)
    all_vals = [v for vals in series.values() for v in vals] or [1.0]
    top_val = max(all_vals)

    half_w = bar_ratio / 2
    total_depth = n_series * (bar_ratio + gap)
    y_start = -total_depth / 2

    traces = []
    for s_idx, name in enumerate(names):
        vals = [float(v) for v in series[name]]
        col = colors.get(name, CHART_SEQ[s_idx % len(CHART_SEQ)])
        y0 = y_start + s_idx * (bar_ratio + gap)
        y1 = y0 + bar_ratio
        for c_idx, val in enumerate(vals):
            if val <= 0:
                continue
            z1 = max(val, top_val * 0.006)
            fmt_val = value_fmt(val) if value_fmt else f"{val:,.0f}"
            traces.append(_cuboid_trace(
                c_idx - half_w - 0.03, c_idx + half_w + 0.03, y0 - 0.02, y1 - 0.02, -top_val * 0.012, 0,
                color="rgba(74,52,28,0.22)",
            ))
            traces.append(_cuboid_trace(
                c_idx - half_w, c_idx + half_w, y0, y1, 0, z1,
                color=col, opacity=0.96, hover=f"{categories[c_idx]} - {name}: {fmt_val}",
            ))

    # one dummy marker per series purely to drive a readable legend
    for s_idx, name in enumerate(names):
        col = colors.get(name, CHART_SEQ[s_idx % len(CHART_SEQ)])
        traces.append(go.Scatter3d(
            x=[None], y=[None], z=[None], mode="markers",
            marker=dict(size=6, color=col), name=name, showlegend=True,
        ))

    fig = go.Figure(data=traces)
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(tickvals=list(range(len(categories))), ticktext=categories, title=dict(text=""))
    layout["scene"]["yaxis"].update(showticklabels=False, title=dict(text=""), showbackground=False)
    layout["scene"]["zaxis"].update(title=dict(text=z_title))
    layout["scene"]["camera"] = dict(
        eye=dict(x=0.4, y=-2.35, z=0.6),
        projection=dict(type="orthographic"),
    )
    layout["scene"]["aspectmode"] = "manual"
    layout["scene"]["aspectratio"] = dict(x=max(1.3, len(categories) / 2.6), y=0.65, z=0.7)
    fig.update_layout(**layout)
    fig.update_layout(legend=dict(font=dict(color=TEXT_PRIMARY, size=11), bgcolor="rgba(255,255,255,0.85)",
                                   bordercolor=CARD_BORDER, borderwidth=1, x=0.01, y=0.99))
    return fig


def target_bar3d(value, target, label, color, max_value=100, height=280, suffix="%"):
    """A single 3D 'thermometer' bar with a translucent target plate -
    used in place of a flat 2D gauge indicator."""
    z1 = max(value, max_value * 0.006)
    traces = [
        _cuboid_trace(-0.3, 0.3, -0.3, 0.3, -max_value * 0.02, 0, color="rgba(74,52,28,0.28)"),
        _cuboid_trace(-0.3, 0.3, -0.3, 0.3, 0, z1, color=color, opacity=0.96,
                      hover=f"{label}: {value:.1f}{suffix} (target {target:.0f}{suffix})"),
        _cuboid_trace(-0.42, 0.42, -0.42, 0.42, target - max_value * 0.012, target + max_value * 0.012,
                      color="rgba(139,46,46,0.45)", opacity=0.5, hover=f"Target: {target:.0f}{suffix}"),
        go.Scatter3d(
            x=[0], y=[0], z=[z1 + max_value * 0.1],
            mode="text", text=[f"{value:.1f}{suffix}"],
            textfont=dict(color=TEXT_PRIMARY, size=17, family="Source Serif 4, Georgia, serif"),
            hoverinfo="skip", showlegend=False,
        ),
    ]
    fig = go.Figure(data=traces)
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(visible=False)
    layout["scene"]["yaxis"].update(visible=False)
    layout["scene"]["zaxis"].update(range=[0, max_value], title=dict(text=""))
    layout["scene"]["camera"] = dict(eye=dict(x=1.4, y=-1.4, z=0.65),
                                      projection=dict(type="orthographic"))
    layout["scene"]["aspectmode"] = "manual"
    layout["scene"]["aspectratio"] = dict(x=0.6, y=0.6, z=1.15)
    fig.update_layout(**layout)
    fig.update_layout(showlegend=False,
                       title=dict(text=label, font=dict(family="Inter, sans-serif", size=12, color=TEXT_MUTED),
                                  x=0.5, xanchor="center", y=0.96))
    return fig


def ribbon3d_chart(x_labels, series: dict, height=380, z_title="Amount"):
    """A gently-raised Surface ribbon for two or more time series - a
    rotatable replacement for a flat area/line trend chart. The surface
    is flattened (shallow z, near-orthographic, near-overhead camera) so
    the trend line itself stays the focus and is easy to read left to
    right, rather than a dramatic wave that obscures its own values."""
    names = list(series.keys())
    n = len(x_labels)
    z = [list(series[name]) for name in names]
    x = list(range(n))
    y = list(range(len(names)))

    colorscale = [[0.0, TEAL_SOFT], [0.55, TEAL_LIGHT], [1.0, TEAL_DARK]]

    fig = go.Figure(data=[go.Surface(
        x=x, y=y, z=z, colorscale=colorscale, showscale=False, opacity=0.95,
        contours=dict(z=dict(show=True, usecolormap=True, project_z=True, width=1.5)),
        lighting=dict(ambient=0.75, diffuse=0.55, specular=0.2, roughness=0.6),
    )])

    step = max(1, n // 6)
    tick_idx = list(range(0, n, step))
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(tickvals=tick_idx, ticktext=[str(x_labels[i]) for i in tick_idx], title=dict(text=""))
    layout["scene"]["yaxis"].update(tickvals=y, ticktext=names, title=dict(text=""))
    layout["scene"]["zaxis"].update(title=dict(text=z_title))
    layout["scene"]["camera"] = dict(
        eye=dict(x=0.15, y=-2.5, z=1.0),
        projection=dict(type="orthographic"),
    )
    layout["scene"]["aspectmode"] = "manual"
    layout["scene"]["aspectratio"] = dict(x=2.2, y=0.35, z=0.45)
    fig.update_layout(**layout)
    return fig


def waterfall3d_chart(labels, values, height=420, colors=None):
    """
    A connected 3D waterfall. `values[0]` is an absolute starting total;
    each subsequent value is a relative delta on the running total
    (same semantics as go.Waterfall), rendered as linked extruded bars.
    """
    colors = colors or {}
    inc_color = colors.get("increasing", TEAL_DARK)
    dec_color = colors.get("decreasing", HIGH)
    tot_color = colors.get("total", TEAL_LIGHT)

    traces = []
    running = 0.0
    tops = []
    for idx, (label, val) in enumerate(zip(labels, values)):
        if idx == 0:
            base, top, color = 0.0, val, tot_color
            running = val
        else:
            base = running
            top = running + val
            color = inc_color if val >= 0 else dec_color
            running = top
        z0, z1 = (base, top) if top >= base else (top, base)
        tops.append(top)
        hover = f"{label}: {val:,.0f}" if idx == 0 else f"{label}: {val:+,.0f}"
        traces.append(_cuboid_trace(idx - 0.28, idx + 0.28, -0.28, 0.28, z0, max(z1, z0 + 0.01),
                                     color=color, opacity=0.96, hover=hover))

    max_top = max(tops) if tops else 1
    traces.append(go.Scatter3d(
        x=list(range(len(labels))), y=[0] * len(labels), z=tops,
        mode="lines", line=dict(color=TEXT_MUTED, width=3, dash="dot"),
        hoverinfo="skip", showlegend=False,
    ))
    traces.append(go.Scatter3d(
        x=list(range(len(labels))), y=[0] * len(labels),
        z=[t + max_top * 0.06 for t in tops],
        mode="text",
        text=[f"{v:,}" if i == 0 else f"{v:+,}" for i, v in enumerate(values)],
        textfont=dict(color=TEXT_PRIMARY, size=11, family="Inter, sans-serif"),
        hoverinfo="skip", showlegend=False,
    ))

    fig = go.Figure(data=traces)
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(tickvals=list(range(len(labels))), ticktext=labels, title=dict(text=""))
    layout["scene"]["yaxis"].update(visible=False)
    layout["scene"]["zaxis"].update(title=dict(text=""))
    layout["scene"]["camera"] = dict(
        eye=dict(x=0.3, y=-2.3, z=0.7),
        projection=dict(type="orthographic"),
    )
    layout["scene"]["aspectmode"] = "manual"
    layout["scene"]["aspectratio"] = dict(x=2.3, y=0.35, z=0.85)
    fig.update_layout(**layout)
    fig.update_layout(showlegend=False)
    return fig


def scatter3d_chart(x, y, z, color_labels=None, color_map=None, size=None,
                     hover_text=None, x_title="", y_title="", z_title="", height=420):
    """
    A genuine 3D scatter (Mesh3d markers via Scatter3d), used in place of
    a flat 2D scatter - e.g. transactions plotted by date, amount and a
    third dimension such as direction or channel, colored by group.
    """
    color_labels = list(color_labels) if color_labels is not None else ["All"] * len(x)
    color_map = color_map or {}
    groups = list(dict.fromkeys(color_labels))
    default_colors = teal_gradient(list(range(len(groups))) or [0])

    traces = []
    for g_idx, g in enumerate(groups):
        idxs = [i for i, lab in enumerate(color_labels) if lab == g]
        col = color_map.get(g, default_colors[g_idx % len(default_colors)])
        marker_size = [size[i] for i in idxs] if size is not None else 6
        traces.append(go.Scatter3d(
            x=[x[i] for i in idxs], y=[y[i] for i in idxs], z=[z[i] for i in idxs],
            mode="markers", name=str(g),
            marker=dict(size=marker_size, color=col, opacity=0.85,
                        line=dict(width=0.5, color=CARD_BORDER)),
            text=[hover_text[i] for i in idxs] if hover_text is not None else None,
            hoverinfo="text" if hover_text is not None else "x+y+z",
        ))

    fig = go.Figure(data=traces)
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(title=dict(text=x_title))
    layout["scene"]["yaxis"].update(title=dict(text=y_title))
    layout["scene"]["zaxis"].update(title=dict(text=z_title))
    layout["scene"]["camera"] = dict(eye=dict(x=1.6, y=-1.8, z=0.9))
    fig.update_layout(**layout)
    fig.update_layout(legend=dict(font=dict(color=TEXT_PRIMARY, size=11), bgcolor="rgba(255,255,255,0.85)",
                                   bordercolor=CARD_BORDER, borderwidth=1))
    return fig


def network3d_chart(center_label, center_kind, nodes, color_map, height=460):
    """
    A 3D ownership / relationship network: the reporting entity sits at
    the origin, each related node is placed around it in a circle with
    its elevation (z) driven by an optional weight (e.g. ownership %),
    and edges are drawn as 3D lines - a rotatable replacement for a flat
    2D node-link diagram.

    `nodes` is a list of dicts: {"label": str, "kind": str, "weight": float}
    where weight is 0-100 (e.g. ownership_pct) and drives elevation.
    `color_map` maps kind -> color, and must include an entry for
    `center_kind`.
    """
    import math

    n = max(len(nodes), 1)
    radius = 1.6
    node_x, node_y, node_z = [0.0], [0.0], [0.0]
    node_text, node_color, node_size = [center_label], [color_map.get(center_kind, TEAL_DARK)], [22]
    edge_traces = []

    for idx, node in enumerate(nodes):
        angle = 2 * math.pi * idx / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        weight = float(node.get("weight", 0) or 0)
        z = 0.25 + (weight / 100.0) * 1.5
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(f"{node['label']} ({weight:.0f}%)" if weight else node["label"])
        node_color.append(color_map.get(node.get("kind"), TEXT_MUTED))
        node_size.append(15)
        edge_traces.append(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            mode="lines", line=dict(color=CARD_BORDER, width=3),
            hoverinfo="skip", showlegend=False,
        ))

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z, mode="markers+text",
        text=node_text, textposition="top center",
        textfont=dict(color=TEXT_PRIMARY, size=11, family="Inter, sans-serif"),
        marker=dict(size=node_size, color=node_color, opacity=0.95,
                    line=dict(width=1.5, color=CARD_BG)),
        hoverinfo="text", showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    layout = _base_scene_layout(height)
    layout["scene"]["xaxis"].update(visible=False)
    layout["scene"]["yaxis"].update(visible=False)
    layout["scene"]["zaxis"].update(title=dict(text="Ownership"))
    layout["scene"]["camera"] = dict(eye=dict(x=1.8, y=-1.8, z=1.1))
    fig.update_layout(**layout)
    fig.update_layout(showlegend=False)
    return fig
