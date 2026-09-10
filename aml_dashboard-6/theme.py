"""
theme.py
Shared visual theme helpers for the AML Compliance Suite.

Design direction: professional / legal-office aesthetic rather than a
consumer "fintech" look - a light, paper-like background, a deep navy and
brass palette, a serif display face for headings paired with a clean sans
for body text and data, restrained (not neon) status colours, and square-
cornered "document tag" pills rather than rounded badges.

Import inject_css() at the top of every page for a consistent look.
"""

import textwrap
import streamlit as st

# ---------------------------------------------------------------- PALETTE
NAVY = "#1E3A5F"          # primary - deep navy (headers, primary buttons)
NAVY_DARK = "#12233B"     # header banner background
INK = "#1F2937"           # body text
MUTED = "#5B6472"         # secondary text
BRASS = "#9C7A34"         # accent - muted brass/gold, used sparingly
PAPER = "#FFFFFF"
PANEL = "#F7F8FA"         # card / secondary background
BORDER = "#DFE3E8"

CRITICAL = "#7A1E1E"      # deep maroon
HIGH = "#B5541F"          # burnt umber / amber
MEDIUM = "#8A6D1D"        # dark gold
LOW = "#1F6F50"           # deep forest green
INFO = "#2A4E73"          # muted steel blue

CHART_SEQUENCE = ["#1E3A5F", "#9C7A34", "#2A4E73", "#7A1E1E", "#1F6F50", "#5B6472"]


def inject_css():
    # NOTE: the CSS below must reach st.markdown with NO leading whitespace on
    # each line. Markdown treats 4+ spaces of indentation as a code block and
    # renders it as literal text (ignoring unsafe_allow_html) - textwrap.dedent
    # strips the indentation this f-string picks up from being inside a
    # function body, which is what previously caused the CSS to print on-screen
    # as plain text instead of being applied as a stylesheet.
    css = f"""
        <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
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

        /* ---------------- Header banner ---------------- */
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

        /* ---------------- KPI cards ---------------- */
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

        /* ---------------- Section headers ---------------- */
        .section-title {{
            font-family: 'Source Serif 4', Georgia, serif;
            font-size: 1.08rem;
            font-weight: 600;
            color: {NAVY_DARK};
            margin: 1.8rem 0 0.7rem 0;
            padding-bottom: 0.45rem;
            border-bottom: 2px solid {NAVY};
        }}

        /* ---------------- Status / risk tags ---------------- */
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
        table tbody tr:nth-child(even) {{
            background: {PANEL};
        }}
        table tbody tr:hover {{
            background: #EEF1F5;
        }}

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
        </style>
        """
    st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", badge: str = ""):
    badge_html = f'<span class="suite-badge">{badge}</span>' if badge else ""
    html = f"""
        <div class="suite-header">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            {badge_html}
        </div>
        """
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", sub_color: str = MUTED):
    html = f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub" style="color:{sub_color};">{sub}</div>
        </div>
        """
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
    """Common layout kwargs to keep every chart on-brand. Usage: fig.update_layout(**plotly_layout_defaults())"""
    return dict(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=INK),
        margin=dict(t=10, b=10, l=10, r=10),
    )
