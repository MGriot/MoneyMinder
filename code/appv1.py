import dash
from dash import Dash, html, dcc, dash_table, State
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import date, timedelta

app = Dash(__name__, suppress_callback_exceptions=True)
file = "C:/Users/Admin/Documents/GitHub/Banca/data/dataframev.csv"

dropdown_category = {
    "Abitazione": [
        "Mutuo o affitto",
        "Tasse sulla proprietà",
        "Riparazioni domestiche",
        "Spese condominiali",
        "Assicurazione casa",
    ],
    "Trasporti": [
        "Pagamento dell'auto",
        "Garanzia auto",
        "Carburante",
        "Pneumatici",
        "Manutenzione e cambio olio",
        "Tariffe di parcheggio",
        "Riparazioni auto",
        "Tasse di registrazione e DMV",
        "Assicurazione auto",
        "Trasporto pubblico (bus, treno, metro, ecc.)",
        "Pedaggi e Telepass",
    ],
    "Alimentazione": ["Spesa alimentare", "Ristoranti", "Cibo per animali domestici"],
    "Utenze": [
        "Elettricità",
        "Acqua",
        "Rifiuti",
        "Telefonia",
        "TV via cavo",
        "Internet",
        "Banca",
    ],
    "Abbigliamento": [
        "Abbigliamento per adulti",
        "Scarpe per adulti",
        "Abbigliamento per bambini",
        "Scarpe per bambini",
    ],
    "Sanità": [
        "Assistenza primaria",
        "Assistenza dentale",
        "Assistenza specialistica (dermatologi, ortodontisti, oculisti, ecc.)",
        "Assistenza urgente",
        "Farmaci",
        "Dispositivi medici",
        "Assicurazione sanitaria",
    ],
    "Articoli e forniture per la casa": [
        "Articoli da toeletta",
        "Detersivo per il bucato",
        "Detersivo per lavastoviglie",
        "Prodotti per la pulizia",
        "Utensili",
    ],
    "Personale": [
        "Abbonamenti palestra",
        "Tagli di capelli",
        "Servizi di salone",
        "Cosmetici (come trucco o servizi come la depilazione laser)",
        "Baby sitter",
        "Abbonamenti (riviste, servizi online, ecc.)",
    ],
    "Debiti": ["Prestiti personali", "Prestiti studenteschi", "Carte di debito"],
    "Pagementi esterni": ["PayPal", "Satispay"],
    "Pensionamento": ["Pianificazione finanziaria", "Investimenti"],
    "Istruzione": [
        "College dei figli",
        "Tuo college",
        "Forniture scolastiche",
        "Libri",
    ],
    "Risparmi": [
        "Fondo di emergenza",
        "Grandi acquisti come un nuovo materasso o laptop",
        "Altri risparmi",
    ],
    "Regali/Donazioni": [
        "Compleanni",
        "Anniversari",
        "Matrimoni",
        "Natale",
        "Occasioni speciali",
        "Beneficenza",
    ],
    "Intrattenimento": [
        "Alcol e/o bar",
        "Giochi",
        "Cinema",
        "Concerti",
        "Vacanze",
        "Abbonamenti (Netflix, Amazon, Hulu, ecc.)",
    ],
    "Stipendi e pensioni": ["Stipendio", "Pensione", "Investimento", "Entrate varie"],
}


df = pd.read_csv(file)
colors = {"positive": "#00FF00", "negative": "#FF0000"}

# Converti la colonna 'Data' in formato datetime
df["Data"] = pd.to_datetime(df["Data"])
df["Data"].fillna(pd.NaT, inplace=True)

# Converti la colonna 'Importo' in numeri
df["Importo"] = pd.to_numeric(df["Importo"], errors="coerce")
# Calcola i totali
total = df["Importo"].sum()
total_positive = df[df["Importo"] > 0]["Importo"].sum()
total_negative = df[df["Importo"] < 0]["Importo"].sum()

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

