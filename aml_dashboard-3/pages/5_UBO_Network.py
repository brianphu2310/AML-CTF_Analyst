import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill

st.set_page_config(page_title="UBO Network | AML Suite", page_icon="🕸️", layout="wide")
inject_css()
page_header("Ultimate Beneficial Ownership Network", "Ownership structure mapping and PEP exposure across entities.", "UBO")

data = load_all()
businesses, ubo = data["businesses"], data["ubo"]

with st.sidebar:
    st.subheader("Filters")
    risk_filter = st.multiselect("Business risk rating", ["Low", "Medium", "High", "Critical"])
    pep_only = st.checkbox("Show only structures with a PEP owner")
    search = st.text_input("Search business name")

biz = businesses.copy()
if risk_filter:
    biz = biz[biz["risk_rating"].isin(risk_filter)]
if search:
    biz = biz[biz["legal_name"].str.contains(search, case=False)]

pep_business_ids = set(ubo[ubo["is_pep"]]["business_id"])
if pep_only:
    biz = biz[biz["business_id"].isin(pep_business_ids)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Entities in Register", f"{len(biz):,}")
c2.metric("With PEP Owner", int(biz["business_id"].isin(pep_business_ids).sum()))
c3.metric("Critical/High Risk", int(biz["risk_rating"].isin(["Critical", "High"]).sum()))
c4.metric("Corporate Owners", int((ubo["owner_type"] == "Corporate").sum()))

section_title("Ownership Structure Register")
show = biz.sort_values("risk_score", ascending=False).copy()
show["Risk"] = show["risk_rating"].apply(risk_pill)
disp = show[["business_id", "legal_name", "abn", "industry", "incorporation_country", "structure_type", "Risk"]]
disp = disp.rename(columns={
    "business_id": "ID", "legal_name": "Legal Name", "abn": "ABN", "industry": "Industry",
    "incorporation_country": "Country", "structure_type": "Structure",
})
st.write(disp.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()
section_title("Beneficial Ownership Graph")
if biz.empty:
    st.warning("No entities match the current filters.")
else:
    options = {f"{r.business_id} - {r.legal_name}": r.business_id for r in biz.itertuples()}
    choice = st.selectbox("Select an entity to visualise", list(options.keys()))
    bid = options[choice]
    owners = ubo[ubo["business_id"] == bid]
    biz_row = businesses[businesses["business_id"] == bid].iloc[0]

    G = nx.Graph()
    G.add_node(bid, label=biz_row["legal_name"], kind="business")
    for _, o in owners.iterrows():
        node_id = f"{o['ubo_id']}"
        G.add_node(node_id, label=o["owner_name"], kind="pep" if o["is_pep"] else o["owner_type"].lower())
        G.add_edge(bid, node_id, weight=o["ownership_pct"])

    pos = nx.spring_layout(G, seed=42, k=0.9)

    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color="#374151"), mode="lines", hoverinfo="none")

    color_map = {"business": "#2DD4BF", "individual": "#60A5FA", "corporate": "#FBBF24", "pep": "#F87171"}
    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for n, attrs in G.nodes(data=True):
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        node_text.append(attrs["label"])
        node_color.append(color_map.get(attrs["kind"], "#94A3B8"))
        node_size.append(34 if attrs["kind"] == "business" else 24)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=node_text, textposition="bottom center",
        textfont=dict(size=11, color="#E5E7EB"),
        marker=dict(size=node_size, color=node_color, line=dict(width=1.5, color="#0B1120")),
        hoverinfo="text",
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False, template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=460,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    st.plotly_chart(fig, use_container_width=True)

    legend_cols = st.columns(4)
    legend_cols[0].markdown("🟢 Reporting entity")
    legend_cols[1].markdown("🔵 Individual owner")
    legend_cols[2].markdown("🟡 Corporate owner")
    legend_cols[3].markdown("🔴 PEP-linked owner")

    section_title("Ownership Detail")
    owner_disp = owners[["ubo_id", "owner_name", "owner_type", "ownership_pct", "is_pep", "nationality"]].copy()
    owner_disp["is_pep"] = owner_disp["is_pep"].map({True: "⚠️ Yes", False: "No"})
    owner_disp = owner_disp.rename(columns={
        "ubo_id": "UBO ID", "owner_name": "Owner", "owner_type": "Type",
        "ownership_pct": "Ownership %", "is_pep": "PEP", "nationality": "Nationality",
    })
    st.dataframe(owner_disp, use_container_width=True, hide_index=True)

    if owners["is_pep"].any():
        st.error(
            "One or more beneficial owners of this entity are flagged as a Politically Exposed Person. "
            "Enhanced Due Diligence (EDD) and senior management sign-off are required.",
            icon="🚨",
        )
