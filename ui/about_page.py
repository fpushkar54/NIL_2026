# ─────────────────────────────────────────────
#  NIL Valuation Engine · About Page
# ─────────────────────────────────────────────

import streamlit as st
from backend.constants import RESEARCH_R2, POSITION_COLORS
from ui.components import page_header


def render_about():
    page_header(
        title="About the Model",
        subtitle="Methodology, research findings, and platform documentation.",
    )

    # ── Section 1: How It Works ──────────────
    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    How It Works
</div>
""", unsafe_allow_html=True)

    steps = [
        ("01", "Player Statistics", "Raw season stats entered for the selected position."),
        ("02", "Normalization", "Each metric is scaled to [0, 1] using position-specific min/max ranges."),
        ("03", "PVM Calculation", "Weighted composite score computed from normalized values."),
        ("04", "Tier Assignment", "Score mapped to one of five performance tiers."),
        ("05", "NIL Recommendation", "Annual NIL valuation range generated based on tier and score position."),
    ]

    cols = st.columns(5, gap="small")
    for i, (num, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
<div style="
    background:#ffffff;
    border:1px solid #e8e4de;
    border-radius:10px;
    padding:20px 16px;
    text-align:center;
    height:100%;
">
    <div style="font-size:22px; font-weight:800; color:#e8e4de;
                margin-bottom:8px; letter-spacing:-0.02em;">{num}</div>
    <div style="font-size:13px; font-weight:700; color:#0d0d0d;
                margin-bottom:6px; line-height:1.3;">{title}</div>
    <div style="font-size:12px; color:#8b7f72; line-height:1.5;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

    # ── Section 2: What You'll Receive ───────
    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    What You'll Receive
</div>
""", unsafe_allow_html=True)

    features = [
        ("PVM Score", "A normalized composite score from 0.000 to 1.000 reflecting overall production relative to position peers."),
        ("Tier Classification", "One of five performance tiers — Elite, High-Level Starter, Starter, Contributor, or Below NIL Threshold — based on PVM score."),
        ("NIL Recommendation", "Annual valuation range and estimated deal value derived from tier placement and score position within that tier."),
        ("Analytics Dashboard", "Interactive Plotly gauge and radar chart visualizing performance across all tracked metrics."),
        ("Downloadable Report", "Structured .txt valuation report including raw stats, normalized values, tier, and NIL recommendation."),
    ]

    col1, col2 = st.columns(2, gap="medium")
    for i, (title, desc) in enumerate(features):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
<div class="nil-card" style="margin-bottom:12px;">
    <div style="font-size:14px; font-weight:700; color:#0d0d0d;
                margin-bottom:6px;">{title}</div>
    <div style="font-size:13px; color:#6b5f52; line-height:1.6;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

    # ── Section 3: Research Findings ─────────
    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    Research Findings
</div>
""", unsafe_allow_html=True)

    r2_cols = st.columns(3, gap="medium")
    positions = ["QB", "RB", "WR"]
    summaries = [
        "Weak relationship between statistical production and NIL valuation.",
        "Weak relationship between statistical production and NIL valuation.",
        "Strongest correlation in the study — receiving production shows meaningful predictive value.",
    ]

    for i, pos in enumerate(positions):
        r2 = RESEARCH_R2[pos]
        color = POSITION_COLORS[pos]
        with r2_cols[i]:
            st.markdown(f"""
<div class="nil-card" style="border-top:3px solid {color}; text-align:center;">
    <div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
                text-transform:uppercase; color:{color}; margin-bottom:10px;">
        {pos}
    </div>
    <div style="font-size:36px; font-weight:800; color:#0d0d0d;
                letter-spacing:-0.03em; margin-bottom:6px;">
        R² = {r2}
    </div>
    <div style="font-size:12px; color:#8b7f72; line-height:1.5;">
        {summaries[i]}
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="nil-card" style="margin-top:16px; background:#f9f7f4;">
    <div style="font-size:13px; font-weight:700; color:#0d0d0d; margin-bottom:10px;">
        Key Takeaway
    </div>
    <div style="font-size:13px; color:#4a4035; line-height:1.7;">
        Across all three positions, statistical production alone is a weak predictor of NIL value.
        School brand equity, recruiting reputation, social media reach, and marketability
        remain dominant drivers of NIL deal size — factors this model intentionally excludes
        to isolate pure on-field performance value.
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Tier Reference ────────────────────────
    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:11px; font-weight:700; letter-spacing:0.12em;
            text-transform:uppercase; color:#8b7f72; margin-bottom:16px;">
    Tier Reference
</div>
""", unsafe_allow_html=True)

    tiers_info = [
        ("Elite",               "0.80 – 1.00", "$500,000 – $2,000,000", "#0d0d0d", "#ffffff"),
        ("High-Level Starter",  "0.70 – 0.79", "$150,000 – $500,000",   "#dbeafe", "#1d4ed8"),
        ("Starter",             "0.60 – 0.69", "$50,000 – $150,000",    "#dcfce7", "#16a34a"),
        ("Contributor",         "0.50 – 0.59", "$10,000 – $50,000",     "#fef3c7", "#d97706"),
        ("Below NIL Threshold", "< 0.50",       "No Allocation",         "#fee2e2", "#dc2626"),
    ]

    for tier_name, score_range, nil_range, bg, tc in tiers_info:
        st.markdown(f"""
<div style="
    display:flex; align-items:center; justify-content:space-between;
    background:#ffffff; border:1px solid #e8e4de; border-radius:8px;
    padding:14px 20px; margin-bottom:8px;
">
    <div style="display:flex; align-items:center; gap:14px;">
        <span style="background:{bg}; color:{tc}; font-size:12px; font-weight:700;
                     padding:4px 10px; border-radius:5px; white-space:nowrap;">
            {tier_name}
        </span>
        <span style="font-size:13px; color:#4a4035;">PVM {score_range}</span>
    </div>
    <span style="font-size:13px; font-weight:600; color:#0d0d0d;">{nil_range}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)