index_page = html.Div(
    [
        html.H1("DashBoard - Personal Financial", style={"textAlign": "center"}),
        html.Div(
            [
                dcc.Link("Dashboard", href="/"),
                html.Span(" | "),
                dcc.Link("Dati", href="/page-1"),
            ],
            style={"textAlign": "center"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        f"Patrimonio: {total}",
                        color="primary",
                        style={"fontSize": 20, "textAlign": "center"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        f"Parziale positivo: {total_positive}",
                        color="primary",
                        style={"fontSize": 20, "textAlign": "center"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        f"Parziale negativo: {total_negative}",
                        color="primary",
                        style={"fontSize": 20, "textAlign": "center"},
                    ),
                    width=4,
                ),
            ],
            justify="center",
        ),
        dcc.DatePickerRange(
            id="my-date-picker-range",
            min_date_allowed=df[
                "Data"
            ].max()  # Calcola la data un mese prima della data massima
            - timedelta(days=30),
            max_date_allowed=df["Data"].max(),
            initial_visible_month=date.today(),
            start_date=df["Data"].max() - timedelta(days=30),
            end_date=date.today(),
        ),
        html.Div(
            [
                html.Div(  # prima riga
                    [
                        dcc.Graph(id="barchart_total"),
                    ],
                    style={"width": "70%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Graph(id="barchart_sum"),
                    ],
                    style={"width": "30%", "float": "right", "display": "inline-block"},
                ),
            ],
        ),
        html.Div(  # seconda riga
            [
                html.Div(  # prima riga
                    [
                        dcc.Graph(id="fig_spese_categorie_barchart"),
                    ],
                    style={"width": "30%", "display": "inline-block"},
                ),
                html.Div(  # prima riga
                    [
                        dcc.Graph(id="fig_cumulative"),
                    ],
                    style={"width": "70%", "display": "inline-block"},
                ),
            ],
        ),
    ]
)

