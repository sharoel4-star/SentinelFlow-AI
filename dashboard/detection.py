from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

import dashboard._bootstrap  # noqa: F401
from dashboard.csv_utils import (
    normalize_column_names,
    row_to_flow_features,
    validate_feature_columns,
)
from predictor import predict_flow, selected_features


def render_detection() -> None:
    st.markdown("### Flow Detection")
    st.caption(
        "Upload a CSV with the 65 CIC-IDS2017 flow features. "
        "The Label column is optional and is not used for inference."
    )

    uploaded = st.file_uploader(
        "CIC-IDS2017-compatible CSV",
        type=["csv"],
        help="Processed or raw-style flow CSVs that include the required feature columns.",
    )

    if uploaded is None:
        st.warning("Upload a CSV file to begin flow analysis.")
        return

    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:  # noqa: BLE001 — show user-facing parse error in UI
        st.error(f"Could not read CSV: {exc}")
        return

    df = normalize_column_names(df)
    present, missing = validate_feature_columns(df)

    if missing:
        st.error(
            f"CSV is missing **{len(missing)}** required feature column(s). "
            "Prediction cannot run until all features are present."
        )
        with st.expander("Missing feature columns"):
            st.code("\n".join(missing))
        st.success(f"Found {len(present)} / {len(selected_features)} required features.")
        return

    st.success(f"All {len(selected_features)} required feature columns are present.")
    extra_cols = [c for c in df.columns if c not in selected_features]
    if extra_cols:
        label_note = " (including Label)" if "Label" in extra_cols else ""
        st.caption(
            f"Additional columns detected{label_note}: {len(extra_cols)} — "
            "only the 65 selected features are sent to the model."
        )

    st.dataframe(df[selected_features].head(10), use_container_width=True)

    row_count = len(df)
    row_index = st.number_input(
        "Select flow row index",
        min_value=0,
        max_value=max(0, row_count - 1),
        value=0,
        step=1,
        help="Zero-based index into the uploaded file.",
    )

    if st.button("Run detection on selected flow", type="primary"):
        row = df.iloc[int(row_index)]
        flow_features = row_to_flow_features(row)
        result = predict_flow(flow_features)
        _render_prediction_result(result, row_index=int(row_index))

        if "Label" in df.columns:
            st.caption(f"Ground-truth Label in file (not used by model): `{row['Label']}`")


def _render_prediction_result(result: dict[str, Any], *, row_index: int) -> None:
    status = result.get("status")

    if status == "error":
        st.markdown(
            f'<div class="sf-card sf-result-error"><div class="sf-card-label">'
            f"Row {row_index} — Validation Error</div></div>",
            unsafe_allow_html=True,
        )
        if result.get("message"):
            st.warning(result["message"])
        if result.get("missing_features"):
            st.error("Missing features")
            st.code("\n".join(result["missing_features"]))
        if result.get("invalid_features"):
            st.error("Invalid feature values (non-numeric, NaN, infinity, or boolean)")
            st.code("\n".join(result["invalid_features"]))
        return

    if status == "BENIGN":
        st.markdown(
            f"""
            <div class="sf-card sf-result-benign">
                <div class="sf-card-label">Row {row_index} — Verdict</div>
                <div class="sf-card-value sf-status-ok">BENIGN</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric("Attack detected", "No")
        return

    if status == "ATTACK":
        attack_type = result.get("attack_type") or "Unknown"
        st.markdown(
            f"""
            <div class="sf-card sf-result-attack">
                <div class="sf-card-label">Row {row_index} — Verdict</div>
                <div class="sf-card-value" style="color:#f85149;">ATTACK</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric("Attack detected", "Yes")
        st.metric("Predicted attack type", attack_type)
        return

    st.warning(f"Unexpected prediction response: {result}")
