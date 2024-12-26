import requests
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# ThingSpeak API URL
API_URL = "https://api.thingspeak.com/channels/1596152/feeds.json?results=10"

# Field Names
FIELD_NAMES = [
    "PM2.5",
    "PM10",
    "Ozone",
    "Humidity",
    "Temperature",
    "CO"
]

# Layout of the dashboard
app.layout = html.Div([
    html.H1("ThingSpeak Dashboard", style={
        "textAlign": "center",
        "marginBottom": "20px",
        "fontSize": "32px",
        "color": "#333"
    }),
    html.Div([
        dcc.Graph(id=f'graph-{i}') for i in range(1, 7)
    ], style={
        "display": "flex",
        "flexDirection": "column",
        "gap": "20px",
        "padding": "20px"
    }),
    dcc.Interval(
        id='interval-component',
        interval=15000,  # Update every 15 seconds
        n_intervals=0
    )
])

# Callback to update all graphs
@app.callback(
    [Output(f'graph-{i}', 'figure') for i in range(1, 7)],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    try:
        # Fetch data from the ThingSpeak API
        response = requests.get(API_URL)
        data = response.json()

        # Extract timestamps and fields
        feeds = data['feeds']
        timestamps = [feed['created_at'] for feed in feeds]
        fields = [[feed[f'field{i + 1}'] for feed in feeds] for i in range(6)]

        # Create figures for each field
        figures = []
        for i in range(6):
            figures.append(go.Figure(
                data=go.Scatter(
                    x=timestamps,
                    y=fields[i],
                    mode='lines+markers',
                    name=FIELD_NAMES[i]
                ),
                layout=go.Layout(
                    title=FIELD_NAMES[i],
                    xaxis_title="Timestamp",
                    yaxis_title="Value",
                    template="plotly_dark"
                )
            ))
        return figures

    except Exception as e:
        print(f"Error fetching or parsing data: {e}")
        return [go.Figure()] * 6

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
