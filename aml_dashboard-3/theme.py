"""
theme.py
Shared visual theme helpers for the AML Compliance Suite.
Import inject_css() at the top of every page for a consistent look.
"""

import streamlit as st

PRIMARY = "#2DD4BF"      # teal accent
DANGER = "#F87171"       # high risk
WARNING = "#FBBF24"      # medium risk
SUCCESS = "#34D399"      # low risk / clear
INFO = "#60A5FA"
BG_CARD = "#111827"
BORDER = "#1F2937"


def inject_css():
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }}

        /* Hide default streamlit chrome for a cleaner app feel */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        /* Page title banner */
        .suite-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.1rem 1.6rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #0F172A 0%, #14202E 60%, #0F2A28 100%);
            border: 1px solid {BORDER};
            margin-bottom: 1.4rem;
        }}
        .suite-header h1 {{
            font-size: 1.5rem;
            margin: 0;
            color: #F8FAFC;
        }}
        .suite-header p {{
            margin: 0.15rem 0 0 0;
            color: #94A3B8;
            font-size: 0.92rem;
        }}
        .suite-badge {{
            background: rgba(45, 212, 191, 0.12);
            color: {PRIMARY};
            border: 1px solid rgba(45, 212, 191, 0.35);
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        /* KPI cards */
        .kpi-card {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 1rem 1.2rem;
            height: 100%;
        }}
        .kpi-label {{
            color: #94A3B8;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.3rem;
        }}
        .kpi-value {{
            color: #F8FAFC;
            font-size: 1.65rem;
            font-weight: 700;
            line-height: 1.1;
        }}
        .kpi-sub {{
            font-size: 0.8rem;
            margin-top: 0.35rem;
        }}

        /* Section headers */
        .section-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #F1F5F9;
            margin: 1.6rem 0 0.6rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid {BORDER};
        }}

        /* Badges for risk / status pills */
        .pill {{
            display: inline-block;
            padding: 0.18rem 0.65rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 600;
        }}
        .pill-critical {{ background: rgba(248,113,113,0.15); color: {DANGER}; border: 1px solid rgba(248,113,113,0.4); }}
        .pill-high     {{ background: rgba(248,113,113,0.12); color: {DANGER}; border: 1px solid rgba(248,113,113,0.3); }}
        .pill-medium   {{ background: rgba(251,191,36,0.13); color: {WARNING}; border: 1px solid rgba(251,191,36,0.35); }}
        .pill-low      {{ background: rgba(52,211,153,0.13); color: {SUCCESS}; border: 1px solid rgba(52,211,153,0.35); }}
        .pill-info     {{ background: rgba(96,165,250,0.13); color: {INFO}; border: 1px solid rgba(96,165,250,0.35); }}

        div[data-testid="stMetric"] {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 0.8rem 1rem;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {BG_CARD};
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", badge: str = ""):
    badge_html = f'<span class="suite-badge">{badge}</span>' if badge else ""
    st.markdown(
        f"""
        <div class="suite-header">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, sub: str = "", sub_color: str = "#94A3B8"):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub" style="color:{sub_color};">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
