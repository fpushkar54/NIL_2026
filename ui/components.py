# ─────────────────────────────────────────────
#  NIL Valuation Engine · Shared Components
# ─────────────────────────────────────────────

import plotly.graph_objects as go
import streamlit as st
from backend.constants import POSITION_COLORS
from backend.tiers import get_tier_badge_style


# ── Page header ──────────────────────────────
def page_header(title: str, subtitle: str, position: str = None):
    accent = POSITION_COLORS.get(position, "#0d0d0d") if position else "#0d0d0d"
    st.markdown(f"""
<div style="margin-bottom:28px;">
    <div style="font-size:11px; font-weight:700; letter-spacing:0.14em;
                text-transform:uppercase; color:{accent}; margin-bottom:6px;">
        {position + ' CALCULATOR' if position else 'NIL ENGINE'}
    </div>
    <h1 style="font-size:28px; font-weight:800; color:#0d0d0d;
               margin:0 0 6px 0; letter-spacing:-0.02em; line-height:1.2;">
        {title}
    </h1>
    <p style="font-size:15px; color:#6b5f52; margin:0; font-weight:400;">
        {subtitle}
    </p>
</div>
""", unsafe_allow_html=True)


# ── Tier badge ────────────────────────────────
def tier_badge(tier: str, size: str = "md") -> str:
    style = get_tier_badge_style(tier)
    fs = "13px" if size == "md" else "11px"
    return (
        f'<span style="display:inline-block; background:{style["bg"]}; '
        f'color:{style["text"]}; font-size:{fs}; font-weight:700; '
        f'letter-spacing:0.04em; padding:4px 10px; border-radius:6px;">'
        f'{tier}</span>'
    )


# ── Plotly Gauge ─────────────────────────────
def pvm_gauge(pvm_score: float, tier: str, position: str) -> go.Figure:
    accent = POSITION_COLORS.get(position, "#0d0d0d")
    tier_styles = get_tier_badge_style(tier)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pvm_score * 100,
        number={
            "suffix": "",
            "font": {"size": 36, "family": "Outfit", "color": "#0d0d0d"},
            "valueformat": ".1f",
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#d0c8be",
                "tickfont": {"size": 11, "family": "Outfit", "color": "#8b7f72"},
                "tickvals": [0, 25, 50, 60, 70, 80, 100],
            },
            "bar": {"color": accent, "thickness": 0.28},
            "bgcolor": "#f4f2ee",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  50], "color": "#fee2e2"},
                {"range": [50, 60], "color": "#fef3c7"},
                {"range": [60, 70], "color": "#dcfce7"},
                {"range": [70, 80], "color": "#dbeafe"},
                {"range": [80, 100],"color": "#e0e7ff"},
            ],
            "threshold": {
                "line": {"color": accent, "width": 3},
                "thickness": 0.82,
                "value": pvm_score * 100,
            },
        },
        title={
            "text": f"<b>PVM Score</b><br><span style='font-size:13px;color:#8b7f72;'>{tier}</span>",
            "font": {"size": 15, "family": "Outfit", "color": "#0d0d0d"},
        },
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=10, l=20, r=20),
        height=260,
        font={"family": "Outfit"},
    )
    return fig


# ── Radar Chart ──────────────────────────────
def radar_chart(normalized: dict, position: str) -> go.Figure:
    accent = POSITION_COLORS.get(position, "#0d0d0d")

    label_map = {
        # QB
        "passing_yards":  "Pass Yards",
        "passing_tds":    "Pass TDs",
        "completion_pct": "Comp %",
        "int_pct":        "Ball Security",
        # RB
        "rushing_yards":  "Rush Yards",
        "rushing_tds":    "Rush TDs",
        "ypc":            "YPC",
        # WR
        "receptions":      "Receptions",
        "receiving_yards": "Rec Yards",
        "receiving_tds":   "Rec TDs",
        "ypr":             "YPR",
    }

    keys   = list(normalized.keys())
    values = [normalized[k] for k in keys]
    labels = [label_map.get(k, k) for k in keys]

    # close the shape
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]
    fig = go.Figure()

    # convert hex color to rgba
    r = int(accent[1:3], 16)
    g = int(accent[3:5], 16)
    b = int(accent[5:7], 16)

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor=f"rgba({r},{g},{b},0.15)",
        line=dict(color=accent, width=2),
        name=position,
        hovertemplate="%{theta}: %{r:.3f}<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0.25, 0.5, 0.75, 1.0],
                tickfont=dict(size=9, color="#8b7f72"),
                gridcolor="#e8e4de",
                linecolor="#e8e4de",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family="Outfit", color="#0d0d0d"),
                gridcolor="#e8e4de",
                linecolor="#e8e4de",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=30, l=40, r=40),
        height=300,
        font={"family": "Outfit"},
        showlegend=False,
    )
    return fig


# ── Stat display row ─────────────────────────
def stat_row(label: str, raw_value, norm_value: float, position: str):
    accent = POSITION_COLORS.get(position, "#0d0d0d")
    pct    = norm_value * 100
    bar_w  = max(2, int(pct))

    st.markdown(f"""
<div style="margin-bottom:14px;">
    <div style="display:flex; justify-content:space-between; align-items:center;
                margin-bottom:5px;">
        <span style="font-size:13px; font-weight:500; color:#4a4035;">{label}</span>
        <span style="font-size:13px; font-weight:700; color:#0d0d0d;">{raw_value}</span>
    </div>
    <div style="background:#e8e4de; border-radius:4px; height:5px; overflow:hidden;">
        <div style="background:{accent}; height:5px; width:{bar_w}%;
                    border-radius:4px; transition:width 0.4s ease;"></div>
    </div>
    <div style="font-size:11px; color:#8b7f72; margin-top:3px;">
        Normalized: {norm_value:.3f}
    </div>
</div>
""", unsafe_allow_html=True)
