import plotly.express as px


def create_chart(df):
    chart_df = df.dropna(subset=["latitude", "longitude", "amount"]).copy()

    color_map = {
        "4%": "#F8766D",
        "9%": "#A3A500",
    }

    fig = px.scatter_mapbox(
        chart_df,
        lat="latitude",
        lon="longitude",
        color="credit_type",
        color_discrete_map=color_map,
        size="amount",
        size_max=12,
        hover_name="project_name",
        hover_data={
            "borough": True,
            "developer": True,
            "year": True,
            "amount": ":,.0f",
            "latitude": False,
            "longitude": False,
        },
        zoom=10.9,
        center={"lat": 40.73, "lon": -73.93},
        mapbox_style="carto-positron",
        title="NYC LIHTC Project Sites",
    )

    fig.update_layout(
        height=620,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend_title="Credit Type",
    )

    return fig