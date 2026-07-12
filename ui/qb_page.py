# ─────────────────────────────────────────────
#  NIL Valuation Engine · QB Calculator
# ─────────────────────────────────────────────

import streamlit as st
from backend.pvm_models import calculate_qb_pvm
from backend.tiers import classify_tier
from backend.nil_recommendations import get_nil_recommendation
from ui.components import page_header


def render_qb():
    page_header(
        title="Quarterback Evaluator",
        subtitle="Enter season statistics to generate a PVM score and NIL valuation.",
        position="QB",
    )

    with st.form("qb_form", clear_on_submit=False):
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    Player Information
</div>
""", unsafe_allow_html=True)

        player_name = st.text_input(
            "Player Name",
            placeholder="e.g. Ryan Leaf",
            key="qb_name",
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
            passing_yards = st.number_input(
                "Passing Yards",
                min_value=0, max_value=6000, value=3500, step=50,
                help="Season passing yards (range: 0 – 5,000+)",
                key="qb_yards",
            )
            completion_pct = st.number_input(
                "Completion %",
                min_value=0.0, max_value=100.0, value=65.0, step=0.5,
                help="Completion percentage (range: 40 – 80%)",
                key="qb_comp",
            )

        with col2:
            passing_tds = st.number_input(
                "Passing TDs",
                min_value=0, max_value=60, value=28, step=1,
                help="Season passing touchdowns (range: 0 – 50)",
                key="qb_tds",
            )
            int_pct = st.number_input(
                "INT %",
                min_value=0.0, max_value=15.0, value=2.5, step=0.1,
                help="Interception percentage – lower is better (range: 0 – 10%)",
                key="qb_int",
            )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        # Weight reference
        with st.expander("Model Weights", expanded=False):
            st.markdown("""
<div style="font-size:13px; color:#4a4035; line-height:2.0;">
    <b>Passing Yards</b> — 35%<br>
    <b>Passing TDs</b> — 35%<br>
    <b>Completion %</b> — 20%<br>
    <b>INT %</b> — 10% <em>(inverted)</em>
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

        pvm_score, norms = calculate_qb_pvm(
            passing_yards, passing_tds, completion_pct, int_pct
        )
        tier    = classify_tier(pvm_score)
        nil_rec = get_nil_recommendation(tier, pvm_score)

        st.session_state.result = {
            "player_name": player_name.strip(),
            "position":    "QB",
            "pvm_score":   pvm_score,
            "tier":        tier,
            "nil_rec":     nil_rec,
            "normalized":  norms,
            "inputs": {
                "Passing Yards":  passing_yards,
                "Passing TDs":    passing_tds,
                "Completion %":   f"{completion_pct:.1f}%",
                "INT %":          f"{int_pct:.1f}%",
            },
        }
        st.session_state.page = "results"
        st.rerun()
