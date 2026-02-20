import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime

# --- AYARLAR ---
TOKEN = "8533861311:AAEYYkqxEbe1VZ_gfHW5Liu6ubkRK5h18c8"
CHAT_ID = "6667602222"
HISSELER = ["XU100.IS", "THYAO.IS", "EREGL.IS", "TUPRS.IS", "KCHOL.IS", "AKBNK.IS", "GARAN.IS", "SASA.IS", "ASELS.IS", "BTC-USD", "ETH-USD"]

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}, timeout=20)
    except:
        pass

def tarama_yap():
    simdi = datetime.now().strftime('%H:%M:%S')
    print(f"🔍 Tarama Basladi: {simdi}")
    for sembol in HISSELER:
        try:
            df = yf.download(sembol, period="1mo", interval="1h", progress=False)
            if df.empty: continue
            
            df_2h = df.resample('2h').agg({'Open':'first','High':'max','Low':'min','Close':'last'}).dropna()
            
            ema20 = ta.ema(df_2h['Close'], length=20)
            ema50 = ta.ema(df_2h['Close'], length=50)
            rsi = ta.rsi(df_2h['Close'], length=14)

            if (ema20.iloc[-2] <= ema50.iloc[-2] and ema20.iloc[-1] > ema50.iloc[-1]) and rsi.iloc[-1] > 30:
                mesaj = f"🚀 **{sembol} AL SINYALI**\nFiyat: {df_2h['Close'].iloc[-1]:.2f}\nRSI: {rsi.iloc[-1]:.2f}\nFurkan Barkin icin pusu tuttu!"
                telegram_gonder(mesaj)
        except:
            continue

if __name__ == "__main__":
    telegram_gonder("🤖 Robot Render'da aktif! Pusu basladi.")
    while True:
        tarama_yap()
        time.sleep(7200)
