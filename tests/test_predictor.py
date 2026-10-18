"""Manual verification script for predict_flow() on processed CIC-IDS2017 data."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from predictor import predict_flow, selected_features  # noqa: E402


def _row_to_feature_dict(row: pd.Series) -> dict:
    return {name: row[name] for name in selected_features}


def _find_flow_example(*, benign: bool) -> tuple[pd.Series, str]:
    processed_files = sorted(PROCESSED_DIR.glob("*.csv"))
    if not processed_files:
        raise FileNotFoundError(f"No processed CSV files found in {PROCESSED_DIR}")

    usecols = selected_features + ["Label"]
    for csv_path in processed_files:
        for chunk in pd.read_csv(csv_path, usecols=usecols, chunksize=50_000):
            if benign:
                matches = chunk[chunk["Label"] == "BENIGN"]
            else:
                matches = chunk[chunk["Label"] != "BENIGN"]
            if matches.empty:
                continue
            row = matches.iloc[0]
            source = f"{csv_path.name} (row label={row['Label']!r})"
            return row, source

    kind = "BENIGN" if benign else "ATTACK"
    raise RuntimeError(f"Could not find a {kind} flow in {PROCESSED_DIR}")


def _print_case(title: str, actual_label: str, result: dict) -> None:
    print(f"\n=== {title} ===")
    print(f"Actual label:     {actual_label}")
    print(f"Prediction result: {result}")


def main() -> None:
    print("SentinelFlow AI — predict_flow() verification")
    print(f"Project root:     {PROJECT_ROOT}")
    print(f"Processed data:   {PROCESSED_DIR}")
    print(f"Selected features: {len(selected_features)}")

    benign_row, benign_source = _find_flow_example(benign=True)
    attack_row, attack_source = _find_flow_example(benign=False)

    benign_features = _row_to_feature_dict(benign_row)
    attack_features = _row_to_feature_dict(attack_row)

    benign_result = predict_flow(benign_features)
    attack_result = predict_flow(attack_features)

    _print_case(f"BENIGN flow ({benign_source})", "BENIGN", benign_result)
    _print_case(
        f"ATTACK flow ({attack_source})",
        str(attack_row["Label"]),
        attack_result,
    )

    missing_key = selected_features[0]
    missing_features = dict(benign_features)
    del missing_features[missing_key]
    missing_result = predict_flow(missing_features)
    _print_case(
        f"Validation — missing feature ({missing_key!r})",
        "N/A (validation test)",
        missing_result,
    )

    invalid_features = dict(benign_features)
    invalid_field = selected_features[1]
    invalid_features[invalid_field] = "not-a-number"
    invalid_result = predict_flow(invalid_features)
    _print_case(
        f"Validation — invalid value ({invalid_field!r} = 'not-a-number')",
        "N/A (validation test)",
        invalid_result,
    )

    print("\n--- Done ---")


if __name__ == "__main__":
    main()
