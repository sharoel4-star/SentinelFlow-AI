from __future__ import annotations

import streamlit as st


def render_coming_soon(page_name: str, description: str) -> None:
    st.markdown(f"### {page_name}")
    st.info(description)
