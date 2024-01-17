import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

import datetime
import os
import json


def create_settings_file(file_path, data_file_path):
    if not os.path.exists(file_path):
        settings = {"data_file_path": data_file_path}
        with open(file_path, "w") as f:
            json.dump(settings, f)


def load_data(file_path):
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["Import"] = df["Import"].astype("float")
    return df


def process_data(file_path, source, name, save):
    """
    Questa funzione processa un file di dati Excel e restituisce un DataFrame pandas.
    Parametri:
    - file_path (str): Il percorso del file Excel da processare.
    - source (str): La fonte dei dati.
    - name (str): Il nome della banca.
    Ritorna:
    - df (DataFrame): Il DataFrame processato.
    La funzione esegue le seguenti operazioni solo se source è "bank" e name è "san_paolo":
    1. Carica il file Excel in un DataFrame pandas.
    2. Rimuove le prime righe fino alla prima cella non vuota nella prima colonna.
    3. Imposta la prima riga come nuova intestazione del DataFrame.
    4. Rimuove la prima riga dal DataFrame.
    5. Rinomina gli indici del DataFrame con i valori della nuova intestazione.
    6. Resetta gli indici del DataFrame.
    7. Converte la colonna "Data" in formato datetime.
    8. Rinomina la colonna 'Categoria' in 'Categoria banca'.
    9. Aggiunge le nuove colonne 'Categoria', 'Subcategoria' e 'Commento', inizialmente impostate su None.
    """
    if source == "bank" and name == "san_paolo":
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
        # Rinomina le colonne
        df = df.rename(
            columns={
                "Data": "Date",
                "Categoria ": "Bank Category",
                "Operazione": "Operation",
                "Dettagli": "Details",
                "Conto o carta": "Account or Card",
                "Contabilizzazione": "Accounting",
                "Valuta": "Valute",
                "Importo": "Import",
            }
        )
        # Converte la colonna "Data" in formato datetime
        df["Date"] = pd.to_datetime(df["Date"])
        # Aggiungi le nuove colonne 'Categoria', 'Subcategoria' e 'Commento'
        df[["Category", "Subcategory", "Comment"]] = None, None, None
        # Converti le colonne 'Categoria', 'Subcategoria' e 'Commento' in formato stringa
        df[["Category", "Subcategory", "Comment"]] = df[
            ["Category", "Subcategory", "Comment"]
        ].astype("str")
        if save == True:
            today = datetime.datetime.now()
            df.to_csv(
                f'C:/Users/Admin/Documents/GitHub/MoneyMinder/data/dataframe_{today.strftime("%Y%m%d_%H%M%S")}.csv',
                index=False,
            )
        else:
            return df


def merge_and_sort(df1, df2, columns, save):
    """
    Unisce due DataFrame, rimuove i duplicati basandosi su specifiche colonne, converte la colonna "Data" in formato datetime, rimuove le righe con valori mancanti o non validi nella colonna "Data" e ordina il DataFrame in base alla colonna "Data".

    Parametri:
    df1 (pandas.DataFrame): Primo DataFrame da unire.
    df2 (pandas.DataFrame): Secondo DataFrame da unire.
    columns (list): Lista di colonne su cui basare la rimozione dei duplicati.

    Restituisce:
    df (pandas.DataFrame): DataFrame risultante dopo l'unione, la rimozione dei duplicati, la conversione della colonna "Data" in datetime, la rimozione delle righe con valori mancanti o non validi nella colonna "Data" e l'ordinamento in base alla colonna "Data".
    """
    # Unisci i due DataFrame
    df2 = process_data(df2, "bank", "san_paolo", save=False)
    df = pd.concat([df1, df2], keys=["df1", "df2"])

    # Converte la colonna "Data" in formato datetime
    df["Data"] = pd.to_datetime(df["Date"], errors="coerce")

    # Rimuovi i duplicati basandoti su specifiche colonne, mantenendo la prima occorrenza (quella da df1)
    df = df.loc[~df.duplicated(subset=columns, keep="first")]

    # Ordina il DataFrame in base alla colonna "Data"
    df = df.sort_values("Data")

    # Resetta l'indice
    df = df.reset_index(drop=True)

    if save == True:
        today = datetime.datetime.now()
        df.to_csv(
            f'C:/Users/Admin/Documents/GitHub/Banca/data/dataframe_{today.strftime("%Y%m%d_%H%M%S")}.csv',
            index=False,
        )
    else:
        return df


