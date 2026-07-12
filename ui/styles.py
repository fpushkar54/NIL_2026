# ─────────────────────────────────────────────
#  NIL Valuation Engine · Styles
# ─────────────────────────────────────────────

import streamlit as st


def load_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    color: #0d0d0d;
}

.stApp {
    background-color: #f4f2ee;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e8e4de !important;
}

[data-testid="stSidebar"] .stMarkdown p {
    color: #0d0d0d !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Inputs ── */
input[type="number"],
input[type="text"],
.stNumberInput input,
.stTextInput input {
    background: #ffffff !important;
    color: #0d0d0d !important;
    border: 1px solid #d0c8be !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 15px !important;
}

input[type="number"]:focus,
input[type="text"]:focus {
    border-color: #0369a1 !important;
    box-shadow: 0 0 0 3px rgba(3,105,161,0.10) !important;
    outline: none !important;
}
/* ── Input Labels ── */
label[data-testid="stWidgetLabel"] {
    color: #000000 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* ── Placeholder Text ── */
input::placeholder {
    color: #8b7f72 !important;
    opacity: 1 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    transition: opacity 0.15s ease, transform 0.1s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    opacity: 1 !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    background: #0d0d0d !important;
    color: #ffffff !important;
    transition: opacity 0.15s ease !important;
}

.stDownloadButton > button:hover {
    opacity: 0.85 !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid #e8e4de !important;
    margin: 1.5rem 0 !important;
}

/* ── Cards ── */
.nil-card {
    background: #ffffff;
    border: 1px solid #e8e4de;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 16px;
}

/* ── Section labels ── */
.section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8b7f72;
    margin-bottom: 6px;
}

/* ── Plotly chart container ── */
[data-testid="stPlotlyChart"] {
    background: transparent !important;
}

/* ── Metric override ── */
[data-testid="stMetric"] {
    background: transparent !important;
}
/* ── Alerts / Warning Messages ── */
[data-testid="stAlert"] {
    background-color: #ffffff !important;
    border-left: 4px solid #d97706 !important;
}

[data-testid="stAlert"] * {
    color: #0d0d0d !important;
    font-weight: 600 !important;
}

/* ── Expander Text ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #4a4035 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}
/* ── Force Expander Text Dark ── */
[data-testid="stExpander"] * {
    color: #0d0d0d !important;
    opacity: 1 !important;
}
</style>

""", unsafe_allow_html=True)
