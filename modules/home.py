import streamlit as st
import modules.data_utils as data_utils


def show_home(change_page):

    st.title(" ReBox Circular Packaging Intelligence Platform")

    st.markdown("""
    ReBox is an analytics platform designed to help e-commerce companies
    optimize packaging reuse, reduce waste, and improve sustainability metrics
    through data-driven insights.
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Upload Dataset
    with col1:

        st.subheader("Upload Dataset")

        uploaded_file = st.file_uploader(
            "Upload CSV or Excel dataset",
            type=["csv","xlsx"]
        )

        if uploaded_file:

            df = data_utils.upload_dataset(uploaded_file)

            if df is not None:

                st.session_state["dataset"] = df

                st.success("Dataset loaded successfully")

    # Generate Demo Data
    with col2:

        st.subheader("Generate Demo Data")

        if st.button("Generate Demo Dataset", use_container_width=True):

            df = data_utils.generate_demo_dataset()

            st.session_state["dataset"] = df

            st.success("Demo dataset generated")

    st.markdown("---")

    # Dataset Preview
    if "dataset" in st.session_state:

        df = st.session_state["dataset"]

        st.subheader("Dataset Preview")

        st.dataframe(df.head(20), use_container_width=True)

        summary = data_utils.dataset_summary(df)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Records", summary["records"])
        col2.metric("Areas", summary["areas"])
        col3.metric("Materials", summary["materials"])
        col4.metric("Suppliers", summary["suppliers"])

        st.markdown("---")

        st.download_button(
            label="Download Dataset",
            data=df.to_csv(index=False),
            file_name="rebox_dataset.csv",
            mime="text/csv"
        )

        if st.button("Start Analysis", use_container_width=True):

            change_page("Dashboard")