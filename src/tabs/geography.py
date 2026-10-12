"""Geography & Work Style tab: top countries and remote work by industry."""

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import SERIES, render_ai_summary, style, top_n_text


def render(filtered: pd.DataFrame) -> None:
    top_countries = (
        filtered["Country"].value_counts().nlargest(15).sort_values()
    ).reset_index()
    top_countries.columns = ["Country", "Jobs"]
    render_ai_summary("Top 15 Countries by Job Count", top_n_text(filtered["Country"].value_counts()))
    fig = px.bar(
        top_countries, x="Jobs", y="Country", orientation="h",
        color_discrete_sequence=[SERIES["violet"]],
        title="Top 15 Countries by Job Count",
    )
    fig.update_traces(marker_color=SERIES["violet"])
    fig.update_layout(height=600)
    style(fig)
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    remote_by_ind = (
        filtered.groupby("Industry")["Remote_Work_%"].mean().sort_values().reset_index()
    )
    remote_by_ind.columns = ["Industry", "Avg Remote Work %"]
    render_ai_summary(
        "Avg Remote Work % by Industry",
        top_n_text(remote_by_ind.set_index("Industry")["Avg Remote Work %"], n=3, fmt="{:.0f}%"),
    )
    fig = px.bar(
        remote_by_ind, x="Avg Remote Work %", y="Industry", orientation="h",
        color_discrete_sequence=[SERIES["green"]],
        title="Avg Remote Work % by Industry",
    )
    fig.update_traces(marker_color=SERIES["green"], hovertemplate="%{y}: %{x:.0f}%<extra></extra>")
    fig.update_layout(height=600)
    style(fig)
    st.plotly_chart(fig, use_container_width=True)
