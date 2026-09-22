"""
theme.py
Shared visual theme for the AML/CTF Compliance Suite.

Design direction: this reads as a real regulatory-office tool - the kind
of internal system an AUSTRAC-regulated law firm's compliance team would
actually use - rather than a consumer fintech app. Slate/ink base, a single
restrained signal-red used ONLY for genuine risk/alert states (never as a
decorative accent), and a muted brass used for the firm's own brand mark.
Charts are flat 2D (bar, line, donut, matrix) - the standard vocabulary of
a real compliance/BI reporting tool - with tight margins so each chart
fills its card.
"""

import textwrap
import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------- PALETTE
# Cool slate base (paper-grey, not warm cream) - a case-management tool,
# not a marketing site. Ink-navy for structure/type, a single restrained
# signal red reserved for genuine risk states, muted brass as the one
# warm accent (used sparingly - firm branding, not decoration).
BG_1          = "#EEF1F4"
BG_2          = "#F5F7F9"
CARD_BG       = "#FFFFFF"
CARD_BORDER   = "#DCE2E8"
CARD_SHADOW   = "0 1px 2px rgba(15,23,32,0.06), 0 1px 1px rgba(15,23,32,0.04)"

INK_DARK      = "#10202E"   # primary text / headings
INK_MID       = "#1E3A4E"   # secondary structural color
SLATE         = "#4A5D6B"   # body text muted
SLATE_LIGHT   = "#8A99A6"

SIGNAL_RED    = "#B4232C"   # reserved for High risk / open alerts only
SIGNAL_AMBER  = "#B4711F"
SIGNAL_GREEN  = "#2C6B4F"
SIGNAL_BLUE   = "#1F5C8B"

BRASS         = "#9C7A3C"   # firm-brand accent, used sparingly
BRASS_SOFT    = "#F1E9D8"

TEXT_PRIMARY  = INK_DARK
TEXT_MUTED    = SLATE

CRITICAL      = SIGNAL_RED
HIGH          = "#C4531F"
MEDIUM        = SIGNAL_AMBER
LOW           = SIGNAL_GREEN
INFO          = SIGNAL_BLUE

CHART_GRID    = "#E1E7EC"
CHART_SEQ     = ["#1F5C8B", "#9C7A3C", "#2C6B4F", "#B4232C", "#4A5D6B",
                  "#6E8CA0", "#C4A15E", "#5E8271", "#8C5A5A", "#3A5468"]

