import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime

# -----------------------------
# DATA ENGINE
# -----------------------------
def get_market_data():
    tickers = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI",
        "DAX": "^GDAXI",
        "Nikkei": "^N225",
        "Oro": "GC=F",
        "WTI": "CL=F",
        "Bitcoin": "BTC-USD",
        "USD/MXN": "MXN=X"
    }

    data = {}
    for name, ticker in tickers.items():
        df = yf.download(ticker, period="2d", interval="1d", progress=False)

        if len(df) >= 2:
            change = (df['Close'].iloc[-1] / df['Close'].iloc[-2] - 1) * 100
            data[name] = round(change, 2)
        else:
            data[name] = 0

    return data

# -----------------------------
# SIGNAL ENGINE
# -----------------------------
def generate_signals(data):
    signals = {}

    signals['S&P 500'] = "LONG" if data['S&P 500'] > 0 else "SHORT"
    signals['Nasdaq'] = "LONG" if data['Nasdaq'] > 0 else "SHORT"
    signals['USD/MXN'] = "SHORT" if data['USD/MXN'] < 0 else "LONG"
    signals['Oro'] = "LONG" if data['Oro'] > 0 else "NEUTRAL"

    return signals

# -----------------------------
# NARRATIVE ENGINE
# -----------------------------
def generate_narrative(data):
    if data['S&P 500'] > 0 and data['Nasdaq'] > 0:
        return "Risk-On: apetito por riesgo impulsa mercados globales."
    else:
        return "Entorno mixto con cautela en mercados globales."

# -----------------------------
# DASHBOARD
# -----------------------------
def main():
    st.set_page_config(page_title="AUREA Dashboard", layout="wide")

    st.title("AUREA CAPITAL - Market Intelligence")

    data = get_market_data()
    signals = generate_signals(data)
    narrative = generate_narrative(data)

    st.subheader("🧠 Resumen")
    st.write(narrative)

    st.subheader("📊 Mercados")
    cols = st.columns(3)

    for i, (k, v) in enumerate(data.items()):
        cols[i % 3].metric(label=k, value=f"{v}%")

    st.subheader("🎯 Señales")

    for k, v in signals.items():
        if v == "LONG":
            st.success(f"{k}: {v}")
        elif v == "SHORT":
            st.error(f"{k}: {v}")
        else:
            st.warning(f"{k}: {v}")

    st.subheader("🕒 Última actualización")
    st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()