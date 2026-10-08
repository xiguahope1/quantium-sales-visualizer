import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
df = pd.read_csv("processed_data/combined_pink_morsels_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Performance", style={"textAlign": "center"}),
    html.P("Analyze sales tracking trends around the January 15, 2021 price adjustments.", style={"textAlign": "center"}),
    
    html.Div([
        html.Label("Filter Visualization by Region: ", style={"fontWeight": "bold"}),
        dcc.RadioItems(
            id="region-filter",
            options=[{"label": f" {r.capitalize()}", "value": r} for r in ["all", "north", "east", "south", "west"]],
            value="all",
            inline=True
        )
    ], style={"margin": "20px auto", "maxWidth": "800px"}),
    
    dcc.Graph(id="sales-line-chart")
], style={"fontFamily": "sans-serif", "padding": "20px"})

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    filtered_df = df if selected_region == "all" else df[df["region"].str.lower() == selected_region.lower()]
    daily_sales = filtered_df.groupby("date")["sales"].sum().reset_index()
    
    fig = px.line(daily_sales, x="date", y="sales", title=f"Daily Revenue - {selected_region.upper()}")
    fig.update_layout(xaxis_title="Date", yaxis_title="Total Revenue ($)", title_x=0.5)
    
    fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="red",
                  annotation_text="Price Adjustment (Jan 15, 2021)", annotation_position="top left")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
