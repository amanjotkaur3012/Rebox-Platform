import streamlit as st
import plotly.express as px
import modules.data_utils as data_utils


def show_dashboard():

    if "dataset" not in st.session_state:
        st.warning("Please generate or upload a dataset first.")
        return

    df = st.session_state["dataset"].copy()

    st.title("Command Center")
    st.caption("Real-time overview of your packaging recovery network.")

    # FILTERS
    areas = st.session_state.get("filter_area", [])
    materials = st.session_state.get("filter_material", [])
    suppliers = st.session_state.get("filter_supplier", [])

    df = data_utils.apply_filters(df,areas,materials,suppliers)

    total_units = len(df)
    active_units = (df["Status"]!="Recycle").sum()

    returned_units = df["Returned"].sum()
    recovery_rate = returned_units/total_units if total_units else 0

    reuse_units = (df["Status"]=="Reuse").sum()

    cost_savings = reuse_units*0.70

    avg_condition = df["Condition_Score"].mean()
    health_score = avg_condition*100

    target_recovery = 0.85

    # KPI CARDS
    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "TOTAL UNITS",
        total_units,
        f"{active_units} active in field"
    )

    c2.metric(
        "RECOVERY RATE",
        f"{recovery_rate:.1%}",
        f"Target: {target_recovery:.0%}"
    )

    c3.metric(
        "COST SAVINGS",
        f"${cost_savings:,.0f}",
        "Monthly estimated"
    )

    c4.metric(
        "CONDITION",
        f"{health_score:.0f}",
        "Average network health"
    )

    st.markdown("---")

    col1,col2 = st.columns([2,1])

    # RECOVERY TREND
    with col1:

        st.subheader("Recovery Trend")

        trend = df.groupby(df["Date"].dt.month)["Returned"].mean().reset_index()

        fig = px.area(
            trend,
            x="Date",
            y="Returned",
            title=""
        )

        st.plotly_chart(fig,use_container_width=True)

    # INSIGHTS PANEL
    with col2:

        st.subheader("Automated Insights")

        insights = []

        area_orders = df.groupby("Area")["Orders"].sum()
        top_area = area_orders.idxmax()

        insights.append(
            f"High packaging volume in **{top_area}**"
        )

        supplier_score = df.groupby("Supplier")["Condition_Score"].mean()
        best_supplier = supplier_score.idxmax()

        insights.append(
            f"**{best_supplier}** outperforms other suppliers in durability"
        )

        if recovery_rate >= 0.75:
           insights.append("Recovery rate performing strongly")

        elif recovery_rate >= 0.55:
           insights.append("Recovery rate stable but improvement possible")

        else:
           insights.append("Recovery rate below optimal threshold")

        area_stats = df.groupby("Area").agg({
            "Returned":"sum",
            "Orders":"sum"
        })

        area_stats["rate"]=area_stats["Returned"]/area_stats["Orders"]

        weak = area_stats[area_stats["rate"]<0.3]

        if len(weak)>0:
            insights.append(f"Low recovery in {len(weak)} area(s)")

        for i in insights:
            st.info(i)

        st.markdown("---")

        csv = df.to_csv(index=False)

        st.download_button(
           "Download Filtered Analysis Data",
            csv,
            "rebox_analysis.csv"
       )    