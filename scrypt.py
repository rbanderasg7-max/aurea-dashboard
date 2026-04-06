import streamlit as st
import yfinance as yf
import numpy as np

# -----------------------------
# DATOS DE MERCADO
# -----------------------------
def get_market_data():
    assets = {
        'S&P 500': '^GSPC',
        'Nasdaq': '^IXIC',
        'USD/MXN': 'MXN=X',
        'Oro': 'GC=F'
    }

    data = {}

    for name, ticker in assets.items():
        try:
            df = yf.download(ticker, period="5d", interval="1h")
            returns = df['Close'].pct_change().dropna()

            momentum = returns.mean() * 100
            volatility = returns.std() * 100

            data[name] = {
                "momentum": float(round(momentum, 2)),
                "volatility": float(round(volatility, 2))
            }
        except:
            data[name] = {
                "momentum": None,
                "volatility": None
            }

    return data

# -----------------------------
# MODELO DE SEÑALES
# -----------------------------
def generate_signals(data):
    signals = {}

    for asset, values in data.items():
        m = values["momentum"]
        v = values["volatility"]

        if m is None:
            signals[asset] = {"signal": "NEUTRAL", "score": 0}
            continue

        score = 0

        # Momentum
        if m > 0:
            score += 1
        else:
            score -= 1

        # Volatilidad (riesgo)
        if v is not None:
            if v > 1:
                score -= 1
            else:
                score += 1

        # Clasificación
        if score >= 2:
            signal = "FUERTE ALCISTA"
        elif score == 1:
            signal = "ALCISTA"
        elif score == 0:
            signal = "NEUTRAL"
        elif score == -1:
            signal = "BAJISTA"
        else:
            signal = "FUERTE BAJISTA"

        signals[asset] = {
            "signal": signal,
            "score": score
        }

    return signals

# -----------------------------
# RÉGIMEN DE MERCADO
# -----------------------------
def market_regime(signals):
    score_total = sum([s["score"] for s in signals.values()])

    if score_total >= 3:
        return "🟢 RISK ON (Entorno favorable para activos de riesgo)"
    elif score_total <= -3:
        return "🔴 RISK OFF (Entorno defensivo)"
    else:
        return "🟡 NEUTRAL (Mercado mixto)"

# -----------------------------
# INTERFAZ
# -----------------------------
def main():
    st.set_page_config(page_title="AUREA CAPITAL", layout="wide")

    st.title("AUREA CAPITAL - Inteligencia de Mercado")

    data = get_market_data()
    signals = generate_signals(data)
    regime = market_regime(signals)

    st.subheader("📊 Resumen de Mercado")
    st.markdown(f"**Régimen actual:** {regime}")

    st.divider()

    cols = st.columns(4)

    for i, asset in enumerate(data.keys()):
        with cols[i]:
            st.metric(
                label=asset,
                value=signals[asset]["signal"],
                delta=f"Score: {signals[asset]['score']}"
            )

    st.divider()

    st.subheader("📈 Detalle Cuantitativo")

    for asset in data:
        st.write(f"**{asset}**")
        st.write(f"Momentum: {data[asset]['momentum']}%")
        st.write(f"Volatilidad: {data[asset]['volatility']}%")
        st.write(f"Señal: {signals[asset]['signal']}")
        st.write("---")

# -----------------------------
if __name__ == "__main__":
    main()
