import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    .stApp{
        background-color:#0b1220;
        color:white;
    }

    section[data-testid="stSidebar"]{
        background-color:#111827;
        border-right:1px solid #1f2937;
    }

    h1,h2,h3,h4{
        color:white;
    }

    .stMetric{
        background:#111827;
        padding:20px;
        border-radius:12px;
        border:1px solid #1f2937;
    }

    .stButton>button{
        background:#3b82f6;
        color:white;
        border-radius:8px;
        height:40px;
        border:none;
    }

    .stDataFrame{
        background:#111827;
        border-radius:10px;
    }

    </style>
    """,unsafe_allow_html=True)