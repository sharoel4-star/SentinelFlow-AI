from __future__ import annotations

import math
from numbers import Real
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

stage1_model = joblib.load(MODELS_DIR / "stage1_binary_random_forest.joblib")
stage2_model = joblib.load(MODELS_DIR / "stage2_attack_classifier_random_forest.joblib")
selected_features: list[str] = joblib.load(MODELS_DIR / "selected_features.joblib")
model_metadata: dict[str, Any] = joblib.load(MODELS_DIR / "model_metadata.joblib")

_ATTACK_CLASS_INDEX = 1


def _error_result(
    *,
    missing_features: list[str] | None = None,
    invalid_features: list[str] | None = None,
    message: str | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "status": "error",
        "is_attack": None,
        "attack_type": None,
    }
    if missing_features:
        out["missing_features"] = missing_features
    if invalid_features:
        out["invalid_features"] = invalid_features
    if message:
        out["message"] = message
    return out


def _coerce_finite_float(value: Any) -> float:
    if isinstance(value, bool):
        raise TypeError("boolean is not a valid feature value")
    if isinstance(value, Real):
        number = float(value)
    elif isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("empty string")
        number = float(stripped)
    else:
        raise TypeError(f"unsupported type: {type(value).__name__}")
    if not math.isfinite(number):
        raise ValueError("non-finite number")
    return number


def _build_feature_row(
    flow_features: dict[str, Any],
) -> tuple[list[float] | None, dict[str, Any] | None]:
    if not isinstance(flow_features, dict):
        return None, _error_result(message="flow_features must be a dictionary")

    missing = [name for name in selected_features if name not in flow_features]
    if missing:
        return None, _error_result(missing_features=missing)

    row: list[float] = []
    invalid: list[str] = []
    for name in selected_features:
        try:
            row.append(_coerce_finite_float(flow_features[name]))
        except (TypeError, ValueError):
            invalid.append(name)

    if invalid:
        return None, _error_result(invalid_features=invalid)

    return row, None


def predict_flow(flow_features: dict[str, Any]) -> dict[str, Any]:
    """
    Run SentinelFlow two-stage inference on one CIC-IDS2017 flow feature dict.

    Returns a dict with keys: status, is_attack, attack_type.
    """
    row, error = _build_feature_row(flow_features)
    if error is not None:
        return error

    X = pd.DataFrame([row], columns=selected_features)

    stage1_pred = int(stage1_model.predict(X)[0])
    is_attack = stage1_pred == _ATTACK_CLASS_INDEX

    if not is_attack:
        return {
            "status": "BENIGN",
            "is_attack": False,
            "attack_type": None,
        }

    attack_type = str(stage2_model.predict(X)[0])
    return {
        "status": "ATTACK",
        "is_attack": True,
        "attack_type": attack_type,
    }


if __name__ == "__main__":
    print("SentinelFlow AI models loaded successfully.")
    print(f"Features: {len(selected_features)}")
    print(f"Attack classes: {len(stage2_model.classes_)}")
