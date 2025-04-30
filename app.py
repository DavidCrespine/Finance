import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Titre de l'application
st.title("Suivi Quotidien de Mes Titres Financiers")

# Liste des symboles boursiers (modifiable par l'utilisateur)
st.sidebar.header("Configuration")
tickers_input = st.sidebar.text_input("Entrez vos symboles boursiers (séparés par des virgules)", "AAPL,MSFT,GOOGL")
tickers = [t.strip() for t in tickers_input.split(",")]

# Date pour les données
today = datetime.today()
yesterday = today - timedelta(days=1)

# Fonction pour récupérer les données
def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            # Récupérer les données du dernier jour
            hist = stock.history(period="1d", start=yesterday, end=today)
            if not hist.empty:
                last_price = hist["Close"].iloc[-1]
                prev_price = hist["Open"].iloc[0]
                change = ((last_price - prev_price) / prev_price) * 100
                data.append({
                    "Symbole": ticker,
                    "Prix Actuel": round(last_price, 2),
                    "Variation (%)": round(change, 2),
                    "Volume": hist["Volume"].iloc[-1]
                })
            else:
                data.append({
                    "Symbole": ticker,
                    "Prix Actuel": "N/A",
                    "Variation (%)": "N/A",
                    "Volume": "N/A"
                })
        except Exception as e:
            data.append({
                "Symbole": ticker,
                "Prix Actuel": "Erreur",
                "Variation (%)": "Erreur",
                "Volume": "Erreur"
            })
    return pd.DataFrame(data)

# Afficher les données
if tickers:
    st.write("### Données Quotidiennes")
    df = get_stock_data(tickers)
    st.dataframe(df)

# Instructions pour l'utilisateur
st.sidebar.markdown("""
### Instructions :
1. Entrez les symboles boursiers (ex. AAPL pour Apple, MSFT pour Microsoft).
2. Les données sont mises à jour quotidiennement via yfinance.
3. Déployez sur Streamlit Community Cloud pour un accès en ligne.
""")
