import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback

layout = html.Div(
    [
        html.H1("Page One"),
        dcc.Dropdown(
            id="page1-dropdown",
            value="x",
            options=[
                {"label": "Graph Nr. 1", "value": "x"},
                {"label": "Graph Nr. 2", "value": "y"},
            ],
            style={"maxWidth": 300},
        ),
     html.Div(id="page1-output")
    ]  
)   

@callback(
    Output("page1-output", "children"),
    Input("page1-dropdown", "value")
)
def render_page(dropdown_value):
    df = pd.DataFrame(dict(
            x_data = [3, 5, 1, 4, 6, 2],
            y_data = [44, 32, 9, 81, 33, 55]
        )) 
    if dropdown_value == "x":
            fig1 = px.line(df, x="x_data", y="y_data", title="Unsorted")
    else:
            fig1 = px.line(df.sort_values("x_data"), x="x_data", y="y_data", title="Sorted")
    return html.Div([dcc.Graph(figure=fig1)])