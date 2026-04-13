from dash import Dash, html, dcc, Input, Output
from util import load_data
import plotly.io as pio
import os

pio.templates.default = "ggplot2"

from components.bar_borough_funding import create_chart as borough_chart
from components.line_funding_trend import create_chart as trend_chart
from components.stacked_construction import create_chart as construction_chart
from components.scatter_funding_vs_units import create_chart as scatter_chart
from components.bar_top_developer_by_borough import create_chart as top_dev_borough_chart
from components.bar_top_developers import create_chart as top_developers_chart
from components.map_borough_funding import create_chart as borough_map_chart
from components.map_project_sites import create_chart as project_map_chart

# load data
df = load_data()

# create app
app = Dash(__name__)
server = app.server

# =========================
# Dropdown options
# =========================
year_options = [{"label": "All", "value": "All"}] + [
    {"label": str(int(y)), "value": int(y)}
    for y in sorted(df["year"].dropna().unique())
]

credit_options = [
    {"label": "All", "value": "All"},
    {"label": "4%", "value": "4%"},
    {"label": "9%", "value": "9%"},
]

construction_options = [{"label": "All", "value": "All"}] + [
    {"label": c, "value": c}
    for c in sorted(df["construction_type"].dropna().unique())
]

# =========================
# Layout
# =========================
app.layout = html.Div([
    html.H1("NYC LIHTC Dashboard"),

    # Filters
    html.Div([
        html.Div([
            html.Label("Select Year"),
            dcc.Dropdown(
                id="year-filter",
                options=year_options,
                value="All",
                clearable=False
            ),
        ], style={"width": "32%", "display": "inline-block"}),

        html.Div([
            html.Label("Select Credit Type"),
            dcc.Dropdown(
                id="credit-filter",
                options=credit_options,
                value="All",
                clearable=False
            ),
        ], style={"width": "32%", "display": "inline-block", "marginLeft": "2%"}),

        html.Div([
            html.Label("Construction Type"),
            dcc.Dropdown(
                id="construction-filter",
                options=construction_options,
                value="All",
                clearable=False
            ),
        ], style={"width": "32%", "display": "inline-block", "marginLeft": "2%"}),
    ], style={"marginBottom": "30px"}),

    # Row 1
    html.Div([
        html.Div([
            dcc.Graph(id="borough-bar-chart")
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            dcc.Graph(id="trend-line-chart")
        ], style={"width": "49%", "display": "inline-block", "marginLeft": "2%", "verticalAlign": "top"}),
    ]),

    # Row 2
    html.Div([
        html.Div([
            dcc.Graph(id="construction-stacked-chart")
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            dcc.Graph(id="scatter-funding-chart")
        ], style={"width": "49%", "display": "inline-block", "marginLeft": "2%", "verticalAlign": "top"}),
    ]),

    # Row 3
    html.Div([
        html.Div([
            dcc.Graph(id="top-developer-borough-chart")
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            dcc.Graph(id="top-developers-chart")
        ], style={"width": "49%", "display": "inline-block", "marginLeft": "2%", "verticalAlign": "top"}),
    ]),

    # Row 4
    html.Div([
        html.Div([
            dcc.Graph(
                id="borough-map-chart",
                config={"scrollZoom": True}
            )
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            dcc.Graph(
                id="project-map-chart",
                config={"scrollZoom": True}
            )
        ], style={"width": "49%", "display": "inline-block", "marginLeft": "2%", "verticalAlign": "top"}),
    ]),
])

# =========================
# Callback
# =========================
@app.callback(
    Output("borough-bar-chart", "figure"),
    Output("trend-line-chart", "figure"),
    Output("construction-stacked-chart", "figure"),
    Output("scatter-funding-chart", "figure"),
    Output("top-developer-borough-chart", "figure"),
    Output("top-developers-chart", "figure"),
    Output("borough-map-chart", "figure"),
    Output("project-map-chart", "figure"),
    Input("year-filter", "value"),
    Input("credit-filter", "value"),
    Input("construction-filter", "value"),
)
def update_charts(selected_year, selected_credit, selected_construction):
    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["year"] == selected_year]

    if selected_credit != "All":
        filtered_df = filtered_df[filtered_df["credit_type"] == selected_credit]

    if selected_construction != "All":
        filtered_df = filtered_df[filtered_df["construction_type"] == selected_construction]

    return (
        borough_chart(filtered_df),
        trend_chart(filtered_df),
        construction_chart(filtered_df),
        scatter_chart(filtered_df),
        top_dev_borough_chart(filtered_df),
        top_developers_chart(filtered_df),
        borough_map_chart(filtered_df),
        project_map_chart(filtered_df),
    )

# =========================
# Run app
# =========================
if __name__ == "__main__":
    app.run(debug=True)