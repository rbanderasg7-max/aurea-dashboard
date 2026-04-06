import streamlit as st
import yfinance as yf

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
            df = yf.download(ticker, period="1d", interval="1m")
            change = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100
            data[name] = float(round(change, 2))
        except:
            data[name] = None

    return data


def generate_signals(data):
    signals = {}

    def safe_signal(value, reverse=False):
        try:
            if value is None:
                return "NEUTRAL"
            value = float(value)
            if reverse:
                return "SHORT" if value < 0 else "LONG"
            else:
                return "LONG" if value > 0 else "SHORT"
        except:
            return "NEUTRAL"

    signals['S&P 500'] = safe_signal(data.get('S&P 500'))
    signals['Nasdaq'] = safe_signal(data.get('Nasdaq'))
    signals['USD/MXN'] = safe_signal(data.get('USD/MXN'), reverse=True)
    signals['Oro'] = safe_signal(data.get('Oro'))

    return signals


def main():
    st.title("AUREA CAPITAL - Market Intelligence")

    data = get_market_data()
    signals = generate_signals(data)

    st.subheader("Resumen")

    for asset in data:
        st.write(f"{asset}: {data[asset]}% → {signals[asset]}")


if __name__ == "__main__":
    main()
