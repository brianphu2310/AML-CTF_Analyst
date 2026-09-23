"""Reusable UI pieces: formatters, KPI cards, cards/containers, chart helpers, tables."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .theme import (LIME, LIME_TINT, INK, MUTED, FAINT, GREEN, RED, AMBER, CARD_2, GRID, GREEN_TINT, RED_TINT, AMBER_TINT)

# ------------------------------------------------------------------ format ----
def fmt_money(v, dec=None, sign=False):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    s = "-" if v < 0 else ("+" if sign and v > 0 else "")
    a = abs(v)
    if a >= 1_000_000:
        return f"{s}${a / 1_000_000:.{2 if dec is None else dec}f}M"
    if a >= 10_000:
        return f"{s}${a / 1_000:.{0 if dec is None else dec}f}K"
    if a >= 1_000:
        return f"{s}${a / 1_000:.{1 if dec is None else dec}f}K"
    return f"{s}${a:,.{0 if dec is None else dec}f}"


def fmt_num(v, dec=0):
    return "—" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:,.{dec}f}"


def fmt_pct(v, dec=1, sign=False):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"{'+' if sign and v > 0 else ''}{v * 100:.{dec}f}%"


def pp(v, dec=1):
    """Percentage-point difference."""
    return "—" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{'+' if v > 0 else ''}{v * 100:.{dec}f} pp"


# ------------------------------------------------------------- html bits ----
def sparkline_svg(values, color=LIME, width=60, height=28):
    v = np.asarray(values, dtype=float)
    if len(v) < 2 or np.all(np.isnan(v)):
        return ""
    lo, hi = np.nanmin(v), np.nanmax(v)
    span = (hi - lo) or 1.0
    step = width / (len(v) - 1)
    pts = " ".join(f"{i * step:.1f},{height - ((x - lo) / span) * (height - 4) - 2:.1f}" for i, x in enumerate(v))
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"><polyline points="{pts}" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _arrow(up, color):
    d = "M6 10V2M2.5 5.5 6 2l3.5 3.5" if up else "M6 2v8M2.5 6.5 6 10l3.5-3.5"
    return (f'<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="{d}" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def delta_html(d, up_good=True, label="vs prior", kind="pct"):
    """d = relative change (or pp change when kind='pp'); None → n/a."""
    if d is None or (isinstance(d, float) and np.isnan(d)):
        return f'<span class="vs" style="color:{FAINT}">n/a</span>'
    if abs(d) < 5e-4:
        return f'<span style="display:inline-flex;align-items:center;gap:4px"><span class="pct" style="color:{FAINT}">0.0{"%" if kind == "pct" else " pp"}</span><span class="vs">{label}</span></span>'
    good = (d >= 0) == up_good
    color = GREEN if good else RED
    txt = pp(d) if kind == "pp" else f"{'+' if d > 0 else ''}{d * 100:.1f}%"
    return (f'<span style="display:inline-flex;align-items:center;gap:4px">{_arrow(d >= 0, color)}'
            f'<span class="pct" style="color:{color}">{txt}</span><span class="vs">{label}</span></span>')


def kpi_html(label, value, d=None, up_good=True, label_cmp="vs prior", kind="pct", spark=None, sub=None, color=INK, accent=None, min_h=0):
    css = []
    if accent:
        css.append(f"--acc:{accent}")
    if min_h:
        css.append(f"min-height:{min_h}px")
    style = f' style="{";".join(css)}"' if css else ""
    cls = "kpi-card kpi-accent" if accent else "kpi-card"
    sp = sparkline_svg(spark, accent or LIME) if spark is not None else ""
    trend = f'<div class="kpi-trend">{delta_html(d, up_good, label_cmp, kind)}</div>' if label_cmp is not None else ""
    subh = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (f'<div class="{cls}"{style}><div class="kpi-label">{label}</div><div class="kpi-bottom"><div>'
            f'<div class="kpi-value" style="color:{color}">{value}</div>{trend}{subh}</div>{sp}</div></div>')


def kpi_row(items, spacer_after=0, min_h=88):
    for col, it in zip(st.columns(len(items)), items):
        with col:
            st.markdown(kpi_html(**{"min_h": min_h, **it}), unsafe_allow_html=True)
    if spacer_after:
        spacer(spacer_after)


def pill(text, kind="neutral"):
    fg, bg = {"good": (GREEN, GREEN_TINT), "bad": (RED, RED_TINT), "warn": (AMBER, AMBER_TINT), "info": (LIME, LIME_TINT),
              "neutral": (MUTED, CARD_2)}[kind]
    return f'<span class="pill" style="background:{bg};color:{fg}">{text}</span>'


STATUS_KIND = {"Open": "warn", "Under investigation": "info", "Escalated to SMR": "bad", "Closed — false positive": "neutral",
               "Closed — no further action": "good", "Submitted": "info", "Acknowledged": "good", "Draft": "warn",
               "Low": "good", "Medium": "warn", "High": "bad"}


def status_pill(s):
    return pill(s, STATUS_KIND.get(s, "neutral"))


def note(text, kind=""):
    st.markdown(f'<div class="note {kind}">{text}</div>', unsafe_allow_html=True)


def spacer(h=8):
    st.markdown(f'<div style="height:{h}px"></div>', unsafe_allow_html=True)


def page_header(title, sub=None, tag=None):
    tag_h = f'<span class="page-tag">{tag}</span>' if tag else ""
    sub_h = f'<div class="page-sub">{sub}</div>' if sub else ""
    st.markdown(f'<div class="page-head"><div><div class="page-title">{title}</div>{sub_h}</div>{tag_h}</div>', unsafe_allow_html=True)


def card_title(text, right=None):
    r = f'<span style="font-size:10.5px;color:{FAINT};font-weight:500">{right}</span>' if right else ""
    st.markdown(f'<div class="card-title" style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:2px">'
                f'<span>{text}</span>{r}</div>', unsafe_allow_html=True)


_seq = [0]


def card(key=None):
    _seq[0] += 1
    return st.container(border=True, key=f"cardblock_{key or 'c'}_{_seq[0]}")


def reset_card_counter():
    _seq[0] = 0


# ------------------------------------------------------------------ charts ---
def base_layout(h, legend=False, **kw):
    lay = dict(margin=dict(l=8, r=8, t=6, b=4), height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
               showlegend=legend, font=dict(family="Inter, sans-serif", color=MUTED, size=10),
               hoverlabel=dict(font_size=11, bgcolor=CARD_2, bordercolor=LIME, font_color=INK))
    if legend:
        lay["legend"] = dict(orientation="h", y=1.14, x=0, font=dict(size=10), bgcolor="rgba(0,0,0,0)")
    lay.update(kw)
    return lay


def style_axes(fig, y_fmt=None, grid=True, x_grid=False):
    fig.update_xaxes(showgrid=x_grid, gridcolor=GRID, tickfont=dict(size=9), zeroline=False, linecolor=GRID)
    fig.update_yaxes(showgrid=grid, gridcolor=GRID, tickfont=dict(size=9), zeroline=False, tickformat=y_fmt, linecolor=GRID)
    return fig


def show(fig, key=None, **kw):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False}, key=key, **kw)


def donut(labels, values, colors, h=150, center=None, key=None):
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.68, marker=dict(colors=colors, line=dict(color="#15171a", width=2)),
                           textinfo="none", sort=False, hovertemplate="%{label}: %{percent}<extra></extra>"))
    fig.update_layout(**base_layout(h, margin=dict(l=2, r=2, t=2, b=2)))
    if center:
        fig.add_annotation(text=center, x=0.5, y=0.5, showarrow=False, align="center", font=dict(family="Inter, sans-serif", color=INK))
    show(fig, key=key)


# ------------------------------------------------------------------ tables ---
def csv_button(df, name, key):
    st.download_button("⬇ CSV", df.to_csv(index=False).encode("utf-8"), file_name=f"{name}.csv", mime="text/csv", key=f"dl_{key}")


def render_html_table(df, num_cols=(), total_row=False, sub_rows=(), fmt=None, compact=False):
    fmt = fmt or {}
    head = "".join(f'<th class="{"num" if c in num_cols else ""}">{c}</th>' for c in df.columns)
    body = ""
    for i, (_, r) in enumerate(df.iterrows()):
        cls = "total" if total_row and i == len(df) - 1 else ("sub" if i in sub_rows else "")
        tds = "".join(f'<td class="{"num" if c in num_cols else ""}">{fmt[c](r[c]) if c in fmt else r[c]}</td>' for c in df.columns)
        body += f'<tr class="{cls}">{tds}</tr>'
    cls = "simple compact" if compact else "simple"
    st.markdown(f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>', unsafe_allow_html=True)


def period_tag(cur, cmp):
    from .period import has_data
    tag = f"{cur.label} · {cur.short()}"
    if cmp is None:
        return tag
    return tag + (f"  vs  {cmp.short()}" if has_data(cmp) else "  · no comparison data before Jul 2023")


def cmp_label(cmp):
    if cmp is None:
        return None
    return "vs LY" if "last year" in cmp.label else "vs prior"


def restore_state(defaults, prefix="_keep_"):
    """Streamlit forgets a widget's value when the page containing it is not drawn. Call this before drawing the widgets to bring back
    the last value (or the default on first use)."""
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = st.session_state.get(prefix + k, v)


def keep_state(keys, prefix="_keep_"):
    """Call after the widgets are drawn: remember their current values so restore_state can bring them back."""
    for k in keys:
        if k in st.session_state:
            st.session_state[prefix + k] = st.session_state[k]


def _open_simulator(target_kind=None, preset=None):
    from . import simulate as S

    def go():
        ss = st.session_state
        ss["view_name"] = "Simulator"
        if target_kind or preset:          # goals and presets live in the tuning mode
            ss["sim_mode"] = ss["_keep_sim_mode"] = "Alert-model tuning"
        if target_kind:
            ss["sim_target_kind"] = target_kind
        if preset:
            for k, v in S.preset_state(preset).items():
                ss[k] = v
    return go


def sim_cta(text, target_kind=None, preset=None, key="cta"):
    """A call-to-action line that opens the Simulator (optionally pre-loaded with a goal or a preset)."""
    c1, c2 = st.columns([5, 1.6], vertical_alignment="center")
    c1.markdown(f'<div class="sim-cta"><span class="sim-cta-star">★</span> {text}</div>', unsafe_allow_html=True)
    c2.button("Open the Simulator →", key=f"act_cta_{key}", on_click=_open_simulator(target_kind, preset), width="stretch")


def sim_button(label, key, target_kind=None, preset=None):
    """Compact one-button version of sim_cta, for tight layouts (e.g. inside a card's title row)."""
    st.button(label, key=f"act_cta_{key}", on_click=_open_simulator(target_kind, preset), width="stretch")


# ------------------------------------------------------------- sidebar radial ---
def radial_rings_svg(items, center_value, center_label, size=176):
    """Concentric radial-bar rings (outermost = first item): each ring's arc is that item's share of the
    total, starting at 12 o'clock and running clockwise over a dark full-circle track.
    items = [(label, value, colour), ...]. Returns one-line SVG (safe for st.markdown)."""
    from .theme import CARD_2 as _TRACK, LIME as _LIME, FAINT as _FAINT
    import math
    total = sum(v for _, v, _ in items) or 1
    c = size / 2
    stroke, step = 11, 16
    r0 = c - stroke / 2 - 2
    parts = [f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="{center_value} {center_label}">']
    for i, (label, v, col) in enumerate(items):
        r = r0 - i * step
        circ = 2 * math.pi * r
        share = v / total
        parts.append(f'<circle cx="{c}" cy="{c}" r="{r:.1f}" fill="none" stroke="{_TRACK}" stroke-width="{stroke}"/>')
        if v:
            parts.append(f'<circle cx="{c}" cy="{c}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="{stroke}" '
                         f'stroke-linecap="round" stroke-dasharray="{max(share * circ - 1, 0.1):.1f} {circ:.1f}" '
                         f'transform="rotate(-90 {c} {c})"><title>{label}: {v} ({share:.0%})</title></circle>')
    parts.append(f'<text x="{c}" y="{c + 4}" text-anchor="middle" font-family="Inter, sans-serif" font-size="24" '
                 f'font-weight="700" fill="{_LIME}">{center_value}</text>'
                 f'<text x="{c}" y="{c + 19}" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" '
                 f'fill="{_FAINT}">{center_label}</text></svg>')
    return "".join(parts)


def combo_bars_line_svg(labels, bars, line, bar_name, line_name, width=176, height=112):
    """Mini combo chart for the sidebar: monthly bars (lime) with a line overlay on its own scale (sky),
    in the spirit of the reference report's spend/ROAS panel. One-line SVG, safe for st.markdown."""
    from .theme import LIME as _L, SKY as _S, FAINT as _F, GRID as _G
    n = len(bars)
    top, bottom, left, right = 14, height - 14, 2, width - 2
    ph = bottom - top
    step = (right - left) / max(n, 1)
    bmax, lmax = max(max(bars), 1), max(max(line), 1)
    parts = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="{bar_name} and {line_name}, last {n} months">',
             f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{_G}" stroke-width="1"/>']
    pts = []
    for i, (lab, b, l) in enumerate(zip(labels, bars, line)):
        x = left + i * step
        h = ph * b / bmax * 0.92
        parts.append(f'<rect x="{x + step * 0.18:.1f}" y="{bottom - h:.1f}" width="{step * 0.64:.1f}" height="{h:.1f}" rx="1" '
                     f'fill="{_L}" fill-opacity="{0.55 if i < n - 1 else 0.95}"><title>{lab}: {b} {bar_name.lower()}, {l} {line_name}</title></rect>')
        pts.append((x + step / 2, bottom - ph * l / lmax * 0.92))
        parts.append(f'<text x="{x + step / 2:.1f}" y="{height - 3}" text-anchor="middle" font-size="7.5" fill="{_F}" '
                     f'font-family="Inter,sans-serif">{lab[0]}</text>')
    parts.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{_S}" stroke-width="1.6" '
                 f'stroke-linejoin="round"/>')
    parts += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{_S}"/>' for x, y in pts]
    lx, ly = pts[-1]
    parts.append(f'<text x="{right}" y="{top - 4}" text-anchor="end" font-size="8.5" font-family="Inter,sans-serif" fill="{_L}">'
                 f'{bars[-1]} alerts <tspan fill="{_S}">· {line[-1]} SMRs</tspan></text></svg>')
    return "".join(parts)


def meter_html(label, value, target=None, good_high=True, fmt="{:.0%}"):
    """A thin labelled progress meter (0-1) with an optional target tick."""
    from .theme import LIME as _L, AMBER as _A, CARD_2 as _T
    ok = (value >= target) if (target is not None and good_high) else ((value <= target) if target is not None else True)
    col = (_L if ok else _A) if target is not None else "#8cc8da"
    tick = (f'<span style="position:absolute;left:{target * 100:.1f}%;top:-3px;width:2px;height:12px;background:#eef0f2;border-radius:1px"></span>'
            if target is not None else "")
    tgt = f' <span style="color:#6f7780">/ {fmt.format(target)}</span>' if target is not None else ""
    return (f'<div style="margin:7px 0 2px;font-size:10.5px;color:#a4abb4;display:flex;justify-content:space-between">'
            f'<span>{label}</span><span><b style="color:{col}">{fmt.format(value)}</b>{tgt}</span></div>'
            f'<div style="position:relative;height:6px;border-radius:3px;background:{_T}">'
            f'<div style="width:{min(max(value, 0), 1) * 100:.1f}%;height:100%;border-radius:3px;background:{col}"></div>{tick}</div>')
