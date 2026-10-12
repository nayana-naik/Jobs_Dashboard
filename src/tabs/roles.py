"""Roles & Compensation tab: salary heatmap, experience mix, and salary distribution."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from theme import CATEGORICAL, MUTED, SEQUENTIAL_BLUE, SERIES, SURFACE, render_ai_summary, style, top_n_text


def render(filtered: pd.DataFrame) -> None:
    st.subheader("Average Salary: Industry × AI Specialization")
    pivot = (
        filtered.pivot_table(
            index="Industry", columns="AI_Specialization", values="Salary_USD", aggfunc="median"
        )
    )
    pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]
    render_ai_summary(
        "Average Salary: Industry × AI Specialization",
        top_n_text(pivot.mean(axis=1), n=3, fmt="${:,.0f}"),
    )
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=SEQUENTIAL_BLUE,
            colorbar=dict(title="Median Salary", outlinewidth=0, tickfont=dict(color=MUTED)),
            hovertemplate="Industry: %{y}<br>Specialization: %{x}<br>Median Salary: $%{z:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(height=600)
    style(fig)
    st.plotly_chart(fig, use_container_width=True)

    counts = filtered["Experience_Level"].value_counts().reindex(
        ["Entry Level", "Mid Level", "Senior Level", "Lead Level", "Executive"]
    ).dropna().reset_index()
    counts.columns = ["Experience_Level", "Jobs"]
    render_ai_summary("Experience Level Mix", top_n_text(counts.set_index("Experience_Level")["Jobs"]))
    fig = px.pie(
        counts, names="Experience_Level", values="Jobs", hole=0.45,
        color_discrete_sequence=CATEGORICAL,
        title="Experience Level Mix",
    )
    fig.update_traces(
        textinfo="percent+label",
        marker=dict(line=dict(color=SURFACE, width=2)),
    )
    style(fig)
    st.plotly_chart(fig, use_container_width=True)

    order = ["Entry Level", "Mid Level", "Senior Level", "Lead Level", "Executive"]
    render_ai_summary(
        "Salary Distribution by Experience Level",
        top_n_text(filtered.groupby("Experience_Level")["Salary_USD"].median(), fmt="${:,.0f}"),
    )
    fig = px.histogram(
        filtered, x="Salary_USD", color="Experience_Level",
        category_orders={"Experience_Level": order},
        color_discrete_sequence=CATEGORICAL,
        barmode="stack",
        histnorm="percent",
        title="Salary Distribution by Experience Level",
        labels={"Salary_USD": "Salary (USD)", "percent": "Share of Jobs", "Experience_Level": ""},
    )
    fig.update_layout(bargap=0.1, bargroupgap=0.05, yaxis_title="Share of Jobs (%)")
    style(fig)
    st.plotly_chart(fig, use_container_width=True)
