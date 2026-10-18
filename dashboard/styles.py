from __future__ import annotations

import streamlit as st


def apply_soc_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --sf-bg: #0b0f14;
            --sf-panel: #121a24;
            --sf-border: #1e2a3a;
            --sf-text: #e6edf3;
            --sf-muted: #8b949e;
            --sf-accent: #3fb950;
            --sf-warn: #d29922;
            --sf-danger: #f85149;
            --sf-info: #58a6ff;
        }

        .stApp {
            background: linear-gradient(180deg, #070a0f 0%, var(--sf-bg) 40%, #0b0f14 100%);
            color: var(--sf-text);
        }

        [data-testid="stSidebar"] {
            background-color: #0a1018;
            border-right: 1px solid var(--sf-border);
        }

        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown p {
            color: var(--sf-text);
        }

        .sf-header-title {
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: var(--sf-text);
            margin-bottom: 0.15rem;
        }

        .sf-header-subtitle {
            font-size: 1rem;
            color: var(--sf-muted);
            margin-bottom: 1.5rem;
        }

        .sf-card {
            background: var(--sf-panel);
            border: 1px solid var(--sf-border);
            border-radius: 10px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.75rem;
        }

        .sf-card-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--sf-muted);
            margin-bottom: 0.35rem;
        }

        .sf-card-value {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--sf-text);
        }

        .sf-status-ok {
            color: var(--sf-accent);
        }

        .sf-pipeline {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.5rem;
            margin: 1rem 0 0.5rem 0;
        }

        .sf-pipeline-step {
            background: #162032;
            border: 1px solid var(--sf-border);
            border-radius: 999px;
            padding: 0.45rem 0.9rem;
            font-size: 0.88rem;
            color: var(--sf-text);
        }

        .sf-pipeline-arrow {
            color: var(--sf-info);
            font-weight: 700;
        }

        .sf-result-benign {
            border-left: 4px solid var(--sf-accent);
        }

        .sf-result-attack {
            border-left: 4px solid var(--sf-danger);
        }

        .sf-result-error {
            border-left: 4px solid var(--sf-warn);
        }

        div[data-testid="stMetricValue"] {
            color: var(--sf-text);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
