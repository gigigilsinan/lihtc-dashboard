import plotly.express as px


def create_chart(df):
    chart_df = (
        df.groupby(["year", "credit_type"], as_index=False)["amount"]
        .sum()
        .sort_values("year")
    )

    fig = px.line(
        chart_df,
        x="year",
        y="amount",
        color="credit_type",
        markers=True,
        title="Funding Over Time",
        labels={
            "year": "Year",
            "amount": "Funding Amount",
            "credit_type": "LIHTC Type",
        },
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Funding Amount",
        legend_title="LIHTC Type",
    )

    return fig