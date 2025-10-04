import requests
import time
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

data = []
URL_NAME = "https://api.github.com"

layout = html.Div(
    [
        html.H1("GitHub Pinging Graph"),
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
    dcc.Graph(id="page3-output"),
    dcc.Graph(id="page3-output-2")
    ]  
) 

def ping_website(url):
        response = requests.get(url)
        elapsed = response.elapsed.total_seconds()
        status = response.status_code
        data.append({"time": elapsed, 
                     "status": status,
                     "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                     })

@callback(
    Output("page3-output", "figure"),
    Output("page3-output-2", "figure"),
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
            title="Pinging "+URL_NAME+". (Inactive)",
            labels={
                    "time_empty": "Response Time",
                    "status_empty": "Timestamp"
                    }
        )

        fig2 = px.line(
            df_empty,
            x="status_empty",
            y="time_empty",
            title="Is the Website Up or Down? (Inactive)",
            labels={
                    "time_empty": "Response Time",
                    "status_empty": "Timestamp"
                    }
        )

        return fig, fig2
    
    else:

        ping_website(URL_NAME)

        df = pd.DataFrame(data)
        df["status_group"] = df["status"].apply(lambda s: 1 if s == 200 else 0)

        # ping graph

        fig = px.line(
            df,
            y="time",
            x="date",
            markers=True,
            title="Pinging "+URL_NAME+".",
            custom_data=["status", "date"],
            labels={
                     "time": "Response Time",
                    }     
            )

        # up or down graph
    
        fig2 = px.line(
        df,
        y="status_group",
        x="date",
        markers=True,
        title="Is the Website Up or Down?",
        custom_data=["status", "date"],
        labels={"status_group": "Status"}
)

        # ping graph updates

        fig.update_traces(
            hovertemplate="Response Time: %{y} seconds<br>Status Code: %{customdata[0]}<br>Timestamp: %{customdata[1]}"
        )

        fig.update_layout(
            xaxis_title="Timestamp", 
            yaxis_title="Response Time"
        )

        fig.update_xaxes(
            tickformat="%Y-%m-%d %H:%M:%S",
            type="category"
        )
         
        # up or down graph updates

        fig2.update_traces(
            hovertemplate="Status: %{y}<br>Status Code: %{customdata[0]}<br>Timestamp: %{customdata[1]}"
        )

        fig2.update_layout(
            xaxis_title="Timestamp", 
            yaxis_title="Status"
        )

        fig2.update_xaxes(
            tickformat="%Y-%m-%d %H:%M:%S",  # No milliseconds, check this later if i understand whats happening
            type="category"
        )

        fig2.update_yaxes(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Down", "Up"]   # CHECK THIS LATER !!!!!!!!!!!!!!
        )

        return fig, fig2