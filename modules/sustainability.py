import streamlit as st
import plotly.express as px
import modules.data_utils as data_utils


def show_sustainability():

    if "dataset" not in st.session_state:

        st.warning("Please load a dataset first.")
        return

    df = st.session_state["dataset"]

    st.title(" Sustainability Impact Dashboard")

    # ---------------------------------------------------
    # DASHBOARD STYLE (makes metric cards look better)
    # ---------------------------------------------------

    st.markdown("""
    <style>
    [data-testid="metric-container"] {
        background-color:#0f172a;
        border-radius:12px;
        padding:20px;
        border:1px solid #1e293b;
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------------------
    # APPLY GLOBAL FILTERS
    # ----------------------------

    areas = st.session_state.get("filter_area", [])
    materials = st.session_state.get("filter_material", [])
    suppliers = st.session_state.get("filter_supplier", [])

    df = data_utils.apply_filters(df, areas, materials, suppliers)

    # ----------------------------
    # REUSE UNITS
    # ----------------------------

    reuse_df = df[df["Status"] == "Reuse"]

    reuse_units = len(reuse_df)

    # ----------------------------
    # ENVIRONMENTAL SAVINGS
    # ----------------------------

    co2_saved = reuse_units * 0.15
    water_saved = reuse_units * 0.5
    trees_saved = reuse_units * 0.003

    # ADDITIONAL METRICS (industry style)

    boxes_recovered = reuse_units
    cardboard_circular = reuse_units * 0.08
    estimated_savings = reuse_units * 12

    # ----------------------------
    # KPI CARDS
    # ----------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("CO₂ Saved (kg)", f"{co2_saved:,.2f}")
    col2.metric("Water Saved (Liters)", f"{water_saved:,.2f}")
    col3.metric("Trees Saved", f"{trees_saved:,.2f}")

    col4, col5, col6 = st.columns(3)

    col4.metric("Boxes Recovered", f"{boxes_recovered:,}")
    col5.metric("Cardboard Kept Circular (kg)", f"{cardboard_circular:,.2f}")
    col6.metric("Estimated Monthly Savings ($)", f"{estimated_savings:,.0f}")

    st.markdown("---")

    # ----------------------------
    # MATERIAL IMPACT ANALYSIS
    # ----------------------------

    st.subheader("Sustainability Impact by Material")

    material_stats = reuse_df.groupby("Material").size().reset_index(name="Reuse_Count")

    material_stats["CO2_Saved"] = material_stats["Reuse_Count"] * 0.15

    fig_material = px.bar(
        material_stats.sort_values("CO2_Saved", ascending=True),
        x="CO2_Saved",
        y="Material",
        orientation="h",
        color="CO2_Saved",
        color_continuous_scale="Tealgrn",
        title="CO₂ Savings by Packaging Material"
    )

    st.plotly_chart(fig_material, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # MATERIAL CONTRIBUTION TREEMAP
    # ---------------------------------------------------

    st.subheader("Material Sustainability Contribution")

    fig_tree = px.treemap(
        material_stats,
        path=["Material"],
        values="Reuse_Count",
        color="CO2_Saved",
        color_continuous_scale="Teal"
    )

    st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # REUSE POTENTIAL BY MATERIAL (REPLACED HISTOGRAM)
    # ---------------------------------------------------

    st.subheader("Reuse Potential by Material")

    material_reuse = reuse_df.groupby("Material")["Reuse_Potential_Score"].mean().reset_index()

    fig_reuse_material = px.bar(
        material_reuse.sort_values("Reuse_Potential_Score"),
        x="Reuse_Potential_Score",
        y="Material",
        orientation="h",
        color="Reuse_Potential_Score",
        color_continuous_scale="Tealgrn",
        title="Average Reuse Potential Score by Material"
    )

    st.plotly_chart(fig_reuse_material, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # REUSE VS CONDITION SCATTER (NEW INSIGHT)
    # ---------------------------------------------------

    st.subheader("Reuse Potential vs Condition Score")

    fig_scatter = px.scatter(
        reuse_df,
        x="Condition_Score",
        y="Reuse_Potential_Score",
        color="Material",
        title="Reuse Potential vs Condition Score"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # METHODOLOGY NOTE
    # ---------------------------------------------------

    st.info(
        """
        **Methodology Note**

        Sustainability metrics are calculated using industry-standard conversion factors:

        • 1 reused box saves approximately **0.15 kg of CO₂ emissions**  
        • **0.5 liters of water** saved per reused unit  
        • **0.003 trees saved** per reused packaging unit  
        • Economic savings assume **$12 per reused box**

        These estimates approximate the environmental impact of circular packaging reuse programs.
        """
    )