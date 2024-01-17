import dash
from dash import Dash, html, dcc, dash_table, State
from dash.dependencies import Output, Input, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
from datetime import date, timedelta


from moduls.function import create_settings_file, load_data
import moduls.globals as globals

settings_file_path = "C:/Users/Admin/Documents/GitHub/MoneyMinder/data/settings.json"
file = "C:/Users/Admin/Documents/GitHub/MoneyMinder/data/dataframe_20231226_111609.csv"

create_settings_file(settings_file_path, file)
globals.df = load_data(file)

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    pages_folder="pages",
)

dash.register_page(__name__, path="/")

app.layout = html.Div(
    [
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
