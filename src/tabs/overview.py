"""Overview & Trends tab: top job titles, industries, and regional distribution."""

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import CATEGORICAL, SERIES, SURFACE, render_ai_summary, style, top_n_text


def render(filtered: pd.DataFrame) -> None:
    top_titles = (
        filtered["Job_Title"].value_counts().nlargest(20).sort_values()
    ).reset_index()
    top_titles.columns = ["Job Title", "Count"]
    render_ai_summary("Top 20 Job Titles by Job Count", top_n_text(filtered["Job_Title"].value_counts()))
    fig = px.bar(
        top_titles, x="Count", y="Job Title", orientation="h",
        color_discrete_sequence=[SERIES["yellow"]],
        title="Top 20 Job Titles by Job Count",
    )
    fig.update_traces(marker_color=SERIES["yellow"])
    fig.update_layout(height=600)
    style(fig)
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    top_ind = (
        filtered["Industry"].value_counts().nlargest(12).sort_values()
    ).reset_index()
    top_ind.columns = ["Industry", "Jobs"]
    render_ai_summary("Top 12 Industries by Job Count", top_n_text(filtered["Industry"].value_counts()))
    fig = px.bar(
        top_ind, x="Jobs", y="Industry", orientation="h",
        color_discrete_sequence=[SERIES["aqua"]],
        title="Top 12 Industries by Job Count",
    )
    fig.update_traces(marker_color=SERIES["aqua"])
    style(fig)
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    counts = filtered["Continent"].value_counts().reset_index()
    counts.columns = ["Continent", "Jobs"]
    render_ai_summary("Jobs by Continent", top_n_text(counts.set_index("Continent")["Jobs"]))
    fig = px.pie(
        counts, names="Continent", values="Jobs", hole=0.45,
        color_discrete_sequence=CATEGORICAL,
        title="Jobs by Continent",
    )
    fig.update_traces(
        textinfo="percent+label",
        marker=dict(line=dict(color=SURFACE, width=2)),
    )
    style(fig)
    st.plotly_chart(fig, use_container_width=True)
