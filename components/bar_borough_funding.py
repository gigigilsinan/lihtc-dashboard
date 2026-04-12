import plotly.express as px

def create_chart(df):
    chart_df = (
        df.groupby(["borough", "credit_type"], as_index=False)["amount"]
        .sum()
    )

    # Order boroughs by total funding (highest to lowest)
    order = (
        chart_df.groupby("borough")["amount"]
        .sum()
        .sort_values(ascending=False)
        .index
    )

    fig = px.bar(
        chart_df,
        x="borough",
        y="amount",
        color="credit_type",
        barmode="group",
        category_orders={"borough": list(order)},
        title="Funding by Borough",
        labels={
            "borough": "Borough",
            "amount": "Funding Amount",
            "credit_type": "Credit Type",
        },
    )

    fig.update_layout(
        xaxis_title="Borough",
        yaxis_title="Funding Amount",
        legend_title="Credit Type",
    )

    fig.update_yaxes(tickformat=",.0s")

    return fig
