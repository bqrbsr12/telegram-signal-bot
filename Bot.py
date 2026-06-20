import ccxt
import pandas as pd
import time
import os
from telegram import Bot

# 🔐 Environment variables from Render
TOKEN = os.getenv("8833264285:AAGKR-aPL72h9PjhkDlOxS2G_JVgzJlCXN0
")
CHAT_ID = os.getenv("8833264285")

bot = Bot(token=8833264285:AAGKR-aPL72h9PjhkDlOxS2G_JVgzJlCXN0)

exchange = ccxt.binance()

symbol = "BTC/USDT"
timeframe = "15m"

def get_data():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=50)
    df = pd.DataFrame(ohlcv, columns=["t","o","h","l","c","v"])
    return df

def signal(df):
    df["ma"] = df["c"].rolling(10).mean()
    last = df.iloc[-1]

    if last["c"] > last["ma"]:
        return "BUY"
    elif last["c"] < last["ma"]:
        return "SELL"
    return None

while True:
    try:
        df = get_data()
        s = signal(df)

        if s:
            price = df.iloc[-1]["c"]
            bot.send_message(chat_id=CHAT_ID, text=f"BTC SIGNAL: {s} @ {price}")

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
