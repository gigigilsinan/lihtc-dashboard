import plotly.express as px


def create_chart(df):
    # remove rows with missing values
    chart_df = df.dropna(subset=["total_units", "amount"]).copy()

    # optional: remove zero or negative values (cleaner chart)
    chart_df = chart_df[
        (chart_df["total_units"] > 0) &
        (chart_df["amount"] > 0)
    ]

    # color mapping
    color_map = {
        "4%": "#F8766D",   # ggplot salmon
        "9%": "#A3A500",   # ggplot olive green
    }

    fig = px.scatter(
        chart_df,
        x="total_units",
        y="amount",
        color="credit_type",
        color_discrete_map=color_map,
        title="Funding Amount vs Total Units (Project Level)",
        labels={
            "total_units": "Total Units",
            "amount": "Funding Amount",
            "credit_type": "Credit Type",
        },
        hover_name="project_name",
        hover_data={
            "developer": True,
            "borough": True,
            "year": True,
            "amount": ":,.0f",
            "total_units": True,
        },
    )

    fig.update_layout(
        xaxis_title="Total Units",
        yaxis_title="Funding Amount",
        legend_title="Credit Type",
    )

    fig.update_yaxes(tickformat=",.0s")

    return fig