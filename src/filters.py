"""Sidebar filter widgets and dataframe filtering logic."""

import pandas as pd
import streamlit as st


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")

    sal_min, sal_max = int(df["Salary_USD"].min()), int(df["Salary_USD"].max())

    filter_defaults = {
        "filter_job_titles": [],
        "filter_continents": [],
        "filter_industries": [],
        "filter_specializations": [],
        "filter_experience": [],
        "filter_company_size": [],
        "filter_skills_required": [],
        "filter_salary_range": (sal_min, sal_max),
    }

    if st.sidebar.button("Reset Filters"):
        for key, default in filter_defaults.items():
            st.session_state[key] = default
        st.rerun()

    job_titles = st.sidebar.multiselect(
        "Job Title", sorted(df["Job_Title"].unique()), key="filter_job_titles"
    )
    continents = st.sidebar.multiselect(
        "Continent", sorted(df["Continent"].unique()), key="filter_continents"
    )
    industries = st.sidebar.multiselect(
        "Industry", sorted(df["Industry"].unique()), key="filter_industries"
    )
    specializations = st.sidebar.multiselect(
        "AI Specialization", sorted(df["AI_Specialization"].unique()), key="filter_specializations"
    )
    experience = st.sidebar.multiselect(
        "Experience Level", sorted(df["Experience_Level"].unique()), key="filter_experience"
    )
    company_size = st.sidebar.multiselect(
        "Company Size", sorted(df["Company_Size"].unique()), key="filter_company_size"
    )
    skills_required = st.sidebar.multiselect(
        "Skills Required", sorted(df["Skills_Filter_List"].explode().unique()), key="filter_skills_required"
    )
    salary_range = st.sidebar.slider(
        "Salary (USD)", min_value=sal_min, max_value=sal_max,
        value=(sal_min, sal_max), step=5000, format="$%d", key="filter_salary_range",
    )

    filtered = df.copy()
    if job_titles:
        filtered = filtered[filtered["Job_Title"].isin(job_titles)]
    if continents:
        filtered = filtered[filtered["Continent"].isin(continents)]
    if industries:
        filtered = filtered[filtered["Industry"].isin(industries)]
    if specializations:
        filtered = filtered[filtered["AI_Specialization"].isin(specializations)]
    if experience:
        filtered = filtered[filtered["Experience_Level"].isin(experience)]
    if company_size:
        filtered = filtered[filtered["Company_Size"].isin(company_size)]
    if skills_required:
        filtered = filtered[
            filtered["Skills_Filter_List"].apply(lambda skills: any(s in skills for s in skills_required))
        ]
    filtered = filtered[filtered["Salary_USD"].between(*salary_range)]

    st.sidebar.markdown(f"**{len(filtered):,}** of {len(df):,} jobs match")

    return filtered
