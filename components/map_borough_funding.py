import plotly.express as px


def create_chart(df):
    chart_df = (
        df.groupby("borough", as_index=False)["amount"]
        .sum()
    )

    borough_coords = {
        "Bronx": (40.8448, -73.8648),
        "Brooklyn": (40.6782, -73.9442),
        "Manhattan": (40.7831, -73.9712),
        "Queens": (40.7282, -73.7949),
        "Staten Island": (40.5795, -74.1502),
    }

    chart_df["latitude"] = chart_df["borough"].map(lambda x: borough_coords[x][0])
    chart_df["longitude"] = chart_df["borough"].map(lambda x: borough_coords[x][1])

    fig = px.scatter_mapbox(
        chart_df,
        lat="latitude",
        lon="longitude",
        size="amount",
        color="borough",
        hover_name="borough",
        hover_data={"amount": ":,.0f"},
        zoom=10.3,
        center={"lat": 40.73, "lon": -73.93},
        mapbox_style="carto-positron",   # gray map
        title="Funding by Borough Map",
    )

    fig.update_layout(
        height=620,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend_title="Borough",
    )

    return fig