RISK_COLOR_MAP = {"Low": LOW, "Medium": MEDIUM, "High": HIGH, "Critical": CRITICAL}
STATUS_COLOR_MAP = {
    "Open": SIGNAL_RED,
    "Escalated to Case": SIGNAL_AMBER,
    "Closed - False Positive": SLATE_LIGHT,
    "Closed - No Issue": SIGNAL_GREEN,
}


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
_CSS = """<style>
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: {TEXT_PRIMARY};
}}
.stApp {{
    background: linear-gradient(180deg, {BG_1} 0%, {BG_2} 100%);
    background-attachment: fixed;
}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1320px; }}
h1, h2, h3 {{ color: {INK_DARK}; font-weight: 700; }}

.suite-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem 1.6rem;
    background: {INK_DARK};
    border-radius: 8px;
    margin-bottom: 1.5rem;
    gap: 1rem; flex-wrap: wrap;
}}
.suite-header h1 {{
    font-size: 1.3rem; font-weight: 700; margin: 0; color: #FFFFFF;
    letter-spacing: -0.01em;
}}
.suite-header p {{
    margin: 0.25rem 0 0 0; color: #A9BAC6; font-size: 0.84rem;
}}
.suite-badge {{
    background: {BRASS}; color: #FFFFFF;
    padding: 0.28rem 0.85rem; border-radius: 4px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.04em;
    white-space: nowrap;
}}

.kpi-card {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-left: 3px solid {INK_MID};
    border-radius: 6px; box-shadow: {CARD_SHADOW};
    padding: 0.95rem 1.1rem; height: 100%;
    transition: box-shadow 0.15s ease, transform 0.15s ease;
}}
.kpi-card:hover {{ box-shadow: 0 4px 14px rgba(15,23,32,0.10); transform: translateY(-1px); }}
.kpi-card.risk-high {{ border-left-color: {SIGNAL_RED}; }}
.kpi-card.risk-medium {{ border-left-color: {SIGNAL_AMBER}; }}
.kpi-card.risk-low {{ border-left-color: {SIGNAL_GREEN}; }}
.kpi-label {{
    color: {TEXT_MUTED}; font-size: 0.71rem; text-transform: uppercase;
    letter-spacing: 0.06em; font-weight: 600; margin-bottom: 0.4rem;
}}
.kpi-value {{ color: {INK_DARK}; font-size: 1.75rem; font-weight: 700; line-height: 1.05; }}
.kpi-sub {{ font-size: 0.76rem; margin-top: 0.35rem; color: {TEXT_MUTED}; }}
.kpi-trend-up {{ color: {SIGNAL_GREEN}; font-weight: 700; }}
.kpi-trend-down {{ color: {SIGNAL_RED}; font-weight: 700; }}
.bi-kpi-row {{ display: flex; align-items: baseline; gap: 0.4rem; margin-top: 0.35rem; font-size: 0.77rem; }}

.section-title {{
    font-size: 1.0rem; font-weight: 700; color: {INK_DARK};
    margin: 1.6rem 0 0.6rem 0; padding-bottom: 0.4rem;
    border-bottom: 2px solid {BRASS};
}}

div[data-testid="stPlotlyChart"] {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 8px; box-shadow: {CARD_SHADOW};
    padding: 0.35rem 0.4rem 0.1rem 0.4rem; overflow: hidden;
}}

.pill {{
    display: inline-block; padding: 0.14rem 0.55rem; font-size: 0.68rem;
    font-weight: 700; letter-spacing: 0.02em; border-radius: 3px; border: 1px solid;
}}
.pill-critical {{ background: #FBE6E5; color: {CRITICAL}; border-color: #EBB7B4; }}
.pill-high     {{ background: #FBEBDE; color: {HIGH};     border-color: #E9C49B; }}
.pill-medium   {{ background: #FAF0DC; color: {MEDIUM};   border-color: #E4C88F; }}
.pill-low      {{ background: #E3EFE8; color: {LOW};      border-color: #A9CBB6; }}
.pill-info     {{ background: #E4EEF5; color: {INFO};     border-color: #A9C6DA; }}
.pill-neutral  {{ background: #EEF1F4; color: {SLATE};    border-color: {CARD_BORDER}; }}

div[data-testid="stMetric"] {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-left: 3px solid {INK_MID}; box-shadow: {CARD_SHADOW};
    padding: 0.85rem 1rem; border-radius: 6px;
}}
div[data-testid="stMetricValue"] {{ color: {INK_DARK}; font-weight: 700; }}
div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED}; text-transform: uppercase; font-size: 0.71rem;
    letter-spacing: 0.05em; font-weight: 600;
}}

table {{
    border-collapse: separate; border-spacing: 0; width: 100%;
    font-size: 0.84rem; background: {CARD_BG};
    border: 1px solid {CARD_BORDER}; border-radius: 6px; overflow: hidden;
    box-shadow: {CARD_SHADOW};
}}
table thead th {{
    background: {INK_DARK}; color: #FFFFFF; text-align: left;
    padding: 0.55rem 0.7rem; font-weight: 600; font-size: 0.71rem;
    text-transform: uppercase; letter-spacing: 0.04em;
}}
table tbody td {{ padding: 0.48rem 0.7rem; border-bottom: 1px solid {CHART_GRID}; color: {TEXT_PRIMARY}; }}
table tbody tr:last-child td {{ border-bottom: none; }}
table tbody tr:nth-child(even) {{ background: {BG_2}; }}
table tbody tr:hover td {{ background: #E4EEF5; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 2px; border-bottom: 1px solid {CARD_BORDER}; }}
.stTabs [data-baseweb="tab"] {{ padding: 0.6rem 1.1rem; font-weight: 600; color: {TEXT_MUTED}; font-size: 0.87rem; }}
.stTabs [aria-selected="true"] {{
    color: {INK_DARK} !important; border-bottom: 3px solid {BRASS} !important;
    background: transparent !important;
}}

.stButton>button, .stDownloadButton>button {{
    border-radius: 4px; border: 1px solid {INK_MID}; background: {CARD_BG};
    color: {INK_MID}; font-weight: 600; font-size: 0.85rem;
}}
.stButton>button:hover {{ background: #E4EEF5; }}
.stButton>button[kind="primary"] {{ background: {INK_DARK}; border-color: {INK_DARK}; color: #FFF; }}

section[data-testid="stSidebar"] {{ background: {CARD_BG}; border-right: 1px solid {CARD_BORDER}; }}
div[data-testid="stAlert"] {{ border-radius: 4px; border-left: 4px solid {INK_MID}; }}
hr {{ border-color: {CARD_BORDER}; margin: 1.4rem 0; }}

.methodology-note {{
    background: {BG_2}; border: 1px dashed {CARD_BORDER}; border-radius: 6px;
    padding: 0.7rem 0.9rem; font-size: 0.8rem; color: {TEXT_MUTED}; margin: 0.6rem 0 1rem 0;
}}
.methodology-note b {{ color: {INK_DARK}; }}
</style>"""


