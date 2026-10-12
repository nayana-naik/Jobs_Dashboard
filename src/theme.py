"""Shared color palette and Plotly layout styling for the dashboard."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ai_client import get_chart_summary

# ---- Palette (validated categorical theme, fixed order - see dataviz skill) ----
SERIES = {
    "blue": "#2a78d6",
    "orange": "#eb6834",
    "aqua": "#1baf7a",
    "yellow": "#eda100",
    "magenta": "#e87ba4",
    "green": "#008300",
    "violet": "#4a3aa7",
    "red": "#e34948",
}
CATEGORICAL = list(SERIES.values())
SEQUENTIAL_BLUE = ["#cde2fb", "#9ec5f4", "#5598e7", "#2a78d6", "#184f95"]
DIVERGING = ["#2a78d6", "#f0efec", "#e34948"]

SURFACE = "#fcfcfb"
PAGE_PLANE = "#f9f9f7"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

# ---- Base chart template matching the dataviz palette ----
BASE_LAYOUT = dict(
    plot_bgcolor=SURFACE,
    paper_bgcolor=SURFACE,
    font=dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif", color=TEXT_PRIMARY),
    title_font=dict(color=TEXT_PRIMARY, size=16),
    legend=dict(bgcolor=SURFACE, bordercolor=GRIDLINE, borderwidth=1, font=dict(color=TEXT_SECONDARY)),
    margin=dict(t=50, l=10, r=10, b=10),
)
AXIS_STYLE = dict(gridcolor=GRIDLINE, zerolinecolor=BASELINE, linecolor=BASELINE, tickfont=dict(color=MUTED), color=MUTED)


def style(fig: go.Figure) -> go.Figure:
    fig.update_layout(**BASE_LAYOUT)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def top_n_text(series: pd.Series, n: int = 5, fmt: str = "{:,.0f}") -> str:
    """Format the top n entries of a Series as compact "label (value)" text."""
    top = series.sort_values(ascending=False).head(n)
    return ", ".join(f"{idx} ({fmt.format(val)})" for idx, val in top.items())


def render_ai_summary(chart_name: str, data_context: str) -> None:
    """Render a one-line AI-generated summary for the chart that follows."""
    summary = get_chart_summary(chart_name, data_context)
    st.markdown(
        f"""
        <div style="
            border: 1px solid {SERIES['blue']};
            border-radius: 6px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.5rem;
            background-color: {SEQUENTIAL_BLUE[0]};
            color: {TEXT_PRIMARY};
            font-size: 1rem;
        ">
            {summary}
        </div>
        """,
        unsafe_allow_html=True,
    )
