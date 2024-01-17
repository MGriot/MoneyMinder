import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go


# barchart tempo vs money
def plot_barchart(filtered_df, colors, saldo=True):
    # Dividi il dataframe in transazioni positive e negative
    positive_df = filtered_df[filtered_df["Import"] >= 0]
    negative_df = filtered_df[filtered_df["Import"] < 0]

    # Crea il grafico a barre
    fig = go.Figure(
        data=[
            go.Bar(
                x=positive_df["Date"],
                y=positive_df["Import"],
                marker_color=colors["positive"],
                name="Input",
            ),
            go.Bar(
                x=negative_df["Date"],
                y=negative_df["Import"],
                marker_color=colors["negative"],
                name="Output",
            ),
        ]
    )

    # Aggiungi lo stato del saldo del conto
    if saldo == True:
        fig.add_trace(
            go.Scatter(
                x=filtered_df["Date"],
                y=filtered_df["Balance"],
                mode="lines",
                marker_color="black",
                name="Balance",
            )
        )
    # Imposta il modo di visualizzazione delle barre
    fig.update_layout(barmode="relative")

    fig.update_yaxes(title_text="Import (€)")
    fig.update_xaxes(
        tickformat="%d-%m-%Y",  # Set tick format to day-month-year
    )
    return fig


def in_out(df):
    # Seleziona le righe con importi negativi/negativi
    df_negative = df[df["Import"] < 0]
    df_positive = df[df["Import"] > 0]
    # Calcola la somma degli importi negativi e positivi
    sum_negative = df_negative["Import"].sum()
    sum_positive = df_positive["Import"].sum()

    # Crea il bar chart
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Incoming", "Outcoming"],
            y=[sum_positive, -sum_negative],
            marker_color=["green", "red"],
        )
    )

    # Aggiungi il titolo al grafico
    fig.update_layout(title="Confronto tra entrate e uscite")
    return fig


def plot_linechart(df, start_date, end_date):
    # Calcola il saldo del conto dopo ogni transazione
    df["Balance"] = df["Import"].cumsum()

    # Filtra il dataframe per la finestra temporale specificata
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    # Crea il grafico a linee
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Balance"],
            mode="lines",
            name="Balance",
        )
    )

    fig.update_yaxes(title_text="Balance (€)")
    return fig


def plot_categories(df, start_date, end_date, colors):
    # Filtra il dataframe per la finestra temporale specificata
    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    # Escludi la categoria 'Stipendi e pensioni'
    df = df[df["Category"] != "Stipendi e pensioni"]

    # Supponendo che 'df' sia il tuo DataFrame e che 'Costo' e 'Categoria' siano le colonne
    df_sum = df.groupby("Category")["Import"].sum().reset_index()

    # Crea il bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=df_sum["Category"],
                y=df_sum["Import"],
                marker_color=[colors[cat] for cat in df_sum["Category"]],
            )
        ]
    )

    fig.update_layout(title_text="Costo per Categoria")

    return fig
