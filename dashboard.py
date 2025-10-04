from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import homepage, pageone, pagetwo, pagethree


app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

SIDEBAR_STYLE = {
    "position": "fixed", 
    "top": 0, 
    "left": 0, 
    "bottom": 0,
    "width": "12em", 
    "padding": "2rem 1rem",
    "backgroundColor": "#2b2b2b", 
    "color": "#cfcfcf",
    "fontSize": "23px", 
    "boxShadow": "5px 5px 5px 5px lightgrey"
}
CONTENT_STYLE = {"marginLeft": "18rem", 
                 "marginRight": "2rem", 
                 "padding": "2rem 1rem"}

sidebar = html.Div(
    [
        html.H2("Sidebar yippee", className="display-4"),
        html.Hr(),
        html.P("Dash Plotly Project", className="lead"),
        html.P("Lea Lassok", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Graph Sorting", href="/page-1", active="exact"),
                dbc.NavLink("Image Editing", href="/page-2", active="exact"),
                dbc.NavLink("Pinging Graph", href="/page-3", active="exact"),
            ],
            vertical=True, pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)


content = html.Div([html.Div(id="page-content")], style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return homepage.layout

    elif pathname == "/page-1":
        return pageone.layout
    
    elif pathname == "/page-2":
        return pagetwo.layout
    
    elif pathname == "/page-3":
        return pagethree.layout

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3"
    )


if __name__ == "__main__":
    app.run(debug=True)