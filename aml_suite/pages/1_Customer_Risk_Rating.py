import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import theme, data_access as da

st.set_page_config(page_title="Customer Risk Rating", layout="wide")
theme.inject_css()
theme.page_header("Customer Risk Rating", "ML/TF risk assessment \u2014 AUSTRAC four-factor model")

customers = da.load_customers()

theme.methodology_note(
    "<b>Methodology:</b> each customer is scored 0/1/2 across four AUSTRAC risk-factor "
    "categories \u2014 customer type, jurisdiction, service/product, delivery channel. "
    "<b>Any single factor scoring 2 (high) sets the overall rating to High</b>, regardless of "
    "the other three \u2014 a single bad factor is not averaged away by three good ones. "
    "Otherwise, the rating is Medium if the summed score reaches the medium threshold, else Low. "
    "The rating then drives Enhanced Due Diligence requirements and ongoing review frequency."
)

# ------------------------------------------------------------ FILTER ROW
c1, c2, c3 = st.columns(3)
with c1:
    rating_filter = st.multiselect("Risk rating", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])
with c2:
    structure_filter = st.multiselect(
        "Customer structure", sorted(customers["structure"].unique().tolist()), default=[]
    )
with c3:
    edd_only = st.checkbox("Enhanced Due Diligence required only", value=False)

filtered = customers[customers["risk_rating"].isin(rating_filter)]
if structure_filter:
    filtered = filtered[filtered["structure"].isin(structure_filter)]
if edd_only:
    filtered = filtered[filtered["edd_required"]]

c1, c2, c3, c4 = st.columns(4)
with c1:
    theme.kpi_card("Customers shown", f"{len(filtered):,}")
with c2:
    theme.kpi_card("High risk", f"{(filtered.risk_rating=='High').sum()}", risk_class="risk-high")
with c3:
    theme.kpi_card("EDD required", f"{filtered['edd_required'].sum()}", "Enhanced due diligence triggered")
with c4:
    theme.kpi_card("Avg. risk score", f"{filtered['risk_score'].mean():.1f}" if len(filtered) else "\u2014")

col1, col2 = st.columns([1, 1])
with col1:
    theme.section_title("Rating distribution by customer structure")
    pivot = filtered.groupby(["structure", "risk_rating"]).size().unstack(fill_value=0)
    for r in ["Low", "Medium", "High"]:
        if r not in pivot.columns:
            pivot[r] = 0
    pivot = pivot[["Low", "Medium", "High"]]
    fig = theme.grouped_bar_chart(
        pivot.index, {r: pivot[r].values for r in ["Low", "Medium", "High"]},
        colors={r: theme.RISK_COLOR_MAP[r] for r in ["Low", "Medium", "High"]},
        horizontal=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col2:
    theme.section_title("Rating distribution by jurisdiction risk")
    jur_pivot = filtered.groupby(["jurisdiction_score", "risk_rating"]).size().unstack(fill_value=0)
    label_map = {0: "Low-risk jurisdiction", 1: "Medium-risk jurisdiction", 2: "High-risk jurisdiction"}
    jur_pivot.index = [label_map.get(i, i) for i in jur_pivot.index]
    for r in ["Low", "Medium", "High"]:
        if r not in jur_pivot.columns:
            jur_pivot[r] = 0
    fig = theme.grouped_bar_chart(
        jur_pivot.index, {r: jur_pivot[r].values for r in ["Low", "Medium", "High"]},
        colors={r: theme.RISK_COLOR_MAP[r] for r in ["Low", "Medium", "High"]},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")
theme.section_title("Client register")

display_cols = [
    "customer_id", "display_name", "structure", "jurisdiction", "pep_level",
    "primary_matter_type", "delivery_channel", "risk_rating", "risk_score",
    "edd_required", "review_cadence",
]
view = filtered[display_cols].copy().sort_values("risk_score", ascending=False)
view["risk_rating"] = view["risk_rating"].apply(theme.risk_pill)
view["edd_required"] = view["edd_required"].map({True: "Yes", False: "No"})
view.columns = ["Customer ID", "Name", "Structure", "Jurisdiction", "PEP status", "Primary matter",
                "Channel", "Risk rating", "Score", "EDD required", "Review cadence"]
st.markdown(view.to_html(escape=False, index=False), unsafe_allow_html=True)

st.markdown("---")
theme.section_title("Rationale lookup \u2014 explain a single customer's rating")
selected_id = st.selectbox("Select a customer", filtered["customer_id"].tolist())
if selected_id:
    row = customers[customers.customer_id == selected_id].iloc[0]
    st.markdown(
        f"**{row.display_name}** ({row.customer_id}) \u2014 {theme.risk_pill(row.risk_rating)} "
        f"&nbsp;\u2022&nbsp; score **{row.risk_score}** &nbsp;\u2022&nbsp; review every **{row.review_cadence}**",
        unsafe_allow_html=True,
    )
    for reason in row.risk_rationale.split(" | "):
        st.markdown(f"- {reason}")
