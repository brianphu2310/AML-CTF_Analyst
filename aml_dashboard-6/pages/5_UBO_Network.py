import streamlit as st
import pandas as pd

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill, network3d_chart, TEAL_DARK, TEAL_MID, BROWN_MID, HIGH

st.set_page_config(page_title="UBO Network | AML Suite", layout="wide")
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

    st.caption("Drag to rotate, scroll to zoom. Height reflects ownership percentage.")
    color_map = {"business": TEAL_DARK, "individual": TEAL_MID, "corporate": BROWN_MID, "pep": HIGH}
    owner_nodes = [
        {
            "label": o["owner_name"],
            "kind": "pep" if o["is_pep"] else o["owner_type"].lower(),
            "weight": o["ownership_pct"],
        }
        for _, o in owners.iterrows()
    ]
    fig = network3d_chart(
        center_label=biz_row["legal_name"], center_kind="business",
        nodes=owner_nodes, color_map=color_map, height=460,
    )
    st.plotly_chart(fig, use_container_width=True)

    legend_cols = st.columns(4)
    legend_items = [
        (color_map["business"], "Reporting entity"),
        (color_map["individual"], "Individual owner"),
        (color_map["corporate"], "Corporate owner"),
        (color_map["pep"], "PEP-linked owner"),
    ]
    for col, (color, label) in zip(legend_cols, legend_items):
        col.markdown(
            f'<span style="display:inline-block;width:10px;height:10px;border-radius:2px;'
            f'background:{color};margin-right:6px;"></span>{label}',
            unsafe_allow_html=True,
        )

    section_title("Ownership Detail")
    owner_disp = owners[["ubo_id", "owner_name", "owner_type", "ownership_pct", "is_pep", "nationality"]].copy()
    owner_disp["is_pep"] = owner_disp["is_pep"].map({True: "Yes", False: "No"})
    owner_disp = owner_disp.rename(columns={
        "ubo_id": "UBO ID", "owner_name": "Owner", "owner_type": "Type",
        "ownership_pct": "Ownership %", "is_pep": "PEP", "nationality": "Nationality",
    })
    st.dataframe(owner_disp, use_container_width=True, hide_index=True)

    if owners["is_pep"].any():
        st.error(
            "One or more beneficial owners of this entity are flagged as a Politically Exposed Person. "
            "Enhanced Due Diligence (EDD) and senior management sign-off are required."
        )
