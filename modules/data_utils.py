import pandas as pd
import numpy as np
import streamlit as st


# -----------------------------------
# CONSTANTS
# -----------------------------------

AREAS = [
"Sector 46","Sector 52","Sector 55","Sector 30","Sector 12",
"Sector 18","Sector 7","Sector 63","Sector 41","Sector 29"
]

MATERIALS = [
"Corrugated Cardboard",
"Kraft Paper",
"Bubble Wrap",
"Foam Box",
"Plastic Box"
]

SUPPLIERS = [
"Supplier A",
"Supplier B",
"Supplier C",
"Supplier D"
]


# -----------------------------------
# STATUS CLASSIFICATION
# -----------------------------------

def compute_status(uses, condition):

    if uses > 6 or condition < 0.40:
        return "Recycle"

    elif uses >= 4:
        return "Inspect"

    else:
        return "Reuse"


# -----------------------------------
# REUSE POTENTIAL SCORE
# -----------------------------------

def reuse_potential_score(uses, condition):

    return round((condition * 10) - uses, 2)


# -----------------------------------
# DEMO DATASET GENERATOR
# -----------------------------------

def generate_demo_dataset(n=800):

    records = []

    for i in range(n):

        uses = np.random.randint(1, 10)
        condition = round(np.random.uniform(0.30, 0.95), 2)

        returned = np.random.choice([True, False], p=[0.6, 0.4])

        status = compute_status(uses, condition)

        reuse_score = reuse_potential_score(uses, condition)

        records.append({

            "Packaging_ID": f"BX{2000+i}",

            "Date": pd.Timestamp("2024-01-01") + pd.to_timedelta(np.random.randint(0,180), unit="D"),

            "Area": np.random.choice(AREAS),

            "Material": np.random.choice(MATERIALS),

            "Supplier": np.random.choice(SUPPLIERS),

            "Uses": uses,

            "Condition_Score": condition,

            "Orders": np.random.randint(20, 300),

            "Returned": returned,

            "Status": status,

            "Reuse_Potential_Score": reuse_score
        })

    df = pd.DataFrame(records)

    return df


# -----------------------------------
# LOAD DATA
# -----------------------------------

def load_data():

    if "dataset" not in st.session_state:
        return None

    return st.session_state["dataset"]


# -----------------------------------
# DATA UPLOAD
# -----------------------------------

def upload_dataset(uploaded_file):

    if uploaded_file is None:
        return None

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):

        df = pd.read_excel(uploaded_file)

    else:

        st.error("Unsupported file type")
        return None


    # CLEAN COLUMN NAMES
    df.columns = df.columns.str.strip()


    # FIX DATE COLUMN
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


    st.session_state["dataset"] = df

    return df


    # -----------------------------------
    # FIX COLUMN NAME ISSUES (NEW)
    # -----------------------------------

    df.columns = df.columns.str.strip()     # remove spaces
    df.columns = df.columns.str.replace(" ", "_")  # normalize spaces
    df.columns = df.columns.str.replace("__", "_")


    st.session_state["dataset"] = df

    return df


# -----------------------------------
# DATA SUMMARY
# -----------------------------------

def dataset_summary(df):

    summary = {

        "records": len(df),

        "areas": df["Area"].nunique(),

        "materials": df["Material"].nunique(),

        "suppliers": df["Supplier"].nunique()

    }

    return summary


# -----------------------------------
# APPLY GLOBAL FILTERS
# -----------------------------------

def apply_filters(df, areas, materials, suppliers):

    filtered = df.copy()

    if areas:

        filtered = filtered[filtered["Area"].isin(areas)]

    if materials:

        filtered = filtered[filtered["Material"].isin(materials)]

    if suppliers:

        filtered = filtered[filtered["Supplier"].isin(suppliers)]

    return filtered
