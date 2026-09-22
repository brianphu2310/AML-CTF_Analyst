"""UBO Network — beneficial-ownership structure for a handful of named entities/matters."""
import plotly.graph_objects as go
import streamlit as st

from core import ui
from core.ref import UBO_ENTITIES
from core.theme import LIME, TEAL, INK, CARD, MUTED, FAINT


def _build_sunburst():
    """Sunburst nodes/edges. Each named entity is its own root wedge (parent ''), so no dummy total node is
    needed — Plotly's Sunburst supports several independent roots sharing an empty parent. Wedges are sized
    uniformly (equal weight per node) — an ownership chain's *depth* is what matters for a red flag, not a
    wedge's angular size — and the actual ownership % is carried in the hover text instead."""
    ids, labels, parents, custom, colors = [], [], [], [], []
    seen = set()

    def add(entity, parent_id, pct, top):
        node_id = f"{top}::{entity}" if parent_id else entity
        if node_id in seen:
            return
        seen.add(node_id)
        is_entity = entity in UBO_ENTITIES
        ids.append(node_id); labels.append(entity); parents.append(parent_id)
        custom.append(f"{pct:.0f}% ownership" if parent_id else "Reviewed entity")
        colors.append(LIME if is_entity else TEAL)
        if is_entity:
            for owner, opct in UBO_ENTITIES[entity]:
                add(owner, node_id, opct, top)

    for entity in UBO_ENTITIES:
        add(entity, "", 100.0, entity)
    values = [1] * len(ids)
    return ids, labels, parents, values, colors, custom


def render(M, cur, cmp):
    ui.page_header("UBO Network", "Beneficial-ownership structure for the firm's higher-risk trust and structuring matters.", ui.period_tag(cur, cmp))

    ui.note("Beneficial-ownership chains are the core evidence base for a Suspicious Matter Report on structuring or trade-based ML "
            "typologies — an unexplained layer, or an owner who is themself an unverified entity, is a red flag under AUSTRAC guidance.")

    c1, c2 = st.columns([1.3, 1.0])
    with c1:
        with ui.card("ubo_sun"):
            ui.card_title("Ownership Layers", right="lime = entity · teal = individual/nominee")
            ids, labels, parents, values, colors, custom = _build_sunburst()
            f = go.Figure(go.Sunburst(ids=ids, labels=labels, parents=parents, values=values, marker=dict(colors=colors, line=dict(color=CARD, width=1.5)),
                                      insidetextfont=dict(color=["#0b0c0e" if c == LIME else "#eef0f2" for c in colors]),
                                      customdata=custom, hovertemplate="%{label}<br>%{customdata}<extra></extra>"))
            f.update_layout(margin=dict(l=4, r=4, t=4, b=4), height=460, paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=11, color=INK))
            ui.show(f, key="ubo_sunburst")
    with c2:
        with ui.card("ubo_flags"):
            ui.card_title("Structures Flagged for Review")
            flags = [
                ("Kalvara Ventures Pty Ltd", "Two-layer ownership through a Tier 3 (FATF-monitored) trust and a foreign holding company — source of funds not yet verified.", "bad"),
                ("Rennport Maritime Holdings", "Beneficial owner resident in a Tier 3 jurisdiction; matter linked to a Trade-based ML indicator alert.", "bad"),
                ("Meridian Pacific Trust", "Ownership traces back to a Tier 2 nominee entity — periodic review is on schedule.", "warn"),
                ("Singapore Trading Group", "Individually-verified beneficial owners, low-risk foreign link — no action required.", "good"),
            ]
            for name, text, kind in flags:
                st.markdown(f'<div class="note {kind}"><b>{name}</b><br>{text}</div>', unsafe_allow_html=True)

    ui.spacer(6)
    with ui.card("ubo_table"):
        ui.card_title("Ownership Register")
        rows = []
        for entity, owners in UBO_ENTITIES.items():
            for owner, pct in owners:
                rows.append(dict(Entity=entity, Owner=owner, Ownership=f"{pct}%", Layered="Yes" if owner in UBO_ENTITIES else "No"))
        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df, width="stretch", hide_index=True, height=240)
        ui.csv_button(df, "ubo_register", "ubo_tbl")