def inject_css():
    st.markdown(textwrap.dedent(_CSS.format(**globals())), unsafe_allow_html=True)


# --------------------------------------------------------------------------
# UI HELPERS
# --------------------------------------------------------------------------
def page_header(title: str, subtitle: str = "", badge: str = ""):
    badge_html = f'<span class="suite-badge">{badge}</span>' if badge else ""
    st.markdown(
        f'<div class="suite-header"><div><h1>{title}</h1><p>{subtitle}</p></div>{badge_html}</div>',
        unsafe_allow_html=True,
    )


def methodology_note(html: str):
    """A small dashed-border callout explaining WHY a number/chart is
    computed the way it is - ties every page back to 01_business_design.md
    so a reviewer can see the methodology, not just the output."""
    st.markdown(f'<div class="methodology-note">{html}</div>', unsafe_allow_html=True)


def kpi_card(label, value, sub="", risk_class=""):
    cls = f"kpi-card {risk_class}".strip()
    st.markdown(
        f'<div class="{cls}"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def kpi_card_trend(label, value, delta="", sub="", higher_is_better=True):
    trend_html = ""
    if delta:
        is_up = delta.strip().startswith("+")
        good = is_up if higher_is_better else (not is_up)
        cls = "kpi-trend-up" if good else "kpi-trend-down"
        arrow = "\u25B2" if is_up else "\u25BC"
        trend_html = f'<span class="{cls}">{arrow} {delta.lstrip("+-")}</span>'
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="bi-kpi-row">{trend_html}<span>{sub}</span></div></div>',
        unsafe_allow_html=True,
    )


def risk_pill(level: str) -> str:
    cls = {"critical": "pill-critical", "high": "pill-high", "medium": "pill-medium",
           "low": "pill-low"}.get((level or "").lower(), "pill-info")
    return f'<span class="pill {cls}">{level}</span>'


