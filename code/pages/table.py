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

from moduls.function import categorize_transactions
import moduls.globals as globals

# Definisci i tuoi array
categorie = ["casa", "stipendio"]
subcategorie = ["corrente", "stipendio"]

df = globals.df

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
                    id="upload-button", children=html.Button("Load"), multiple=False
                ),
                html.Button("Categorize", id="categorize-button"),
            ]
        ),
        dash_table.DataTable(
            id="table",
            columns=[
                {"id": "Data", "name": "Data", "type": "datetime"},
                {"id": "Operazione", "name": "Operazione"},
                {"id": "Dettagli", "name": "Dettagli"},
                {"id": "Conto o carta", "name": "Conto o carta"},
                {"id": "Contabilizzazione", "name": "Contabilizzazione"},
                {"id": "Categoria banca", "name": "Categoria banca"},
                {"id": "Valuta", "name": "Valuta"},
                {"id": "Importo", "name": "Importo", "type": "text"},
                {
                    "id": "Categoria",
                    "name": "Categoria",
                    "presentation": "dropdown",
                    "type": "text",
                },
                {
                    "id": "Subcategoria",
                    "name": "Subcategoria",
                    "presentation": "dropdown",
                    "type": "text",
                },
                {"id": "Commento", "name": "Commento"},
            ],
            data=df.to_dict("records"),
            editable=True,
            dropdown={
                "Categoria": {
                    "options": [{"label": str(i), "value": str(i)} for i in categorie],
                },
                "Subcategoria": {
                    "options": [
                        {"label": str(i), "value": str(i)} for i in subcategorie
                    ],
                },
            },
        ),
        html.Div(id="table-dropdown-container"),
    ]
)


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
