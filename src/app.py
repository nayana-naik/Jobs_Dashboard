"""Interactive dashboard for the Global AI Jobs 2026 dataset."""

import streamlit as st

from data_loader import load_data
from filters import render_sidebar_filters
from tabs import geography, overview, roles, skills

st.set_page_config(page_title="Global AI Jobs 2026", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; }
    section[data-testid="stSidebar"] div[data-testid="stSidebarHeader"] {
        height: 2.5rem;
        min-height: 0;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_data()

st.markdown(
    f"""
    <h1 style="margin-bottom:0.1rem; color:var(--text-color); font-weight:700;">
        Global AI Jobs 2026
    </h1>
    <p style="margin-top:0; margin-bottom:1rem; color:var(--text-color); opacity:0.7; font-size:1rem;">
        Global AI Jobs Explorer 2026 is an interactive visual analytics dashboard that aggregates global AI labor market data. It enables professionals, hiring managers, and career strategists to analyze compensation structures, high-demand skills, geographic distribution, and automation risks across specialized AI job postings.
    </p>
    """,
    unsafe_allow_html=True,
)

filtered = render_sidebar_filters(df)

if filtered.empty:
    st.warning("No jobs match the current filters. Adjust the filters in the sidebar.")
    st.stop()

st.info("AI-powered summaries are automatically generated based on active filters.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview & Trends", "Roles & Compensation", "Skills & Demand", "Geography & Work Style"]
)

with tab1:
    overview.render(filtered)

with tab2:
    roles.render(filtered)

with tab3:
    skills.render(filtered)

with tab4:
    geography.render(filtered)

# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------
st.divider()
with st.expander("View filtered data table"):
    st.dataframe(
        filtered.drop(columns=["Skills_List", "Skills_Filter_List"]).reset_index(drop=True),
        use_container_width=True,
    )