def status_pill(status: str) -> str:
    cls = {
        "open": "pill-critical", "escalated to case": "pill-medium",
        "closed - false positive": "pill-neutral", "closed - no issue": "pill-low",
    }.get((status or "").lower(), "pill-neutral")
    return f'<span class="pill {cls}">{status}</span>'


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# FLAT 2D CHART ENGINE
# --------------------------------------------------------------------------
def _flat_layout(height=300, legend=False, title=""):
    layout = dict(
        template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=11),
        margin=dict(t=30 if title else (26 if legend else 8), b=8, l=8, r=10),
        height=height, bargap=0.32,
        xaxis=dict(gridcolor=CHART_GRID, zeroline=False, linecolor=CARD_BORDER,
                    tickfont=dict(color=TEXT_MUTED, size=10.5)),
        yaxis=dict(gridcolor=CHART_GRID, zeroline=False, linecolor=CARD_BORDER,
                    tickfont=dict(color=TEXT_MUTED, size=10.5)),
        hoverlabel=dict(bgcolor=CARD_BG, bordercolor=CARD_BORDER,
                         font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12)),
        showlegend=legend,
    )
    if legend:
        layout["legend"] = dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0,
                                 font=dict(color=TEXT_PRIMARY, size=10.5))
    if title:
        layout["title"] = dict(text=title, font=dict(size=14, color=INK_DARK), x=0.0, xanchor="left", y=0.97)
    return layout


def bar_chart(categories, values, colors=None, horizontal=False, height=300,
              value_fmt=None, axis_title=""):
    categories = list(categories); values = [float(v) for v in values]
    if colors is None:
        colors = [CHART_SEQ[0]] * len(values)
    if isinstance(colors, str):
        colors = [colors] * len(values)
    text = [value_fmt(v) if value_fmt else f"{v:,.0f}" for v in values]
    bar = go.Bar(
        x=values if horizontal else categories, y=categories if horizontal else values,
        orientation="h" if horizontal else "v",
        marker=dict(color=colors, line=dict(width=0.6, color="rgba(16,32,46,0.12)")),
        text=text, textposition="outside", cliponaxis=False,
        textfont=dict(color=TEXT_PRIMARY, size=10.5),
        hovertemplate=("%{y}: %{x:,.0f}<extra></extra>" if horizontal else "%{x}: %{y:,.0f}<extra></extra>"),
    )
    fig = go.Figure(data=[bar])
    layout = _flat_layout(height)
    if horizontal:
        layout["yaxis"].update(showgrid=False, categoryorder="total ascending")
        layout["xaxis"].update(showgrid=True, title=dict(text=axis_title))
    else:
        layout["xaxis"].update(showgrid=False)
        layout["yaxis"].update(showgrid=True, title=dict(text=axis_title))
    fig.update_layout(**layout)
    return fig


def grouped_bar_chart(categories, series: dict, colors: dict = None, height=320,
                       horizontal=False, axis_title=""):
    categories = list(categories); names = list(series.keys()); colors = colors or {}
    traces = []
    for i, name in enumerate(names):
        vals = [float(v) for v in series[name]]
        col = colors.get(name, CHART_SEQ[i % len(CHART_SEQ)])
        hover = (f"{name} - %{{y}}: %{{x:,.0f}}<extra></extra>") if horizontal else \
                (f"{name} - %{{x}}: %{{y:,.0f}}<extra></extra>")
        traces.append(go.Bar(
            x=vals if horizontal else categories, y=categories if horizontal else vals,
            orientation="h" if horizontal else "v", name=name,
            marker=dict(color=col, line=dict(width=0.6, color="rgba(16,32,46,0.12)")),
            hovertemplate=hover,
        ))
    fig = go.Figure(data=traces)
    layout = _flat_layout(height, legend=True)
    layout["barmode"] = "group"
    if horizontal:
        layout["yaxis"].update(showgrid=False, categoryorder="array", categoryarray=list(reversed(categories)))
        layout["xaxis"].update(showgrid=True, title=dict(text=axis_title))
    else:
        layout["xaxis"].update(showgrid=False, categoryorder="array", categoryarray=categories)
        layout["yaxis"].update(showgrid=True, title=dict(text=axis_title))
    fig.update_layout(**layout)
    return fig


