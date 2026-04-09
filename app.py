import streamlit as st

import modules.auth as auth
import modules.home as home
import modules.dashboard as dashboard
import modules.analytics as analytics
import modules.optimization as optimization
import modules.sustainability as sustainability
import modules.insights as insights
import modules.data_utils as data_utils
import modules.theme as theme
from fpdf import FPDF


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="ReBox Platform",
    page_icon="📦",
    layout="wide"
)

# Apply dark theme once
theme.apply_theme()


# ------------------------------------------------
# GLOBAL STYLING
# ------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
}

.app-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg,#60a5fa,#22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.app-subtitle {
    font-size: 15px;
    color: #94a3b8;
    margin-top: -10px;
    margin-bottom: 30px;
}

h1, h2, h3 {
    font-weight: 600;
    letter-spacing: 0.3px;
}

section[data-testid="stSidebar"] {
    padding-top: 10px;
}

div[role="radiogroup"] > label {
    padding: 8px 6px;
    font-size: 15px;
}

.sidebar-title {
    font-size: 14px;
    font-weight: 600;
    color: #9ca3af;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# GLOBAL HEADER
# ------------------------------------------------

st.markdown(
"""
<div class="app-title">ReBox</div>
<div class="app-subtitle">Circular Packaging Intelligence Platform</div>
""",
unsafe_allow_html=True
)


# ------------------------------------------------
# PDF REPORT FUNCTION
# ------------------------------------------------

def generate_pdf_report(df):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ReBox Analytics Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total Records: {len(df)}", ln=True)

    if "Area" in df.columns:
        pdf.cell(0, 10, f"Areas: {df['Area'].nunique()}", ln=True)

    if "Material" in df.columns:
        pdf.cell(0, 10, f"Materials: {df['Material'].nunique()}", ln=True)

    if "Supplier" in df.columns:
        pdf.cell(0, 10, f"Suppliers: {df['Supplier'].nunique()}", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Sample Data:", ln=True)

    pdf.set_font("Arial", "", 10)

    sample = df.head(10)

    for _, row in sample.iterrows():
        pdf.cell(0, 8, str(row.values), ln=True)

    return pdf.output(dest="S").encode("latin-1")


# ------------------------------------------------
# SESSION STATE INIT
# ------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if "navigate_to" not in st.session_state:
    st.session_state["navigate_to"] = None


# ------------------------------------------------
# PAGE MAPPING
# ------------------------------------------------

PAGES = {
    "Home": "Overview",
    "Dashboard": "Operations Intelligence",
    "Analytics": "Packaging Analytics",
    "Optimization": "Recovery Optimization",
    "Sustainability": "Sustainability Metrics",
    "Insights": "Strategic Insights"
}


def change_page(page):

    st.session_state["navigate_to"] = PAGES[page]

    st.rerun()


# ------------------------------------------------
# MAIN APP
# ------------------------------------------------

def main():

    if not st.session_state["logged_in"]:
        auth.login_page()
        return


    # ------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------

    with st.sidebar:

        st.caption("Circular Packaging Intelligence")

        st.markdown("---")

        st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

        if st.session_state["navigate_to"] is not None:
            st.session_state["current_page"] = st.session_state["navigate_to"]
            st.session_state["navigate_to"] = None

        selected_page = st.radio(
            "",
            list(PAGES.values()),
            key="current_page"
        )

        st.markdown("---")

        # ------------------------------------------------
        # LOAD DATASET
        # ------------------------------------------------

        df = data_utils.load_data()

        if df is not None:

            df.columns = df.columns.str.strip()

            st.markdown('<div class="sidebar-title">Filters</div>', unsafe_allow_html=True)

            if "Area" in df.columns:
                st.multiselect(
                    "Area",
                    options=sorted(df["Area"].dropna().unique()),
                    key="filter_area"
                )

            if "Material" in df.columns:
                st.multiselect(
                    "Material",
                    options=sorted(df["Material"].dropna().unique()),
                    key="filter_material"
                )

            if "Supplier" in df.columns:
                st.multiselect(
                    "Supplier",
                    options=sorted(df["Supplier"].dropna().unique()),
                    key="filter_supplier"
                )

        st.markdown("---")


        # ------------------------------------------------
        # DOWNLOAD PDF REPORT
        # ------------------------------------------------

        if df is not None:

            pdf_bytes = generate_pdf_report(df)

            st.download_button(
                label="Download Analytics Report (PDF)",
                data=pdf_bytes,
                file_name="rebox_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )


        # ------------------------------------------------
        # USER PANEL
        # ------------------------------------------------

        with st.container(border=True):

            st.write(f"User: **{st.session_state['username']}**")

            if st.button("Logout", use_container_width=True):

                st.session_state["logged_in"] = False
                st.rerun()


    # ------------------------------------------------
    # ROUTING
    # ------------------------------------------------

    if selected_page == PAGES["Home"]:
        home.show_home(change_page)

    elif selected_page == PAGES["Dashboard"]:
        dashboard.show_dashboard()

    elif selected_page == PAGES["Analytics"]:
        analytics.show_analytics()

    elif selected_page == PAGES["Optimization"]:
        optimization.show_optimization()

    elif selected_page == PAGES["Sustainability"]:
        sustainability.show_sustainability()

    elif selected_page == PAGES["Insights"]:
        insights.show_insights()


# ------------------------------------------------
# RUN APP
# ------------------------------------------------

if __name__ == "__main__":
    main()
