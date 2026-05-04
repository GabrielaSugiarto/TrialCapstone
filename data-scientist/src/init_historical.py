import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

LQ45_TICKERS = [
    "AADI.JK","ADMR.JK","ADRO.JK","AKRA.JK","AMMN.JK",
    "AMRT.JK","ANTM.JK","ASII.JK","BBCA.JK","BBNI.JK",
    "BBRI.JK","BBTN.JK","BMRI.JK","BRPT.JK","BUMI.JK",
    "CPIN.JK","CUAN.JK","DEWA.JK","EMTK.JK","ESSA.JK",
    "EXCL.JK","GOTO.JK","HRTA.JK","ICBP.JK","INCO.JK",
    "INDF.JK","INKP.JK","ISAT.JK","ITMG.JK","JPFA.JK",
    "KLBF.JK","MAPI.JK","MBMA.JK","MDKA.JK","MEDC.JK",
    "PGAS.JK","PGEO.JK","PTBA.JK","SCMA.JK","SMGR.JK",
    "TLKM.JK","TOWR.JK","UNTR.JK","UNVR.JK","WIFI.JK",
]

START_DATE = "2020-01-01"
END_DATE   = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "lq45_historical.csv")

def init():
    print(f"Fetching data dari {START_DATE} sampai hari ini...")
    all_close = {}

    for ticker_str in LQ45_TICKERS:
        try:
            hist = yf.Ticker(ticker_str).history(
                start=START_DATE, end=END_DATE, auto_adjust=True
            )

            if hist.empty:
                print(f"  ⚠  {ticker_str}: kosong")
                continue

            hist.index = hist.index.tz_localize(None)
            all_close[ticker_str.replace('.JK', '')] = hist['Close']

            print(f"  ✓  {ticker_str:8s} ({len(hist)} hari)")

        except Exception as e:
            print(f"  ✗  {ticker_str}: {e}")

    df = pd.DataFrame(all_close)
    df.index.name = 'Date'
    df = df.reset_index()

    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    # 🔥 tambahan penting
    df = df.sort_values("Date").reset_index(drop=True)

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(CSV_PATH, index=False)

    print(f"\n✓ Selesai!")
    print(f"Saved: {CSV_PATH}")

if __name__ == "__main__":
    init()
