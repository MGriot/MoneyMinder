import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go


# barchart tempo vs money
def plot_barchart(df, colors):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["Data"],
            y=df["Importo"],
            marker_color=df["Importo"].apply(
                lambda x: colors["positive"] if x >= 0 else colors["negative"]
            ),
        )
    )
    fig.update_yaxes(title_text="Importo (€)")
    fig.update_xaxes(
        tickformat="%d-%m-%Y",  # Set tick format to day-month-year
    )
    return fig


def in_out(df):
    # Seleziona le righe con importi negativi/negativi
    df_negative = df[df["Importo"] < 0]
    df_positive = df[df["Importo"] > 0]
    # Calcola la somma degli importi negativi e positivi
    sum_negative = df_negative["Importo"].sum()
    sum_positive = df_positive["Importo"].sum()

    # Crea il bar chart
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Uscite", "Entrate"],
            y=[-sum_negative, sum_positive],
            marker_color=["red", "green"],
        )
    )

    # Aggiungi il titolo al grafico
    fig.update_layout(title="Confronto tra entrate e uscite")
    return fig


def plot_linechart(df, start_date, end_date):
    # Filtra il dataframe per la finestra temporale specificata
    df = df[(df["Data"] >= start_date) & (df["Data"] <= end_date)]

    # Calcola il saldo del conto dopo ogni transazione
    df["Saldo"] = df["Importo"].cumsum()

    # Crea il grafico a linee
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Data"], y=df["Saldo"], mode="lines"))
    fig.update_yaxes(title_text="Saldo (€)")
    return fig


def plot_categories(df, start_date, end_date, colors):
    # Filtra il dataframe per la finestra temporale specificata
    df = df[(df["Data"] >= start_date) & (df["Data"] <= end_date)]
    # Escludi la categoria 'Stipendi e pensioni'
    df = df[df["Categoria"] != "Stipendi e pensioni"]

    # Supponendo che 'df' sia il tuo DataFrame e che 'Costo' e 'Categoria' siano le colonne
    df_sum = df.groupby("Categoria")["Importo"].sum().reset_index()

    # Crea il bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=df_sum["Categoria"],
                y=df_sum["Importo"],
                marker_color=[colors[cat] for cat in df_sum["Categoria"]],
            )
        ]
    )

    fig.update_layout(title_text="Costo per Categoria")

    return fig
