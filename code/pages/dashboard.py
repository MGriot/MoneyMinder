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
from datetime import date, timedelta


from moduls.graph import plot_barchart, in_out, plot_linechart, plot_categories
from moduls.colors import colors_in_out, colors_categories
import moduls.globals as globals

df = globals.df


# Converti la colonna 'Data' in formato datetime
df["Data"] = pd.to_datetime(df["Data"])
df["Data"].fillna(pd.NaT, inplace=True)

# Converti la colonna 'Importo' in numeri
df["Importo"] = pd.to_numeric(df["Importo"], errors="coerce")
# Calcola i totali
total = df["Importo"].sum()
total_positive = df[df["Importo"] > 0]["Importo"].sum()
total_negative = df[df["Importo"] < 0]["Importo"].sum()

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
                        "Data"
                    ].min()  # Calcola la data un mese prima della data massima
                    - timedelta(days=30),
                    max_date_allowed=df["Data"].max(),
                    initial_visible_month=date.today(),
                    start_date=df["Data"].max() - timedelta(days=30),
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
    filtered_df = df[(df["Data"] >= start_date) & (df["Data"] <= end_date)]
    return [
        plot_barchart(filtered_df, colors=colors),
        in_out(filtered_df),
        plot_linechart(df, start_date, end_date),
        plot_categories(df, start_date, end_date, colors=colors_categories),
    ]
