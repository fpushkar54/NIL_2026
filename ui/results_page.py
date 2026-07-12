# ─────────────────────────────────────────────
#  NIL Valuation Engine · Results Page
# ─────────────────────────────────────────────

import streamlit as st
from backend.constants import POSITION_COLORS
from backend.tiers import get_tier_badge_style
from backend.report_generator import generate_pdf_report, generate_txt_report
from ui.components import pvm_gauge, radar_chart, stat_row, tier_badge


def render_results():
    result = st.session_state.get("result")

    if not result:
        st.info("No results found. Please run a calculation first.")
        if st.button("← Go to Home"):
            st.session_state.page = "home"
            st.rerun()
        return

    name     = result["player_name"]
    position = result["position"]
    pvm      = result["pvm_score"]
    tier     = result["tier"]
    nil_rec  = result["nil_rec"]
    norms    = result["normalized"]
    inputs   = result["inputs"]
    color    = POSITION_COLORS.get(position, "#0d0d0d")
    badge    = get_tier_badge_style(tier)

    # ── Back button ──────────────────────────
    if st.button("← Back to Calculator"):
        st.session_state.page = position.lower()
        st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── Player Profile Card ──────────────────
    nil_display = nil_rec.get("display", "No Recommended NIL Allocation")
    eligible    = nil_rec.get("eligible", False)
    nil_color   = color if eligible else "#dc2626"

    st.markdown(f"""
<div style="
    background: #ffffff;
    border: 1px solid #e8e4de;
    border-top: 4px solid {color};
    border-radius: 14px;
    padding: 32px 36px;
    margin-bottom: 24px;
">
    <div style="display:flex; align-items:flex-start; justify-content:space-between;
                flex-wrap:wrap; gap:20px;">
        <div>
            <div style="font-size:11px; font-weight:700; letter-spacing:0.14em;
                        text-transform:uppercase; color:{color}; margin-bottom:8px;">
                {position} · Player Valuation Report
            </div>
            <h2 style="font-size:32px; font-weight:800; color:#0d0d0d;
                       margin:0 0 10px 0; letter-spacing:-0.02em;">{name}</h2>
            <div style="margin-bottom:14px;">
                {tier_badge(tier, "md")}
            </div>
            <div style="font-size:14px; color:{nil_color}; font-weight:600;">
                {nil_display}
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
                        text-transform:uppercase; color:#8b7f72; margin-bottom:6px;">
                PVM Score
            </div>
            <div style="font-size:52px; font-weight:800; color:#0d0d0d;
                        letter-spacing:-0.03em; line-height:1.0;">
                {pvm:.3f}
            </div>
            <div style="font-size:13px; color:#8b7f72; margin-top:4px;">
                out of 1.000
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Charts ───────────────────────────────
    col_gauge, col_radar = st.columns([1, 1], gap="large")

    with col_gauge:
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:10px;">
    Performance Gauge
</div>
""", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="nil-card" style="padding:16px;">', unsafe_allow_html=True)
            st.plotly_chart(
                pvm_gauge(pvm, tier, position),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with col_radar:
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:10px;">
    Stat Profile
</div>
""", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="nil-card" style="padding:16px;">', unsafe_allow_html=True)
            st.plotly_chart(
                radar_chart(norms, position),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Stat Breakdown ───────────────────────
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:14px;">
    Statistical Breakdown
</div>
""", unsafe_allow_html=True)

    label_map = {
        "passing_yards":   "Passing Yards",
        "passing_tds":     "Passing TDs",
        "completion_pct":  "Completion %",
        "int_pct":         "Ball Security (INT %)",
        "rushing_yards":   "Rushing Yards",
        "rushing_tds":     "Rushing TDs",
        "ypc":             "Yards Per Carry",
        "receptions":      "Receptions",
        "receiving_yards": "Receiving Yards",
        "receiving_tds":   "Receiving TDs",
        "ypr":             "Yards Per Reception",
    }

    raw_vals = list(inputs.values())
    norm_keys = list(norms.keys())

    with st.container():
        st.markdown('<div class="nil-card">', unsafe_allow_html=True)
        cols = st.columns(2, gap="large")
        for i, (norm_key, norm_val) in enumerate(norms.items()):
            raw = raw_vals[i] if i < len(raw_vals) else "—"
            label = label_map.get(norm_key, norm_key)
            with cols[i % 2]:
                stat_row(label, raw, norm_val, position)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tier + NIL Section ───────────────────
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    col_tier, col_nil = st.columns([1, 1], gap="large")

    with col_tier:
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:10px;">
    Tier Classification
</div>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div class="nil-card">
    <div style="margin-bottom:10px;">{tier_badge(tier, "lg")}</div>
    <div style="font-size:22px; font-weight:800; color:#0d0d0d;
                letter-spacing:-0.01em; margin-bottom:6px;">{tier}</div>
    <div style="font-size:13px; color:#8b7f72;">
        PVM Score: <b style="color:#0d0d0d;">{pvm:.4f}</b>
    </div>
</div>
""", unsafe_allow_html=True)

    with col_nil:
        st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:10px;">
    NIL Recommendation
</div>
""", unsafe_allow_html=True)
        if eligible:
            range_display = nil_rec.get("range_display", "—")
            estimated     = nil_rec.get("estimated", 0)
            st.markdown(f"""
<div class="nil-card">
    <div style="font-size:11px; font-weight:700; letter-spacing:0.10em;
                text-transform:uppercase; color:#8b7f72; margin-bottom:6px;">
        Estimated Annual Value
    </div>
    <div style="font-size:28px; font-weight:800; color:{color};
                letter-spacing:-0.02em; margin-bottom:6px;">
        ${estimated:,.0f}
    </div>
    <div style="font-size:13px; color:#8b7f72; margin-bottom:12px;">
        Range: {range_display}
    </div>
    <div style="font-size:13px; color:#4a4035; line-height:1.6;">
        {nil_rec.get('description', '')}
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="nil-card" style="border-color:#fecaca;">
    <div style="font-size:14px; font-weight:700; color:#dc2626; margin-bottom:8px;">
        No Recommended NIL Allocation
    </div>
    <div style="font-size:13px; color:#4a4035; line-height:1.6;">
        {nil_rec.get('description', '')}
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Full Report + Download ───────────────
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:10px;">
    Valuation Report
</div>
""", unsafe_allow_html=True)

    report_pdf = generate_pdf_report(result)
    report_txt = generate_txt_report(result)

    with st.expander("View Text Report", expanded=False):
        st.code(report_txt, language=None)

    dl_col1, dl_col2 = st.columns([2, 1], gap="small")
    with dl_col1:
        st.download_button(
            label="Download PDF Report",
            data=report_pdf,
            file_name=f"NIL_Report_{name.replace(' ', '_')}_{position}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with dl_col2:
        st.download_button(
            label=".txt",
            data=report_txt,
            file_name=f"NIL_Report_{name.replace(' ', '_')}_{position}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)