def categorize_transactions(
    dataframe_path,
    description_columns,
    training_columns,
    label_columns,
    transaction_column,
    confidence_threshold=0.7,
):
    """
    Questa funzione categorizza le transazioni in un dataframe.

    Parametri:
    - dataframe_path (str): Il percorso del file CSV che contiene il dataframe.
    - description_columns (list of str): Una lista di colonne da concatenare per formare la descrizione.
    - training_columns (list of str): Una lista di colonne su cui eseguire il drop delle righe con valori NaN.
    - label_columns (list of str): Una lista di colonne per formare l'etichetta.
    - transaction_column (str): La colonna per le nuove transazioni.
    - confidence_threshold (float, optional): La soglia di confidenza per la categorizzazione. Il valore predefinito è 0.7.

    Ritorna:
    - df_completo (DataFrame): Il DataFrame completo con le categorie predette.
    """
    df = pd.read_csv(dataframe_path)
    df["Descrizione"] = df[description_columns].apply(
        lambda row: " - ".join(row.values.astype(str)), axis=1
    )
    df_training = df.dropna(subset=training_columns)
    df_nan = df[df[label_columns[0]].isna() | df[label_columns[1]].isna()]
    df_training["Etichetta"] = df_training[label_columns].apply(
        lambda row: " - ".join(row.values.astype(str)), axis=1
    )
    transazioni = df_training["Descrizione"].tolist()
    categorie = df_training["Etichetta"].tolist()

    encoder = LabelEncoder()
    y = encoder.fit_transform(categorie)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(transazioni)

    model = MultinomialNB()
    model.fit(X, y)

    nuove_transazioni = df_nan[transaction_column].tolist()
    X_nuovo = vectorizer.transform(nuove_transazioni)

    probabilita_predizioni = model.predict_proba(X_nuovo)
    categorie_predette = []

    for probabilita in probabilita_predizioni:
        if max(probabilita) > confidence_threshold:
            categorie_predette.append(
                encoder.inverse_transform([probabilita.argmax()])[0]
            )
        else:
            categorie_predette.append(np.nan)

    df_nan["Etichetta_predetta"] = categorie_predette

    df_completo = pd.concat([df.reset_index(drop=True), df_nan.reset_index(drop=True)])

    df_completo["Etichetta_predetta"] = df_completo["Etichetta_predetta"].replace(
        np.nan, "", regex=True
    )
    df_completo[["Categoria_temp", "Subcategoria_temp"]] = df_completo[
        "Etichetta_predetta"
    ].str.split(" - ", expand=True)

    df_completo[label_columns[0]] = df_completo[label_columns[0]].where(
        df_completo["Etichetta_predetta"] == "", df_completo["Categoria_temp"]
    )
    df_completo[label_columns[1]] = df_completo[label_columns[1]].where(
        df_completo["Etichetta_predetta"] == "", df_completo["Subcategoria_temp"]
    )

    df_completo = df_completo.drop(["Categoria_temp", "Subcategoria_temp"], axis=1)
    # Supponendo che 'Data' sia la colonna che contiene le date
    df_completo = df_completo.sort_values("Data")
    # Resetta l'indice del DataFrame
    df_completo = df_completo.reset_index(drop=True)

    today = datetime.date.today()
    df_completo.to_csv(
        f'C:/Users/Admin/Documents/GitHub/Banca/data/dataframe_{today.strftime("%Y%m%d")}_{today.strftime("%Y%m%d")}.csv',
        index=False,
    )

    # return df_completo


def date_for_forecast(date, forecast_day=30):
    # Trova la data più grande
    data_max = date.max()

    # Crea un array con le 30 date successive
    date_range = pd.date_range(
        start=data_max, periods=forecast_day + 1, freq=DateOffset(days=1)
    )

    # Converti l'array in UTC
    date_range = date_range.tz_localize("UTC")

    return date_range
