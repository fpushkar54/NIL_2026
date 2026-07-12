# ─────────────────────────────────────────────
#  NIL Valuation Engine · RB Calculator
# ─────────────────────────────────────────────

import streamlit as st
from backend.pvm_models import calculate_rb_pvm
from backend.tiers import classify_tier
from backend.nil_recommendations import get_nil_recommendation
from ui.components import page_header


def render_rb():
    page_header(
        title="Running Back Evaluator",
        subtitle="Enter season statistics to generate a PVM score and NIL valuation.",
        position="RB",
    )

    with st.form("rb_form", clear_on_submit=False):
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    Player Information
</div>
""", unsafe_allow_html=True)

        player_name = st.text_input(
            "Player Name",
            placeholder="e.g. Rickey Williams",
            key="rb_name",
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
            rushing_yards = st.number_input(
                "Rushing Yards",
                min_value=0, max_value=3000, value=1200, step=25,
                help="Season rushing yards (range: 0 – 2,000+)",
                key="rb_yards",
            )
            ypc = st.number_input(
                "Yards Per Carry",
                min_value=0.0, max_value=15.0, value=5.2, step=0.1,
                help="Yards per carry average (range: 2.0 – 8.0)",
                key="rb_ypc",
            )

        with col2:
            rushing_tds = st.number_input(
                "Rushing TDs",
                min_value=0, max_value=40, value=12, step=1,
                help="Season rushing touchdowns (range: 0 – 25)",
                key="rb_tds",
            )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        with st.expander("Model Weights", expanded=False):
            st.markdown("""
<div style="font-size:13px; color:#4a4035; line-height:2.0;">
    <b>Rushing Yards</b> — 35%<br>
    <b>Rushing TDs</b> — 30%<br>
    <b>Yards Per Carry</b> — 35%
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

        pvm_score, norms = calculate_rb_pvm(rushing_yards, rushing_tds, ypc)
        tier    = classify_tier(pvm_score)
        nil_rec = get_nil_recommendation(tier, pvm_score)

        st.session_state.result = {
            "player_name": player_name.strip(),
            "position":    "RB",
            "pvm_score":   pvm_score,
            "tier":        tier,
            "nil_rec":     nil_rec,
            "normalized":  norms,
            "inputs": {
                "Rushing Yards":   rushing_yards,
                "Rushing TDs":     rushing_tds,
                "Yards Per Carry": f"{ypc:.1f}",
            },
        }
        st.session_state.page = "results"
        st.rerun()
