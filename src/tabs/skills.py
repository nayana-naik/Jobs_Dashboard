"""Skills & Demand tab: top skills and skill premium analyzer."""

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import SERIES, render_ai_summary, style, top_n_text


def render(filtered: pd.DataFrame) -> None:
    top_skills = (
        filtered["Skills_Filter_List"].explode().value_counts().nlargest(20).sort_values()
    ).reset_index()
    top_skills.columns = ["Skill", "Count"]
    render_ai_summary("Top 20 Skills Required", top_n_text(filtered["Skills_Filter_List"].explode().value_counts()))
    fig = px.bar(
        top_skills, x="Count", y="Skill", orientation="h",
        color_discrete_sequence=[SERIES["magenta"]],
        title="Top 20 Skills Required",
    )
    fig.update_traces(marker_color=SERIES["magenta"], hovertemplate="%{y}: %{x} jobs<extra></extra>")
    fig.update_layout(height=600)
    style(fig)
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Skill Premium Analyzer")
    all_skills = sorted(filtered["Skills_Filter_List"].explode().dropna().unique())
    if all_skills:
        selected_skill = st.selectbox("Select a skill", all_skills, key="skill_premium_select")
        has_skill = filtered["Skills_Filter_List"].apply(lambda skills: selected_skill in skills)
        with_skill = filtered[has_skill]
        without_skill = filtered[~has_skill]

        if with_skill.empty or without_skill.empty:
            st.info(f"Not enough data to compare jobs with vs. without '{selected_skill}' under the current filters.")
        else:
            median_with = with_skill["Salary_USD"].median()
            median_without = without_skill["Salary_USD"].median()
            premium_pct = (median_with - median_without) / median_without * 100
            st.metric(
                f"Median Salary Premium for '{selected_skill}'",
                f"${median_with:,.0f}",
                f"{premium_pct:+.1f}% vs. ${median_without:,.0f} without",
            )

            by_industry = (
                with_skill.groupby("Industry")["Salary_USD"]
                .median().sort_values().reset_index()
            )
            by_industry.columns = ["Industry", "Median Salary"]
            render_ai_summary(
                f"Median Salary by Industry for Jobs Requiring '{selected_skill}'",
                f"With '{selected_skill}': median ${median_with:,.0f} ({premium_pct:+.1f}% vs. "
                f"${median_without:,.0f} without). " + top_n_text(by_industry.set_index("Industry")["Median Salary"], n=3, fmt="${:,.0f}"),
            )
            fig = px.bar(
                by_industry, x="Median Salary", y="Industry", orientation="h",
                color_discrete_sequence=[SERIES["orange"]],
                title=f"Median Salary by Industry for Jobs Requiring '{selected_skill}'",
            )
            fig.update_traces(marker_color=SERIES["orange"], hovertemplate="%{y}: $%{x:,.0f}<extra></extra>")
            style(fig)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skills available under the current filters.")
