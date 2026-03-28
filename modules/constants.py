import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #05070a; color: #e1e1e1; }
        .block-container { max-width: 1400px; padding: 2rem; margin: auto; }
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 25px !important;
        }
        [data-testid="stSidebar"] { background-color: #0a0c10; border-right: 1px solid rgba(0, 209, 178, 0.2); }
        .stButton>button {
            width: 100%; border-radius: 12px; background: linear-gradient(90deg, #00d1b2 0%, #0097a7 100%);
            color: white; font-weight: 800; height: 50px; border: none; transition: 0.4s;
        }
        .stTabs [aria-selected="true"] { background: rgba(0, 209, 178, 0.1) !important; border: 1px solid #00d1b2 !important; color: #00d1b2 !important; }
        </style>
    """, unsafe_allow_html=True)