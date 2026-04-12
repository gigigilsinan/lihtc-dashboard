import plotly.express as px


def create_chart(df):
    chart_df = (
        df.groupby("developer", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .head(10)
        .sort_values("amount", ascending=True)
    )

    fig = px.bar(
        chart_df,
        x="amount",
        y="developer",
        orientation="h",
        title="Top 10 Developers by Funding",
        labels={
            "developer": "Developer",
            "amount": "Funding Amount",
        },
    )

    fig.update_layout(
        xaxis_title="Funding Amount",
        yaxis_title="Developer",
    )

    fig.update_xaxes(tickformat=",.0s")

    return fig