# ─────────────────────────────────────────────
#  NIL Valuation Engine · WR Calculator
# ─────────────────────────────────────────────

import streamlit as st
from backend.pvm_models import calculate_wr_pvm
from backend.tiers import classify_tier
from backend.nil_recommendations import get_nil_recommendation
from ui.components import page_header


def render_wr():
    page_header(
        title="Wide Receiver Evaluator",
        subtitle="Enter season statistics to generate a PVM score and NIL valuation.",
        position="WR",
    )

    with st.form("wr_form", clear_on_submit=False):
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    Player Information
</div>
""", unsafe_allow_html=True)

        player_name = st.text_input(
            "Player Name",
            placeholder="e.g. Tavon Austin",
            key="wr_name",
        )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin:8px 0 16px 0;">
    Season Statistics
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            receptions = st.number_input(
                "Receptions",
                min_value=0, max_value=150, value=72, step=1,
                help="Season receptions (range: 0 – 120)",
                key="wr_rec",
            )
            receiving_tds = st.number_input(
                "Receiving TDs",
                min_value=0, max_value=30, value=8, step=1,
                help="Season receiving touchdowns (range: 0 – 20)",
                key="wr_tds",
            )

        with col2:
            receiving_yards = st.number_input(
                "Receiving Yards",
                min_value=0, max_value=2500, value=1050, step=25,
                help="Season receiving yards (range: 0 – 1,800+)",
                key="wr_yards",
            )
            ypr = st.number_input(
                "Yards Per Reception",
                min_value=0.0, max_value=40.0, value=14.6, step=0.1,
                help="Yards per reception average (range: 5.0 – 25.0)",
                key="wr_ypr",
            )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        with st.expander("Model Weights", expanded=False):
            st.markdown("""
<div style="font-size:13px; color:#4a4035; line-height:2.0;">
    <b>Receptions</b> — 30%<br>
    <b>Receiving Yards</b> — 35%<br>
    <b>Receiving TDs</b> — 25%<br>
    <b>Yards Per Reception</b> — 10%
</div>
""", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "Calculate PVM Score →",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if not player_name.strip():
            st.warning("Please enter a player name.")
            return

        pvm_score, norms = calculate_wr_pvm(receptions, receiving_yards, receiving_tds, ypr)
        tier    = classify_tier(pvm_score)
        nil_rec = get_nil_recommendation(tier, pvm_score)

        st.session_state.result = {
            "player_name": player_name.strip(),
            "position":    "WR",
            "pvm_score":   pvm_score,
            "tier":        tier,
            "nil_rec":     nil_rec,
            "normalized":  norms,
            "inputs": {
                "Receptions":       receptions,
                "Receiving Yards":  receiving_yards,
                "Receiving TDs":    receiving_tds,
                "Yards Per Rec":    f"{ypr:.1f}",
            },
        }
        st.session_state.page = "results"
        st.rerun()
