import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import modules.data_utils as data_utils


def show_analytics():

    if "dataset" not in st.session_state:
        st.warning("Please load a dataset first.")
        return

    df = st.session_state["dataset"]

    st.title("Intelligence & Analytics")

    # -----------------------------------
    # APPLY GLOBAL FILTERS
    # -----------------------------------

    areas = st.session_state.get("filter_area", [])
    materials = st.session_state.get("filter_material", [])
    suppliers = st.session_state.get("filter_supplier", [])

    df = data_utils.apply_filters(df, areas, materials, suppliers)

    palette = ["#3b82f6","#10b981","#f59e0b","#14b8a6","#ef4444"]

    tabs = st.tabs([
        "Lifecycle",
        "Density",
        "Suppliers",
        "Hotspots",
        "Packaging Units"
    ])

# ======================================================
# LIFECYCLE TAB
# ======================================================

    with tabs[0]:

        col1, col2 = st.columns(2)

        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status","Count"]

        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.6,
            color="Status",
            color_discrete_map={
                "Reuse":"#10b981",
                "Inspect":"#3b82f6",
                "Recycle":"#ef4444"
            },
            title="Packaging Lifecycle Distribution"
        )

        fig_status.update_layout(template="plotly_dark")

        col1.plotly_chart(fig_status, use_container_width=True)

        reuse_rate = (df["Status"] == "Reuse").mean()*100
        inspect_rate = (df["Status"] == "Inspect").mean()*100
        recycle_rate = (df["Status"] == "Recycle").mean()*100

        with col2:

            st.subheader("Lifecycle Conversion Rates")

            st.progress(reuse_rate/100)
            st.write(f"Reuse Rate: **{reuse_rate:.1f}%**")

            st.progress(inspect_rate/100)
            st.write(f"Inspect Rate: **{inspect_rate:.1f}%**")

            st.progress(recycle_rate/100)
            st.write(f"Recycle Rate: **{recycle_rate:.1f}%**")

        st.markdown("---")

        material_stats = df.groupby("Material").agg({
            "Reuse_Potential_Score":"mean",
            "Condition_Score":"mean",
            "Packaging_ID":"count"
        }).reset_index()

        material_stats.rename(columns={
            "Reuse_Potential_Score":"Avg_Reuse",
            "Condition_Score":"Avg_Condition",
            "Packaging_ID":"Volume"
        }, inplace=True)

        fig_scatter = px.scatter(
            material_stats,
            x="Avg_Reuse",
            y="Avg_Condition",
            size="Volume",
            color="Material",
            title="Strategic Material Performance Quadrant",
            color_discrete_sequence=palette
        )

        fig_scatter.update_layout(
            template="plotly_dark",
            xaxis_title="Average Reuse Potential",
            yaxis_title="Average Condition Score"
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("### Insights")

        insights = []

        if recycle_rate > 50:
            insights.append("High recycle rate detected. Packaging durability may be declining.")

        if reuse_rate < 30:
            insights.append("Reuse rate is below optimal operational threshold.")

        if inspect_rate > 30:
            insights.append("High inspection rate indicates packaging degradation.")

        for insight in insights:
            st.info(insight)


# ======================================================
# DENSITY TAB
# ======================================================

    with tabs[1]:

        st.subheader("Volume Density by Area")

        area_stats = df.groupby("Area").agg({
            "Packaging_ID":"count",
            "Returned":"sum",
            "Orders":"sum"
        }).reset_index()

        area_stats.rename(columns={"Packaging_ID":"Total_Units"}, inplace=True)

        area_stats["Recovery_Rate"] = area_stats["Returned"] / area_stats["Orders"] * 100

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=area_stats["Area"],
            y=area_stats["Total_Units"],
            name="Total Units",
            marker_color="#334155"
        ))

        fig.add_trace(go.Bar(
            x=area_stats["Area"],
            y=area_stats["Recovery_Rate"],
            name="Recovery %",
            marker_color="#10b981",
            yaxis="y2"
        ))

        fig.update_layout(
            template="plotly_dark",
            yaxis=dict(title="Total Units"),
            yaxis2=dict(
                title="Recovery %",
                overlaying="y",
                side="right"
            ),
            barmode="group"
        )

        st.plotly_chart(fig, use_container_width=True)


# ======================================================
# SUPPLIERS TAB
# ======================================================

    with tabs[2]:

        col1, col2 = st.columns(2)

        supplier_durability = (
            df.groupby("Supplier")["Condition_Score"]
            .mean()
            .reset_index()
        )

        fig_supplier = px.bar(
            supplier_durability,
            y="Supplier",
            x="Condition_Score",
            orientation="h",
            color="Supplier",
            title="Supplier Durability",
            color_discrete_sequence=palette
        )

        fig_supplier.update_layout(template="plotly_dark")

        col1.plotly_chart(fig_supplier, use_container_width=True)

        supplier_stats = df.groupby("Supplier").agg({
            "Condition_Score":"mean",
            "Uses":"mean"
        }).reset_index()

        supplier_stats["Reliability_Score"] = (
            supplier_stats["Condition_Score"] * supplier_stats["Uses"]
        )

        fig_reliability = px.scatter(
            supplier_stats,
            x="Uses",
            y="Condition_Score",
            size="Reliability_Score",
            color="Supplier",
            title="Supplier Reliability Landscape",
            color_discrete_sequence=palette
        )

        fig_reliability.update_layout(template="plotly_dark")

        col2.plotly_chart(fig_reliability, use_container_width=True)


# ======================================================
# HOTSPOTS TAB
# ======================================================

    with tabs[3]:

        st.subheader("Waste Hotspots")

        recycle_data = df[df["Status"] == "Recycle"]

        hotspot = recycle_data.groupby("Area").size().reset_index(name="Recycle_Count")

        st.dataframe(hotspot, use_container_width=True)


# ======================================================
# PACKAGING UNITS TABLE (REFERENCE STYLE)
# ======================================================

    with tabs[4]:

        st.subheader("Packaging Asset Registry")

        col1, col2 = st.columns([4,1])

        with col1:
            search = st.text_input(
                "",
                placeholder="Search by ID, Area, or Supplier..."
            )

        with col2:
            status_filter = st.selectbox(
                "",
                ["All Statuses","Reuse","Inspect","Recycle"]
            )

        table = df.copy()

        if search:
            table = table[
                table["Packaging_ID"].str.contains(search,case=False)
                |
                table["Area"].str.contains(search,case=False)
                |
                table["Supplier"].str.contains(search,case=False)
            ]

        if status_filter != "All Statuses":
            table = table[table["Status"] == status_filter]

        table["Health"] = (table["Condition_Score"]*100).round(0).astype(int).astype(str)+"%"

        display = table[[
            "Packaging_ID",
            "Status",
            "Area",
            "Supplier",
            "Uses",
            "Health"
        ]]

        display.columns = [
            "Asset ID",
            "Status",
            "Area",
            "Supplier",
            "Uses",
            "Health"
        ]

        st.dataframe(
            display,
            use_container_width=True,
            height=520
        )
