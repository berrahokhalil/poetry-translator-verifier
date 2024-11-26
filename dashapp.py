from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 1, 2, 5],
    "City": ["SF", "SF", "NYC", "NYC"]
})

# Initialize Dash app
app = Dash(__name__)

# Layout definition
app.layout = html.Div([
    html.H1("Fruit Sales Dashboard"),  # Title
    dcc.Dropdown(
        id="city-dropdown",
        options=[
            {"label": city, "value": city} for city in df["City"].unique()
        ],
        value="SF",  # Default value
        placeholder="Select a City"
    ),
    dcc.Graph(id="bar-chart"),  # Placeholder for the graph
])

# Callback to update the graph based on dropdown selection
@app.callback(
    Output("bar-chart", "figure"),
    Input("city-dropdown", "value")
)
def update_chart(selected_city):
    filtered_df = df[df["City"] == selected_city]
    fig = px.bar(filtered_df, x="Fruit", y="Amount", title=f"Fruit Sales in {selected_city}")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
