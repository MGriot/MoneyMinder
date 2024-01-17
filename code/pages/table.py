global df

import dash
from dash import Dash, html, dcc, dash_table, State, callback
from dash.dependencies import Output, Input, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import io

from moduls.function import categorize_transactions, load_data
import moduls.globals as globals

# Definisci i tuoi array
categorie = ["casa", "stipendio"]
subcategorie = ["corrente", "stipendio"]

df = globals.df

# Aggiorna i tipi di dati delle colonne
df["Category"] = df["Category"].astype("category")
df["Subcategory"] = df["Subcategory"].astype("category")


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

dash.register_page(__name__)

layout = html.Div(
    [
        html.Div(
            children=[
                html.Button("Save", id="save-button"),
                html.Button("Reload", id="reload-button"),
                dcc.Upload(
                    id="upload-button",
                    children=html.Button("Load"),
                    multiple=False,
                ),
                html.Button("Categorize", id="categorize-button"),
            ]
        ),
        dash_table.DataTable(
            id="table",
            data=df.to_dict("records"),
            editable=True,
            dropdown={
                "Category": {
                    "options": [{"label": i, "value": i} for i in categorie],
                },
                "Subcategory": {
                    "options": [{"label": i, "value": i} for i in subcategorie],
                },
            },
        ),
        html.Div(id="table-dropdown-container"),
    ]
)


@callback(
    Output("table", "data"),
    Input("upload-button", "contents"),
)
def update_table(contents):
    if contents is not None:
        # Recupera i contenuti del file caricato
        print(io.StringIO(contents))
        data = load_data(io.StringIO(contents))

        # Aggiorna il dataframe globale
        globals.df = data

        # Riempie la tabella con i nuovi dati
        return globals.df.to_dict("records")


# CallBack per i pulsanti della pagina con la tabella
# Modifica la tua callback per impostare 'confirm' su 'displayed' quando il pulsante viene premuto
@callback(
    Output("confirm", "displayed"),
    Input("categorize-button", "n_clicks"),
    State("table", "data"),
)
def update_output(n_clicks, rows):
    if n_clicks is not None:
        # Aggiorna il percorso del file CSV e le altre variabili secondo le tue esigenze
        dataframe_path = "C:/Users/Admin/Documents/GitHub/Banca/data/dataframe.csv"
        description_columns = ["Operazione", "Dettagli", "Categoria banca"]
        training_columns = ["Categoria", "Subcategoria"]
        label_columns = ["Categoria", "Subcategoria"]
        transaction_column = "Dettagli"
        confidence_threshold = 0.7

        categorize_transactions(
            dataframe_path,
            description_columns,
            training_columns,
            label_columns,
            transaction_column,
            confidence_threshold,
        )
    # Mostra il pop-up
    return True


# Aggiungi questo componente alla tua app
confirm = dcc.ConfirmDialog(
    id="confirm",
    message="Il processo di categorizzazione è in atto.",
)
