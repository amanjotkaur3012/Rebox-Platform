import streamlit as st
import pandas as pd
import plotly.express as px
import modules.data_utils as data_utils


def show_optimization():

    if "dataset" not in st.session_state:
        st.warning("Please load a dataset first.")
        return

    df = st.session_state["dataset"]

    st.title(" Recovery Optimization Engine")

    # --------------------------------------------------
    # UI STYLE (added – improves dashboard look)
    # --------------------------------------------------

    st.markdown("""
    <style>
    [data-testid="metric-container"] {
        background-color: #0f172a;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #1e293b;
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
    # RECOVERY DENSITY CALCULATION
    # ----------------------------

    area_stats = df.groupby("Area").agg({
        "Returned": "sum",
        "Orders": "sum",
        "Condition_Score": "mean"
    }).reset_index()

    area_stats["Recovery_Density"] = area_stats["Returned"] / area_stats["Orders"]

    area_stats["Recovery_Opportunity"] = (
        area_stats["Returned"] * area_stats["Condition_Score"]
    )

    # --------------------------------------------------
    # KPI SUMMARY (added)
    # --------------------------------------------------

    total_returns = df["Returned"].sum()
    total_orders = df["Orders"].sum()

    if total_orders == 0:
        recovery_rate = 0
    else:
        recovery_rate = total_returns / total_orders

    avg_condition = df["Condition_Score"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Returns", f"{total_returns:,}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Recovery Rate", f"{recovery_rate:.2%}")
    col4.metric("Avg Condition Score", f"{avg_condition:.2f}")

    st.markdown("---")

    # ----------------------------
    # RECOVERY DENSITY CHART
    # ----------------------------

    st.subheader("Recovery Density by Area")

    fig_density = px.bar(
        area_stats.sort_values("Recovery_Density", ascending=False),
        x="Area",
        y="Recovery_Density",
        color="Recovery_Density",
        color_continuous_scale="Teal",
        title="Recovery Density Ranking"
    )

    st.plotly_chart(fig_density, use_container_width=True)

    st.markdown("---")

    # --------------------------------------------------
    # NEW INSIGHT CHART (scatter)
    # --------------------------------------------------

    st.subheader("Recovery Efficiency Map")

    fig_scatter = px.scatter(
        area_stats,
        x="Recovery_Density",
        y="Recovery_Opportunity",
        size="Returned",
        color="Condition_Score",
        hover_name="Area",
        color_continuous_scale="Tealgrn",
        title="High Value Recovery Zones"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # ----------------------------
    # RECOVERY OPPORTUNITY SCORE
    # ----------------------------

    st.subheader("Recovery Opportunity Score")

    fig_opportunity = px.bar(
        area_stats.sort_values("Recovery_Opportunity", ascending=False),
        x="Area",
        y="Recovery_Opportunity",
        color="Recovery_Opportunity",
        color_continuous_scale="Teal",
        title="Recovery Opportunity by Area"
    )

    st.plotly_chart(fig_opportunity, use_container_width=True)

    st.markdown("---")

    # --------------------------------------------------
    # TREEMAP (added insight visualization)
    # --------------------------------------------------

    st.subheader("Recovery Distribution Map")

    fig_tree = px.treemap(
        area_stats,
        path=["Area"],
        values="Returned",
        color="Recovery_Density",
        color_continuous_scale="Tealgrn"
    )

    st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")

    # ----------------------------
    # TOP RECOVERY ZONES
    # ----------------------------

    st.subheader("Top Recovery Zones")

    top_zones = area_stats.sort_values(
        "Recovery_Density",
        ascending=False
    ).head(5)

    st.dataframe(top_zones, use_container_width=True)

    st.markdown("---")

    # --------------------------------------------------
    # NETWORK OPTIMIZATION PANEL
    # --------------------------------------------------

    st.header("Network Optimization")

    col_left, col_right = st.columns([2, 1])

    # -----------------------------
    # STRATEGY SIMULATOR
    # -----------------------------

    with col_left:

        st.subheader("Strategy Simulator")

        scenario = st.selectbox(
            "Recovery Scenario",
            [
                "Centralized Warehouse",
                "Hybrid Pickup & Drop-off",
                "Decentralized Micro Hubs"
            ]
        )

        hub_count = st.number_input(
            "Proposed Hub Count",
            1,
            20,
            5
        )

        if st.button("Run Simulation"):

            scenario_multiplier = {
                "Centralized Warehouse": 0.08,
                "Hybrid Pickup & Drop-off": 0.12,
                "Decentralized Micro Hubs": 0.16
            }

            multiplier = scenario_multiplier.get(scenario, 0.1)

            projected_rate = recovery_rate + (hub_count * multiplier)

            if projected_rate > 0.95:
                projected_rate = 0.95

            monthly_savings = 300 * hub_count * (1 + multiplier)

            co2_reduction = 0.003 * hub_count * (1 + multiplier)

            boxes_recovered = int(total_returns * projected_rate)

            implementation_cost = hub_count * 75000

            roi_months = implementation_cost / (monthly_savings * 12)

            st.markdown("### Simulation Results")

            col1, col2 = st.columns(2)

            col1.metric(
                "Recovery Shift",
                f"{projected_rate:.0%}"
            )

            col2.metric(
                "ROI Timeline",
                f"{roi_months:.0f} months"
            )

            st.write("Current Recovery Rate:", f"{recovery_rate:.1%}")
            st.write("Projected Recovery Rate:", f"{projected_rate:.1%}")
            st.write("Monthly Cost Savings:", f"${monthly_savings:,.0f}")
            st.write("CO₂ Reduction:", f"{co2_reduction:.2f} tons")
            st.write("Boxes Recovered:", boxes_recovered)
            st.write("Implementation Cost:", f"${implementation_cost:,.0f}")

    # --------------------------------------------------
    # RECOMMENDED HUBS PANEL (fixed layout)
    # --------------------------------------------------

    with col_right:

        st.subheader("Recommended Hubs")

        hubs = area_stats.sort_values(
            "Recovery_Opportunity",
            ascending=False
        ).head(8)

        for i, row in hubs.iterrows():

            container = st.container()

            c1, c2 = container.columns([4, 2])

            c1.markdown(f"### {row['Area']}")
            c1.caption("5km coverage radius")

            c2.metric(
                label="Est Capture / Mo",
                value=f"{int(row['Recovery_Opportunity'])}"
            )

            st.markdown("---")

    st.markdown("---")

    # ----------------------------
    # EFFICIENCY SIMULATION
    # ----------------------------

    st.subheader("Logistics Efficiency Simulation")

    efficiency_gain = st.slider(
        "Recovery Route Efficiency Improvement (%)",
        5,
        30,
        15
    )

    base_cost = 10000

    optimized_cost = base_cost * (1 - efficiency_gain / 100)

    savings = base_cost - optimized_cost

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Logistics Cost", f"${base_cost:,.0f}")

    col2.metric("Optimized Cost", f"${optimized_cost:,.0f}")

    col3.metric("Estimated Savings", f"${savings:,.0f}")