page_1_layout = html.Div(
    [
        html.H1("Tabella dei Dati", style={"textAlign": "center"}),
        html.Button("Save", id="save-button"),
        html.Button("Reload", id="reload-button"),
        html.Button("Load", id="upload-button"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Trascina o ", html.A("Seleziona File")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        html.Div(id="output-data-upload"),
        html.Div(
            [
                dcc.Link("Dashboard", href="/"),
                html.Span(" | "),
                dcc.Link("Dati", href="/page-1"),
            ],
            style={"textAlign": "center"},
        ),
        dash_table.DataTable(
            id="table",
            columns=[
                {"name": i, "id": i, "presentation": "dropdown"} for i in df.columns
            ],
            data=df.to_dict("records"),
            editable=True,
            dropdown={
                "Categoria": {
                    "options": [
                        {"label": k, "value": k} for k in dropdown_category.keys()
                    ]
                },
                "Subcategoria": {
                    "options": [
                        {"label": i, "value": i}
                        for i in sum(dropdown_category.values(), [])
                    ]
                },
            },
        ),
    ]
)


@app.callback(Output("table", "dropdown"), Input("table", "dropdown_category"))
def update_subcategoria_dropdown(rows):
    if rows is None or len(rows) == 0:
        raise dash.exceptions.PreventUpdate()

    categoria = rows[-1]["Categoria"]
    return {
        "Categoria": {
            "options": [{"label": k, "value": k} for k in dropdown_category.keys()]
        },
        "Subcategoria": {
            "options": [
                {"label": i, "value": i} for i in dropdown_category.get(categoria, [])
            ]
        },
    }


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/page-1":
        return page_1_layout
    else:
        return index_page


@app.callback(Output("table", "data"), Input("reload-button", "n_clicks"))
def reload_data(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        df = pd.read_csv(file)
        return df.to_dict("records")
    return dash.no_update


@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
@app.callback(
    [
        Output("barchart_total", "figure"),
        Output("barchart_sum", "figure"),
        Output("fig_spese_categorie_barchart", "figure"),
    ],
    [
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_graph(start_date, end_date):
    filtered_df = df[(df["Data"] >= start_date) & (df["Data"] <= end_date)]
    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(
            x=filtered_df["Data"],
            y=filtered_df["Importo"],
            marker_color=filtered_df["Importo"].apply(
                lambda x: colors["positive"] if x >= 0 else colors["negative"]
            ),
        )
    )
    fig1.update_yaxes(title_text="Importo (€)")

    # Seleziona le righe con importi negativi/negativi
    df_negative = filtered_df[filtered_df["Importo"] < 0]
    df_positive = filtered_df[filtered_df["Importo"] > 0]
    # Calcola la somma degli importi negativi e positivi
    sum_negative = df_negative["Importo"].sum()
    sum_positive = df_positive["Importo"].sum()

    # Crea il bar chart
    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(
            x=["Uscite", "Entrate"],
            y=[-sum_negative, sum_positive],
            marker_color=["red", "green"],
        )
    )

    # Aggiungi il titolo al grafico
    fig2.update_layout(title="Confronto tra entrate e uscite")

    # barchart spese x Categorie
    spese_per_categoria = (
        df_negative.groupby("Categoria")["Importo"].sum().sort_values()
    )

    # Crea il grafico a barre
    fig_spese_categorie_barchart = go.Figure(
        go.Bar(
            x=-spese_per_categoria.values,
            y=spese_per_categoria.index,
            orientation="h",
        )
    )
    fig_spese_categorie_barchart.update_layout(
        title="Confronto tra le principali categorie"
    )
    # Crea un grafico separato per la somma cumulativa
    # filtered_df = df[(df["Data"] >= start_date) & (df["Data"] <= end_date)]

    # Calcola la somma cumulativa dei valori
    # filtered_df["Cumulative"] = np.cumsum(filtered_df["Importo"])
    # fig_cumulative = go.Figure()
    # fig_cumulative.add_trace(
    # go.Scatter(
    # x=filtered_df["Data"],
    # y=filtered_df["Cumulative"],
    # mode="lines",
    # name="Cumulative",
    # )
    # )
    # fig_cumulative.update_yaxes(title_text="Cumulative (€)")

    return fig1, fig2, fig_spese_categorie_barchart  # , fig_cumulative


def save_data(n_clicks, rows):
    if n_clicks is not None and n_clicks > 0:
        df = pd.DataFrame(rows)
        df.to_csv(file, index=False)
    return n_clicks


def process_data(file_path):
    # Carica il file xlsx in un DataFrame
    df = pd.read_excel(file_path)
    # Rimuovi le prime righe fino alla prima cella vuota nella prima colonna
    df = df[df.iloc[:, 0].notna()]
    # Imposta la prima riga come nuova intestazione
    new_header = df.iloc[0]
    # Rimuovi la prima riga dal DataFrame
    df = df[1:]
    # Rinomina gli indici del DataFrame con i valori della nuova intestazione
    df = df.rename(columns=new_header)
    # Resetta gli indici del DataFrame
    df = df.reset_index(drop=True)
    # Converte la colonna "Data" in formato datetime
    df["Data"] = pd.to_datetime(df["Data"])
    # Rinomina la colonna 'Categoria' in 'Categoria banca'
    df = df.rename(columns={"Categoria ": "Categoria banca"})
    # Aggiungi le nuove colonne 'Categoria' e 'Subcategoria'
    df["Categoria"] = None
    df["Subcategoria"] = None
    df["Commento"] = None

    return df


def merge_and_sort(df1, df2):
    # Unisci i due DataFrame
    df = pd.concat([df1, df2])

    # Rimuovi i duplicati
    df = df.drop_duplicates()
    # Converte la colonna "Data" in formato datetime
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    # Rimuove le righe con valori mancanti o non validi nella colonna "Data"
    # df = df.dropna(subset=["Data"])
    df["Data"].fillna(pd.NaT, inplace=True)

    # Ordina il DataFrame in base alla colonna "Data"
    df = df.sort_values("Data")

    return df


def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "xls" in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
                df = process_data(df)
                df = merge_and_sort(df, df)
                df.to_csv("../data/dataframev.csv", index=False)
                df = pd.read_csv("../data/dataframev.csv")
                return html.Div(
                    [
                        "File caricato con successo!",
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in df.columns],
                        ),
                    ]
                )
        except Exception as e:
            return html.Div(["C'è stato un errore nel processamento del file."])
    return html.Div(["Nessun file caricato."])


if __name__ == "__main__":
    app.run_server(debug=True)
