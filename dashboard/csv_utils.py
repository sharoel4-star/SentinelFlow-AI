from __future__ import annotations

from typing import Any

import pandas as pd

import dashboard._bootstrap  # noqa: F401
from predictor import selected_features


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.copy()
    renamed.columns = [str(col).strip() for col in renamed.columns]
    return renamed


def validate_feature_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return (present_features, missing_features) in training order."""
    columns = set(df.columns)
    missing = [name for name in selected_features if name not in columns]
    present = [name for name in selected_features if name in columns]
    return present, missing


def row_to_flow_features(row: pd.Series) -> dict[str, Any]:
    return {name: row[name] for name in selected_features}