def line_area_chart(x_labels, series: dict, colors=None, height=300, y_title="", area=True):
    names = list(series.keys()); colors = colors or {}
    traces = []
    for i, name in enumerate(names):
        col = colors.get(name, CHART_SEQ[i % len(CHART_SEQ)])
        r, g, b = tuple(int(col.lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
        traces.append(go.Scatter(
            x=list(x_labels), y=list(series[name]), mode="lines", name=name,
            line=dict(color=col, width=2.3, shape="spline", smoothing=0.3),
            fill="tozeroy" if area else None,
            fillcolor=f"rgba({r},{g},{b},0.10)" if area else None,
            hovertemplate=f"{name} - %{{x}}: %{{y:,.0f}}<extra></extra>",
        ))
    fig = go.Figure(data=traces)
    layout = _flat_layout(height, legend=len(names) > 1)
    layout["xaxis"].update(showgrid=False)
    layout["yaxis"].update(showgrid=True, title=dict(text=y_title))
    fig.update_layout(**layout, hovermode="x unified")
    return fig


def donut_chart(labels, values, colors=None, height=280, center_label="", center_value=""):
    labels = list(labels); values = [float(v) for v in values]
    if colors is None:
        colors = CHART_SEQ[:len(labels)]
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.64, sort=False,
        marker=dict(colors=colors, line=dict(color=CARD_BG, width=2)),
        textinfo="percent", textfont=dict(size=10.5, color=TEXT_PRIMARY),
        hovertemplate="%{label}: %{value:,.0f} (%{percent})<extra></extra>",
    )])
    annotations = []
    if center_value:
        annotations.append(dict(text=f"<b>{center_value}</b>", x=0.5, y=0.56, showarrow=False,
                                 font=dict(size=18, color=INK_DARK)))
    if center_label:
        annotations.append(dict(text=center_label, x=0.5, y=0.40, showarrow=False,
                                 font=dict(size=9.5, color=TEXT_MUTED)))
    fig.update_layout(
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", height=height,
        margin=dict(t=6, b=6, l=6, r=6), annotations=annotations,
        legend=dict(orientation="v", x=1.0, y=0.5, font=dict(color=TEXT_PRIMARY, size=10)),
    )
    return fig


def waterfall_chart(labels, values, height=340, colors=None):
    colors = colors or {}
    measures = ["absolute"] + ["relative"] * (len(values) - 1)
    text = [f"{values[0]:,.0f}"] + [f"{v:+,.0f}" for v in values[1:]]
    fig = go.Figure(go.Waterfall(
        x=list(labels), y=list(values), measure=measures, text=text, textposition="outside",
        textfont=dict(color=TEXT_PRIMARY, size=10.5),
        increasing=dict(marker=dict(color=colors.get("increasing", INFO))),
        decreasing=dict(marker=dict(color=colors.get("decreasing", SIGNAL_RED))),
        totals=dict(marker=dict(color=colors.get("total", INK_MID))),
        connector=dict(line=dict(color=CARD_BORDER, width=1.2)),
    ))
    layout = _flat_layout(height, legend=False)
    layout["xaxis"].update(showgrid=False); layout["yaxis"].update(showgrid=True)
    fig.update_layout(**layout)
    return fig


def matrix_table_html(row_labels, col_labels, values, row_header="", value_fmt=None, color=None):
    color = color or INFO
    flat = [v for row in values for v in row]
    vmax = max(flat) if flat else 0
    vmax = vmax or 1
    def fmt(v): return value_fmt(v) if value_fmt else f"{v:,.0f}"
    thead = f"<th>{row_header}</th>" + "".join(f"<th>{c}</th>" for c in col_labels)
    body = []
    for r_label, row in zip(row_labels, values):
        cells = []
        for v in row:
            pct = 0 if v <= 0 else max(6, round(v / vmax * 100))
            cells.append(
                f'<td><div style="position:relative;height:1.4em;">'
                f'<div style="position:absolute;top:1px;bottom:1px;right:0;width:{pct}%;'
                f'background:{color}28;border-radius:2px;"></div>'
                f'<span style="position:relative;font-weight:600;">{fmt(v)}</span></div></td>'
            )
        body.append(f"<tr><td style=\"font-weight:600;\">{r_label}</td>{''.join(cells)}</tr>")
    return ('<div style="overflow-x:auto;"><table><thead><tr>' + thead + "</tr></thead><tbody>"
            + "".join(body) + "</tbody></table></div>")
