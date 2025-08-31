import requests
import time
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

data = []
URL_NAME = "https://api.github.com"

layout = html.Div(
    [
        html.H1("Page Three"),
        dcc.Dropdown(
            id="page3-dropdown",
            value="x",
            options=[
                {"label": "Inactive Graph", "value": "x"},
                {"label": "Active Graph", "value": "y"},
            ],
            style={"maxWidth": 300},
        ),
    dcc.Interval(id="tick", interval=300000, n_intervals=0),
    dcc.Graph(id="page3-output")
    ]  
) 

def ping_website(url):
        response = requests.get(url)
        elapsed = response.elapsed.total_seconds()
        status = response.status_code
        data.append({"time": elapsed, "status": status})

@callback(
    Output("page3-output", "figure"),
    Input("page3-dropdown", "value"),
    Input("tick", "n_intervals")
)
def render_page(dropdown_value, n_intervals):
    if dropdown_value == "x":
        print("No Graph here, yet")
        df_empty = pd.DataFrame({"time_empty": [], "status_empty": []})
        fig = px.line(
            df_empty,
            x="status_empty", 
            y="time_empty",
            title="Inactive",
            labels={
                    "time_empty": "Response Time",
                    "status_empty": "Amount of Pings"
                    }
        )
        return fig
    
    else:
        ping_website(URL_NAME)
        fig = px.line(
            data,
            y="time",
            markers=True,
            title="Pinging "+URL_NAME+".",
            custom_data=["status"],
            labels={
                     "time": "Response Time",
                    }     
            )
        
        fig.update_traces(
            hovertemplate="Status: %{customdata[0]}"
        )

        fig.update_layout(
            xaxis_title="Amount of Pings", yaxis_title="Response Time"
        )
        return fig