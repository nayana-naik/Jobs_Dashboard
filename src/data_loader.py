"""Dataset loading and skill-list preprocessing for the dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "global_ai_jobs_2026_cleaned.csv"

CLOUD_SKILL_SPLITS = {
    "AWS/GCP": ["AWS", "GCP"],
    "AWS/GCP/Azure": ["AWS", "GCP", "Azure"],
}


def expand_cloud_skills(skills: list[str]) -> list[str]:
    expanded = []
    for skill in skills:
        expanded.extend(CLOUD_SKILL_SPLITS.get(skill, [skill]))
    return expanded


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, parse_dates=["Posted_Date", "Application_Deadline"])
    df["Skills_List"] = df["Skills_Required"].str.split(", ")
    df["Skills_Filter_List"] = df["Skills_List"].apply(expand_cloud_skills)
    return df
