import plotly.express as px


def create_chart(df):
    chart_df = (
        df.groupby(["borough", "construction_type"], as_index=False)["amount"]
        .sum()
    )

    fig = px.bar(
        chart_df,
        x="borough",
        y="amount",
        color="construction_type",
        barmode="stack",
        title="New Construction vs Rehabilitation by Borough",
        labels={
            "borough": "Borough",
            "amount": "Funding Amount",
            "construction_type": "Construction Type",
        },
    )

    fig.update_layout(
        xaxis_title="Borough",
        yaxis_title="Funding Amount",
        legend_title="Construction Type",
    )

    return fig