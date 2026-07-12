# ─────────────────────────────────────────────
#  NIL Valuation Engine · Navigation
# ─────────────────────────────────────────────

import streamlit as st


PAGES = {
    "Home":          "home",
    "QB Calculator": "qb",
    "RB Calculator": "rb",
    "WR Calculator": "wr",
    "About":         "about",
}

# Lucide SVG icons (inline, minimal)
ICONS = {
    "Home": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
        <polyline points="9 22 9 12 15 12 15 22"/></svg>""",
    "QB Calculator": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <circle cx="12" cy="12" r="3"/>
        <line x1="12" y1="2" x2="12" y2="5"/>
        <line x1="12" y1="19" x2="12" y2="22"/>
        <line x1="2" y1="12" x2="5" y2="12"/>
        <line x1="19" y1="12" x2="22" y2="12"/></svg>""",
    "RB Calculator": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>""",
    "WR Calculator": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="2"/>
        <path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/></svg>""",
    "About": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="20" x2="18" y2="10"/>
        <line x1="12" y1="20" x2="12" y2="4"/>
        <line x1="6" y1="20" x2="6" y2="14"/></svg>""",
}


def render_sidebar():
    with st.sidebar:
        st.markdown("""
<div style="padding: 20px 0 24px 0;">
    <div style="font-size:13px; font-weight:800; letter-spacing:0.10em;
                text-transform:uppercase; color:#8b7f72; margin-bottom:4px;">
        NIL ENGINE
    </div>
    <div style="font-size:11px; color:#b0a898; letter-spacing:0.04em;">
        v2.0 · 2026
    </div>
</div>
""", unsafe_allow_html=True)

        current = st.session_state.get("page", "home")

        for label, page_key in PAGES.items():
            is_active = current == page_key
            icon_svg  = ICONS.get(label, "")

            accent_map = {"qb": "#0369a1", "rb": "#16a34a", "wr": "#c2410c"}
            accent = accent_map.get(page_key, "#0d0d0d")
            active_bg = f"{accent}12"

            if is_active:
                border_left = f"3px solid {accent}"
                text_color  = accent
                font_weight = "700"
                bg          = active_bg
            else:
                border_left = "3px solid transparent"
                text_color  = "#4a4035"
                font_weight = "500"
                bg          = "transparent"

            st.markdown(f"""
<div style="
    display:flex; align-items:center; gap:10px;
    padding:9px 12px 9px 16px;
    margin-bottom:2px;
    border-radius:8px;
    background:{bg};
    border-left:{border_left};
    color:{text_color};
    font-weight:{font_weight};
    font-size:14px;
    pointer-events:none;
    user-select:none;
">
    <span style="color:{text_color}; display:flex; align-items:center;">{icon_svg}</span>
    {label}
</div>
""", unsafe_allow_html=True)

            if st.button(
    label,
    key=f"nav_{page_key}",
    use_container_width=True
):
                st.session_state.page = page_key
                st.rerun()

        st.markdown("<div style='height:1px; background:#e8e4de; margin:16px 0;'></div>",
                    unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:11px; color:#b0a898; padding:0 4px; line-height:1.6;">
    Performance-Based<br>Athlete Valuation
</div>
""", unsafe_allow_html=True)
