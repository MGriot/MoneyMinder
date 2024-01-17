import dash
from dash import Dash, html, dcc, dash_table, State, callback
from dash.dependencies import Output, Input, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
from datetime import date, timedelta, datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

from moduls.function import date_for_forecast
from moduls.graph import plot_barchart, in_out, plot_linechart, plot_categories
from moduls.colors import colors_in_out, colors_categories
import moduls.globals as globals

df = globals.df

# days = globals.dates = df["Date"]

# Calcola i totali
total = globals.total = df["Import"].sum()
total_positive = globals.total_positive = df[df["Import"] > 0]["Import"].sum()
total_negative = globals.total_negative = df[df["Import"] < 0]["Import"].sum()


dash.register_page(__name__)

layout = html.Div(
    [
        html.Div(
            children=[
                dbc.Button(
                    f"Patrimonio: {round(total,2)}",
                    color="primary",
                    style={
                        "fontSize": 20,
                        "textAlign": "center",
                        "marginRight": "10px",
                    },
                ),
                dbc.Button(
                    f"Parziale positivo: {round(total_positive,2)}",
                    color="primary",
                    style={
                        "fontSize": 20,
                        "textAlign": "center",
                        "marginRight": "10px",
                    },
                ),
                dbc.Button(
                    f"Parziale negativo: {round(total_negative,2)}",
                    color="primary",
                    style={
                        "fontSize": 20,
                        "textAlign": "center",
                        "marginRight": "10px",
                    },
                ),
            ]
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id="my-date-picker-range",
                    min_date_allowed=df[
                        "Date"
                    ].min()  # Calcola la data un mese prima della data massima
                    - timedelta(days=30),
                    max_date_allowed=df["Date"].max(),
                    initial_visible_month=date.today(),
                    start_date=df["Date"].max() - timedelta(days=30),
                    end_date=date.today(),
                    display_format="DD/MM/YY",  # Set the date format to day-month-year
                ),
                ### GRAFICI
                html.Div(
                    [
                        html.Div(  # prima riga
                            [
                                dcc.Graph(id="barchart"),
                            ],
                            style={"width": "70%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="barchart_in_out"),
                            ],
                            style={
                                "width": "30%",
                                "float": "right",
                                "display": "inline-block",
                            },
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Div(  # prima riga
                            [
                                dcc.Graph(id="plot_linechart"),
                            ],
                            style={"width": "70%", "display": "inline-block"},
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Div(  # prima riga
                            [
                                dcc.Graph(id="plot_categories"),
                            ],
                            style={"width": "30%", "display": "inline-block"},
                        ),
                    ],
                ),
            ]
        ),
    ]
)


# Aggiungi una callback per aggiornare il grafico quando un pulsante del mese o il selettore dell'anno viene cliccato
@callback(
    [
        Output("barchart", "figure"),
        Output("barchart_in_out", "figure"),
        Output("plot_linechart", "figure"),
        Output("plot_categories", "figure"),
    ],
    [
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_graph(
    start_date,
    end_date,
    colors=colors_in_out,
    colors_categories=colors_categories,
):
    df["Balance"] = df["Import"].cumsum()
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    return [
        plot_barchart(filtered_df, colors=colors),
        in_out(filtered_df),
        plot_linechart(df, start_date, end_date),
        plot_categories(df, start_date, end_date, colors=colors_categories),
    ]
