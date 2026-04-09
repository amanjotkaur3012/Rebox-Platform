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
# GLOBAL STYLING (NEW)
# ------------------------------------------------

st.markdown("""
<style>

/* remove extra padding from top */
.block-container {
    padding-top: 1.5rem;
}

/* main product title */
.app-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg,#60a5fa,#22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* subtitle */
.app-subtitle {
    font-size: 15px;
    color: #94a3b8;
    margin-top: -10px;
    margin-bottom: 30px;
}

/* section headers */
h1, h2, h3 {
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* sidebar spacing */
section[data-testid="stSidebar"] {
    padding-top: 10px;
}

/* sidebar navigation radio buttons */
div[role="radiogroup"] > label {
    padding: 8px 6px;
    font-size: 15px;
}

/* filter titles */
.sidebar-title {
    font-size: 14px;
    font-weight: 600;
    color: #9ca3af;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# GLOBAL HEADER (Better typography)
# ------------------------------------------------

st.markdown(
"""
<div class="app-title">ReBox</div>
<div class="app-subtitle">Circular Packaging Intelligence Platform</div>
""",
unsafe_allow_html=True
)


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

            # FIX column issues automatically
            df.columns = df.columns.str.strip()

            st.markdown('<div class="sidebar-title">Filters</div>', unsafe_allow_html=True)

            # SAFE FILTER CREATION

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

        # USER PANEL
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