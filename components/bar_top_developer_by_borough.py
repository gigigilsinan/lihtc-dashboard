import plotly.express as px


def create_chart(df):
    # aggregate by borough + developer + year
    chart_df = (
        df.groupby(["borough", "developer", "year"], as_index=False)["amount"]
        .sum()
    )

    # then sum again at borough + developer level
    # this keeps the logic consistent with the selected filters
    chart_df = (
        chart_df.groupby(["borough", "developer"], as_index=False)["amount"]
        .sum()
    )

    # sort so highest funding developer is first within each borough
    chart_df = chart_df.sort_values(
        ["borough", "amount"],
        ascending=[True, False]
    )

    # pick top 1 developer per borough
    chart_df = chart_df.groupby("borough", as_index=False).head(1)

    # sort for horizontal bar readability
    chart_df = chart_df.sort_values("amount", ascending=True)

    fig = px.bar(
        chart_df,
        x="amount",
        y="borough",
        color="developer",
        orientation="h",
        title="Top Developer by Borough",
        labels={
            "amount": "Funding Amount",
            "borough": "Borough",
            "developer": "Developer",
        },
        hover_data={
            "developer": True,
            "amount": ":,.0f",
        },
    )

    fig.update_layout(
        xaxis_title="Funding Amount",
        yaxis_title="Borough",
        legend_title="Developer",
    )

    fig.update_xaxes(tickformat=",.0s")

    return fig