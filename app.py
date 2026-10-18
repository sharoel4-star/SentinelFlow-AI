"""
SentinelFlow AI — SOC Dashboard (Streamlit)

Run from project root:
    .\\.venv\\Scripts\\python.exe -m streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dashboard.config import APP_SUBTITLE, APP_TITLE, NAV_PAGES  # noqa: E402
from dashboard.detection import render_detection  # noqa: E402
from dashboard.overview import render_overview  # noqa: E402
from dashboard.placeholders import render_coming_soon  # noqa: E402
from dashboard.styles import apply_soc_theme  # noqa: E402

# Import loads trained models once per Streamlit server process.
import predictor  # noqa: F401, E402


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_soc_theme()

    with st.sidebar:
        st.markdown(f"## {APP_TITLE}")
        st.caption(APP_SUBTITLE)
        st.divider()
        page = st.radio(
            "Navigation",
            NAV_PAGES,
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("Models loaded from `models/` via `src.predictor`.")

    if page == "Overview":
        render_overview()
    elif page == "Traffic Analysis":
        render_coming_soon(
            "Traffic Analysis",
            "Upcoming: aggregate traffic statistics, flow distributions, and timeline "
            "views from uploaded or ingested datasets. No live traffic in this version.",
        )
    elif page == "Detection":
        render_detection()
    elif page == "Alerts":
        render_coming_soon(
            "Alerts",
            "Upcoming: alert queue, severity triage, and analyst workflow. "
            "This version does not generate synthetic or live alerts.",
        )
    elif page == "Model Insights":
        render_coming_soon(
            "Model Insights",
            "Upcoming: explainability (feature importance / SHAP), model metrics, "
            "and class coverage from training artifacts.",
        )
    else:
        render_overview()


if __name__ == "__main__":
    main()
