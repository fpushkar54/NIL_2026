# ─────────────────────────────────────────────
#  NIL Valuation Engine · Home Page
# ─────────────────────────────────────────────

import streamlit as st
from backend.constants import POSITION_COLORS

QB_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"
    fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/>
    <line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/>
    <line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/></svg>"""

RB_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"
    fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>"""

WR_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"
    fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="2"/>
    <path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/></svg>"""


def position_card(key: str, label: str, full_name: str,
                  description: str, color: str, icon_svg: str) -> bool:
    """
    Renders an HTML card via st.markdown followed by a single
    native Streamlit button styled to match the colored pill.
    Returns True when the button is clicked.
    """
    # Card body — no button inside, no pill duplicate
    st.markdown(f"""
<div style="
    background: #ffffff;
    border: 1px solid #e8e4de;
    border-top: 3px solid {color};
    border-radius: 12px 12px 0 0;
    padding: 28px 24px 20px 24px;
    font-family: 'Outfit', sans-serif;
">
    <div style="color:{color}; margin-bottom:14px; line-height:1;">{icon_svg}</div>
    <div style="font-size:24px; font-weight:800; color:#0d0d0d;
                letter-spacing:-0.01em; margin-bottom:4px;">{label}</div>
    <div style="font-size:14px; font-weight:500; color:#4a4035;
                margin-bottom:10px;">{full_name}</div>
    <div style="font-size:12px; color:#8b7f72; line-height:1.5;">{description}</div>
</div>
<style>
    div[data-testid="stButton"]:has(~ *) {{ }}
    .btn-{key} > button {{
        background-color: {color} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 10px 24px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        font-family: 'Outfit', sans-serif !important;
        width: 100% !important;
        text-align: left !important;
        cursor: pointer !important;
        transition: opacity 0.15s ease !important;
        box-shadow: none !important;
        margin-top: 0 !important;
    }}
    .btn-{key} > button:hover {{
        opacity: 0.88 !important;
        color: #ffffff !important;
    }}
</style>
""", unsafe_allow_html=True)

    # Native Streamlit button — the only interactive element
    st.markdown(f'<div class="btn-{key}">', unsafe_allow_html=True)
    clicked = st.button("Open Calculator →", key=key, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked


def render_home():
    # ── Hero ─────────────────────────────────
    st.markdown("""
<div style="padding: 48px 0 40px 0;">
    <div style="font-size:11px; font-weight:700; letter-spacing:0.18em;
                text-transform:uppercase; color:#8b7f72; margin-bottom:14px;">
        College Football
    </div>
    <h1 style="font-size:42px; font-weight:800; color:#0d0d0d;
               margin:0 0 10px 0; letter-spacing:-0.03em; line-height:1.1;">
        NIL Valuation<br>Engine
    </h1>
    <p style="font-size:16px; color:#6b5f52; margin:0; font-weight:400;">
        Performance-Based Athlete Valuation
    </p>
    <div style="width:48px; height:3px; background:#0d0d0d; border-radius:2px;
                margin-top:20px;"></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    Select Position
</div>
""", unsafe_allow_html=True)

    positions = [
        {
            "key":   "home_qb",
            "page":  "qb",
            "label": "QB",
            "full":  "Quarterback",
            "desc":  "Passing yards · TDs · Completion % · INT %",
            "color": POSITION_COLORS["QB"],
            "icon":  QB_ICON,
        },
        {
            "key":   "home_rb",
            "page":  "rb",
            "label": "RB",
            "full":  "Running Back",
            "desc":  "Rushing yards · TDs · Yards per carry",
            "color": POSITION_COLORS["RB"],
            "icon":  RB_ICON,
        },
        {
            "key":   "home_wr",
            "page":  "wr",
            "label": "WR",
            "full":  "Wide Receiver",
            "desc":  "Receptions · Receiving yards · TDs · YPR",
            "color": POSITION_COLORS["WR"],
            "icon":  WR_ICON,
        },
    ]

    cols = st.columns(3, gap="medium")

    for i, pos in enumerate(positions):
        with cols[i]:
            if position_card(
                key=pos["key"],
                label=pos["label"],
                full_name=pos["full"],
                description=pos["desc"],
                color=pos["color"],
                icon_svg=pos["icon"],
            ):
                st.session_state.page = pos["page"]
                st.rerun()

    st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)