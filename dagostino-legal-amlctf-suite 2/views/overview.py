"""Overview — the whole compliance posture on one screen (no scrolling at 1440×900):

  header bar   brand · period · alert filters · "view by" switch
  row 1        MAIN KPIs rail | alert investigation pipeline (typology sources → five workflow stages)
  row 2        clients by <dim> (risk-tier split) | alert outcomes by <dim> | compliance metrics table

Every number is derived from core.model / core.metrics for the selected reporting period — the
layout changes, the single source of truth does not.
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import metrics as X
from core import ui
from core.ref import TYPOLOGY_NAMES, DISPOSITIONS, BRANCH_NAMES, AU_STATE_NAMES
from core.theme import (inject_css, LIME, SLATE, INK, MUTED, FAINT, AMBER, TITLE, CARD, CARD_2,
                        TIER_COLORS, TYP_COLORS, SMR_COLOR)

GEO_DIMS = ["State", "Risk Tier", "Typology", "Channel"]
TYP_SHORT = {"Structuring / smurfing": "Structuring", "Rapid movement of funds": "Rapid movement",
             "High-risk jurisdiction transfer": "High-risk jurisdiction", "Cash-intensive pattern": "Cash-intensive",
             "Trade-based ML indicator": "Trade-based ML"}
CHANNEL_SHORT = {"Non face-to-face (digital)": "Digital", "Introduced / referral": "Referral",
                 "Third-party intermediary": "Intermediary"}
ROW2_H = 244          # plot height shared by the two breakdown charts so the row lines up


# ------------------------------------------------------------------------------------------ header ----
def _header_bar(cur, cmp):
    with st.container(key="ov_header"):
        c_brand, c_status, c_branch, c_tier, c_typ, c_view = st.columns([1.95, 1.15, 1.15, 1.05, 1.3, 2.95],
                                                                        vertical_alignment="center")
        with c_brand:
            st.markdown('<div class="ov-brand"><div class="ov-brand-badge">D</div><div>'
                        '<div class="ov-brand-title">Compliance Overview</div>'
                        f'<div class="ov-brand-sub">{cur.label} · {cur.short()}</div></div></div>', unsafe_allow_html=True)
        with c_status:
            st.selectbox("Alert status", ["All"] + DISPOSITIONS, key="ov_f_status",
                         format_func=lambda v: "Status: all" if v == "All" else v)
        with c_branch:
            st.selectbox("Branch", ["All"] + BRANCH_NAMES, key="ov_f_branch",
                         format_func=lambda v: "Branch: all" if v == "All" else v)
        with c_tier:
            st.selectbox("Risk tier", ["All", "Low", "Medium", "High"], key="ov_f_tier",
                         format_func=lambda v: "Risk: all" if v == "All" else f"{v} risk")
        with c_typ:
            st.selectbox("Typology", ["All"] + TYPOLOGY_NAMES, key="ov_f_typ",
                         format_func=lambda v: "Typology: all" if v == "All" else v)
        with c_view:
            lab, pills = st.columns([0.16, 1], vertical_alignment="center")
            lab.markdown('<div class="bd-label">View by</div>', unsafe_allow_html=True)
            with pills:
                st.pills("View by", GEO_DIMS, default="State", key="ov_geo_dim", label_visibility="collapsed",
                         on_change=_keep_one_dim)
    return st.session_state.get("ov_geo_dim") or "State"


def _keep_one_dim():
    """Pills can be clicked off; clicking the active one again keeps it selected instead of leaving
    the charts on an unhighlighted fallback."""
    ss = st.session_state
    if ss.get("ov_geo_dim") is None:
        ss["ov_geo_dim"] = ss.get("_ov_geo_dim_last", "State")
    ss["_ov_geo_dim_last"] = ss["ov_geo_dim"]


def _filtered_alerts(M, cur):
    a = X.alerts_in(M, cur)
    status, branch, tier, typ = (st.session_state.get(k, "All") for k in ("ov_f_status", "ov_f_branch", "ov_f_tier", "ov_f_typ"))
    if status != "All":
        a = a[a["disposition"] == status]
    if branch != "All":
        a = a[a["branch"] == branch]
    if tier != "All":
        a = a[a["risk_tier"] == tier]
    if typ != "All":
        a = a[a["typology"] == typ]
    return a


# ------------------------------------------------------------------------------------------ KPI rail ----
def _kpi_rail(M, cur, cmp):
    H = X.headline(M, cur, cmp)
    items = [
        ("Clients screened", ui.fmt_num(H["fc"]["screenings"]) if H["fc"] is not None else "—", "in period"),
        ("Active alerts", f"{H['active_alerts']:.0f}", "open at period end"),
        ("SMRs filed", f"{H['smrs_ytd']}", "financial year to date"),
        ("Overdue reviews", f"{H['overdue_reviews']:.0f}",
         f"{ui.fmt_pct(H['overdue_reviews'] / H['active_customers']) if H['active_customers'] else '—'} of active book"),
    ]
    html = '<div class="kpi-rail-wrap"><div class="kpi-rail-title">MAIN KPIs</div><div class="kpi-rail">' + "".join(
        f'<div class="kpi-rail-card"><div class="kpi-rail-value">{v}</div><div class="kpi-rail-label">{lab}</div>'
        f'<div class="kpi-rail-sub">{sub}</div></div>' for lab, v, sub in items) + "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


# ------------------------------------------------------------------------------------------ pipeline ----
# Typology sources flow (even-width ribbons) into the first stage; after that each stage is a dark track
# with a solid lime bar whose height is the stage's alert count, and grey tapered connectors show the
# drop-off between stages. Drawn as one inline SVG with a fixed viewBox so it scales uniformly with the
# card (circles stay round, bands stay even) — Plotly shapes on a stretched 0-100 axis can't do that.
def _svg_esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _pipeline_svg(pf, typ_labels, typ_counts):
    W, H = 1000, 262
    TRACK_Y0, TRACK_Y1 = 72, 214
    BAR_TOP, BAR_BOT = TRACK_Y0 + 22, TRACK_Y1 - 6        # bar zone sits below the track's "Info" label
    MID = (BAR_TOP + BAR_BOT) / 2
    BAR_MAX = BAR_BOT - BAR_TOP
    X0, W_COL, GAP = 300, 112, 33              # 5 columns * 112 + 4 gaps * 33 = 692 -> ends at 992
    lag = pf["smr_lag_days"]
    stages = [
        ("Alert generated", pf["total"],
         "Every transaction-monitoring alert opened in the period.",
         [(AMBER, f"{pf['open']} awaiting triage")] if pf["open"] else [(FAINT, "all triaged")]),
        ("L1 triage", pf["triaged"],
         "First-line review: is the rule hit explained by known client activity?",
         [(FAINT, f"{pf['closed_fp']} false positives")]),
        ("L2 investigation", pf["l2"],
         "Full investigation: source of funds, related parties, prior alerts.",
         [(SLATE, f"{pf['closed_nfa']} closed, no action")]
         + ([(AMBER, f"{pf['under_investigation']} still open")] if pf["under_investigation"] else [])),
        ("MLRO review", pf["mlro"],
         "The MLRO decides whether a suspicion is formed and an SMR is required.",
         [(LIME, "suspicion formed")]),
        ("SMR lodged", pf["smr_lodged"],
         "Suspicious Matter Report submitted to AUSTRAC.",
         ([(AMBER, f"{pf['smr_drafting']} in drafting")] if pf["smr_drafting"] else [])
         + ([(FAINT, f"avg {lag:.1f}d to lodge")] if lag == lag else [])),
    ]
    vmax = max(c for _, c, *_ in stages) or 1
    bar_h = [max(BAR_MAX * c / vmax, 3 if c else 0) for _, c, *_ in stages]

    out = [f'<svg class="pipe-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Alert investigation pipeline">']

    # ---- source column header + ribbons into the first bar (stacked like a Sankey node column) ----
    SX, RX0, RX1 = 206, 212, X0
    out.append(f'<text x="{SX + 6}" y="18" text-anchor="end" class="pipe-name">Alert source</text>'
               f'<text x="{SX + 6}" y="34" text-anchor="end" class="pipe-sub">Monitoring rule · alerts</text>')
    tot = sum(typ_counts) or 1
    band = [bar_h[0] * c / tot for c in typ_counts]
    n = len(band)
    span_avail = TRACK_Y1 - TRACK_Y0 + 34
    gap = max((span_avail - sum(band)) / max(n - 1, 1), 12)
    y = MID - (sum(band) + gap * (n - 1)) / 2
    tgt = MID - bar_h[0] / 2
    for label, c, b in zip(typ_labels, typ_counts, band):
        col = TYP_COLORS[TYPOLOGY_NAMES.index(label) % len(TYP_COLORS)]
        sy0, sy1, ty0, ty1 = y, y + b, tgt, tgt + b
        xm = (RX0 + RX1) / 2
        path = (f"M{RX0},{sy0:.1f} C{xm},{sy0:.1f} {xm},{ty0:.1f} {RX1},{ty0:.1f} "
                f"L{RX1},{ty1:.1f} C{xm},{ty1:.1f} {xm},{sy1:.1f} {RX0},{sy1:.1f} Z")
        cy = (sy0 + sy1) / 2
        out.append(f'<g class="pipe-src"><title>{_svg_esc(label)}: {c} alerts ({c / tot:.0%})</title>'
                   f'<path d="{path}" fill="{col}" fill-opacity="0.72"/>'
                   f'<rect x="{RX0 - 2}" y="{sy0:.1f}" width="3" height="{max(b, 1):.1f}" fill="{col}"/>'
                   f'<circle cx="{SX}" cy="{cy:.1f}" r="4.5" fill="{CARD}" stroke="{col}" stroke-width="1.8"/>'
                   f'<text x="{SX - 11}" y="{cy + 3.8:.1f}" text-anchor="end" class="pipe-src-lbl">{_svg_esc(label)}'
                   f'<tspan class="pipe-src-n" dx="5">{c}</tspan></text></g>')
        y += b + gap
        tgt += b

    # ---- stage columns ----
    for i, ((name, c, info, notes), h) in enumerate(zip(stages, bar_h)):
        x = X0 + i * (W_COL + GAP)
        cx = x + W_COL / 2
        conv = "" if i == 0 else (f" · {c / stages[i - 1][1]:.0%} of previous stage" if stages[i - 1][1] else "")
        out.append(f'<g class="pipe-stage"><title>{_svg_esc(name)}: {c} alerts{conv}. {_svg_esc(info)}</title>'
                   f'<text x="{x}" y="18" class="pipe-name">{_svg_esc(name)}</text>'
                   f'<text x="{x}" y="34" class="pipe-sub">Total alerts</text>'
                   f'<text x="{x}" y="58" class="pipe-num">{c:,}</text>'
                   f'<rect x="{x}" y="{TRACK_Y0}" width="{W_COL}" height="{TRACK_Y1 - TRACK_Y0}" rx="2" class="pipe-track"/>'
                   f'<text x="{cx}" y="{TRACK_Y0 + 14}" text-anchor="middle" class="pipe-info">Info</text>'
                   + (f'<rect x="{x}" y="{MID - h / 2:.1f}" width="{W_COL}" height="{h:.1f}" class="pipe-bar"/>' if h else "")
                   + '</g>')
        for j, (dot, txt) in enumerate(notes[:2]):
            ny = TRACK_Y1 + 18 + j * 16
            out.append(f'<circle cx="{x + 4}" cy="{ny - 3.8}" r="3.4" fill="{dot}"/>'
                       f'<text x="{x + 12}" y="{ny}" class="pipe-note-t">{_svg_esc(txt)}</text>')

    # ---- grey tapered connectors: left edge = previous bar, right edge = next bar ----
    for i in range(len(stages) - 1):
        xa = X0 + i * (W_COL + GAP) + W_COL + 5
        xb = xa + GAP - 10
        ha, hb = bar_h[i] * 0.86, bar_h[i + 1] * 0.86
        if ha < 1 and hb < 1:
            continue
        out.append(f'<polygon points="{xa},{MID - ha / 2:.1f} {xb},{MID - hb / 2:.1f} {xb},{MID + hb / 2:.1f} '
                   f'{xa},{MID + ha / 2:.1f}" class="pipe-conn"/>')
    out.append("</svg>")
    return "".join(out)


PIPE_CSS = f"""<style>
.pipe-svg {{ width:100%; height:auto; display:block; font-family:Inter, 'Source Sans Pro', sans-serif; }}
.pipe-name {{ font-size:13px; font-weight:600; fill:{TITLE}; }}
.pipe-sub {{ font-size:11px; fill:{FAINT}; }}
.pipe-num {{ font-size:22px; font-weight:700; fill:{INK}; }}
.pipe-track {{ fill:{CARD_2}; }}
.pipe-bar {{ fill:{LIME}; }}
.pipe-info {{ font-size:10.5px; font-weight:600; fill:{LIME}; letter-spacing:.02em; }}
.pipe-conn {{ fill:#3a3f46; }}
.pipe-src-lbl {{ font-size:11.5px; fill:{MUTED}; }}
.pipe-src-n {{ font-weight:600; fill:{FAINT}; }}
.pipe-note-t {{ font-size:11px; fill:{MUTED}; }}
.pipe-stage:hover .pipe-track {{ fill:#262a2f; }}
.pipe-stage:hover .pipe-bar {{ fill:#c8e24a; }}
.pipe-src:hover path {{ fill-opacity:.7; }}
</style>"""


def _pipeline_card(M, cur, alerts_f):
    with ui.card("ov_pipeline"):
        t, b = st.columns([4, 1.15], vertical_alignment="center")
        with t:
            ui.card_title("Current Alerts in Investigation Pipeline", right="alerts opened in period · hover a stage for detail")
        with b:
            ui.sim_button("★ Tune thresholds →", key="ov")
        pf = X.pipeline_flow(M, cur, alerts=alerts_f)
        if pf["total"] == 0:
            ui.note("No alerts in this period / filter combination.", "warn")
            return
        typ_labels = [t for t in TYPOLOGY_NAMES if pf["by_typology"].get(t, 0) > 0]
        typ_counts = [pf["by_typology"][t] for t in typ_labels]
        inject_css(PIPE_CSS)
        # st.html() sanitises inline SVG away; the markdown HTML path keeps it. The SVG is emitted as a
        # single line (no blank lines), so the markdown parser can't end the HTML block early.
        st.markdown(f'<div class="pipe-wrap">{_pipeline_svg(pf, typ_labels, typ_counts)}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------------------------------ row 2 ----
OUTCOMES = [("Escalated to SMR", "SMR", SMR_COLOR),
            ("Closed — no further action", "No action", SLATE),
            ("Closed — false positive", "False positive", "#4a5058"),
            ("Open", "Open", AMBER)]


def _groups(M, cur, dim):
    c = M["cust"]
    if dim == "State":   # biggest client book first, same order in every breakdown
        return list(c[c["onboarded"] <= cur.end]["state"].value_counts().reindex(AU_STATE_NAMES, fill_value=0)
                    .sort_values(ascending=False, kind="stable").index)
    if dim == "Typology":
        return list(TYPOLOGY_NAMES)
    if dim == "Risk Tier":
        return ["Low", "Medium", "High"]
    return list(c[c["onboarded"] <= cur.end]["channel"].value_counts().index)


def _short(dim, g):
    return {"Typology": TYP_SHORT, "Channel": CHANNEL_SHORT}.get(dim, {}).get(g, g)


def _legend(items):
    """One-line HTML legend above a chart — Plotly's horizontal legend wraps unpredictably in narrow cards."""
    st.markdown('<div class="legend-row" style="margin:0 0 2px 2px">' + "".join(
        f'<span class="legend-item"><span class="legend-sq" style="background:{c}"></span>{lab}</span>' for lab, c in items)
        + "</div>", unsafe_allow_html=True)


def _hbar(fig, n):
    fig.update_layout(**ui.base_layout(ROW2_H), barmode="stack", bargap=0.38 if n > 5 else 0.5)
    fig.update_layout(margin=dict(l=4, r=48, t=4, b=2))
    fig.update_xaxes(showgrid=True, gridcolor="#24282d", zeroline=False, tickfont=dict(size=9.5, color=FAINT), rangemode="tozero")
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=11, color="#c9ced4"), ticksuffix="  ", showgrid=False)
    return fig


def _clients_card(M, cur, dim):
    """Active client book split by AUSTRAC risk tier — who is on the books, and how risky they are."""
    with ui.card("ov_clients"):
        c = M["cust"]
        active = c[c["onboarded"] <= cur.end]
        groups = _groups(M, cur, dim)
        if dim == "Typology":
            # typology is an alert attribute: count distinct clients touched by that typology's alerts
            base, col = X.alerts_in(M, cur).drop_duplicates(["typology", "customer_id"]), "typology"
            sub = "clients with an alert of that type"
        else:
            base, col = active, X.GROUP_DIMS[dim]
            sub = "active book, by risk tier"
        ui.card_title(f"Clients by {dim}", right=sub)
        tab = base.groupby([col, "risk_tier"]).size().unstack(fill_value=0).reindex(index=groups, fill_value=0)
        tab = tab.reindex(columns=["Low", "Medium", "High"], fill_value=0)
        if tab.values.sum() == 0:
            ui.note("No clients in this view for the selected period.", "warn")
            return
        ylab = [_short(dim, g) for g in tab.index]
        _legend([(f"{t} risk", TIER_COLORS[t]) for t in ["Low", "Medium", "High"] if tab[t].sum()])
        fig = go.Figure()
        for tier in ["Low", "Medium", "High"]:
            if tab[tier].sum() == 0:
                continue
            fig.add_bar(y=ylab, x=tab[tier], orientation="h", name=f"{tier} risk",
                        marker=dict(color=TIER_COLORS[tier], line=dict(width=0)),
                        hovertemplate="%{y} · " + tier + " risk: %{x}<extra></extra>")
        tot = tab.sum(axis=1)
        fig.add_scatter(y=ylab, x=tot, mode="text", text=[f"  {int(v)}" for v in tot], textposition="middle right",
                        textfont=dict(size=10.5, color=INK), showlegend=False, hoverinfo="skip", cliponaxis=False)
        ui.show(_hbar(fig, len(tab)), key="ov_clients_fig")


def _outcomes_card(M, cur, dim, alerts_f):
    """Where each group's alerts ended up — how much turned into an SMR versus was cleared."""
    with ui.card("ov_outcomes"):
        ui.card_title(f"Alert outcomes by {dim}", right="SMR rate at bar end")
        col = X.GROUP_DIMS[dim]
        groups = _groups(M, cur, dim)
        a = alerts_f.copy()
        a["outcome"] = a["disposition"].replace({"Under investigation": "Open"})
        tab = a.groupby([col, "outcome"]).size().unstack(fill_value=0).reindex(index=groups, fill_value=0)
        tab = tab.reindex(columns=[o for o, *_ in OUTCOMES], fill_value=0)
        if tab.values.sum() == 0:
            ui.note("No alerts for this period / filter combination.", "warn")
            return
        ylab = [_short(dim, g) for g in tab.index]
        _legend([(label, color) for key, label, color in OUTCOMES if tab[key].sum()])
        fig = go.Figure()
        for key, label, color in OUTCOMES:
            if tab[key].sum() == 0:
                continue
            fig.add_bar(y=ylab, x=tab[key], orientation="h", name=label,
                        marker=dict(color=color, line=dict(width=0)),
                        hovertemplate="%{y} · " + label + ": %{x}<extra></extra>")
        tot = tab.sum(axis=1)
        rate = [f"  {s / t:.0%}" if t else "" for s, t in zip(tab["Escalated to SMR"], tot)]
        fig.add_scatter(y=ylab, x=tot, mode="text", text=rate, textposition="middle right",
                        textfont=dict(size=10.5, color=LIME), showlegend=False, hoverinfo="skip", cliponaxis=False)
        ui.show(_hbar(fig, len(tab)), key="ov_outcomes_fig")


def _table_card(M, cur, dim, alerts_f):
    with ui.card("ov_table"):
        ui.card_title("Compliance Metrics by " + dim, right=cur.short())
        df = X.group_metrics_table(M, cur, dim, alerts_filtered=alerts_f)
        if len(df):          # same row order as the two breakdown charts
            body = df[df["group"] != "Total"].set_index("group").reindex(_groups(M, cur, dim)).reset_index()
            df = pd.concat([body, df[df["group"] == "Total"]], ignore_index=True)
        df["group"] = [_short(dim, g) for g in df["group"]]
        show = df.rename(columns={"group": dim, "customers": "Clients", "alerts": "Alerts", "smrs": "SMRs",
                                  "smr_rate": "SMR %", "closed": "Closed", "closed_rate": "Closed %"})
        ui.render_html_table(show, num_cols=("Clients", "Alerts", "SMRs", "SMR %", "Closed", "Closed %"),
                             total_row=True, fmt={"SMR %": ui.fmt_pct, "Closed %": ui.fmt_pct}, compact=True)


# ------------------------------------------------------------------------------------------ page ----
def render(M, cur, cmp):
    dim = _header_bar(cur, cmp)
    alerts_f = _filtered_alerts(M, cur)

    rail_col, pipe_col = st.columns([0.92, 5.3])
    with rail_col:
        _kpi_rail(M, cur, cmp)
    with pipe_col:
        _pipeline_card(M, cur, alerts_f)

    c1, c2, c3 = st.columns([1, 1, 1.22])
    with c1:
        _clients_card(M, cur, dim)
    with c2:
        _outcomes_card(M, cur, dim, alerts_f)
    with c3:
        _table_card(M, cur, dim, alerts_f)
