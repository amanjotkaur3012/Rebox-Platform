import streamlit as st
import modules.data_utils as data_utils


def show_insights():

    if "dataset" not in st.session_state:
        st.warning("Please load a dataset first.")
        return

    df = st.session_state["dataset"]

    st.title(" Insights ")

    # ----------------------------
    # APPLY GLOBAL FILTERS
    # ----------------------------

    areas = st.session_state.get("filter_area", [])
    materials = st.session_state.get("filter_material", [])
    suppliers = st.session_state.get("filter_supplier", [])

    df = data_utils.apply_filters(df, areas, materials, suppliers)

    insights = []

    # ----------------------------
    # MATERIAL REUSE POTENTIAL
    # ----------------------------

    material_reuse = df[df["Status"] == "Reuse"]["Material"].value_counts()

    if not material_reuse.empty:

        best_material = material_reuse.idxmax()
        best_material_count = material_reuse.max()

        insights.append(
            f" **{best_material}** shows the highest reuse potential with **{best_material_count} reused units**."
        )

        worst_material = material_reuse.idxmin()
        worst_material_count = material_reuse.min()

        insights.append(
            f" **{worst_material}** has the lowest reuse frequency (**{worst_material_count} units**) and may require redesign."
        )

    # ----------------------------
    # SUPPLIER DURABILITY
    # ----------------------------

    supplier_durability = df.groupby("Supplier")["Condition_Score"].mean()

    if not supplier_durability.empty:

        best_supplier = supplier_durability.idxmax()
        best_score = supplier_durability.max()

        insights.append(
            f" **{best_supplier}** provides the most durable packaging with an average condition score of **{best_score:.2f}**."
        )

        worst_supplier = supplier_durability.idxmin()
        worst_score = supplier_durability.min()

        insights.append(
            f" **{worst_supplier}** shows the lowest durability score (**{worst_score:.2f}**) and may need quality improvements."
        )

    # ----------------------------
    # RECOVERY DENSITY
    # ----------------------------

    area_stats = df.groupby("Area").agg({
        "Returned": "sum",
        "Orders": "sum"
    })

    area_stats["Recovery_Density"] = area_stats["Returned"] / area_stats["Orders"]

    if not area_stats.empty:

        best_area = area_stats["Recovery_Density"].idxmax()
        best_density = area_stats["Recovery_Density"].max()

        insights.append(
            f" **{best_area}** shows the highest packaging recovery density (**{best_density:.2%}**)."
        )

        worst_area = area_stats["Recovery_Density"].idxmin()
        worst_density = area_stats["Recovery_Density"].min()

        insights.append(
            f" **{worst_area}** has the lowest recovery density (**{worst_density:.2%}**) and may benefit from additional drop-off points."
        )

    # ----------------------------
    # REUSE POTENTIAL SCORE
    # ----------------------------

    avg_reuse_score = df["Reuse_Potential_Score"].mean()

    if avg_reuse_score > 6:
        insights.append(
            f" Packaging reuse potential is **very strong** with an average score of **{avg_reuse_score:.2f}**."
        )

    elif avg_reuse_score > 4:
        insights.append(
            f" Reuse potential is **moderate** (average score **{avg_reuse_score:.2f}**). Improving packaging durability could increase reuse cycles."
        )

    else:
        insights.append(
            f" Reuse potential is **low** (average score **{avg_reuse_score:.2f}**). Packaging redesign may be required."
        )

    # ----------------------------
    # COST SAVINGS INSIGHT
    # ----------------------------

    reuse_units = (df["Status"] == "Reuse").sum()

    estimated_savings = reuse_units * 0.70

    insights.append(
        f" Estimated cost savings from reuse could reach **${estimated_savings:,.0f}** based on **{reuse_units} reused packages**."
    )

    # ----------------------------
    # DISPLAY INSIGHTS
    # ----------------------------

    st.subheader("Automated Insights")

    for insight in insights:
        st.success(insight)

    st.markdown("---")

    st.info(
        "These insights are generated automatically using packaging lifecycle analytics."
    )