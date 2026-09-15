import streamlit as st
import pandas as pd

from db_utils import load_all
from theme import inject_css, page_header, section_title, risk_pill, grouped_bar3d_chart, RISK_COLOR_MAP

st.set_page_config(page_title="Business KYC | AML Suite", layout="wide")
inject_css()
page_header("Business Customer KYC", "Corporate due diligence register and re-verification tracking.", "BUSINESS KYC")

data = load_all()
businesses, ubo = data["businesses"], data["ubo"]

with st.sidebar:
    st.subheader("Filters")
    countries = st.multiselect("Incorporation country", sorted(businesses["incorporation_country"].unique()))
    structures = st.multiselect("Structure type", sorted(businesses["structure_type"].unique()))
    risk_filter = st.multiselect("Risk rating", ["Low", "Medium", "High", "Critical"])

df = businesses.copy()
if countries:
    df = df[df["incorporation_country"].isin(countries)]
if structures:
    df = df[df["structure_type"].isin(structures)]
if risk_filter:
    df = df[df["risk_rating"].isin(risk_filter)]

today = pd.Timestamp.today().normalize()
df["age_days"] = (today - df["incorporation_date"]).dt.days
df["due_for_review"] = df["risk_score"] >= 60  # simplified: high-risk entities need annual EDD refresh

c1, c2, c3, c4 = st.columns(4)
c1.metric("Business Customers", f"{len(df):,}")
c2.metric("Newly Incorporated (<1yr)", int((df["age_days"] < 365).sum()))
c3.metric("Due for EDD Refresh", int(df["due_for_review"].sum()))
c4.metric("Foreign Incorporated", int((df["incorporation_country"] != "Australia").sum()))

section_title("Risk Rating by Structure Type")
st.caption("Drag to rotate, scroll to zoom, hover any bar for its exact count.")
if df.empty:
    st.info("No entities match the current filters.")
else:
    structures = sorted(df["structure_type"].unique())
    pivot = df.groupby(["structure_type", "risk_rating"]).size().unstack(fill_value=0)
    for lvl in ["Low", "Medium", "High", "Critical"]:
        if lvl not in pivot.columns:
            pivot[lvl] = 0
    pivot = pivot.reindex(structures).fillna(0)

    fig = grouped_bar3d_chart(
        categories=structures,
        series={lvl: pivot[lvl].tolist() for lvl in ["Low", "Medium", "High", "Critical"]},
        colors=RISK_COLOR_MAP,
        z_title="Entities",
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

section_title("KYC Register")
show = df.sort_values("risk_score", ascending=False).copy()
show["Risk"] = show["risk_rating"].apply(risk_pill)
show["EDD Refresh"] = show["due_for_review"].map({True: '<span class="pill pill-high">Due</span>', False: '<span class="pill pill-low">Current</span>'})
disp = show[["business_id", "legal_name", "abn", "industry", "incorporation_country", "structure_type",
             "incorporation_date", "Risk", "EDD Refresh"]]
disp = disp.rename(columns={
    "business_id": "ID", "legal_name": "Legal Name", "abn": "ABN", "industry": "Industry",
    "incorporation_country": "Country", "structure_type": "Structure", "incorporation_date": "Incorporated",
})
disp["Incorporated"] = disp["Incorporated"].dt.strftime("%d %b %Y")
st.write(disp.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()
section_title("Entity Profile Lookup")
options = {f"{r.business_id} - {r.legal_name}": r.business_id for r in df.itertuples()}
if options:
    choice = st.selectbox("Select an entity", list(options.keys()))
    bid = options[choice]
    biz = businesses[businesses["business_id"] == bid].iloc[0]
    owners = ubo[ubo["business_id"] == bid]

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
**Legal name:** {biz['legal_name']}
**ABN:** {biz['abn']}
**Industry:** {biz['industry']}
**Structure:** {biz['structure_type']}
**Incorporation country:** {biz['incorporation_country']}
**Incorporation date:** {biz['incorporation_date'].strftime('%d %B %Y')}
**Risk rating:** {biz['risk_rating']} ({biz['risk_score']}/100)
        """)
    with col2:
        st.markdown("**Beneficial Owners**")
        st.dataframe(
            owners[["owner_name", "owner_type", "ownership_pct", "is_pep"]].rename(
                columns={"owner_name": "Owner", "owner_type": "Type", "ownership_pct": "Ownership %", "is_pep": "PEP"}
            ),
            use_container_width=True, hide_index=True,
        )
    st.caption("Full ownership graph available on the **UBO Network** page.")
