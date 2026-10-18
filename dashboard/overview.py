from __future__ import annotations

import streamlit as st

import dashboard._bootstrap  # noqa: F401
from dashboard.config import APP_SUBTITLE, APP_TITLE, PIPELINE_STEPS
from predictor import model_metadata, selected_features, stage2_model


def render_overview() -> None:
    st.markdown(f'<div class="sf-header-title">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sf-header-subtitle">{APP_SUBTITLE}</div>',
        unsafe_allow_html=True,
    )

    stage1 = model_metadata["stage1"]
    attack_class_count = len(model_metadata["stage2"]["classes"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _metric_card("System Status", "Operational", status_ok=True)
    with col2:
        _metric_card("Stage 1 Model", "Binary Intrusion Detection")
    with col3:
        _metric_card("Stage 2 Model", f"{attack_class_count} Attack Types")
    with col4:
        _metric_card("Required Features", str(len(selected_features)))

    st.markdown("#### Detection pipeline")
    pipeline_html = _pipeline_html(PIPELINE_STEPS)
    st.markdown(pipeline_html, unsafe_allow_html=True)

    with st.expander("Model details"):
        st.write(f"**Project:** {model_metadata.get('project', 'SentinelFlow AI')}")
        st.write(f"**Dataset:** {model_metadata.get('dataset', 'CIC-IDS2017')}")
        st.write(f"**Stage 1:** {stage1.get('task')} ({stage1.get('model')})")
        st.write(
            f"**Stage 1 labels:** "
            f"{stage1.get('labels', {}).get(0, 'BENIGN')} / "
            f"{stage1.get('labels', {}).get(1, 'ATTACK')}"
        )
        st.write(f"**Stage 2:** {model_metadata['stage2'].get('task')}")
        st.write(f"**Stage 2 classifier classes loaded:** {len(stage2_model.classes_)}")

    st.info(
        "Upload a CIC-IDS2017-compatible flow CSV on the **Detection** page to analyze "
        "individual network flows. Live packet capture is not enabled in this version."
    )


def _metric_card(label: str, value: str, *, status_ok: bool = False) -> None:
    value_class = "sf-card-value sf-status-ok" if status_ok else "sf-card-value"
    st.markdown(
        f"""
        <div class="sf-card">
            <div class="sf-card-label">{label}</div>
            <div class="{value_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _pipeline_html(steps: list[str]) -> str:
    parts: list[str] = ['<div class="sf-pipeline">']
    for index, step in enumerate(steps):
        if index > 0:
            parts.append('<span class="sf-pipeline-arrow">→</span>')
        parts.append(f'<span class="sf-pipeline-step">{step}</span>')
    parts.append("</div>")
    return "".join(parts)
