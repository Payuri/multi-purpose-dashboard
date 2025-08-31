import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback

layout = html.Div(
    [
        html.H1("Page Two"),
        dcc.Dropdown(
            id="page2-dropdown",
            value="x",
            options=[
                {"label": "Graph Nr. 1", "value": "x"},
                {"label": "Graph Nr. 2", "value": "y"},
            ],
            style={"maxWidth": 300},
        ),
     html.Div(id="page2-output")
    ]  
) 

@callback(
    Output("page2-output", "children"),
    Input("page2-dropdown", "value")
)
def render_page(dropdown_value):
    df2 = pd.DataFrame(dict(
            x_data = [3, 7, 9, 2, 1, 5, 4, 6, 8],
            y_data = [51, 45, 32, 75, 14, 96, 82, 27, 68]
        ))
    if dropdown_value == "x":
            fig2 = px.line(df2, x="x_data", y="y_data", title="Unsorted")
    else:
            fig2 = px.line(df2.sort_values("x_data"), x="x_data", y="y_data", title="Sorted")
    return html.Div([dcc.Graph(figure=fig2)])