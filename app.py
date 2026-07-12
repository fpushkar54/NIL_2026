# ─────────────────────────────────────────────
#  NIL Valuation Engine · app.py
#  Entrypoint — routing, session state, styles
# ─────────────────────────────────────────────

import streamlit as st

# ── Page config (must be first Streamlit call) ──
st.set_page_config(
    page_title="NIL Valuation Engine",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ───────────────────────────────────
from ui.styles    import load_styles
from ui.navigation import render_sidebar
from ui.home       import render_home
from ui.qb_page    import render_qb
from ui.rb_page    import render_rb
from ui.wr_page    import render_wr
from ui.results_page import render_results
from ui.about_page import render_about


# ── Session state defaults ────────────────────
def init_session_state():
    defaults = {
        "page":   "home",
        "result": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ── Router ─────────────────────────────────────
ROUTES = {
    "home":    render_home,
    "qb":      render_qb,
    "rb":      render_rb,
    "wr":      render_wr,
    "results": render_results,
    "about":   render_about,
}


def main():
    init_session_state()
    load_styles()
    render_sidebar()

    page_key = st.session_state.get("page", "home")
    render_fn = ROUTES.get(page_key, render_home)

    with st.container():
        render_fn()


if __name__ == "__main__":
    main()
